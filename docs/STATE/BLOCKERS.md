# Blockers and Open Dependencies

## Current blockers
- S015 discrepancy register locally reproduced; no external audit blocker.
  Exact-head CI/integration and acceptance records pending. Three observed issues
  remain open in S015_DISCREPANCY_REGISTER.json; audit acceptance will not fix them.
- S014 bounded source-extraction artifact accepted after exact-head CI/permitted
  integration (E-S014-04). No open S014 blocker. Scientific/reuse/dynamic limits
  remain explicit and do not constitute physical model acceptance.
- S013 bounded inventory accepted after CI/integration (E-S013-02); no open
  inventory blocker. Historical trust unknowns are retained explicitly
  (E-S013-01); they are not scientifically validated or silently reproduced.
- No unresolved scope/sandbox blocker for the two authorized S012 attempts.
  S012 failed-report deliverable accepted after exact-head CI/integration
  (E-S012-04). Neither attempt is a successful baseline. See F-S012-01.
- Local GitHub CLI credential is invalid; connector works, so publication is not blocked.

## Resolved blockers
- B-S012-01 CLOSED — owner explicitly answered yes to the exact two-run plan
  (120s wall/60 CPU seconds/1GiB address space/64MiB outputs per attempt, one
  corrective retry each). ADR-0009 accepted; technical gates remain mandatory.

- B-S011-02 CLOSED 2026-10-25 — owner enabled administrator authentication;
  privileged namespace setup plus setpriv drops to non-root UID/zero capabilities.
  Real trusted probes verify read-only mounts, denied networking/fork/exec and
  CPU/address-space/file/wall limits (verified5 receipt). No host security policy
  changes. Separately verified private trusted dependencies resolve missing headers.
  All five actual validation cases pass after retained dependency/concurrency fixes.
  E-S011-07 and ADR-0008 record exact scope, original failures and limitations.

- B-S011-01 CLOSED 2026-10-25 — owner explicitly answered yes to the scoped
  preparation/build/five-case question. ADR-0007 records the persistent exception;
  do not request the same authorization again. New technical blocker B-S011-02
  does not revoke that authority.

- B-S009-02 CLOSED by explicit owner quarantine-only policy amendment (ADR-0006),
  tested continuation and complete 11049-member private inventory. Unsafe entries
  remain quarantined; no archive safety, reuse, license or scientific approval.
  Earlier per-member/CPU exhaustion runs are retained in E-S009-04.

- B-S009-01 CLOSED: owner designation/read-only handling authorization plus exact
  size/SHA-256 verification resolve original selection ambiguity. B-S009-02 is new.
- B-S001-01 — CLOSED 2026-10-22. Sole owner waived independent-person review by accepted ADR-0005. Exact-head GitHub Actions passed for PR #1; PR #1 merged as `7aaa0b8ee76fb276506bbaf0a97b65101583901b`. S001 technical gate accepted. This does not waive later scientific/technical gates.

## Known baseline findings
- F-S012-01 — both unchanged normal runs exit 3 with route_complete=false;
  successful baseline NOT reproduced. Source emits validation_only=true literally
  even on normal path (entry-00010836:952), contradicting a prepared criterion.
  Raw event files differ only at observed host-time fields; raw replay criterion
  fails and is NOT weakened. Summaries match only under the already declared
  host-runtime exclusion. See E-S012-03 and sanitized outcome JSON. These are
  retained negative audit findings, not physical-model validation or a waiver of
  future scientific/model gates. Read-only audit must not patch the baseline.

## Future evidence gates
1. Legacy source bundle required for S009–S016; do not infer code behavior from chat summaries.
2. Bin/environment equations require evidence before S045–S054 lock models.
3. Vehicle/fuel parameters require source review before S055–S064 accept physical values.
4. PLC sources/parameters must be identified in the legacy audit; do not substitute silently.
5. SUMO/ns-3 versions and smoke tests must be recorded before integration claims.
6. Pollutant, odor, leachate, fill-rate, fuel, and communication claims need evidence/calibration or remain provisional/unavailable.
7. Statistical model choice requires outcomes, experimental unit, dependence, repetitions, pairing, and estimands.
8. Repository is public. Do not commit credentials, private datasets, or material not authorized for publication.

## Blocker format
Record ID, affected sprint, issue, evidence checked, exact missing evidence, risk if guessed, owner/action, and condition to resume. Close only with resolving evidence.
