---
dcterms:title: "Style Guide: Technical Documentation for Technologists"
dcterms:version: "0.4.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "Governs the authoring of technical documentation for technologists: research-paper-flavoured register, decision rationale requirements, and conceptual boundary documentation."
dcterms:created: "2026-07-23"
dcterms:modified: "2026-07-24"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "style-guide--technical-documentation-for-technologists"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.4.0"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: "Recreated in the sat-doc-automa repository and brought into compliance with the markdown defaults: spaced em dashes replaced with commas, H1 double hyphen replaced with a colon and capitalization corrected, governing style guide reference line added. Known drafting rough edges in the body retained for author revision per the guide's own authoring process."
  - version: "0.3.0"
    date: "2026-07-23"
    author: "Christopher Steel"
    notes: "Migrated into the sat-doc-automa repository. Added frontmatter. Resolved a version inconsistency in the source (filename said 0.2.0, version block said 0.1.1) by superseding both with 0.3.0. Body content unchanged; known drafting rough edges retained for the author to revise per the guide's own authoring process."
---

# Style Guide: Technical Documentation for Technologists

Version: 0.4.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Purpose

This style guide governs the authoring of technical documentation for technologists

It exists to ensure for consistency across sessions and versions of the document.

It should may be provided to any collaborators, human or AI at the start of a new project of session involving the creation of technical documentation for technologists.

## Versioning This Style Guide

The style guide itself is versioned using semantic versioning (MAJOR.MINOR.PATCH):

- **PATCH**, spelling, grammar, or clarification of existing rules with no change to intent
- **MINOR**, new rules added, or existing rules meaningfully refined
- **MAJOR**, a fundamental change in approach, audience, or scope

The version and status (Draft, Review, Stable) appear in the header of this document and targeted documents .

Changes should be noted at the bottom of the document in a changelog section.

The style guide version in use should be referenced in the header of any document it governs.

## Intended Reader

A technical peer who has a good understands of the technologies involved but needs to better understand the structure of the implementation and the decisions behind it.

The goal is transparency and clear understanding of provenience as well as longer term goals so the reader should be able to follow not just what was built but why
decisions where as made, what alternatives were considered and how this reflects organizational values and goals.

## Voice and Register

Write in the author's voice. Correct spelling and grammar but do not rewrite. Offer suggestions for improvements in clarity and writing as a summary. Then go through on one section at a time, offering any suggestions section by section until the author is satisfied.

These documents should register is research paper flavoured, precise, considered, and direct. Avoiding 
conversational filler, marketing language, and unnecessary qualification.

Use first person plural ("we chose", "we considered") when describing decisions and rationale.

Use third person ("the shim does not", "the orchestrator connects") when describing how components behave.

## Tone by Section Type

**Historical and existing implementation(s)**, concise and precise. State what exists and the version in use. Do not over-explain what can be shown. Note the version of
tools and implementations being described.

**Changes and new implementations**, more expansive. Document the parameters considered, the alternatives evaluated, and the rationale for the decision made. The guiding principle for all implementation decisions is: make it work, make it correct, make it fast, in that order.

**Conceptual boundaries**, the most detailed treatment is reserved for transitions between concepts, particularly the egress/ingress boundaries between tools.

These sections must define the full contract: structured output, operator visibility and logging, not just the minimal connection details.

## Decisions and Rationale

Every significant decision must document:

1. What was decided
2. Why it was decided
3. What alternatives were considered and why they were not chosen
4. Links to any resulting ADR's

This applies especially at conceptual boundaries where the design of one component affects another. For example:

* Cascading configurations
* Operator variables
* egress from one tool and ingress of another
* changes to that contract between the old and new implementations.

## Terminology

Prefer generic terms over specific tool names when the concept is more important than the implementation.

This aids in building the vocabulary for tech a tech stack that aims to allow for easier pivots over time via agnostic approaches that support accessibility and sovereignty as well as user, operator and community well being.

For example: "orchestrator" rather than "Ansible" in sections that describe the pattern rather than the specific tool or tools.

When a specific tool is named, note its version if the section describes a historical or existing implementation.

Examples of definition that might be used:

- **Shim**, the thin, provider-specific layer responsible for creating the server, injecting the SSH key, and configuring the bootstrap firewall. Knows nothing about what the machine will eventually do.
- **Orchestrator**, the system that connects to the normalised SSH baseline the shim produces and applies configuration in layers.
- **Egress**, the full output of the shim: structured data, operator-visible output,  and logs produced at the end of a shim run.
- **Ingress**, the full input the orchestrator requires to begin its run: connection details, credentials, inventory, and any operator or log data passed across the boundary.
- **Bootstrap firewall**, the minimal firewall configured by the shim. Permits only what is necessary to establish a secured orchestrator connection.
- **Sovereign**, self-contained, free of external dependencies, (proprietary services and technologies) and portable across providers and environments.

## Structure

Documents governed by this style guide follow this general structure:

1. **The old implementation**, concise description of the existing approach, tools, versions, and known limitations
2. **The new implementation**, detailed description of the new approach, decisions, parameters considered, and rationale
3. **Any egress/ingress boundary**, explicit definition of the contract between shim and orchestrator, noting what changes between old and new
4. **Implementation**, production-ready code (python preferred) and configuration (yaml prefered), directly usable

Sections are composed paragraph by paragraph. Each paragraph is agreed before proceeding to the next. Use standard markdown headings. Never use bold in markdown headings

`##` for major sections.
Demark markdown heading using:
* `#` Document Title
*  `##` Major Sections
*  and `###`, `####` `#####` and `######` for nested subheadings

## Code and Examples

All code must be production ready and directly usable. Illustrative placeholders are not acceptable. Where a value is environment-specific, use a clearly named variable or note the value explicitly.

Version pin all dependencies. Note the version of any tool, provider, or library
referenced in code.

## Authoring Process

Work one paragraph at a time. Agree each paragraph before moving to the next.
Spelling and grammar are corrected by the collaborator without changing the author's
intent or voice. Factual corrections are flagged as questions before being applied.

At the start of each new session, provide this style guide and the current state of
the document being worked on. This gives a new collaborator the context needed to
continue coherently.

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.4.0 | Draft | Recreated in sat-doc-automa; compliance pass: em dashes to commas, H1 retitled with colon, style guide reference line added; drafting rough edges retained for author revision |
| 0.3.0 | Draft | Migrated into the sat-doc-automa repository; added frontmatter; resolved the filename (0.2.0) vs version block (0.1.1) inconsistency by superseding both; body content unchanged |
| 0.1.0 | Draft | Initial draft derived from working session |
| 0.2.0 | Draft | Rewrite |
