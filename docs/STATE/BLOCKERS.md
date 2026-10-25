# Blockers and Open Dependencies

## Current blockers
- B-S011-02 OPEN — verified isolation unavailable for the approved S011 plan.
  Bubblewrap 0.9.0 network namespace setup fails with `Failed RTM_NEWADDR:
  Operation not permitted`; explicit UID/GID 0 gives the same failure. Without
  network isolation, UID-map setup also fails. `unshare --user --map-root-user
  --net -- /usr/bin/true` fails writing uid_map. Docker daemon socket is absent;
  firejail/nsjail/podman/runsc are unavailable. Only trusted `/usr/bin/true` was
  used in probes; no legacy copy/build/execution occurred. Host policy was not
  changed. Dependency headers are also not all present/verified (JSON and SUMO).
  Resume on a host with demonstrated plan-compliant isolation, then verify trusted
  dependency provenance/licenses and execute only ADR-0007's approved cases.
  Reproducible fixed trusted-tool check: scripts/check_execution_isolation.py;
  actual rerun remains BLOCKED (E-S011-06). A passing namespace probe alone
  cannot clear the remaining sandbox/dependency gates.
  No unsandboxed fallback. S011 incomplete; S012 remains not_started.
- Local GitHub CLI credential is invalid; connector works, so publication is not blocked.

## Resolved blockers
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
