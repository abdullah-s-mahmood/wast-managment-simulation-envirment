# S051 — Sensor inventory and telemetry separation

- **Status:** NOT_STARTED
- **Phase:** P5 — Bin physical/environmental models
- **Risk:** MEDIUM
- **Prerequisite:** S050 must be `completed` in `docs/STATE/PROGRESS.json`.
- **Scope rule:** one sprint only; do not begin the next until this gate passes.

## Objective
Represent all sensors and internal fields while allow-listing what communication transmits.

## Scope
**In scope**
- Sensor registry and telemetry profile contract.
- Define observable contracts, units, identifiers, failure semantics, and evidence where relevant.
- Keep changes narrow and update dependent documentation only when required.

**Out of scope**
- Skipping gates for a quick demo.
- Treating legacy behavior, assumptions, or software tests as scientific validation.
- Unrelated features or unreviewed changes to accepted decisions.

## Prerequisites
S050 must be `completed` in `docs/STATE/PROGRESS.json`.
- Read `AGENTS.md`, progress state, handoff, blockers, and this sprint fully.
- Inspect repository status and relevant files before editing.
- If material evidence is unavailable, record a blocker; do not invent a substitute.

## Execution steps
1. State the observed behavior/evidence and exact gap.
2. Inspect relevant contracts/source locations; distinguish fact from inference.
3. Make the smallest change satisfying the objective.
4. Add/update tests and deterministic fixtures before relying on behavior.
5. Run WB, BB, adversarial/negative, regression, and applicable reference/integration tests.
6. Review the diff for hidden defaults, unit errors, IDs, secrets, partial writes, and scope creep.
7. Record exact commands, exit codes, environment, versions, expected/observed results, and artifacts.
8. Run `python scripts/validate_project_docs.py` if governance/state files changed.
9. Update progress and handoff only after verification; open a focused PR.

## Deliverables
- Sensor registry and telemetry profile contract.
- Test/validation evidence linked from `docs/STATE/VALIDATION_LOG.md`.
- Updated handoff/progress only when state truly changes.
- Any necessary evidence record, ADR, schema, fixture, or regression test.

## White-box tests
- Check internal invariants, state transitions, accounting, deterministic branches, and failure handling relevant to this sprint.
- **Sprint-specific check:** Check sensor units, sample intervals, source fields, and payload allow-list.
- Confirm exceptions do not leave hidden or contradictory state.
- For stochastic behavior, test seed/replay separately from empirical distribution validity.

## Black-box tests
- **Sprint-specific observable check:** Sensor may update internally without its field being transmitted.
- Exercise a small deterministic fixture through the public boundary.
- Verify output IDs, units, status, and errors are observable and traceable.
- Do not depend on undocumented chat context.

## Adversarial/negative tests
- **Required attack case:** Disabled sensor still transmits or internal state leaks into packet.
- Also test missing fields, malformed values, duplicate IDs, unsupported versions, boundaries, and interruption where relevant.
- Invalid input must fail closed before creating plausible-looking results.
- Preserve reproducers and diagnostics; do not hide a failure by retrying until green.

## Acceptance criteria
- [ ] Objective satisfied by observable behavior or reviewed artifact.
- [ ] WB checks pass or are explicitly not applicable with rationale.
- [ ] BB checks pass.
- [ ] Adversarial/negative checks pass.
- [ ] Units, IDs, time semantics, defaults, and provenance explicit where relevant.
- [ ] Scientific claims sourced or labelled provisional/unavailable.
- [ ] Actual commands, exit codes, environment, versions, and evidence recorded.
- [ ] No critical blocker hidden; tests not run disclosed.
- [ ] Progress, handoff, and validation log match reality.

## Evidence record
Record commit, changed files, source/evidence IDs and exact locations, commands/exit codes, platform/version, expected vs observed, fixture/config hashes, limitations, and review decision. Never claim a test passed unless it was executed and observed.

## Failure handling and rollback
- On failure, preserve the reproducer and mark `in_progress` or `blocked`; do not mark complete.
- Revert only this sprint's changes in a reviewable commit; never rewrite shared history.
- If evidence is inadequate, leave the model provisional and name the missing evidence.
- External simulator failure retains version, command, exit code, logs, and input hashes.

## Stop conditions
- Stop if a required source, equation, standard, license decision, or measurement is unavailable.
- Stop if a new architecture/science decision lacks an ADR.
- Stop if physical conservation, safety, raw-data integrity, or provenance cannot be protected.
- Do not ask routine questions answerable from repository docs; ask only for material ambiguity evidence cannot resolve or an irreversible choice.

## Handoff
Before closing, update `docs/STATE/AGENT_HANDOFF.md` with changes, tests/results, blockers, limitations, and next sprint ID: S052.

**Sprint-specific gate:** Sensor registry and telemetry profile contract. Gate passes only with recorded evidence, not merely file existence.
