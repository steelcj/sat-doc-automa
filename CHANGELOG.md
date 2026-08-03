# Changelog

All notable changes to the sat-doc-automa repository are recorded here. This is the repository-level changelog: it records what each tagged release contained and why. Each document additionally carries its own changelog, in its frontmatter and in a Changelog table, for changes internal to that document.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions track the `VERSION` file and the git tags. Dates are ISO 8601.

## [Unreleased]

### Added

- file-fairy Usage guide (en/docs/guides/devops/), the operator guide the fairy roadmap called for: concepts, verbs, sync modes, retraction, managed blocks, conflicts, and the receive-then-commit pattern. Distributed to file-fairy and sat via the devops-docs groups.
- The shared CLAUDE.md signpost block (en/docs/automa/claude-md/) and a claude-md group in all three manifests: a fairy-owned block at the top of each target's CLAUDE.md, per the recommendation in decisions/ai-collaboration. sat-doc-automa's own root CLAUDE.md carries the same block between fairy markers.
- publish-release.py, the fourth release-ceremony script: builds a deterministic tarball for an already-pushed tag (built twice, refused on any byte difference), writes SHA256SUMS, optionally GPG-signs it (never blocking when gpg is absent), and publishes through a provider backend (gh for GitHub; a plain directory as the narrowest backend). Per decision--publish-release-shared-script-with-provider-interface. Ships with test_publish_release.py, an offline suite (20 checks) covering the ceremony, the refusals, and real signing.

### Changed

- Versioned Documents in Unrendered Markdown amended to 0.4.0: the Namespace rules paragraph now states the metadata ingress pipeline's resolution, canonical `dc:` in the generated sidecar, frontmatter as an unlegislated working dialect recorded in provenance. ROADMAP gains a Pending item for a configurable check-conformance.py.
- README gains a DevOps scripts section listing the four ceremony scripts and the test suite, with pointers to the workflow guide and the decision records.
- The three sync manifests distribute publish-release.py and test_publish_release.py in their devops-scripts groups. Standard OSAT Repository Layout amended to 0.4.0: publish-release.py joins the skeleton as required for release-managed repositories, and the sat drift row is corrected (the divergent bump-sat-version.py no longer exists).
- Commit and Versioning Workflow amended to 0.3.0: a "Publish the release" section completes the ceremony's documentation (write entries, cut, push, publish), with maintainer-side requirements stated. The 0.2.0 version parks under guides/devops/artifacts/; the three sync manifests now point at 0.3.0.
- Decision records gain their own tree, `en/docs/decisions/`, subdivided by the same domain names automa/ and guides/ use. The gh-cli decision moves from `guides/devops/` to `decisions/devops/`; decisions are cited by identifier, not synced. Standard OSAT Repository Layout amended to 0.3.0 to match.
- Shared zone gains the `guides/` layer: `en/docs/style-guides/` and `en/docs/devops/` move to `en/docs/guides/style-guides/` and `en/docs/guides/devops/`, matching the layout the README already advertises and the guides convention the receiving repositories use. All three sync manifests updated at `source == dest`. Standard OSAT Repository Layout amended to 0.2.0 to match.

## [0.1.4] - 2026-07-28

### Changed

- Roadmap compliance pass, resolving ROADMAP.md Milestones 0.2.0 through 0.4.0. Designated *Versioned Documents in Unrendered Markdown* (now 0.3.0) authoritative for structure, naming, frontmatter, and closing sections, with every other guide carrying an explicit deference statement. Reconciled the filename version separator, numbered body sections, closing-section order, bullet markers, and heading case across the guides. Bumped and brought into compliance: Technical Documentation (0.5.0, License section added), Plain Language (0.5.0), Web-Ready APA 7 (0.5.0, License section and title/identifier prefix added), Navigation and Accessibility (0.2.0, identifier and WCAG URL fixed), Energy Conservation (0.2.0, arithmetic corrected and citations moved to the CAP workflow), Commit and Versioning Workflow (0.1.1, em dash removed). Corrected `bump-version.py` to stop referencing a `bump-doc-versions.py` that does not exist. Brought the CNCF reference and license-block files into naming and structural conformance.

### Added

- This CHANGELOG.md.
- `check-conformance.py`, a script that reports the mechanically-detectable conformance issues (dotted filename versions, missing frontmatter fields, identifier/slug mismatch, em dashes in prose, asterisk bullets, numbered headings).

## [0.1.2] - 2026-07-24

### Changed

- Reorganized documents into the per-format archive layout: the markdown automa moved under `automa/markdown/`, the style guides under `guides/style-guides/`, and the commit workflow under `guides/devops/`. Added per-directory README files and expanded the root README.

### Added

- *Collaboration: Energy Conservation in AI Collaborations*, the first `automa/ai-collaboration/` directive.

### Removed

- The *Versioning Repositories and Documents* guide, superseded by the versioned-documents style guide and the commit-and-versioning workflow.

## [0.1.1] - 2026-07-24

### Added

- *Commit and Versioning Workflow* guide.

## [0.1.0] - 2026-07-24

### Added

- Initial repository: README, `bump-version.py`, the markdown automa (no heading numbers, no horizontal rules, use commas not em dashes, license statement templates), and the first style guides.
