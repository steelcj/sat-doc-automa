---
dc:title: "Proposal: One OS-Agnostic End-to-End Pass for OSAT Managers"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Opus 5.5 (Anthropic)"
dc:description: "Proposes replacing the POSIX-only end-to-end pass and the separate Windows validation script of osat-manager-python with one OS-agnostic pass and thin platform adapters, run offline from a seed in Incus containers for Linux and in a snapshot-restored Incus Windows virtual machine, and records what can and cannot be verified on macOS without Apple hardware."
dcterms:created: "2026-10-04"
dcterms:modified: "2026-10-04"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "proposal--one-os-agnostic-end-to-end-pass-for-osat-managers"
dc:relation: "proposal--offline-testing-for-osat-managers"
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
      Initial draft, written with Claude Opus 5.5 (Anthropic). One
      end-to-end pass with platform adapters, run from seeds in Incus
      containers and a snapshot-restored Incus Windows virtual machine;
      validate-windows.ps1 narrowed to Windows-only shells and the
      registry; macOS covered by shared POSIX paths and simulation, with
      its verification gap and the options for closing it recorded. The
      Incus agent checked on a copy of pristine-windows-11-002 and found
      absent: the Windows agent needs Incus 6.19.0 or later and the estate
      runs 6.0.0; upgrade and SSH-over-isolated-network routes recorded.
---

# Proposal: One OS-Agnostic End-to-End Pass for OSAT Managers

Version: 0.1.0
Status: Draft
Style Guide: style-guide--technical-documentation-for-technologists

## Abstract

osat-manager-python is one OS-agnostic implementation, but it is verified by two unrelated end-to-end programs: a POSIX-only Python pass for Linux and macOS, and a PowerShell script for Windows. Each repeats the manager's lifecycle checks in its own language, and the two can drift. This proposal replaces them with one OS-agnostic pass, written in Python, with thin platform adapters for paths, sandbox variables and alias invocation, and with a check catalogue in which each check states the platforms it applies to. `validate-windows.ps1` is narrowed to what a Python program cannot reach: `install.ps1` under Windows PowerShell 5.1, the aliases under `cmd.exe` and `powershell.exe`, command precedence and the registry. Every run reads its artifacts from a seed, as proposed in *Proposal: Offline Testing for OSAT Managers*, so no run needs the network. Linux distributions are exercised in Incus containers, and Windows in an Incus virtual machine restored to a pristine btrfs snapshot after each run. macOS cannot be run in Incus and no licence-compliant Apple hardware is available, so this proposal records exactly what of macOS is covered by shared code paths and simulation, what remains unverified, and the options for closing that gap.

## Sources and acknowledgements

The pass follows the collection's OS-agnostic method, one implementation absorbing the platform differences <a name="apa-os-agnostic-citation"></a>([Steel, 2026a](#apa-os-agnostic-reference)), and the manager design in *Proposal: osat-manager-python Layout, Lifecycle and Aliases* <a name="apa-manager-python-citation"></a>([Steel, 2026b](#apa-manager-python-reference)). Its artifacts come from the store and seeds of *Proposal: Offline Testing for OSAT Managers* <a name="apa-offline-citation"></a>([Steel, 2026c](#apa-offline-reference)). Incus behaviour is taken from the Incus documentation <a name="apa-incus-snapshots-citation"></a>([Linux Containers, n.d.-a](#apa-incus-snapshots-reference)). The test estate described, Incus containers, an Incus Windows 11 virtual machine with a pristine snapshot on btrfs, and no usable Apple hardware, is the operator's as of 2026-10-04. The existing programs were read on that date, with AI assistance from Claude Opus 5.5 (Anthropic); no tests were run for this proposal.

## Design principle

A behaviour that is the same on every platform is checked by the same code on every platform. Only a behaviour that exists on one platform alone is checked by code for that platform alone, and it lives inside the one pass as a platform-tagged check unless no Python program can reach it.

## Terminology

- **Pass**, the end-to-end program that installs, switches, renames, removes and restores runtimes through a manager, as a user would, and checks the result.
- **Platform adapter**, the small part of the pass that answers platform questions: where the real home is, which sandbox variables to set, how to run an alias, how to read permissions.
- **Check catalogue**, the list of checks the pass performs, each tagged with the platforms it applies to.
- **Harness Python**, a Python runtime used only to run the pass, kept outside every location the manager under test writes to, so that installing Python is never a precondition of testing a Python installer.
- **Test estate**, the machines available for testing: here, Incus containers for Linux and one Incus Windows 11 virtual machine.

## The old implementation

This section records osat-manager-python 1.0.x on 2026-10-04.

### e2e_manage_python.py

`e2e_manage_python.py`, 322 lines, runs a real end-to-end pass in a scratch home with sandbox mode on. It loads this checkout's `manage-python.py` in-process for the first install, then drives the installed aliases as a user would: two micro versions of one minor line and the latest of a second, then switch, rename, remove and restore from the archive with the network made unreachable. It checks every alias, `--status`, the pip refusal, a venv, the operator log, owner-only permissions, and that the real home is unchanged. Its downloads are cached in `WORK/cache`.

It is POSIX-only by construction. It imports `pwd` to find the real home, sets only the POSIX sandbox variables (`HOME` and the XDG variables, with `LOCALAPPDATA` and `APPDATA` pointed into the scratch area but unused), puts `/usr/bin` and `/bin` on `PATH`, runs aliases as files in `bin/`, and checks POSIX permission bits. It has been run on Linux. It should run on macOS, which takes the same code paths in the manager, but it has not been.

### validate-windows.ps1

`validate-windows.ps1`, 677 lines of Windows PowerShell 5.1, validates the real Windows behaviour on a disposable Windows 11 virtual machine from a fresh snapshot. It covers what a simulation cannot: `install.ps1`, the registry write that prepends `%LOCALAPPDATA%\Programs` to the user `PATH`, the `.cmd` and `.ps1` aliases under `cmd.exe` and `powershell.exe`, command precedence, and the lifecycle against real downloads. It writes a report of `PASS`, `FAIL` and `NOTE` lines with a checklist of manual steps.

It also repeats, in PowerShell, most of the lifecycle the Python pass checks: installs of two lines and an older pinned build, switch, rename, remove, offline restore, the pip refusal and a venv. It downloads every runtime on every run.

### Limitations

- **Two implementations of one lifecycle.** A change to the manager's lifecycle must be reflected in two programs in two languages, and nothing detects when they disagree.
- **Different coverage by accident.** Checks present in one program and not the other reflect when each was written, not a platform difference.
- **Different report formats.** The Python pass prints a summary line; the PowerShell script writes a report file. Results from different platforms cannot be compared or collected the same way.
- **No macOS run at all.** The manager is meant to work on macOS through its shared POSIX paths, but neither program has been run there.
- **No offline, isolated runs.** Linux runs use the developer's own machine; Windows runs download everything again after every snapshot revert.

## The test estate

### Linux, in Incus containers

Incus containers give clean Linux systems of several distributions, created and deleted in seconds, with copy-on-write storage on btrfs. They cover glibc distributions such as Debian, Ubuntu and Fedora, and musl through Alpine, for which the manager selects python-build-standalone's musl builds. A container can be given no network device at all, which is a stronger guarantee than `OSAT_NETWORK=deny` alone.

### Windows, in an Incus virtual machine

The operator's Incus virtual machine `windows` runs Windows 11 (`image.os: Windows 11`, four CPUs) and has a pristine snapshot, `pristine-windows-11-002`, taken on 2026-09-27. Because its storage is on btrfs, restoring the snapshot after a run is fast and returns the machine to exactly its pristine state <a name="apa-incus-snapshots-citation-2"></a>([Linux Containers, n.d.-a](#apa-incus-snapshots-reference)).

Two Incus facilities make the virtual machine scriptable from the host. The Incus agent runs in Windows virtual machines, installed from the virtual CD-ROM drive, and with it `incus exec` runs commands in the guest and returns their output <a name="apa-incus-files-citation"></a>([Linux Containers, n.d.-b](#apa-incus-files-reference)). An ISO custom storage volume can be attached to a virtual machine read-only, which carries a seed into the guest without any network <a name="apa-incus-volumes-citation"></a>([Linux Containers, n.d.-c](#apa-incus-volumes-reference)). The agent is not available on the estate today. On 2026-10-04 a throwaway copy of `pristine-windows-11-002` was started: Windows booted and took a network address, but `incus exec` reported that the agent was not running, and the virtual machine had never had the `agent:config` CD-ROM attached, from which the Windows agent is installed. The cause is the Incus version. The estate runs Incus 6.0.0, the Ubuntu long-term-support package, and the Windows agent installer first appears in Incus 6.19.0; no 6.0.x long-term-support release, up to 6.0.6, includes it.

Two routes make the Windows virtual machine scriptable from the host:

- **Upgrade Incus to 6.19.0 or later**, attach the agent CD-ROM with `incus config device add windows agent disk source=agent:config`, run its `install.ps1` as a local administrator, and take a new pristine snapshot, `pristine-windows-11-003`. Every step below then works as written. This moves the host off the long-term-support line.
- **Stay on Incus 6.0.0 and use SSH over an isolated network.** Windows 11 includes an OpenSSH server as an optional feature. Installed once in a new pristine snapshot, it lets the harness run commands and copy files over SSH. The run's network device is then attached to an Incus network with no uplink, created with NAT and IPv6 routing turned off, instead of being masked with `none`, so the host can reach the guest while the guest cannot reach anything beyond the host.

### macOS, not available

macOS cannot be run in Incus on this estate. Apple's software licence permits macOS virtual machines only on Apple-branded hardware <a name="apa-apple-sla-citation"></a>([Apple, n.d.](#apa-apple-sla-reference)), so running macOS in an Incus virtual machine on other hardware is not an option. The operator's Intel Mac is not usable at present, so there is no physical Mac, and no licence-compliant virtual machine, on the estate.

## The new implementation

### One pass, written in Python

The pass stays in Python, the manager's own language, and becomes OS-agnostic in the same way the manager is: by asking the manager's own helpers the platform questions rather than answering them again. It loads `manage-python.py` as it does today, and uses that module's `real_home()`, `protected_locations()`, sandbox variable lists and `Paths` class, so the pass and the manager can never disagree about where things belong.

A platform adapter supplies the rest:

| Question | Linux and macOS | Windows |
|----------|-----------------|---------|
| Real home | `real_home()` from the manager | `real_home()` from the manager |
| Sandbox variables | `HOME`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME`, `XDG_STATE_HOME`, `XDG_BIN_HOME` | `LOCALAPPDATA`, `APPDATA` |
| Base `PATH` | `/usr/bin`, `/bin` | `%SystemRoot%\System32`, `%SystemRoot%` |
| Running an alias | execute `bin/<alias>` | `cmd.exe /d /c <alias>.cmd` |
| Owner-only check | POSIX mode bits | the file's ACL lists only the user, through `icacls` |

### The check catalogue

Each check names the platforms it applies to. Most checks apply to all three: install, switch, rename, remove, offline restore, `--status`, the pip refusal, a venv, the operator log, owner-only files, the real home unchanged, and the store and `OSAT_NETWORK` behaviour of the offline proposal. A few apply to one platform:

| Check | Platforms | Why |
|-------|-----------|-----|
| musl build selected and runs | Linux (Alpine) | Only Linux has musl distributions |
| Apple Silicon build selected under Rosetta | macOS | Only macOS has Rosetta |
| `install.sh` under the system `/bin/sh` | Linux, macOS | POSIX bootstrap |
| `.cmd` alias under `cmd.exe` | Windows | Windows-only wrapper |

A check that does not apply is reported as `SKIP` with the reason, never silently omitted, so a report always shows the whole catalogue.

### What validate-windows.ps1 keeps

`validate-windows.ps1` keeps only what a Python program cannot exercise faithfully: `install.ps1` under Windows PowerShell 5.1 with the default execution policy, the `.ps1` aliases under `powershell.exe`, command precedence between `.cmd`, `.ps1` and other commands of the same name, and the registry `PATH` write as a new session sees it. Its lifecycle steps are removed, because the pass now performs them. It writes its results in the pass's report format.

### The harness Python

On a pristine Windows virtual machine, or a minimal Alpine container, there is no Python to run the pass. The harness therefore brings its own: a python-build-standalone runtime taken from the seed and extracted into the scratch area, outside every location the manager writes to. The pass runs on the harness Python; the manager under test installs its own runtimes as it would for a user. Using a runtime from the seed keeps the harness offline and identical to what the manager itself installs.

### One report format

Every run, on every platform, writes one report: a header naming the platform, triple, manager version and seed, then one line per check with `PASS`, `FAIL`, `SKIP` or `NOTE`, then a summary. `validate-windows.ps1` writes the same format. Reports from all platforms can then be collected side by side, and a report can be produced on a machine the operator does not control and sent back as a single text file.

### Running on Linux in Incus

For each distribution, the harness launches a container from a local image, attaches no network device, pushes the seed, the manager checkout and the pass, runs the pass with `OSAT_NETWORK=deny`, pulls the report and deletes the container:

```bash
incus create images:alpine/3.22 osat-e2e-alpine
incus config device add osat-e2e-alpine eth0 none
incus start osat-e2e-alpine
incus file push -r "$SEED_DIR" osat-e2e-alpine/opt/
incus file push -r "$CHECKOUT_DIR" osat-e2e-alpine/opt/
incus exec osat-e2e-alpine --env OSAT_STORE=/opt/seed --env OSAT_NETWORK=deny -- \
    /opt/osat-manager-python/run-e2e.sh --report /opt/report.txt
incus file pull osat-e2e-alpine/opt/report.txt "reports/alpine-3.22.txt"
incus delete --force osat-e2e-alpine
```

`SEED_DIR` is a seed exported with `osat-store.py --export`, named `seed`; `CHECKOUT_DIR` is the osat-manager-python checkout. `run-e2e.sh` is the small POSIX entry point that extracts the harness Python from the seed and starts the pass. Launching from an image already in the local store downloads nothing, and prepared images can be built offline from the store as proposed for uc-cboard <a name="apa-uc-cboard-citation"></a>([Steel, 2026d](#apa-uc-cboard-reference)).

### Running on Windows in the Incus virtual machine

One Windows run restores the pristine snapshot, attaches the seed as a read-only ISO volume, masks the network device, runs the pass and the narrowed `validate-windows.ps1` through the agent, captures the report from their output, and restores the snapshot again:

```bash
incus snapshot restore windows pristine-windows-11-002
xorriso -as mkisofs -J -joliet-long -R -V OSATSEED -graft-points -o "$WORK_DIR/seed.iso" \
    seed="$SEED_DIR" osat-manager-python="$CHECKOUT_DIR"
incus storage volume import default "$WORK_DIR/seed.iso" osat-seed --type=iso
incus config device add windows osat-seed disk pool=default source=osat-seed
incus config device add windows eth0 none
incus start windows
incus exec windows -- powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    '& ((Get-Volume -FileSystemLabel OSATSEED).DriveLetter + ":\osat-manager-python\run-e2e.ps1")' \
    > "reports/windows-11.txt"
incus stop windows
incus config device remove windows eth0
incus config device remove windows osat-seed
incus storage volume delete default osat-seed
incus snapshot restore windows pristine-windows-11-002
```

`WORK_DIR` is a scratch directory on the host. The `none` device stops the virtual machine inheriting its network device from its profile for the duration of the run <a name="apa-incus-none-citation"></a>([Linux Containers, n.d.-d](#apa-incus-none-reference)); it is removed afterwards so the pristine machine keeps its network for other uses. The drive letter of the attached ISO depends on the virtual machine's existing drives, so the command finds it by the volume label `OSATSEED` rather than assuming one. Windows reads an ISO's Joliet names, which are limited to 64 characters unless `-joliet-long` raises the limit to 103; the store's 64-character hash directories and runtime file names of about 80 characters need it. These commands are a design, not yet run, and assume the first route above; the `incus exec` step needs the Incus agent, which needs Incus 6.19.0 or later.

### macOS without Apple hardware

Without a Mac, macOS behaviour divides into three parts.

Covered by running on Linux: everything macOS shares with Linux in the manager, which is nearly all of it, including the XDG paths, the POSIX alias wrappers, the pointer file, the archive, owner-only permissions, sandbox mode, and every store and seed behaviour. Because the pass uses the manager's own helpers and the same checks on both platforms, a Linux pass is direct evidence for this shared code, though not proof that macOS's own tools, such as its `/bin/sh` and file system, behave identically.

Covered by simulation: the macOS-only decisions the manager makes from what the platform reports, such as selecting `aarch64-apple-darwin` or `x86_64-apple-darwin`, and detecting Rosetta. The unit tests already simulate these by replacing `platform.system`, `platform.machine` and the Rosetta check, and that coverage should be kept and widened to every macOS branch.

Not covered without a Mac: that the python-build-standalone macOS runtimes start and pass the manager's health check, that `install.sh` behaves under macOS's `/bin/sh` and login shell, that the aliases are found in a new Terminal session, and that Gatekeeper or file quarantine does not interfere with a runtime extracted by the manager. These remain unverified, and the manager's documentation should say so plainly until a run on Apple hardware confirms them.

The options for closing that gap, each compatible with the one pass and its report format:

- **A tester with an Apple Silicon Mac.** Someone with a Mac imports a seed, runs the pass with `OSAT_NETWORK=deny` and networking off, and returns the report file. The seed carries everything, so the tester needs no bandwidth, and the report format makes their result directly comparable with Linux and Windows runs.
- **Apple Silicon hardware for the estate.** A Mac mini or similar on the estate permits macOS virtual machines under Apple's licence <a name="apa-apple-sla-citation-2"></a>([Apple, n.d.](#apa-apple-sla-reference)), which would let macOS be restored to a pristine state between runs as the Windows virtual machine is. It is the only option that brings macOS fully under the operator's control.
- **Rented Apple hardware or hosted macOS runners.** Cloud providers rent Apple hardware, and hosted continuous-integration services offer macOS runners. Both are licence-compliant, but both are proprietary services outside the operator's control, the same reason the collection moved its security scan off a hosted service.

### Advantages and disadvantages

| Choice | Advantage | Disadvantage |
|--------|-----------|--------------|
| One pass in Python | One lifecycle implementation for three platforms; drift becomes impossible | The pass needs a Python before the manager under test has installed one |
| Manager's own helpers in the pass | Pass and manager cannot disagree about locations | The pass depends on the manager's internal names, which become a contract |
| Platform-tagged checks with `SKIP` | Every report shows the whole catalogue | Some checks are written once and run on one platform only |
| Narrowed `validate-windows.ps1` | PowerShell kept only where no other language reaches | Windows still has two programs, run in sequence |
| Harness Python from the seed | Works on pristine Windows and minimal Linux, offline | The seed must carry one more runtime per platform |
| Incus containers and a snapshot-restored virtual machine | Clean, offline, repeatable runs at no bandwidth cost | Windows automation needs Incus 6.19.0 or later for the agent, or SSH over an isolated network |
| macOS by shared paths and simulation | Most macOS code is exercised today | The macOS-only runtime, shell and Gatekeeper behaviour stays unverified |

## The contracts between components

### Harness to pass

The harness starts the pass with the harness Python and these inputs:

| Input | Meaning |
|-------|---------|
| `--work DIR` | Scratch area: run directory and harness Python |
| `--report FILE` | Where to write the report; standard output when absent |
| `--checkout DIR` | The manager checkout under test |
| `OSAT_STORE` | The seed or store to read artifacts from |
| `OSAT_NETWORK` | `deny` for every estate run |

The pass sets the sandbox variables itself, from the platform adapter, and refuses to run if any location it would write is one of the manager's real locations, using the manager's own `protected_locations()`.

### Pass to operator

The report is UTF-8 text. The header lines are `platform:`, `triple:`, `manager:`, `seed:` and `started:`, in the `key: value` form of `PROVENANCE`. Each check is one line: the result, two spaces, the check's identifier, two spaces, a one-line detail. The final line is `summary: <n> pass, <n> fail, <n> skip`. The exit status is 0 when there is no `FAIL`, and 1 otherwise. `validate-windows.ps1` writes the same header and line format, with its own check identifiers, so the two Windows reports can be concatenated into one.

## Implementation

The work follows *Proposal: Offline Testing for OSAT Managers*, whose store, seeds and `OSAT_NETWORK` it uses. The order below is suggested, each step useful on its own.

### The platform adapter and report format

Replace `pwd` and the fixed POSIX values in `e2e_manage_python.py` with the adapter, built on the manager's helpers, and write the report format. Run it on Linux to confirm nothing is lost.

### The check catalogue

Turn the pass's checks into catalogue entries with platform tags, add the Windows behaviours that `validate-windows.ps1` checks today and that Python can reach, and add the platform-only checks listed above.

### The harness

Write `run-e2e.sh` and `run-e2e.ps1`, which extract the harness Python from the seed and start the pass, and the host-side Incus scripts for Linux containers and the Windows virtual machine shown above.

### Narrowing validate-windows.ps1

Remove its lifecycle steps, keep the Windows-only shell and registry checks, and switch it to the report format.

### macOS

Widen the simulated macOS unit tests to every macOS branch in the manager, state macOS's verification status in the README as "shared paths verified on Linux, macOS-only behaviour simulated, not verified on Apple hardware", and choose one of the options above for a real run.

## Decisions and alternatives considered

### Python for the pass, not PowerShell or shell

We chose Python because it is the manager's own language, runs on all three platforms, and can load the manager's helpers directly. We considered PowerShell, which also runs on Linux and macOS as PowerShell 7, but it is not present on a pristine Linux or macOS system, and it cannot reuse the manager's code. We considered POSIX shell with a separate Windows script, which is the current arrangement this proposal replaces.

### Keeping validate-windows.ps1, narrowed

We chose to keep a PowerShell script for the behaviours only PowerShell and `cmd.exe` can exercise, because driving `install.ps1` under Windows PowerShell 5.1 and observing the registry `PATH` from a new session are what users experience, and a Python stand-in would test the stand-in. We considered removing it entirely and simulating those behaviours, and rejected that for the same reason.

### A harness Python from the seed, not the system Python

We chose a python-build-standalone runtime from the seed because pristine Windows and minimal Linux have no Python, and because a system Python would differ between machines. We considered installing Python with each platform's package manager before the run, which needs the network and elevated rights, both of which the collection avoids.

### Incus for Linux and Windows, not hosted runners

We chose the operator's Incus estate because runs are offline, repeatable, free of proprietary services, and restorable to a pristine state. We considered hosted continuous-integration runners for all three platforms; they would cover macOS, but they need the network, run on someone else's infrastructure, and would reintroduce the dependency the collection removed when it replaced its hosted security scan.

### Stating the macOS gap rather than closing it by assumption

We chose to separate what Linux runs and simulation cover from what only a Mac can confirm, and to record the remainder as unverified. We considered treating macOS as covered because it shares Linux's code paths; that would hide exactly the behaviours, runtime start-up, shell and Gatekeeper, that differ.

## Testing this proposal

The implementation is accepted when:

- The one pass passes in Incus containers for Debian 12, Ubuntu 24.04 and Alpine 3.22, each with no network device, reading only from a seed.
- The one pass and the narrowed `validate-windows.ps1` pass in the Incus Windows 11 virtual machine, restored from `pristine-windows-11-002`, with the seed attached as an ISO volume and the network device masked, and the snapshot is restored afterwards.
- The reports from all four runs use the one format and show the whole check catalogue, with `SKIP` and a reason for every platform-tagged check that does not apply.
- No lifecycle check exists in both the pass and `validate-windows.ps1`.
- The macOS unit tests cover every macOS branch in the manager, and the README states macOS's verification status as described above.
- When a Mac becomes available by any of the options above, the one pass runs on it unchanged from a seed, with no macOS-specific program.

## Open questions

- Whether to upgrade Incus to 6.19.0 or later for the Windows agent, or stay on the 6.0 long-term-support line and use SSH over an isolated network. Either way the result becomes `pristine-windows-11-003`.
- Which Linux distributions and versions form the standard set.
- Which option, if any, to pursue for a real macOS run, and whether a tester's report should be accepted as verification.
- Whether the pass should move to a shared location in sat-doc-automa, so other managers, such as osat-manager-slugify, use the same adapter, catalogue form and report format.

## License

This document, *Proposal: One OS-Agnostic End-to-End Pass for OSAT Managers*, by **Christopher Steel**, with AI assistance from **Claude Opus 5.5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

### OSAT collection

- [Creating OS-Agnostic Tools: A Worked Process](#apa-os-agnostic-reference)
- [Proposal: osat-manager-python Layout, Lifecycle and Aliases](#apa-manager-python-reference)
- [Proposal: Offline Testing for OSAT Managers](#apa-offline-reference)
- [Proposal: Minimizing Network Bandwidth for Local Testing](#apa-uc-cboard-reference)

### Incus

- [Instance snapshots](#apa-incus-snapshots-reference)
- [Accessing files and the Incus agent](#apa-incus-files-reference)
- [Storage volumes, including ISO volumes](#apa-incus-volumes-reference)
- [The none device](#apa-incus-none-reference)

### Licensing

- [Apple software licence agreements](#apa-apple-sla-reference)

## References

<a name="apa-apple-sla-reference"></a>Apple. (n.d.). *Software license agreements*. Retrieved October 4, 2026, from https://www.apple.com/legal/sla/
[Return to citation](#apa-apple-sla-citation)

<a name="apa-incus-snapshots-reference"></a>Linux Containers. (n.d.-a). *How to use snapshots for instances*. Incus documentation. Retrieved October 4, 2026, from https://linuxcontainers.org/incus/docs/main/howto/instances_snapshots/
[Return to citation](#apa-incus-snapshots-citation)

<a name="apa-incus-files-reference"></a>Linux Containers. (n.d.-b). *How to access files in an instance*. Incus documentation. Retrieved October 4, 2026, from https://linuxcontainers.org/incus/docs/main/howto/instances_access_files/
[Return to citation](#apa-incus-files-citation)

<a name="apa-incus-volumes-reference"></a>Linux Containers. (n.d.-c). *How to manage storage volumes*. Incus documentation. Retrieved October 4, 2026, from https://linuxcontainers.org/incus/docs/main/howto/storage_volumes/
[Return to citation](#apa-incus-volumes-citation)

<a name="apa-incus-none-reference"></a>Linux Containers. (n.d.-d). *Type: none*. Incus documentation. Retrieved October 4, 2026, from https://linuxcontainers.org/incus/docs/main/reference/devices_none/
[Return to citation](#apa-incus-none-citation)

<a name="apa-os-agnostic-reference"></a>Steel, C. (2026a). *Creating OS-agnostic tools: A worked process* (Version 0.1.0) [Process document]. sat-doc-automa repository, `en/docs/design/`.
[Return to citation](#apa-os-agnostic-citation)

<a name="apa-manager-python-reference"></a>Steel, C. (2026b). *Proposal: osat-manager-python layout, lifecycle and aliases* (Version 0.7.0) [Proposal]. osat-manager-python repository, `en/docs/`.
[Return to citation](#apa-manager-python-citation)

<a name="apa-offline-reference"></a>Steel, C. (2026c). *Proposal: Offline testing for OSAT managers* (Version 0.1.0) [Proposal]. sat-doc-automa repository, `en/docs/design/osat-managers/`.
[Return to citation](#apa-offline-citation)

<a name="apa-uc-cboard-reference"></a>Steel, C. (2026d). *Proposal: Minimizing network bandwidth for local testing* (Version 0.1.0) [Proposal]. uc-cboard repository, `en/docs/proposals/`.
[Return to citation](#apa-uc-cboard-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft: one OS-agnostic pass with platform adapters and a tagged check catalogue, a harness Python from the seed, one report format, offline runs in Incus containers and a snapshot-restored Incus Windows virtual machine, `validate-windows.ps1` narrowed to Windows-only shells and the registry, and the macOS coverage and verification gap recorded with options |
