---
dcterms:title: "Style Guide: Versioned Documents in Unrendered Markdown"
dcterms:version: "0.3.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "Conventions for creating versioned documents in SAT using unrendered markdown: filename patterns, frontmatter schema, document structure, and prose authoring rules. Authoritative for structure and naming across the repository's guides."
dcterms:created: "2026-07-21"
dcterms:modified: "2026-07-25"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "style-guide--versioned-documents-in-unrendered-markdown"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.3.0"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: >
      Designated the authoritative guide for structure, naming,
      frontmatter, and closing sections across the repository's guides,
      per ROADMAP.md Milestone 0.2.0. Register-and-audience guides now
      defer to it; it defers to the markdown automa for markdown-specific
      rules. Added Resources as an optional closing section so the one
      canonical closing sequence covers the register guides. Repaired the
      Changelog table, which listed only 0.1.0.
  - version: "0.2.0"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: >
      Recreated in the sat-doc-automa repository and brought into
      compliance with its own conventions and the markdown defaults.
      Added the frontmatter block this guide itself defines but did not
      previously carry. Removed heading numbers and horizontal rules.
      Retitled the H1 em dash to a colon. Revised two rules that
      conflicted with the markdown defaults: the section-numbering
      instruction now defers to Markdown: No Heading Numbers, and the
      em dash rule now defers to Markdown: Use Commas, Not Em Dashes.
  - version: "0.1.0"
    date: "2026-07-21"
    author: "Christopher Steel"
    notes: "Initial draft."
---

# Style Guide: Versioned Documents in Unrendered Markdown

Version: 0.3.0
Status: Draft
Style Guide: self-referential

## Abstract

This guide defines the conventions for creating versioned documents in SAT using unrendered markdown. It covers filename patterns, frontmatter schema, document structure, and prose authoring rules. It is written to be read as plain text and to render cleanly in any markdown renderer without relying on either for correctness.

This guide is authoritative for document structure, filename patterns, frontmatter schema, and closing sections across the repository. The register-and-audience guides (*Technical Documentation for Technologists*, *Plain Language for General Audiences*, *Web-Ready Unrendered Markdown Using APA 7*, and *Navigation and Accessibility*) govern voice, register, audience, and citation practice, and defer to this guide on structure and naming. This guide in turn defers to the markdown automa in `automa/markdown/defaults/` for the markdown-specific rules they define, heading numbers, em dashes, horizontal rules, and license statement form.

## Filename conventions

### The stable filename is the slug

At stable release (`v1.0.0` and above), the filename is the slug alone, no version suffix.

```
cascade-resolution-specification.md
universal-cake--an-introduction.md
```

The `sat:uuid` carries document identity. The filename can evolve without loss of continuity.

### Pre-release files carry a version suffix

While a document is at major version zero (`v0.n.n`), the version suffix is appended to the slug using hyphens as separators.

```
cascade-resolution-specification-v0-1-0.md
universal-cake--an-introduction-v0-2-7.md
```

The hyphen separator pattern (`v0-1-0`) is mandatory. Dots and underscores are not used in the suffix.

### Major version zero signals pre-release status

A `v0.n.n` version indicates the document is pre-release. No additional alpha, beta, or rc label is added to the filename. The version number is the signal.

### Filename maturation is a first-class obligation

The pre-release period exists partly to arrive at a correct, fully self-describing filename before the version suffix is dropped at stable release. The filename must be readable without surrounding context, by a person navigating a command line or using assistive technology. Treat filename review as part of every version cycle.

### Slug construction rules

Slugs are lowercase ASCII letters, digits, and hyphens only. No spaces, underscores, or special characters. A single hyphen (`-`) separates words within a group. A double hyphen (`--`) marks a semantic boundary between groups.

```
sat-radar-entry-template         ← single group
universal-cake--an-introduction  ← two groups: concept -- subtitle
adr-015-slug-pattern-language    ← two groups: series-number -- title
```

## Frontmatter

SAT documents in the working document model (pre-ADR-012 migration) carry a YAML frontmatter block. All fields use the `dcterms:` namespace. SAT-specific fields use the `sat:` namespace.

### Required fields

```yaml
---
dcterms:title: "Human-readable title of the document"
dcterms:version: "0.1.0"
dcterms:creator: "Author Name"
dcterms:description: "One sentence describing this document."
dcterms:created: "YYYY-MM-DD"
dcterms:modified: "YYYY-MM-DD"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "the-slug-without-version-suffix"
dcterms:rightsHolder: "Rights Holder Name"
dcterms:rights: >
  Copyright YYYY Rights Holder.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.n.n"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "YYYY-MM-DD"
    author: "Author Name"
    notes: "Initial draft."
---
```

### Optional fields

Include these when the values are known and meaningful:

```yaml
dcterms:contributor: "Contributor Name"
dcterms:subject:
  - "keyword"
  - "keyword"
dcterms:publisher: "Publisher or Organisation"
dcterms:type: "Text"
dcterms:source: ""
dcterms:relation: ""
```

### Namespace rules

Use `dcterms:` (Dublin Core Terms) throughout. The legacy `dc:` (Dublin Core Elements) prefix is deprecated in SAT. Do not mix namespaces in a single document.

### The `dcterms:identifier` field

This is the slug of the document, without the version suffix, regardless of the version the document is currently at. It is the stable identity of the document expressed as a string.

```yaml
dcterms:identifier: "cascade-resolution-specification"
```

### The `sat:uuid` field

Leave `sat:uuid` as an empty string in a new document. It is populated at ingress by the SAT tool or by the author at creation time. Once set, it is never changed.

### The `sat:version_at_creation` field

This records the version of the SAT system at the time the document was created, not the document's own version. It is distinct from `dcterms:version`.

### Changelog entries

Each changelog entry records the document version, the date, the author, and a note describing the change. Notes use the YAML `>` block scalar for multi-line entries or a plain quoted string for short entries.

```yaml
sat:changelog:
  - version: "0.2.0"
    date: "2026-06-18"
    author: "Author Name"
    notes: >
      Rewrote section 3 to clarify cascade resolution semantics.
      Added examples for the three resolution paths.
  - version: "0.1.0"
    date: "2026-06-01"
    author: "Author Name"
    notes: "Initial draft."
```

Entries are listed newest-first.

## Document structure

### The H1 heading

The H1 is the document title. It is the first line of the document body, immediately after the closing `---` of the frontmatter. There is exactly one H1 per document.

```markdown
# Style Guide: Versioned Documents in Unrendered Markdown
```

### Version line

Immediately below the H1, place a compact version block. This makes the version and status visible without frontmatter parsing.

```
Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown
```

The `Style Guide:` line names the governing style guide slug. A self-referential document may write `self-referential` until the document reaches stable release.

### Abstract

The first section is `## Abstract`. It is a short paragraph, two to five sentences, that answers: what is this document, and what does it cover? It does not repeat the title.

### Section headings

Use ATX headings (`#`, `##`, `###`) only. Do not use Setext underline headings. Headings do not skip levels.

Do not number headings. If numbered headings would genuinely aid navigation in a specific document, ask before adding them (see *Markdown: No Heading Numbers* in this repository's markdown defaults).

### Closing sections

End every versioned document with these sections, in this order. Sections marked optional are omitted when they would be empty.

**License**, the document's licence statement, using the author name and the SPDX identifier.

**Resources** (optional), a topic-grouped list of sources that links to their reference anchors, not to raw URLs. Register-and-audience guides that carry a Resources section place it here; structural documents omit it.

**References** (optional), APA 7 formatted references for any cited works. Omit this section if there are no citations.

**Changelog**, a markdown table with columns `Version`, `Status`, and `Notes`. Entries are listed newest-first.

This is the one canonical closing sequence. Document classes vary only by which optional sections they carry, not by reordering the sequence.

```markdown
## License

This document, *Title of Document*, by **Author Name**, with AI assistance
from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the
[GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.2.0 | Draft | Recreated in sat-doc-automa; added the frontmatter this guide defines but lacked; removed heading numbers and horizontal rules; H1 em dash retitled to colon; section-numbering and em dash rules revised to defer to the markdown defaults |
| 0.1.0 | Draft | Initial draft |
```

## Prose authoring rules

### No hard line wraps in prose

Do not wrap prose at 80 characters or any fixed column. Let lines run to their natural length. Hard wraps are appropriate only inside code blocks. This rule applies whether the document is viewed rendered or unrendered.

### Code blocks

Use fenced code blocks (triple backtick) with a language tag. Indented code blocks are not used in SAT documents.

````markdown
```yaml
dcterms:title: "Example"
```
````

### Emphasis

Use `*italic*` for titles of works and for introducing terms. Use `**bold**` sparingly, only for the single most important term in a definition or warning. Do not bold for decoration.

### Em dashes are not used

Do not use em dashes in prose; use paired commas for parenthetical asides instead (see *Markdown: Use Commas, Not Em Dashes* in this repository's markdown defaults). Do not use ` -- ` (double hyphen) in prose either. The double hyphen is reserved for slugs as a grouping separator.

### Lists

Use lists when items are genuinely enumerable and parallel. Do not use a list where a sentence would read more clearly. Bullet marker is `-`. Ordered list marker is `1.`, `2.`, etc.

### Tables

Tables are appropriate for structured reference data, field names, version histories, rule sets. They are not appropriate for flowing information that belongs in prose. Use the pipe-delimited GFM table syntax.

## Versioning the document

### Semantic versioning

SAT documents follow semantic versioning (`MAJOR.MINOR.PATCH`). For documents, interpret the parts as:

- **PATCH**, corrections, typo fixes, wording clarifications that do not change meaning
- **MINOR**, new content, new sections, substantial rewrites of existing sections
- **MAJOR**, structural changes that alter the document's purpose or audience; graduation from pre-release to stable

### Version zero

Documents at `v0.n.n` are pre-release. They may change substantially between versions. The filename carries the version suffix during this period.

### Graduating to stable

At `v1.0.0`, the version suffix is dropped from the filename. The document's own version history (in `sat:changelog` and in the Changelog table) records the progression. The `sat:uuid` ensures all references and citations remain valid through the rename.

### Updating the changelog and frontmatter together

When bumping a version, update `dcterms:version` in the frontmatter, update `dcterms:modified` to today's date, and add a changelog entry. These three changes are always made together.

## License

This document, *Style Guide: Versioned Documents in Unrendered Markdown*, by **Christopher Steel**, with AI assistance from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.3.0 | Draft | Designated authoritative for structure, naming, frontmatter, and closing sections; added Resources as an optional closing section; repaired this table, which previously listed only 0.1.0 |
| 0.2.0 | Draft | Recreated in sat-doc-automa; added the frontmatter this guide defines but lacked; removed heading numbers and horizontal rules; H1 em dash retitled to colon; section-numbering and em dash rules revised to defer to the markdown defaults |
| 0.1.0 | Draft | Initial draft |
