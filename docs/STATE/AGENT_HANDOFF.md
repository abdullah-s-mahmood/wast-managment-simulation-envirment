# Agent Handoff — S012 explicit failed-reproduction report in review

Current 2026-10-26: S001–S011 completed (11/88); S012 in_review, S013+ not_started.
Branch sprint/S012-authorized-baseline, base 4865de107d4e4be3b77e2e07240b2769de8e18f0.
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
baseline reproduction record. Self-audit/CI/integration still required before
accepting that report/sprint. Do NOT call the failed baseline successful, loosen
raw-event comparison or mark scientific models validated. Then select S013 only
after acceptance, read full contract and preserve these negative findings.

Private root locator codex-s011-execution.json in Git common metadata only. Durable
raw evidence under private-evidence/S012/runtime20261026; comparison/dependency
manifests alongside. Existing S011 evidence intact. No legacy source/binary/raw
campaign outputs/private paths enter public repo. Current run plan authorizes only
these two normal cases and bounded correction, not archived test/script execution.
No further normal runs needed: retain actual outcomes, complete report gates next.
