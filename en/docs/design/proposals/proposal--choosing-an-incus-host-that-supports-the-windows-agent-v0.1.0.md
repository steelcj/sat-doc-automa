---
dc:title: "Proposal: Choosing an Incus Host That Supports the Windows Agent"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Opus 5.5 (Anthropic)"
dc:description: "Examines the Linux distributions and installation routes that provide an Incus version able to run the Incus agent in Windows virtual machines, evaluates them against the Universal Cake pillars and the operator's preference for Debian-based systems, and recommends three, led by Debian 13 with Incus 7.0 LTS from trixie-backports."
dcterms:created: "2026-10-04"
dcterms:modified: "2026-10-04"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "proposal--choosing-an-incus-host-that-supports-the-windows-agent"
dc:relation: "proposal--one-os-agnostic-end-to-end-pass-for-osat-managers"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:repository: "sat-doc-automa"
sat:path: "en/docs/design/proposals/"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-10-04"
    author: "Christopher Steel"
    notes: >
      Initial draft, written with Claude Opus 5.5 (Anthropic). Records the
      Incus 6.19.0 requirement for the Windows agent, the Incus versions
      and Windows agent binaries shipped by each distribution on
      2026-10-04, nine options, and three recommendations. Zabbly lts-7.0
      Windows agent build confirmed from its build workflow.
---

# Proposal: Choosing an Incus Host That Supports the Windows Agent

Version: 0.1.0
Status: Draft
Style Guide: style-guide--web-ready-unrendered-markdown-using-apa-7

## Abstract

Testing OSAT managers on Windows in an Incus virtual machine depends on the Incus agent running inside Windows, so that the host can run commands in the guest and collect their results. The current test host runs Incus 6.0.0, which cannot provide the agent to a Windows guest; support begins with Incus 6.19.0 and is part of the Incus 7.0 long-term-support line. This document records which Linux distributions and installation routes provide a suitable Incus, including whether each ships the Windows agent binary itself, examines nine options up to and including a change of host operating system, and evaluates them against the four Universal Cake pillars and the operator's preference for Debian-based systems. It recommends, in order, Debian 13 with Incus 7.0 LTS from the official trixie-backports archive on the operator's second, more powerful machine; Debian 13 with Incus 7.0 LTS from the Zabbly repository; and NixOS 26.05 with its `incus-lts` package.

## Sources and acknowledgements

Package versions are taken from Repology <a name="apa-repology-citation"></a>([Repology, n.d.](#apa-repology-reference)), the Debian package archive <a name="apa-debian-incus-citation"></a>([Debian, n.d.-a](#apa-debian-incus-reference)), the Zabbly repository documentation and metadata <a name="apa-zabbly-citation"></a>([Zabbly, n.d.](#apa-zabbly-reference)) and the nixpkgs package definition <a name="apa-nixpkgs-citation"></a>([NixOS contributors, n.d.](#apa-nixpkgs-reference)), all on 2026-10-04. The version in which Windows agent support begins was established by reading the Incus source code at each release tag <a name="apa-incus-source-citation"></a>([Linux Containers, 2026](#apa-incus-source-reference)). The evaluation applies the Universal Cake pillars as they are used in *Collaboration: Energy Conservation in AI Collaborations* <a name="apa-energy-citation"></a>([Steel, 2026a](#apa-energy-reference)), and the need for the agent comes from *Proposal: One OS-Agnostic End-to-End Pass for OSAT Managers* <a name="apa-one-pass-citation"></a>([Steel, 2026b](#apa-one-pass-reference)). The research was carried out with AI assistance from Claude Opus 5.5 (Anthropic). Nothing described here has yet been installed.

## Context

### Why the agent matters

The proposed Windows test run restores a pristine snapshot of a Windows 11 virtual machine, attaches a seed, runs the end-to-end pass inside the guest, collects its report and restores the snapshot again <a name="apa-one-pass-citation-2"></a>([Steel, 2026b](#apa-one-pass-reference)). Every step that reaches inside the guest uses `incus exec`, which works only when the Incus agent is running in the guest <a name="apa-incus-create-citation"></a>([Linux Containers, n.d.-a](#apa-incus-create-reference)).

### What was found on the current host

The current test host runs Linux Mint 22.3 with Incus 6.0.0 from the Ubuntu archive (`incus 6.0.0-1ubuntu0.3`). On 2026-10-04 a throwaway copy of the Windows virtual machine's snapshot `pristine-windows-11-002` was started. Windows booted and took a network address, but `incus exec` reported that the agent was not running, and the virtual machine had never had the agent's CD-ROM attached. The copy was then deleted, leaving the original virtual machine and snapshot unchanged.

### The requirement

The requirement has two parts.

The Incus server must be able to give a Windows guest the agent's installer. For Windows, Incus delivers the agent on a virtual CD-ROM, from which an `install.ps1` script installs it as a Windows service <a name="apa-incus-create-citation-2"></a>([Linux Containers, n.d.-a](#apa-incus-create-reference)). The code that writes `install.ps1` to that CD-ROM is absent from every Incus release checked up to 6.18.0 (6.0.0, 6.0.5, 6.6.0, 6.10.0, 6.12.0 and 6.14.0 to 6.18.0) and present in every release checked from 6.19.0 onwards (6.19.0 to 6.23.0 and 7.0.0 to 7.5.1) <a name="apa-incus-source-citation-2"></a>([Linux Containers, 2026](#apa-incus-source-reference)). No release of the 6.0 long-term-support line, up to 6.0.6, includes it. Incus 7.0 is the current long-term-support line, which the Incus project recommends to users who need a longer support length and less frequent changes <a name="apa-incus-news-citation"></a>([Linux Containers, n.d.-b](#apa-incus-news-reference)).

The host's package must also ship the Windows agent binary itself. The Windows setup script installs `incus-agent.exe` from the CD-ROM, so a server new enough to support the agent is still not sufficient if the distribution's package leaves out the Windows build of the agent.

### Selection criteria

Each option is evaluated against the four Universal Cake pillars <a name="apa-energy-citation-2"></a>([Steel, 2026a](#apa-energy-reference)), as they apply to a test host:

- **Agency**, sovereignty over the host: packages from a community archive the operator can rely on without a third party, and no dependency on a proprietary service.
- **Transparency**, the ability to see how the host is built: packages built from published source, and host configuration that can be read and reproduced.
- **Sustainability**, fewer avoidable upgrades and downloads: a long-term-support Incus line and a stable base system.
- **Inclusive**, a low cognitive and economic cost: familiar tools, and a setup another operator could follow.

Two further criteria are the operator's: a preference for Debian-based systems, and that the Windows agent binary be confirmed, not assumed.

## Availability by distribution

The tables below record the Incus version each distribution or repository provided on 2026-10-04 <a name="apa-repology-citation-2"></a>([Repology, n.d.](#apa-repology-reference)).

### With Windows agent support

| Distribution or repository | Incus version | Windows agent binary |
|----------------------------|---------------|----------------------|
| Debian 13 trixie-backports | 7.0.1 (LTS) | Confirmed: `incus-agent.windows.x86_64` <a name="apa-debian-agent-citation"></a>([Debian, n.d.-b](#apa-debian-agent-reference)) |
| Debian 14 forky and Debian unstable | 7.0.1 (LTS) | Same packaging as trixie-backports |
| Zabbly `lts-7.0` for Debian 12 and 13, Ubuntu 22.04, 24.04 and 26.04 | 7.0.1 (LTS) | Confirmed in the build workflow: `incus-agent.windows.x86_64` <a name="apa-zabbly-builds-citation"></a>([Zabbly, 2026](#apa-zabbly-builds-reference)) |
| Zabbly `stable`, same distributions | 7.5.1 | Built by the same workflow on its own branch; not separately checked |
| NixOS 26.05 and unstable | `incus-lts` 7.0.1, `incus` 7.5.1 | Confirmed: built for Windows on x86-64, i686 and ARM64 <a name="apa-nixpkgs-citation-2"></a>([NixOS contributors, n.d.](#apa-nixpkgs-reference)) |
| NixOS 25.11 | `incus` 7.0.0 | As above |
| Ubuntu 26.10 | 7.0.1 | Not checked |
| Fedora 42, 43 and 44 | 6.23 | Not checked |
| Arch Linux, Void Linux | 7.5.1 | Not checked |
| openSUSE Tumbleweed, Gentoo | 7.4 | Not checked |
| Alpine 3.24 | 7.0.1 | Not checked |

### Without Windows agent support

| Distribution | Incus version |
|--------------|---------------|
| Linux Mint 22.3, the current host | 6.0.0 |
| Ubuntu 24.04 LTS | 6.0.0 |
| Ubuntu 25.04 | 6.0.3 |
| Ubuntu 25.10 | 6.0.4 |
| Ubuntu 26.04 LTS | 6.0.5 |
| Debian 13 trixie, main archive | 6.0.4 |
| Debian 12 bookworm-backports | 6.0.4 |

No Ubuntu long-term-support release ships a suitable Incus from its own archive.

## Options examined

### Debian 13 with Incus 7.0 LTS from trixie-backports

Debian 13 is installed on the second machine, and Incus 7.0.1 is installed from trixie-backports, Debian's official archive of newer packages rebuilt for the stable release <a name="apa-backports-citation"></a>([Debian Backports, n.d.](#apa-backports-reference)). The `incus-agent` package ships `incus-agent.windows.x86_64` <a name="apa-debian-agent-citation-2"></a>([Debian, n.d.-b](#apa-debian-agent-reference)).

- **Agency:** strong. Every package comes from the Debian archive, signed by Debian, with no third-party repository.
- **Transparency:** strong. Debian builds from published source, and the package's file list is public.
- **Sustainability:** strong. A stable base system and the Incus long-term-support line mean few upgrades.
- **Inclusive:** strong. Standard Debian tooling, and the operator's preferred family.
- **Risks:** backports follow Debian testing and are supported on a best-effort basis, so a backported Incus can lag an upstream point release.

### Debian 13 with Incus 7.0 LTS from Zabbly

Debian 13 is installed, and Incus 7.0.1 is installed from the `lts-7.0` repository maintained by Zabbly, the company of the Incus project's lead developer <a name="apa-zabbly-citation-2"></a>([Zabbly, n.d.](#apa-zabbly-reference)).

- **Agency:** good. The repository is signed and maintained by upstream, but it is a third-party source added to the system.
- **Transparency:** good. Packages are built from the upstream source.
- **Sustainability:** strong. The same long-term-support line, with upstream point releases arriving promptly.
- **Inclusive:** strong. Standard Debian tooling.
- **Agent binary:** confirmed. The `lts-7.0` branch's build workflow compiles the agent for Windows on x86-64, i686 and ARM64 into `/opt/incus/agent`, and the `incus` package installs that directory <a name="apa-zabbly-builds-citation-2"></a>([Zabbly, 2026](#apa-zabbly-builds-reference)). The package also bundles its own QEMU and `virtiofsd` under `/opt/incus`, so the host's QEMU packages are not used.
- **Risks:** a third-party repository, and a QEMU that follows Zabbly's builds rather than Debian's security updates.

### Linux Mint 22.3 with Zabbly, in place

The current host keeps Linux Mint 22.3 and replaces its Incus 6.0.0 with Incus 7.0.1 from Zabbly's `lts-7.0` repository for Ubuntu 24.04, on which Mint 22.3 is based.

- **Agency, Transparency:** as for the previous option.
- **Sustainability:** good. No reinstallation, but the existing Incus database and all its instances are upgraded in place.
- **Inclusive:** strong for the operator, who keeps a familiar machine.
- **Risks:** an Incus database upgraded by a newer release should be treated as one-way, so every existing instance must be backed up first. The host remains a workstation as well as a test host.

### Ubuntu 26.10

Ubuntu 26.10 ships Incus 7.0.1 from its own archive. It is an interim release with a short support period, so the host would need upgrading again soon. It is not recommended.

### Debian 14 testing or Debian unstable

Both ship Incus 7.0.1, the same packaging as trixie-backports, but on a base system that changes continually. For a test host whose value lies in being stable and repeatable, the backports route gives the same Incus on a stable base. It is not recommended.

### IncusOS

IncusOS is an immutable operating system image dedicated to running Incus, based on Debian 13, which relies on UEFI Secure Boot and TPM 2.0 for boot security and disk encryption <a name="apa-incusos-citation"></a>([Linux Containers, n.d.-c](#apa-incusos-reference)). The machine becomes an Incus appliance, managed remotely with the `incus` client.

- **Agency, Transparency:** good. Built from published sources by the Incus project.
- **Sustainability:** strong. Image-based updates and no general-purpose software to maintain.
- **Inclusive:** mixed. Simple to run once installed, but different from a conventional Debian system, and the machine cannot be used for anything else.
- **Risks:** the second machine must support Secure Boot and TPM 2.0, and the Windows agent binary in IncusOS images is not confirmed.

### NixOS 26.05 with incus-lts

NixOS 26.05 provides `incus-lts` 7.0.1 and `incus` 7.5.1, and its package builds the agent for Windows <a name="apa-nixpkgs-citation-3"></a>([NixOS contributors, n.d.](#apa-nixpkgs-reference)). The whole host, Incus configuration included, is declared in one configuration file.

- **Agency:** strong. A community distribution with no third-party repository.
- **Transparency:** strongest of all the options. The host is reproducible from its configuration, which can be versioned beside the test documents.
- **Sustainability:** good. Long-term-support Incus, with a new NixOS release every six months.
- **Inclusive:** weaker. NixOS works very differently from Debian, which raises the cost for the operator and for anyone following the setup.
- **Risks:** a learning curve, and not Debian-based.

### Fedora, Arch Linux and other distributions

Fedora 42 to 44 ship Incus 6.23, and Arch Linux, Void Linux, openSUSE Tumbleweed and Gentoo ship 7.x releases. All would support the agent, but none is Debian-based, and the rolling distributions change continually. They are not recommended.

### Staying on Incus 6.0 with SSH

The current host keeps Incus 6.0.0, and the Windows virtual machine gets the OpenSSH server included with Windows 11, reached over an Incus network with no uplink. No host changes, but the harness must use SSH instead of `incus exec` on Windows alone, which adds a second way of reaching guests. It remains the fallback if no host change is made.

## Comparison

| Option | Agency | Transparency | Sustainability | Inclusive | Debian-based | Agent binary |
|--------|--------|--------------|----------------|-----------|--------------|--------------|
| Debian 13, trixie-backports | Strong | Strong | Strong | Strong | Yes | Confirmed |
| Debian 13, Zabbly `lts-7.0` | Good | Good | Strong | Strong | Yes | Confirmed in build workflow |
| Mint 22.3, Zabbly, in place | Good | Good | Good | Strong | Yes | Confirmed in build workflow |
| Ubuntu 26.10 | Strong | Strong | Weak | Strong | Yes | Not checked |
| Debian 14 or unstable | Strong | Strong | Weak | Strong | Yes | Same packaging as backports |
| IncusOS | Good | Good | Strong | Mixed | Debian 13 base | To confirm |
| NixOS 26.05, `incus-lts` | Strong | Strongest | Good | Weaker | No | Confirmed |
| Fedora, Arch and others | Strong | Strong | Mixed | Mixed | No | Not checked |
| Incus 6.0 with SSH | Strong | Strong | Strong | Mixed | Yes | Not needed |

## Recommendations

### First: Debian 13 with Incus 7.0 LTS from trixie-backports

This is the only option that is strong on all four pillars, Debian-based, confirmed to ship the Windows agent binary, and free of any repository beyond Debian's own. It also leaves the current workstation untouched while the second machine becomes the test host.

On a fresh Debian 13 installation, these commands, run as root, enable trixie-backports as the Debian Backports instructions describe <a name="apa-backports-citation-2"></a>([Debian Backports, n.d.](#apa-backports-reference)) and install Incus with the agent package, QEMU and the UEFI firmware a Windows 11 virtual machine with Secure Boot needs:

```bash
cat > /etc/apt/sources.list.d/debian-backports.sources <<'EOF'
Types: deb deb-src
URIs: http://deb.debian.org/debian
Suites: trixie-backports
Components: main
Enabled: yes
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF
apt update
apt install -t trixie-backports incus incus-agent qemu-system-x86 ovmf
```

After installation, the presence of the Windows agent binary can be confirmed with `ls /usr/libexec/incus/incus-agent.windows.x86_64`. The operator's account is then added to the `incus-admin` group and `incus admin init` run, as on any Incus host. These commands follow the published instructions and file lists but have not yet been run on the second machine.

### Second: Debian 13 with Incus 7.0 LTS from Zabbly

This is the same Incus line on the same base system, from upstream's own repository. It is the route to take if trixie-backports lags behind an upstream fix that the tests need, at the cost of adding a third-party repository. The repository is added as its documentation describes, after checking the signing key's fingerprint, `4EFC 5906 96CB 15B8 7C73 A3AD 82CC 8797 C838 DCFD` <a name="apa-zabbly-citation-3"></a>([Zabbly, n.d.](#apa-zabbly-reference)). Its build workflow confirms the Windows agent binary; `ls /opt/incus/agent/incus-agent.windows.x86_64` confirms it on the installed host.

### Third: NixOS 26.05 with incus-lts

This is the option that best serves Transparency: the test host itself becomes a reviewable, versioned configuration, and the Windows agent build is confirmed in the package definition <a name="apa-nixpkgs-citation-4"></a>([NixOS contributors, n.d.](#apa-nixpkgs-reference)). It ranks third only because it is not Debian-based and costs more to learn. If reproducing the test host exactly on another machine becomes important, it should be reconsidered.

### Moving the Windows virtual machine

On any of the recommended hosts, the Windows test machine can either be copied from the current host with `incus copy`, snapshots included, or rebuilt from the Windows 11 and VirtIO driver ISOs already held on the current host. Rebuilding is preferred: it gives a clean installation whose only change from a fresh Windows 11 is the agent, and it avoids depending on the virtual TPM state surviving a move between hosts, which has not been checked. Once Windows is installed, the agent's CD-ROM is attached with `incus config device add windows agent disk source=agent:config`, `install.ps1` is run from it as a local administrator, and the result is snapshotted as `pristine-windows-11-003`.

## Unverified points

- The commands in the recommendations have not been run on the second machine.
- Whether IncusOS images include the Windows agent binary. For Zabbly, the build workflow is confirmed but a built package has not been inspected.
- Whether the virtual TPM state of the existing Windows virtual machine survives `incus copy` between hosts.
- Whether the second machine supports Secure Boot and TPM 2.0, which IncusOS requires and a Windows 11 guest uses.

## Open questions

- Which recommendation to adopt.
- Whether the current host should later move to Incus 7.0 LTS as well, or remain on 6.0 for other work.
- Whether the chosen host's setup should be recorded as a decision in `en/docs/decisions/devops/` and as a guide.

## License

This document, *Proposal: Choosing an Incus Host That Supports the Windows Agent*, by **Christopher Steel**, with AI assistance from **Claude Opus 5.5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

### Incus

- [How to create instances, including the agent on Windows](#apa-incus-create-reference)
- [Incus news, including the 7.0 LTS line](#apa-incus-news-reference)
- [Incus source code at 7.0.1](#apa-incus-source-reference)
- [IncusOS documentation](#apa-incusos-reference)

### Packages and repositories

- [Repology: incus](#apa-repology-reference)
- [Debian: incus in trixie-backports](#apa-debian-incus-reference)
- [Debian: incus-agent file list in trixie-backports](#apa-debian-agent-reference)
- [Debian Backports instructions](#apa-backports-reference)
- [Zabbly Incus packages](#apa-zabbly-reference)
- [Zabbly lts-7.0 build workflow](#apa-zabbly-builds-reference)
- [nixpkgs incus package definition](#apa-nixpkgs-reference)

### Project documents

- [Collaboration: Energy Conservation in AI Collaborations](#apa-energy-reference)
- [Proposal: One OS-Agnostic End-to-End Pass for OSAT Managers](#apa-one-pass-reference)

## References

<a name="apa-debian-incus-reference"></a>Debian. (n.d.-a). *Package: incus (7.0.1-3~bpo13+1) [trixie-backports]*. Retrieved October 4, 2026, from https://packages.debian.org/trixie-backports/incus
[Return to citation](#apa-debian-incus-citation)

<a name="apa-debian-agent-reference"></a>Debian. (n.d.-b). *File list of package incus-agent in trixie-backports of architecture amd64*. Retrieved October 4, 2026, from https://packages.debian.org/trixie-backports/amd64/incus-agent/filelist
[Return to citation](#apa-debian-agent-citation)

<a name="apa-backports-reference"></a>Debian Backports. (n.d.). *Instructions*. Retrieved October 4, 2026, from https://backports.debian.org/Instructions/
[Return to citation](#apa-backports-citation)

<a name="apa-incus-create-reference"></a>Linux Containers. (n.d.-a). *How to create instances*. Incus documentation. Retrieved October 4, 2026, from https://linuxcontainers.org/incus/docs/main/howto/instances_create/
[Return to citation](#apa-incus-create-citation)

<a name="apa-incus-news-reference"></a>Linux Containers. (n.d.-b). *Incus news*. Retrieved October 4, 2026, from https://linuxcontainers.org/incus/news/
[Return to citation](#apa-incus-news-citation)

<a name="apa-incusos-reference"></a>Linux Containers. (n.d.-c). *IncusOS documentation*. Retrieved October 4, 2026, from https://linuxcontainers.org/incus-os/docs/main/
[Return to citation](#apa-incusos-citation)

<a name="apa-incus-source-reference"></a>Linux Containers. (2026). *Incus* (Version 7.0.1) [Computer software]. GitHub. https://github.com/lxc/incus/blob/v7.0.1/internal/server/instance/drivers/driver_qemu.go
[Return to citation](#apa-incus-source-citation)

<a name="apa-nixpkgs-reference"></a>NixOS contributors. (n.d.). *nixpkgs: pkgs/by-name/in/incus/generic.nix* [Computer software]. GitHub. Retrieved October 4, 2026, from https://github.com/NixOS/nixpkgs/blob/nixos-unstable/pkgs/by-name/in/incus/generic.nix
[Return to citation](#apa-nixpkgs-citation)

<a name="apa-repology-reference"></a>Repology. (n.d.). *Versions for incus*. Retrieved October 4, 2026, from https://repology.org/project/incus/versions
[Return to citation](#apa-repology-citation)

<a name="apa-energy-reference"></a>Steel, C. (2026a). *Collaboration: Energy conservation in AI collaborations* (Version 0.2.0) [Standing directive]. sat-doc-automa repository, `en/docs/automa/ai-collaboration/defaults/`.
[Return to citation](#apa-energy-citation)

<a name="apa-one-pass-reference"></a>Steel, C. (2026b). *Proposal: One OS-agnostic end-to-end pass for OSAT managers* (Version 0.1.0) [Proposal]. sat-doc-automa repository, `en/docs/design/osat-managers/`.
[Return to citation](#apa-one-pass-citation)

<a name="apa-zabbly-builds-reference"></a>Zabbly. (2026). *Incus package builds, lts-7.0 branch* [Build workflow]. GitHub. Retrieved October 4, 2026, from https://github.com/zabbly/incus/blob/lts-7.0/.github/workflows/builds.yml
[Return to citation](#apa-zabbly-builds-citation)

<a name="apa-zabbly-reference"></a>Zabbly. (n.d.). *Incus package repository* [README]. GitHub. Retrieved October 4, 2026, from https://github.com/zabbly/incus
[Return to citation](#apa-zabbly-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft: Incus 6.19.0 requirement and agent binary requirement, distribution availability on 2026-10-04, nine options evaluated against the Universal Cake pillars, three recommendations led by Debian 13 with trixie-backports. Zabbly lts-7.0 Windows agent build confirmed from its build workflow |
