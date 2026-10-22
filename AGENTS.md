# Mandatory Operating Protocol for Every AI Agent

This file is the source of truth for agent behavior. Follow it before inspecting or changing any project file.

## 1. Resume without routine questions

At the start of every session, read in this order:
1. `README.md`
2. `AGENTS.md`
3. `docs/STATE/PROGRESS.json`
4. `docs/STATE/AGENT_HANDOFF.md`
5. `docs/STATE/BLOCKERS.md`
6. `docs/STATE/DECISION_LOG.md`
7. `docs/SPRINT_INDEX.md`
8. The complete file for the next eligible sprint in `docs/sprints/`.

Do not depend on chat history. The repository must contain enough state to resume work.

## 2. Strict sprint selection

- Select the lowest-numbered sprint not marked `completed`.
- Start only if every prerequisite is marked `completed`.
- Execute one sprint at a time. Do not skip, combine, reorder, or mark future work complete for convenience.
- Current bootstrap state: S001 is next. No simulation implementation or scientific model has been accepted.
- A status change is not proof of completion; acceptance evidence is required.

## 3. Mandatory workflow for each sprint

1. Inspect repository status, relevant files, and current diff.
2. Read the sprint contract completely.
3. State the exact gap and create a narrow implementation/test plan.
4. Change only files needed for that sprint and its tests.
5. Add/update tests before relying on new behavior.
6. Run required white-box, black-box, adversarial/negative, regression, and applicable reference/integration tests.
7. Run `python scripts/validate_project_docs.py` after governance/progress changes.
8. Record exact commands, exit codes, platform, versions, outputs, artifacts, and tests not run.
9. Review the diff for scope creep, hard-coded settings, undocumented units, secrets, and false claims.
10. Update progress, handoff, validation log, and blockers to match actual state.
11. Open a focused PR with the sprint ID. Do not self-approve or self-merge.
12. Mark complete only after every mandatory gate passes and evidence is linked.

## 4. Allowed statuses

Allowed values: `not_started`, `in_progress`, `blocked`, `in_review`, `completed`.

Permitted transitions:
- `not_started -> in_progress`
- `in_progress -> blocked | in_review`
- `blocked -> in_progress` only after blocker resolution is evidenced
- `in_review -> in_progress` when changes are requested, or `completed` after accepted review
- `completed -> in_progress` only through a documented regression/reopen decision

Never edit progress merely to make a dashboard look green.

## 5. Scientific integrity gates

- Do not invent papers, DOI values, standards, equations, parameters, distributions, calibration data, or results.
- Distinguish `observed in legacy code`, `reported by a source`, `derived mathematically`, `scenario input`, `provisional assumption`, and `validated by test`.
- A passing software test proves only the tested software property, not physical accuracy.
- Every accepted scientific model needs a traceable source, exact equation, variable definitions, units, applicability domain, uncertainty/limitations, reference tests, and an empirical/independent validation plan.
- No causal inference claim without a stated estimand, identification assumptions, design justification, and diagnostics.
- Preserve failed runs and negative results. Do not promise 100% correctness; state the tested domain and residual risks.

## 6. JSON-first and clean-room rules

- Scenario settings and model parameters must not be hidden in source code.
- Keep specifications, scenario settings, mutable runtime state, telemetry payloads, and derived analysis outputs separate.
- Use stable IDs, explicit units, schema versions, deterministic seed management, and provenance hashes.
- Do not copy legacy code into this repository by default. Legacy source audit is read-only; reuse requires provenance, licensing review, comparison, and an explicit ADR.
- Do not commit secrets, local machine paths, or private data without authorization.
- Never silently default an invalid physical/network parameter to a plausible-looking value.
- Internal sensor state is not automatically transmitted; telemetry uses an explicit allow-list.
- PLC behavior retains the currently approved source set until an evidence-backed decision explicitly changes it.

## 7. Required test layers

- **White-box:** internal invariants, state transitions, accounting, deterministic branches, error handling, dependency boundaries.
- **Black-box:** observable behavior through public interfaces and produced artifacts.
- **Adversarial:** malformed, missing, contradictory, extreme, boundary, reordered, duplicated, interrupted, corrupted, and unsupported inputs.
- **Property/metamorphic:** general invariants across generated inputs where applicable.
- **Reference/differential:** hand-calculated or source-backed expected values where available.
- **Integration/cross-platform:** actual adapter boundaries and every platform advertised as supported.

If a dependency/platform is unavailable, report NOT RUN and keep the gate open. Do not fabricate test execution.

## 8. Failure and recovery

- Do not delete user data, force-push, rewrite shared history, or perform destructive actions without explicit authorization.
- Preserve minimal reproducers, logs, input hashes, and exit codes.
- If a failure could corrupt scientific results, stop the pipeline and mark the run failed; do not continue with partial data.
- If a requirement affects scientific validity, safety, licensing, data integrity, or an irreversible choice and evidence cannot resolve it, stop and log a blocker instead of guessing.

## 9. Completion report

For each sprint report: ID/title; files changed; decisions/evidence IDs; exact test commands and exit codes; tests passed/failed/not run; evidence paths; blockers; known limitations; next sprint ID. “Everything works” is not an acceptable report.

## 10. Non-negotiable order

Evidence and requirements -> schemas/contracts -> isolated modules -> module tests -> adapters -> integrated runs -> raw-data validation -> statistical analysis -> UI/export -> release. Do not reverse this order for a quick demo.
