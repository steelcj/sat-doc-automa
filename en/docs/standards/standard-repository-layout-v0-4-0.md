---
dcterms:title: "Standard OSAT Repository Layout"
dcterms:version: "0.4.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "The standard directory and file layout for OSAT repositories: the repository skeleton, the shared zone synced from sat-doc-automa, and the project zone each repository owns."
dcterms:created: "2026-08-02"
dcterms:modified: "2026-08-02"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "standard-repository-layout"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.1.4"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.4.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: >
      publish-release.py joins the skeleton as the fourth
      release-ceremony script, required for release-managed
      repositories, now that it exists, is tested, and has published
      its first real release (sat-doc-automa v0.1.4). Corrected the
      known-drift table's sat row: the divergent bump-sat-version.py
      no longer exists; sat's devops trio is byte-identical to
      canonical.
  - version: "0.3.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: >
      Decision records gain their own tree, decisions/, subdivided by
      the same domain names the automa and guides trees use. Decisions
      are cited by identifier, not synced, the same reference-only
      footing as style guides. The gh-cli decision relocates from
      guides/devops/ accordingly.
  - version: "0.2.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: >
      Shared zone gains the guides/ layer: style-guides/ and devops/ move
      to guides/style-guides/ and guides/devops/, matching the layout the
      README and the fleet's guides convention already advertise. Paths
      updated throughout, including the known-drift table.
  - version: "0.1.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: >
      Initial draft. Names the repository skeleton, the shared zone (synced
      from sat-doc-automa, source equals dest), and the project zone each
      repository owns. Derived from comparing the on-disk layouts of sat,
      file-fairy, osat-fluent, and sat-doc-automa.
---

# Standard OSAT Repository Layout

Version: 0.4.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Purpose

This document names the standard layout an OSAT repository is expected to hold, so that shared tooling and shared conventions can be distributed with confidence and a new repository can be scaffolded without guesswork. It exists because the receiving repositories have converged on a common skeleton in practice but had never written the standard down, which left each new repository and each sync manifest re-deriving it by eye.

The layout is described in three zones because that is how it actually behaves: a small skeleton every repository shares, a shared zone that is synced from sat-doc-automa and must stay identical across repositories, and a project zone each repository owns and organizes for itself. Conflating these three is what makes a single flat "standard directory tree" feel wrong, because two of the zones are common and one is deliberately not.

## The three zones

The **skeleton** is the handful of root files and the single language directory that every OSAT repository carries regardless of what it contains. It is small, required, and identical in shape everywhere.

The **shared zone** is the set of scripts and documents that originate in sat-doc-automa and are copied into each repository that opts in, at the same paths they occupy in the source. It is standardized precisely because it is shared: keeping source and destination paths identical is what lets a sync tool detect drift by comparing the same path in both repositories, and it is what keeps a rule or a script from meaning two different things in two places.

The **project zone** is everything a repository writes for itself: its architecture records, its specifications, its session logs, its own source code and packaging. It follows a light naming convention but is not forced into a common tree, because a documentation project, a library, and a CLI tool have genuinely different things to organize and a shape that fits one would be dead weight in another.

## The repository skeleton

Every OSAT repository carries these at its root. Required items are expected in every repository; recommended items are expected wherever they apply.

| Path | Status | Purpose |
|------|--------|---------|
| `VERSION` | required | A single semantic version line, the repository's own version, read by tooling and never guessed. |
| `README.md` | required | The entry document, including a License section. |
| `CHANGELOG.md` | required | Keeps an `## [Unreleased]` heading that `cut-release.py` rolls into a dated version heading at release time. |
| `ROADMAP.md` | recommended | Running record of decisions and open work, newest entry first. |
| `LICENSE` | required | The repository's license text. |
| `CONTRIBUTING.md` | recommended | Contributor guidance. The name is standardized as `CONTRIBUTING.md`, not `CONTRIBUTORS.md`, so the slot is found the same way everywhere. |
| `bump-version.py` | required for release-managed repositories | Writes `VERSION` only, single purpose, cannot half-update a repository. |
| `cut-release.py` | required for release-managed repositories | Reads the changelog, calls `bump-version.py`, rolls `Unreleased` into a dated heading, commits `VERSION` and `CHANGELOG.md` surgically, tags, and stops before push. |
| `publish-release.py` | required for release-managed repositories | Publishes an already-pushed tag: deterministic tarball (built twice, refused on any byte difference), `SHA256SUMS`, optional never-blocking GPG signature, through a provider backend, `gh` for GitHub or a plain directory. Ships with `test_publish_release.py`, its offline suite. |
| `check-conformance.py` | recommended | Lints the repository's markdown against the shared house rules. |
| `en/` | required | The language root. All documentation lives under a language directory, English at `en/`, so a repository is multilingual-ready by construction. |

Language-specific project files (`pyproject.toml`, `requirements.txt`, and a tool's own entry module) are project-zone concerns and are not part of the skeleton, even though they also sit at the root.

## The shared zone

The shared zone lives under `en/docs/` and is synced from sat-doc-automa at identical paths. A repository holds only the parts it opts into, but where it holds them, they match the source.

```text
en/docs/
  automa/
    <domain>/
      README.md
      defaults/
      examples/
  decisions/
    <domain>/
  guides/
    devops/
      artifacts/
    style-guides/
```

The `automa/` tree holds shared conventions grouped by domain, each domain a `README.md` describing the domain, a `defaults/` directory of the standing rules or snippets, and an `examples/` directory. The domains in use today are `ai-collaboration`, `licenses`, `markdown`, and `svg`. The `decisions/` tree holds decision records, subdivided by the same domain names the other trees use; decisions are cited by identifier, not synced, since a decision is a record of a choice, not a rule to distribute. The `guides/` tree holds the shared guides: `guides/devops/` for workflow documents such as the commit and versioning workflow, with superseded versions parked under `guides/devops/artifacts/` rather than deleted, and `guides/style-guides/` for style guides that are cited rather than copied.

Two rules govern this zone. First, synced items are copied at `source == dest`: a shared document keeps the same path in every repository, which is what makes drift detectable and keeps the fleet consistent. Second, style guides are reference-only: a repository cites a style guide by its versionless slug and a future check compares the cited version against the source's current version, rather than holding a second copy that can silently fall behind. A copied style guide is exactly the drift this zone is meant to prevent.

If a shared item ever needs a tidier home, the canonical path is changed once in sat-doc-automa and inherited everywhere through `source == dest`. Per-repository path remapping is avoided, because it fragments a repository away from its peers and turns drift detection into a per-repository special case.

## The project zone

Everything else under `en/docs/` belongs to the repository and is organized for its own needs. The convention here is light and is about naming and a few well-known slots, not about a mandated tree.

Documents are versioned markdown named by slug and version, for example `some-document-v0-1-0.md`, per the versioned-documents style guide. Session logs, where a repository keeps them, live under `en/docs/process/sessions/`. Where a document supersedes earlier versions, the earlier versions may be parked under a sibling `artifacts/` directory, the same retired-not-erased pattern the shared `guides/devops/` tree uses.

Beyond that, a repository arranges its own material as suits it. The documentation-heavy flagship repository organizes `en/docs/` by artifact type, with `architecture/adrs/`, `specifications/`, `guides/`, and `process/`, while a small tool repository may have almost nothing here beyond a `guides/devops/` entry. Both are conformant: the project zone is theirs to shape.

## How a repository is measured against this

A repository conforms when its skeleton is present, its shared-zone items match the source at the same paths, and its own documents follow the project-zone naming convention. Three instruments cover these, each a separate concern.

Skeleton presence is a simple existence check: the required root files and `en/` are there. Shared-zone currency is what the sync manifest and its stamp track: the manifest declares which shared items belong in the repository and at which paths, and the stamp records which have actually been applied and from which source version. Markdown conformance is what `check-conformance.py` reports: the house rules a repository's own documents are expected to honor.

These are intentionally independent. A repository can be current on shared items while its own documents still carry conformance findings, and it can have a complete skeleton while opting into only part of the shared zone.

## Adopting the layout

A new repository is scaffolded with the skeleton first, then opts into shared-zone groups through its sync manifest. An existing repository is brought into line incrementally: add missing skeleton files, apply the shared-zone groups it wants through the manifest, and then work down the conformance findings on its own documents as a separate pass.

Neither path forces the project zone into a new shape. Adopting the standard adds the skeleton and the shared zone; it leaves a repository's own documents where they are.

## Known drift at v0.1.0

A snapshot of where the current repositories stand against this layout, recorded so the reconciliation work is visible rather than implied. This table is a point-in-time observation, not part of the standard itself.

| Repository | Standing against the layout |
|------------|-----------------------------|
| sat-doc-automa | The source of the shared zone. Holds the full `automa/`, `guides/devops/`, and `guides/style-guides/` trees and the devops scripts. |
| sat | Skeleton nearly complete. The devops trio is present and byte-identical to canonical (the formerly divergent `bump-sat-version.py` is gone); not yet opted into the shared `en/docs/automa` or `en/docs/guides/devops` trees. Rich project zone. |
| file-fairy | Skeleton present with the full devops trio; missing `ROADMAP.md`. Minimal project zone beyond its own tool. |
| osat-fluent | Skeleton incomplete: no `CHANGELOG.md` and none of the devops scripts. Uses `CONTRIBUTORS.md` where the standard names `CONTRIBUTING.md`. Shared zone not yet applied. |

## License

This document, *Standard OSAT Repository Layout*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.4.0 | Draft | `publish-release.py` joins the skeleton, required for release-managed repositories, after its first real publish (sat-doc-automa v0.1.4). Corrected the sat drift row: the divergent `bump-sat-version.py` no longer exists. |
| 0.3.0 | Draft | Decision records gain their own tree, `decisions/`, subdivided by the shared domain names; cited by identifier, not synced. The gh-cli decision relocates from `guides/devops/`. |
| 0.2.0 | Draft | Shared zone gains the `guides/` layer: `style-guides/` and `devops/` become `guides/style-guides/` and `guides/devops/`, matching the layout the README and the fleet's guides convention already advertise. |
| 0.1.0 | Draft | Initial draft. Names the repository skeleton, the shared zone synced from sat-doc-automa at source equals dest, and the project zone each repository owns. Derived from comparing the layouts of sat, file-fairy, osat-fluent, and sat-doc-automa. |
