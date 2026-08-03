---
dcterms:title: "file-fairy: Run All Manifests"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:contributor: "Claude Fable 5 (Anthropic) — drafting assistance"
dcterms:description: "The two-loop pattern for reviewing and applying every fleet manifest in one pass, with the captured output of the first fleet-wide sync, 2026-08-03, as the worked example."
dcterms:created: "2026-08-03"
dcterms:modified: "2026-08-03"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:relation: "file-fairy-usage"
dcterms:identifier: "file-fairy--run-all-manifests"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:repository: "sat-doc-automa"
sat:path: "en/docs/guides/file-fairy/"
sat:version_at_creation: "0.1.4"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-03"
    author: "Christopher Steel"
    notes: "Initial guide, captured from the first fleet-wide sync. Apply loop corrected to tee so the operator sees the prompts being answered."
---

# file-fairy: Run All Manifests

Version: 0.1.0
Status: Draft
Style Guide: style-guide--technical-documentation-for-technologists

## The pattern

From the sat-doc-automa checkout, two loops: review everything first, writing nothing, then apply, confirming each target as its plan appears. The plan loop can redirect to a file for review; the apply loop must not, because the plans and prompts you are answering arrive on stdout, so capture with `tee` instead of `>`.

```bash
# review the whole fleet first, writes nothing
for m in ff-manifest-*.yaml; do echo "== $m =="; ff plan "$m"; done > plan-log.txt

# then apply, confirming each target as its plan appears; tee, never >
for m in ff-manifest-*.yaml; do echo "== $m =="; ff "$m"; done | tee apply-log.txt
```

Never loop `--yes` on a first fleet contact, and never loop `--force` at all; the per-target confirmation is the point. After the run, each target holds new files and a written state file; finish with a receive commit in every touched repository, per the receive-then-commit pattern in the file-fairy usage guide.

## Worked example

Captured from the first fleet-wide sync, 2026-08-03. A target already nearly current receives only what it lacks:

```text
NEW  (not yet synced)
  [devops-docs] en/docs/guides/devops/file-fairy-usage-v0-1-1.md -> en/docs/guides/devops/file-fairy-usage-v0-1-1.md

[file-fairy] 1 item(s) would be synced, 0 conflict(s), 0 missing source(s)

Apply the above? [y/N] y
  synced: en/docs/guides/devops/file-fairy-usage-v0-1-1.md -> en/docs/guides/devops/file-fairy-usage-v0-1-1.md
[file-fairy] 1 item(s) synced; state written to /home/initial/2-areas/development/file-fairy/.file-fairy-state.yaml
```

A fresh target receives the full shared zone, eighteen items across six groups, ending with the CLAUDE.md signpost block:

```text
NEW  (not yet synced)
  [devops-scripts] bump-version.py -> bump-version.py
  [devops-scripts] cut-release.py -> cut-release.py
  [devops-scripts] check-conformance.py -> check-conformance.py
  [devops-scripts] publish-release.py -> publish-release.py
  [devops-scripts] test_publish_release.py -> test_publish_release.py
  [devops-docs] en/docs/guides/devops/commit-and-versioning-workflow-v0-3-0.md -> en/docs/guides/devops/commit-and-versioning-workflow-v0-3-0.md
  [devops-docs] en/docs/guides/devops/file-fairy-usage-v0-1-1.md -> en/docs/guides/devops/file-fairy-usage-v0-1-1.md
  [markdown-automa] en/docs/automa/markdown/defaults/markdown--no-heading-numbers-v0-4-1.md -> en/docs/automa/markdown/defaults/markdown--no-heading-numbers-v0-4-1.md
  ... five more markdown-automa items ...
  [ai-collaboration] en/docs/automa/ai-collaboration/defaults/collaboration--energy-conservation-in-ai-collaborations-v0-2-0.md -> ...
  [license-blocks] en/docs/automa/licenses/license-block--agpl-3-0-or-later.md -> ...
  ... two more license blocks ...
  [claude-md] en/docs/automa/claude-md/claude-md-signpost-block.md -> CLAUDE.md

[file-fairy] 18 item(s) would be synced, 0 conflict(s), 0 missing source(s)

Apply the above? [y/N] y
  ... eighteen synced lines ...
[file-fairy] 18 item(s) synced; state written to /home/initial/2-areas/development/fluent/osat-fluent-hugo/.file-fairy-state.yaml
```

The same shape repeated across osat-fluent-myrepos-tool, osat-fluent-python-tool, osat-fluent-rclone-tool, osat-fluent-restic-tool, osat-fluent-sat-tool, osat-fluent-wekan-tool, and uc-radar; sat took only the usage guide; osat-fluent reported nothing to apply, already current. uc-radar's zero conflicts, under the fairy's first-contact protection, is the run confirming that its pre-manifest hand-synced copies were byte-identical to canonical: adopted, with state recorded.

## License

This document, *file-fairy: Run All Manifests*, by **Christopher Steel**, with AI assistance from **Claude Fable 5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial guide from the first fleet-wide sync: the two-loop pattern, tee not redirect on apply, and the captured worked example. |
