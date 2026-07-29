# sat-doc-automa

The canonical home for the style guides, formats, templates, and automa that govern documentation across SAT, OSAT Fluent, Universal Cake, and any other project that adopts them.

## What is an automa?

Start with an example. A new document is finished, and at the bottom of it sits a correctly formatted License section: the right license for the content type, the author named, the AI assistance attributed, the link pointing at the canonical license text. Nobody asked for it. Nobody explained how to write one, or which license applies to which kind of document, or where the bold goes. The license statement templates were simply present, and the License section followed from them, exactly, the way it does in every other document, every time.

That is an automa at work. An automa is a self-operating mechanism designed to follow a sequence of predetermined instructions automatically. The word is used here deliberately, and literally: the documents in this repository are written to function as automa. Handed to any collaborator, human or AI, they produce consistent behavior mechanically, without the rules needing to be re-derived, re-negotiated, or re-explained each time. A guide can be read and set aside; an automa is followed, exactly, every time, by whoever or whatever picks it up.

## What lives here

### Automa

Standing directives, organized per-format, with a `defaults/` directory answering "what is in force right now" and an `examples/` directory for deliberately-chosen alternatives. The directory designates status; titles state only the rule.

#### Markdown

- [Markdown: Use Commas, Not Em Dashes](en/docs/automa/markdown/defaults/markdown--use-commas-not-em-dashes-v0-3-1.md)
- [Markdown: No Heading Numbers](en/docs/automa/markdown/defaults/markdown--no-heading-numbers-v0-4-1.md)
- [Markdown: No Horizontal Rules](en/docs/automa/markdown/defaults/markdown--no-horizontal-rules-v0-3-1.md)
- [Markdown: License Statement Templates](en/docs/automa/markdown/defaults/markdown--license-statement-templates-v0-3-1.md)

#### AI collaboration

- [Collaboration: Energy Conservation in AI Collaborations](en/docs/automa/ai-collaboration/defaults/collaboration--energy-conservation-in-ai-collaborations-v0-2-0.md)

#### Licenses

Reusable License-section blocks, copied into a document's or project's own License section.

- [Content: CC BY 4.0 International](en/docs/automa/licenses/license-block--content-cc-4-0-international.md)
- [Document: GNU GPL v3.0 or later](en/docs/automa/licenses/license-block--gnu-general-public-license-3-plus.md)
- [Software: GNU GPL v3.0 or later](en/docs/automa/licenses/license-block--gplv3plus.md)

### Guides

#### Style guides

- [Versioned Documents in Unrendered Markdown](en/docs/guides/style-guides/style-guide--versioned-documents-in-unrendered-markdown-v0-3-0.md), the authoritative guide: filename patterns, frontmatter schema, document structure, and prose authoring rules
- [Technical Documentation for Technologists](en/docs/guides/style-guides/style-guide--technical-documentation-for-technologists-v0-5-0.md), register, decision rationale requirements, and conceptual boundary documentation
- [Plain Language for General Audiences](en/docs/guides/style-guides/style-guide--plain-language-for-general-audiences-v0-5-0.md), the companion guide for general-audience writing
- [Navigation and Accessibility](en/docs/guides/style-guides/style-guide--navigation-accessibility-v0-2-0.md), real headings over bolded pseudo-headings, grounded in WCAG 2.1
- [Web-Ready Unrendered Markdown Using APA 7](en/docs/guides/style-guides/style-guide--web-ready-unrendered-markdown-using-apa-7-v0-5-0.md), APA 7 conformance and the Citation Anchor Pair workflow

#### DevOps

- [Commit and Versioning Workflow](en/docs/guides/devops/commit-and-versioning-workflow-v0-2-0.md), the two paths: initial commit and every version bump after it

### References

- [SPDX License Identifiers](en/docs/references/reference--spdx-license-identifiers-v0-1-0.md), the canonical SPDX identifiers used in `dcterms:rights`, License sections, and `LICENSE` files
- [CNCF Project Maturity Levels](en/docs/references/cncf-project-maturity-levels-v0-1-0.md), the three CNCF maturity levels as a governance signal for tool evaluation

## Structure

This repository is structured as a SAT archive from its first commit, per the decision recorded in *Decision: Standalone Repository or SAT Archive for the Authoring Prompts and Style Guides Project*: every convention SAT's archive will require, frontmatter schema, semantic versioning, changelog discipline, correct naming, is adopted now, while nothing here depends on SAT tooling that does not yet exist. When SAT's archive mechanism is built, this repository becomes the first archive with close to zero rework.

The language layer sits at the root of the subtree that varies by language, matching the governance repository's convention:

```
en/docs/
    automa/                          standing directives, organized per-format
        ai-collaboration/defaults/   directives for AI collaboration sessions
        ai-collaboration/examples/   deliberately-chosen alternatives
        licenses/                    reusable License-section blocks
        markdown/defaults/           directives in force for markdown documents
        markdown/examples/           deliberately-chosen alternatives
    guides/
        devops/                      operational workflow guides
        style-guides/                normative style guides
    references/                      standing reference material
```

## Languages

- [English](en/docs/)

## License

This repository's documents are individually licensed; see each document's own License section. Unless a document states otherwise, content is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).
