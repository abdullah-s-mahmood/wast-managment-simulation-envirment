# Change control and architecture decisions

Authority: AGENTS.md, ADR-0005 and S007. Routine implementation within an accepted
contract proceeds autonomously. Material changes need a reviewable ADR and
stronger evidence; a second human is not required. External restrictions,
irreversible/privacy/paid actions retain applicable explicit authorization rules.

## When a record is required
A new dependency, changed public JSON/API/behavior contract, scientific equation/
parameter/source/domain choice, licensing/reuse choice or irreversible design
choice is material. Record compatibility, migration, consumers and rollback.
Do not hide a dependency behind a helper, change defaults in place, replace PLC
sources silently, or label a contract change a bug fix without evidence.
Routine fixes that restore an accepted contract need a scoped rationale and tests;
they do not automatically need a new architecture decision or user confirmation.

Before edits: inspect full diff, dependency manifests, public signatures/schema
versions, accepted ADRs and affected source/evidence locations. Enumerate affected
consumers and input/output/provenance changes. Declarations do not discover code
semantics: full diff review must independently check them. Missing evidence is a
blocker; an ADR is not permission to invent science or bypass a sprint prerequisite.

## Record and lifecycle
Use docs/templates/ADR_TEMPLATE.md with a unique ADR-NNNN ID and date. Include
context/constraints, options including deferral, exact decision/rationale/scope,
source evidence and provisional assumptions, consequences/risks/migration, tests
and explicit revisit conditions. Variable units/domain/uncertainty belong to the
scientific evidence record, linked from the ADR, not unexplained numbers here.

- Proposed: documented option; not implementation authority.
- Provisional: bounded assumption/decision awaiting named evidence; cannot be
  presented as accepted science or permit bypass of mandatory missing evidence.
- Accepted: choice accepted within its stated scope under the owner-authorized
  technical gate. Qualifiers remain binding (ADR-0002 accepts a principle only).
- Rejected: retained with rationale; not implementation authority.
- Superseded: retained history with replacement ID and reasons; old consumers,
  migration and regression coverage must be accounted for before switching.

Proposed may become Provisional, Accepted or Rejected with evidence/rationale.
Provisional may become Accepted or Rejected when its named gate is resolved.
Accepted becomes Superseded through a new accepted ADR; do not silently rewrite
its historical choice. Rejected/superseded records stay immutable in meaning;
reconsideration uses a new ID. Corrections/addenda label date and changed scope,
retain original evidence, and do not imply an unperformed historical evaluation.
Do not reuse IDs, create cycles or silently turn qualified acceptance into full
acceptance. Record decision IDs/revisit trigger in STATE/DECISION_LOG.md and the
owning sprint report; record concrete blockers in STATE/BLOCKERS.md.

## Observable checks and integration
`scripts/validate_change_control.py` checks each ADR's explicit status and six
nonempty unique sections. Its check_change public function accepts a version-1
declaration with adds_dependency, changes_public_contract, changes_science,
irreversible (strict booleans), decision_id and nonempty rationale. Any true flag
requires an existing complete Accepted record; other statuses fail closed. Routine
changes use no decision ID. This read-only example checks declarations, not their
truth, scientific acceptance, authorization or all dependencies hidden in code.

Run `python scripts/validate_change_control.py` and
`python -m unittest discover -s tests -p test_change_control.py -v`.
CLI exits 0 for complete records, 1 for invalid/missing/duplicate records and
writes no artifacts. Status is distinct from sprint status. No model units,
scenario defaults, timestamps or random seeds are introduced by this policy.

Author self-audit must match declared flags to the actual diff, assess qualified
scope and required source tests, then verify exact-head CI and permitted merge.
Update progress/handoff/report/validation records only with observed results.
Public contract changes require explicit version/migration/negative compatibility
checks in their owning sprint. Revert only the scoped change with a normal commit;
retain decision/evidence history and failed inputs. Reopened scientific defects
stop affected runs and analyses until results can be trusted.
