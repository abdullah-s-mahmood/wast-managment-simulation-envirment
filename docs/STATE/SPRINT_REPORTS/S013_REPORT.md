# S013 — Legacy tests and results inventory (COMPLETED)

Current acceptance: E-S013-02; older sections retain historical state.

## E-S013-01 — Static inventory, provenance and trust labels (2026-10-26)

Base 06bd1b37cd79acb0140979e01f99291fbccd08d5; branch
sprint/S013-test-result-inventory. S012 acceptance PR #33 exact head
5fa6035eb48fee3081e8786f1086712ab5ffdf2b passed CI run 40370154763
(completed/success), merged as this base. Local acceptance tree
ef70c0707bb6d710f2e568f27f86b0b3529449d6 matched remote. S012 accepted only its
failed-reproduction report; normal baseline remains FAILED (F-S012-01). S013
not_started -> in_progress on audit -> in_review after local gates; 12/88 completed.
Original worktree/.vscode unchanged; no competing remote S013 progress found.

Gap/plan: S009 role hints and S010 syntax graph did not distinguish assertion
intent/process-only checks or give every historical result a reproduction trust
label. Read static source as data, catalog fixtures/metrics/provenance, never run
archived tests/scripts, and refuse scientific validation based on old reports.

Files changed: independently authored scripts/inventory_test_evidence.py and
synthetic tests/test_test_evidence_inventory.py; public sanitized JSON/protocol;
this report, progress/handoff/blocker/validation log and repository inventory.
No legacy source, historical result values, private paths, binaries or credentials
published. No new simulation implementation or scientific equation accepted.

Observed artifact:
- Full designated archive identity matches accepted S009 inventory, every logical
  member ID/path/size agrees, selected payload SHA-256 verified. Full before/after
  hash/stat, bounded gzip/TAR termination/CRC and limits succeed. Nothing extracted,
  reconstructed, imported, evaluated or executed from the archive. Links/special
  members never passed to payload access; nested archives remain unopened.
- 9,035 candidate records. 83 active-scope source payloads hash-verified/read,
  including CMake and ten shell scripts (shell semantics unresolved). “Active” and
  “retired” are path scopes, not authorship or scientific relevance decisions.
- 18 active test-path files; four retired-context test-path files. Active files:
  17 with behavioral assertion syntax, one with no observed assertion syntax;
  299 assertion-bearing line candidates and 20 common fixture-string lines.
  These are NOT numbers of passing/effective tests, resolved fixtures or coverage.
- Root CMake entry-00011035 declares add_test at lines 19,24,35,45,53. Conditional
  resolution, compilation and execution unverified here. Every test runtime status
  NOT_RUN; source syntax cannot establish actual check outcomes/physical validity.
- Every historical result candidate labelled: 2,369 unverifiable; zero reproduced,
  zero syntactically complete self-reported provenance records promoted to even
  unreproduced. 34 active-context texts inspected; 2,335 retired-context artifacts
  remain explicitly metadata-only. Do NOT claim all historical provenance absent
  or every payload read. S009 full index remains available for future focused review.
  No currently approved PLC source set changed or retired evidence discarded.
- Metric JSON keys/CSV headers stay private, units UNVERIFIED. Raw numeric metrics,
  test descriptions, campaign data and screenshot content are not copied publicly.
  Source reuse PROHIBITED; scientific validation UNVALIDATED for every record.

Scope refinement/errors preserved: v1's broad project-source scope consumed its
8MiB source budget on 2,872 retired-context source files before later active code;
content skips remained explicit. v2 separated retired context and prioritized
current source without raising budgets. v3 added shell-source inventory with
unresolved semantics; v4 repeated it byte-identically. v5 added strict schema/member
and compressed/member/count guards and still matches v3/v4 byte-for-byte. All
intermediate manifests retained privately, not deleted or relabelled full coverage.
CMake strings/comments are not counted as add_test declarations. Unknown dynamic
paths/aliases/conditional macros or outputs outside defined candidates are stated
limitations, not inferred as absent or passing.

Commands/results:
- `python -m unittest discover -s tests -p test_test_evidence_inventory.py -v`:
  earlier 11 tests exit 0; final added public-CLI fixture included in full 140 suite.
  White-box execution-only vs behavioral/trivial assertion syntax; native comment/
  string masking; CMake declarative vs execution; shell/retired scope separation;
  malformed schema and explicit compressed/member/count limits. Test source with
  a write side effect is never imported/executed and leaves its marker absent.
- Required adversarial attack: stale screenshot/old JSON claiming status passed,
  reproduced=true or scientifically VALIDATED remains unverifiable/UNVALIDATED.
  Even complete self-reported source/config/dependency hashes/seed/command remains
  unreproduced, never fresh reproduction/scientific validation. Corrupt/duplicate/
  nonfinite claims fail closed. Generated field/order/syntax cases preserve trust.
- Black-box: `python scripts/inventory_test_evidence.py SYNTHETIC_ARCHIVE INTAKE
  --project-root p` from another CWD: exit 0, all result labels present, source
  side-effect marker absent; CLI help also exit 0 without reading legacy inputs.
- Actual private CLI (v1–v5): `timeout --signal=KILL 120 python
  scripts/inventory_test_evidence.py PRIVATE_ARCHIVE PRIVATE_INTAKE
  --project-root PRIVATE_PREFIX`, each exit 0. CLI hard AS256MiB/CPU120s; wall120s,
  full intake compressed/expanded/member/metadata/count limits; per text 1MiB,
  source total8MiB/result total16MiB. Final selected source615078/result375040 bytes.
- Final v3/v4/v5 canonical SHA-256
  4339e6a6bd5a1a614d3f7cc5b88fc8ba4de9dd7eb26408c51bb92d348b29e987;
  raw JSON fdfcda01e86815299da2671827c31c38470214b4a1193b1afd36a14fd20af275,
  byte equality observed. Hashes prove consistency/identity, not authentic run
  provenance or scientific validation. No historical comparison was executed.
- `python -m unittest discover -s tests -v`: exit 0, 140 tests passed (all prior
  128 plus 12 new source/trust/CLI/adversarial cases). Linux 7.0.0-38-generic x86_64,
  Python3.11.15. Windows actual audit NOT_RUN/not advertised as verified.

Private manifests/stderr/transcripts: Git common metadata private-evidence/S013/
test-result-inventory-v1.json through v5.json and regression-final.log. Public
S013_TEST_RESULT_SUMMARY.json contains counts/entry IDs/digests only; protocol
records definitions, resource policy and content-coverage limitations.
No legacy tests executed (not authorized under baseline exception and not required
for static inventory); no historical result independently reproduced. F-S012-01
negative baseline remains; no scientific/empirical model acceptance. Self-audit
accepts only bounded inventory/trust-label evidence after remaining CI/integration.
Next S014 is ineligible until S013 accepted; read full contract/fetch before starting.

Final refinement: mixed assertions combining a process return-code check and a
payload condition are retained as behavioral assertion candidates as well as
status-check syntax. Regression covers this case. Hardened final v6/v7 scans both
exit 0 and match each other and v3–v5 byte-for-byte; original records preserved.
No extra legacy test execution or scientific trust was introduced. Final source
and assertion counts/digests unchanged. Private final invocation receipt retains
exact argv/limits and designated identity without publishing archive paths.

Final local gates: all 140 tests pass after final mixed-assertion/schema/resource
checks. `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`, `python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, `python scripts/validate_risk_protocol.py`
all exit 0; `git diff --check` exit 0. Scope/privacy/units/false-trust self-audit
found no published legacy source/raw outputs/credentials/private paths or claims
of scientific validity. Exact-head CI/permitted integration still pending.

## E-S013-02 — Sole-maintainer inventory acceptance (2026-10-26)
PR #34 exact head c3bd2ebb69629b48a1daa2de38e0fe5739eb72dd passed CI run
40379607640 (completed/success; 140 tests/mandatory checks), permitted merge
f6c124ab6503ddda3a2975d51fc4cf07820bb2cc. Local checkpoint
5206372ea2af1703c05b0e39b9a69937944ed486 and published tree
d6016c710bd617a62f6b01cc8e38ba1dc3a29967 verified equal before integration.
Owner-authorized self-audit under ADR-0005 accepts bounded candidate inventory,
assertion/execution-status distinctions and explicit historical trust labels.
No legacy test pass, historical reproduction, provenance authentication, empirical
validation or source reuse is accepted. No independent reviewer claimed. All
unknown/retired/dynamic coverage limits and F-S012-01 remain carried forward.
S013 in_review -> completed, 13/88 audit deliverables; next S014 not_started.
Acceptance record needs its own exact-head CI/integration. Fetch/read full S014
before starting; no arbitrary legacy execution is authorized by this acceptance.
