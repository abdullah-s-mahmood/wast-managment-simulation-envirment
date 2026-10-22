# S007 — Change control and architecture decisions

Date 2026-10-22 Asia/Baghdad; branch sprint/S007-change-control.
Base bd86e49e69e93f8d7e2a2ca527f962d22e180326; E-S007-01, ADR-0005.

Gap: existing ADRs lacked some required alternatives/evidence/revisit sections,
and material dependency/contract changes had no observable decision-record gate.
Added CHANGE_CONTROL.md, read-only validate_change_control.py, five tests,
explicitly dated clarifying addenda to ADR-0001–0005, template lifecycle/method
fields and dependent inventory/state/report/log changes. Accepted choices are
unchanged; ADR-0002 schema details remain provisional. Addenda explicitly avoid
claiming undocumented historical evaluations. No new science/architecture choice.

Author self-audit: six unique nonempty sections and explicit status per ADR,
Proposed/Provisional/Accepted/Rejected/Superseded are distinguishable. Declared
dependency/public-contract/science/irreversible changes require a complete
accepted ADR; routine corrections have rationale and no new ADR. Qualified
acceptance remains scope-bound; machine status parsing does not accept details.
Full diff/dependency/source review remains required: checker cannot infer hidden
undeclared code semantics, licensing, science validity or external authorization.

Linux x86_64 / Python 3.11.15, standard library.
python -m unittest discover -s tests -p test_change_control.py -v:
initial exit 1 test-first missing module; after validator exit 1 with 2 tests
failing (24 missing required sections in existing ADRs). Added labeled sections
without changing decisions; final focused exit 0, 5 tests. Same command and
missing-section mutations retain reproducers. Final regression E-S007-01 below.
WB: per-section completeness and statuses. BB: repository CLI distinguishes
complete records; each status tested independently. Adversarial: missing/duplicate
sections/status, absent decision for each material flag, nonaccepted decisions,
wrong booleans/missing declaration fields; no output state mutated. Metamorphic:
routine vs independently toggled material flags. Reference: original accepted
ADRs/D-0001–0008 preserved, not a scientific numerical calculation.
NOT RUN: Windows, simulators, physical/empirical validation; governance-only scope.
No stochastic/process/numeric/unit/time behavior introduced. Next after accepted
CI/integration: S008. Status and acceptance evidence must match actual GitHub runs.

## E-S007-02 — Accepted integration
- PR #12 exact head 0fa70fb0d21b4fced9239fe87dda5c8e2cb21503 passed CI run
  39711665684, completed/success; permitted merge 86326c298ccadd19bf2df3e78aec407db5ce5d6d.
- Published tree 62af707d8f1388c797b0ab93759a67f96a43e51b equals local checkpoint
  ecf99e9 tree, preserved branch. 44 tests/four validators pass.
- Author self-audit accepted S007 under ADR-0005 (7/88); S008 next.
- No change to prior accepted decisions or scientific/runtime validity claim.
