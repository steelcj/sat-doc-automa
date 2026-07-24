# sat-doc-automa

The canonical home for the style guides, formats, templates, and automa that govern documentation across SAT, OSAT Fluent, Universal Cake, and any other project that adopts them.

## What is an automa?

Start with an example. A new document is finished, and at the bottom of it sits a correctly formatted License section: the right license for the content type, the author named, the AI assistance attributed, the link pointing at the canonical license text. Nobody asked for it. Nobody explained how to write one, or which license applies to which kind of document, or where the bold goes. The license statement templates were simply present, and the License section followed from them, exactly, the way it does in every other document, every time.

That is an automa at work. An automa is a self-operating mechanism designed to follow a sequence of predetermined instructions automatically. The word is used here deliberately, and literally: the documents in this repository are written to function as automa. Handed to any collaborator, human or AI, they produce consistent behavior mechanically, without the rules needing to be re-derived, re-negotiated, or re-explained each time. A guide can be read and set aside; an automa is followed, exactly, every time, by whoever or whatever picks it up.

## What lives here

### Style guides

- [Versioned Documents in Unrendered Markdown](en/docs/style-guide--versioned-documents-in-unrendered-markdown-v0-2-0.md), filename patterns, frontmatter schema, document structure, and prose authoring rules
- [Technical Documentation for Technologists](en/docs/style-guide--technical-documentation-for-technologists-v0-4-0.md), register, decision rationale requirements, and conceptual boundary documentation
- [Plain Language for General Audiences](en/docs/style-guide--plain-language-for-general-audiences-v0-4-0.md), the companion guide for general-audience writing
- [Navigation and Accessibility](en/docs/style-guide-navigation-accessibility-v0-1-1.md), real headings over bolded pseudo-headings, grounded in WCAG 2.1
- [Web-Ready Unrendered Markdown Using APA 7](en/docs/web-ready-unrendered-markdown-using-apa-7-v0-4-0.md), APA 7 conformance and the Citation Anchor Pair workflow

### Templates and defaults

Standing directives for markdown documents live in [en/docs/markdown/](en/docs/markdown/), organized per-format with a `defaults/` directory answering "what is in force right now" and an `examples/` directory for deliberately-chosen alternatives:

- [Markdown: Use Commas, Not Em Dashes](en/docs/markdown/defaults/markdown--use-commas-not-em-dashes-v0-3-1.md)
- [Markdown: No Heading Numbers](en/docs/markdown/defaults/markdown--no-heading-numbers-v0-4-1.md)
- [Markdown: No Horizontal Rules](en/docs/markdown/defaults/markdown--no-horizontal-rules-v0-3-1.md)
- [Markdown: License Statement Templates](en/docs/markdown/defaults/markdown--license-statement-templates-v0-3-1.md)

## Structure

This repository is structured as a SAT archive from its first commit, per the decision recorded in *Decision: Standalone Repository or SAT Archive for the Authoring Prompts and Style Guides Project*: every convention SAT's archive will require, frontmatter schema, semantic versioning, changelog discipline, correct naming, is adopted now, while nothing here depends on SAT tooling that does not yet exist. When SAT's archive mechanism is built, this repository becomes the first archive with close to zero rework.

The language layer sits at the root of the subtree that varies by language, matching the governance repository's convention:

```
en/docs/                     style guides and other versioned documents
en/docs/markdown/defaults/   standing directives in force for markdown documents
en/docs/markdown/examples/   deliberately-chosen alternatives to the defaults
```

## Languages

- [English](en/docs/)

## License

This repository's documents are individually licensed; see each document's own License section. Unless a document states otherwise, content is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).
