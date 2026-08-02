# SAT en/docs Proposed Layout (working draft)

## Proposed top level
```text
en/docs/
  decisions/
  design/
  explanation/
  guides/
  ideas/
  legal/
  process/
  reference/
```

### decisions/

What is not a decision does not live here. Supporting research and comparisons that fed a decision, without themselves being one, belong in `background/`.

Holds the project's Architecture Decision Records: the append-only, numbered log of the architectural choices SAT has made and why. One decision per file, named `adr-NNN-slug.md`, numbered sequentially and never renumbered, following the Nygard ADR convention. Each record captures the context, the decision, and its consequences at the time it was made.

```bash
decisions/
  README.md          # index of ADRs with number, title, and status (the map into the log)
  adr-template.md    # the blank ADR form new records are copied from
  adr-NNN-slug.md    # the records themselves, flat and numbered (adr-001 .. adr-033 today)
  background/        # research and comparisons that inform decisions but are not decisions
                     #   (e.g. uuidv4-vs-uuidv7.md), retired-not-erased applies here, not to ADRs
```

### design/
Holds the plan: what SAT intends to build and the contracts for building it. Where `decisions/` records choices already made and `explanation/` describes how the built system works, `design/` is forward-looking. It contains the formal specifications tools are implemented against, the goals documents that state what a capability should achieve and why before it is specced, the roadmaps that sequence the work, and the retired versions of all of these.

Three document kinds sit here, each with a clear job. Specifications are the build contracts, one per capability, versioned when they iterate (for example `content-ingress-specification-v0-3-1.md`). Goals documents are the intent-and-rationale that precede a spec, capturing what a capability is for before its mechanics are pinned. Roadmaps sequence and scope the work. The current version of each document lives in its subfolder; superseded versions move to `artifacts/`, which is where most of today's loose version sprawl belongs (the three older `document-identity-...-goals` versions, the four older `language-in-sat` versions, and so on).

```bash
design/
  specifications/    # formal build contracts, current version of each (was specifications/)
  goals/             # intent-and-rationale docs that precede a spec (the *-goals-* docs)
  roadmaps/          # scoped, sequenced plans (sat-mvp-roadmap, sat-ui-readiness-roadmap + next-steps)
  explorations/      # keep-worthy design investigations that shaped specs/goals
                     #   (the salvageable parts of metadata/mvp-artifacts)
  artifacts/         # superseded versions of any of the above (retired-not-erased)
```

### explanation/
Holds the evergreen account of how and why the built system works: architecture overviews, the shared-library rationale, the metadata conceptual model, and topic deep-dives. If a document answers "how does this work and why is it shaped this way," it lives here. Multi-document topics become subfolders; single-file topics stay as loose, well-named files rather than one-file folders. The boundary with `design/explorations/` is tense: `explanation/` describes the current system, `explorations/` is how we got there.
```bash
explanation/
  architecture/      # system overviews: three-tier, content-pipeline, semantic-container-model, declarative-archive
  satlib/            # satlib design and rationale (current; older versions to artifacts/)
  metadata/          # how the metadata model works: DC-as-canonical, well-formed frontmatter
  automation-core/   # automation-core (AC) concept docs
  artifacts/         # superseded explanation versions (retired-not-erased)
                     #   loose single-file topics live at the top level (datalad, config-styles, etc.)
```

### guides/
Task-oriented how-to and tutorials: the reader is trying to do something. One topic per subfolder. Distinct from `reference/` (look-it-up) and `explanation/` (understand-it).
```bash
guides/
  development/       # working on SAT: setup, workflows, contributor conventions
  testing/           # how to run and write tests (includes smoke-test/)
  metadata/          # how-to for authoring and handling metadata
  zotero/            # Zotero setup and use
  markdownlint/      # markdownlint setup and use (older versions to artifacts/)
  sat-customization/ # customizing a SAT instance
```

### ideas/
Speculative, pre-decision thinking, clearly fenced off so nobody mistakes a daydream for a spec or a decision. When an idea is acted on, it graduates to `design/` or `decisions/`.
```bash
ideas/
  blue-sky/          # unfiltered "worth deciding while it's still blue sky" notes
                     #   loose files for one-off speculation: sat-and-at-protocol,
                     #   sat-gui-cross-platform-accessibility
```

### legal/
Licensing and compliance material for the repository itself.
```bash
legal/
  <files>            # license policy, SPDX/AGPL notes, compliance records
```

### process/
How SAT is developed and released, and the running record of that work. Standing responsibilities (release, conformance) and time-bound tracking (sessions, status) both live here.
```bash
process/
  sessions/               # session logs and status snapshots (state-of-sat-*, claude-sessions/*), one home
  commit-and-versioning/  # release and versioning workflow (candidate: reference-only to the automa doc)
  <files>                 # sat-development-cycle, project-status.yml
```

### reference/
Look-it-up material: stable facts a reader consults rather than reads through. One home, ending today's split between `references/` and `architecture/references/`.
```bash
reference/
  commands/          # command and init-sequence reference (older versions to artifacts/)
  toolchain/         # tool reference (markdownlint, and so on)
  language/          # language codes and language reference
  <files>            # Dublin Core reference, controlled vocabulary
```
