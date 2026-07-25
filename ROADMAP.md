---
dcterms:title: "sat-doc-automa Roadmap"
dcterms:version: "0.2.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "Planned work for the sat-doc-automa repository, sequenced by target repository version, with the governing-hierarchy decisions resolved and the compliance work applied."
dcterms:created: "2026-07-25"
dcterms:modified: "2026-07-25"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "roadmap"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.2.0"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: >
      Resolved every scheduled item. Recorded the seven governing-hierarchy
      decisions with their alternatives and rationale in a new Decisions
      section. Marked Milestones 0.2.0, 0.3.0, and 0.4.0 resolved, item by
      item, with what was decided and applied. Answered the three open
      questions. Milestone 1.0.0 remains forward-looking; the criteria it
      still gates on are noted. Produced with Claude Opus 4.8; the 0.1.0
      draft was produced with Claude Opus 5, per the model-attribution
      decision recorded below.
  - version: "0.1.0"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: >
      Initial draft. Records the findings of the first full read of the
      repository at VERSION 0.1.2, sequenced into target releases. The
      governing-guide decision is placed first because the compliance work
      in later milestones cannot be completed correctly without it.
---

# sat-doc-automa Roadmap

Version: 0.2.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This roadmap records the planned work for the sat-doc-automa repository, sequenced by target repository version, and its resolution. It covers one directional decision, which style guide is authoritative, and the remediation work that follows from it. As of version 0.2.0 every scheduled item is resolved: the governing-hierarchy decisions are recorded below, and the compliance work has been applied to the documents. Milestone 1.0.0, graduation, remains forward-looking because two of its criteria depend on work outside this roadmap's scope. The repository was at VERSION 0.1.2 when this work was done.

## How to read this roadmap

Each milestone states what it was for and records its resolution. Every scheduled item carries a real heading so it can be linked to from commit messages, issues, and other documents, per *Style Guide: Navigation and Accessibility*, and a **Status** line stating how it was resolved. Purely mechanical corrections are collected into a table, since a table is the right form for structured reference data and a link target is not useful for a single typo.

Version impact notes use the semantic versioning definitions in *Style Guide: Versioned Documents in Unrendered Markdown*, applied to the affected document, not to the repository.

## Decisions

The versioned-documents guide requires that a directional decision record what was decided, the alternatives considered, and the rationale. The seven decisions that Milestone 0.2.0 turned on are recorded here so the later milestones can reference them.

### D1: The authoritative style guide

*Style Guide: Versioned Documents in Unrendered Markdown* is authoritative for document structure, filename patterns, frontmatter schema, and closing sections across the repository. The register-and-audience guides (*Technical Documentation for Technologists*, *Plain Language for General Audiences*, *Web-Ready Unrendered Markdown Using APA 7*, and *Navigation and Accessibility*) govern voice, register, audience, citation practice, and heading semantics, and defer to the versioned-documents guide on structure and naming. The versioned-documents guide in turn defers to the markdown automa for the markdown-specific rules they define.

The alternative considered was a flat set of peers with no designated authority, which is the state that produced the contradictions this roadmap catalogues. It was rejected because overlapping rules with no tie-breaker cannot be resolved except by rewriting one guide to match another arbitrarily. A named authority makes every later reconciliation a deference rather than a negotiation.

### D2: Filename version separator

Hyphens, always: `v0-1-0`, never `v0.1.0`. The alternative, the plain-language guide's rationale that dots keep the version machine-detectable, was answered rather than overruled silently: a hyphenated suffix is equally machine-detectable with a fixed pattern (`-v\d+-\d+-\d+`), and the double-hyphen semantic separator already gives the repository a consistent hyphen grammar. Dotted versions in filenames are now caught by the conformance checker.

### D3: Numbered body sections

Body sections are not numbered. Both register guides that specified numbered body sections now defer to *Markdown: No Heading Numbers*, which already carries the "ask first" carve-out. The alternative, amending the automa to exempt these document classes, was rejected because the automa's existing exception (ask before adding numbers when they genuinely aid navigation) already covers the legitimate case without a standing exemption.

### D4: Closing sections

One canonical closing sequence: **License**, then **Resources** (optional), then **References** (optional), then **Changelog**. Resources and References are omitted when empty. Document classes vary only by which optional sections they carry, never by reordering. This reconciled three competing lists: the versioned-documents guide's License/References/Changelog, and the two register guides' Resources-before-References lists that omitted License entirely.

### D5: Bullet markers and heading case

Hyphen (`-`) bullets everywhere; asterisks are not used. Headings below the H1 are sentence case; the H1 title is title case; proper nouns and acronyms keep their case. This resolved the technical-documentation guide's asterisk bullets and title-case headings and the APA 7 guide's own title-case headings against the hyphen-and-sentence-case rules the other guides already stated.

### D6: Collaboration format directory

`ai-collaboration`, matching the README and the file's actual location. The document's `collaboration--` identifier prefix is kept, since the identifier names the format (collaboration) while the directory names its place in the tree.

### D7: Meaning of sat:version_at_creation

The field records the SAT system version at the time the document was created, not the document's own version. It is uniform at `0.4.0` across the repository. The one outlier, the CNCF reference at `0.3.1`, was an error and was corrected to `0.4.0`.

## Milestone 0.2.0: Establish the governing hierarchy

Three style guides gave overlapping and partly contradictory rules for the same things: filename patterns, heading numbering, required sections, bullet markers, and emphasis. This milestone made the decisions the compliance work depends on. It is resolved: see the Decisions section for the decisions themselves, and the items below for how each was applied.

### Designate the authoritative style guide

**Status: Resolved (D1).** The versioned-documents guide (now 0.3.0) states its authority in its Abstract. Each register guide carries an explicit deference statement in the same inline form the versioned-documents guide uses when it defers to the markdown automa.

Affected: all five style guides. Version impact: MINOR for each, applied.

### Resolve the filename version separator conflict

**Status: Resolved (D2).** The plain-language and APA 7 guides use the hyphen pattern. The conformance checker now flags dotted filename versions, and the one new file that had reintroduced the dot (the CNCF reference) was renamed.

Affected: *Plain Language for General Audiences*, *Web-Ready Unrendered Markdown Using APA 7*. Version impact: MINOR.

### Resolve the numbered body sections conflict

**Status: Resolved (D3).** The plain-language Structure section and the APA 7 Required sections list no longer specify numbered body sections; both defer to *Markdown: No Heading Numbers*.

Affected: *Plain Language for General Audiences*, *Web-Ready Unrendered Markdown Using APA 7*. Version impact: MINOR.

### Reconcile the required closing sections

**Status: Resolved (D4).** The versioned-documents guide now defines the one canonical closing sequence, with Resources as an optional section. The register guides' section lists were reordered to match, and License was added where it had been omitted.

Affected: three style guides. Version impact: MINOR.

### Reconcile bullet markers and heading case

**Status: Resolved (D5).** The technical-documentation guide's asterisk bullets became hyphens and its title-case body headings became sentence case; the APA 7 guide's own title-case headings were corrected. The energy conservation directive's one title-case heading was corrected.

Affected: all guides, plus the energy conservation directive. Version impact: PATCH for the corrections, MINOR where a rule was added.

### Settle the collaboration format directory name

**Status: Resolved (D6).** The directive's Placement prose and code block name `ai-collaboration`, matching the README and the file's location.

Affected: the directive's Placement section. Version impact: PATCH, folded into the directive's 0.2.0 bump.

### Confirm the meaning of sat:version_at_creation

**Status: Resolved (D7).** The field records the SAT system version; it is uniform at `0.4.0`, and the CNCF outlier was corrected.

Affected: the CNCF reference. Version impact: PATCH.

## Milestone 0.3.0: Bring documents into compliance

With the hierarchy settled, each document was brought into line and bumped once, so that a document was not touched three times for three separate rules.

### Repair the versioned-documents guide's own changelog

**Status: Resolved.** The Changelog table now carries the 0.2.0 and 0.3.0 rows. Bumped to 0.3.0.

### Repair the APA 7 guide's changelog table

**Status: Resolved.** The malformed 0.2.2 rows are one well-formed row, and the stale numbered-section references ("section 1.1", "section 2.4") were removed from the changelog notes. Bumped to 0.5.0.

### Add a License section to the technical-documentation guide

**Status: Resolved.** The technical-documentation guide now carries a License section. During this work the APA 7 guide was found to be *also* missing one (the original roadmap's claim that the technical guide was the only document without a License was inaccurate); both were fixed. Bumped to 0.5.0 each.

### Reorder the technical-documentation guide's changelog

**Status: Resolved.** The Changelog table runs newest-first (0.5.0, 0.4.0, 0.3.0, 0.2.0, 0.1.0).

### Correct the navigation-accessibility identifier

**Status: Resolved.** The identifier is `style-guide--navigation-accessibility`, with the double hyphen. Bumped to 0.2.0.

### Correct the APA 7 guide identifier and naming layers

**Status: Resolved.** Title, H1, `dcterms:identifier`, and filename now agree on the `style-guide--` prefix: the identifier is `style-guide--web-ready-unrendered-markdown-using-apa-7` and the title carries the `Style Guide:` prefix.

### Correct the energy conservation directive's arithmetic

**Status: Resolved.** The one-team-of-ten water figure is 33 litres per day, not 3.3, and the annual and thousand-team figures scale from it. The per-year figures now state the 260-working-day basis explicitly. Bumped to 0.2.0.

### Bring the energy conservation directive's citations into the CAP workflow

**Status: Resolved.** Every in-text citation carries a CAP anchor pair, and the References section carries reference anchors with return links. The Epoch AI in-text citation was corrected to match its reference entry, filed under You, J. (2025).

### Remove the em dash from the commit workflow example

**Status: Resolved.** The initial-commit example reads `"Initial commit, v0.1.0"`. Bumped to 0.1.1.

### Copy-edit pass

**Status: Resolved.** Every correction in the table below was applied.

| Document | Correction |
|----------|------------|
| Energy conservation directive | `todays` to `today's` |
| Energy conservation directive | `live giving` to `life giving`, two occurrences |
| Energy conservation directive | Missing terminal periods on three of the five bullets in The Reality |
| Technical-documentation guide | `provenience` to `provenance` |
| Technical-documentation guide | `has a good understands` to `has a good understanding` |
| Technical-documentation guide | `It should may be provided` |
| Technical-documentation guide | `a new project of session` to `or session` |
| Technical-documentation guide | `These documents should register is research paper flavoured` |
| Technical-documentation guide | `decisions where as made` |
| Technical-documentation guide | `ADR's` to `ADRs` |
| Technical-documentation guide | `yaml prefered` to `preferred` |
| Technical-documentation guide | `for a tech a tech stack` |
| Technical-documentation guide | `targeted documents .` stray space before the period |
| Technical-documentation guide | Double space inside the Egress definition |
| Technical-documentation guide | Garbled Structure section, a fragment precedes a marker list that repeats it |
| Plain-language guide | Double hyphen in prose when naming the technical guide, two occurrences |
| Plain-language guide | Changelog reference to "section 8.1", a stale numbered-section reference |
| Navigation-accessibility guide | Second W3C URL points at WCAG20 rather than WCAG21 |

## Milestone 0.4.0: Tooling and the repository record

The repository had version discipline for documents and almost none for itself. Resolved.

### Write bump-doc-versions.py or remove the reference to it

**Status: Resolved.** The reference was removed. `bump-version.py` now states that document version lines and changelogs are updated by hand as part of each document's own bump. A second tool was not written; the manual step is small and the promise of a tool that did not exist was the actual defect.

### Add a repository-level changelog

**Status: Resolved.** `CHANGELOG.md` at the repository root records the 0.1.0, 0.1.1, and 0.1.2 releases (reconstructed from the tags and their contents) and an Unreleased section for this compliance work.

### Consider a conformance check

**Status: Resolved (built).** `check-conformance.py` reports the mechanically-detectable issues in this roadmap: dotted filename versions, missing required frontmatter fields, an identifier that does not match the filename slug, em dashes in prose, asterisk bullets, and numbered headings. It is a linter, changes nothing, and exits non-zero on any finding so it can gate a commit. It reports zero issues across the repository as of this version.

## Milestone 1.0.0: Graduation

Criteria for dropping the version suffix from document filenames and declaring the conventions stable. Two criteria are now met; three remain, two of them gated on work outside this roadmap.

- One authoritative style guide, with every other guide explicitly deferring to it. **Met (D1).**
- No contradictions between any two documents in force. **Met**, as of this compliance pass.
- Every document carrying a populated `sat:uuid`. **Not met**, and gated: the versioned-documents guide specifies that `sat:uuid` is populated at ingress by the SAT tool, which does not yet exist. Every document carries an empty `sat:uuid` deliberately.
- Every document reviewed for filename maturity, which the versioned-documents guide names as a first-class obligation of the pre-release period. **In progress**: every filename was reviewed and renamed to its current version this pass; maturity review continues each version cycle.
- Status advanced from Draft through Review to Stable on each document. **Not met**: every document is still Draft. This is an editorial gate, not a mechanical one, and is the last step before graduation.

## Open questions

These are now answered.

### Where this roadmap lives

**Resolved.** This file is `ROADMAP.md` at the repository root, alongside `README.md`, `CHANGELOG.md`, and `VERSION`. The stated exception the original draft asked for: root operational files are the repository's stable front matter and do not carry a version-suffixed filename. Their version, where they have one, lives in the document's own version block and frontmatter, as this document's does. The alternative, `roadmap-v0-1-0.md` under `en/docs/`, was rejected because it would rename the repository's front door on every version bump and break external links to it.

### How mixed-model AI attribution is recorded

**Resolved.** The License section names the model that produced the current version. The per-version record of which model produced which version lives in the changelog. When a single version was produced across several models, name the one that produced the majority of the current text and note the others in that version's changelog entry. Accordingly, this document's License names Claude Opus 4.8, which produced 0.2.0, and the changelog records that 0.1.0 was produced with Claude Opus 5.

### Whether the automa should be numbered or ordered

**Resolved.** The automa remain a flat set with no inherent precedence. When two directives appear to conflict, the governing hierarchy resolves it: the authoritative versioned-documents guide and each document's explicit deference, not an ordering among the automa. This is revisited only if the set grows enough that genuine conflicts arise. Nothing conflicts today.

## License

This document, *sat-doc-automa Roadmap*, by **Christopher Steel**, with AI assistance from **Claude Opus 4.8 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.2.0 | Draft | Resolved every scheduled item; recorded the seven governing-hierarchy decisions with rationale; marked Milestones 0.2.0, 0.3.0, and 0.4.0 resolved item by item; answered the three open questions; noted the remaining 1.0.0 graduation criteria |
| 0.1.0 | Draft | Initial draft, findings from the first full read of the repository at VERSION 0.1.2, sequenced into target releases |
