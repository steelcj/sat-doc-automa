---
dcterms:title: "Versioning Repositories and Documents"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "Procedural guide to versioning: how repository versions and document versions differ, how each is bumped, and which tool does what."
dcterms:created: "2026-07-24"
dcterms:modified: "2026-07-24"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "versioning-repositories-and-documents"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: "Initial draft. Establishes the guides directory and records the repository-version versus document-version distinction, the bump procedures for each, and the tooling division between bump-version.py and the planned bump-doc-versions.py."
---

# Versioning Repositories and Documents

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This guide explains how versioning works in practice: what carries a version, how each kind of version is bumped, and which tool is responsible for what. It is the procedural companion to the versioned-documents style guide, which defines the conventions; this guide walks through actually applying them.

## Two different things carry versions

A repository has a version. Each document inside it also has its own version. These are different numbers, on different lifecycles, and treating them as the same number is a category error that eventually forces a bad choice.

The repository version tracks the project as a whole: its code, its tooling, its releases. It lives in a `VERSION` file at the repository root and advances when the project meaningfully changes.

A document's version tracks that document's own content, and nothing else. A document can go through five revisions while the repository version never moves, and a repository can cut three releases while a given document never changes. A style guide at `0.4.0` inside a repository at `1.2.0` is normal, not a mistake.

The practical consequence: nothing should ever bump both kinds of version in one operation. A tool that updates the `VERSION` file and also rewrites version lines inside documents couples two lifecycles that are not actually coupled, and it stops working the moment a document legitimately needs a different version than the repository, which happens immediately and often.

## What the version parts mean

Both kinds of version use semantic versioning, `MAJOR.MINOR.PATCH`, but the parts are interpreted against different subject matter.

For a repository: PATCH covers fixes and corrections with no change in behavior, MINOR covers new capability or meaningful refinement, MAJOR covers breaking changes to how the project is used.

For a document: PATCH covers corrections, typo fixes, and wording clarifications that do not change meaning, MINOR covers new content, new sections, or substantial rewrites of existing sections, MAJOR covers structural changes that alter the document's purpose or audience, including graduation from pre-release to stable.

## Bumping a repository version

```bash
python3 bump-version.py
```

output

```bash
bump-version.py, bump this repository's version.

Updates the VERSION file in this script's own directory. Nothing else.
Document version lines and changelogs are a separate concern, handled by
bump-doc-versions.py, so that this script stays a single-purpose tool
that cannot half-update a repository.

Usage:
    bump-version.py patch          0.1.0 -> 0.1.1
    bump-version.py minor          0.1.1 -> 0.2.0
    bump-version.py major          0.2.0 -> 1.0.0
    bump-version.py 0.3.2          set an explicit version
```



The repository version is bumped with `bump-version.py`, which does exactly one thing: it updates the `VERSION` file in its own directory. It touches nothing else, by design.

```bash
bump-version.py patch          0.1.0 -> 0.1.1
bump-version.py minor          0.1.1 -> 0.2.0
bump-version.py major          0.2.0 -> 1.0.0
bump-version.py 0.3.2          set an explicit version
```

The commit that records a version bump is pure: only the `VERSION` file changes in it. Tagging the release is a separate, deliberate act performed once per version and never rerun.

## Bumping a document version

A document version bump is three changes made together, never separately:

- `dcterms:version` in the frontmatter is set to the new version.
- `dcterms:modified` in the frontmatter is set to today's date.
- A changelog entry is added, in both places the document keeps one: the `sat:changelog` list in the frontmatter, newest first, and the Changelog table at the bottom of the document, also newest first.

The visible version block below the H1 is updated to match the frontmatter, and, while the document is pre-release, the filename's version suffix is updated too, so `some-document-v0-2-0.md` becomes `some-document-v0-3-0.md`. The `dcterms:identifier` never changes during any of this; it is the document's stable identity and carries no version.

## Pre-release and graduation

A document at major version zero, `v0.n.n`, is pre-release. Its filename carries the hyphenated version suffix, and it may change substantially between versions. The pre-release period is also when the filename itself matures: filename review is part of every version cycle, because at `v1.0.0` the suffix is dropped and the slug alone becomes the permanent filename. Graduation is a MAJOR change and is recorded in the changelog like any other.

## Which tool does what

`bump-version.py` bumps the `VERSION` file. Nothing else. It cannot half-update a repository because it only updates one file.

`bump-doc-versions.py`, planned but not yet built, will handle document-side bumping: the three-changes-together rule, the version block, and the filename rename, for a specified document. Until it exists, document bumps are performed by hand, following the steps above.

Keeping these as two tools, rather than one tool with two modes, is deliberate. Each maps to exactly one of the two lifecycles, so neither can accidentally reach across into the other's subject matter.

## License

This document, *Versioning Repositories and Documents*, by **Christopher Steel**, with AI assistance from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft |
