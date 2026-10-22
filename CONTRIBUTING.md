# Contribution Rules

Use one branch per sprint, e.g. `agent/S001-charter-scope`. Keep PRs focused and include the sprint ID. Do not force-push shared branches or commit secrets, private datasets without permission, local paths, or unreviewed bulk outputs.

Every PR reports actual test commands/exit codes, tests not run, evidence IDs, assumptions, limitations, and rollback. Comments explain intent, units, invariants, or non-obvious rationale. Configuration examples are labelled synthetic or source-backed.

Review checklist:
- [ ] One-sprint scope.
- [ ] WB, BB, adversarial, and applicable reference/integration tests recorded.
- [ ] Units, timestamps, IDs, schema versions, and defaults explicit.
- [ ] Evidence and uncertainty documented.
- [ ] Raw data/provenance preserved.
- [ ] Failures and tests not run disclosed.
- [ ] Progress and handoff match reality.
