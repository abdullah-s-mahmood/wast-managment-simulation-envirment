# ADR-0003 — Separate hypotheses from scenario settings

- Status: Accepted
- Date: 2026-10-22

A hypothesis describes testable module behavior or a relationship. A scenario setting defines the case under study: city geometry, population heatmap, bin count, fleet size, depot location, climate input, or policy choice. Varying a scenario must not rewrite the model contract. Analysis states which factors are manipulated, held fixed, blocked, or measured.

S007 clarification addendum (2026-10-22): supplements record structure without
changing the accepted choice. Alternatives below are present review options, not
claims of undocumented historical evaluations.

## Context
A case setting can otherwise be mistaken for a scientific relationship or silently alter its definition.

## Options considered
Retain explicit separation; combine hypotheses and cases; defer classification. Mixing defeats controlled comparisons; S004 now supplies classification examples.

## Decision
Keep the original accepted separation. Rationale: varying a case must preserve a named model contract, while experimental roles and measured outcomes remain explicit.

## Evidence and assumptions
D-0002, S004 report and docs/HYPOTHESES_AND_SETTINGS.md. Its synthetic identity test proves a software boundary only, not causal identification or empirical validity.

## Consequences
Mixed statements split into distinct IDs; scenario changes reference stable model versions. New models need separate source/validation gates.

## Validation and revisit conditions
Run study-separation tests on boundary changes. Revisit classification with documented counterexample and ADR; any causal claim needs estimand, design, assumptions and diagnostics.
