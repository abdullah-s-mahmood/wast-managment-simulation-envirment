# S012 — Legacy baseline reproduction (IN_REVIEW — FAILED REPRODUCTION)

Current evidence: E-S012-03; earlier checkpoints retain historical status.

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

## E-S012-03 — Authorized attempts; explicit failed-reproduction report (2026-10-26)

Base 4865de107d4e4be3b77e2e07240b2769de8e18f0, branch
sprint/S012-authorized-baseline. PR #31 final head
9cef239ed7c087d57551dcf02e1da8d3d7f2b454 passed exact-head CI run 40225464063,
then merged as this base. Owner explicitly answered yes to two bounded private
baseline runs/one corrective retry each; ADR-0009 Accepted, D-0013/B-S012-01
resolved. Approval persists; static review JSON remains historically false/NOT_RUN.
S012 blocked -> in_progress -> in_review; completed count stays 11 pending CI and
integration. Original worktree/settings and historical evidence remain preserved.

Deliverable selection: S012 explicitly permits a “Baseline reproduction record or
explicit failed-reproduction report.” This checkpoint supplies the latter. A normal
baseline has NOT passed. No route, determinism or scientific acceptance is claimed.
The original success criteria/checker remain unchanged despite failing outcomes.

Files changed: accepted ADR-0009; independently authored baseline_commands.py,
baseline_supervisor.py, baseline_transport.py, run_private_baseline.py; synthetic
C fixture and transport/runner tests; sanitized S012_BASELINE_OUTCOME.json; progress,
handoff/blockers/decision/report/validation/inventory records. No legacy source,
binary, raw events/metrics, private paths or credential is published.

Execution mechanism: unchanged S011 read-only input/source/binary and trusted
private dependencies. Privileged trusted timeout/Bubblewrap setup then nonroot UID,
zero capabilities, cleared groups/no-new-privileges. No host security policy or
service changes. Target cannot network/fork/exec/create threads, use ptrace,
unshare/setns/io_uring setup. Only /outputs (64MiB tmpfs), /tmp and /dev/shm (16MiB
each) are writable; no writable host target mounts. Target AS 1GiB, CPU 60s, file
16MiB. Supervisor child deadline 100s leaves export reserve under outer 120s wall
watchdog. One CPU affinity inherited. Address-space bounds are not aggregate
cgroup RSS guarantees. Export has 64-entry/64MiB data bounds; encoded packet cap
90,000,000 bytes accounts for base64 metadata overhead, never additional target
data. Private regular-file capture prevents unbounded parent pipe-memory growth.

Trusted exporter waits for target termination, rejects traversal/duplicates/case
collisions/links/special files/changed members/oversized data, checks hashes, and
exclusively publishes into a fresh owner-only evidence directory. Complete export
is separate from successful target exit/artifact validation. All raw failures stay.

Commands/results (PRIVATE_ROOT resolves only through Git common metadata locator):
- `python -m unittest discover -s tests -p 'test_baseline*.py' -v`: exit 0, 21 tests.
  New transport/runner tests plus existing eleven baseline-result negatives.
- `cc -O0 -Wall -Wextra -Werror ... tests/fixtures/baseline_fixture.c`: exit 0.
  Trusted fixture only; no legacy implementation copied into tests.
- `python scripts/run_private_baseline.py probes PRIVATE_ROOT`: initial exit 1;
  quota actually enforced but final marker could not be written into full tmpfs.
  A mistakenly zero-size last-file cleanup freed no space. Readiness packet absent.
  Initial BASELINE_A CLI preflight then failed before attempt marker/legacy launch;
  this is NOT a normal simulation attempt. Full original failed probe/code retained.
- Corrected fixture frees its known 8MiB quota0 file after ENOSPC before marking
  success, without weakening the quota or expected outcome. Rerun with new labels,
  preserving originals: seven probes pass. Fixture/security/memory/quota target
  exits 0; CPU/file signals -9/-25 and inner timeout -9 are expected enforcement,
  not successful baseline results. Corrected readiness packet binds all tool and
  fixture hashes. Actual namespace and raw-export round trip exercised.
- Preflight full archive size/SHA-256 verified before normal attempts (exit 0).
  S011 source/input/binary and trusted package digests checked before/after each.
  129 actually loaded shared-library hashes captured and unchanged after both.
- `python scripts/run_private_baseline.py run PRIVATE_ROOT --run-id BASELINE_A`:
  runner exit 1; actual normal target exit 3, termination exited; complete export;
  wall 0.465345662s. `... --run-id BASELINE_B`: runner exit 1, target exit 3,
  complete export, wall 0.365409602s. Exact argv for each:
  `/build/sw_cosim /inputs/config.json /A/city_fixture /outputs/baseline`, CWD /A.
  Separate fresh output tmpfs, same namespace basename/run ID and configured seed.
- Exactly two normal invocations, zero corrective retries. No input/source patch,
  changed horizon/fleet, rebuilt target, expanded resource limit or campaign replay.

Observed failed outcomes:
Both return route_complete=false and emit run_summary.json/events.jsonl. No
failure.json; this is source-declared noncompletion exit 3, not a hidden successful
run. The prepared validation_only=false criterion was an incorrect assumption:
normal source entry-00010836:952 emits true literally. Keep this conflict recorded;
actual normal CLI/loop execution is distinct from that summary label. Never change
the output/test merely to fit the assumption. Scientific models remain UNVALIDATED.

Each event file contains 2261 JSON rows. Raw bytes/hashes differ. Row-aligned JSON
diff found only /signing_wall_us (25 transmissions), /crypto_verification_wall_us
(25 receives), and /simulation_runtime_seconds (one summary event). Source anchors
entry-00010836:498,394,950 respectively identify host timing fields. Raw-event
replay criterion FAILED; no post-hoc event normalization was introduced. Summary
raw hashes differ only at simulation_runtime_seconds; the preregistered projection
matches (cc96a4022ec4214d594216f977210049e46fce0f74219b70f80f17bfdcb11606).
This explains bounded software differences, not physical accuracy or robustness.

Raw event hashes A de3031373087b688c6344d61aad1f3ee63da33eebb99275589a134222b3a52f4,
B a8eb0e2a232b099971f0de52466c5f57628c1068243deec5162d48edddcb12e3.
Full sanitized hashes/status/difference inventory: docs/audit/S012_BASELINE_OUTCOME.json.
Raw packets/streams/source fixtures/results are restricted under Git common
metadata private-evidence/S012/runtime20261026; root locator remains private.
Hash/diff/dependency manifests also private-evidence/S012. Never commit raw outputs.

Failure/report integrity: actual checker returns false for both nonzero targets,
so their complete exports are NOT accepted as successful simulations. Synthetic
negative tests also reject missing dependencies, absent outputs, nonattempts,
malformed/duplicate/nonfinite JSON, invalid identifiers, links and size budgets.
No fake second operator/reviewer; documented protocol lets a second operator attempt
independently if supplied the private designated inputs and same approved authority.

`python -m unittest discover -s tests -v`: exit 0, 128 tests passed (all prior 116
plus twelve new transport/runner/property tests). Actual trusted enforcement probes supplement
unit tests. Normal success/replay criteria failed as above; the failed-report
alternative remains subject to self-audit, exact-head CI and permitted integration.
Archive after normal runs: full 487062036-byte SHA-256 unchanged (exit 0); source,
inputs and binary unchanged. Existing package provenance/license constraints stay;
no source reuse or redistribution authorization. Linux x86_64 only; Windows actual
baseline NOT RUN. Python 3.11.15 supervisor system Python3.12.3; compiled S011 GCC
13.3.0/SUMO1.28.0-1/OpenSSL3.0.13; tool versions retained from S011 and private logs.

Known findings F-S012-01 must carry to later audit/model gates. S012 is not a
successful-model acceptance. Next S013 only after this sprint's report gates and
integration; do not run archived tests/scripts or historical campaigns under the
baseline-only exception. No new approval needed for already authorized work.

Final scope/self-audit: tests now include seeded arbitrary-byte transport/member
order invariance and parent-directory case collisions. All 128 tests pass; both
normal baseline attempts remain failed, not reclassified. Five governance commands
`python scripts/validate_project_docs.py`, `python scripts/validate_repository_boundary.py`,
`python scripts/validate_evidence_ledger.py`, `python scripts/validate_change_control.py`,
`python scripts/validate_risk_protocol.py` exit 0; `git diff --check` exit 0.
No source copy/patch, secret, private path, raw legacy output or false scientific
claim found in publication scope. Accept only the contract's failed-report
alternative after exact-head CI/permitted integration. Successful-baseline/model
acceptance remains absent. Final regression transcript retained separately.
