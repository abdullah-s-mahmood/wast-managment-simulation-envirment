# S011 — Legacy execution path and data flow (COMPLETED)

Current checkpoint: E-S011-08 accepted after exact-head CI and permitted integration.
Earlier dated sections below retain their historical status and failures.

Date 2026-10-24, Asia/Baghdad. Branch sprint/S011-readonly-flow.
Base cd8c4445024efff28ef2be79faf1de624cccdf58; E-S011-01, B-S011-01.
S010 acceptance PR #22 head 2a1c2fdf8558bed0c8f2457fb95504e74bfe8b2a passed
CI run 40105633489 and merged before S011 entered in_progress.

## Authorized static work completed
Read full S011 contract, existing source graph, inventory and authorization.
Located three shallow native entrypoint candidates using recorded source-role
hints and source syntax, then read only those regular payload streams. Verified
each payload SHA-256 against S009; no link target, extraction, source execution,
reconstruction or redistribution. Private source anchors retained under Git common
metadata private-evidence/S011/static-flow-candidates.json. Raw artifact SHA-256
0e9e1e28ab6b3987e001983de37a9a8f26b41a97116d61924db9eec364a2e8be.

| Candidate | Source SHA-256 | Main source line | Static lead |
|---|---|---|---|
| entry-00010836 | 103b125ba273f52c832c252dfdb78acbb7cdd2f62ac157f15c2048a179cb5ca7 | 124 | Argument, input, clock/seed, state/step, output and simulator lexical anchors available. |
| entry-00010852 | 96cc75a1132f41e31dd5dd37a88670e8e4ef84345d04b2d2f510db5d473baa2e | 64 | Argument/input/clock/output lexical anchors; no state/simulator behavior inferred. |
| entry-00010853 | 7046a6e1a1324c6e2ae83168eec0887393925c16259459d2666dbf49fb07f5b6 | 8 | Argument/input lexical anchors only. |

These are navigation leads, not a completed execution/dataflow map, selected
production executable or verified stage ordering. Keyword hits may be comments,
declarations or unrelated paths; do not infer behavior from them or filenames.
S010's static graph remains the source-backed map; real configuration/time-step/
seed/clock/serializer/output semantics still require detailed trace and validation.

## Unresolved mandatory gate and concrete recovery plan
S011 requires: “Run from a different working directory or omit an optional input
to expose hidden assumptions.” Actual legacy execution is expressly prohibited
by current owner scope, which authorizes read-only audit and quarantine-only
inventory. Executing our audit tool in another directory would not prove this
legacy runtime property. No such substitute is claimed; mandatory gate NOT RUN.
No legacy run command, exit code, artifact or seed was fabricated.

B-S011-01: the runtime verification requires execution outside existing authority.
Keep S011 blocked, S012 onward not_started. Further static trace work may be
prepared safely in the same sprint, but cannot close the runtime gate alone.
Before any future permission request/execution, finish the source-bound plan:
1. Resolve intended entrypoint/build target and exact argument contract from the
   private source anchors; record input bytes/units/paths, optional vs required
   flags, stages, seed/time semantics and expected output artifact contract.
2. Prepare a reviewable isolated execution plan, exact commands/input hashes and
   two disposable working directories plus one justified omitted-input case.
   No network, source reconstruction, extraction, code execution or writes to the
   archive/source/project are authorized by preparing this document.
3. Obtain specific additional authority for any actual source preparation and
   execution, or suitable provenance-verified external evidence meeting the gate.
   Do not silently substitute another working tree, archive or old campaign result.
4. Only within that authority run and preserve exit codes, stderr/stdout, seed and
   output integrity comparisons. Failures/not-run status remain visible. Rerun
   mandatory technical gates and exact-head CI before accepting S011.

The owner has not been asked for a routine continuation approval. This blocker
preserves a concrete authorization boundary rather than bypassing the contract.
No new ADR/architecture/scientific model or implementation is introduced here.

## Actual checks and limits
Source-anchor probe: exit 0; regular source hashes verified; CPU hard limit 120s,
address space 256 MiB, selected member read cap 1 MiB. Full current archive size/
SHA-256 verification: exit 0, matches 487062036 bytes and designated hash.
No source/archive bytes changed. Existing full inventory/replay evidence retained.

Local governance commands/results in E-S011-01. Existing regression is not an
S011 execution test. WB entrypoint/clock/seed/serializer/output semantic checks:
NOT COMPLETE. BB actual run/stage/artifact mapping and required runtime attack:
NOT RUN. Physical/empirical/Windows/simulator execution: NOT RUN. No failing or
missing gate relabeled passed. Current S011 deliverable remains incomplete.

Only report, inventory, progress, handoff, blockers, validation and risk-status
records change. No new behavior requiring speculative implementation/tests.
Next safe action is the static source-bound plan above; S012 is NOT eligible.

## E-S011-02 — Detailed static trace and concrete review packet (2026-10-25)
Continued authorized work while the runtime gate remains blocked. Fetch confirmed
origin/main at 401b9dd5f1f43de93f5ceb8a82fd0c5956e9a8a4; no competing sprint work.
Branch sprint/S011-source-bound-plan, isolated worktree; original tree preserved.

Read/hash-checked primary source entry-00010836 in memory and reviewed root build,
event writer, mobility, network, dynamics, provenance, security and IPC bodies.
No archive member was written to disk or executed; only audit metadata saved.
Public source-flow map now documents exact entry/hash/line ranges for CLI/input
validation, initialization, seed streams, clock order, callbacks/telemetry,
policy/collection, drain, metrics and failure artifacts. The actual build target
is sw_cosim (root build entry-00011035:46); other native mains are auxiliary tools.

Material observed findings (not accepted models or runtime results):
- Optional feeder/model and relative city/config/output paths lack uniform
  rebasing; feeder path opened directly, city-directory parameter unused there.
- Current network body is a local capacity queue with unused seed/run constructor
  arguments and zero modeled drop/outage returns; inspected root build has no
  explicit ns-3 link. Transitive/dynamic linkage remains unverified.
- Events refuses an existing output directory and checks stream errors; summary/
  failure writer expressions do not have the same post-write check. Exit code
  alone cannot prove complete artifacts. Incomplete routes may write summary/exit 3.
- Host timing diagnostics and simulated clocks are distinct. Seed identity does
  not establish full raw-output equality, cross-platform RNG validity or physics.

Prepared docs/audit/S011_EXECUTION_REVIEW_PLAN.json, SHA-256
6a3ee7bc8ae61c8d1060fd9a197e012d9e680f1387e2dd787988b267f2960a41.
It binds 32 native text/build entries, three immutable input references and five
planned validation/argument cases to accepted S009 evidence. execution_authorized
and working_copy_prepared are false; every case remains NOT_RUN. No full simulation,
training, ONNX inference, source extraction/preparation/build or archived binary
execution occurred. The future budget/isolation/permissions are proposals only.

Private source-boundary assertions, input-static-review checklist and candidate
metadata are retained under Git common metadata private-evidence/S011. Ten source
anchor boundary/token assertions passed after manually reading the referenced
bodies. An independently authored JSON checklist found required source-declared
keys/types/profile/basic bounds in the chosen archived inputs. This is not the
legacy validator, runtime execution or scientific validity. Config reference is
entry-00011013, city JSON entry-00000089, road-network entry-00000088, all hashes
in the review packet; no raw scenario values or private paths published.

Independent metadata-only linter validate_execution_review_plan.py checks fixed
argv/CWD scope, input/source identity, stale/quarantined references and false
preparation/execution/reuse/scientific claims. It has no build/process execution
API. A valid packet cannot authorize an action. Synthetic tests include case-order
properties, altered-CWD/argv consistency, arbitrary/full-simulation commands,
missing/unknown/malformed records, inventory/hash corruption and read-only CLI.
Running this linter from another CWD is explicitly NOT the legacy runtime attack.

Actual commands: python -m unittest discover -s tests -p test_execution_review_plan.py
-v initially exit 1 (test-first FileNotFoundError: linter not implemented); after
implementation exit 0, seven tests. No assertions weakened or legacy behavior
reimplemented. Real packet linter with --inventory <private accepted S009 manifest>
exit 0, reports VALID_STATIC_PLAN, execution_authorized=false/runtime_status=NOT_RUN.
Read-only payload/hash/metadata probes exit 0. Linux x86_64, Python 3.11.15.
python -m unittest discover -s tests -v exit 0: 79 tests, original 72 retained.
All five governance validators plus git diff --check exit 0, 179 inventory artifacts.

Files changed: this report, handoff, blockers, validation log, progress date,
repository inventory; new source-flow review document, JSON packet, linter and
seven-test module. No scientific/architecture decision or authority expansion.
Runtime/working-directory/optional-input legacy test, external simulator runs,
physical validation and Windows tests remain NOT RUN. S011 stays blocked;
S012+ untouched. Next dependent step is specific owner authority for the reviewable
private preparation/build/five-case exception, or suitable verified external
runtime evidence. CI/merge of these records cannot accept S011.

## E-S011-03 — Review-packet integration and pending authority (2026-10-25)
PR #24 exact head 0b8f37da14ac8bc8b390b4f4724b78ffdf9cce09 passed CI run
40217362016 (completed/success); permitted merge
709ceba97c6a2c34d4d8f31fed0467dc8f93c281. Local checkpoint 523e938 and
published tree both a2184aa687d23f1049e05ce8e414b296fccda28d, equality checked.
79 tests/five validators passed. This integrates static tracing/plan tooling only;
S011 remains blocked, S012+ untouched, 10/88 completed.

Owner was asked for the specific exception described in the review packet:
private disposable preparation of exactly 32 native/build source entries and
three input references outside the implementation repository, trusted-dependency
build of only sw_cosim, and five bounded validation/argument cases. No simulation
or redistribution. No answer/authorization received at this checkpoint; request
acceptance by the question UI is NOT an approval. Source preparation/build/legacy
execution remains prohibited. The published static packet stays historically
false/NOT_RUN even if a later separate execution authority is received.

Prospective host-tool presence checked read-only: cmake, c++, bwrap, unshare and
pkg-config are present. Versions, dependency provenance, actual sandbox behavior
and license permissions are NOT verified by presence. Nothing was installed,
prepared, built or executed from the archive. No unsandboxed fallback is allowed.

If authority is granted later, first record its precise scope, complete prerequisite
source/dependency/license/isolation checks, preserve the archive identity and
execute only approved cases with separate actual execution records. A static-plan
linter is not a permission source or runtime result. Any remaining mandatory gate
keeps S011 incomplete. Original worktree/.vscode and private historical evidence
remain untouched. This checkpoint needs its own exact-head CI for integration.

## E-S011-04 — Owner authority recorded; isolation preflight failed (2026-10-25)

Base origin/main cfcc1e0d8516ca9d1d0e8fd4d701cfbfe16dfd77; branch
sprint/S011-authorized-validation. Original worktree and untracked settings preserved.
Owner explicitly answered yes to the exact isolated private build/five-case plan.
ADR-0007 resolves B-S011-01. State transition: blocked -> in_progress on authority,
then in_progress -> blocked on B-S011-02. Completed count remains 10/88.

Archive full size/SHA-256 and plan SHA-256 reverified with Python hashlib (exit 0).
No source preparation, build, target execution or simulation occurred. All five
legacy cases remain NOT_RUN; source reuse prohibited, models unvalidated.

Trusted-host probes (no archived executable/code):
- `bwrap --version`: exit 0, 0.9.0.
- `bwrap --unshare-user --unshare-net --unshare-pid --unshare-ipc --unshare-uts --die-with-parent --new-session --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind /lib64 /lib64 --proc /proc --dev /dev --tmpfs /tmp --chdir /tmp -- /usr/bin/true`: exit 1, loopback `Failed RTM_NEWADDR: Operation not permitted`.
- Same probe with `--uid 0 --gid 0`: exit 1, same loopback failure.
- Same initial probe without `--unshare-net`: exit 1, `setting up uid map: Permission denied`.
- `unshare --user --map-root-user --net -- /usr/bin/true`: exit 1, `write failed /proc/self/uid_map: Operation not permitted`.
- `docker version --format '{{.Server.Version}}'`: exit 1, daemon socket absent.
- Python shutil.which for firejail/nsjail/podman/runsc: exit 0, all absent.
- Read-only kernel metadata: unprivileged_userns_clone=1, max_user_namespaces=25657,
  apparmor_restrict_unprivileged_userns=1; effective capabilities zero. These are
  observations, not definitive attribution of the denial. No policy changes made.
- Python header/library presence probe: exit 0; OpenSSL header, Catch2 CMake config
  and sumocpp library present; nlohmann/json.hpp and libsumo/Simulation.h absent at
  standard inspected paths. Presence does not verify versions/provenance/licenses.

Platform: Linux 7.0.0-38-generic x86_64, glibc 2.39; Python 3.11.15.
No alternative sandbox backend was found. The approved plan explicitly requires
isolation before any target run; no unsandboxed fallback was attempted. A compliant
execution host is required. Missing dependency provenance remains a prerequisite.
Changed scope: ADR, decision/blocker/handoff/report/validation records and inventory.
No runtime-test success or S011 acceptance is claimed. CI is pending this checkpoint.

Checkpoint verification: `python -m unittest discover -s tests -v` exit 0,
79 tests passed. `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`,
`python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, and
`python scripts/validate_risk_protocol.py` each exit 0; `git diff --check` exit 0.
No production/test code changed; runtime legacy tests remain NOT_RUN.
Full size/SHA-256 verification repeated after preflight, exit 0, unchanged.
Restricted diagnostic/regression records: private-evidence/S011/
authorized-preflight-20261025.md and authorized-preflight-regression-20261025.log.
PROGRESS.json remains accurate: S011 blocked, 10 completed; no completion change.

## E-S011-05 — Authorization/preflight checkpoint integrated
PR #26 head a049f049359dd13739bc415469590a2e1ec400a7 passed exact-head
GitHub Actions run 40219535165 (completed/success). Permitted merge
8b9e1176d2fff33c16cb7962f3ffb44ed58b3810. Local checkpoint bfd5fad and
published tree both 1c40c09e115cb90fe7548d7cd45fcf00a018b67a, equality verified.
Self-audit accepted recovery documentation only, not S011. Owner authority under
ADR-0007 persists. B-S011-02 remains open; all five legacy cases NOT_RUN.
Next executable sprint remains S011 on a compliant execution host; S012 untouched.

## E-S011-06 — Repeatable trusted namespace preflight (2026-10-25)

Base origin/main cc626b34bcc21dd03f39f9c7cfcfbe1ed09fb9d8, branch
sprint/S011-isolation-recheck. PR #27 previously passed exact-head CI run
40219621481 at 564884627219acbe4acd4ab60082e3763b9fbd32 and merged as this
base. Original worktree and settings preserved. S011 remains blocked, 10/88.

Gap: previous isolation failures were manual probes. Added independently authored
scripts/check_execution_isolation.py and ten tests, inventory registrations and
source-flow/handoff/report/validation documentation. The fixed trusted namespace
probe never accepts a legacy target or prepares/runs archive content. A successful
namespace probe cannot set readiness true. Raw diagnostics stay in a new private
mode-0600 report; existing reports/symlinks are refused. All other isolation,
dependency/license and target identity requirements remain unverified.

Commands and observed results:
- `git fetch origin`: exit 0, current main cc626b3; lowest incomplete sprint S011.
- Repeated E-S011-04 Bubblewrap command: exit 1, loopback namespace denial persists.
- `sudo -n -l`: exit 1, password required; no elevated action attempted.
- `flatpak --version`: exit 0, 1.14.6; `flatpak list --columns=application,runtime`:
  exit 0, no installed applications. Packaged flatpak-bwrap helpers absent at the
  two inspected standard paths. No alternative sandbox ready for this plan.
- `pkg-config --modversion nlohmann_json libsumo`: exit 1, packages not found in
  pkg-config search path; this does not prove absence at all possible locations.
- Initial private-parent permission assertion: FAILED before report generation;
  evidence directories were not owner-only. Verified directory ownership/no
  symlinks, set only private-evidence and S011 evidence directory modes to 0700,
  then reran successfully. No archive/source permissions or host policy changed.
- `python scripts/check_execution_isolation.py --report PRIVATE_NEW_REPORT`:
  exit 1, namespace_probe_status BLOCKED, failure_kind NONZERO_EXIT,
  ready_for_legacy_execution false, legacy_cases_status NOT_RUN. Raw error is
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Restricted artifact private-evidence/S011/namespace-preflight-recheck-20261025.json,
  SHA-256 0a32171d13d1e071f973bbf45f29f9c9b1fa405423b392c8d38e1bd9e06f515c.
- Full archive size and SHA-256 reverified by hashlib.file_digest after probe:
  exit 0, designated 487062036 bytes/SHA-256 unchanged.
- `python -m unittest discover -s tests -p test_execution_isolation_preflight.py -v`:
  exit 0, ten tests passed. White-box branch/no-fallback/readiness invariants;
  black-box CLI from another CWD and unsupported target rejection; adversarial
  missing/denied tool, simulated timeout/signals, invalid UTF-8/oversized diagnostic,
  private report overwrite/symlink attacks; seeded generated nonzero-exit cases.
  These are trusted helper tests, not the mandatory legacy runtime attack.

Linux 7.0.0-38-generic x86_64/glibc 2.39, Python 3.11.15, Bubblewrap 0.9.0.
No host security changes, source preparation/build/execution, simulation or reuse.
All five approved actual legacy cases remain NOT_RUN. Owner's ADR-0007 authority
persists. Resume only with demonstrated plan-compliant isolation and verified
trusted dependencies/provenance/licenses. S012 not eligible. CI pending checkpoint;
integration of preflight tooling is not acceptance of S011 or scientific validity.

Final local verification: `python -m unittest discover -s tests -v` exit 0,
89 tests passed, including all previous 79. All five commands
`python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`,
`python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`,
`python scripts/validate_risk_protocol.py` exit 0; `git diff --check` exit 0.
Restricted regression transcript: private-evidence/S011/namespace-preflight-regression-20261025.log.
Initial assertion failure summary retained as namespace-preflight-initial-permission-failure-20261025.txt.
The failing Python helper exited 1; its original combined shell returned 0 because
the subsequent regression command passed. No failed preflight was treated as ready.
PROGRESS.json remains unchanged and accurate: S011 blocked, S012 not_started.

Preflight implementation checkpoint: PR #28 head
cec2c03170463197c8a063159f50a651ee21c436 passed exact-head GitHub Actions run
40220194016 (completed/success). Local implementation checkpoint 7ebc395 and
published tree ff3deb2afddac9591cb99518f113acd49dab480b are identical.
Self-audit found no scope expansion or false execution/scientific claims; accepts
preflight tooling only. This evidence update requires its own exact-head CI before
merge. Integration status and final merge SHA are recorded by PR #28 on GitHub.
B-S011-02 remains OPEN; next required action is a namespace-enabled execution host
and the remaining ADR-0007 prerequisite checks. Do not repeat owner authorization.

## E-S011-07 — Isolated private build and actual validation (2026-10-25)

Base 7440183035c154f79a8a89556f2e1a46bf94876d, branch
sprint/S011-privileged-isolation. Original worktree/settings untouched. State:
blocked -> in_progress after B-S011-02 resolution -> in_review after technical
checks; completed count remains 10 pending exact-head CI/integration/acceptance.

Owner supplied administrator authentication for the disclosed sandbox blocker.
Only sudo/timeout/Bubblewrap setup is privileged; setpriv drops to the owner's
nonzero UID, clears groups/capabilities and sets no-new-privileges before any
compiler/legacy target. No password is saved; no host security settings, services,
sudoers or installed SUMO packages changed. ADR-0008 records this implementation.
Existing policy still blocks the old unprivileged helper; it is not the runner.

Trusted prerequisites:
- `apt-get download sumo=1.28.0-1 sumo-dev=1.28.0-1 nlohmann-json3-dev=3.11.3-1`:
  exit 0, package-index SHA-256 verified; `dpkg-deb --extract` each into a private
  dependency prefix: exit 0. No maintainer scripts or archived dependency binaries.
- Package digests: sumo 53f808c42bd001337de22914a6802117d9dccacda20c1be94ddda2ef919011af;
  sumo-dev 62615b2e9502ec14db5b7e1e7498c12fade4364510f535886d45bd941ae7e78b;
  JSON 85e4e95dc4bdc6034d593e1933ee88e085319fee36cae83c178e8ddc1a66e8fd.
  Configured sources: SUMO stable Launchpad PPA and Ubuntu noble archive; no
  unauthenticated override. Package copyright metadata retained privately (SUMO
  EPL-2.0; JSON MIT metadata). Existing Catch2 3.4.0/OpenSSL 3.0.13 system packages
  supply separate dependencies. Third-party/legacy provenance remains unapproved
  for redistribution/reuse; private owner-authorized audit is the only purpose.
- `python scripts/probe_private_sandbox.py PRIVATE_ROOT --label verified5`: exit 0.
  Trusted independent C fixture: security/memory probes exit 0; CPU probe exit 137,
  file-size probe 153, watchdog probe -9. Those signals are expected enforcement,
  not successful target executions. Evidence binds wrapper/fixture and raw hashes.
  Fork/vfork/clone/clone3, repeated execve, execveat, networking all denied; actual
  target UID nonzero, effective caps zero, no-new-privileges, mounts read-only.

Preparation/build:
- Bounded private copy helper under `prlimit --as=268435456 --cpu=120 --core=0`
  and `timeout --signal=KILL 120`: exit 0, exactly 32 approved native/build texts
  plus three approved JSON/XML inputs. Full archive hash before/after, gzip CRC,
  TAR membership, payload hashes and output paths verified; links never copied.
  Archive is unchanged. Private locator remains only in Git metadata.
- `python scripts/execute_private_validation.py build PRIVATE_ROOT`: configure
  command `cmake -S /source -B /build -DSW_BUILD_COSIM=ON` exit 0; build command
  `cmake --build /build --target sw_cosim --parallel 2` initially exit 2.
- Cause: BLAS/LAPACK links traverse /etc/alternatives; missing/unsearchable sandbox
  /etc caused linker dependency errors. First mount-only retry also exit 2;
  explicit sandbox /etc traversal permission correction resolved it. No source
  patch. `python scripts/execute_private_validation.py resume-build PRIVATE_ROOT`
  final retry exit 0 (make exit 0). Original logs/receipts preserved.
- All build attempts combined: 13.137115927 seconds, below cumulative 300-second
  wall/CPU budget; one CPU affinity, per-process 1-GiB address space. Binary SHA-256
  939c2bd50379e557936f0adb944dfe1e38fbad9428be8c738b6493b198097fd3.

Runtime results (exact commands after binary; all under guarded_target):

| Case | CWD | Arguments | Actual exit | Result |
|---|---|---|---|---|
| ABS_A | /A | --validate-config /inputs/config.json /A/city_fixture | 0 | PASS |
| ABS_B | /B | --validate-config /inputs/config.json /A/city_fixture | 0 | PASS |
| REL_A | /A | --validate-config /inputs/config.json city_fixture | 0 | PASS |
| REL_B | /B | --validate-config /inputs/config.json city_fixture | 1 | expected missing-city error |
| MISSING_CITY | /A | --validate-config /inputs/config.json | 2 | expected usage error |

`python scripts/execute_private_validation.py cases PRIVATE_ROOT --attempt serialdeps`:
exit 0. Exact five case IDs, one corrected bounded batch, not new test scope.
Each case used 10-second root watchdog, 5-second CPU, 256-MiB address space,
1-MiB captured-stream file limit; /tmp and /dev/shm each bounded 16 MiB. Raw stderr
includes tracer lines and is preserved as stderr-with-trace, not misrepresented
as target-only stderr. No host-writable target mounts. Hash checks after every
case found all 35 copied input/source files and binary unchanged.

Three successful stdout bytes are identical, SHA-256
5ff2ec170631e7e921f468e13e0101bc55f2047ebd3fd05d3703c5318a177c32.
Parsed status/policy/seed/map-default/bin-count/profile fields match private input
and source-bound predictions. This tests input-to-validation-artifact flow and
actual CWD attack; it does not test ordinary simulation dynamics or clock coupling.

Failures retained (never counted as passing): initial ABS_A exited 130 because
OpenBLAS initialization attempted denied clone3 and raised SIGINT. Set only trusted
dependency environment OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1, retained all
denials, reran probes and the same five cases under authorized failure recovery.
Five distinct case IDs, six total legacy invocations including the failed attempt;
max_cases=5 per batch and every per-attempt cap unchanged. No unbounded retries.
Earlier trusted probe found occurrence-delayed exec injection permitted an extra
exec; removing the delay fixed it before any legacy target. Another probe exposed
non-writable /tmp and an expected watchdog -9 misclassified by the probe checker;
fixed namespace tmpfs permissions/explicit signal expectations, kept failed logs.
All these are engineering findings, not scientific evidence.

Evidence: public docs/audit/S011_VALIDATION_EXECUTION_SUMMARY.json contains only
sanitized counts/status/hashes. Private Git common metadata private-evidence/S011/
runtime20261025 holds original build/probe/case logs and receipts; runtime summary,
copy/dependency bootstraps and regression transcript also retained privately.
Private worktree locator codex-s011-execution.json is never committed. Hashes of
principal receipts are in the public summary; canonical hashes prove consistency,
not authorship, security clearance, licensing or model accuracy.

Verification: `python -m unittest discover -s tests -v` exit 0, 105 tests passed
(all prior 89 plus 16 new synthetic white-box/black-box/adversarial/generated/
regression tests). Tests cover links/traversal/case-collision, CRC/hash corruption,
staging/decompression limits, immutable sources, private capture, stale enforcement
receipts and cumulative retry accounting. Actual trusted probes independently
exercise namespace/runtime boundaries. Full archive size 487062036 and SHA-256
reverified after execution (exit 0), unchanged. No archived binaries/scripts,
normal simulation, ONNX/training or historical campaign replay executed.

Platform Linux 7.0.0-38-generic x86_64 GNU/Linux, Python 3.11.15 (CMake finds system
Python 3.12.3), GCC 13.3.0, CMake 3.28.3, Bubblewrap 0.9.0, strace 6.8, setpriv
util-linux 2.39.3. Scope is tested Linux x86_64 only; Windows runtime NOT RUN and
not advertised as validated by this audit. Scientific models remain UNVALIDATED;
source reuse/redistribution PROHIBITED. Full-run seed replay/empirical validity,
comprehensive malformed-input coverage and simulation metrics remain untested.
Next sprint S012 is ineligible until S011 permitted acceptance/integration.

Final governance verification: `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`, `python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, `python scripts/validate_risk_protocol.py`
all exit 0; `git diff --check` exit 0. Self-audit checked changed-file scope,
no source/binary/private paths/credentials, parameter separation and no scientific
clearance claims. All mandatory S011 gates pass locally; CI/integration pending.

## E-S011-08 — Sole-maintainer acceptance after CI/integration (2026-10-25)
PR #29 exact head 6b198976a62be198ad6265012024c98cc0ed94e6 passed GitHub
Actions run 40224316143 (completed/success), including 105 tests and mandatory
repository checks. Permitted merge 4339fae73884632126303e1a520fc27847f87182.
Local checkpoint 5b0bc99eb3db6c798194894fafb20e342d9e2edf and published tree
695345cbb28ec2a06c167cbd6366f8ac1cb65a59 verified equal before merge.
Author self-audit under ADR-0005 accepts S011's source execution/data-flow map and
bounded actual validation contracts. No independent-person review is claimed.

Acceptance: source/hash/line-bound entry/input/state/clock/RNG/serializer/writer
map reviewed; actual deterministic fixture output matches source/input predictions;
ABS_A/B exercises different CWD with invariant absolute inputs, REL_B exposes
relative-path failure; usage error observable. Synthetic negative/property and
actual security/resource tests pass. Original failures and residual risks remain
in E-S011-07. Full archive and 35 copied files/binary unchanged. No source reuse,
redistribution, normal simulation or physical/scientific validation accepted.
All applicable S011 gates satisfied; in_review -> completed; 11/88 completed.
Next eligible sprint S012 (not_started); fetch and read its complete contract.
This acceptance-record commit still needs its own exact-head CI before integration.
