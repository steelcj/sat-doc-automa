---
dcterms:title: "Universal Cake Wellbeing Evaluation Metrics"
dcterms:version: "0.3.0"
dcterms:creator: "Christopher Steel"
dcterms:contributor: "Claude (Anthropic)"
dcterms:subject:
  - "evaluation"
  - "metrics"
  - "wellbeing"
  - "relationships"
  - "presence"
  - "agency"
  - "inclusive design"
dcterms:description: "Evaluation metrics for ideas, tools, and practices that claim to bring about wellbeing. Operationalizes the Universal Cake Wellbeing Model — wellbeing as the quality of a person's relationships with body, mind, and others — into ratings, evidence tags, gates, an effects discussion, and a scorecard, with practice-level pillars evaluating the fourth relationship: the person's relationship with the practice, vendor, or teacher itself."
dcterms:publisher: "UniversalCake"
dcterms:created: "2026-07-30"
dcterms:modified: "2026-07-30"
dcterms:type: "Text"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:source: ""
dcterms:relation: "universal-cake-wellbeing-model, universal-cake-evaluation-metrics, uc-radar-entry-template, uc-radar--evaluation-lifecycle"
dcterms:identifier: "universal-cake-wellbeing-evaluation-metrics"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.1.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.3.0"
    date: "2026-07-30"
    author: "Christopher Steel, Claude (Anthropic)"
    notes: >
      Split. The model — wellbeing as relationship quality,
      foundations, abilities, agency, the three relationships, hub
      diagram, return loops, upstream reach — moved to the new
      universal-cake-wellbeing-model document (v0.1.0), which this
      document now opens by summarizing and references throughout.
      This document retains and owns the method: rating scale,
      evidence tags, gates, stakeholder lenses, measuring dependence,
      the effects discussion, Layer one (foundations and
      relationships metrics), Layer two (the fourth relationship),
      self-application, lifecycle attachment, and the scorecard. The
      two documents version independently; the model changes rarely,
      the metrics iterate with evaluation experience. Document
      accessibility obligations are inherited from the model document
      and restated in brief.
  - version: "0.2.0"
    date: "2026-07-30"
    author: "Christopher Steel, Claude (Anthropic)"
    notes: >
      Major restructure. Wellbeing defined as relationship quality;
      model reorganized into foundations, abilities, and
      relationships with return loops; sleep relocated to
      foundations; gates reserved for true floor conditions; effects
      discussion and upstream-reach principle added; How to read this
      document, diagram-as-navigation convention, and
      self-application added; Layer two reframed as the fourth
      relationship.
  - version: "0.1.1"
    date: "2026-07-30"
    author: "Christopher Steel, Claude (Anthropic)"
    notes: >
      Added The three spheres section with hub diagram; access placed
      at the head of the causal chain; asymmetry paragraph added.
  - version: "0.1.0"
    date: "2026-07-30"
    author: "Christopher Steel, Claude (Anthropic)"
    notes: >
      Initial complete draft adapting the Universal Cake Evaluation
      Metrics (v0.3.1) architecture to wellbeing subjects.
---

# universal-cake-wellbeing-evaluation-metrics-v0.3.0

Version: 0.3.0
Status: Draft
Model: universal-cake-wellbeing-model-v0.1.0

## Purpose

This document operationalizes the Universal Cake Wellbeing Model into an evaluation method for ideas, tools, and practices that claim to bring about wellbeing — meditation apps and meditation itself, exercise programs, therapy modalities, journalling methods, sleep tools, courses, communities, retreats, and habits of any kind. The model is the theory and lives in its own document, which changes rarely; this document is the method and iterates as evaluation experience accumulates. The two version independently.

The wellbeing space needs this evaluation more than most. It is dense with unverifiable claims, guru dependence, subscription models that hold benefits hostage, and products that market presence while running on distraction. An evaluator that makes the difference visible — between what is claimed and what is verified, between what builds capacity and what builds dependence — is the tool this document defines.

## The model in brief

Per the model document, which is normative for everything in this section: wellbeing is the quality of a person's relationships with their body, their mind, and others. That quality is worked on with abilities the person carries — presence load-bearing among them, because agency depends on it — and those abilities are conditioned by foundations, the conditions for relating: sleep, access, safety, time, material security. Foundations are qualities on a continuum, not binaries; they condition the work, they do not cast the vote, and improvements to them tend to travel furthest because they sit upstream of many effects. Influence also flows back: relationships tended well replenish the foundations they rest on. Agency is exercised choice — who authors the relationships — and every evaluative question below shares one root: does this subject widen the gap between stimulus and response, or close it?

Everything this document measures is a quality of a relationship: the three relationships and their foundations in Layer one, the abilities as relational capacities, and in Layer two a fourth relationship — the person's relationship with the practice, vendor, or teacher itself — evaluated to check whether it is worthy of mediating the other three.

## How to read this document

This document inherits the accessibility obligations stated in full in the model document: prose is normative and diagrams are navigation; a plain-language companion at a Grade 7 reading level is a committed deliverable; translation targets are English, Canadian French, and Spanish. This document's own compliance status is tracked in its self-application section below.

## How to answer

### Rating scale

Answer each metric with one of the following ratings so that evaluations remain comparable across subjects, over time, and with the parent metrics.

- **Strong**, the subject actively advances this value
- **Moderate**, the subject is adequate, with named limitations
- **Weak**, the subject works against this value
- **Unknown**, insufficient information to rate, record what would resolve it

Nearly everything in this framework — foundations included — is graded on this scale, not answered yes or no. The rare true binaries are handled by gates.

### Evidence tags

Tag every rating with how it is known.

- **Verified**, confirmed by direct trial, testing, measurement, or peer-reviewed research, record the method and date
- **Inferred**, a reasonable conclusion from the practice's structure, mechanism, or documentation, not yet tested
- **Claimed**, asserted by the vendor, teacher, or community, not independently checked

Evidence tags matter more here than in technical evaluation. Wellness claims are overwhelmingly Claimed rather than Verified, and making that visible is half this tool's value. A rating of Strong with a tag of Claimed is weaker than a rating of Moderate with a tag of Verified.

### Gates

Gates are reserved for true floor conditions — genuine zero-states where nothing downstream is reachable — not for foundations in general, which are qualities on a continuum and are scored. A failed gate cannot be averaged away by strength elsewhere; it moves the subject to hold or rejected in the uc-radar lifecycle until the named condition changes. Gate criteria are marked **[GATE]** throughout. The default gates are:

- Credible harm or contraindications concealed, or the practice presented as universally safe when it is not
- Failure of the access floor — the practice is unreachable for people with disabilities, low income, or without prior training, and no adapted path exists
- No exit — stopping incurs penalty, rebound, loss of accumulated benefit records, or loss of the person's own data
- Engagement mechanics that attack presence — streaks, manufactured urgency, infinite feeds — that cannot be disabled, in a product claiming to serve wellbeing

Projects may add gates but should not remove these without recording why.

### Stakeholder lenses

Each question is asked from one or more perspectives. Where perspectives conflict, record the conflict rather than letting one answer hide the other.

- **Person**, the individual undertaking the practice
- **Others**, household, family, and relationships affected by the person's practice
- **Community**, the wider group of practitioners, contributors, and the public affected
- **Environment**, energy, material, travel, and consumption consequences of the practice

Example of a conflict worth surfacing: a retreat may increase the person's wellbeing while imposing costs on a household left to absorb their absence.

### Measuring dependence

Two principles from the parent metrics apply directly, translated.

**Asymmetry of information is itself measurable.** Compare what each party can know. A wellness vendor with engagement telemetry on a person's every session, facing a person who cannot see the evidence base, the pricing model, or the mechanism, scores badly regardless of stated intentions.

**Measure reversibility, not promises.** A teacher's or vendor's stated values are unfalsifiable; the cost of leaving is not. Nearly every dependence question below reduces to one question, estimable during evaluation:

> If this practice, teacher, tool, or service disappeared tomorrow, what capacity would the person retain, and what would it cost them to walk away?

Record that cost in hours, dollars, or lost capacity wherever it can be estimated. Capability-building practices leave you whole. Dependence-forming ones hold the benefit hostage.

### The effects discussion

Every evaluation carries, in prose, an effects discussion: **what does this subject affect, and in what ways, and how far does the improvement (or damage) travel?** This is description, not classification — practices affect multiple things in multiple ways at once, and they do not respect tier boxes. The discussion names the foundations, abilities, and relationships the subject touches, describes the direction and character of each effect, and estimates the reach.

Upstream improvements tend to travel furthest, per the model. A subject that improves sleep propagates that improvement through emotional regulation, presence, energy, and patience with others. A subject that tends a single relationship directly is not lesser for having narrower reach — it is doing different work, and the discussion describes the reach honestly rather than ranking it. The mirror also holds and matters more: a subject that damages a foundation while servicing a relationship — the fitness program that wrecks sleep — has its damage cascade through everything the foundation conditions, and the effects discussion is where that cascade is made visible.

Honest practices know what they affect. Overreaching ones claim relationship-level outcomes from mechanisms that never touch them.

## Layer one, the relationships and their foundations

What the idea, tool, or practice actually affects in a person's life. Foundations are scored first, then each relationship, each carrying a state-presence thread question. Every metric here is a relationship-quality or foundation-quality metric per the model; rate each named item.

### Foundations

Lens: person. For each foundation, the question is the same: does the subject strengthen, spare, or tax it?

- **Sleep.** Does it protect, improve, or tax sleep quantity and quality? Evening screen exposure, stimulation timing, and schedule pressure count. Because sleep sits upstream of so much, effects here weigh heavily in the effects discussion.
- **Access.** Scored in detail under Inclusive access in Layer two; recorded here because access is a foundation, and a subject's access posture belongs in its effects discussion alongside the other foundations.
- **Safety.** Physical and psychological. Does the practice create conditions in which the person can be honest, make mistakes, and disagree without harm?
- **Time.** Does the practice fit inside a real life, or demand time the person must take from sleep, relationships, or rest? A practice that only works at a dose the person cannot sustain taxes this foundation.
- **Material security.** Does the practice's cost structure threaten the person's financial footing at the dose that actually works? Escalating spend disguised as commitment rates Weak.

### Relationship with the body

Lens: person.

- **Movement.** Does it invite movement suited to the person's actual body, or prescribe movement suited to an imagined one?
- **Nourishment.** Does it support eating that sustains, or attach moral weight, restriction, or anxiety to food?
- **Rest and recovery.** Does it honour recovery as part of the practice, or treat rest as failure?
- **Pain and comfort.** Does it work with the body's signals or override them? "Push through pain" framing is a warning sign, not a feature.
- **Energy.** Over weeks, does the person report more energy or less? An observed indicator of the relationship's direction.
- **Presence thread.** Does the practice engage the body with awareness, or encourage dissociation from it — exercise as punishment, eating while distracted, metrics watched instead of sensations felt?

### Relationship with the mind

Lens: person.

- **Emotional range and regulation.** Does it expand the person's capacity to feel and regulate emotion, or narrow it — suppression marketed as calm, positivity enforced as policy?
- **Attention.** Does it gather attention or fragment it? The supportive-versus-dark-patterns table from the parent metrics applies verbatim to any digital subject.
- **Meaning and purpose.** Does it connect the practice to something the person recognizes as mattering, or manufacture goals for them — streaks, leaderboards, badges as ersatz purpose?
- **Competence and growth.** Is the person learning something real and transferable, or riding an engagement treadmill that resets daily?
- **Cognitive load.** Is the practice learnable without training, forgiving of lapses, and explained without blame?
- **Presence thread.** Does it cultivate awareness of mental activity, or feed absorption in it — rumination, anticipation, comparison, self-measurement?

### Relationships with others

Lens: person, others, community.

- **Connection.** Does it deepen relationships or substitute for them? A tool that simulates connection while displacing it rates Weak here regardless of how it markets itself.
- **Belonging.** Does the practice's community welcome the person as they are, or condition belonging on purchase, performance, or conformity?
- **Contribution.** Does it open paths for the person to give — teach, help, share — or position them permanently as consumer?
- **Trust and psychological safety.** Within the practice's community or between practitioner and teacher, can a person disagree, question, or leave without punishment? Charismatic authority structures rate Weak.
- **Load on others.** What does the person's practice cost the people around them, and is that cost visible and consented to?
- **Presence thread.** Does it support actually-being-with, or simulate connection while fragmenting attention — the phone at the dinner table, the notification during the conversation?

### The abilities, engage and build

Lens: person. For each ability named in the model — presence, emotional regulation, self-compassion, capacity to rest, and any added — ask two questions and rate each:

- **Engage.** Does the subject engage this ability during practice, or run on its absence?
- **Build.** Does the person walk away with more of this capacity, deployed elsewhere in their life? This is the reversibility question stated positively.

A subject that erodes presence while claiming to serve wellbeing fails at its foundation.

## Layer two, the fourth relationship

How the subject delivers its effects, and at what cost. Layer two is itself a relationship — the person's relationship with the practice, vendor, or teacher — and its whole function is to check whether that relationship is worthy of mediating the other three. Inclusive access asks whether the person can enter it. Agency and dependence asks about its power balance. Evidence and integrity asks whether the other party is honest. Endurance and exit asks whether the person can leave it whole. This is where the power thread earns its keep.

### Inclusive access

Lens: person, community. **[GATE]** if the access floor fails.

- **Physical access.** Can it be practised with a disabled body? Is there an adapted path, or does the practice quietly encode a nondisabled body as "normal"?
- **Economic access.** Is it free or affordable at the dose that actually works? Does the free tier deliver genuine benefit, or exist to convert?
- **Cognitive access.** Learnable without prior training? Plain language? Forgiving of lapses, and blame-free when they happen?
- **Linguistic and cultural access.** Available in languages the audience understands, and in the modalities of communication the audience uses? Where a practice is extracted from a tradition, is the source community credited, compensated, or erased?
- **Representation distance.** Are the people designing or teaching the practice drawn from, or accountable to, the communities most affected? Where this cannot be assessed from public information, rate Unknown and record that the absence is itself a data point.

### Agency and dependence

Lens: person. The reversibility test, applied specifically.

- **Exit cost.** The hours, dollars, or lost capacity needed to stop or switch. Record the estimate.
- **Capability transfer.** After a defined period, could the person continue the core practice with no product at all? A meditation app whose users can meditate without it has transferred capability; one whose users cannot has built dependence.
- **Data and record portability.** Journals, logs, streaks, histories — do they export in open, human-readable formats, or are they hostage?
- **Teacher and authority structure.** Is knowledge transferred or withheld? Progressive paywalled "levels" and initiation hierarchies are dependence structures; rate them as such.
- **Terms volatility and pricing asymmetry.** As in the parent metrics: how often have terms or prices changed unilaterally, and is pricing public or negotiated in the dark?

### Evidence and integrity

Lens: person, community. **[GATE]** for concealed harm or contraindications presented as universally safe.

- **Evidence base.** Is the claimed benefit supported by peer-reviewed research, by a tradition with a long observable track record, or by marketing alone? Record which, with citations where they exist.
- **Effect honesty.** Are claimed effect sizes proportionate to the evidence, or inflated? "Rewire your brain in ten days" is a rating of Weak in one sentence.
- **Harm profile.** What are the known adverse effects, and for whom? Meditation-related adverse events, exercise injury profiles, and contraindications for specific conditions exist and are documented; a subject that omits them entirely is concealing, not simplifying.
- **Falsifiability.** Could the practice's claims be wrong in principle? Claims constructed so that failure is always the practitioner's fault — "it didn't work because you didn't believe" — rate Weak and warrant a gate review.
- **Who profits from the claim.** Follow the money from the claim to its beneficiary. Independent replication by parties with nothing to sell weighs more than any number of vendor studies.

### Endurance and exit

Lens: person. **[GATE]** if no exit exists.

- **Benefit persistence.** Does the benefit persist after the practice ends, plateau into light maintenance, or vanish on stopping? Vanishing benefit plus high ongoing cost is a subscription to a state, not a practice.
- **Sustainable dose.** Is the practice sustainable in time, money, and effort at the dose that actually works — not the demo dose, the working dose?
- **Graceful stopping.** Can the person pause or stop without penalty, rebound, shame mechanics, or loss of their own records?
- **Practice longevity.** For tools and services: the parent metrics' longevity questions apply — institutional backing, funding model, maintenance activity. For traditions and methods: is the knowledge documented and free-standing, or locked in a single organization or person?

## Self-application

This document applies its own access obligations to itself, each requirement carrying a status and an evidence tag like any other rating. This section is updated at each version. The plain-language companion is tracked against the model document, which is what a general reader needs; this document remains the practitioner's tool.

| Requirement | Status at 0.3.0 | Evidence | What would resolve it |
|-------------|-----------------|----------|------------------------|
| Prose normative, diagrams navigational | Met trivially — this version contains no diagrams; the convention binds any future ones | Verified (by inspection, 2026-07-30) | Re-verify if diagrams are added |
| Reading level of this document measured | Not yet measured | Unknown | Run a readability measure, record instrument, score, and date |
| Translation feasibility (en, fr-CA, es) | Structurally feasible, en only | Inferred | fr-CA and es translations exist |

The Unknown and Inferred tags above are recorded rather than hidden, per this document's own rules.

## Using these metrics in the lifecycle

These metrics attach to the uc-radar lifecycle exactly as the parent metrics do.

- **Assess**, a light pass, ratings may carry Inferred and Claimed tags, gates checked on available evidence.
- **Trial**, the gate pass. All gate criteria, the harm profile, and the dependence questions must carry Verified tags before a subject moves to trial. For practices, trial means a bounded personal or small-group trial with defined duration and exit criteria, recorded.
- **Adopt**, the evaluation attaches to the adoption record and migrates with the entry.
- **Re-review**, adopted subjects are re-evaluated on a schedule or on trigger events: a change of ownership, pricing, or terms; new research on efficacy or harm; the appearance of engagement mechanics in a product update; a leadership or governance change in a practice community.

## Scorecard template

Copy this table into each evaluation and summarize one row per metric area. The effects discussion is prose and accompanies the table; it is not reducible to a row.

| Metric area | Rating | Evidence | Notes |
|-------------|--------|----------|-------|
| Foundation, sleep | | | |
| Foundation, safety | | | |
| Foundation, time | | | |
| Foundation, material security | | | |
| Body, movement | | | |
| Body, nourishment | | | |
| Body, rest and recovery | | | |
| Body, pain and comfort | | | |
| Body, energy | | | |
| Body, presence thread | | | |
| Mind, emotional range and regulation | | | |
| Mind, attention | | | |
| Mind, meaning and purpose | | | |
| Mind, competence and growth | | | |
| Mind, cognitive load | | | |
| Mind, presence thread | | | |
| Others, connection | | | |
| Others, belonging | | | |
| Others, contribution | | | |
| Others, trust and psychological safety | | | |
| Others, load on others | | | |
| Others, presence thread | | | |
| Ability, presence (engage / build) | | | |
| Ability, emotional regulation (engage / build) | | | |
| Ability, self-compassion (engage / build) | | | |
| Ability, capacity to rest (engage / build) | | | |
| Agency, the gap | | | |
| Inclusive access (physical, economic, cognitive, linguistic, representation) | | | |
| Agency and dependence (exit cost, capability transfer, portability, authority structure) | | | |
| Evidence and integrity (evidence base, effect honesty, harm profile, falsifiability, who profits) | | | |
| Endurance and exit (persistence, sustainable dose, graceful stopping, longevity) | | | |
| Gates | Pass / Fail (name any failed gate) | | |

## Further scaffolding

Measurement instruments for the framework's constructs, for citation if wanted: Brown and Ryan's Mindful Attention Awareness Scale and the Five Facet Mindfulness Questionnaire (trait presence); Neff's Self-Compassion Scale; the Multidimensional Assessment of Interoceptive Awareness (the body edge); decentering instruments (the mind edge); established relationship-quality measures (the others edge). On harms: the literature on meditation-related adverse events (e.g. Britton and colleagues) grounds the harm-profile requirement. Theoretical anchors — Self-Determination Theory, Ryff, PERMA, the capability approach, Killingsworth and Gilbert, Frankl — are cited in the model document.

## Resources

### Related documents

- Universal Cake Wellbeing Model (the theory this document operationalizes)
- Universal Cake Evaluation Metrics (parent metrics, shared vocabulary)
- UC Radar Entry Template
- UC Radar Evaluation Lifecycle

## License

This document, *Universal Cake Wellbeing Evaluation Metrics*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.3.0 | Draft | Split: the model moved to universal-cake-wellbeing-model v0.1.0, summarized in The model in brief and referenced throughout; this document retains the method (ratings, tags, gates, lenses, dependence, effects discussion, Layers one and two, self-application, lifecycle, scorecard); accessibility obligations inherited from the model document; scaffolding split, instruments here, theory there |
| 0.2.0 | Draft | Major restructure: wellbeing as relationship quality, foundations–abilities–relationships model with return loops, sleep to foundations, gates as floor conditions, effects discussion, self-application, Layer two as the fourth relationship |
| 0.1.1 | Draft | The three spheres section with hub diagram; access at the head of the causal chain; asymmetry paragraph |
| 0.1.0 | Draft | Initial complete draft |
