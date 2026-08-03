---
dc:title: "Decision: GitHub CLI (gh) for Release Asset Publishing"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude (Anthropic) — drafting assistance"
dc:description: "Records the choice of the gh CLI over raw GitHub API calls for release-asset publishing scripts, and the scope boundary between this dev-only dependency and the git-free self-update work in the tool repositories."
dcterms:created: "2026-07-29"
dcterms:modified: "2026-07-29"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "decision--gh-cli-for-release-asset-publishing"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-07-29"
    author: "Christopher Steel"
    notes: "Initial draft, recording the decision reached in design discussion following the cut-release.py work."
---

# Decision: GitHub CLI (gh) for Release Asset Publishing

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Context

`cut-release.py` stops before push, by design. Once a tag is pushed, a separate, later step is needed to create the corresponding GitHub Release and attach a self-generated tarball and its `SHA256SUMS`, so self-update in tools like `osat-fluent-restic-tool` has a byte-stable artifact to verify against, rather than GitHub's auto-generated, not-guaranteed-stable tag archive. Creating a Release and uploading assets is a GitHub platform operation, not a git operation, and needs a way to authenticate and call GitHub.

## Decision

Release-publishing scripts (`publish-release.py` or equivalent, per repository) shell out to the `gh` CLI (`gh release create <tag> <files...> --notes "..."`) rather than calling GitHub's REST API directly. `gh` is confirmed to run on macOS, Windows, and Linux, with official installers on each: Homebrew or a direct binary on macOS, an MSI or `winget install --id GitHub.cli` on Windows, and `.deb`/`.rpm`/`.tar.gz` or a distribution's package manager on Linux.

This is a dev-only, release-side dependency. It applies to the small number of scripts a maintainer runs to cut and publish a release. It does not apply to, and must never be added as a requirement of, any `install-<tool-name>.py` that end users run to install or self-update a tool. That boundary is the point of this decision record: without it written down, "we needed gh for releases" could easily drift into "so gh is now a requirement," which is exactly the kind of dependency creep the self-update work was trying to avoid on the installer side.

## A requirement worth stating plainly: gh depends on git

`gh` and `git` are separate tools, and `gh` requires `git` to already be installed; this was confirmed by an install failure on a minimal Linux image where `dnf` refused to install `gh` because it depends on `git`, which was not yet present. This does not undo the self-update decision recorded separately (self-update deliberately avoids requiring `git` for end users installing or updating a tool). It does mean that `gh`-based release publishing carries a `git` requirement transitively, on top of `git` already being assumed for anyone developing these tools in the first place. The scope stays the same either way: end users of a tool never need `git`; maintainers releasing a tool already have it.

## Alternatives considered

**Raw HTTP against GitHub's REST API.** `POST /repos/{owner}/{repo}/releases` to create the Release, then `POST` asset bytes to the `upload_url` the response returns, a different host (`uploads.github.com`) than the API itself. This stays stdlib-only (`urllib`), consistent with every installer script in this collection. It was not chosen for this use because it requires the script to manage a personal access token itself, reading it from a private, non-repository location, never shell history, and failing cleanly and specifically on a missing or expired token rather than surfacing a raw 401. That's real surface area to get right for a dev-only tool that already has a lower-maintenance answer available. `gh` handles its own authentication once, via `gh auth login`, and the release-publishing script never touches a token directly.

## Consequences

- Any `publish-release.py`-equivalent script's own requirements documentation must state `gh` (authenticated via `gh auth login`) as a prerequisite, separate from and in addition to whatever `install-<tool-name>.py` requires.
- `install-<tool-name>.py` scripts across the collection are unaffected; their requirements remain `git` for initial acquisition only, trending toward none at all once the self-update-via-release-archive pattern lands per tool.
- The eventual GPG-signing of `SHA256SUMS` (paralleling `osat-fluent-restic-tool`'s deferred "Optional GPG verification" ROADMAP item, applied to the checksum file rather than the binary) is a natural extension of this same publishing step and should be recorded against this decision or its own follow-on, not invented separately per tool.
