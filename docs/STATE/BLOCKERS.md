# Blockers and Open Dependencies

## Current blockers
- B-S001-01 — RESOLVED BY OWNER (2026-10-22): independent-person acceptance is no longer mandatory. Accepted ADR-0005 and AGENTS.md §4A permit a single-maintainer self-audit, exact-head CI and permitted merge. S001 now awaits the updated PR's required checks and integration only; S002 remains ineligible until S001 is marked completed.

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
