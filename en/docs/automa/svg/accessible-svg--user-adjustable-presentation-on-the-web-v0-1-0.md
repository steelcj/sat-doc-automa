---
dcterms:title: "Accessible SVG: User-Adjustable Presentation on the Web"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:description: "How to author SVG diagrams whose language, colour, typography, encoding, motion, and layout are set by the reader through a preferences toolbar rather than fixed by the author."
dcterms:created: "2026-07-26"
dcterms:modified: "2026-07-26"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:identifier: "accessible-svg--user-adjustable-presentation-on-the-web"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-07-26"
    author: "Christopher Steel"
    notes: >
      Initial draft. Supersedes an unversioned checklist-style answer on SVG
      accessibility, replacing its fifteen-point list with a presentation
      contract between the graphic and a reader-controlled preferences
      toolbar. Adds the multilingual string catalogue approach, the text
      reflow problem and its layout tier answer, the forced-colors and
      encoding-mode cases, the Universal Cake evaluation, and a prior art
      survey. Brought to the versioned-document standard with frontmatter,
      version block, Abstract, Sources and acknowledgements, License,
      Resources, References, and Changelog.
---

# Accessible SVG: User-Adjustable Presentation on the Web

Version: 0.1.0
Status: Draft
Style Guide: style-guide--web-ready-unrendered-markdown-using-apa-7

## Abstract

This document sets out how to author SVG diagrams whose presentation is decided by the reader rather than fixed by the author. It treats the graphic as a document with a declared presentation contract, a small set of custom properties and data attributes that a page-level preferences toolbar writes to, covering language, colour, contrast, typeface, text size, symbolic encoding, motion, and layout density. It states the mechanisms that work, names the ones that do not, and is honest about the single hard constraint: SVG text does not reflow, so adjustable typography requires either reserved label geometry, build-time line breaking, or an alternative layout. It closes with a Universal Cake evaluation and a survey of what appears to exist already.

## Sources and acknowledgements

The semantic requirements in this document derive from the <a name="apa-graphics-aria-citation"></a>[World Wide Web Consortium (2018)](#apa-graphics-aria-reference) WAI-ARIA Graphics Module and from the SVG Accessibility API Mappings working draft by <a name="apa-svg-aam-citation"></a>[Shelly and Rogers (2026)](#apa-svg-aam-reference). Conformance targets follow <a name="apa-wcag22-citation"></a>[Web Content Accessibility Guidelines 2.2 (World Wide Web Consortium, 2023)](#apa-wcag22-reference). The user requirements that motivate an adjustable graphic, rather than a merely labelled one, are drawn from the SVG Accessibility Task Force's own requirements wiki <a name="apa-svg-wiki-citation"></a>([World Wide Web Consortium, n.d.](#apa-svg-wiki-reference)), which names changeable contrast, typeface, weight, and stroke thickness as user needs. The preferences model follows the Fluid Infusion Preferences Framework <a name="apa-fluid-prefs-citation"></a>([Fluid Project, n.d.-a](#apa-fluid-prefs-reference)) developed at the Inclusive Design Research Centre, and the interoperability model follows the AccessForAll standards <a name="apa-iso-24751-2-citation"></a>([International Organization for Standardization & International Electrotechnical Commission, 2008a](#apa-iso-24751-2-reference)).

## The problem this document addresses

A conventional accessible SVG is a graphic that has been labelled. It carries a title, a description, sensible grouping, adequate contrast, and encodings that do not depend on colour alone. That is necessary and it is not sufficient, because every one of those decisions is still the author's. The reader who needs yellow on black, or twenty-four point labels, or the diagram in Spanish, or no colour at all because the page is being printed on a monochrome laser, receives the author's single fixed compromise.

The separation of presentation from content has been the stated route out of this since the earliest work on SVG accessibility, on the grounds that when presentation is separated the reader gains control over style <a name="apa-svg-access-citation"></a>([World Wide Web Consortium, 2000](#apa-svg-access-reference)). Twenty-six years later the tooling exists to act on that: custom properties, media queries for user preference, and mature preference editors that already adapt page text. What is missing is a documented contract that lets a graphic participate in the same adaptation as the prose around it.

This document defines that contract.

## Two different needs behind "make it bigger"

These are routinely conflated and the conflation is why adjustable diagrams break.

**Magnification** means the reader wants the whole graphic larger. Everything scales together, geometry and labels alike, the relationships between elements are preserved, and the cost is viewport area. This is solved entirely by a `viewBox` with no intrinsic `width` and `height`, sized by CSS, plus browser zoom. It requires no special authoring.

**Label legibility** means the reader wants the text larger relative to the graphic, because the text is what carries the meaning and the geometry is only scaffolding. Labels grow, geometry does not, and text that fitted its slot at eighteen units overflows it at thirty-two. This is the hard case, and it is the one a preferences toolbar actually triggers, because a toolbar text-size setting is a statement about reading, not about zoom.

An adjustable diagram must serve both, and must not silently answer the second request with the first.

## Prerequisite: the graphic must be in the document

Custom properties, scripted language switching, and page-level preference propagation all require the SVG to be part of the containing document's DOM and CSS cascade. An `<img src="diagram.svg">` renders in an isolated document that cannot see the parent's custom properties, classes, or script.

The rule is therefore: inline the SVG, or inject it at load time from an external file so that it is cached once and reused, and keep the file self-sufficient with an internal `<style>` element so that it still behaves correctly when it is opened directly, embedded as an image, or rasterised by a build tool. Internal styles and preference media queries do apply inside an `<img>`, so the standalone file degrades to a sensible author default rather than to nothing. Test that degradation deliberately; support for evaluating preference media queries inside an embedded image has been inconsistent across browser versions.

## The presentation contract

The graphic declares a small vocabulary and reads nothing else. The toolbar writes that vocabulary onto an ancestor element and knows nothing about the graphic's internals. Neither side imports the other.

| Property | Type | Meaning |
|----------|------|---------|
| `--uc-canvas` | colour | Background of the graphic |
| `--uc-ink` | colour | Default foreground for labels and line art |
| `--uc-cat-1` to `--uc-cat-8` | colour | Categorical encoding slots |
| `--uc-font` | font stack | Label typeface |
| `--uc-label-size` | length | Base label size in user units |
| `--uc-label-weight` | number | Label weight |
| `--uc-label-tracking` | length | Letter spacing |
| `--uc-line-height` | number | Multiplier for generated line breaks |
| `--uc-stroke` | number | Base stroke width |
| `--uc-texture` | 0 or 1 | Whether pattern fills are shown alongside colour |
| `data-uc-lang` | BCP 47 tag | Active language |
| `data-uc-tier` | keyword | `standard`, `spacious`, or `linear` |
| `data-uc-motion` | keyword | `full`, `reduced`, or `none` |
| `data-uc-detail` | keyword | `concise` or `full`, selecting description verbosity |

Two implementation details make this work rather than nearly work.

First, browsers do not substitute custom properties inside presentation attributes. A `fill="var(--uc-ink)"` attribute is inert. Variable-driven values belong in CSS declarations, applied by class. This turns out to be useful rather than annoying: presentation attributes sit at the very start of the author origin, so any class rule overrides them, and the attribute can therefore carry a hard-coded fallback for renderers that ignore stylesheets while the class carries the adjustable value.

```xml
<circle class="uc-shape uc-cat-1" cx="240" cy="200" r="130" fill="#0072B2" />
```

Second, the reader's explicit choice must beat the environment's inferred one. Put media query defaults in the stylesheet, and have the toolbar write custom properties as inline styles on the container, which win over any rule in the sheet. A reader who has asked for high contrast in daylight does not want a `prefers-color-scheme` guess to override the request.

## A working skeleton

The following is a complete file. It renders standalone, adapts to environment preferences unaided, and exposes the contract above.

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 720 420"
     class="uc-diagram"
     role="img"
     aria-labelledby="dg-title dg-desc"
     lang="en" xml:lang="en"
     data-uc-lang="en" data-uc-tier="standard" data-uc-motion="full">
  <title id="dg-title">Three conditions for learning</title>
  <desc id="dg-desc">A Venn diagram of three overlapping circles labelled Mindset, Motivation, and Methods. Each pair overlaps, and all three overlap at the centre, which is labelled Learning.</desc>

  <style>
    .uc-diagram {
      --uc-canvas: #ffffff;
      --uc-ink: #1a1a1a;
      --uc-cat-1: #0072b2;
      --uc-cat-2: #e69f00;
      --uc-cat-3: #009e73;
      --uc-font: "Atkinson Hyperlegible Next", "Atkinson Hyperlegible", system-ui, sans-serif;
      --uc-label-size: 20px;
      --uc-label-weight: 600;
      --uc-label-tracking: 0;
      --uc-stroke: 2.5;
      --uc-texture: 0;
    }
    .uc-canvas { fill: var(--uc-canvas); }
    .uc-shape { stroke: var(--uc-ink); stroke-width: var(--uc-stroke); fill-opacity: 0.28; }
    .uc-cat-1 { fill: var(--uc-cat-1); }
    .uc-cat-2 { fill: var(--uc-cat-2); }
    .uc-cat-3 { fill: var(--uc-cat-3); }
    .uc-texture { opacity: var(--uc-texture); }
    .uc-label {
      font-family: var(--uc-font);
      font-size: var(--uc-label-size);
      font-weight: var(--uc-label-weight);
      letter-spacing: var(--uc-label-tracking);
      fill: var(--uc-ink);
    }
    .uc-diagram:not([data-uc-lang="en"]) [lang="en"] { display: none; }
    .uc-diagram:not([data-uc-lang="fr"]) [lang="fr"] { display: none; }
    @media (prefers-color-scheme: dark) {
      .uc-diagram { --uc-canvas: #101214; --uc-ink: #f2f2f2; }
    }
    @media (prefers-contrast: more) {
      .uc-diagram { --uc-stroke: 4; --uc-label-weight: 700; --uc-texture: 1; }
      .uc-shape { fill-opacity: 0.15; }
    }
    @media (forced-colors: active) {
      .uc-canvas { fill: Canvas; }
      .uc-shape { fill: Canvas; stroke: CanvasText; }
      .uc-label { fill: CanvasText; }
      .uc-texture { opacity: 1; }
    }
  </style>

  <defs>
    <pattern id="uc-tex-1" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="currentColor" stroke-width="1.5" />
    </pattern>
    <pattern id="uc-tex-2" width="8" height="8" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.4" fill="currentColor" />
    </pattern>
    <pattern id="uc-tex-3" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M0 8 L8 0" stroke="currentColor" stroke-width="1.5" fill="none" />
    </pattern>
  </defs>

  <rect class="uc-canvas" x="0" y="0" width="720" height="420" />

  <g role="graphics-object" aria-labelledby="grp-1-title">
    <title id="grp-1-title">Mindset</title>
    <circle class="uc-shape uc-cat-1" cx="280" cy="190" r="130" fill="#0072b2" />
    <circle class="uc-texture" cx="280" cy="190" r="130" fill="url(#uc-tex-1)" color="#0072b2" />
    <text class="uc-label" x="196" y="96" text-anchor="middle" lang="en">Mindset</text>
    <text class="uc-label" x="196" y="96" text-anchor="middle" lang="fr">État d'esprit</text>
  </g>

  <g role="graphics-object" aria-labelledby="grp-2-title">
    <title id="grp-2-title">Motivation</title>
    <circle class="uc-shape uc-cat-2" cx="440" cy="190" r="130" fill="#e69f00" />
    <circle class="uc-texture" cx="440" cy="190" r="130" fill="url(#uc-tex-2)" color="#e69f00" />
    <text class="uc-label" x="524" y="96" text-anchor="middle" lang="en">Motivation</text>
    <text class="uc-label" x="524" y="96" text-anchor="middle" lang="fr">Motivation</text>
  </g>

  <g role="graphics-object" aria-labelledby="grp-3-title">
    <title id="grp-3-title">Methods</title>
    <circle class="uc-shape uc-cat-3" cx="360" cy="300" r="130" fill="#009e73" />
    <circle class="uc-texture" cx="360" cy="300" r="130" fill="url(#uc-tex-3)" color="#009e73" />
    <text class="uc-label" x="360" y="404" text-anchor="middle" lang="en">Methods</text>
    <text class="uc-label" x="360" y="404" text-anchor="middle" lang="fr">Méthodes</text>
  </g>
</svg>
```

Note the texture layers. They are separate elements at zero opacity by default, promoted to full opacity when the environment or the reader asks for non-colour encoding. `currentColor` on the pattern content lets each texture take its parent category colour without duplicating the pattern per category.

## Colour, contrast, and encoding modes

Colour is one channel among several and never the only one. The practical formulation is three encoding modes the reader can select.

- **Colour**, categorical fills from a colour vision deficiency safe palette, with labels
- **Colour and texture**, the same fills with distinct patterns overlaid, which survives greyscale printing and photocopying
- **Texture only**, monochrome fills with patterns and heavier outlines, for forced-colors mode and for readers who find saturated fills fatiguing

The default palette is the eight-colour set from the Color Universal Design work <a name="apa-okabe-ito-citation"></a>([Okabe & Ito, 2008](#apa-okabe-ito-reference)), popularised for scientific figures by <a name="apa-wong-citation"></a>[Wong (2011)](#apa-wong-reference). It was chosen empirically to stay distinguishable under protanopia, deuteranopia, and tritanopia, which together affect roughly eight percent of men and half a percent of women of northern European descent <a name="apa-okabe-ito-citation-2"></a>([Okabe & Ito, 2008](#apa-okabe-ito-reference)).

| Slot | Hex | Name |
|------|-----|------|
| `--uc-cat-1` | `#0072B2` | Blue |
| `--uc-cat-2` | `#E69F00` | Orange |
| `--uc-cat-3` | `#009E73` | Bluish green |
| `--uc-cat-4` | `#CC79A7` | Reddish purple |
| `--uc-cat-5` | `#56B4E9` | Sky blue |
| `--uc-cat-6` | `#D55E00` | Vermillion |
| `--uc-cat-7` | `#F0E442` | Yellow |
| `--uc-cat-8` | `#000000` | Black |

Two constraints apply on top of the palette. Text drawn in a category colour must still meet the text contrast ratios, which the lighter slots do not against white, so category colour is for fills and strokes and the label stays in `--uc-ink` <a name="apa-wcag-contrast-citation"></a>([World Wide Web Consortium Web Accessibility Initiative, n.d.-b](#apa-wcag-contrast-reference)). Any line, boundary, or fill that a reader must distinguish in order to understand the graphic is a graphical object under Success Criterion 1.4.11 and needs at least a three to one ratio against what sits next to it, which is why the outline stroke exists independently of the fill <a name="apa-wcag-nontext-citation"></a>([World Wide Web Consortium Web Accessibility Initiative, n.d.-a](#apa-wcag-nontext-reference)).

Forced colours mode deserves separate attention because it is where diagrams most often vanish. The operating system substitutes its palette for CSS colours in HTML, but SVG fills are not forced in the same way, so a diagram that encoded everything in fill colour becomes a field of undifferentiated shapes. Handle it explicitly with `@media (forced-colors: active)`, switch to system colour keywords, and turn textures on.

## Typography and the reflow problem

Use real text, always. Converting labels to paths destroys the accessible name, the ability to translate, selection, search, and the reader's typeface preference in one move. There is no case in an educational diagram where outlined text is the right trade.

Choose a typeface that survives poor conditions. Atkinson Hyperlegible was designed to make individual characters distinguishable rather than typographically uniform, and its 2025 successor extended coverage from twenty-seven to more than one hundred and fifty languages, with seven weights and a variable version <a name="apa-atkinson-citation"></a>([Braille Institute of America, 2025](#apa-atkinson-reference)). Multilingual coverage and a variable weight axis are exactly what an adjustable multilingual diagram needs, so it is a reasonable default, offered alongside the system stack and the reader's own choice.

Then the constraint. SVG text does not wrap. A `<text>` element is a single line at a fixed origin, and nothing in SVG 1.1 or in browser support for SVG 2 changes that. When `--uc-label-size` doubles, the label runs off its shape and over its neighbour. Three responses, in order of preference.

**Reserve the geometry.** Give every label a documented slot: an origin, a maximum width, an anchor, and a growth direction. Place slots outside shapes rather than inside them where the layout permits, since a slot with room to grow outward is the cheapest form of adjustability. Verify each slot against the longest translation at the largest supported size, not against the English string at the default size.

**Break lines at build time.** The build step measures each translated string in the target typeface at each supported size tier and emits `<tspan>` elements with computed `dy` offsets derived from `--uc-line-height`. This puts wrapping where the knowledge lives, in a build tool with font metrics, rather than in the browser, which will not do it for you. It is the reason this document treats a published SVG as a compiled artifact rather than as a source file.

**Change layout.** Past a certain size the diagram is no longer a diagram. Provide a `linear` tier that stacks the same content vertically with full-width labels, and treat the reader arriving there as a success rather than a fallback.

Avoid `textLength` with `lengthAdjust` as a fitting mechanism. It makes text fit by distorting glyph spacing or shapes, which trades the problem you can see for the one you cannot.

`<foreignObject>` with HTML inside will wrap text properly and inherits page typography directly. It is worth using when the graphic is inline in a browser and the wrapping is genuinely dynamic, but several non-browser rasterisers and print pipelines do not render it, so keep an SVG `<text>` fallback and treat the fallback as canonical.

One sizing subtlety to document per diagram: lengths inside the graphic are user units, mapped to CSS pixels by the `viewBox` and the rendered width. A twenty unit label is twenty pixels only when the mapping is one to one. Either render at a known width, or express the label size against a scale factor the enactor computes, and verify the effective rendered size at the narrowest supported viewport.

## Multilingual text

### Why switch and systemLanguage is not the mechanism

SVG has a built-in facility: `<switch>` selects the first child whose `systemLanguage` matches the user agent or operating system language <a name="apa-mdn-citation"></a>([Mozilla, n.d.](#apa-mdn-reference)). Wikimedia Commons uses it at scale, and the argument for it is real, one file, one set of geometry, all translations sharing every future correction to the drawing <a name="apa-commons-citation"></a>([Wikimedia Commons, n.d.](#apa-commons-reference)).

It is nevertheless the wrong mechanism here, for three reasons that have been understood in the SVG working group since 2006 <a name="apa-schepers-citation"></a>([Schepers, 2006](#apa-schepers-reference)). Evaluation follows the author's document order rather than the reader's order of preference, so a reader fluent in two languages gets whichever the author listed first. If no branch matches and no catch-all is present, nothing renders at all <a name="apa-mdn-citation-2"></a>([Mozilla, n.d.](#apa-mdn-reference)). And the matched language comes from the environment, which for a great many readers is not the language they would choose, and which in any case they cannot change from inside the page.

The last point is the disqualifying one. A toolbar exists precisely to let the reader override the environment. A mechanism that only reads the environment cannot be driven by one.

### Keep the strings, switch the presentation

Author every language as a sibling element carrying a `lang` attribute, and let a single attribute on the root select which is shown, as in the skeleton above. Use `display: none` for the inactive languages rather than opacity or off-canvas positioning, because `display: none` removes the content from the accessibility tree as well as from the picture, so no `aria-hidden` bookkeeping is required and no screen reader reads the diagram three times over.

Externalise the strings themselves. The repository source is a geometry template plus one message catalogue per language, keyed by identifier, and the build emits the compiled multilingual SVG. Translators never open the SVG, geometry changes never invalidate translations, and a missing key is a build error rather than a blank label.

```json
{
  "lang": "fr",
  "dir": "ltr",
  "title": "Trois conditions de l'apprentissage",
  "desc": "Diagramme de Venn à trois cercles qui se chevauchent, intitulés État d'esprit, Motivation et Méthodes. Chaque paire se chevauche, et les trois se chevauchent au centre, intitulé Apprentissage.",
  "labels": {
    "mindset": "État d'esprit",
    "motivation": "Motivation",
    "methods": "Méthodes",
    "centre": "Apprentissage"
  }
}
```

### Language, direction, and the accessible name

Three details separate a diagram that is translated from one that is genuinely multilingual.

Mark the language on the elements, not only on the file. Set `lang` and `xml:lang` on each language group so that speech synthesis selects the right voice mid-page. A French label announced by an English voice is worse than no label.

Swap the accessible name with the visible text. Only the first `<title>` child of an element is used, so a stack of translated titles does not work. Keep one `<title>` and one `<desc>` and have the enactor write their text content from the catalogue when the language changes, at the same moment it flips the visible labels. A graphic whose picture is in French and whose description is in English is a bug that no visual test will catch.

Handle direction and expansion as layout inputs. Right to left languages need `direction: rtl` and mirrored `text-anchor` values, and they need a per-element decision about whether the geometry itself should mirror: a reading-order arrow should, a map should not, so mark each with `data-uc-mirror`. For expansion, budget around forty percent over English for German and Finnish, and verify slots against the longest available string rather than the shortest.

## Semantics and structure

For a graphic that is a single indivisible illustration, `role="img"` with `aria-labelledby` pointing at the title and description is correct and well supported.

For a structured graphic whose parts are separately meaningful, the Graphics Module provides `graphics-document` for the whole, `graphics-object` for a part with internal structure, and `graphics-symbol` for an atomic part whose meaning matters more than its appearance <a name="apa-graphics-aria-citation-2"></a>([World Wide Web Consortium, 2018](#apa-graphics-aria-reference)). These roles let assistive technology navigate the graphic semantically instead of announcing one undifferentiated image.

Support is the caveat. The mapping specification remains a working draft <a name="apa-svg-aam-citation-2"></a>([Shelly & Rogers, 2026](#apa-svg-aam-reference)), so the roles are an enhancement layered over a structure that already works without them. Every group carries a `<title>` regardless of role, the reading order in the source matches the intended narrative order, identifiers describe meaning rather than appearance, and the text equivalent below carries the full content independently.

Reading order in source is worth stating plainly, because it is invisible when the file renders correctly and decisive when it is read aloud. Order the source as title, description, then each region as a unit with its label immediately following its shape, then any summary or centre element. Painting order occasionally conflicts with reading order; when it does, use explicit `z` ordering through separate layer groups rather than reordering the narrative.

## Motion

Animate only when the movement carries meaning, which in an educational diagram usually means sequencing or transition, never decoration.

Read `prefers-reduced-motion` for the default and let `data-uc-motion` override it. Reduced should mean the animation is replaced by its end state, not that it plays faster. Provide a control to replay, and never autoplay a loop. Nothing flashes.

## The non-visual equivalent is not a fallback

Every diagram ships with a text equivalent that carries the whole content: what the parts are, how they relate, and what the reader is meant to take from the arrangement. It is generated from the same source as the graphic, it is translated through the same catalogue, and it is available to everyone through a control on the figure rather than hidden behind assistive technology.

The `data-uc-detail` preference chooses between the concise form, which is the `<desc>` content, and the full form, which is the linearised structure with every label and relationship. Readers who do not use a screen reader use this too: it is what people copy, quote, and search.

This is also where verbosity belongs. Do not attempt to serve both a short accessible name and an exhaustive description from the same string.

## Wiring the graphic to a preferences toolbar

The toolbar on the Inclusive Design Research Centre site is an instance of the pattern Fluid Infusion calls UI Options, a separated-panel preferences editor built on the Infusion Preferences Framework <a name="apa-fluid-uio-citation"></a>([Fluid Project, n.d.-b](#apa-fluid-uio-reference)). The framework's structure is the useful part: preferences are model state, and enactors are the components that apply that state to the page <a name="apa-fluid-prefs-citation-2"></a>([Fluid Project, n.d.-a](#apa-fluid-prefs-reference)). Text size, contrast theme, and typeface already have enactors that operate on page text.

A diagram needs its own enactor because three of its preferences cannot be expressed as page CSS: the language swap must update `<title>` and `<desc>` alongside the visible labels, the encoding mode must toggle texture layers, and the layout tier must select among alternative geometries. Everything else is a custom property the page-level enactor could set directly.

The enactor below is deliberately framework-neutral. Call it from an Infusion model listener, from a plain `<select>`, or from a `matchMedia` handler.

```javascript
const CATALOGUE_CACHE = new Map();

async function loadCatalogue(langTag, basePath) {
  if (CATALOGUE_CACHE.has(langTag)) {
    return CATALOGUE_CACHE.get(langTag);
  }
  const response = await fetch(`${basePath}/${langTag}.json`);
  if (!response.ok) {
    throw new Error(`Missing message catalogue for ${langTag}`);
  }
  const catalogue = await response.json();
  CATALOGUE_CACHE.set(langTag, catalogue);
  return catalogue;
}

function applyVisualPreferences(diagram, prefs) {
  const tokens = {
    "--uc-canvas": prefs.canvas,
    "--uc-ink": prefs.ink,
    "--uc-font": prefs.fontFamily,
    "--uc-label-size": prefs.labelSize,
    "--uc-label-weight": prefs.labelWeight,
    "--uc-label-tracking": prefs.labelTracking,
    "--uc-stroke": prefs.strokeWidth,
    "--uc-texture": prefs.encoding === "colour" ? "0" : "1"
  };
  for (const [name, value] of Object.entries(tokens)) {
    if (value === undefined || value === null || value === "") {
      diagram.style.removeProperty(name);
    } else {
      diagram.style.setProperty(name, String(value));
    }
  }
  diagram.dataset.ucTier = prefs.tier;
  diagram.dataset.ucMotion = prefs.motion;
  diagram.dataset.ucDetail = prefs.detail;
}

async function applyLanguage(diagram, langTag, basePath) {
  const catalogue = await loadCatalogue(langTag, basePath);
  diagram.dataset.ucLang = langTag;
  diagram.setAttribute("lang", langTag);
  diagram.setAttribute("xml:lang", langTag);
  diagram.style.setProperty("direction", catalogue.dir);

  const title = diagram.querySelector(":scope > title");
  const desc = diagram.querySelector(":scope > desc");
  if (title) {
    title.textContent = catalogue.title;
  }
  if (desc) {
    desc.textContent = catalogue.desc;
  }
  for (const node of diagram.querySelectorAll("[data-uc-key]")) {
    const value = catalogue.labels[node.dataset.ucKey];
    if (value !== undefined) {
      node.textContent = value;
    }
  }
  return catalogue;
}

export async function applyDiagramPreferences(root, prefs, basePath) {
  const diagrams = root.querySelectorAll(".uc-diagram");
  for (const diagram of diagrams) {
    applyVisualPreferences(diagram, prefs);
    if (prefs.language) {
      await applyLanguage(diagram, prefs.language, basePath);
    }
  }
}
```

Two design decisions in that code are worth stating rather than leaving implicit. The enactor writes inline custom properties so the reader's choice outranks every media query default in the stylesheet. And it rewrites `<title>` and `<desc>` text content in the same call that rewrites the labels, because the failure mode of doing otherwise is silent and only surfaces for the readers least able to report it.

## Preferences should be portable

A preference set that lives in one site's local storage is a preference set the reader configures again on every site. The AccessForAll standards exist for this: a personal needs and preferences description is a machine-readable statement of what a reader requires, meant to be matched against a resource description of what a given resource can provide <a name="apa-iso-24751-2-citation-2"></a>([International Organization for Standardization & International Electrotechnical Commission, 2008a](#apa-iso-24751-2-reference); <a name="apa-iso-24751-3-citation"></a>[2008b](#apa-iso-24751-3-reference)).

Two things follow for a diagram. Preference names should map onto that vocabulary rather than being invented locally, so that a stored preference set travels. And the graphic should declare, in its `<metadata>`, which adaptations it actually supports, so that a matching engine can choose between a plain diagram and an adjustable one instead of guessing.

```xml
<metadata>
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:uc="https://universalcake.org/ns/adaptation#">
    <rdf:Description rdf:about="">
      <dcterms:title>Three conditions for learning</dcterms:title>
      <dcterms:creator>Christopher Steel</dcterms:creator>
      <dcterms:rights>SPDX-License-Identifier: AGPL-3.0-or-later</dcterms:rights>
      <dcterms:language>en</dcterms:language>
      <uc:availableLanguage>en</uc:availableLanguage>
      <uc:availableLanguage>fr</uc:availableLanguage>
      <uc:adjustable>colour</uc:adjustable>
      <uc:adjustable>contrast</uc:adjustable>
      <uc:adjustable>typeface</uc:adjustable>
      <uc:adjustable>textSize</uc:adjustable>
      <uc:adjustable>encodingMode</uc:adjustable>
      <uc:adjustable>motion</uc:adjustable>
      <uc:adjustable>layoutTier</uc:adjustable>
      <uc:textEquivalent>full</uc:textEquivalent>
    </rdf:Description>
  </rdf:RDF>
</metadata>
```

The `uc:` namespace above is a placeholder for a vocabulary this project has not yet defined. Defining it, or adopting an existing one, is an open question recorded below.

## The diagram as a compiled artifact

Everything above points the same direction. The published SVG is an output, not a source.

```text
diagrams/
  three-conditions/
    geometry.svg.tmpl      geometry, slots, classes, no strings
    strings/en.json        message catalogue per language
    strings/fr.json
    tokens.json            palette, type scale, stroke scale
    tiers.json             slot geometry per layout tier
```

The build resolves strings into slots, computes `<tspan>` breaks per language and per size tier from real font metrics, emits the metadata block, and produces both the compiled SVG and the text equivalent. It fails on a missing translation key, on a label that overflows its slot at the largest supported size, on a contrast pair below its target, and on a group without a title.

This is where accessibility conformance becomes mechanical rather than aspirational. A checklist a person runs after the fact catches what the person remembers to look for. A build that refuses to emit a graphic with an untitled group catches it every time.

## Universal Cake evaluation

### Sustainability (reduce)

The alternative to an adjustable graphic is a matrix of exported ones: light and dark, standard and high contrast, three languages, two sizes, which is twenty-four raster files for one diagram. Each is generated, stored, transferred, and regenerated whenever the diagram changes. One vector file with a presentation contract replaces the matrix, and the reduction is in bytes stored and transferred, in build compute on every subsequent edit, and in the human time that the regeneration would have consumed. The reduction is largest where it is least visible: in the edits that never happen because updating twenty-four files was too expensive to bother.

### Inclusive (economic and cognitive accessibility)

The immediate gain is the obvious one, that readers with low vision, colour vision deficiency, reading disabilities, and language needs other than the author's all get a presentation they can use from the same artifact. The less obvious gain is bandwidth. A vector diagram that adapts is a fraction of the weight of the raster set it replaces, which matters most on metered and intermittent connections, and it does not degrade when the connection forces a lower quality image.

Cognitive load is served by the layout tiers and the detail preference. A reader who needs less on screen at once can have it without losing the content.

### Agency (sovereignty)

This is the pillar the whole document turns on. A fixed graphic asserts that the author's visual judgement outranks the reader's knowledge of their own perception. An adjustable graphic returns that decision to the reader.

Sovereignty extends to the preferences themselves. Preferences held in an open, standards-aligned form travel with the reader; preferences held in a vendor's account are a dependency the reader did not ask for. The contract in this document is deliberately plain, custom properties and data attributes, so that it is implementable against any preference editor or none, and so that a reader with no toolbar at all still gets the environment defaults.

### Transparency

The metadata block states who made the graphic, under what licence, in which languages, and what it can adapt to. The build states what it verified. A reader or an integrator can determine what they are getting without opening it in a browser and guessing.

## Prior art, and what appears to be missing

The pieces exist separately.

Multilingual SVG in a single file is established practice at Wikimedia Commons, though through the author-controlled `switch` mechanism <a name="apa-commons-citation-2"></a>([Wikimedia Commons, n.d.](#apa-commons-reference)). Reader-controlled presentation preferences for page text are mature and deployed, in Infusion UI Options and its descendants <a name="apa-fluid-uio-citation-2"></a>([Fluid Project, n.d.-b](#apa-fluid-uio-reference)). Semantic structure for graphics is standardised <a name="apa-graphics-aria-citation-3"></a>([World Wide Web Consortium, 2018](#apa-graphics-aria-reference)). Media queries for colour scheme, contrast, forced colours, and reduced motion are broadly supported. Colour vision deficiency safe palettes are settled <a name="apa-okabe-ito-citation-3"></a>([Okabe & Ito, 2008](#apa-okabe-ito-reference)).

The requirements for the combination were articulated by the SVG Accessibility Task Force, whose user requirements wiki lists changeable luminosity contrast, changeable typeface and weight, changeable stroke thickness and colour, and behaviour that plays well with high contrast mode, alongside worked personas for exactly these needs <a name="apa-svg-wiki-citation-2"></a>([World Wide Web Consortium, n.d.](#apa-svg-wiki-reference)). That is close to the contract set out above, written down more than a decade ago.

What we have not found is a published open specification or reference implementation that connects a reader-facing preference editor to a graphic's presentation contract, including language, and treats the text equivalent as a first-class output. Commercial offerings advertise adaptive SVG with media query theming, and individual charting libraries implement parts of it internally, but a documented, reusable, standards-aligned contract does not appear to exist. This should be read as an invitation to look harder before building, not as a claim of novelty: the search space includes data visualisation research, digital publishing, and tactile graphics pipelines, and a negative result across a handful of searches is weak evidence.

## Conformance checklist

Verified by the build where the column says build, and by a person where it says manual.

| Check | Mode |
|-------|------|
| Every graphic has a title and a description | build |
| Every meaningful group has a title | build |
| No text converted to paths | build |
| Every label carries a catalogue key and every key resolves in every language | build |
| No label overflows its slot at the largest supported size in any language | build |
| Text contrast at least 4.5 to 1, graphical object contrast at least 3 to 1, in every theme | build |
| Content is understandable in greyscale and in texture-only mode | manual |
| Content is understandable in forced colours mode | manual |
| Reading order in source matches narrative order | manual |
| Screen reader announcement is correct in each language, with the right voice | manual |
| Reduced motion yields the end state, not a faster animation | manual |
| Text equivalent alone conveys the full content | manual |
| Graphic remains usable at 320 CSS pixels wide and at 400 percent zoom | manual |
| File still renders sensibly with no stylesheet and as an embedded image | build |

## Open questions

- Whether to define a `uc:` adaptation vocabulary or bind directly to the AccessForAll resource description terms, which are the standard but are oriented toward e-learning resources rather than components within a page
- Whether layout tiers should be authored by hand per diagram or derived by the build from slot geometry, and how many tiers are worth maintaining
- How the preference contract should behave for a diagram embedded in a document that is itself being exported to PDF, where the reader's preferences must be baked in at export time
- Whether the text equivalent should be generated into the page markup or fetched on demand, given that generating it inline doubles the payload for readers who never open it
- Whether to carry a tactile-graphics tier, given that the constraints are well documented and the build already knows the geometry

## Placement

This is the first document in an `accessibility` directory under `en/docs/guides/`:

```bash
en/docs/guides/accessibility/accessible-svg--user-adjustable-presentation-on-the-web-v0-1-0.md
```

The directory sits alongside `devops/` and `style-guides/` and holds guides on accessible implementation practice, as distinct from the style guides, which govern how documents are written.

## License

This document, *Accessible SVG: User-Adjustable Presentation on the Web*, by **Christopher Steel**, with AI assistance from **Claude Opus 5 (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Resources

### Graphics semantics

- [WAI-ARIA Graphics Module](#apa-graphics-aria-reference)
- [SVG Accessibility API Mappings](#apa-svg-aam-reference)
- [SVG Accessibility: People and Issues](#apa-svg-wiki-reference)
- [Accessibility Features of SVG](#apa-svg-access-reference)

### Conformance

- [Web Content Accessibility Guidelines 2.2](#apa-wcag22-reference)
- [Understanding Success Criterion 1.4.11: Non-text Contrast](#apa-wcag-nontext-reference)
- [Understanding Success Criterion 1.4.3: Contrast (Minimum)](#apa-wcag-contrast-reference)

### Preferences and interoperability

- [Infusion Preferences Editor](#apa-fluid-prefs-reference)
- [Infusion User Interface Options API](#apa-fluid-uio-reference)
- [ISO/IEC 24751-2, personal needs and preferences](#apa-iso-24751-2-reference)
- [ISO/IEC 24751-3, digital resource description](#apa-iso-24751-3-reference)

### Colour and typography

- [Color Universal Design](#apa-okabe-ito-reference)
- [Points of View: Color Blindness](#apa-wong-reference)
- [Atkinson Hyperlegible](#apa-atkinson-reference)

### Multilingual SVG

- [MDN, systemLanguage](#apa-mdn-reference)
- [Wikimedia Commons, Translation Possible](#apa-commons-reference)
- [www-svg, switch with systemLanguage](#apa-schepers-reference)

## References

<a name="apa-atkinson-reference"></a>Braille Institute of America. (2025). *Atkinson Hyperlegible font*. https://www.brailleinstitute.org/freefont/
[Return to citation](#apa-atkinson-citation)

<a name="apa-fluid-prefs-reference"></a>Fluid Project. (n.d.-a). *Preferences editor*. Infusion Documentation. Retrieved July 26, 2026, from https://docs.fluidproject.org/infusion/development/PreferencesEditor
[Return to citation](#apa-fluid-prefs-citation)

<a name="apa-fluid-uio-reference"></a>Fluid Project. (n.d.-b). *User interface options API*. Infusion Documentation. Retrieved July 26, 2026, from https://docs.fluidproject.org/infusion/development/UserInterfaceOptionsAPI
[Return to citation](#apa-fluid-uio-citation)

<a name="apa-iso-24751-2-reference"></a>International Organization for Standardization & International Electrotechnical Commission. (2008a). *Information technology, individualized adaptability and accessibility in e-learning, education and training, Part 2: "Access for all" personal needs and preferences for digital delivery* (ISO/IEC 24751-2:2008). https://www.iso.org/standard/43603.html
[Return to citation](#apa-iso-24751-2-citation)

<a name="apa-iso-24751-3-reference"></a>International Organization for Standardization & International Electrotechnical Commission. (2008b). *Information technology, individualized adaptability and accessibility in e-learning, education and training, Part 3: "Access for all" digital resource description* (ISO/IEC 24751-3:2008). https://www.iso.org/standard/43604.html
[Return to citation](#apa-iso-24751-3-citation)

<a name="apa-mdn-reference"></a>Mozilla. (n.d.). *systemLanguage*. MDN Web Docs. Retrieved July 26, 2026, from https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/systemLanguage
[Return to citation](#apa-mdn-citation)

<a name="apa-okabe-ito-reference"></a>Okabe, M., & Ito, K. (2008). *Color universal design (CUD): How to make figures and presentations that are friendly to colorblind people*. https://jfly.uni-koeln.de/color/
[Return to citation](#apa-okabe-ito-citation)

<a name="apa-schepers-reference"></a>Schepers, D. (2006, November 16). *Re: Switch with systemLanguage is broken by standards* [Mailing list post]. www-svg. https://lists.w3.org/Archives/Public/www-svg/2006Nov/0025.html
[Return to citation](#apa-schepers-citation)

<a name="apa-svg-aam-reference"></a>Shelly, C., & Rogers, M. (2026). *SVG accessibility API mappings* (W3C Working Draft). World Wide Web Consortium. https://www.w3.org/TR/svg-aam-1.0/
[Return to citation](#apa-svg-aam-citation)

<a name="apa-commons-reference"></a>Wikimedia Commons. (n.d.). *Translation possible/Learn more*. Retrieved July 26, 2026, from https://commons.wikimedia.org/wiki/Commons:Translation_possible/Learn_more
[Return to citation](#apa-commons-citation)

<a name="apa-wong-reference"></a>Wong, B. (2011). Points of view: Color blindness. *Nature Methods*, *8*(6), 441. https://doi.org/10.1038/nmeth.1618
[Return to citation](#apa-wong-citation)

<a name="apa-svg-access-reference"></a>World Wide Web Consortium. (2000). *Accessibility features of SVG*. https://www.w3.org/1999/09/SVG-access/note-20000702.html
[Return to citation](#apa-svg-access-citation)

<a name="apa-graphics-aria-reference"></a>World Wide Web Consortium. (2018). *WAI-ARIA graphics module* (W3C Recommendation). https://www.w3.org/TR/graphics-aria-1.0/
[Return to citation](#apa-graphics-aria-citation)

<a name="apa-wcag22-reference"></a>World Wide Web Consortium. (2023). *Web content accessibility guidelines (WCAG) 2.2* (W3C Recommendation). https://www.w3.org/TR/WCAG22/
[Return to citation](#apa-wcag22-citation)

<a name="apa-svg-wiki-reference"></a>World Wide Web Consortium. (n.d.). *SVG accessibility: People and issues* [Wiki]. Retrieved July 26, 2026, from https://www.w3.org/wiki/SVG_Accessibility/People_and_Issues
[Return to citation](#apa-svg-wiki-citation)

<a name="apa-wcag-nontext-reference"></a>World Wide Web Consortium Web Accessibility Initiative. (n.d.-a). *Understanding success criterion 1.4.11: Non-text contrast*. Retrieved July 26, 2026, from https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html
[Return to citation](#apa-wcag-nontext-citation)

<a name="apa-wcag-contrast-reference"></a>World Wide Web Consortium Web Accessibility Initiative. (n.d.-b). *Understanding success criterion 1.4.3: Contrast (minimum)*. Retrieved July 26, 2026, from https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
[Return to citation](#apa-wcag-contrast-citation)

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Initial draft; supersedes an unversioned checklist answer, reframing SVG accessibility as a presentation contract between the graphic and a reader-controlled preferences toolbar; adds the multilingual string catalogue, the text reflow constraint and layout tiers, encoding modes and forced colours, the enactor pattern, the Universal Cake evaluation, and a prior art survey |
