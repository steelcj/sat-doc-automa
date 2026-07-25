---
dcterms:title: "Reference: SPDX License Identifiers"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "Reference table of SPDX license identifiers in use or anticipated across sat-doc-automa and the projects that adopt its conventions."
dcterms:created: "2026-07-25"
dcterms:modified: "2026-07-25"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "reference--spdx-license-identifiers"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: "Initial draft. Lists the four identifiers currently in use across the license statement templates, with canonical URLs and scope notes."
---

# Reference: SPDX License Identifiers

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

This document lists the SPDX license identifiers in use or anticipated across sat-doc-automa and the projects that adopt its conventions. It exists so that every document's `dcterms:rights` field, every License section, and every `LICENSE` file names the license the same way: by the identifier the SPDX License List defines, written exactly as SPDX publishes it.

## What SPDX identifiers are

The SPDX License List is maintained by the SPDX Project under the Linux Foundation. It assigns a standardized short identifier, a full name, vetted license text, and a canonical permanent URL to each license and exception it covers. The list is versioned; the current version at the time of writing is 3.28.0 (2026-02-20). The full list contains roughly 650 licenses and over 50 license exceptions. Only the identifiers relevant to this repository and its downstream projects are listed here.

The canonical source is `https://spdx.org/licenses/`. The machine-readable data is at `https://github.com/spdx/license-list-data`. The XML source used to generate both is at `https://github.com/spdx/license-list-XML`.

## Identifiers in use

| SPDX identifier | Slug | Full name | Scope in this repository | Canonical URL |
|-----------------|-----------|--------------------------|---------------|---------------|
| `AGPL-3.0-or-later` | agpl-3-0-or-later | GNU Affero General Public License v3.0 or later | Versioned documents, style guides, automa, and any document in this repository unless stated otherwise | https://www.gnu.org/licenses/agpl-3.0.html |
| `GPL-3.0-or-later` | gpl-3-0-or-later | GNU General Public License v3.0 or later | Code and code documentation in downstream projects (OSAT Fluent, SAT tooling) | https://www.gnu.org/licenses/gpl-3.0.html |
| `CC-BY-4.0` | cc-by-4-0 | Creative Commons Attribution 4.0 International | General-audience prose documents, guides, and other content not tied to code | https://creativecommons.org/licenses/by/4.0/ |

## Identifiers anticipated

These are not yet in use in any document governed by this repository but are likely candidates as the project grows.

| SPDX identifier | Full name | Likely scope | Canonical URL |
|-----------------|-----------|--------------|---------------|
| `CC0-1.0` | Creative Commons Zero v1.0 Universal | Public domain dedication for datasets, schemas, or metadata where attribution is not required | https://creativecommons.org/publicdomain/zero/1.0/ |

## How identifiers appear in documents

The identifier appears in three places, each with a specific form.

In `dcterms:rights` in the YAML frontmatter, the identifier follows the `SPDX-License-Identifier:` tag:

```yaml
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
```

In the License section of the document body, the full name is used as link text pointing at the canonical URL:

```markdown
## License

This document, *[Document Title]*, by **[Author Name]**, with AI assistance
from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the
[GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).
```

In a `LICENSE` file at the root of a code repository, the full verbatim license text is included. The License section in a document links to the canonical URL rather than reproducing the full text.

The license statement templates in *Markdown: License Statement Templates* give the exact wording for each content type. This document standardizes the identifiers those templates use; it does not replace them.

## Adding identifiers

When a new license is needed, add it to the appropriate table above with its SPDX identifier copied exactly from `https://spdx.org/licenses/`, its full name as SPDX lists it, a scope note, and the canonical URL. Then update *Markdown: License Statement Templates* with a template for the new content type if one does not already exist. SPDX endeavors to never change published identifiers, so an identifier added here should remain stable.

## Placement

This is the first document in the `references` directory under `en/docs/`:

```
en/docs/references/reference--spdx-license-identifiers-v0-1-0.md
```

The `references/` directory sits alongside `automa/` and `guides/` and holds reference data, tables, and lookup documents that other documents depend on but that are not themselves directives or procedural guides.

## License

This document, *Reference: SPDX License Identifiers*, by **Christopher Steel**, with AI assistance from **Claude Opus 4.6 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## References

SPDX Project. (2026). *SPDX license list* (Version 3.28.0). Linux Foundation. https://spdx.org/licenses/

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft, four identifiers covering the license statement templates' current and anticipated scope |
