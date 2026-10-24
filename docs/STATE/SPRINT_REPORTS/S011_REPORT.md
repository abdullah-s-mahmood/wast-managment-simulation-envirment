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
