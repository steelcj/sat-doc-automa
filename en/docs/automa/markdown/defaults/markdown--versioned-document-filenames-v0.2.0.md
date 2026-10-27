---
dc:title: "Markdown: Versioned Document Filenames"
dcterms:version: "0.2.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Opus 5.5 (Anthropic)"
dc:description: "House rule: before version 1.0.0, a versioned markdown document's filename is its identifier followed by its version in dotted form, joined by a single hyphen, or by a double hyphen when the identifier ends with a variant segment."
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
  - version: "0.2.0"
    date: "2026-10-03"
    author: "Christopher Steel"
    notes: >
      Added variant segments. A document published in more than one layout
      or form carries a trailing variant segment introduced by a double
      hyphen, and the version separator after a variant segment is also a
      double hyphen. Distinguished trailing variant segments from leading
      category prefixes, which use the same double hyphen but do not change
      the version separator. The variant segment is part of dc:identifier.
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

Version: 0.2.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This directive states how a versioned markdown document is named on disk while its version is below 1.0.0, including documents published in more than one variant, such as two layouts of the same source. It exists so that an AI collaborator names files correctly by default, at generation time, rather than inferring a pattern from whatever filenames happen to be in front of it.

## The rule

Before version 1.0.0, a versioned document's filename is its identifier, followed by a version separator, followed by its version written with a lowercase `v` and dots, followed by `.md`.

The version separator is a single hyphen, unless the identifier ends with a variant segment, in which case it is a double hyphen:

```text
<slug>-v<major>.<minor>.<patch>.md
<slug>--<variant>--v<major>.<minor>.<patch>.md
```

## Segments and separators

A double hyphen (`--`) separates the major segments of a name. A single hyphen joins the words within a segment. Two kinds of double-hyphen segment exist, and only one of them affects the version separator.

A category prefix comes first and states what kind of document this is, such as `markdown--`, `style-guide--`, or a source-document code such as `dge-60-vf--`. A category prefix does not change the version separator: `markdown--no-heading-numbers` is versioned as `markdown--no-heading-numbers-v0.4.1.md`.

A variant segment comes last and distinguishes one form of a document from another form of the same document, such as `--original-layout` and `--balise-layout`. When the identifier ends with a variant segment, the version separator is a double hyphen, so the version reads as a segment of its own: `...--balise-layout--v0.1.0.md`.

## Where each part comes from

The identifier is the document's `dc:identifier`, which never carries a version but does carry any variant segment. The version is the document's `dcterms:version`, prefixed with `v`. The two must agree: a document whose frontmatter says `dc:identifier: "example--balise-layout"` and `dcterms:version: "0.1.0"` is saved as `example--balise-layout--v0.1.0.md`.

Variants of the same document point at each other with `dc:relation`, naming the other variant's identifier.

When the version changes, the filename changes with it. Updating `dcterms:version` without renaming the file, or renaming the file without updating `dcterms:version`, leaves the document inconsistent. The same applies to adding, removing, or renaming a variant segment, which changes `dc:identifier` as well.

## Examples

Correct:

```text
markdown--no-heading-numbers-v0.4.1.md
style-guide--markdown-mermaid-navigation-flowcharts-and-linked-sections-v0.1.5.md
markdown--versioned-document-filenames-v0.2.0.md
dge-60-vf--scrutateur-et-secretaire-du-bureau-de-vote--original-layout--v0.2.1.md
dge-60-vf--scrutateur-et-secretaire-du-bureau-de-vote--balise-layout--v0.1.0.md
```

Incorrect:

| Filename | Problem |
| --- | --- |
| `markdown--no-heading-numbers-v0_4_1.md` | Underscores instead of dots |
| `markdown--no-heading-numbers-v0-4-1.md` | Hyphens instead of dots |
| `markdown--no-heading-numbers-0.4.1.md` | Missing the `v` |
| `markdown--no-heading-numbers_v0.4.1.md` | Underscore instead of a hyphen before the version |
| `markdown--no-heading-numbers--v0.4.1.md` | Double hyphen before the version without a variant segment; a category prefix does not count |
| `example--balise-layout-v0.1.0.md` | Single hyphen before the version after a variant segment |
| `markdown--no-heading-numbers.md` | Missing the version suffix before 1.0.0 |

Copies of documents whose filenames show underscored or hyphenated versions are not evidence of the convention. Name new and revised files by this rule, not by the pattern of nearby files.

## Scope

This directive covers versions below 1.0.0 only. The filename convention at 1.0.0 and later is not defined here.

## License

This document, *Markdown: Versioned Document Filenames*, by **Christopher Steel**, with AI assistance from **Claude Opus 5.5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.2.0 | Draft | Added trailing variant segments, which take a double-hyphen version separator; distinguished them from leading category prefixes, which do not; variant segments belong in `dc:identifier`, and variants point at each other with `dc:relation` |
| 0.1.0 | Draft | Initial draft; states the pre-1.0.0 filename convention `<slug>-v0.1.0.md` after an underscored suffix was inferred from uploaded filenames |
