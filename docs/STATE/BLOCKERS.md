# Blockers and Open Dependencies

## Current blockers
- B-S009-01 — OPEN (S009). Located legacy candidates, but no owner-designated
  immutable baseline or verified handling/publication record. LEGACY-CANDIDATE-001
  is locally readable; SHA-256 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8
  matches sidecar. Bounded 1000-member metadata scan is incomplete, not intake acceptance.
  Source owner/license/secret/unknown-binary status unverified; do not guess, extract,
  execute, copy or publish source. Owner/action: designate intended revision/archive
  and handling restrictions; agent verifies provenance/license and bounded safe intake.
  Resume condition: designation/handling evidence recorded, then S009 blocked ->
  in_progress with resolving evidence. Exact commands and private locator mechanism
  in S009 report. Risk if guessed: wrong source, invalid provenance or unauthorized
  publication/reuse. No second-human review is requested; ADR-0005 remains in force.
- Local GitHub CLI credential is invalid; connector works, so publication is not blocked.

## Resolved blockers
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
