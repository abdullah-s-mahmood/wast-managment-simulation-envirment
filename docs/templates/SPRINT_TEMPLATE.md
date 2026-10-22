# S### — Sprint title

- Status: NOT_STARTED
- Phase:
- Prerequisites:
- Risk level:
- Scope boundary: one sprint only

## Objective
One observable outcome.

## Scope
In-scope changes and explicit exclusions.

## Prerequisites
Read AGENTS.md and authoritative progress/handoff/blocker state.

## Execution steps
1. Inspect contracts and evidence.
2. Make the smallest change.
3. Add tests.
4. Run required test layers.
5. Record evidence and update state.

## Deliverables
List exact files/artifacts.

## White-box tests
Internal invariants, state, branches, and errors.

## Black-box tests
Observable behavior at the public boundary.

## Adversarial/negative tests
Malformed, missing, contradictory, boundary, duplicate, unsupported, interrupted, and corrupted inputs as relevant.

## Acceptance criteria
- [ ] Observable criteria pass.
- [ ] Commands and exit codes recorded.
- [ ] Evidence and units explicit.
- [ ] No critical blocker hidden.
- [ ] State matches reality.

## Evidence record
Commands, exit codes, environment, outputs, source IDs, and limitations.

## Failure handling and rollback
Preserve reproducers; do not hide failures or rewrite shared history.

## Stop conditions
Decisions/evidence that require a blocker rather than guessing.

## Handoff
Completed sprint, evidence, blockers, next eligible sprint.
