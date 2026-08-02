# Changelog

All notable changes to the sat-doc-automa repository are recorded here. This is the repository-level changelog: it records what each tagged release contained and why. Each document additionally carries its own changelog, in its frontmatter and in a Changelog table, for changes internal to that document.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions track the `VERSION` file and the git tags. Dates are ISO 8601.

## [Unreleased]

### Changed

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
