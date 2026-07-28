---
dcterms:title: "Commit and Versioning Workflow"
dcterms:version: "0.1.2"
dcterms:creator: "Christopher Steel"
dcterms:description: "Practical workflow for commits and version bumps: initial commit, and every subsequent version bump after that."
dcterms:created: "2026-07-24"
dcterms:modified: "2026-07-25"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "commit-and-versioning-workflow"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.2"
    date: "2026-07-25"
    author: "Christopher Steel"
    notes: "Compliance pass per ROADMAP.md Milestone 0.3.0. Replaced the em dash in the initial-commit example message with a comma, per Markdown: Use Commas, Not Em Dashes; a template the reader copies is not exempt from the rule."
  - version: "0.1.0"
    date: "2026-07-24"
    author: "Christopher Steel"
    notes: "Initial draft. Generalized from the osat-fluent-rclone-tool workflow into a project-neutral guide."
---

# Commit and Versioning Workflow

Version: 0.1.2
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Abstract

Two paths, one for the first commit and one for every commit after it, because they do not follow the same steps or produce the same kind of commit message.

## Which workflow

```mermaid
flowchart TD
    A[Has this repository already had its first commit?]
    A -->|No| B[Initial commit workflow]
    A -->|Yes| C[Version bump workflow]
    click B "#initial-commit-workflow"
    click C "#version-bump-workflow"
```

GitHub's mermaid renderer strips click links, so on github.com the chart is visual only; the section headings below are the actual navigation.

## Initial commit workflow

Use this once, the first time the repository is committed.

### Verify the branch

```bash
git status
```

If not on `main`:

```bash
git checkout -b main
```

### Stage and review

```bash
git add .
git status
```

The `git status` output after staging is used directly in the commit body. At initial commit this is the full file listing, every file is new. This full listing is expected only here; ordinary bumps produce a much shorter list.

### Commit

Summary line, then the staged file list from `git status`:

```bash
git commit -m "Initial commit, v0.1.0

	new file:   bump-version.py
	new file:   en/docs/README.md
	new file:   en/docs/automa/ai-collaboration/README.md
	new file:   en/docs/automa/ai-collaboration/defaults/collaboration--energy-conservation-in-ai-collaborations-v0-2-0.md
	renamed:    en/radar/assess/clean-text--text-normalization.md -> en/docs/automa/ai-collaboration/examples/.gitkeep
	new file:   en/docs/automa/licenses/license-block--agpl-3-0-or-later.md
	new file:   en/docs/automa/licenses/license-block--code-and-code-docs--gpl-3-0-or-later.md
	new file:   en/docs/automa/licenses/license-block--content-cc-by-4-0.md
	new file:   en/docs/automa/markdown/README.md
	new file:   en/docs/automa/markdown/defaults/markdown--apa-7-citations-using-citation-anchor-pairs-v0-1-0.md
	new file:   en/docs/automa/markdown/defaults/markdown--license-statement-templates-v0-3-1.md
	new file:   en/docs/automa/markdown/defaults/markdown--no-heading-numbers-v0-4-1.md
	new file:   en/docs/automa/markdown/defaults/markdown--no-horizontal-rules-v0-3-1.md
	new file:   en/docs/automa/markdown/defaults/markdown--use-commas-not-em-dashes-v0-3-1.md
	renamed:    en/radar/assess/euro-office-testing.md -> en/docs/automa/markdown/examples/.gitkeep
	new file:   en/docs/automa/svg/accessible-svg--user-adjustable-presentation-on-the-web-v0-1-0.md
	new file:   en/docs/guides/accessibility/accessible-svg--user-adjustable-presentation-on-the-web-v0-1-0.md
	new file:   en/docs/guides/accessibility/diagrams-readers-can-adjust--a-plain-language-guide-v0-1-0.md
	new file:   en/docs/guides/devops/commit-and-versioning-workflow-v0-1-1.md
	new file:   en/docs/guides/style-guides/style-guide--navigation-accessibility-v0-2-0.md
	new file:   en/docs/guides/style-guides/style-guide--plain-language-for-general-audiences-v0-5-0.md
	new file:   en/docs/guides/style-guides/style-guide--technical-documentation-for-technologists-v0-5-0.md
	new file:   en/docs/guides/style-guides/style-guide--versioned-documents-in-unrendered-markdown-v0-3-0.md
	new file:   en/docs/guides/style-guides/style-guide--web-ready-unrendered-markdown-using-apa-7-v0-5-0.md
	renamed:    en/radar/README.md -> en/docs/radar/README.md
	renamed:    en/radar/ROADMAP.md -> en/docs/radar/ROADMAP.md
	renamed:    en/radar/adopt/universal-cake-evaluation--infusion--accessibility-bar-v0.1.0.md -> en/docs/radar/adopt/accessibility/universal-cake-evaluation--infusion--accessibility-bar-v0.1.0.md
	renamed:    en/radar/assess/atproto--universal-cake-praxis-evaluation-v0.1.0.md -> en/docs/radar/adopt/atproto/atproto--universal-cake-praxis-evaluation-v0.1.0.md
	renamed:    en/radar/assess/assessed/shims--options-for-provider-agnostic-approaches-to-provisioning--v0.1.0.md -> en/docs/radar/adopt/iac/shims--options-for-provider-agnostic-approaches-to-provisioning--v0.1.0.md
	renamed:    en/radar/adopt/shims--options-for-provider-agnostic-approaches-to-provisioning--v0.1.1.md -> en/docs/radar/adopt/iac/shims--options-for-provider-agnostic-approaches-to-provisioning--v0.1.1.md
	renamed:    en/radar/assess/assessed/open-source-identity-systems.md -> en/docs/radar/adopt/iam/open-source-identity-systems.md
	renamed:    en/radar/assess/assessed/opensource-identity-systems--iam--radar-entry-v0.1.0.md -> en/docs/radar/adopt/iam/opensource-identity-systems--iam--radar-entry-v0.1.0.md
	renamed:    en/radar/adopt/opensource-identity-systems--iam--radar-entry-v0.1.1.md -> en/docs/radar/adopt/iam/opensource-identity-systems--iam--radar-entry-v0.1.1.md
	renamed:    en/radar/adopt/tool-installation-pattern--versioned-local-binaries-and-wrappers-for-nix-v0.1.0.md -> en/docs/radar/adopt/installers/tool-installation-pattern--versioned-local-binaries-and-wrappers-for-nix-v0.1.0.md
	renamed:    en/radar/adopt/kanban/uc--kanban-setup-v0.1.0.md -> en/docs/radar/adopt/kanban/uc--kanban-setup-v0.1.0.md
	renamed:    en/radar/adopt/kanban/wekan--accessible-kanban-board-v0.2.0.md -> en/docs/radar/adopt/kanban/wekan--accessible-kanban-board-v0.2.0.md
	renamed:    en/radar/adopt/kanban/wekan--accessible-kanban-board.md -> en/docs/radar/adopt/kanban/wekan--accessible-kanban-board.md
	renamed:    en/radar/assess/assessed/server-os--concise-technical-rating-for-server-os-options.md -> en/docs/radar/adopt/linux/server-os--concise-technical-rating-for-server-os-options.md
	renamed:    en/radar/adopt/server-os--linux-server-operating-system--radar-entry-v0.1.0.md -> en/docs/radar/adopt/linux/server-os--linux-server-operating-system--radar-entry-v0.1.0.md
	renamed:    en/radar/adopt/flowmark--semantic-linebreak-markdown-formatter.md -> en/docs/radar/adopt/markdown/flowmark--semantic-linebreak-markdown-formatter.md
	renamed:    en/radar/adopt/mdformat--commonmark-compliant-markdown-formatter.md -> en/docs/radar/adopt/markdown/mdformat--commonmark-compliant-markdown-formatter.md
	renamed:    en/radar/assess/1b-sat-dublin-core-metadata-usage-current-state-and-recommended-improvements-v0.1.1.md -> en/docs/radar/adopt/metadata/1b-sat-dublin-core-metadata-usage-current-state-and-recommended-improvements-v0.1.1.md
	renamed:    en/radar/assess/1-dublin-core-metadata-usage-in-sat-v0.1.1.md -> en/docs/radar/adopt/metadata/dublin-core-metadata-usage-in-sat-v0.1.2.md
	new file:   en/docs/radar/adopt/metadata/metadata-resolution-process.md
	renamed:    en/radar/adopt/reverse-proxies--options-for-http-routing-and-tls-termination--v0.1.0.md -> en/docs/radar/adopt/proxies-and-reverse-proxies/reverse-proxies--options-for-http-routing-and-tls-termination--v0.1.0.md
	renamed:    en/radar/adopt/sat-licence-check-py.md -> en/docs/radar/adopt/spdx/sat-licence-check-py.md
	renamed:    en/radar/adopt/spdx/spdx-license-list--machine-readable-license-identifiers.md -> en/docs/radar/adopt/spdx/spdx-license-list--machine-readable-license-identifiers.md
	renamed:    en/radar/adopt/webservers--options-for-static-site-hosting--v0.1.0.md -> en/docs/radar/adopt/webservers/webservers--options-for-static-site-hosting--v0.1.0.md
	renamed:    en/radar/assess/README.md -> en/docs/radar/assess/README.md
	renamed:    en/radar/assess/built-in-screen-readers-v0.1.0.md -> en/docs/radar/assess/accessibility/built-in-screen-readers-v0.1.0.md
	renamed:    en/radar/assess/fluid-infusion-technical-overview-v0.1.0.md -> en/docs/radar/assess/accessibility/fluid-infusion-technical-overview-v0.1.0.md
	renamed:    en/radar/assess/1a-archive-identity-provenance-and-definition-as-distinct-concerns.md -> en/docs/radar/assess/archives/1a-archive-identity-provenance-and-definition-as-distinct-concerns.md
	renamed:    en/radar/assess/bibtexparser--parsing-and-writing-bibtex.md -> en/docs/radar/assess/bibtex/bibtexparser--parsing-and-writing-bibtex.md
	renamed:    en/radar/assess/bootstrap-5.md -> en/docs/radar/assess/bootstrap-5.md
	renamed:    en/radar/assess/citeproc-py--citation-style-language-csl-processor.md -> en/docs/radar/assess/citations/citeproc-py--citation-style-language-csl-processor.md
	renamed:    en/radar/assess/datalad/1. Identity + scope.md -> en/docs/radar/assess/datalad/1. Identity + scope.md
	renamed:    en/radar/assess/datalad/1. Where it should live.md -> en/docs/radar/assess/datalad/1. Where it should live.md
	renamed:    en/radar/assess/datalad/datalad-architecture-guide-flat-vs-federated-entity-repositories.md -> en/docs/radar/assess/datalad/datalad-architecture-guide-flat-vs-federated-entity-repositories.md
	renamed:    en/radar/assess/datalad/datalad-installation-and-configuration-guide-ubuntu-24-04.md -> en/docs/radar/assess/datalad/datalad-installation-and-configuration-guide-ubuntu-24-04.md
	renamed:    en/radar/assess/datalad/enforcing-structural-conventions-in-a-datalad-based-repository.md -> en/docs/radar/assess/datalad/enforcing-structural-conventions-in-a-datalad-based-repository.md
	renamed:    en/radar/assess/community-led-co-design-kit.md -> en/docs/radar/assess/design/community-led-co-design-kit.md
	renamed:    en/radar/assess/dual-mode-language-authority--standard-aware-not-standard-dependent.md -> en/docs/radar/assess/dual-mode-language-authority--standard-aware-not-standard-dependent.md
	renamed:    en/radar/assess/fastapi--web-framework.md -> en/docs/radar/assess/fastapi--web-framework.md
	renamed:    en/radar/assess/goldmark--markdown-parser.md -> en/docs/radar/assess/goldmark--markdown-parser.md
	renamed:    en/radar/assess/inclusive-design-for-learning--creating-flexible-and-adaptable-content-with-learners.md -> en/docs/radar/assess/inclusive-design-for-learning--creating-flexible-and-adaptable-content-with-learners.md
	renamed:    en/radar/assess/incus--open-source-system-container-and-virtual-machine-manager.md -> en/docs/radar/assess/incus--open-source-system-container-and-virtual-machine-manager.md
	renamed:    en/radar/assess/incus--universal-cake-praxis-evaluation-v0.1.0.md -> en/docs/radar/assess/incus--universal-cake-praxis-evaluation-v0.1.0.md
	renamed:    en/radar/assess/libre-screen-readers-talking-browsers-v0.1.0.md -> en/docs/radar/assess/libre-screen-readers-talking-browsers-v0.1.0.md
	renamed:    en/radar/assess/copyright-checkers.md -> en/docs/radar/assess/licensing/copyright-checkers.md
	renamed:    en/radar/assess/markdown-parser--goldmark.md -> en/docs/radar/assess/markdown-parser--goldmark.md
	renamed:    en/radar/assess/mdformat--commonmark-compliant-markdown-formatter.md -> en/docs/radar/assess/mdformat--commonmark-compliant-markdown-formatter.md
	renamed:    en/radar/assess/myst-parser--extensible-markdown-flavour.md -> en/docs/radar/assess/myst-parser--extensible-markdown-flavour.md
	renamed:    en/radar/assess/collabora-online--collaborative-document-editor.md -> en/docs/radar/assess/online-editors/collabora-online--collaborative-document-editor.md
	renamed:    en/radar/assess/cryptpad--encrypted-collaboration-suite.md -> en/docs/radar/assess/online-editors/cryptpad--encrypted-collaboration-suite.md
	renamed:    en/radar/assess/etherpad--realtime-text-editor.md -> en/docs/radar/assess/online-editors/etherpad--realtime-text-editor.md
	renamed:    en/radar/assess/euro-office--collaborative-document-editor.md -> en/docs/radar/assess/online-editors/euro-office--collaborative-document-editor.md
	renamed:    en/radar/assess/euro-office-evaluating-on-incus-v0.1.0.md -> en/docs/radar/assess/online-editors/euro-office-evaluating-on-incus-v0.1.0.md
	new file:   en/docs/radar/assess/online-editors/euro-office-testing.md
	renamed:    en/radar/assess/libreoffice-online--collaborative-document-editor.md -> en/docs/radar/assess/online-editors/libreoffice-online--collaborative-document-editor.md
	renamed:    en/radar/assess/open-source-file-synchronization-tools.md -> en/docs/radar/assess/open-source-file-synchronization-tools.md
	renamed:    en/radar/assess/pandoc--universal-document-converter.md -> en/docs/radar/assess/pandoc--universal-document-converter.md
	renamed:    en/radar/assess/pip-licenses.md -> en/docs/radar/assess/pip-licenses.md
	renamed:    en/radar/assess/prometheus--universal-cake-praxis-evaluation-v0.1.0.md -> en/docs/radar/assess/prometheus--universal-cake-praxis-evaluation-v0.1.0.md
	renamed:    en/radar/assess/pybtex-apa7--python-bibtex-processor.md -> en/docs/radar/assess/pybtex-apa7--python-bibtex-processor.md
	renamed:    en/radar/assess/sat-radar-entries--atproto-and-pds-v0.1.0.md -> en/docs/radar/assess/sat-radar-entries--atproto-and-pds-v0.1.0.md
	renamed:    en/radar/assess/scancode-toolkit.md -> en/docs/radar/assess/scancode-toolkit.md
	renamed:    en/radar/assess/screen-readers.md -> en/docs/radar/assess/screen-readers.md
	renamed:    en/radar/assess/snow-special-needs-opportunity-windows--an-overview.md -> en/docs/radar/assess/snow-special-needs-opportunity-windows--an-overview.md
	renamed:    en/radar/assess/snow-special-needs-opportunity-windows-source-and-license-attribution-example.md -> en/docs/radar/assess/snow-special-needs-opportunity-windows-source-and-license-attribution-example.md
	renamed:    en/radar/assess/static-cms-frontmatter-and-sidecar-metadata-survey.md -> en/docs/radar/assess/static-cms-frontmatter-and-sidecar-metadata-survey.md
	renamed:    en/radar/assess/static-site-generator-frontmatter-and-sidecar-metadata-survey.md -> en/docs/radar/assess/static-site-generator-frontmatter-and-sidecar-metadata-survey.md
	renamed:    en/radar/assess/datalad--evaluation-and-swot-analysis.md -> en/docs/radar/assess/sync/datalad--evaluation-and-swot-analysis.md
	new file:   en/docs/radar/assess/sync/fairy--file-sync-cli.md
	new file:   en/docs/radar/assess/sync/fairy--git-hook-integration-using-core-hookspath-v0-1-1.md
	renamed:    en/radar/assess/filesystem-synchronisation-git-annex-v0-1-0.md -> en/docs/radar/assess/sync/filesystem-synchronisation-git-annex-v0-1-0.md
	renamed:    en/radar/assess/filesystem-synchronisation-nextcloud-v0-1-0.md -> en/docs/radar/assess/sync/filesystem-synchronisation-nextcloud-v0-1-0.md
	renamed:    en/radar/assess/clean-text--text-cleaning-and-normalisation.md -> en/docs/radar/assess/text-normalization/clean-text--text-cleaning-and-normalisation.md
	new file:   en/docs/radar/assess/text-normalization/clean-text--text-normalization.md
	renamed:    en/radar/assess/typora--markdown-editor.md -> en/docs/radar/assess/typora--markdown-editor.md
	renamed:    en/radar/assess/uc-file-sync-comparison.md -> en/docs/radar/assess/uc-file-sync-comparison.md
	renamed:    en/radar/assess/universal-cake-evaluation--infusion--accessibility-bar-v0.1.0.md -> en/docs/radar/assess/universal-cake-evaluation--infusion--accessibility-bar-v0.1.0.md
	renamed:    en/radar/assess/caddy--web-server--approaches-to-multi-tenant-hosting.md -> en/docs/radar/assess/webservers/caddy--web-server--approaches-to-multi-tenant-hosting.md
	renamed:    en/radar/assess/caddy--web-server--manual-installation-and-configuration-on-a-production-server-v0.1.1.md -> en/docs/radar/assess/webservers/caddy--web-server--manual-installation-and-configuration-on-a-production-server-v0.1.1.md
	renamed:    en/radar/assess/caddy--web-server-radar-entry-v0.1.1-draft.md -> en/docs/radar/assess/webservers/caddy--web-server-radar-entry-v0.1.1-draft.md
	renamed:    en/radar/assess/caddy--webserver--universal-cake-praxis-evaluation-v0.1.0.md -> en/docs/radar/assess/webservers/caddy--webserver--universal-cake-praxis-evaluation-v0.1.0.md
	renamed:    en/radar/assess/zotero-plus-better-bibtex-reference.md -> en/docs/radar/assess/zotero-plus-better-bibtex-reference.md
	renamed:    en/radar/hold/README.md -> en/docs/radar/hold/README.md
	renamed:    en/radar/hold/kanban/leantime--cognitively-accessible-project-management-v0.2.0.md -> en/docs/radar/hold/kanban/leantime--cognitively-accessible-project-management-v0.2.0.md
	renamed:    en/radar/hold/kanban/leantime--cognitively-accessible-project-management.md -> en/docs/radar/hold/kanban/leantime--cognitively-accessible-project-management.md
	renamed:    en/radar/prompt--universal-cake-praxis-evaluation-v0.1.1.md -> en/docs/radar/prompt--universal-cake-praxis-evaluation-v0.1.1.md
	renamed:    en/radar/radar-entry-template.md -> en/docs/radar/radar-entry-template.md
	renamed:    en/radar/text-normalisation-rough-list.md -> en/docs/radar/text-normalisation-rough-list.md
	renamed:    en/radar/uc-radar--evaluation-lifecycle-v0.1.0.md -> en/docs/radar/uc-radar--evaluation-lifecycle-v0.1.0.md
	renamed:    en/radar/uc-radar-entry-template-v0.2.0.md -> en/docs/radar/uc-radar-entry-template-v0.2.0.md
	renamed:    en/radar/universal-cake-evaluation-metrics-v0.3.1.md -> en/docs/radar/universal-cake-evaluation-metrics-v0.3.1.md
	new file:   en/docs/references/cncf-project-maturity-levels-v0-1-0.md
	new file:   en/docs/references/reference--spdx-license-identifiers-v0-1-0.md

"
```

Post commit confirmation

```bash
git status
```

Output example:

```bash
On branch main
Your branch is based on 'origin/main', but the upstream is gone.
  (use "git branch --unset-upstream" to fixup)

nothing to commit, working tree clean
```

### Tag and push

Use `-u` on this **first push only**:

```bash
git tag v0.1.0
git push -u origin main
git push origin v0.1.0
```

Every future release goes through the version bump workflow below.

## Version bump workflow

Use this for every release after the initial commit.

### Bump the version

```bash
python3 bump-version.py patch
```

Output example:

```bash
VERSION: 0.1.0 -> 0.1.1
```

Or `minor`, `major`, or an explicit version. This updates the `VERSION` file and nothing else.

Confirm version bump

```bash
git status
```

Output example

```bash
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   VERSION
	modified:   docs/en/devops/commit-and-versioning-workflow-v0-1-1.md

no changes added to commit (use "git add" and/or "git commit -a")
```

Note: Since I am updating this file it shows up in addition to our version bump.

### Stage and review

Stage any other files that belong in this release alongside the version bump, then review:

```bash
git add .
git status
```

A pure version-bump commit changes only `VERSION`. If other files changed too, the commit message should reflect that.

### Commit

Summary line references the new version. Body is the staged file list from `git status`:

```bash
git commit -m "Bump version to 0.1.1

	modified:   VERSION
"
```

If additional files are included:

```bash
 git commit -m "Bump version to 0.1.1 
        modified:   VERSION
        modified:   docs/en/devops/commit-and-versioning-workflow-v0-1-1.md
"
```

Output example:

```bash
[main 5a16f8a] Bump version to 0.1.1
 1 file changed, 1 insertion(+)
 create mode 100644 VERSION
```



### Tag and push

```bash
git tag v0.1.1
git push
git push origin v0.1.1
```

Output example:

```bash
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:steelcj/uc-radar.git
 * [new tag]         v0.1.1 -> v0.1.1
```

## License

This document, *Commit and Versioning Workflow*, by **Christopher Steel**, with AI assistance from **Claude Sonnet 4.6 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.2 | Draft | Minor edits |
| 0.1.1 | Draft | Compliance pass: replaced the em dash in the initial-commit example message with a comma |
| 0.1.0 | Draft | Initial draft, generalized from the osat-fluent-rclone-tool workflow into a project-neutral guide |
