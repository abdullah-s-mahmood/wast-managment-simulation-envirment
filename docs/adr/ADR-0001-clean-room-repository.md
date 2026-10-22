# ADR-0001 — Clean-room repository

- Status: Accepted
- Date: 2026-10-22

## Context
The existing execution may contain undocumented assumptions and defects. The new environment must not inherit them by default.

## Decision
Build a new project here. Legacy code/results may be inspected as read-only evidence after documented intake. Code reuse requires provenance, licensing review, comparison, and an explicit ADR.

## Consequences
Start with contracts and tests, not copy/paste. Legacy findings remain distinct from validated scientific behavior.
