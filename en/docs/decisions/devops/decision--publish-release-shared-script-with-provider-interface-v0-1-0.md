---
dcterms:title: "Decision: publish-release.py as a Shared Script with a Provider Interface"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:contributor: "Claude Fable 5 (Anthropic) — drafting assistance"
dcterms:description: "Records the choice of a shared publish-release.py, distributed by file-fairy beside the existing devops trio, over a standalone osat-fluent-gh-tool, and the design that makes it durable: connectivity as a named two-layer requirement, a provider interface governed by the narrowest-backend rule, gh as first backend, and an SSH-to-controlled-host backend as the sovereign extension path."
dcterms:created: "2026-08-02"
dcterms:modified: "2026-08-02"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "decision--publish-release-shared-script-with-provider-interface"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.1.4"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: "Initial draft, recording the resolution of the fork named in the osat-fluent-gh-tool radar entry, per the comparative evaluation in release-publishing--options-for-the-fleet-release-ceremony, and the connectivity and provider-interface design reached in discussion."
---

# Decision: publish-release.py as a Shared Script with a Provider Interface

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Context

The release ceremony ends where publishing should begin. `cut-release.py` bumps, rolls the changelog, commits, tags, and stops before push, by design; pushing stays a human decision. After the push, no tooling exists: creating the platform Release, generating a byte-stable tarball, computing `SHA256SUMS`, uploading the assets, and eventually GPG-signing the checksum file are all hand work or not done at all. Two ROADMAP items hang off this gap, sat-doc-automa's pending GPG-sign item and osat-fluent-restic-tool's mirrored GPG-verification item, and *Decision: GitHub CLI (gh) for Release Asset Publishing* warns that the two "should be resolved together, or explicitly cross-referenced, rather than drifting into separate answers." The gap is load-bearing, not cosmetic: the consuming tools' self-update verifies downloaded archives against `SHA256SUMS` from the Release, so the publish side must be complete and deterministic every time, which is exactly what hand ceremony is bad at.

Two evaluations preceded this record. The radar entry `osat-fluent-gh-tool--release-publishing-cli` evaluated the capability against Universal Cake Evaluation Metrics v0.3.1 and deliberately left open the fork between a standalone fluent tool and a shared script. The comparison `release-publishing--options-for-the-fleet-release-ceremony` resolved the fork analytically and recommended the shared-script form. This record makes that recommendation a decision and adds the design that hardened during review: publishing is a connectivity problem, and connectivity has more than one honest answer.

## Decision

The release ceremony's publishing step is a single shared script, `publish-release.py`, living at sat-doc-automa's root beside `bump-version.py`, `cut-release.py`, and `check-conformance.py`, and distributed to each release-managed repository by file-fairy as the fourth member of the devops-scripts manifest group, in `mirror` sync mode so a local hand-edit surfaces as a conflict rather than being silently kept or overwritten.

The script does not depend on GitHub. It depends on *connectivity*, a named requirement with two layers, and reaches providers through a thin interface.

### Connectivity, two layers

The first layer is git transport: push, fetch, tags. It is provider-agnostic today and stays that way. The preferred mechanism is SSH with ssh-agent and passphrase-protected keys, which works identically against GitHub, GitLab, Forgejo, Gitea, or a bare server. `publish-release.py` uses this layer only for preflight, `git ls-remote --tags` to confirm the tag it is about to publish exists on the remote, and never for publishing itself. Pushing remains a human act over whatever transport the maintainer trusts, upstream of this script entirely.

The second layer is the publish channel: creating the Release object and attaching assets. This is a platform operation, not a git operation, the distinction the gh-cli decision record already draws, and on hosted providers it is reachable only through the provider's authenticated HTTPS API. An SSH key that can push all day cannot create a GitHub Release. This layer is where providers differ, and therefore where the interface sits.

### The provider interface

`publish-release.py` reaches the publish channel through a small internal seam:

```text
detect(remote_url)      which provider is this repository on
preflight()             is the channel authenticated and the tag pushed
publish(tag, files)     create the release, attach the artifacts
release_url(tag)        where self-update will find them
```

Backends implement the seam. The first backend is `gh`, per the standing gh-cli decision: it handles its own authentication once via `gh auth login`, and the script never reads, stores, logs, or echoes a token. `glab` (GitLab) and `tea` (Forgejo/Gitea) are the anticipated hosted siblings if the fleet ever moves. The sovereign backend is SSH/rsync to a controlled host: artifacts pushed to a directory the operator owns and served statically, tarball, `SHA256SUMS`, signature, stable URLs. Self-update verifies checksums and does not care whose domain the URL carries. This backend is recorded now as the extension path even though it is not built first, because its existence is what keeps every hosted backend optional.

### The narrowest-backend rule

The interface must stay honest to its narrowest backend, not its richest. The SSH directory backend can express files at stable URLs, a checksum file, and a signature; therefore that is what a release *is*. Anything a richer provider offers beyond it, rendered release notes, draft states, reactions, is provider garnish and stays out of the seam. If `publish(tag, files)` ever grows a GitHub-only parameter, the abstraction has failed and this record should be revisited. Design against the directory; implement against `gh`.

### Dependencies and their guarantors

Every prerequisite is named with its guarantor, or with the deliberate absence of one.

| Prerequisite | Guarantor | Notes |
|--------------|-----------|-------|
| Python 3.8+ | osat-fluent-python-tool | Installs a self-contained user-space CPython on any platform lacking one. Shared by every script on the fairy road, not specific to this one. |
| `gh` | None, accepted | Official installers on macOS, Windows, and Linux; precompiled binaries on Releases with Sigstore build-provenance attestations since v2.50.0. Maintainer machines only, release-side only. A fluent acquirer is a named flip condition, not a present need. |
| `git` | None, environmental | A maintainer of these repositories has git by definition; the prerequisite predates the solution. `gh` requires it transitively. |
| Authentication | None, human by design | `gh auth login` once per machine, or an SSH key with a passphrase. No tool can or should perform it; proving identity is the one irreducibly human step, and that is the security posture working as intended. |
| Connectivity | The provider interface | The named requirement this design exists to satisfy; each backend is one way of satisfying it. |

### Security gates

Two gates must carry Verified evidence tags before the script is trusted with a real release, per the metrics document's trial rule. First, the script never touches credentials: authentication is delegated entirely to the backend (`gh`'s own auth, the ssh-agent), and no token or key material is read, stored, logged, or echoed by the script under any code path. Second, tarball determinism: the same tag produces the same bytes every time, with timestamps, file ordering, and ownership metadata pinned, verified by building twice and comparing checksums, because self-update's verification downstream is only as trustworthy as the artifact's stability.

## Flip conditions

Carried forward from the options entry so a future reversal is a decision, not a drift. The standalone-tool form (osat-fluent-gh-tool as ceremony wrapper) becomes right if any of these hold: the ceremony grows per-platform needs the script cannot carry cleanly, generated wrappers, Windows-specific paths, the problems the fluent pattern exists for; fleet scale defeats per-repository sync discipline, releases demonstrably shipping with stale scripts despite `ff status` visibility; the script needs a release cadence decoupled from sat-doc-automa's, or external users appear who need it without the fleet's conventions; or `gh` acquisition itself becomes a managed problem, pinned versions and verification beyond the OS package manager, at which point a fluent *acquirer* for the `gh` binary is warranted, a different tool than the ceremony wrapper even if it shares the name.

## Alternatives considered

**Hand-run `gh` commands, documented ceremony only.** Rejected. Hand ceremony fails exactly where the requirement is load-bearing: byte-stable artifacts and never-skipped steps, with self-update verification downstream amplifying every mistake. This is the baseline the ceremony exists to retire, and it is not a flip target at any scale.

**A standalone osat-fluent-gh-tool.** Rejected for now, with the flip conditions above. The fluent pattern's substance is third-party binary lifecycle management, versioned installs, checksum verification, provenance, wrappers, rollback, which is restic-tool's and python-tool's genuine problem and not this one: `gh` arrives through official installers, and the ceremony is a single pure-Python script, precisely the artifact class the devops-scripts group already distributes successfully, as the byte-identical copies across sat and sat-doc-automa demonstrate. The standalone form also carries a bootstrap knot, the tool that publishes releases must hand-publish its own first release, and a whole repository of overhead, VERSION, CHANGELOG, releases, install story, for one script's worth of behavior.

**A shared script hard-coded to `gh`.** Rejected. It would have been the smallest diff, but it mistakes one satisfier of the requirement for the requirement itself. Connectivity is the requirement; `gh` is the first backend. The seam costs little now (the first implementation carries exactly one backend) and is what keeps the sovereign exit real rather than theoretical. The gh-cli decision record is unaffected: `gh` remains the chosen tool for the GitHub channel, for the same token-handling reasons.

## Consequences

- `publish-release.py` is written at sat-doc-automa's root beside its three siblings, implementing the provider interface with the `gh` backend, the two-layer preflight, and the deterministic tarball rules.
- The devops-scripts group in all three sync manifests gains the fourth item, and the standard-repository-layout skeleton table gains one row: `publish-release.py`, required for release-managed repositories. The standard's known-drift table is also due a happy correction independent of this decision: sat no longer carries a divergent `bump-sat-version.py`; its trio is byte-identical to canonical.
- The radar entries update: `osat-fluent-gh-tool--release-publishing-cli` records in its status notes that the capability proceeds in script form with the standalone form parked behind the flip conditions; `release-publishing--options-for-the-fleet-release-ceremony` records the fork as resolved by this document.
- The two GPG ROADMAP items, signing in sat-doc-automa and verification in osat-fluent-restic-tool, resolve against this script's publish step and the consuming tools' verify step respectively, together, as the gh-cli decision record required.
- The SSH-to-controlled-host backend is the recorded sovereign extension: when built, release publishing gains an exit from hosted platforms entirely, and the options entry's Sovereignty rating is due re-evaluation upward at that time.
- The narrowest-backend rule governs this seam now and is a candidate for promotion to a standing automa directive (a design domain under `automa/`) once it has earned its keep in a second seam; promotion is deferred deliberately rather than granted on first use.
- First real use: the next tagged release of a fleet repository is published with the script, building twice to verify determinism, which is what turns the radar entry's Inferred ratings and both security gates into Verified.

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft: Form B decided; connectivity named as a two-layer requirement; provider interface with gh as first backend and SSH-to-controlled-host as sovereign extension; narrowest-backend rule stated; dependency guarantor table; two security gates; four flip conditions carried from the options entry. |
