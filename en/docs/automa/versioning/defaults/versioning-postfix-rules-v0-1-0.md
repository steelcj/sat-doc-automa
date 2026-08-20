---
dc:title: "Versioning Postfix Rules"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Opus 5 (Anthropic)"
dc:description: "House rule: a pre-1.0.0 document carries its version in the filename as a hyphenated postfix; once 1.0.0 is attained the postfix is dropped and the filename becomes stable."
dcterms:created: "2026-08-12"
dcterms:modified: "2026-08-12"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "versioning-postfix-rules"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.2.2"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-12"
    author: "Christopher Steel"
    notes: >
      Initial draft. Written after a repository audit found two competing
      version postfix forms split by location, dotted inside radar/ and
      hyphenated everywhere else, with no directive stating which was
      correct. The hyphenated form was already implied by the file naming
      section of the web-ready APA 7 style guide but was stated only as an
      example, so it did not survive contact with a directory that had
      drifted. This directive states the rule directly and adds the
      drop-at-1.0.0 half, which was not previously recorded anywhere.
---

# Versioning Postfix Rules

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## The rule

A document filename takes this shape:

```
<title-slug>-<version-postfix>.<file-extension>
```

The version postfix is the letter `v` followed by the document's semantic version, with hyphens in place of the dots.

| Document version | Filename                                      |
| ---------------- | --------------------------------------------- |
| 0.1.0            | `markdown--no-hard-line-wraps-v0-1-0.md`      |
| 0.3.1            | `markdown--use-commas-not-em-dashes-v0-3-1.md` |
| 0.5.0            | `style-guide--plain-language-for-general-audiences-v0-5-0.md` |

Once the document reaches version 1.0.0, the version postfix is no longer used. The filename becomes the title slug and the extension alone, and it stays that way for every subsequent version.

| Document version | Filename                    |
| ---------------- | --------------------------- |
| 1.0.0            | `<title-slug>.md`           |
| 1.2.0            | `<title-slug>.md`           |
| 2.0.0            | `<title-slug>.md`           |

Dropping the postfix at 1.0.0 is a one-way transition. A document that has reached 1.0.0 does not reacquire a postfix, even if later work is substantial.

## Why the version lives in the filename before 1.0.0 and not after

Before 1.0.0 a document is still finding its shape. Successive drafts are often worth keeping side by side, and a reader needs to see at a glance which one they have without opening it. Encoding the version in the name makes that visible in a directory listing and makes divergent drafts impossible to confuse.

After 1.0.0 the document has a settled identity, and the cost reverses. A filename that changes with every release breaks every link, bookmark, and cross-reference pointing at it, and each release silently orphans the last set of references. A stable name is worth more at that point than an at-a-glance version, which the version block and changelog inside the document already provide.

## Why hyphens and not dots

A dot separates a filename from its extension. Using dots inside the version postfix puts several of them in one name, so tooling that splits on a dot has to be told which one matters, and different tools choose differently. Splitting on the first dot and splitting on the last dot give different answers for `report-v0.1.0.md`, and neither answer is wrong in general.

Hyphens keep exactly one dot in the filename, so the extension is unambiguous to anything that reads it. This also keeps version postfixes consistent with the rest of the naming scheme, which is already lowercase and hyphen-separated throughout.

## What the postfix does not carry

The version postfix carries the version and nothing else. Status, review state, and working markers do not belong in a filename.

- `report-v0-1-1-draft.md` is wrong. Status belongs on the `Status:` line of the version block.
- `analysis-v0-1-0-X.md` is wrong. A working marker belongs in a branch, a scratch directory, or nowhere.
- `report--v0-1-0.md` is wrong. A single hyphen separates the slug from the postfix, even where the slug itself uses double hyphens internally to separate its own segments.

A file whose name needs to say something the version postfix cannot express is a file whose title slug should say it instead.

## Scope

This directive applies to every published document artifact regardless of format, including markdown sources and any rendered output such as PDF. A document and its rendered siblings share one title slug and one version postfix, so that they sort together and can be seen to correspond.

It does not apply to files that are not versioned documents: source code, configuration, README files that describe a directory rather than carry a version, and license blocks that are identified by their content rather than a version.

## License

This document, *Versioning Postfix Rules*, by **Christopher Steel**, with AI assistance from **Claude Opus 5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft. States the hyphenated postfix form directly rather than by example, adds the drop-at-1.0.0 rule, and records what the postfix must not carry |
