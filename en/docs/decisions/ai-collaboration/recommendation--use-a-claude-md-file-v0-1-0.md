---
dcterms:title: "Recommendation: Use a CLAUDE.md File"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:contributor: "Claude (Anthropic) — drafting assistance"
dcterms:description: "Recommends adding a small CLAUDE.md signpost file to sat-doc-automa and to every project it feeds, so AI work sessions load the standing automa directives automatically instead of depending on a person to point to them."
dcterms:created: "2026-08-02"
dcterms:modified: "2026-08-02"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "recommendation--use-a-claude-md-file"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:repository: "sat-doc-automa"
sat:path: "en/docs/decisions/ai-collaboration/"
sat:version_at_creation: "0.1.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: "Initial draft: the signpost design, the worked example file, distribution through file-fairy, and the limits of the mechanism."
---

# Recommendation: Use a CLAUDE.md File

Version: 0.1.0
Status: Draft
Style Guide: style-guide--plain-language-for-general-audiences

## Abstract

This document recommends adding a small file named CLAUDE.md to sat-doc-automa, and later to every project it feeds. The file makes sure that AI work sessions load the project's standing rules automatically. It explains what the file is, what belongs in it, what stays out, and why. It is written for anyone who works in these projects, with or without an AI partner.

## What a CLAUDE.md file is

A CLAUDE.md file is a plain text file that sits at the top of a repository. A repository is the folder that holds a project and its history. When a Claude session starts work inside that folder, it reads the file on its own <a name="apa-anthropic-citation"></a>([Anthropic, 2026](#apa-anthropic-reference)). Nobody has to remember to point to it. The file is ordinary markdown, so people can read it too.

## The gap this closes

This repository already has rules for AI collaboration. They live in `en/docs/automa/ai-collaboration/defaults/`, and every file in that folder is in force by definition. The markdown rules in `en/docs/automa/markdown/defaults/` work the same way.

But rules only work if the reader has seen them. A new AI session starts with no memory. Today, a person must paste the rules in, or point to them, at the start of every session. That step is easy to forget. When it is forgotten, the session breaks rules it never saw. The result looks like carelessness, but it is really a loading problem.

A CLAUDE.md file closes that gap. The rules get loaded because the file is loaded, every session, with no human step.

## The recommendation

Add a short CLAUDE.md file to the root of sat-doc-automa. Make it a signpost, not a rulebook.

A signpost file does three things. It names the rules that are in force. It says where each rule lives. It says what to do when the signpost and a rule disagree: the rule wins.

The rules themselves stay where they are, in the automa documents. Nothing moves. Nothing is copied.

## Why a signpost and not a rulebook

This was the main design choice, so the reasons are recorded here.

First, copies drift. If the rules were pasted into CLAUDE.md, the project would hold two versions of every rule. One would go stale. This repository exists to fight exactly that problem, so it should not create a new case of it.

Second, short files work better. Claude follows a short, specific file more reliably than a long one. The guidance from Anthropic is to keep the file under 200 lines <a name="apa-anthropic-citation-2"></a>([Anthropic, 2026](#apa-anthropic-reference)).

Third, loading everything costs energy. CLAUDE.md can pull whole documents into a session using a special import syntax. But the automa documents carry front matter, references, and changelogs that most sessions never need. Loading all of that, every session, works against the energy conservation directive this repository already follows. A signpost names the rule in one line and lets the session read the full document only when it needs to.

One alternative was considered and set aside: writing no file at all and relying on people to point to the rules. That is the current state, and the gap it leaves is described above.

## What the file says

Here is the recommended content. It is ready to use as written.

```markdown
# CLAUDE.md

This repository governs its documents with standing rules, called automa. An automa is followed exactly, every time, by whoever picks it up, human or AI.

Read this before starting any work.

## Rules in force

- Every directive in `en/docs/automa/ai-collaboration/defaults/` applies to this session.
- Every markdown rule in `en/docs/automa/markdown/defaults/` applies to everything you write here.
- License sections come from the templates in `en/docs/automa/licenses/`.

## Style guides

- Style guides are defined in `en/docs/guides/style-guides/`.
- Every document names its governing guide on the `Style Guide:` line in its version block.
- Follow the guide the document names. When editing, the document's declared guide wins.
- When creating a new document, ask which register applies, technical or plain language, and record the choice on the `Style Guide:` line.

## Attribution

- Record AI assistance in `dcterms:contributor` using the form "Name (Organization)".
- Transcribe what is true. Never invent it. Leave the field out entirely when no AI helped.

## Versioning

- New documents start at version 0.1.0 with Status: Draft.
- Every change gets a changelog entry.

## If this file and a rule disagree

The rule document wins. This file is a signpost, not the law. If it points the wrong way, fix this file.
```

The paths above are wrapped in backticks on purpose. Without the backticks, a path starting with `@` would be treated as an import and pulled into the session in full <a name="apa-anthropic-citation-3"></a>([Anthropic, 2026](#apa-anthropic-reference)).

## How the file reaches the other projects

sat-doc-automa is the canonical source. The File Fairy distributes its files to the sibling projects. CLAUDE.md should travel the same road.

Two patterns fit, and both are already candidates in the fairy's feature work. The first is seed if missing: the fairy plants a starting CLAUDE.md in a project that has none, and the project owns it from then on. The second is a managed block: the fairy owns one marked section inside the file, the shared rules, while the project keeps its own instructions above and below the marks. The managed block is the better fit long term, because the shared rules stay current in every project without touching what each project added for itself.

Which pattern to use, and how it is written in the sync manifest, is decided in the manifest organization step, not here.

## What this file does not do

Two limits are worth stating plainly.

The file only loads for sessions working inside a checkout of the repository. A checkout is a copy of the repository on a computer. Sessions that reach the project another way, such as through a chat project's synced sources, do not load it. For those, put the same signpost in the chat project's instructions.

The file guides, it does not enforce. Claude treats it as trusted context, not as a lock <a name="apa-anthropic-citation-4"></a>([Anthropic, 2026](#apa-anthropic-reference)). A rule that must never be broken needs a tool-level control, not a sentence in a file. For this repository's needs, guidance is the right strength: the automa were always meant to be followed, not enforced.

## License

This document, *Recommendation: Use a CLAUDE.md File*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

On the CLAUDE.md mechanism itself, see <a name="apa-anthropic-citation-5"></a>[Anthropic (2026)](#apa-anthropic-reference).

Inside this project family, the related documents are `en/docs/automa/ai-collaboration/README.md` for how defaults and examples relate, ADR-023 in the sat repository for the attribution convention, and `decision--file-fairy-manifest-declared-sync-policy` with `analysis--ansible-builtin-modules-as-file-fairy-feature-candidates` for the distribution patterns named above.

## References

<a name="apa-anthropic-reference"></a>Anthropic. (2026). *How Claude remembers your project*. https://code.claude.com/docs/en/memory
[Return to citation](#apa-anthropic-citation)

## Changelog

| Version | Status | Notes |
| --- | --- | --- |
| 0.1.0 | Draft | Initial draft: the signpost design and its rationale, the ready-to-use example file, distribution through the File Fairy, and the two limits of the mechanism. |
