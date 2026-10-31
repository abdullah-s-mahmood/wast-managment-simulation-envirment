# S014 — Legacy model and parameter extraction (IN PROGRESS)

## E-S014-01 — recovered source-anchor candidate checkpoint, 2026-10-31

Base e8b356bae3bc6a6bf197bbd54c1644ddb25fd909, S013 accepted in PR #35.
Fetched origin and verified S001–S013 completed (13/88). Prior temporary S014
worktree absent; Git still retained its branch/worktree registration. No tracked
S014 edits recovered there. Created sprint/S014-audit-recovery from origin/main;
original resume/S009-blocked worktree and untracked .vscode/ preserved. No branch
reset, force push or history rewrite. Archive/private Git metadata accessible;
S011 disposable source/build tree no longer accessible. No reconstruction of it.

Gap/plan: generate reproducible exact source anchors and original identifier
spellings before semantic review; forbid invented constants, units or scientific
validation. A lexical candidate ledger alone cannot satisfy S014 acceptance.

Changed files: independent scripts/extract_model_ledger.py;
tests/test_model_ledger.py; optional trusted observer in
scripts/inventory_test_evidence.py; extraction protocol; repository inventory;
this report and progress/handoff/validation/blocker records. No legacy source,
raw campaign results, private paths or credentials copied into the repository.
No scientific equation or parameter accepted; global evidence ledger stays empty.

Actual commands/results (Linux 7.0.0-38-generic x86_64, Python 3.11.15):

- `python -m unittest discover -s tests -p test_model_ledger.py -v`: first exit1,
  eight tests with one failing boolean-coordinate attack. Python True compared
  equal to line1. Added strict integer-coordinate validation; same eight tests
  exit0. Original reproducer retained in test_anchor_and_identifier_tampering_rejected.
- WB: exact source/span hashes, original names, UTF-8 offsets/CRLF boundaries,
  tampered anchors/source/names rejected; distribution/time/protocol tags separate
  from physical validity. BB: public CLI from another CWD, unchanged archive,
  executable source text leaves side-effect marker absent; unsafe symlink skipped
  and legitimate later source inspected. Retired source not silently current.
- Required adversarial: unknown constant cannot become guessed normalization;
  scientifically-validating source comment cannot promote scientific support,
  resolve units or confirm intent. Generated 100 deterministic multi-line fixtures
  preserve byte/span hashes and replay (not empirical-distribution validation).
- `timeout --signal=KILL 120 python scripts/extract_model_ledger.py
  PRIVATE_ARCHIVE PRIVATE_INTAKE --project-root PRIVATE_PREFIX`: two actual runs,
  both exit0, full before/after archive verification and bounded traversal pass.
  Designated SHA-256 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8
  unchanged. Exact private invocation uses documented Git candidate locator and
  S009 quarantine-v2-run3 intake. No extraction, execution or nested archive access.
- Each output: 83 active-path source files, 597878 source bytes, 4024 candidate
  lines. This includes tests/tools, not 4024 accepted equations. S013's additional
  retired test-source content is excluded explicitly from the active ledger.
  Canonical manifest SHA-256
  47935d8ff9bddff843874bcef18fac7d71211d4cf599c99e5dca07b0077370f4;
  raw JSON SHA-256 b23751162ad9c78589f8d5e90b34923a76394cf579c9e59e8976c33b6913b70d.
  Two files byte-identical. traversal_complete=true, semantic_extraction_complete
  and review_complete=false; all science UNVALIDATED, reuse PROHIBITED.
- `python -m unittest discover -s tests -v`: exit0, 148 tests (140 prior +8 new).
  Full transcript private-evidence/S014/regression-148.log in Git common metadata.
- `python scripts/validate_project_docs.py`,
  `python scripts/validate_repository_boundary.py`,
  `python scripts/validate_evidence_ledger.py`,
  `python scripts/validate_change_control.py`,
  `python scripts/validate_risk_protocol.py`, `git diff --check`: exit0 before final
  state updates; rerun required afterward. Boundary initially212 approved artifacts.

Private outputs: Git common metadata private-evidence/S014/candidate-ledger-v1.json,
v2.json and corresponding stderr, owner0700 directory/0600 files. Previous S009–
S013 evidence retained. First failure evidence is the test/reproducer and diagnostic
above; no false pass recorded. No arbitrary legacy tests, simulator execution,
physical/reference calibration or Windows execution performed in this checkpoint.

Remaining gates: expression-level review and completeness, original units/names,
intended/source-supported distinctions and reference audit, reviewed ledger,
final verification, focused PR, exact-head CI, permitted integration/acceptance.
These are pending work, not external authorization blockers. S014 in_progress;
S015 not_started. Do not mark completed or skip ahead based on this candidate index.
