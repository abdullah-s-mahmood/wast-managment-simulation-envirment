# Agent Handoff — Authoritative Resume Point

## Current checkpoint (2026-10-22)
- S001–S004 completed, 4/88; S005 in_review on sprint/S005-conventions.
- S004 PR #6 passed exact-head CI run 39710355019 and merged 707e7a3.
  Acceptance PR #7 head 0012c1587ee3690e9d4259ecde44ae0a597a128b passed run
  39710464037 and merged 3799b5cdf9a2e5355885d93a86c492490cb1aced.
- S005 glossary/unit catalog/time/coordinates/ID policy and read-only reference
  checker implemented. Six focused tests pass; malformed timezone +01:99 exposed
  a Python normalization issue, now rejected with regression. See S005 report.
- Next: full regression, exact-head CI, self-audit, normal merge and acceptance
  records; S006 only after S005 completion. No second human needed (ADR-0005).
- Sources/sections and limits in docs/conventions/README.md. No physical models,
  runtime schemas, geodesy transforms or Windows/simulator validity claimed.
- Connector works despite invalid local gh credential. Local checkpoints and
  named original S003-drafts stash preserved; do not reset/discard them.
