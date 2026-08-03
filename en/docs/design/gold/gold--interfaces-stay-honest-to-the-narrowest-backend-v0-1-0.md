---
dc:title: "Gold: Interfaces Stay Honest to the Narrowest Backend"
dcterms:version: "0.1.0"
dc:creator: "Christopher Steel"
dc:contributor: "Claude Fable 5 (Anthropic) — drafting assistance"
dc:description: "A distilled design principle: an interface over multiple backends must be designed against its poorest backend and merely implemented against its richest. Emerged from the publish-release provider-interface design; recorded with provenance and a running list of applications."
dcterms:created: "2026-08-02"
dcterms:modified: "2026-08-02"
dc:format: "text/markdown"
dc:language: "en"
sat:language_bcp47: "en"
dc:identifier: "gold--interfaces-stay-honest-to-the-narrowest-backend"
dcterms:rightsHolder: "Christopher Steel"
dc:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:repository: "sat-doc-automa"
sat:path: "en/docs/design/gold/"
sat:version_at_creation: "0.1.4"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-08-02"
    author: "Christopher Steel"
    notes: "Initial capture, from the provider-interface design discussion recorded in decision--publish-release-shared-script-with-provider-interface. First application: the release-publishing provider interface."
---

# Gold: Interfaces Stay Honest to the Narrowest Backend

Version: 0.1.0
Status: Draft
Style Guide: style-guide--technical-documentation-for-technologists

## The principle

An interface over multiple backends must be designed against its poorest backend and merely implemented against its richest. Whatever the narrowest backend can express is what the abstraction *is*. Anything a richer backend offers beyond that is backend garnish, and it stays out of the seam.

## Why this is gold

The failure it prevents is quiet and common. A seam is drawn to keep options open, then the first implementation is built against the richest backend, and capability by capability the interface absorbs what only that backend can do. Nothing breaks. The abstraction still compiles, the calls still work, and the exit it was supposed to guarantee is gone: every other backend is now unimplementable without faking the rich features. The seam has become decoration, a costume the favored backend wears.

Designing against the narrowest backend inverts the pressure. The poorest backend acts as a useful tyrant: anything it cannot express is challenged at design time, when the question "is this essential or is this garnish" is still cheap to ask. The richest backend loses nothing, it simply carries its extras outside the interface, where they are visibly optional.

The test is mechanical, which is what makes the principle followable rather than aspirational: any backend-specific parameter appearing in a shared interface is a finding. If the seam admits one, either the parameter goes or the record explaining the seam is revisited, but the disagreement is never silent.

## Provenance

Emerged 2026-08-02, designing the provider interface for the fleet's release-publishing ceremony, recorded in *Decision: publish-release.py as a Shared Script with a Provider Interface*. The narrowest backend there is a directory reached over SSH, which can hold files at stable URLs, a checksum file, and a signature; therefore that is what a release is. GitHub's rendered notes, draft states, and reactions are garnish, and the `gh` backend carries them outside the seam or not at all. Design against the directory; implement against `gh`.

## Applications

A running list, one entry per seam the principle has shaped. When the list demonstrates the principle across unrelated seams, it becomes a candidate for promotion to a binding directive under `automa/design/defaults/`, per the deferral recorded in the originating decision.

1. **The release-publishing provider interface** (2026-08-02). The SSH-directory backend defines the release contract; `gh` is the first implementation. Origin of the principle.

## Related observations

The principle rhymes with two standing practices, recorded here so the pattern is visible. file-fairy's manifest vocabulary stays small because its narrowest backend is a plain local file copy, an instance of the principle obeyed before it was named. And the plain-language style guide's rule, write for the reader with the least context and the expert reads it faster too, is the same shape applied to prose: design for the narrowest, and the richest still works.

## License

This document, *Gold: Interfaces Stay Honest to the Narrowest Backend*, by **Christopher Steel**, with AI assistance from **Claude Fable 5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial capture with provenance and first application. Promotion to automa/design/defaults/ deferred until the applications list earns it, per the originating decision record. |
