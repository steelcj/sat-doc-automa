# Versioning

Standing directives governing how documents are versioned and how that version is expressed, organized so that what applies by default is answerable by listing one directory.

## Structure

```
defaults/    the directives in force: what every document follows unless explicitly told otherwise
examples/    alternative directives for specific situations, adopted per-document or per-project, never silently
```

## Why this category is not per-format

Most sibling directories under `automa/` are organized per-format, one for markdown, one for SVG, one for AI collaboration. This directory is organized by concern instead, and deliberately so.

Versioning rules govern the artifact rather than its contents. How a version is expressed in a filename, and when that expression stops being used, are questions that arise identically for a markdown source, a rendered PDF, and any other published artifact. Filing such a rule under `markdown/` would state it too narrowly and leave the PDF beside it unaccounted for.

The test for whether a directive belongs here rather than in a format directory: if the rule would still hold when the document is exported to a different format, it belongs here.

## How defaults and examples relate

A directive's title states the rule itself and the directory it lives in states its status. Everything under `defaults/` is in force for all documents automatically. Documents under `examples/` hold alternatives, adopted per-document or per-project as a deliberate choice over the default. Neither kind of document repeats its status in its title; moving a directive between directories is a status change and is recorded in the document's changelog like any other change.

Adjusting a default over time means versioning the default document itself, the same way any versioned document changes, not editing an example into its place. The `defaults/` directory always answers the question "what is in force right now."

## Other formats

Format-specific directives live in their own sibling directories under `automa/`, each with the same `defaults/` and `examples/` shape. See [markdown](../markdown/) and [ai-collaboration](../ai-collaboration/).
