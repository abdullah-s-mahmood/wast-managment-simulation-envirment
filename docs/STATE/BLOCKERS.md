# Blockers and Open Dependencies

## Current blockers
- B-S012-01 OPEN — normal baseline simulation is outside ADR-0007's exact
  validation-only execution exception. Owner administrator authentication resolves
  sandbox setup, not simulation scope. Two bounded same-input runs and failure
  policy are concretely proposed in docs/audit/S012_BASELINE_REVIEW.md and JSON
  plan (SHA-256 5a8ef0be672f616bd9c40e68db4ea431e82dbb54c7dcea3ac31dd18bfb893187).
  Action: explicit owner scope authority for proposed ADR-0009. Before actual
  execution, also implement/test bounded output export and baseline-limit probes;
  plan approval alone is not readiness. No normal baseline attempted; NOT_RUN
  is neither failure evidence nor success. S012 blocked, S013 not_started.
- Local GitHub CLI credential is invalid; connector works, so publication is not blocked.

## Resolved blockers
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
