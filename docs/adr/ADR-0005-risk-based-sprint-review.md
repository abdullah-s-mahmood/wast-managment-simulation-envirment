# ADR-0005 — Sole-maintainer, evidence-gated sprint acceptance

- **Status: Accepted** by the sole project owner, 2026-10-22.
- **Applies to:** S001–S088.
- **Supersedes:** Earlier proposed risk-based review requiring a second human.

## Context
The owner confirmed there is no additional human reviewer and explicitly cancelled
mandatory independent-person approval. S001 was blocked despite green tests and CI.

## Decision
**No second human reviewer or GitHub APPROVE review is required.** An authorized
agent may self-audit and merge its own sprint PR after passing all mandatory
sprint checks and GitHub CI at the **exact-head commit**, if GitHub permissions
and actual branch protections permit. Do not forge approvals or bypass settings.

## Mandatory acceptance gate
1. Complete all sprint acceptance criteria.
2. Run and record applicable WB, BB, adversarial/negative, regression,
   property/reference and integration tests. Mandatory FAIL or NOT RUN blocks.
3. Verify required GitHub CI success at the exact commit SHA to be merged.
4. Document a thorough **self-audit**, requirements traceability, changed-file
   scope, source evidence, commands, outcomes, limitations and honest verdict.
5. Merge through permitted GitHub operations, update progress and handoff
   to reflect actual integration, then continue to the next eligible sprint.

## Scientific and safety limits
Removal of a second PERSON does not remove independently reproducible scientific
calculations, sources, calibration/validation, statistical controls, safety,
physical conservation, privacy, licensing, or technical checks.
Higher-risk sprints require stronger **technical evidence**, not another person.
Stop on unresolved scientific evidence or irreversible high-impact decisions
instead of inventing parameters or bypassing protections.

## Consequences
S001 no longer needs an external reviewer; existing tests and exact-head CI are
still mandatory. No routine questions are required between completed sprints.
If a team is formed later, governance can change through a new ADR.
