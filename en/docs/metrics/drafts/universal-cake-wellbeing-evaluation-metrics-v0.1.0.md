---
dcterms:title: "Universal Cake Wellbeing Evaluation Metrics"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:contributor: "Claude (Anthropic)"
dcterms:subject:
  - "evaluation"
  - "metrics"
  - "wellbeing"
  - "presence"
  - "agency"
  - "inclusive design"
dcterms:description: "Evaluation metrics for ideas, tools, and practices that claim to bring about wellbeing. Defines the measurable foundations of wellbeing — three outcome spheres, an abilities axis headed by presence, and agency as the bridge — together with practice-level pillars evaluating how a subject delivers those outcomes and at what cost."
dcterms:publisher: "UniversalCake"
dcterms:created: "2026-07-30"
dcterms:modified: "2026-07-30"
dcterms:type: "Text"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:source: ""
dcterms:relation: "universal-cake-evaluation-metrics, uc-radar-entry-template, uc-radar--evaluation-lifecycle"
dcterms:identifier: "universal-cake-wellbeing-evaluation-metrics"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.1.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-07-30"
    author: "Christopher Steel, Claude (Anthropic)"
    notes: >
      Initial complete draft. Adapts the architecture of the
      Universal Cake Evaluation Metrics (v0.3.1) to the evaluation of
      ideas, tools, and practices that claim to bring about
      wellbeing. Defines a two-layer category set: layer one,
      wellbeing outcomes (Body, Mind, Others, each threaded with a
      state-presence question); layer two, the practice itself
      (inclusive access, agency and dependence, evidence and
      integrity, endurance and exit). Establishes presence as an
      ability rather than a fourth sphere, introduces the abilities
      axis with presence as its load-bearing member, and states the
      causal chain presence, agency, spheres, wellbeing as the
      framework's conceptual architecture. Carries over the rating
      scale, evidence tags, gate mechanism, and stakeholder lenses
      from the parent metrics so both documents share one vocabulary.
---

# universal-cake-wellbeing-evaluation-metrics-v0.1.0

Version: 0.1.0
Status: Draft

## Purpose

The general idea is the same one that animates the parent metrics: support more people in better ways that support wellbeing. Where the parent document evaluates products, services, and technical approaches, this document evaluates ideas, tools, and practices that claim to bring about wellbeing directly — meditation apps and meditation itself, exercise programs, therapy modalities, journalling methods, sleep tools, courses, communities, retreats, supplements-adjacent claims, and habits of any kind.

The wellbeing space needs this evaluation more than most. It is dense with unverifiable claims, guru dependence, subscription models that hold benefits hostage, and products that market presence while running on distraction. An evaluator that makes the difference visible — between what is claimed and what is verified, between what builds capacity and what builds dependence — is the tool this document defines.

The metrics ask two kinds of questions, mirroring the structural and interaction split in the parent document. Outcome questions ask what a practice does to a person's life across the three spheres. Practice questions ask how the subject delivers those outcomes, and at what cost, to whom.

## Conceptual architecture

The framework rests on one causal chain:

> **Presence (ability) → enables → Agency (exercised choice) → directed toward → the three spheres (Body, Mind, Others) → producing → wellbeing.**

Presence is treated as an ability, not a fourth sphere and not a region where the spheres overlap. Abilities belong to the person; the spheres describe domains of the person's life. Presence is what the person brings to whichever sphere they are inhabiting. It is trainable, it atrophies under hostile conditions, it is deployable across domains, and it is measurable with validated instruments.

Presence is load-bearing for agency. A person cannot choose among options they have not noticed, and cannot notice without being there. Presence opens the gap between stimulus and response; agency acts in that gap. An absent person still behaves, but their behaviour runs on default, habit, or even someone else's design.

This chain gives every practice-level question a common root: **does this subject widen the gap or close it?** Does it build the ability, respect the ability, and honour what the ability enables — the person's own goals?

Two clarifications keep the model honest:

- **Presence is not sufficient for wellbeing.** Attention is neutral; a person can be intensely present in an activity that harms them. Presence multiplies the value of what the spheres deliver, it does not replace them.
  - Creators note: We do not yet know what the spheres are in this document

- **Presence is not strictly necessary for every foundation.** Sleep is among the deepest foundations of wellbeing and involves no presence at all. The spheres carry weight of their own.

Two forms of presence are evaluated separately throughout:

- **State presence.** Being here, now, during the practice itself. Evaluated as a thread through each outcome sphere: does the practice engage the sphere with awareness, or run on distraction?
- **Trait presence.** The cultivated capacity to return to the present, retained after the practice ends. Evaluated under the abilities axis: does the person walk away with more capacity to be present elsewhere in their life?

A practice can score well on one and not the other. A gripping game engages attention totally, yet may not build towards wellbeing. Effortful meditation training may be unglamorous in the moment even though it may be more likely build the foundations of wellbeing. The best practices do both, and surfacing that difference is a core function of this evaluator.

## How to answer

### Rating scale

Answer each metric with one of the following ratings so that evaluations remain comparable across subjects, over time, and with the parent metrics.

- **Strong**, the subject actively advances this value
- **Moderate**, the subject is adequate, with named limitations
- **Weak**, the subject works against this value
- **Unknown**, insufficient information to rate, record what would resolve it

### Evidence tags

Tag every rating with how it is known.

- **Verified**, confirmed by direct trial, testing, measurement, or peer-reviewed research, record the method and date
- **Inferred**, a reasonable conclusion from the practice's structure, mechanism, or documentation, not yet tested
- **Claimed**, asserted by the vendor, teacher, or community, not independently checked

Evidence tags matter more here than in technical evaluation. Wellness claims are overwhelmingly Claimed rather than Verified, and making that visible is half this tool's value. A rating of Strong with a tag of Claimed is weaker than a rating of Moderate with a tag of Verified.

### Gates

Some criteria are gates, not scores. A failed gate cannot be averaged away by strength elsewhere; it moves the subject to hold or rejected in the uc-radar lifecycle until the named condition changes. Gate criteria are marked **[GATE]** throughout. The default gates are:

- Credible harm or contraindications concealed, or the practice presented as universally safe when it is not
- Failure of the access floor, the practice is unreachable for people with disabilities, low income, or without prior training, and no adapted path exists
- No exit, stopping incurs penalty, rebound, loss of accumulated benefit records, or loss of the person's own data
- Engagement mechanics that attack presence — streaks, manufactured urgency, infinite feeds — that cannot be disabled, in a product claiming to serve wellbeing

Projects may add gates but should not remove these without recording why.

### Stakeholder lenses

Each question is asked from one or more perspectives. Where perspectives conflict, record the conflict rather than letting one answer hide the other.

- **Person**, the individual undertaking the practice
- **Others**, household, family, and relationships affected by the person's practice
- **Community**, the wider group of practitioners, contributors, and the public affected
- **Environment**, energy, material, travel, and consumption consequences of the practice

Example of a conflict worth surfacing: a retreat may increase the person's wellbeing while imposing costs on a household left to absorb their absence, or a fitness practice may benefit the person while its equipment and travel footprint burdens the environment.

### Measuring dependence

Two principles from the parent metrics apply directly, translated.

**Asymmetry of information is itself measurable.** Compare what each party can know. A wellness vendor with engagement telemetry on a person's every session, facing a person who cannot see the evidence base, the pricing model, or the mechanism, scores badly regardless of stated intentions.

**Measure reversibility, not promises.** A teacher's or vendor's stated values are unfalsifiable; the cost of leaving is not. Nearly every dependence question below reduces to one question, estimable during evaluation:

> If this practice, teacher, tool, or service disappeared tomorrow, what capacity would the person retain, and what would it cost them to walk away?

Record that cost in hours, dollars, or lost capacity wherever it can be estimated. Capability-building practices leave you whole. Dependence-forming ones hold the benefit hostage.

## Layer one, wellbeing outcomes

What the idea, tool, or practice actually affects in a person's life. Each sphere carries its own questions plus a state-presence thread question. Rate each named item.

### Body

Lens: person.

- **Sleep.** Does it protect, improve, or tax sleep quantity and quality? Evening screen exposure, stimulation timing, and schedule pressure count.
- **Movement.** Does it invite movement suited to the person's actual body, or prescribe movement suited to an imagined one?
- **Nourishment.** Does it support eating that sustains, or attach moral weight, restriction, or anxiety to food?
- **Rest and recovery.** Does it honour recovery as part of the practice, or treat rest as failure?
- **Pain and comfort.** Does it work with the body's signals or override them? "Push through pain" framing is a warning sign, not a feature.
- **Energy.** Over weeks, does the person report more energy or less?
- **Presence thread.** Does the practice engage the body with awareness, or encourage dissociation from it — exercise as punishment, eating while distracted, metrics watched instead of sensations felt?

### Mind

Lens: person.

- **Emotional range and regulation.** Does it expand the person's capacity to feel and regulate emotion, or narrow it — suppression marketed as calm, positivity enforced as policy?
- **Attention.** Does it gather attention or fragment it? The supportive-versus-dark-patterns table from the parent metrics applies verbatim to any digital subject.
- **Meaning and purpose.** Does it connect the practice to something the person recognizes as mattering, or manufacture goals for them — streaks, leaderboards, badges as ersatz purpose?
- **Competence and growth.** Is the person learning something real and transferable, or riding an engagement treadmill that resets daily?
- **Cognitive load.** Is the practice learnable without training, forgiving of lapses, and explained without blame?
- **Presence thread.** Does it cultivate awareness of mental activity, or feed absorption in it — rumination, anticipation, comparison, self-measurement?

### Others

Lens: person, others, community.

- **Connection.** Does it deepen relationships or substitute for them? A tool that simulates connection while displacing it rates Weak here regardless of how it markets itself.
- **Belonging.** Does the practice's community welcome the person as they are, or condition belonging on purchase, performance, or conformity?
- **Contribution.** Does it open paths for the person to give — teach, help, share — or position them permanently as consumer?
- **Trust and psychological safety.** Within the practice's community or between practitioner and teacher, can a person disagree, question, or leave without punishment? Charismatic authority structures rate Weak.
- **Load on others.** What does the person's practice cost the people around them, and is that cost visible and consented to?
- **Presence thread.** Does it support actually-being-with, or simulate connection while fragmenting attention — the phone at the dinner table, the notification during the conversation?

## The abilities axis

Lens: person. Abilities are what the person retains when the practice, tool, or teacher is taken away. They are the framework's answer to the reversibility question, stated positively. For each ability, ask two questions: does the subject **engage** it during practice, and does it **build** it — leaving the person with more capacity deployed elsewhere in their life?

- **Presence.** The load-bearing ability, first among them because agency depends on it. Trainable, measurable (MAAS, FFMQ acting-with-awareness facet), and under active attack from the attention economy. A subject that erodes this ability while claiming to serve wellbeing fails at its foundation.
- **Emotional regulation.** The capacity to notice, name, tolerate, and modulate emotional states. Depends on presence — an emotion not noticed cannot be regulated.
- **Self-compassion.** The capacity to meet one's own failure without contempt. Practices that motivate through shame score Weak here even when they produce short-term compliance.
- **Capacity to rest.** The ability to stop, genuinely, without guilt and without a screen. Increasingly rare, rarely trained, and a legitimate output for a practice to claim.

This list is non-exhaustive. New abilities are added as evaluation demands, using the same engage/build pair of questions.

## Agency, the bridge

Lens: person. Agency is where layer one meets layer two: the exercised choice that directs a person's abilities toward their spheres. Every interaction with the subject can be tested with the parent metrics' question, **whose goal does this interaction serve, and would the person recognize it as their own?**

Dark patterns are attacks on presence in order to defeat agency. Infinite scroll does not argue with a person's goals; it prevents the moment of noticing in which those goals would be consulted. Autoplay removes the stopping point precisely because a stopping point is where presence re-enters and a choice gets made. Manufactured urgency floods the gap so nothing deliberate can happen in it. The supportive patterns are the mirror image: honest defaults, natural endings, and quiet-by-default all protect the gap.

- Does the practice widen the gap between stimulus and response, or close it?
- Are goals set by the person, or manufactured by the subject?
- Can the person adjust the practice — intensity, schedule, method — or is deviation treated as failure?
- When the person and the practice disagree, who wins?

## Layer two, the practice itself

How the subject delivers its outcomes, and at what cost. This is where the power thread earns its keep.

### Inclusive access

Lens: person, community. **[GATE]** if the access floor fails.

- **Physical access.** Can it be practised with a disabled body? Is there an adapted path, or does the practice quietly encode a nondisabled body as "normal"?
- **Economic access.** Is it free or affordable at the dose that actually works? Does the free tier deliver genuine benefit, or exist to convert?
- **Cognitive access.** Learnable without prior training? Plain language? Forgiving of lapses, and blame-free when they happen?
- **Linguistic and cultural access.** Available in languages the audience understands? Where a practice is extracted from a tradition, is the source community credited, compensated, or erased?
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

## Using these metrics in the lifecycle

These metrics attach to the uc-radar lifecycle exactly as the parent metrics do.

- **Assess**, a light pass, ratings may carry Inferred and Claimed tags, gates checked on available evidence.
- **Trial**, the gate pass. All gate criteria, the harm profile, and the dependence questions must carry Verified tags before a subject moves to trial. For practices, trial means a bounded personal or small-group trial with defined duration and exit criteria, recorded.
- **Adopt**, the evaluation attaches to the adoption record and migrates with the entry.
- **Re-review**, adopted subjects are re-evaluated on a schedule or on trigger events: a change of ownership, pricing, or terms; new research on efficacy or harm; the appearance of engagement mechanics in a product update; a leadership or governance change in a practice community.

## Scorecard template

Copy this table into each evaluation and summarize one row per metric area.

| Metric area | Rating | Evidence | Notes |
|-------------|--------|----------|-------|
| Body, sleep | | | |
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

For citation, if wanted: Deci and Ryan's Self-Determination Theory (autonomy, competence, relatedness) maps nearly one-to-one onto Mind, Others, and the agency bridge. Ryff's psychological wellbeing dimensions and Seligman's PERMA are the standard multi-dimensional wellbeing anchors. Killingsworth and Gilbert's experience-sampling work grounds the claim that presence multiplies wellbeing largely independent of activity. Brown and Ryan's Mindful Attention Awareness Scale and the Five Facet Mindfulness Questionnaire ground trait presence as measurable. Sen and Nussbaum's capability approach grounds the abilities axis. Frankl grounds the gap between stimulus and response. Neff grounds self-compassion as a measurable construct. On harms: the literature on meditation-related adverse events (e.g. Britton and colleagues) grounds the harm-profile requirement.

## Resources

### Related documents

- Universal Cake Evaluation Metrics (parent document, shared vocabulary)
- UC Radar Entry Template
- UC Radar Evaluation Lifecycle

## License

This document, *Universal Cake Wellbeing Evaluation Metrics*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial complete draft. Two-layer category set (outcome spheres threaded with state-presence questions; practice-level pillars), abilities axis headed by presence, agency as the bridge, presence-agency-spheres causal chain stated as conceptual architecture, rating scale, evidence tags, gates, and stakeholder lenses carried over from the parent metrics |
