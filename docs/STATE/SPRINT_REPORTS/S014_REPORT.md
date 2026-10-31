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

## E-S014-02 — reviewed source ranges, 2026-10-31 (not acceptance)

Previous checkpoint published as draft PR #36 head
8b00cbb6081e10ff273930c38d027ed33e83d75a. Exact-head run41148905449
completed/success. Local951c4202b1e4cf550ef21a65cdae3ab9580c899a and
published tree f6d7a0a1e74fa406c45185e74f2fd6a1b1485242 verified equal.
Git push exit128 (interactive credentials unavailable); GitHub connector
publication succeeded without bypassing protections. Moved the new audit worktree
out of temporary storage; locate with `git worktree list`. Original preserved.

Added independent scripts/review_model_spans.py, six synthetic tests in
tests/test_model_span_review.py, sanitized S014_REVIEW_PLAN.json and
S014_REVIEW_SUMMARY.json. Updated protocol, inventory and state records.
The plan binds E4 review observations to source hash/entry/line ranges; private
manifest resolves exact UTF-8 byte ranges/span hashes, identifier spellings and
numeric lexical spellings (including digit separators/scientific notation).
No expression evaluation, source reconstruction, legacy execution or normalization.
Intended behavior remains UNAVAILABLE; original units not inferred; science
UNVALIDATED and reuse PROHIBITED. Hash binding does not prove interpretation.

Actual review: 86 selected ranges across 22 active-path files: 18 equations,
20 defaults, 7 distributions, 13 time rules, 11 protocol ranges, 3 seed rules,
14 boundaries. Includes core dynamics/collection/encoding/masks, nominal feeder
capacity and packet outcomes, field-trial interpolation, mobility/routing/SLA,
reward/runtime orchestration, identity/admission, optional inference/training and
export formulas. Original sensor dynamics source labels itself provisional;
fuel implementation is a proxy; field-trial digitization and interpolation are
source observations, not new calibration/latency/uncertainty validation. Runtime
summary marker retains F-S012-01. No PLC source-set substitution.

Commands/results, same Linux/Python platform as E-S014-01:

- `python -m unittest discover -s tests -p test_model_span_review.py -v`:
  initial five tests exit0. Final sixth adds Unicode line boundaries, digit
  separators and malformed category/nonfinite-coordinate attacks; included in
  full154 suite. No new observed failing test in this phase.
- `python -m unittest discover -s tests -v`: exit 0, 154 tests (all prior148 plus6),
  final 154 run2.472 seconds. Transcript private-evidence/S014/regression-154.log.
  WB multiline byte/line source anchors, changed source/range/budget failures;
  BB CLI from other CWD, identical archive, no source-side-effect marker;
  duplicate/missing/unsupported/bool/nonfinite plans fail closed. Required
  intuitive-constant/comment-validation attacks cannot add guessed units,
  normalized expressions or scientific-support promotions. Exact known synthetic
  byte slices/hashlib checks provide reference/differential checks for extraction,
  not scientific equations. The prior100 generated fixtures remain passing.
- `timeout --signal=KILL 120 python scripts/review_model_spans.py PRIVATE_ARCHIVE
  PRIVATE_INTAKE docs/audit/S014_REVIEW_PLAN.json --project-root PRIVATE_PREFIX`:
  four actual runs exit0. v1/v2 select52 ranges and are byte-identical; after
  expanded review v3/v4 select86 ranges and are byte-identical. All retain full
  designated archive before/after identity/CRC/terminator/resource checks.
  Hard 256MiB address-space,120 CPU/120 wall seconds and inherited intake/text limits.
- Four additional bounded in-memory source-inspection passes exit0 and report
  TRAVERSAL_COMPLETE true; trusted observer prints selected source lines for local
  review only. No legacy files extracted or executed. No copied source in public
  plan/report. No simulation/training/replay performed.
- Final 86-range canonical digest
  540aff926902fc9e3632f90e9cbf7e60e1941f8aa3b11e564a899f21ff526a84;
  raw JSON SHA-256 026879ce319fca9fbe3aec1ec1d24ebbcfdb4ecda1b90651be02525e3d70cf73.
  v1/v2 canonical a277fbe44e604c8f2bddfba90fbe8b52316033358e72a5f8f6188ab771db5506
  retained privately, not overwritten or claimed to have expanded coverage.
- Required project-doc, boundary, evidence-ledger, change-control and risk validators
  and diff check pass with source/tests; final documentation rerun follows below.

Artifacts: Git common metadata private-evidence/S014/reviewed-ranges-v1.json
through v4.json with stderr, candidate-ledger-v1/v2, coverage-next.json and full
regression logs, owner0700 directory/0600 files. Public plan/sanitized summary
hold observations/anchors/counts only, no raw source/formulas/historical values.
No source reference promoted to physical evidence; primary-paper interpretation
is not accepted by these E4 source observations. Windows execution NOT RUN.

Remaining coverage:61 of83 candidate source files do not yet have selected review
ranges; these include18 test files and additional scenario/campaign/analysis/tools,
headers and build context. Do not call all61 unreviewed scientific models, but do
not assume those tools contain no defaults/assumptions either. Their classification
and relevant model extraction remain S014 work. Whole-project extraction remains
false. Current changes need exact-head CI; draft PR stays unmerged. S014 stays
in_progress; no S015 work and no external authorization blocker invented.
