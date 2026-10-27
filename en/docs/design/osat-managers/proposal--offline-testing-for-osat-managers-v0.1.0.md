---
dc:title: "Proposal: Offline Testing for OSAT Managers"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Opus 5.5 (Anthropic)"
dc:description: "Assesses how OSAT managers are tested today with respect to network bandwidth, and proposes a shared, content-addressed artifact store, portable seeds, an explicit no-network mode, and offline installation for pip-based managers, so that every manager can be installed and tested with no network once a seed is present."
dcterms:created: "2026-10-04"
dcterms:modified: "2026-10-04"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "proposal--offline-testing-for-osat-managers"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:repository: "sat-doc-automa"
sat:path: "en/docs/design/osat-managers/"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-10-04"
    author: "Christopher Steel"
    notes: >
      Initial draft, written with Claude Opus 5.5 (Anthropic). Aligned with
      osat-store.py 0.1.0 before first commit: lookups as .body and .meta
      named by the full SHA-256 of the URL, source kept on import with a
      new via key, seeds in the store layout and usable in place,
      --path and --add added, --prune deferred. macOS added throughout:
      Apple Silicon wheel hash and per-platform acceptance criteria;
      macOS validated by the same OS-agnostic end-to-end pass as Linux,
      with macOS-only checks inside it, not by a separate script; the
      one agnostic pass for all three platforms moved to its own proposal. Records the
      current test arrangements of osat-manager-python 1.0.x and
      osat-manager-slugify 1.1.0 with measured artifact sizes, and proposes
      a shared content-addressed store, portable seeds, OSAT_NETWORK=deny,
      hash-pinned offline pip installs, and store-backed end-to-end and
      Windows validation runs.
---

# Proposal: Offline Testing for OSAT Managers

Version: 0.1.0
Status: Draft
Style Guide: style-guide--technical-documentation-for-technologists

## Abstract

OSAT managers are meant to be usable, and testable, in environments with limited or no network bandwidth. This proposal assesses how far the collection has come toward that goal, using osat-manager-python 1.0.x and osat-manager-slugify 1.1.0 as the existing implementations, and proposes the pieces still missing. osat-manager-python is already close: its unit tests use no network, its end-to-end pass caches every download, and its offline restore is tested with the network made unreachable. What the collection lacks is a single place where every downloaded artifact is kept once, verified on every read, and carried to another machine, together with an explicit no-network mode and an offline installation path for managers that depend on pip. We propose a shared content-addressed artifact store, portable seeds exported from it, an `OSAT_NETWORK=deny` mode honoured by every manager and test, and hash-pinned offline wheels for pip-based managers. Once a seed is present, every manager can then be installed, end-to-end tested and validated on Windows and macOS with no network at all.

## Sources and acknowledgements

The manager lifecycle, archive and `PROVENANCE` contract this proposal extends are defined in *Proposal: osat-manager-python Layout, Lifecycle and Aliases* <a name="apa-manager-python-citation"></a>([Steel, 2026b](#apa-manager-python-reference)), which follows the OSAT user-space installation specification <a name="apa-osat-spec-citation"></a>([Steel, 2026a](#apa-osat-spec-reference)). Two design principles from this repository shape the store: *Gold: Interfaces Stay Honest to the Narrowest Backend* <a name="apa-gold-narrowest-citation"></a>([Steel, 2026c](#apa-gold-narrowest-reference)) and the note *Gold: Provenance Is the Invariant, Canonical Is Configuration* <a name="apa-gold-provenance-citation"></a>([Steel, 2026d](#apa-gold-provenance-reference)). The shared-script form of the proposed store tool follows *Decision: publish-release.py as a Shared Script with a Provider Interface* <a name="apa-publish-release-citation"></a>([Steel, 2026e](#apa-publish-release-reference)). The bandwidth analysis repeats, for the managers, the method of *Proposal: Minimizing Network Bandwidth for Local Testing* in uc-cboard <a name="apa-uc-cboard-proposal-citation"></a>([Steel, 2026f](#apa-uc-cboard-proposal-reference)). The assessment was made by reading the two manager repositories on 2026-10-04, with AI assistance from Claude Opus 5.5 (Anthropic); no tests were run for it, and artifact sizes were taken from HTTP `Content-Length` headers and package index metadata on that date.

## Design principle

Every artifact crosses the network at most once, and a machine with no network is a fully supported environment, not a degraded one. After a seed has been imported, installing, switching, restoring and testing any OSAT manager needs no network, and a run that tries to reach the network fails at once and names the artifact it lacked.

## Terminology

- **Artifact**, any file a manager or test obtains from outside the machine: a release tarball, a checksum file, a wheel, a release-metadata response.
- **Artifact store**, the per-user directory, shared by all OSAT managers and their tests, in which every artifact is kept once, under its SHA-256, with a `PROVENANCE` record.
- **Seed**, a directory exported from an artifact store, holding a chosen set of artifacts, their records and a checksum list. A seed is what is carried to another machine, on removable media or over a local link.
- **Connected, limited and disconnected environments**, a machine with ordinary network access, with metered, slow or intermittent access, and with none.
- **Operator**, the person who runs a manager and decides when artifacts are fetched or refreshed.

## The old implementation

This section records the state of the collection on 2026-10-04. Sizes are for Linux x86-64 unless stated.

### osat-manager-python 1.0.x

The manager, `manage-python.py`, uses only the Python standard library. It obtains runtimes from python-build-standalone <a name="apa-pbs-citation"></a>([Astral, n.d.](#apa-pbs-reference)): it queries the GitHub Releases API, downloads the `install_only_stripped` tarball and the release's `SHA256SUMS`, verifies the tarball, and keeps it in `archive/<version>+<build>/` beside a `PROVENANCE` record <a name="apa-manager-python-citation-2"></a>([Steel, 2026b](#apa-manager-python-reference)). A runtime that is in the archive is restored with no network, and a fully pinned install does not query the API. One runtime, `cpython-3.12.14+20260924-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz`, is 34.3 MB.

Its tests are arranged in three tiers:

- `test_manage_python.py`, 2,675 lines of unit tests, runs against a fake network class and uses no network at all. It includes tests that assert the absence of network use, such as `test_pinned_needs_no_network` and `test_version_found_in_archive_needs_no_network`.
- `e2e_manage_python.py` performs a real end-to-end pass in a scratch home with sandbox mode on. It replaces the manager's `Network` class with a caching subclass that stores every response and download in `WORK/cache`, keyed by a hash of the URL, and logs each request as `fetched` or `cached`. A rerun downloads nothing. The offline steps run with every proxy variable set to `http://127.0.0.1:9`, where nothing listens, and with `PIP_NO_INDEX=1`, so any accidental download fails. The pass installs three runtimes, about 100 MB on the first run, estimated from the size above.
- `validate-windows.ps1` validates the real Windows behaviour on a disposable Windows 11 virtual machine, starting from a fresh snapshot each time. It installs the manager with `install.ps1` and then about four runtimes from GitHub. It tests the offline restore, but it has no cache of its own, so every run starts by downloading everything again.

osat-manager-python is built by the collection's OS-agnostic method: one implementation absorbs the platform differences, rather than one implementation per platform <a name="apa-os-agnostic-citation"></a>([Steel, 2026g](#apa-os-agnostic-reference)). Linux and macOS share every code path except a few detections, such as Rosetta, the platform triple and the C library, and both use the same XDG paths and POSIX alias wrappers; only Windows has paths, wrappers and a registry write of its own. That is why `validate-windows.ps1` exists and no macOS script does: the POSIX tests are meant to cover macOS as they cover Linux. They have not yet been run there, however, and the osat-manager-python README lists macOS as not yet verified. The same runtime for macOS is 25,017,789 bytes on Apple Silicon (`aarch64-apple-darwin`) and 24,719,239 bytes on Intel (`x86_64-apple-darwin`).

`test_publish_release.py` tests the release tooling and needs no network.

### osat-manager-slugify 1.1.0

`install-slug.py` builds a virtual environment and installs three pinned packages from PyPI with `pip install -r requirements.txt`: `python-slugify==8.0.4`, `text-unidecode==1.3` and `PyYAML==6.0.3`. The download is small: the first two are pure-Python wheels of 10,051 and 78,154 bytes, and PyYAML's compiled wheel for Python 3.12 ranges from 154,003 bytes on Windows x86-64 and 173,973 bytes on macOS Apple Silicon to 807,870 bytes on glibc Linux x86-64, one wheel per Python version and platform. The pins name versions but not hashes, and there is no path that installs without PyPI. The manager therefore cannot be installed, or its installation tested, on a disconnected machine at all.

### Limitations

- **No shared store.** Each manager keeps its own archive, and each test keeps its own cache. The end-to-end cache does not read the manager's archive, so a machine that has already archived a runtime downloads it again for a test, and two managers that need the same artifact each fetch it.
- **No portable form.** The end-to-end cache names files by a hash of their URL, with no manifest, so it cannot be inspected, subset, verified as a whole or carried to another machine with any confidence.
- **Verification on read is incidental.** Cached files are re-verified only because the manager happens to check them against a `SHA256SUMS` that comes from the same cache.
- **Freshness is implicit.** Cached release-metadata responses never expire, so reruns are silently pinned to whatever was newest when the cache was filled. The only refresh is `--clean`, which discards everything.
- **No explicit no-network mode.** Offline behaviour is forced from outside by a dead proxy. That covers HTTP clients that honour proxy variables, but it is not a contract a manager states and honours, and it does not report which artifact was missing.
- **Windows validation always downloads.** Reverting the snapshot discards everything the previous run fetched.
- **macOS is not yet verified.** The POSIX end-to-end pass that should cover it has never been run on macOS, so its offline behaviour there is unconfirmed.
- **pip-based managers have no offline path.** osat-manager-slugify depends on PyPI at install time, and its pins carry no hashes.
- **Bytes are not measured.** The end-to-end pass reports request counts but not bytes fetched.

## The new implementation

### Goals and non-goals

The goals are that, with a seed present, every OSAT manager can be installed, switched, restored and tested with no network; that reruns in a connected environment fetch nothing; that an operator can see, refresh and carry exactly what is stored; and that every run reports the bytes it fetched.

It is not a goal to build a package manager or a mirror. The store holds the artifacts that the managers and their tests already name, and nothing resolves dependencies. Trust in an artifact still comes from its upstream checksum or a hash pinned in a manager's repository; the store adds no new authority.

### The artifact store

The artifact store is one directory per user account, shared by all OSAT managers. Its location follows the same platform conventions as the managers themselves <a name="apa-xdg-citation"></a>([freedesktop.org, n.d.](#apa-xdg-reference)):

- Linux and macOS: `$XDG_DATA_HOME/osat-store/`, defaulting to `~/.local/share/osat-store/`
- Windows: `%LOCALAPPDATA%\osat-store\`
- Any platform: the `OSAT_STORE` environment variable, when set, overrides both

Artifacts are stored by content. Each artifact lives in a directory named for its SHA-256, holding the file under its original name and a `PROVENANCE` record:

```text
osat-store/
  blobs/
    3f/
      3f9c...e1/                     full SHA-256 of the file
        cpython-3.12.14+20260924-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
        PROVENANCE
  lookups/
    7a41...09.body                   a response body, named by the SHA-256 of its URL
    7a41...09.meta                   its URL, the body's SHA-256, fetch time and ETag
  STORE                              format version of this layout
```

Because a blob's name is its hash, every read can and does re-verify the file, the same artifact needed by two managers is stored once, and two stores can be merged by copying directories. Release-metadata responses are not content-addressed, because their content is what changes; they are kept in `lookups/`, named by the SHA-256 of their URL, with the body's own SHA-256 so that they too are verified on every read, and with the `ETag` and fetch time needed to refresh them conditionally. Checksum files whose hash is not known before they are fetched, such as a release's `SHA256SUMS`, are kept as lookups for the same reason <a name="apa-github-rest-citation"></a>([GitHub, n.d.](#apa-github-rest-reference)).

A manager's existing archive is kept as it is. When a manager needs an artifact it looks first in its own archive, then in the store, and only then at the network; every artifact it fetches is added to the store as well as to its archive. In a later version the archive could become a set of references into the store, but that change is not needed for any goal here.

### The no-network mode

Every manager and every test honours one environment variable, `OSAT_NETWORK`:

- `allow`, the default: artifacts missing from the archive and the store are fetched and stored.
- `deny`: nothing is fetched. A missing artifact stops the command with an error naming the artifact, the URL it would have come from and how to provide it, for example by importing a seed. Release lookups are answered from `lookups/`, and the age of each answer is shown.

This replaces the dead-proxy technique as the contract. The dead proxy remains useful inside tests, as a second guard that also catches a code path that bypasses the manager's `Network` class.

### Checking for updates

Fetching an artifact and finding out whether a newer one exists are separate operator actions. A refresh of release metadata uses conditional requests, so an unchanged release costs a `304 Not Modified` with no body <a name="apa-github-rest-citation-2"></a>([GitHub, n.d.](#apa-github-rest-reference)). Each manager's `--status` reports the age of the lookups it relied on, so a disconnected operator knows how current their view is. Nothing downloads a newer version because it exists; an install is always an explicit command.

### Seeds

A seed is an exported subset of a store, in the store's own layout, plus a `SHA256SUMS` file over everything in it. It holds the selected blobs with their `PROVENANCE` records and the selected lookups. Because a seed is a store, it can also be used in place, read-only, by pointing `OSAT_STORE` at it. Its narrowest backend is a plain directory: a USB stick, a shared folder in a virtual machine or a directory copied over a local link is a complete transport, and nothing in the design depends on a richer one <a name="apa-gold-narrowest-citation-2"></a>([Steel, 2026c](#apa-gold-narrowest-reference)).

Export and import are performed by a shared, standard-library Python script, `osat-store.py`, distributed like `publish-release.py` <a name="apa-publish-release-citation-2"></a>([Steel, 2026e](#apa-publish-release-reference)):

```text
osat-store.py --status                         list artifacts, lookups, sizes and ages
osat-store.py --verify                         re-hash every artifact and lookup
osat-store.py --path SHA256                    print a verified artifact's path
osat-store.py --add FILE --source URL [--sha256 HASH]
                                               add a file obtained some other way
osat-store.py --export DIR [--select FILE]     write a seed
osat-store.py --import DIR                     verify a seed and merge it
```

Import verifies every file against the seed's `SHA256SUMS` and every blob against its own name before adding anything, and refuses the whole seed on any mismatch: a listed file missing or different, an unlisted file, a symbolic link, an unsafe path, a file outside the store layout, or a record that disagrees with its file. A selection file names what to export, one rule per line, by asset-name pattern, by hash or by lookup-URL pattern, so an operator can prepare, for example, a seed holding everything needed to install and test manage-python 3.12 and 3.13 on Linux x86-64 and Windows x86-64.

### Offline installation for pip-based managers

A manager that installs Python packages pins them by version and by hash in its requirements file, and installs with hash checking <a name="apa-pip-secure-citation"></a>([Python Packaging Authority, n.d.-a](#apa-pip-secure-reference)):

```text
python-slugify==8.0.4 \
    --hash=sha256:276540b79961052b66b7d116620b36518847f52d5fd9e3a70164fc8c50faa6b8
text-unidecode==1.3 \
    --hash=sha256:1311f10e8b895935241623731c2ba64f4c455287888b18189350b67134a822e8
PyYAML==6.0.3 \
    --hash=sha256:ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc \
    --hash=sha256:41715c910c881bc081f1e8872880d3c650acf13dfa8214bad49ed4cede7c34ea \
    --hash=sha256:7f047e29dcae44602496db43be01ad42fc6f1cc0d8cd6c83d342306c32270196 \
    --hash=sha256:fc09d0aa354569bc501d4e787133afc08552722d3ab34836a80547331bb5d4a0 \
    --hash=sha256:5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b
```

These are the published SHA-256 values on PyPI as of 2026-10-04. The five PyYAML hashes cover its Python 3.12 wheels for glibc Linux and musl Linux on x86-64, macOS on Intel and on Apple Silicon, and Windows on x86-64; each further Python version or platform a manager supports adds one hash. pip accepts a requirement when the file it installs matches any of the listed hashes. The wheels for each supported platform and Python version are fetched once with `pip download --only-binary=:all:` and the matching `--platform` and `--python-version` options <a name="apa-pip-download-citation"></a>([Python Packaging Authority, n.d.-b](#apa-pip-download-reference)), and kept in the store like any other artifact. Installation then never contacts an index:

```bash
python3.12 -m pip install --no-index --find-links "$WHEEL_DIR" --require-hashes -r requirements.txt
```

`WHEEL_DIR` is a temporary directory the manager fills from the store with the wheels named in the requirements file. Pure-Python wheels, such as `python-slugify` and `text-unidecode`, serve every platform; compiled wheels, such as PyYAML's, are needed once per platform and Python minor version a seed is meant to support.

### Tests that read the store

The unit tests need no change; they already use no network.

The end-to-end pass replaces its private URL-keyed cache with the artifact store. A run against a scratch copy of the store, seeded read-only from the operator's store, keeps the real store untouched while still downloading nothing that is already present. Two options are added: `--offline`, which sets `OSAT_NETWORK=deny` from the first step, so the whole pass, bootstrap included, must succeed from the store; and a final report of bytes fetched alongside the request counts.

Windows validation reads a seed instead of the network. The seed, including the manager's own release archive for `install.ps1`, is copied into the virtual machine or attached as a shared folder, `OSAT_STORE` points at it, and the run proceeds with `OSAT_NETWORK=deny`. Reverting the snapshot then discards nothing that needs downloading again.

macOS needs no validation script of its own, because it takes the same code paths as Linux. It is validated by running the same `e2e_manage_python.py --offline` pass on Apple hardware, from an imported seed, with networking turned off. The few behaviours that exist only on macOS are added to that one pass as checks that run when the platform is macOS, not split into a separate script: the check that selects the `aarch64-apple-darwin` build when the manager itself runs under Rosetta and would otherwise see an Intel machine <a name="apa-manager-python-citation-4"></a>([Steel, 2026b](#apa-manager-python-reference)), and `install.sh` under macOS's own `/bin/sh` and default login shell. A seed meant for macOS holds runtimes for each architecture it is to support, about 25 MB per runtime per architecture.

The same reasoning applies to Windows in the longer term. `validate-windows.ps1` covers what a Python test cannot reach, `cmd.exe`, Windows PowerShell 5.1 and the registry, but the store, seed and `OSAT_NETWORK` behaviour is the same on every platform. Making `e2e_manage_python.py` run on Windows as well, and narrowing `validate-windows.ps1` to the Windows-only shells and registry, would give one agnostic pass on all three platforms. This is independent of offline testing and is proposed separately in *Proposal: One OS-Agnostic End-to-End Pass for OSAT Managers* (`proposal--one-os-agnostic-end-to-end-pass-for-osat-managers`).

Clean-machine Linux testing, on distributions other than the operator's, can use prepared Incus images built from the store with no network device, as proposed for uc-cboard <a name="apa-uc-cboard-proposal-citation-2"></a>([Steel, 2026f](#apa-uc-cboard-proposal-reference)). This is optional, Linux-only, and builds on the store rather than replacing any part of it. macOS cannot be tested this way, because macOS virtual machines run only on Apple hardware; a fresh user account or a fresh macOS virtual machine on Apple hardware serves instead, running the same end-to-end pass.

### Advantages and disadvantages

| Choice | Advantage | Disadvantage |
|--------|-----------|--------------|
| One shared store | Each artifact fetched once per machine, across managers and tests | A new shared component every manager must read |
| Content addressing | Verification on every read, deduplication, merge by copy | Lookups need a separate, non-addressed area |
| Seeds as plain directories | Any medium is a complete transport | Seeds for many platforms grow large, about 34 MB per runtime |
| `OSAT_NETWORK=deny` | A stated contract with a useful error | Every manager and test must implement it |
| Hash-pinned offline wheels | pip-based managers installable with no network, with stronger integrity | One compiled wheel per platform and Python version to collect |
| Store-backed Windows validation, and the same end-to-end pass on macOS | Snapshot reverts and fresh accounts no longer cost downloads; no macOS-only script to maintain | A seed must be prepared and attached before the run; macOS needs Apple hardware |

## The contracts between components

### Store layout and format version

The layout above is format 1, recorded as the single line `format: 1` in `STORE`. A reader that finds a higher format refuses to write and reports it. Blob directories are named by the lowercase hexadecimal SHA-256 of the file, sharded by its first two characters. Every file a manager writes into the store is owner-only, as in manager archives, and a store directory broader than that is refused. Seeds are exempt, because removable media often has no POSIX permissions. Tests set `OSAT_STORE_SANDBOX`, under which nothing may write to the account's default store location.

### Blob PROVENANCE

Each blob carries a `PROVENANCE` file in the format manage-python already writes: UTF-8, one `key: value` pair per line, unknown keys ignored by readers <a name="apa-manager-python-citation-3"></a>([Steel, 2026b](#apa-manager-python-reference)). The first five keys are the existing ones, so the same parser reads archive and store records; the store adds three, and a fourth on import. The example shows the record a manager implementing this proposal would write; `1.1.0` stands for that future manager version.

| Key | Meaning |
|-----|---------|
| `manager` | The manager and version that stored the artifact |
| `asset` | The file name |
| `sha256` | The file's checksum, equal to its directory name |
| `source` | The URL it was fetched from, or how it reached the machine when it was not fetched; unchanged by import |
| `installed` | UTC time it entered this store, ISO 8601 |
| `size` | Size in bytes |
| `verified-against` | The upstream checksum file or pinned hash it was verified against |
| `fetched` | UTC time it was first fetched from the network, carried through seeds unchanged |
| `via` | Present only on imported artifacts: `seed` and the SHA-256 of the seed's `SHA256SUMS` |

```text
manager: manage-python 1.1.0
asset: cpython-3.12.14+20260924-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
sha256: <64 hexadecimal characters>
source: https://github.com/astral-sh/python-build-standalone/releases/download/20260924/cpython-3.12.14+20260924-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
installed: 2026-10-04T18:02:11Z
size: 34270188
verified-against: https://github.com/astral-sh/python-build-standalone/releases/download/20260924/SHA256SUMS
fetched: 2026-10-04T18:02:11Z
```

Provenance travels with the artifact, while where the store lives is configuration, which is the principle recorded in *Gold: Provenance Is the Invariant, Canonical Is Configuration* <a name="apa-gold-provenance-citation-2"></a>([Steel, 2026d](#apa-gold-provenance-reference)).

### Environment variables

| Variable | Values | Effect |
|----------|--------|--------|
| `OSAT_STORE` | A directory | Overrides the default store location |
| `OSAT_NETWORK` | `allow`, `deny` | `deny` forbids every fetch; default `allow` |

Both are read by every manager, by `osat-store.py`, and by every test harness, and both are passed through by sandbox mode.

### Operator output and logging

Every artifact a command uses is reported once, on one line, with its origin: `archive`, `store`, `seed` or `fetched`, followed by the size for anything fetched. Each command ends with a one-line total, for example `fetched 0 B; 3 artifacts from the store`. The same lines go to the manager's operator log. In `deny` mode, the refusal is a single message naming the asset, its URL and the remedy, and the exit status is the manager's existing error status.

## Implementation

The work divides by repository; the order below is the suggested order, each step useful on its own. The first step has begun.

### osat-store.py and the store format

A new shared script in sat-doc-automa, standard library only, with the commands listed under Seeds. Version 0.1.0 exists as `osat-store.py`, with 45 offline unit tests in `test_osat_store.py`, all passing on Linux on 2026-10-04; it has not yet been run on Windows or macOS. A guide and `--prune` remain.

### osat-manager-python

Read and write the store in `Network`, honour `OSAT_NETWORK`, report origins and bytes, and show lookup ages in `--status`. Replace the end-to-end cache with the store, and add `--offline` and the bytes report. Teach `validate-windows.ps1` to use an attached seed. Add the macOS-only checks to `e2e_manage_python.py`, and run it on macOS for the first time.

### osat-manager-slugify

Add hashes to `requirements.txt`, fetch and store wheels for the supported platforms, install with `--no-index --find-links --require-hashes`, honour `OSAT_NETWORK`, and add an end-to-end pass that installs with no network from a seed.

### The OSAT specification

Record the store location, `OSAT_STORE`, `OSAT_NETWORK`, the blob `PROVENANCE` keys and the operator output rule as collection-wide requirements <a name="apa-osat-spec-citation-2"></a>([Steel, 2026a](#apa-osat-spec-reference)).

## Decisions and alternatives considered

### A shared store rather than per-manager archives alone

We chose one store for all managers because artifacts are shared across managers and tests, and because a single place is what an operator can inspect, export and carry. We considered extending each manager's archive with export and import; it would duplicate shared artifacts and give an operator one seed per manager to manage.

### Content addressing rather than URL keys

We chose SHA-256 names so that every read verifies the file and identical artifacts are stored once. We considered keeping the end-to-end cache's URL keys, which are simpler, but a URL key says nothing about the content and cannot detect corruption or substitution.

### A stated no-network mode rather than a dead proxy

We chose `OSAT_NETWORK=deny` because it is a contract managers can document and test, and it lets them name the missing artifact. We considered relying on the dead proxy, which already works in tests; it is kept as a second guard, but it is not something an operator should have to set.

### A shared script rather than store commands in every manager

We chose `osat-store.py` for export, import, verification and pruning, because those operations concern the store, not any one manager, and the collection already distributes shared scripts. We considered adding the commands to each manager, which would give several implementations of the same operations.

### Hash-pinned wheels rather than a local package index

We chose wheels in the store installed with `--no-index --find-links` because it needs no running service and works from any directory. We considered a local package index or caching proxy, which would serve all of PyPI but adds a service to run and secure, and does not help on a machine with no network unless it was filled in advance anyway.

### Keeping existing archives unchanged

We chose to leave manager archives as they are and add the store beside them, so that no released manager's on-disk layout changes. We considered making archives references into the store immediately; that is a larger migration with no benefit for the goals here.

## Testing this proposal

The implementation is accepted when the following hold on three platforms: Linux on x86-64, a Windows 11 virtual machine on x86-64, and macOS on Apple Silicon.

On all three platforms:

- `test_osat_store.py` passes.
- A seed with one byte changed is refused by `osat-store.py --import`, and nothing from it is added.
- In `deny` mode, a missing artifact produces the single named refusal, not a network error.
- osat-manager-slugify installs and passes its end-to-end pass with `OSAT_NETWORK=deny` from a seed.

On Linux and macOS, where `e2e_manage_python.py` runs:

- `e2e_manage_python.py --offline` passes on a machine whose only source of artifacts is an imported seed, and reports `fetched 0 B`.
- A second connected run of `e2e_manage_python.py` reports `fetched 0 B`.

On Windows:

- `validate-windows.ps1` passes from a fresh snapshot with an attached seed and no network adapter.

On macOS:

- The `e2e_manage_python.py --offline` pass, including its macOS-only checks, passes in a fresh user account on Apple Silicon with an attached seed and networking turned off.

## Open questions

- The name `osat-store` and whether the store should live under an existing OSAT data directory.
- Whether the end-to-end pass should copy the operator's store or read it directly in a read-only mode.
- The set of platforms and Python versions a standard seed should cover, including whether macOS on Intel, Linux on ARM64 and Windows on ARM64 are supported, and so whether their runtimes and wheels belong in it.
- Whether macOS acceptance should also be run on an Intel Mac while Intel macOS remains supported.
- Whether seeds should carry a detached signature, in addition to `SHA256SUMS`, for transfer between operators.
- A retention policy and a `--prune` command, for example keeping only artifacts referenced by an installed or archived version. `osat-store.py` 0.1.0 does not prune, because it cannot yet know which artifacts a manager references.

## License

This document, *Proposal: Offline Testing for OSAT Managers*, by **Christopher Steel**, with AI assistance from **Claude Opus 5.5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

### OSAT collection

- [OSAT user-space installation specification](#apa-osat-spec-reference)
- [Proposal: osat-manager-python Layout, Lifecycle and Aliases](#apa-manager-python-reference)
- [Decision: publish-release.py as a Shared Script with a Provider Interface](#apa-publish-release-reference)
- [Proposal: Minimizing Network Bandwidth for Local Testing](#apa-uc-cboard-proposal-reference)

### Design principles

- [Gold: Interfaces Stay Honest to the Narrowest Backend](#apa-gold-narrowest-reference)
- [Gold: Provenance Is the Invariant, Canonical Is Configuration](#apa-gold-provenance-reference)
- [Creating OS-Agnostic Tools: A Worked Process](#apa-os-agnostic-reference)

### Platforms and packaging

- [python-build-standalone](#apa-pbs-reference)
- [XDG Base Directory Specification](#apa-xdg-reference)
- [pip secure installs](#apa-pip-secure-reference)
- [pip download](#apa-pip-download-reference)
- [GitHub REST API best practices](#apa-github-rest-reference)

## References

<a name="apa-pbs-reference"></a>Astral. (n.d.). *python-build-standalone* [Computer software]. GitHub. https://github.com/astral-sh/python-build-standalone
[Return to citation](#apa-pbs-citation)

<a name="apa-xdg-reference"></a>freedesktop.org. (n.d.). *XDG Base Directory Specification*. Retrieved October 4, 2026, from https://specifications.freedesktop.org/basedir-spec/latest/
[Return to citation](#apa-xdg-citation)

<a name="apa-github-rest-reference"></a>GitHub. (n.d.). *Best practices for using the REST API*. GitHub Docs. Retrieved October 4, 2026, from https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
[Return to citation](#apa-github-rest-citation)

<a name="apa-pip-secure-reference"></a>Python Packaging Authority. (n.d.-a). *Secure installs*. pip documentation. Retrieved October 4, 2026, from https://pip.pypa.io/en/stable/topics/secure-installs/
[Return to citation](#apa-pip-secure-citation)

<a name="apa-pip-download-reference"></a>Python Packaging Authority. (n.d.-b). *pip download*. pip documentation. Retrieved October 4, 2026, from https://pip.pypa.io/en/stable/cli/pip_download/
[Return to citation](#apa-pip-download-citation)

<a name="apa-osat-spec-reference"></a>Steel, C. (2026a). *OSAT user-space installation specification* (Version 0.2.0). GitHub. https://github.com/steelcj/osat-fluent
[Return to citation](#apa-osat-spec-citation)

<a name="apa-manager-python-reference"></a>Steel, C. (2026b). *Proposal: osat-manager-python layout, lifecycle and aliases* (Version 0.7.0) [Proposal]. osat-manager-python repository, `en/docs/`.
[Return to citation](#apa-manager-python-citation)

<a name="apa-gold-narrowest-reference"></a>Steel, C. (2026c). *Gold: Interfaces stay honest to the narrowest backend* (Version 0.1.0) [Design principle]. sat-doc-automa repository, `en/docs/design/gold/`.
[Return to citation](#apa-gold-narrowest-citation)

<a name="apa-gold-provenance-reference"></a>Steel, C. (2026d). *Gold: Provenance is the invariant, canonical is configuration* [Design note]. sat-doc-automa repository, `en/docs/design/gold/`.
[Return to citation](#apa-gold-provenance-citation)

<a name="apa-publish-release-reference"></a>Steel, C. (2026e). *Decision: publish-release.py as a shared script with a provider interface* (Version 0.1.0) [Decision record]. sat-doc-automa repository, `en/docs/decisions/devops/`.
[Return to citation](#apa-publish-release-citation)

<a name="apa-uc-cboard-proposal-reference"></a>Steel, C. (2026f). *Proposal: Minimizing network bandwidth for local testing* (Version 0.1.0) [Proposal]. uc-cboard repository, `en/docs/proposals/`.
[Return to citation](#apa-uc-cboard-proposal-citation)

<a name="apa-os-agnostic-reference"></a>Steel, C. (2026g). *Creating OS-agnostic tools: A worked process* (Version 0.1.0) [Process document]. sat-doc-automa repository, `en/docs/design/`.
[Return to citation](#apa-os-agnostic-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft: assessment of osat-manager-python 1.0.x and osat-manager-slugify 1.1.0 test arrangements with measured sizes; proposed shared content-addressed store, seeds, `OSAT_NETWORK=deny`, hash-pinned offline wheels, store-backed end-to-end and Windows validation. Aligned with osat-store.py 0.1.0 before first commit. macOS added to the assessment, wheel hashes and per-platform acceptance criteria, validated by the same OS-agnostic end-to-end pass as Linux |
