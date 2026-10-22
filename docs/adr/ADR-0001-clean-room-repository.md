# ADR-0001 — Clean-room repository

- Status: Accepted
- Date: 2026-10-22

## Context
The existing execution may contain undocumented assumptions and defects. The new environment must not inherit them by default.

## Decision
Build a new project here. Legacy code/results may be inspected as read-only evidence after documented intake. Code reuse requires provenance, licensing review, comparison, and an explicit ADR.

## Consequences
Start with contracts and tests, not copy/paste. Legacy findings remain distinct from validated scientific behavior.

S007 clarification addendum (2026-10-22): supplements record structure without
changing the accepted choice. Alternatives below are present review options, not
claims of undocumented historical evaluations.

## Options considered
For present review: continue clean-room isolation; copy legacy immediately; defer reuse. Immediate copying conflicts with D-0001 and licensing/evidence gates. This addendum does not claim a historical comparative experiment.

## Evidence and assumptions
Authority: D-0001, S002 report and docs/CLEAN_ROOM_BOUNDARY.md. No legacy source bundle has been audited. Tests establish bounded inventory behavior, not scientific correctness or licensing clearance.

## Validation and revisit conditions
Run repository-boundary tests/validator for inventory changes. Revisit only through a new ADR with provenance, licensing review and explicit comparison before any reuse.
