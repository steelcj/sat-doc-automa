---
dcterms:title: "CNCF Project Maturity Levels"
dcterms:version: "0.1.0"
dcterms:creator: "Christopher Steel"
dcterms:contributor: "Claude (Anthropic)"
dcterms:subject:
  - "reference"
  - "cncf"
  - "governance"
  - "open-source"
dcterms:description: "Reference document explaining the Cloud Native Computing Foundation's three project maturity levels, for use when evaluating CNCF-hosted tools on the uc-radar."
dcterms:publisher: "UniversalCake"
dcterms:created: "2026-07-25"
dcterms:modified: "2026-07-25"
dcterms:type: "Text"
dcterms:format: "text/markdown"
dcterms:language: "en"
sat:language_bcp47: "en"
dcterms:source: "https://www.cncf.io/projects/"
dcterms:relation: ""
dcterms:identifier: "cncf-project-maturity-levels"
dcterms:rightsHolder: "Christopher Steel"
dcterms:rights: >
  Copyright 2026 Christopher Steel / UniversalCake.
  SPDX-License-Identifier: AGPL-3.0-or-later
sat:uuid: ""
sat:version_at_creation: "0.4.0"
sat:migration_status: pre-sat
sat:changelog:
  - version: "0.1.0"
    date: "2026-07-25"
    author: "Christopher Steel, Claude (Anthropic)"
    notes: >
      Extracted from cloud-native-computing-foundation-about.md,
      previously sitting incorrectly in uc-radar adopt/ as if CNCF
      were an adopted tool. Keycloak-specific content removed, that
      context already lives in the IAM radar entry. Reformatted as
      a standing reference document for sat-doc-automa, with the
      version block, hyphenated filename suffix, em-dash-free
      definitions, and Changelog the versioned-documents guide requires.
---

# CNCF Project Maturity Levels

Version: 0.1.0
Status: Draft
Style Guide: style-guide--versioned-documents-in-unrendered-markdown

## Purpose

This document explains the Cloud Native Computing Foundation's three project maturity levels. It is reference material for use when evaluating CNCF-hosted tools on the uc-radar, specifically when assessing the Longevity and Market Position metrics under the Universal Cake Evaluation Metrics. A tool's CNCF maturity level is a governance signal, not a quality rating, it tells you about project health, contributor diversity, and resilience to single-vendor capture.

## What CNCF is

CNCF (Cloud Native Computing Foundation) is a vendor-neutral foundation under the Linux Foundation that hosts and governs open source projects in the cloud native infrastructure space. Kubernetes is the most well-known CNCF project.

## Maturity levels

CNCF has three maturity levels for hosted projects.

**Sandbox**, early-stage projects that the CNCF considers interesting and worth nurturing. Low bar for entry. No guarantee of production readiness or long-term sustainability. For radar purposes, treat Sandbox status as "the CNCF is watching this," not as an endorsement of readiness.

**Incubating**, projects that have demonstrated growth, a healthy contributor base, adoption by multiple organisations in production, and a governance structure that is not dependent on a single vendor. The project has passed a due diligence process. For radar purposes, Incubating status is a meaningful signal of project health and longevity, it means the CNCF has formally recognised the project as serious and production-used, with multi-vendor governance.

**Graduated**, the highest level. Projects that have reached broad production adoption, a mature governance model, and a demonstrated commitment to long-term sustainability. Kubernetes, Prometheus, Envoy, and Fluentd are examples. For radar purposes, Graduated status is the strongest available third-party governance signal for a cloud native tool.

## Relevance to Universal Cake Evaluation Metrics

A CNCF maturity level is relevant to two metrics areas.

Under **Longevity**, foundation governance is more resilient to key-contributor departure or commercial acquisition than single-company governance. A project under CNCF is not dependent on any one company's continued interest.

Under **Market Position**, specifically forkability and contributor concentration, CNCF governance ensures that no single vendor controls merge authority or project direction. This is a structural check on the power-imbalance proxies the metrics document asks about.

CNCF status does not substitute for the other metrics. A Graduated project can still fail on exit/portability, accessibility, or sovereignty. The maturity level tells you about governance, not about the product itself.

## License

This document, *CNCF Project Maturity Levels*, by **Christopher Steel**, with AI assistance from **Claude (Anthropic)**, is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html).

## Changelog

| Version | Status | Notes |
|---------|--------|-------|
| 0.1.0 | Draft | Extracted from cloud-native-computing-foundation-about.md; Keycloak-specific content removed; reformatted as a standing reference document with version block, em-dash-free definitions, and Changelog |
