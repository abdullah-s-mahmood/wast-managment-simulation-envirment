# S011 — Legacy execution path and data flow (BLOCKED)

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
