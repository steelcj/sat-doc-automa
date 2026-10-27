#!/usr/bin/env python3
#
# source
#   project: sat-doc-automa
#   path: test_osat_store.py
#
"""
test_osat_store.py, offline unit tests for osat-store.py.

Every test works in a scratch directory with OSAT_STORE_SANDBOX set, so the
account's real store is never touched, and nothing uses the network.

Usage:
    python3 test_osat_store.py [-v]
"""
import contextlib
import hashlib
import importlib.util
import io
import os
import stat
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent / "osat-store.py"
_spec = importlib.util.spec_from_file_location("osat_store", SCRIPT)
osat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(osat)

POSIX = os.name != "nt"
URL = "https://github.com/example/project/releases/download/v1.0.0/tool-1.0.0.tar.gz"
API = "https://api.github.com/repos/example/project/releases/latest"
NOW = datetime(2026, 10, 4, 18, 0, 0, tzinfo=timezone.utc)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Scratch(unittest.TestCase):
    """A scratch area with a store, an incoming directory and a seed path."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.env = {osat.SANDBOX_VAR: "1"}
        self.store = osat.Store(self.tmp / "store", environ=self.env)
        self.incoming = self.tmp / "incoming"
        self.incoming.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def file(self, name: str, data: bytes) -> Path:
        path = self.incoming / name
        path.write_bytes(data)
        return path

    def add(self, name="tool-1.0.0.tar.gz", data=b"tool archive", **kw):
        kw.setdefault("source", URL)
        return self.store.add(self.file(name, data), now=NOW, **kw)

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.dict(os.environ, {osat.SANDBOX_VAR: "1"}):
            code = osat.main(list(argv))
        return code, out.getvalue(), err.getvalue()


class TestRecords(unittest.TestCase):

    def test_parse_matches_manage_python(self):
        fields = osat.parse_record("﻿a: 1\nno colon\na: 2\n b : x: y \n")
        self.assertEqual(fields, {"a": "1", "b": "x: y"})

    def test_render_orders_known_then_extra_and_drops_empty(self):
        text = osat.render_record({"z": "9", "asset": "f", "manager": "m", "size": ""},
                                  osat.PROVENANCE_KEYS)
        self.assertEqual(text, "manager: m\nasset: f\nz: 9\n")

    def test_render_refuses_multiline_value(self):
        with self.assertRaises(osat.StoreError):
            osat.render_record({"source": "https://x\nmanager: forged"}, osat.PROVENANCE_KEYS)

    def test_asset_names(self):
        for bad in ("", ".", "..", "PROVENANCE", "a/b", "a\\b", "a\nb"):
            with self.assertRaises(osat.StoreError, msg=bad):
                osat.check_asset_name(bad)
        osat.check_asset_name("cpython-3.12.14+20260924-x86_64.tar.gz")


class TestLocation(unittest.TestCase):

    def test_option_beats_environment(self):
        self.assertEqual(osat.resolve_store("/a", {"OSAT_STORE": "/b"}), Path("/a"))

    def test_environment_beats_default(self):
        self.assertEqual(osat.resolve_store(None, {"OSAT_STORE": "/b"}), Path("/b"))

    @unittest.skipUnless(POSIX, "XDG applies on Linux and macOS")
    def test_xdg_default(self):
        self.assertEqual(osat.default_store({"XDG_DATA_HOME": "/data"}),
                         Path("/data/osat-store"))


class TestAdd(Scratch):

    def test_new_artifact_is_stored_with_its_record(self):
        path, new = self.add(verified_against="https://example/SHA256SUMS", manager="manage-x 1.0.0")
        digest = sha(b"tool archive")
        self.assertTrue(new)
        self.assertEqual(path, self.store.blobs / digest[:2] / digest / "tool-1.0.0.tar.gz")
        record = osat.parse_record((path.parent / "PROVENANCE").read_text())
        self.assertEqual(record, {
            "manager": "manage-x 1.0.0", "asset": "tool-1.0.0.tar.gz", "sha256": digest,
            "source": URL, "installed": "2026-10-04T18:00:00Z", "size": "12",
            "verified-against": "https://example/SHA256SUMS", "fetched": "2026-10-04T18:00:00Z"})
        self.assertEqual(self.store.format(), 1)

    @unittest.skipUnless(POSIX, "permission bits")
    def test_everything_written_is_owner_only(self):
        self.add()
        for path in [self.store.root, *self.store.root.rglob("*")]:
            self.assertEqual(stat.S_IMODE(path.stat().st_mode) & 0o077, 0, path)

    def test_same_content_is_held_once_with_first_record(self):
        self.add(manager="first")
        path, new = self.add(name="renamed.tar.gz", manager="second")
        self.assertFalse(new)
        self.assertEqual(path.name, "tool-1.0.0.tar.gz")
        self.assertEqual(len(list(self.store.iter_blobs())), 1)
        record = osat.parse_record((path.parent / "PROVENANCE").read_text())
        self.assertEqual(record["manager"], "first")

    def test_wrong_expected_hash_is_refused_and_nothing_stored(self):
        with self.assertRaises(osat.StoreError):
            self.add(expected_sha256="0" * 64)
        self.assertEqual(list(self.store.iter_blobs()), [])
        self.assertEqual([p.name for p in self.store.blobs.iterdir()], [])

    def test_source_is_required(self):
        with self.assertRaises(osat.StoreError):
            self.add(source="")

    def test_symbolic_link_is_refused(self):
        target = self.file("real", b"x")
        link = self.incoming / "link"
        link.symlink_to(target)
        with self.assertRaises(osat.StoreError):
            self.store.add(link, source=URL)

    def test_path_of(self):
        path, _ = self.add()
        self.assertEqual(self.store.path_of(sha(b"tool archive").upper()), path)
        self.assertIsNone(self.store.path_of("1" * 64))
        with self.assertRaises(osat.StoreError):
            self.store.path_of("not-a-hash")

    def test_path_of_refuses_a_changed_file(self):
        path, _ = self.add()
        path.write_bytes(b"tampered")
        with self.assertRaises(osat.StoreError):
            self.store.path_of(sha(b"tool archive"))


class TestStoreRules(Scratch):

    def test_newer_format_is_refused(self):
        self.add()
        (self.store.root / "STORE").write_text("format: 2\n")
        with self.assertRaises(osat.StoreError):
            self.add(data=b"other")
        with self.assertRaises(osat.StoreError):
            self.store.path_of(sha(b"tool archive"))

    @unittest.skipUnless(POSIX, "permission bits")
    def test_broad_permissions_are_refused(self):
        self.add()
        self.store.root.chmod(0o755)
        with self.assertRaises(osat.StoreError):
            self.add(data=b"other")

    def test_sandbox_protects_the_real_store(self):
        real = osat.Store(osat.real_default_store(), environ=self.env)
        with self.assertRaises(osat.StoreError):
            real.ensure_writable()

    def test_no_store_yet_is_not_an_error(self):
        code, out, _err = self.run_main("--store", str(self.tmp / "none"), "--status")
        self.assertEqual(code, 0)
        self.assertIn("no store here yet", out)
        self.assertFalse((self.tmp / "none").exists())


class TestLookups(Scratch):

    def test_put_and_get(self):
        self.store.put_lookup(API, b'{"tag_name": "v1.0.0"}', etag='"abc"', now=NOW)
        body, meta = self.store.get_lookup(API)
        self.assertEqual(body, b'{"tag_name": "v1.0.0"}')
        self.assertEqual(meta["etag"], '"abc"')
        self.assertEqual(meta["fetched"], "2026-10-04T18:00:00Z")
        self.assertIsNone(self.store.get_lookup(API + "?page=2"))

    def test_replace(self):
        self.store.put_lookup(API, b"old", now=NOW)
        self.store.put_lookup(API, b"new", now=NOW + timedelta(hours=1))
        self.assertEqual(self.store.get_lookup(API)[0], b"new")
        self.assertEqual(len(list(self.store.iter_lookups())), 1)

    def test_changed_body_is_detected(self):
        self.store.put_lookup(API, b"body", now=NOW)
        body_path, _meta = self.store.lookup_paths(API)
        body_path.write_bytes(b"changed")
        with self.assertRaises(osat.StoreError):
            self.store.get_lookup(API)


class TestVerify(Scratch):

    def test_clean_store(self):
        self.add()
        self.store.put_lookup(API, b"body", now=NOW)
        code, _out, err = self.run_main("--store", str(self.store.root), "--verify")
        self.assertEqual(code, 0)
        self.assertIn("verified 2 entries", err)

    def test_faults_are_listed(self):
        path, _ = self.add()
        path.write_bytes(b"tampered")
        self.store.put_lookup(API, b"body", now=NOW)
        self.store.lookup_paths(API)[0].write_bytes(b"changed")
        code, out, err = self.run_main("--store", str(self.store.root), "--verify")
        self.assertEqual(code, 1)
        self.assertEqual(out.count("FAULT"), 2)
        self.assertIn("2 faults", err)


class TestSeeds(Scratch):

    def fill(self):
        self.add(name="tool-1.0.0.tar.gz", data=b"tool archive")
        self.add(name="SHA256SUMS", data=b"sums file", source=URL + ".sums")
        self.store.put_lookup(API, b'{"tag_name": "v1.0.0"}', now=NOW)

    def export(self, *extra):
        seed = self.tmp / "seed"
        code, _out, err = self.run_main("--store", str(self.store.root),
                                        "--export", str(seed), *extra)
        self.assertEqual(code, 0, err)
        return seed

    def import_into(self, seed, store_dir=None):
        target = store_dir or self.tmp / "other"
        return self.run_main("--store", str(target), "--import", str(seed)), \
            osat.Store(target, environ=self.env)

    def test_round_trip(self):
        self.fill()
        seed = self.export()
        self.assertTrue((seed / "SHA256SUMS").is_file())
        (code, _out, err), other = self.import_into(seed)
        self.assertEqual(code, 0, err)
        self.assertIn("2 artifacts added", err)
        digest = sha(b"tool archive")
        path = other.path_of(digest)
        self.assertEqual(path.read_bytes(), b"tool archive")
        record = osat.parse_record((path.parent / "PROVENANCE").read_text())
        self.assertEqual(record["source"], URL)
        self.assertEqual(record["fetched"], "2026-10-04T18:00:00Z")
        self.assertTrue(record["via"].startswith("seed "))
        self.assertEqual(other.get_lookup(API)[0], b'{"tag_name": "v1.0.0"}')

    def test_second_import_adds_nothing(self):
        self.fill()
        seed = self.export()
        self.import_into(seed)
        (code, _out, err), _other = self.import_into(seed)
        self.assertEqual(code, 0)
        self.assertIn("0 artifacts added, 2 already held, 0 lookups", err)

    def test_seed_is_usable_directly_as_a_store(self):
        self.fill()
        seed = osat.Store(self.export(), environ=self.env, owner_only=False)
        self.assertEqual(seed.path_of(sha(b"tool archive")).read_bytes(), b"tool archive")

    def test_selection(self):
        self.fill()
        selection = self.tmp / "select"
        selection.write_text("# only the tarball\nasset tool-*.tar.gz\n")
        seed = self.export("--select", str(selection))
        exported = osat.Store(seed, environ=self.env, owner_only=False)
        self.assertEqual([p.name for p in exported.iter_blobs()], [sha(b"tool archive")])
        self.assertEqual(list(exported.iter_lookups()), [])

    def test_selection_by_hash_and_lookup(self):
        self.fill()
        selection = self.tmp / "select"
        selection.write_text(f"sha256 {sha(b'sums file')}\nlookup https://api.github.com/*\n")
        exported = osat.Store(self.export("--select", str(selection)), environ=self.env,
                              owner_only=False)
        self.assertEqual([p.name for p in exported.iter_blobs()], [sha(b"sums file")])
        self.assertEqual(len(list(exported.iter_lookups())), 1)

    def test_bad_selection_line(self):
        self.fill()
        selection = self.tmp / "select"
        selection.write_text("everything\n")
        code, _out, err = self.run_main("--store", str(self.store.root), "--export",
                                        str(self.tmp / "seed"), "--select", str(selection))
        self.assertEqual(code, 1)
        self.assertIn("expected 'asset', 'sha256' or 'lookup'", err)

    def test_export_refuses_a_non_empty_directory(self):
        self.fill()
        (self.tmp / "seed").mkdir()
        (self.tmp / "seed" / "keep").write_text("x")
        code, _out, err = self.run_main("--store", str(self.store.root), "--export",
                                        str(self.tmp / "seed"))
        self.assertEqual(code, 1)
        self.assertIn("not an empty directory", err)

    def test_newer_lookup_in_store_is_kept(self):
        self.fill()
        seed = self.export()
        other = osat.Store(self.tmp / "other", environ=self.env)
        other.put_lookup(API, b"newer", now=NOW + timedelta(days=1))
        (code, _out, _err), _ = self.import_into(seed)
        self.assertEqual(code, 0)
        self.assertEqual(other.get_lookup(API)[0], b"newer")

    def assert_refused(self, seed, expect):
        before = sorted(p.as_posix() for p in (self.tmp / "other").rglob("*")) \
            if (self.tmp / "other").exists() else []
        (code, _out, err), _ = self.import_into(seed)
        self.assertEqual(code, 1)
        self.assertIn(expect, err)
        after = sorted(p.as_posix() for p in (self.tmp / "other").rglob("*")) \
            if (self.tmp / "other").exists() else []
        self.assertEqual(before, after, "a refused seed changed the store")

    def resum(self, seed):
        lines = [f"{osat.sha256_of(seed / rel)}  {rel.as_posix()}\n"
                 for rel in osat.seed_files(seed) if rel.as_posix() != "SHA256SUMS"]
        (seed / "SHA256SUMS").write_text("".join(lines))

    def test_refuses_without_sums(self):
        self.fill()
        seed = self.export()
        (seed / "SHA256SUMS").unlink()
        self.assert_refused(seed, "not a seed")

    def test_refuses_one_changed_byte(self):
        self.fill()
        seed = self.export()
        blob = next(osat.Store(seed, environ={}, owner_only=False).iter_blobs())
        asset = next(p for p in blob.iterdir() if p.name != "PROVENANCE")
        data = bytearray(asset.read_bytes())
        data[0] ^= 1
        asset.write_bytes(bytes(data))
        self.assert_refused(seed, "does not match SHA256SUMS")

    def test_refuses_an_unlisted_file(self):
        self.fill()
        seed = self.export()
        (seed / "lookups" / "extra").write_text("x")
        self.assert_refused(seed, "does not list")

    def test_refuses_a_missing_file(self):
        self.fill()
        seed = self.export()
        next(seed.glob("lookups/*.body")).unlink()
        self.assert_refused(seed, "missing files")

    def test_refuses_a_symbolic_link(self):
        self.fill()
        seed = self.export()
        (seed / "lookups" / "link").symlink_to(seed / "STORE")
        self.assert_refused(seed, "symbolic link")

    def test_refuses_an_unsafe_path(self):
        self.fill()
        seed = self.export()
        with open(seed / "SHA256SUMS", "a") as handle:
            handle.write(f"{'0' * 64}  ../outside\n")
        self.assert_refused(seed, "unsafe path")

    def test_refuses_a_blob_not_named_by_its_hash_even_with_matching_sums(self):
        self.fill()
        seed = self.export()
        blob = next(osat.Store(seed, environ={}, owner_only=False).iter_blobs())
        asset = next(p for p in blob.iterdir() if p.name != "PROVENANCE")
        asset.write_bytes(b"substituted")
        self.resum(seed)
        self.assert_refused(seed, "has SHA-256")

    def test_refuses_files_outside_the_layout(self):
        self.fill()
        seed = self.export()
        (seed / "README").write_text("hello")
        self.resum(seed)
        self.assert_refused(seed, "outside the store layout")


class TestCommandLine(Scratch):

    def test_add_and_path(self):
        source = self.file("tool.tar.gz", b"data")
        code, out, _err = self.run_main("--store", str(self.store.root), "--add", str(source),
                                        "--source", URL, "--sha256", sha(b"data"))
        self.assertEqual(code, 0)
        code, out2, _err = self.run_main("--store", str(self.store.root), "--path", sha(b"data"))
        self.assertEqual((code, out2), (0, out))

    def test_missing_path_exits_1(self):
        code, _out, err = self.run_main("--store", str(self.store.root), "--path", "a" * 64)
        self.assertEqual(code, 1)
        self.assertIn("is not in", err)

    def test_add_needs_source(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            osat.main(["--store", str(self.store.root), "--add", "x"])

    def test_status_lists_entries(self):
        self.add()
        self.store.put_lookup(API, b"body", now=NOW)
        code, out, _err = self.run_main("--store", str(self.store.root), "--status")
        self.assertEqual(code, 0)
        self.assertIn("artifacts: 1", out)
        self.assertIn("tool-1.0.0.tar.gz  12 B", out)
        self.assertIn(API, out)

    @unittest.skipUnless(hasattr(os, "geteuid"), "POSIX accounts")
    def test_refuses_root(self):
        with mock.patch.object(osat.os, "geteuid", return_value=0):
            code, _out, err = self.run_main("--store", str(self.store.root), "--status")
        self.assertEqual(code, 1)
        self.assertIn("do not run this with sudo", err)


if __name__ == "__main__":
    unittest.main()
