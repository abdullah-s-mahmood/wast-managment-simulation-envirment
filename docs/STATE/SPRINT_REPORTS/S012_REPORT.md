# S012 — Legacy baseline reproduction (BLOCKED)

## E-S012-01 — Concrete scope review and fail-closed evidence checker (2026-10-25)

Base 7bfa6c45afe1058bf6c2e99156f88f73ac7c7e30; branch
sprint/S012-baseline-review. S011 acceptance PR #30 exact head
979fb80ddc14227e4b3d15ab3831ff62f3199de1 passed CI run 40224443484
(completed/success), merged as this base; tree f4fdb54bcd39aeae53314450ec948d9e6b7cda32
matches local checkpoint 8cedd4b. S001–S011 completed, 11/88. S012 transitions
not_started -> in_progress on contract review -> blocked on B-S012-01.
Original worktree/settings/historical progress preserved; S013+ untouched.

Exact gap: full S012 contract requires actual baseline reproduction or a genuine
failed-reproduction attempt and a second operator's copyable evidence. S011 only
executed configuration/argument validation. ADR-0007 explicitly excludes normal
simulation; administrator authentication does not expand that scope. No normal
baseline was attempted and NOT_RUN cannot be called failed reproduction.

Changed files: proposed ADR-0009; audit review Markdown/JSON; independently written
scripts/validate_baseline_result.py and tests/test_baseline_result.py; this report,
progress/handoff/blockers/validation log and repository inventory. No legacy source,
archived results/private paths/credentials/binaries are published. No simulator or
scientific model implemented. Current runtime evidence remains S011 only.

The plan binds the unchanged S011 binary/source/input identities and proposes two
same-seed normal runs with isolated fresh output tmpfs at one namespace path,
120-second wall/60-second target CPU/1-GiB address-space caps per attempt, 64-MiB
output/count/file limits and at most one preserved corrective retry per run.
No launch authority or baseline-ready sandbox/exporter is claimed. Existing
validation-only runner is not an authorized normal-run fallback. Read plan and
ADR-0009 for full prerequisites/exclusions before any execution.
Plan SHA-256 5a8ef0be672f616bd9c40e68db4ea431e82dbb54c7dcea3ac31dd18bfb893187.
Observed scenario shape is 12 bins/two trucks, 600 simulated seconds/0.1-second
step. These are owner archived scenario settings, not calibrated physical facts.
Current-code audit would use trusted private SUMO 1.28.0-1, not recreate unknown
historical campaign environments. No historical output or measurement invented.

White-box/source reference: entry-00010836:181,870 binds run ID to output basename;
27–28,197,950 binds simulation_runtime_seconds to a steady-clock microsecond helper
scaled by 1e6. A preregistered comparison excludes ONLY that host-duration summary
field; raw bytes/hashes/differences remain retained. All other summary fields and
all raw event bytes compare without removals/tolerances. Event header source has
run_id, seed, kind, time_s keys. These are source observations, not actual normal
runtime proof or physical-model acceptance.

Tests/commands:
- `git fetch origin`: exit 0, verified accepted S011 and no competing S012 work.
- `python -m unittest discover -s tests -p test_baseline_result.py -v`: exit 0,
  eleven synthetic tests pass. Negative cases: missing dependency, no attempt,
  nonzero/signal/timeout exit, absent/empty/failure artifacts, links, wrong IDs,
  validation-only flag, duplicates/nonfinite/malformed JSON and resource budgets.
  Property/reference checks retain all raw bytes and distinguish only the stated
  host-runtime projection from an altered semantic field. Black-box CLI tested
  from another CWD; it never launches legacy code. These are NOT normal-run tests.
- `python -m unittest discover -s tests -v`: exit 0, 116 tests passed (all prior
  105 plus eleven new). Raw transcript private-evidence/S012/review-regression.log.
- Normal BASELINE_A/B, baseline sandbox/exporter adversarial probes and full-run
  determinism: NOT RUN. Required S012 gate remains open; no fake second operator
  or independent review and no scientific/physical validation claimed.

Environment: Linux 7.0.0-38-generic x86_64 GNU/Linux, Python 3.11.15. Windows
normal-baseline NOT RUN. Blocker B-S012-01 requires explicit owner authority for
proposed normal-run scope; then implement/verify all remaining technical gates,
retain actual outcomes, run checks/exact-head CI and integrate before acceptance.
Do not start S013. Original source archive remains unchanged; no new legacy target
execution/copy/source patch during S012 preparation. Self-audit accepts only the
review artifact/checker, not sprint completion. Publication CI pending checkpoint.

Final local governance checks: `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`, `python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, `python scripts/validate_risk_protocol.py`
all exit 0; `git diff --check` exit 0. Scope audit found only S012 preparation,
synthetic tests and governance records; no private material or claimed normal run.

## E-S012-02 — Review/checker CI provenance
PR #31 initial exact head 5879de1f9fc2d301da70a2701248bca7566a9865 passed
GitHub Actions run 40225369631 (completed/success), including 116 tests. Local
checkpoint 5be922133fb64bb3395c382a898d45d21954c215 and published tree
9688dd4915026d6f330a57a918710fee27af4f54 match. Owner scope question was
presented for the exact plan, but no owner answer at this checkpoint; a queued
question is not approval. ADR-0009 remains Proposed and all normal runs NOT_RUN.
This receipt needs its own exact-head CI before integration; final status/merge
SHA is recorded on PR #31. Integrating preparation does not accept S012.
