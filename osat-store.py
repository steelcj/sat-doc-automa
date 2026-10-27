#!/usr/bin/env python3
#
# source
#   project: sat-doc-automa
#   path: osat-store.py
#
"""
osat-store.py, the shared artifact store for OSAT managers and their tests:
inspect it, verify it, add to it, and carry it to another machine as a seed.

The store keeps every artifact a manager or test obtains from outside the
machine once, named by its SHA-256, beside a PROVENANCE record, per
proposal--offline-testing-for-osat-managers. Release-metadata responses and
other URL-keyed text, whose content is what changes, are kept separately as
lookups. This script never uses the network; filling the store from the
network is each manager's job, and OSAT_NETWORK has nothing to forbid here.

Layout, format 1:

    STORE                                format: 1
    blobs/<aa>/<sha256>/<asset>          the artifact, under its own name
    blobs/<aa>/<sha256>/PROVENANCE       manager, asset, sha256, source,
                                         installed, size, verified-against,
                                         fetched, and via when imported
    lookups/<sha256 of url>.body         a response body
    lookups/<sha256 of url>.meta         url, sha256, fetched, etag

A seed is a store directory plus SHA256SUMS over every file in it. Its
narrowest backend is a plain directory (gold--interfaces-stay-honest-to-
the-narrowest-backend), so a USB stick, a virtual machine's shared folder
or a copied directory is a complete transport, and a seed can also be used
directly as a read-only store by pointing OSAT_STORE at it.

Store location: --store DIR, else OSAT_STORE, else %LOCALAPPDATA%\\osat-store
on Windows, else $XDG_DATA_HOME/osat-store (default ~/.local/share/osat-store).

Usage:
    osat-store.py --status                       artifacts, lookups, sizes, ages
    osat-store.py --verify                       re-hash everything; exit 1 on any fault
    osat-store.py --path SHA256                  print a verified artifact's path
    osat-store.py --add FILE --source URL [--sha256 HASH] [--asset NAME]
                  [--verified-against REF] [--manager NAME]
    osat-store.py --export DIR [--select FILE]   write a seed
    osat-store.py --import DIR                   verify a seed, then merge it

Select file, one rule per line, blank lines and # comments ignored:
    asset   <glob on the asset name>
    sha256  <full hash>
    lookup  <glob on the lookup URL>

Refusals: running as root or Administrator; a store whose format is newer
than this script; a store directory broader than owner-only; an artifact
whose content does not match the hash it was given; exporting into a
non-empty directory; any seed fault, checked in full before anything is
merged: no SHA256SUMS, a listed file missing or different, an unlisted file,
a symbolic link, an unsafe path, a blob not named by its own hash, a
PROVENANCE or lookup record disagreeing with its file. In sandbox mode
(OSAT_STORE_SANDBOX set), refuses to touch the default store location.
"""
import argparse
import fnmatch
import hashlib
import os
import re
import shutil
import stat
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterator, List, Mapping, Optional, Tuple

TOOL = "osat-store"
TOOL_VERSION = "0.1.0"
STORE_FORMAT = 1
STORE_DIR_NAME = "osat-store"
SANDBOX_VAR = "OSAT_STORE_SANDBOX"

POSIX_MODES = os.name != "nt"
DIR_MODE = 0o700
FILE_MODE = 0o600

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PROVENANCE_KEYS = ("manager", "asset", "sha256", "source", "installed",
                   "size", "verified-against", "fetched")
LOOKUP_KEYS = ("url", "sha256", "fetched", "etag")
SEED_SUMS = "SHA256SUMS"


class StoreError(RuntimeError):
    """A refusal or fault, reported to the operator as one message."""


# ── Small helpers ───────────────────────────────────────────────────────────

def log(message: str) -> None:
    print(f"[{TOOL}] {message}", file=sys.stderr)


def utc_timestamp(now: Optional[datetime] = None) -> str:
    moment = now or datetime.now(timezone.utc)
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_timestamp(text: str) -> Optional[datetime]:
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1000 or unit == "GB":
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1000
    return f"{size} B"


def age_of(timestamp: str, now: Optional[datetime] = None) -> str:
    moment = parse_timestamp(timestamp)
    if moment is None:
        return "unknown age"
    seconds = int(((now or datetime.now(timezone.utc)) - moment).total_seconds())
    if seconds < 3600:
        return f"{max(seconds, 0) // 60} min"
    if seconds < 172800:
        return f"{seconds // 3600} h"
    return f"{seconds // 86400} d"


def parse_record(text: str) -> Dict[str, str]:
    """`key: value` pairs, as manage-python reads PROVENANCE. Unknown keys are
    kept for the caller to ignore; for a repeated key the first value wins;
    lines without a colon are skipped."""
    fields: Dict[str, str] = {}
    for line in text.lstrip("﻿").splitlines():
        key, sep, value = line.partition(":")
        key = key.strip()
        if not sep or not key or key in fields:
            continue
        fields[key] = value.strip()
    return fields


def render_record(fields: Mapping[str, str], keys: Tuple[str, ...]) -> str:
    """Known keys in their fixed order, then any extra keys in sorted order.
    Empty values are omitted; values may not span lines."""
    order = list(keys) + sorted(k for k in fields if k not in keys)
    lines = []
    for key in order:
        value = fields.get(key, "")
        if not value:
            continue
        if any(ch in value for ch in "\r\n"):
            raise StoreError(f"record value for {key} spans lines")
        lines.append(f"{key}: {value}\n")
    return "".join(lines)


def check_asset_name(name: str) -> None:
    if (not name or name in (".", "..", "PROVENANCE") or "/" in name or "\\" in name
            or any(ord(ch) < 32 for ch in name)):
        raise StoreError(f"{name!r} is not a usable asset file name")


def refuse_privileged() -> None:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        raise StoreError("the store belongs to your account; do not run this with sudo")
    if os.name == "nt":
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin():  # type: ignore[attr-defined]
                raise StoreError("the store belongs to your profile; do not run this as Administrator")
        except (AttributeError, OSError):
            pass


# ── Location ────────────────────────────────────────────────────────────────

def default_store(environ: Mapping[str, str] = os.environ) -> Path:
    """The store location when neither --store nor OSAT_STORE is given."""
    if os.name == "nt":
        local = environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(local) / STORE_DIR_NAME
    data = environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(data) / STORE_DIR_NAME


def real_default_store() -> Path:
    """The default location for this account, from the system rather than
    from HOME or XDG_DATA_HOME, which a test overrides."""
    if os.name == "nt":
        return default_store({})
    import pwd
    return Path(pwd.getpwuid(os.getuid()).pw_dir) / ".local" / "share" / STORE_DIR_NAME


def resolve_store(option: Optional[str], environ: Mapping[str, str] = os.environ) -> Path:
    if option:
        return Path(option).expanduser()
    if environ.get("OSAT_STORE"):
        return Path(environ["OSAT_STORE"]).expanduser()
    return default_store(environ)


def _inside(path: Path, root: Path) -> bool:
    target = os.path.normcase(os.path.realpath(str(path)))
    base = os.path.normcase(os.path.realpath(str(root)))
    return target == base or target.startswith(base.rstrip(os.sep) + os.sep)


# ── The store ───────────────────────────────────────────────────────────────

class Store:
    """One store directory. Reading never creates anything; the first write
    creates the layout with owner-only permissions."""

    def __init__(self, root: Path, environ: Mapping[str, str] = os.environ,
                 owner_only: bool = True):
        self.root = Path(root)
        # A seed on removable media may sit on a filesystem without POSIX
        # permissions, so only a store is held to owner-only.
        self.owner_only = owner_only and POSIX_MODES
        self.blobs = self.root / "blobs"
        self.lookups = self.root / "lookups"
        self.environ = environ

    # ── format and permissions ──

    def format(self) -> Optional[int]:
        """The layout format, None for a directory that is not yet a store."""
        marker = self.root / "STORE"
        if not marker.is_file():
            return None
        value = parse_record(marker.read_text(encoding="utf-8")).get("format", "")
        if not value.isdigit():
            raise StoreError(f"{marker} does not state a format")
        return int(value)

    def check_readable(self) -> None:
        found = self.format()
        if found is not None and found > STORE_FORMAT:
            raise StoreError(f"{self.root} is store format {found}; this script reads "
                             f"format {STORE_FORMAT}. Use a newer osat-store.py")

    def guard(self) -> None:
        if self.environ.get(SANDBOX_VAR) and _inside(self.root, real_default_store()):
            raise StoreError(f"sandbox mode: refusing to change {self.root}, the real "
                             f"store location for this account")

    def ensure_writable(self) -> None:
        """Create the layout if needed, and refuse a newer format or a
        directory broader than owner-only."""
        self.guard()
        self.check_readable()
        for directory in (self.root, self.blobs, self.lookups):
            created = not directory.exists()
            directory.mkdir(parents=True, exist_ok=True)
            if not self.owner_only:
                continue
            if created:
                directory.chmod(DIR_MODE)
            elif stat.S_IMODE(directory.stat().st_mode) & 0o077:
                raise StoreError(f"{directory} has permissions "
                                 f"{oct(stat.S_IMODE(directory.stat().st_mode))}, broader "
                                 f"than the owner-only {oct(DIR_MODE)} this collection "
                                 f"requires; fix the permissions and rerun")
        if self.format() is None:
            write_file(self.root / "STORE", f"format: {STORE_FORMAT}\n".encode(),
                       self.owner_only)

    # ── blobs ──

    def blob_dir(self, sha256: str) -> Path:
        return self.blobs / sha256[:2] / sha256

    def iter_blobs(self) -> Iterator[Path]:
        if not self.blobs.is_dir():
            return
        for shard in sorted(self.blobs.iterdir()):
            if shard.name.startswith(".") or not shard.is_dir():
                continue
            for entry in sorted(shard.iterdir()):
                if entry.is_dir():
                    yield entry

    def blob_asset(self, directory: Path) -> Path:
        """The one artifact file in a blob directory."""
        files = [p for p in directory.iterdir() if p.name != "PROVENANCE"]
        if len(files) != 1:
            raise StoreError(f"{directory} holds {len(files)} artifact files, not one")
        if files[0].is_symlink() or not files[0].is_file():
            raise StoreError(f"{files[0]} is not a regular file")
        return files[0]

    def check_blob(self, directory: Path) -> Tuple[Path, Dict[str, str]]:
        """Re-hash one blob and check it against its name and record."""
        name = directory.name
        if not SHA256_RE.match(name) or directory.parent.name != name[:2]:
            raise StoreError(f"{directory} is not named by a SHA-256 in its shard")
        asset = self.blob_asset(directory)
        record_path = directory / "PROVENANCE"
        if not record_path.is_file():
            raise StoreError(f"{directory} has no PROVENANCE")
        record = parse_record(record_path.read_text(encoding="utf-8"))
        actual = sha256_of(asset)
        if actual != name:
            raise StoreError(f"{asset} has SHA-256 {actual}, not {name}")
        if record.get("sha256") != name:
            raise StoreError(f"{record_path} records sha256 {record.get('sha256')!r}, not {name}")
        if record.get("asset") != asset.name:
            raise StoreError(f"{record_path} records asset {record.get('asset')!r}, "
                             f"not {asset.name!r}")
        return asset, record

    def path_of(self, sha256: str) -> Optional[Path]:
        """A verified artifact's path, or None when the store does not hold it."""
        sha256 = sha256.lower()
        if not SHA256_RE.match(sha256):
            raise StoreError(f"{sha256!r} is not a SHA-256")
        self.check_readable()
        directory = self.blob_dir(sha256)
        if not directory.is_dir():
            return None
        asset, _record = self.check_blob(directory)
        return asset

    def add(self, source_file: Path, *, source: str, asset: Optional[str] = None,
            expected_sha256: Optional[str] = None, verified_against: str = "",
            manager: str = "", fetched: str = "", via: str = "",
            now: Optional[datetime] = None) -> Tuple[Path, bool]:
        """Add a file. Returns its path in the store and whether it was new.
        An artifact already held is verified and kept with its first record."""
        source_file = Path(source_file)
        if source_file.is_symlink() or not source_file.is_file():
            raise StoreError(f"{source_file} is not a regular file")
        name = asset or source_file.name
        check_asset_name(name)
        if not source:
            raise StoreError("an artifact needs a source: the URL it came from, or how "
                             "it reached this machine")
        self.ensure_writable()
        digest = sha256_of(source_file)
        if expected_sha256 and digest != expected_sha256.lower():
            raise StoreError(f"{source_file} has SHA-256 {digest}, not the expected "
                             f"{expected_sha256.lower()}; not added")
        target = self.blob_dir(digest)
        if target.is_dir():
            held, _record = self.check_blob(target)
            return held, False
        stamp = utc_timestamp(now)
        record = {
            "manager": manager or f"{TOOL} {TOOL_VERSION}",
            "asset": name,
            "sha256": digest,
            "source": source,
            "installed": stamp,
            "size": str(source_file.stat().st_size),
            "verified-against": verified_against,
            "fetched": fetched or stamp,
            "via": via,
        }
        staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=str(self.blobs)))
        try:
            shutil.copyfile(source_file, staging / name)
            if self.owner_only:
                (staging / name).chmod(FILE_MODE)
            if sha256_of(staging / name) != digest:
                raise StoreError(f"{source_file} changed while it was being added")
            write_file(staging / "PROVENANCE",
                       render_record(record, PROVENANCE_KEYS).encode("utf-8"), self.owner_only)
            self.make_shard(target.parent)
            try:
                os.rename(staging, target)
            except OSError:
                if not target.is_dir():
                    raise
                held, _record = self.check_blob(target)   # added meanwhile by another run
                return held, False
        finally:
            if staging.exists():
                shutil.rmtree(staging, ignore_errors=True)
        return target / name, True

    def make_shard(self, shard: Path) -> None:
        if not shard.exists():
            shard.mkdir()
            if self.owner_only:
                shard.chmod(DIR_MODE)

    def copy_blob_from(self, source_dir: Path) -> None:
        """Copy a verified blob directory as it is, record included, then
        verify the copy. Used for seeds, where nothing is re-recorded."""
        target = self.blob_dir(source_dir.name)
        self.make_shard(target.parent)
        target.mkdir()
        for item in source_dir.iterdir():
            shutil.copyfile(item, target / item.name)
        self.check_blob(target)

    # ── lookups ──

    def lookup_paths(self, url: str) -> Tuple[Path, Path]:
        key = sha256_text(url)
        return self.lookups / f"{key}.body", self.lookups / f"{key}.meta"

    def iter_lookups(self) -> Iterator[Path]:
        if self.lookups.is_dir():
            yield from sorted(self.lookups.glob("*.meta"))

    def check_lookup(self, meta_path: Path) -> Tuple[bytes, Dict[str, str]]:
        meta = parse_record(meta_path.read_text(encoding="utf-8"))
        url = meta.get("url", "")
        if not url or sha256_text(url) != meta_path.stem:
            raise StoreError(f"{meta_path} is not named by the SHA-256 of its url")
        body_path = meta_path.with_suffix(".body")
        if body_path.is_symlink() or not body_path.is_file():
            raise StoreError(f"{meta_path} has no body file")
        body = body_path.read_bytes()
        if hashlib.sha256(body).hexdigest() != meta.get("sha256"):
            raise StoreError(f"{body_path} does not match the sha256 in {meta_path.name}")
        return body, meta

    def get_lookup(self, url: str) -> Optional[Tuple[bytes, Dict[str, str]]]:
        """A stored response for `url` and its record, or None."""
        self.check_readable()
        _body_path, meta_path = self.lookup_paths(url)
        if not meta_path.is_file():
            return None
        return self.check_lookup(meta_path)

    def put_lookup(self, url: str, body: bytes, *, etag: str = "", fetched: str = "",
                   now: Optional[datetime] = None) -> None:
        """Store or replace the response for `url`. The body is written before
        its record, so a reader never sees a record for a body not yet there."""
        if not url or any(ch in url for ch in "\r\n"):
            raise StoreError("a lookup needs a single-line url")
        self.ensure_writable()
        body_path, meta_path = self.lookup_paths(url)
        meta = {"url": url, "sha256": hashlib.sha256(body).hexdigest(),
                "fetched": fetched or utc_timestamp(now), "etag": etag}
        write_file(body_path, body, self.owner_only)
        write_file(meta_path, render_record(meta, LOOKUP_KEYS).encode("utf-8"), self.owner_only)


def write_file(path: Path, data: bytes, owner_only: bool = True) -> None:
    """Write beside `path` and rename into place, owner-only unless told
    otherwise."""
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if owner_only and POSIX_MODES:
            os.chmod(tmp_name, FILE_MODE)
        os.replace(tmp_name, str(path))
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# ── Commands ────────────────────────────────────────────────────────────────

def command_status(store: Store) -> int:
    store.check_readable()
    if store.format() is None:
        print(f"{store.root}: no store here yet")
        return 0
    now = datetime.now(timezone.utc)
    total = 0
    blobs = list(store.iter_blobs())
    print(f"{store.root} (format {store.format()})")
    print(f"artifacts: {len(blobs)}")
    for directory in blobs:
        record = parse_record((directory / "PROVENANCE").read_text(encoding="utf-8")
                              if (directory / "PROVENANCE").is_file() else "")
        size = int(record.get("size", "0") or 0)
        total += size
        print(f"  {record.get('asset', '?')}  {human_size(size)}  {directory.name[:12]}  "
              f"fetched {age_of(record.get('fetched', ''), now)} ago")
    lookups = list(store.iter_lookups())
    print(f"lookups: {len(lookups)}")
    for meta_path in lookups:
        meta = parse_record(meta_path.read_text(encoding="utf-8"))
        print(f"  {meta.get('url', '?')}  fetched {age_of(meta.get('fetched', ''), now)} ago")
    print(f"total artifact size: {human_size(total)}")
    return 0


def command_verify(store: Store) -> int:
    store.check_readable()
    faults: List[str] = []
    count = 0
    for directory in store.iter_blobs():
        count += 1
        try:
            store.check_blob(directory)
        except StoreError as error:
            faults.append(str(error))
    for meta_path in store.iter_lookups():
        count += 1
        try:
            store.check_lookup(meta_path)
        except StoreError as error:
            faults.append(str(error))
    for fault in faults:
        print(f"FAULT  {fault}")
    log(f"verified {count} entries in {store.root}: "
        f"{'no faults' if not faults else f'{len(faults)} faults'}")
    return 1 if faults else 0


def command_path(store: Store, sha256: str) -> int:
    path = store.path_of(sha256)
    if path is None:
        log(f"{sha256} is not in {store.root}")
        return 1
    print(path)
    return 0


def command_add(store: Store, args: argparse.Namespace) -> int:
    path, new = store.add(Path(args.add), source=args.source, asset=args.asset,
                          expected_sha256=args.sha256,
                          verified_against=args.verified_against or "",
                          manager=args.manager or "")
    log(f"{'added' if new else 'already held'}: {path.name} ({path.parent.name[:12]})")
    print(path)
    return 0


# ── Seeds ───────────────────────────────────────────────────────────────────

def read_selection(path: Path) -> List[Tuple[str, str]]:
    rules = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        kind, _sep, pattern = line.partition(" ")
        pattern = pattern.strip()
        if kind not in ("asset", "sha256", "lookup") or not pattern:
            raise StoreError(f"{path}:{number}: expected 'asset', 'sha256' or 'lookup' "
                             f"and a pattern")
        rules.append((kind, pattern))
    return rules


def selected(rules: Optional[List[Tuple[str, str]]], kind: str, value: str,
             sha256: str = "") -> bool:
    if rules is None:
        return True
    for rule_kind, pattern in rules:
        if rule_kind == kind and fnmatch.fnmatchcase(value, pattern):
            return True
        if kind == "asset" and rule_kind == "sha256" and pattern.lower() == sha256:
            return True
    return False


def seed_files(root: Path) -> List[Path]:
    """Every file under a seed or store, as paths relative to it, refusing
    symbolic links anywhere."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            if Path(dirpath, name).is_symlink():
                raise StoreError(f"{Path(dirpath, name)} is a symbolic link")
        for name in filenames:
            found.append(Path(dirpath, name).relative_to(root))
    return sorted(found, key=lambda p: p.as_posix())


def command_export(store: Store, target: Path, select: Optional[Path]) -> int:
    store.check_readable()
    if store.format() is None:
        raise StoreError(f"{store.root} is not a store")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise StoreError(f"{target} exists and is not an empty directory")
    rules = read_selection(select) if select else None
    seed = Store(target, environ={}, owner_only=False)
    seed.ensure_writable()
    artifacts = lookups = 0
    for directory in store.iter_blobs():
        asset, record = store.check_blob(directory)
        if not selected(rules, "asset", asset.name, directory.name):
            continue
        seed.copy_blob_from(directory)
        artifacts += 1
    for meta_path in store.iter_lookups():
        _body, meta = store.check_lookup(meta_path)
        if not selected(rules, "lookup", meta["url"]):
            continue
        shutil.copyfile(meta_path.with_suffix(".body"), seed.lookups / f"{meta_path.stem}.body")
        shutil.copyfile(meta_path, seed.lookups / meta_path.name)
        lookups += 1
    lines = [f"{sha256_of(target / rel)}  {rel.as_posix()}\n" for rel in seed_files(target)]
    write_file(target / SEED_SUMS, "".join(lines).encode("utf-8"), owner_only=False)
    log(f"seed written to {target}: {artifacts} artifacts, {lookups} lookups")
    return 0


def safe_relative(text: str) -> Path:
    path = Path(text)
    if (not text or text.startswith(("/", "\\")) or path.is_absolute()
            or any(part in ("..", "") for part in Path(text).parts) or ":" in text):
        raise StoreError(f"{SEED_SUMS} lists an unsafe path: {text!r}")
    return path


def check_seed(seed_root: Path) -> Tuple[str, Store]:
    """Verify a seed in full. Returns the SHA-256 of its SHA256SUMS, which
    identifies the seed in imported records."""
    sums_path = seed_root / SEED_SUMS
    if not sums_path.is_file() or sums_path.is_symlink():
        raise StoreError(f"{seed_root} has no {SEED_SUMS}; it is not a seed")
    listed: Dict[str, str] = {}
    for number, line in enumerate(sums_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        digest, sep, name = line.partition("  ")
        if not sep or not SHA256_RE.match(digest):
            raise StoreError(f"{SEED_SUMS} line {number} is not '<sha256>  <path>'")
        listed[safe_relative(name).as_posix()] = digest
    present = {rel.as_posix() for rel in seed_files(seed_root)} - {SEED_SUMS}
    unlisted = sorted(present - set(listed))
    missing = sorted(set(listed) - present)
    if unlisted:
        raise StoreError(f"seed holds files {SEED_SUMS} does not list: {', '.join(unlisted)}")
    if missing:
        raise StoreError(f"seed is missing files {SEED_SUMS} lists: {', '.join(missing)}")
    for name, digest in listed.items():
        if sha256_of(seed_root / name) != digest:
            raise StoreError(f"seed file {name} does not match {SEED_SUMS}")
    seed = Store(seed_root, environ={}, owner_only=False)
    seed.check_readable()
    if seed.format() is None:
        raise StoreError(f"{seed_root} has no STORE file; it is not a seed")
    for name in present:
        top = name.split("/", 1)[0]
        if top not in ("STORE", "blobs", "lookups"):
            raise StoreError(f"seed holds {name}, outside the store layout")
    for directory in seed.iter_blobs():
        seed.check_blob(directory)
    for meta_path in seed.iter_lookups():
        seed.check_lookup(meta_path)
    return sha256_of(sums_path), seed


def command_import(store: Store, seed_root: Path) -> int:
    seed_id, seed = check_seed(seed_root)
    store.ensure_writable()
    added = held = lookups = 0
    for directory in seed.iter_blobs():
        asset, record = seed.check_blob(directory)
        _path, new = store.add(
            asset, source=record.get("source", "") or f"seed {seed_id}",
            asset=asset.name, expected_sha256=directory.name,
            verified_against=record.get("verified-against", ""),
            manager=record.get("manager", ""), fetched=record.get("fetched", ""),
            via=f"seed {seed_id}")
        added += new
        held += not new
    for meta_path in seed.iter_lookups():
        body, meta = seed.check_lookup(meta_path)
        current = store.get_lookup(meta["url"])
        if current is not None:
            ours = parse_timestamp(current[1].get("fetched", ""))
            theirs = parse_timestamp(meta.get("fetched", ""))
            if ours and (theirs is None or theirs <= ours):
                continue
        store.put_lookup(meta["url"], body, etag=meta.get("etag", ""),
                         fetched=meta.get("fetched", ""))
        lookups += 1
    log(f"imported seed {seed_id[:12]} into {store.root}: {added} artifacts added, "
        f"{held} already held, {lookups} lookups added or newer")
    return 0


# ── Entry point ─────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="osat-store.py",
        description="The shared artifact store for OSAT managers and their tests.")
    parser.add_argument("--store", metavar="DIR",
                        help="store directory (default: OSAT_STORE, then the platform default)")
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--status", action="store_true", help="list artifacts and lookups")
    actions.add_argument("--verify", action="store_true", help="re-hash everything")
    actions.add_argument("--path", metavar="SHA256", help="print a verified artifact's path")
    actions.add_argument("--add", metavar="FILE", help="add a file to the store")
    actions.add_argument("--export", metavar="DIR", help="write a seed")
    actions.add_argument("--import", dest="import_dir", metavar="DIR",
                         help="verify a seed, then merge it")
    parser.add_argument("--source", metavar="URL", help="with --add: where the file came from")
    parser.add_argument("--sha256", metavar="HASH", help="with --add: refuse unless the file has this hash")
    parser.add_argument("--asset", metavar="NAME", help="with --add: the name to store it under")
    parser.add_argument("--verified-against", metavar="REF",
                        help="with --add: the checksum file or pinned hash it was checked against")
    parser.add_argument("--manager", metavar="NAME", help="with --add: the manager adding it")
    parser.add_argument("--select", metavar="FILE", help="with --export: which entries to export")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.add and not args.source:
        parser.error("--add needs --source")
    if args.select and not args.export:
        parser.error("--select goes with --export")
    try:
        refuse_privileged()
        store = Store(resolve_store(args.store))
        if args.status:
            return command_status(store)
        if args.verify:
            return command_verify(store)
        if args.path:
            return command_path(store, args.path)
        if args.add:
            return command_add(store, args)
        if args.export:
            return command_export(store, Path(args.export).expanduser(),
                                  Path(args.select) if args.select else None)
        return command_import(store, Path(args.import_dir).expanduser())
    except StoreError as error:
        print(f"[{TOOL} ERROR] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
