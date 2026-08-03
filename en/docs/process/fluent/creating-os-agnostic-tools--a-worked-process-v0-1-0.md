---
dc:title: "Creating OS-Agnostic Tools: A Worked Process"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic)"
dc:description: "The process of creating an OS-Agnostic Tool in the OSAT Fluent collection, as a worked example: choosing the underlying tool by verified capability rather than reputation, locating the governing specification in osat-fluent, building to it, and feeding discovered gaps back into the specification rather than working around them."
dcterms:created: "2026-08-03"
dcterms:modified: "2026-08-03"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "creating-os-agnostic-tools--a-worked-process"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:repository: "sat-doc-automa"
sat:path: "en/docs/process/fluent/"
sat:version_at_creation: "0.1.4"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-03"
    author: "Christopher Steel"
    notes: "Initial draft, derived from the rclone-tool installer migration to OSAT Fluent Archetype 5. Brought into house conformance on intake: frontmatter added, License section added, heading numbering removed, style-guide citations normalized to versionless slugs."
---

# Creating OS-Agnostic Tools: A Worked Process

Version: 0.1.0
Status: Draft
Style Guide: style-guide--web-ready-unrendered-markdown-using-apa-7; style-guide--technical-documentation-for-technologists

## Abstract

This document describes the process of creating an OS-Agnostic Tool, an installer that behaves identically on Linux, macOS, and Windows rather than requiring a separate implementation per platform. It uses the recent replacement of rclone-tool's installer as a worked example, from identifying rclone as more versatile than scp for the underlying sync problem, through locating and building to the current OSAT Fluent specification, to feeding a gap discovered during implementation back into that specification. It is intended for anyone building a new tool in the OSAT Fluent collection, or extending an existing one, who needs to know both the steps to follow and where the authoritative specification actually lives.

## Sources and Acknowledgements

This process and its terminology are derived primarily from the <a name="apa-osat-fluent-citation"></a>[osat-fluent repository (Steel, 2026)](#apa-osat-fluent-reference), the governing specification for the collection, and from <a name="apa-rclone-tool-citation"></a>[rclone-tool (Steel, 2026)](#apa-rclone-tool-reference) as the concrete tool this process was most recently applied to.

## Purpose and audience

This document is for anyone creating or updating a tool in the OSAT Fluent collection. It assumes familiarity with the collection's goals, self-contained installers with no elevation and no external dependencies beyond Python 3.8, but not necessarily familiarity with the specific steps that turn "we need tool X on three platforms" into a working, specification-compliant installer. It also serves as a record of one complete pass through that process, so a future pass can be compared against it rather than reconstructed from memory.

## Why the process matters

A cross-platform tool is not simply a script that happens to run on three operating systems. Linux, macOS, and Windows disagree about where user-installed executables belong, how permissions work, and what a configuration directory is called. An OS-Agnostic Tool absorbs those disagreements once, in the installer, so that every other part of the tool, and every person who uses it, only ever deals with one consistent behaviour. Skipping the documented process tends to reproduce the disagreements instead of absorbing them, for example a wrapper that only exists on Linux and macOS, or a permissions model that quietly does nothing on Windows because `chmod` is a no-op there.

The process below has four parts: choosing the right underlying tool before writing any installer code, locating the specification that governs how the installer must behave, building to that specification, and, when the specification itself turns out to be incomplete, updating it rather than working around it silently.

## Step 1: Establish versatility requirements before choosing a tool

Before writing an installer, the tool being wrapped has to be chosen. This step is easy to skip when an obvious candidate is already in front of you, in this case scp, which is native on all three target platforms with nothing to install. The obvious candidate is not always the right one, and the only way to know is to compare capability ceilings directly rather than assuming the native option is sufficient because it is native.

For directory sync specifically, three candidates were compared: scp, rsync, and rclone.

scp copies whole files with no filtering and no mirroring concept.

rsync adds delta transfer, filtering, and mirroring, but is not native on Windows without WSL or a separate install, and ships as a legacy, unmaintained build on macOS.

rclone is a single static binary with no dependencies, identical across all three platforms, and was already the basis of the surrounding backup infrastructure.

Choosing rclone was not the end of the comparison. Its age-based filtering, `--min-age` and `--max-age`, was assumed to support absolute calendar dates the way `find -newermt` does. It does not: both flags take durations measured from the current time, and an absolute-date filter has been requested by the rclone community but is not yet implemented (<a name="apa-rclone-issue-8462-citation"></a>[rclone, 2025](#apa-rclone-issue-8462-reference)).

Confirming this before committing to rclone as the tool of choice avoided a false assumption from reaching the installer. The general lesson: verify the specific capability the task actually needs, not the tool's reputation for capability in general, and verify it against the tool's current documentation or issue tracker rather than prior familiarity.

## Step 2: Locate the governing specification

Once the tool is chosen, the second step is finding the specification that defines how an OSAT Fluent installer for that tool must behave. This specification does not live with the tool itself, it lives in the collection's governing repository, <a name="apa-osat-fluent-citation-2"></a>[osat-fluent (Steel, 2026)](#apa-osat-fluent-reference), under `en/docs/`.

Two documents in that directory matter most for a self-contained binary installer, which covers most tools in the collection.

### User space targets

`osat--user-space-installation-specification` defines the target filesystem layout, the platform-native paths for binaries, wrappers, configuration, credentials, and state, and the permissions model. This is the specification in the strict sense, it defines what must be true of the finished installer, not how to write the code that produces it.

### Archetypes

`osat-fluent--archetype-5--self-contained-binary` is the implementation guide. It defines the installer's internal structure, `platform_paths()`, checksum verification, archive formats, wrapper rendering, in enough detail to be copied from directly. Its own abstract states that it supersedes the older `osat--tool-creation-pattern` document for new work, which is the signal that the archetype document, not the older pattern document, is current.

Determining which document is authoritative when more than one appears to cover the same ground comes down to two checks: the version number, since a higher minor or major version supersedes a lower one for the same document, and the abstract's own language, since a document that explicitly states it supersedes another is telling you which one to use. Do not assume the most recently modified file is the current one; check what the document says about its own place in the collection.

## Step 3: Build to the specification

With the specification identified, the installer itself follows the archetype-5 pattern directly. For rclone-tool, this meant four substantive changes to the existing installer, beyond a straightforward pass of path substitution.

`platform_paths()` replaced the previous module-level path constants with a single function returning a dictionary of resolved paths for the current platform, XDG variables with explicit fallbacks on Linux and macOS, `LOCALAPPDATA` and `APPDATA` with explicit fallbacks on Windows.

Permissions moved from `755` throughout to `700` on directories and executables, following the principle of least privilege defined in the specification. On Windows, where `os.chmod` only toggles the read-only attribute rather than restricting ownership, the equivalent restriction is applied with `icacls`, invoked via `subprocess`, on a best-effort basis, since Windows has no direct POSIX-permission equivalent to fall back on.

A local executive archive was added, a verified copy of every installed version kept under `archive/<version>/`, so that a version already installed once can be restored without a network request. This is new capability the archetype-5 pattern calls for that the tool's previous installer did not have.

Windows wrapper rendering was implemented in full, `.cmd` and `.ps1`, where the previous installer only installed the Windows binary and explicitly declined to render a wrapper. Implementing this is a specification requirement, but it introduces an obligation the specification itself is explicit about: a wrapper that has not been run on the platform it targets is untested, and that fact belongs in `ROADMAP.md`, not silently in the code.

## Step 4: Surface specification gaps rather than work around them

Building to the specification exposed a gap in the specification itself. The specification's path templates use a single `<tool-name>` placeholder for the wrapper, the data directory, and the configuration directory alike. For rclone, using `rclone` as that single identifier would place the installer's own env file at `~/.config/rclone/env`, the same directory rclone itself uses for `rclone.conf`. This is a real collision, not a theoretical one, between the installer's bookkeeping and the wrapped tool's own configuration.

The resolution applied to rclone-tool was to give the installer's own management directories a distinct identifier, `rclone-tool`, while keeping the command name and wrapper filename as plain `rclone`, the name the user actually types. This is a decision, not a workaround, and the distinction matters: a workaround stays local to the one tool that needed it and the next person building a tool hits the same problem again. A decision gets written into the specification so the next person checks for it before choosing a name.

The general principle: when building to a specification exposes a case the specification did not anticipate, the fix belongs in two places, the tool that surfaced it, and the specification itself, documented with the same rigour, what was decided, why, and what alternative was considered and rejected, that the specification applies to every other decision it records.

## Step 5: Version and publish the specification update

Specification documents in this collection are versioned documents in their own right, governed by `style-guide--versioned-documents-in-unrendered-markdown`, and follow semantic versioning for document changes specifically. Adding a new design principle, a new layout note, and a new decisions-and-rationale subsection is new content, not a correction, which makes it a minor version bump under that guide's own rule: patch is for corrections and wording clarifications, minor is for new content and new sections.

The updated `osat--user-space-installation-specification` moved from version 0.2.0 to 0.3.0 accordingly, with a new design principle in its second section, a note at the top of its layout section pointing at that principle before the reader reaches the path templates it qualifies, and a full decisions-and-rationale entry, in the same form as every other entry in that section, recording the rclone collision as the motivating case.

The implementation guide, `osat-fluent--archetype-5--self-contained-binary`, received a lighter, patch-level touch, one cross-reference sentence placed at the exact point where `platform_paths()` is defined, since that is where someone building a new installer will actually need the warning. This moved from 0.1.0 to 0.1.1, a clarification rather than new content in its own right, since it points at the specification's new section rather than restating its rationale.

Both updates are stored in the same place the documents they amend already live, `osat-fluent`, under `en/docs/`, using the collection's filename convention, the slug of the title with the version suffix appended using hyphens while the document remains at major version zero.

## Where to find the current specification

The authoritative, current specification for OSAT Fluent tools is the <a name="apa-osat-fluent-citation-3"></a>[osat-fluent repository (Steel, 2026)](#apa-osat-fluent-reference) itself, under `en/docs/`, not any copy or summary of it. At the time of this document, the two documents that matter for building a self-contained binary installer are `osat--user-space-installation-specification`, currently at version 0.3.0, and `osat-fluent--archetype-5--self-contained-binary`, currently at version 0.1.1. Both numbers will continue to move as the collection grows; the version and status block at the top of each document, and any superseding language in its abstract, are the source of truth for which document currently governs, not this document, and not any single conversation that produced an update to them.

## Decisions and rationale

The four-step shape of this process, tool selection, specification location, implementation, and feedback into the specification, was chosen over documenting only the implementation step on its own. Documenting implementation alone would have captured how rclone-tool's installer was rewritten but not why rclone was chosen over scp and rsync in the first place, and not why the naming collision it exposed became a specification change rather than a private fix. Both of those decisions carry information a future tool-builder needs and would otherwise have to rediscover.

The decision to record the specification's own location and current version numbers in the closing section above, rather than treating that as obvious context, follows from the same reasoning that produced section 10.7 of the updated specification itself: a document that is authoritative today can be superseded tomorrow, and a process document that does not say how to check for that becomes stale silently rather than visibly.

## License

This document, *Creating OS-Agnostic Tools: A Worked Process*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

### OSAT Fluent specification

- [osat-fluent repository](#apa-osat-fluent-reference)

### Worked example

- [rclone-tool repository](#apa-rclone-tool-reference)
- [rclone documentation](#apa-rclone-docs-reference)

## References

<a name="apa-osat-fluent-reference"></a>Steel, C. (2026). *osat-fluent* (Version 0.3.0) [Computer software]. GitHub. https://github.com/steelcj/osat-fluent
[Return to citation](#apa-osat-fluent-citation)

<a name="apa-rclone-docs-reference"></a>Rclone. (2024). *Rclone documentation*. https://rclone.org/docs/

<a name="apa-rclone-issue-8462-reference"></a>rclone/rclone. (2025). *Filter similar to --max-age but with a static date* (Issue #8462) [GitHub issue]. https://github.com/rclone/rclone/issues/8462
[Return to citation](#apa-rclone-issue-8462-citation)

<a name="apa-rclone-tool-reference"></a>Steel, C. (2026). *rclone-tool* [Computer software]. GitHub. https://github.com/steelcj/rclone-tool
[Return to citation](#apa-rclone-tool-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft, derived from the rclone-tool installer migration to OSAT Fluent Archetype 5 |
