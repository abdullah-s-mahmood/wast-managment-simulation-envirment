# Agent Handoff — S012 failed-report audit accepted; S013 next

Current 2026-10-26: S001–S012 audit deliverables completed (12/88); S013+ not_started.
Branch sprint/S012-acceptance, base 2cdc1b8d4bf69d7197b59975cdee38a63be8f33a.
Original worktree/.vscode/history preserved. No competing remote progress found.

Owner explicitly authorized exact two-run plan with one corrective retry each;
ADR-0009 Accepted, B-S012-01 closed. Do not ask that authority again. Review JSON
is historical metadata and stays false/NOT_RUN; actual outcomes are separate.

Two actual unchanged normal invocations ran under verified private guards. Both
exit 3, route_complete=false. Their exports are intact but baseline checker rejects
both; NO successful baseline reproduced. 2261 event rows each, raw bytes differ
only at observed host timing fields. Summary differs only at preregistered excluded
host runtime and its projection matches. Normal source emits validation_only=true
literally, contradicting a prepared criterion. Neither criterion/test was weakened.
See E-S012-03, F-S012-01 and docs/audit/S012_BASELINE_OUTCOME.json.

128 unit/regression tests pass; seven actual trusted resource/export probes pass.
Initial quota-probe evidence bug and denied preflight preserved; no legacy launch
until corrected probes produced readiness proof. Exactly two normal executions,
zero retries; no source/input/binary changes or bigger budgets. Archive full hash
unchanged before/after; 129 loaded library hashes unchanged. No credentials stored
or host security policy changes; targets nonroot, no caps/network/fork/exec.

S012 contract permits an explicit failed-reproduction report as alternative to a
baseline reproduction record. Self-audit/CI/integration recorded in E-S012-04 accepts only
that failed-report deliverable. Do NOT call the failed baseline successful, loosen
raw-event comparison or mark scientific models validated. Then select S013 only
after acceptance, read full contract and preserve these negative findings.

Private root locator codex-s011-execution.json in Git common metadata only. Durable
raw evidence under private-evidence/S012/runtime20261026; comparison/dependency
manifests alongside. Existing S011 evidence intact. No legacy source/binary/raw
campaign outputs/private paths enter public repo. Current run plan authorizes only
these two normal cases and bounded correction, not archived test/script execution.
No further normal runs needed: retain actual outcomes, complete report gates next.

## E-S012-04 — Acceptance of failed-reproduction audit deliverable (2026-10-26)
PR #32 exact head cdafda62f5106a621fa958c7e02e094761b39c68 passed CI run
40369769249 (completed/success; 128 tests/mandatory checks) and permitted merge
2cdc1b8d4bf69d7197b59975cdee38a63be8f33a. Local checkpoint
c13533025b682f1248f1220e209f767a22852a19 and published tree
77efec03ae5dc9d28d526b54ceccb7b5772a43d8 matched before merge.

Owner-authorized self-audit under ADR-0005 accepts S012's explicitly allowed
“failed-reproduction report” alternative. All report-integrity/security/unit/
negative/reproducible-command evidence gates pass. Both normal attempts still
FAIL successful-baseline criteria: exit3/incomplete route/true validation marker/
raw event differences. No failed simulation is relabelled passing, criterion
weakened or physical model accepted. F-S012-01 stays a known negative finding for
later source/model/defect audits. A successful normal baseline remains absent.
S012 in_review -> completed as audit deliverable; 12/88 sprints completed.
Next S013 not_started; fetch/review its contract before proceeding. This acceptance
record needs its own exact-head CI before permitted integration.
