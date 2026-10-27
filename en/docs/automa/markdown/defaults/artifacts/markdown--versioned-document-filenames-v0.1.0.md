---
dc:title: "Markdown: Versioned Document Filenames"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Opus 5.5 (Anthropic)"
dc:description: "House rule: before version 1.0.0, a versioned markdown document's filename is its slug followed by a hyphen and its version in dotted form, as in <slug>-v0.1.0.md."
dcterms:created: "2026-10-03"
dcterms:modified: "2026-10-03"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "markdown--versioned-document-filenames"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: ""
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-10-03"
    author: "Christopher Steel"
    notes: >
      Initial draft. Written after an AI collaborator named a converted
      document with an underscored version suffix (v0_1_0), copied from the
      filenames of uploaded project files rather than from any stated rule.
      States the pre-1.0.0 filename convention so it applies at generation
      time.
---

# Markdown: Versioned Document Filenames

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This directive states how a versioned markdown document is named on disk while its version is below 1.0.0. It exists so that an AI collaborator names files correctly by default, at generation time, rather than inferring a pattern from whatever filenames happen to be in front of it.

## The rule

Before version 1.0.0, a versioned document's filename is its slug, followed by a hyphen, followed by its version written with a lowercase `v` and dots, followed by `.md`:

```text
<slug>-v<major>.<minor>.<patch>.md
```

The suffix appended to the slug is therefore always of the form `-v0.1.0.md`.

## Where each part comes from

The slug is the document's `dc:identifier`, which never carries a version. The version is the document's `dcterms:version`, prefixed with `v`. The two must agree: a document whose frontmatter says `dcterms:version: "0.3.1"` is saved as `<slug>-v0.3.1.md`.

When the version changes, the filename changes with it. Updating `dcterms:version` without renaming the file, or renaming the file without updating `dcterms:version`, leaves the document inconsistent.

## Examples

Correct:

```text
markdown--no-heading-numbers-v0.4.1.md
style-guide--markdown-mermaid-navigation-flowcharts-and-linked-sections-v0.1.5.md
dge-60-vf--scrutateur-et-secretaire-du-bureau-de-vote-v0.1.0.md
```

Incorrect:

| Filename | Problem |
| --- | --- |
| `markdown--no-heading-numbers-v0_4_1.md` | Underscores instead of dots |
| `markdown--no-heading-numbers-v0-4-1.md` | Hyphens instead of dots |
| `markdown--no-heading-numbers-0.4.1.md` | Missing the `v` |
| `markdown--no-heading-numbers_v0.4.1.md` | Underscore instead of a hyphen before the version |
| `markdown--no-heading-numbers.md` | Missing the version suffix before 1.0.0 |

Copies of documents whose filenames show underscored or hyphenated versions are not evidence of the convention. Name new and revised files by this rule, not by the pattern of nearby files.

## Scope

This directive covers versions below 1.0.0 only. The filename convention at 1.0.0 and later is not defined here.

## License

This document, *Markdown: Versioned Document Filenames*, by **Christopher Steel**, with AI assistance from **Claude Opus 5.5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft; states the pre-1.0.0 filename convention `<slug>-v0.1.0.md` after an underscored suffix was inferred from uploaded filenames |
