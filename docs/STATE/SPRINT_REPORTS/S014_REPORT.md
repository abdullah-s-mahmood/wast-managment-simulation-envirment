# S014 — Legacy model and parameter extraction (COMPLETED)

Current acceptance: E-S014-04. Earlier checkpoint sections preserve historical state.

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

## E-S014-03 — bounded active-source extraction verified (2026-10-31)

Source checkpoint PR36 head8aa101033564007dc5221cc1376c09ebe9544077
passed exact-head CI41149768875. Local89d2a2aef24c89617366e2076f72d5607c98df68
and published tree2aa2d6f19c185808e5c13f4345fb1c95b0ccc096 verified equal.
Main remains e8b356bae3bc6a6bf197bbd54c1644ddb25fd909; fetched before continuing.
Original worktree/uncommitted .vscode preserved. No competing completion found.

Resolved gap: previously remaining61 file contexts now classified; added exact
scenario/geometry/sampling/statistical ranges, remaining native interfaces/tools,
build/default gates, all shell wrappers and embedded monitoring formulas. New
independent audit_auxiliary_models.py parses Python as AST data, retaining exact
expression source hashes/byte ranges, original names, E4/UNVALIDATED labels and
unresolved intention/units/calls. No import/eval/unparse/legacy execution. Captures
all calls as well as assignments/defaults/returns/guards, so configuration arguments
in unassigned calls are traceable. Added validate_model_coverage.py to reject
missing/duplicate/unbound sources, plan/hash disagreement and model-as-test hiding.

Scope/result:83 hash-verified active-path source files classified,18 test/probe
files retained as S013 evidence,28 non-test Python files parsed,7769 source syntax
expressions. All26 native source/interface files,10 shell files and one build file
have selected reviewed ranges. Final114 reviewed ranges across45 files (overlaps
with Python AST scope explicit). The ledger defines exact source anchors, original
spellings, defaults/time/seed/protocol and provisional assumptions without claiming
scientific equations are accepted. Dynamic calls/imports/external inputs/native
preprocessing/arbitrary shell semantics and retired context remain explicit limits;
whole-archive semantic analysis is false. No previously unclassified active file
is silently excluded or counted as an independently validated physical model.

Files added/changed: auxiliary audit + ten tests; coverage validator + four tests;
expanded review plan/summary and public auxiliary/coverage summaries; extraction
ledger/protocol; inventory, progress/handoff/blockers/report/validation records.
No source implementation, raw dataset/campaign output, private path or secret
published. Approved PLC source set unchanged; no scientific evidence promoted.

Actual evidence (same Linux7.0.0-38-generic x86_64/Python3.11.15):

- `python -m unittest discover -s tests -p test_auxiliary_model_audit.py -v`:
  exit0, final10 tests. Static defaults/multiline expressions/unassigned calls,
  UTF-8 AST byte columns with CRLF/CR and Unicode separators in strings; malformed
  syntax/hash and10001-expression budget reject; no side effects/imports executed.
  Public CLI from another CWD preserves archive bytes, skips unsafe link, emits
  no partial success on malformed source.100 generated expression fixtures replay,
  IDs unique and span hashes agree with direct independent byte slicing/hashlib.
- `python -m unittest discover -s tests -p test_model_coverage.py -v`: exit0,
  four tests. Complete fixture remains UNVALIDATED/prohibited reuse; missing,
  duplicate, hash/plan mismatch, scientific promotion and test-scope substitution
  rejected. These tests prove extraction/accounting properties, not physics.
- `python -m unittest discover -s tests -v`: final168 tests exit0 (all prior154
  plus14). Earlier163/167 runs also pass; private transcripts retained.
- Actual auxiliary CLI: `timeout --signal=KILL 120 python
  scripts/audit_auxiliary_models.py PRIVATE_ARCHIVE PRIVATE_INTAKE
  docs/audit/S014_REVIEW_PLAN.json --project-root PRIVATE_PREFIX`.
  Runs v1–v6 exit0. v1/v2 classify83 files/2841 expressions; v3/v4 bind expanded
  plan; v5/v6 add all calls, yield7769 expressions and are byte-identical.
  Final canonical346503350542089998e4fd6a5e2c82a6c0a78ee10e3e107fc3dcb32ad5ab7b34;
  rawd4edada659d20448c7e2456df5117907a1b2b2741dc46b9d5dcff19fee471de6.
- Actual reviewed-range CLI same as E-S014-02: v5/v6 exit0, final114 ranges,
  byte-identical. Canonical11df147fa11dc385ddc3e99bb42987ad6fdf5d9f3fef543187acb17ddf8ac25e;
  raw4072dc52c58f55128862e007dca40d2a874cfe49190024835f35ad5fac62223a.
- Three additional bounded source-inspection passes exit0/TRAVERSAL_COMPLETE;
  scenario/statistics, native wrappers/build, shell data reviewed only in memory.
- Every real scan retains256MiB AS/120CPU/120wall limits plus accepted full archive,
  member/metadata/count/text/cumulative decompression limits. Full designated
  487062036-byte archive SHA-256 unchanged before/after; CRC/termination checks
  pass. No unsafe link dereference, extraction, recursive archive opening or run.
- `python scripts/validate_model_coverage.py PRIVATE_CANDIDATE PRIVATE_AUXILIARY
  PRIVATE_REVIEWED docs/audit/S014_REVIEW_PLAN.json`: exit0, scope_coverage_complete
  true for explicitly bounded active-path source audit; whole_archive_semantic_analysis
  false, dynamic_call_resolution UNAVAILABLE. Public sanitized result retained.

Private Git metadata private-evidence/S014 holds all original manifests/stderr,
coverage-validation.json and regression transcripts, owner-only permissions. Exact
private locators remain there. Public ledger/plan/summary expose only sanitized
source observations, opaque IDs and hashes. No physical model implemented or
validated; primary-paper calibration/reference/empirical tests NOT RUN (no such
model accepted in this extraction sprint); Windows audit NOT RUN/not advertised.
S012 remains a failed-reproduction report; F-S012-01 and historical trust limits
persist. No new failure hidden; the original boolean-coordinate regression remains.

Local self-audit accepts the extraction artifact's declared scope/traceability,
not program-semantic completeness or physical validity. Required local validators
and final CI/integration remain acceptance gates. S014 -> in_review only after
local coverage/tests/docs pass; remains13/88 until permitted integration. S015
not_started. No independent reviewer claimed and no GitHub protection bypass.

## E-S014-04 — sole-maintainer extraction acceptance, 2026-10-31

PR36 final exact head f982766ffe254f04735ac499cbb8ddf77fba8db2 passed
CI41153333228 (completed/success;168 tests/required checks), permitted merge
1c95db52c589bdac1a4aa77e812465e7f54d2e2f. Local9b979f15b210f9f90820ceb7c03216211dce9bde
and published tree85d35bc3d765a556d36ada48db5d69eaac9c722b verified equal.
Changed-file scope reproducible with `git diff --name-only
 e8b356bae3bc6a6bf197bbd54c1644ddb25fd909 1c95db52c589bdac1a4aa77e812465e7f54d2e2f`:
21 files covering independent audit/validation utilities, synthetic tests, sanitized
ledger/plan/summaries, inventory and state records. No implementation reuse or
private source/raw campaign data published. Original worktree preserved.

Honest self-audit under ADR-0005 accepts the bounded active-path source extraction
ledger: exact provenance/original spellings, defaults/distributions/time/protocol
observations, explicit unknowns and cross-artifact coverage. All applicable WB/BB/
adversarial/property/regression/reference extraction checks pass. Original failure
and all intermediate manifests retained. No independent review fabricated. No
physical/calibration validation, source reuse, license clearance, source-comment
verification or exhaustive dynamic program semantics accepted. Scientific support
remains UNVALIDATED; unit/intention/retired/dynamic and F-S012-01 limitations remain.

S014 in_review -> completed,14/88 audit deliverables. S015 is next/not_started.
This acceptance record needs its own exact-head CI and permitted integration;
fetch/read S015 fully only after that durable state is integrated.
