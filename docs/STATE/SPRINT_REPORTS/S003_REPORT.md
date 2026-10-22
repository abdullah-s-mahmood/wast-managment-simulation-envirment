# S003 — Scientific evidence ledger

Date: 2026-10-22, Asia/Baghdad. Branch: `sprint/S003-evidence-ledger`.
Base: `b591b2339f3e5b2b87bc26f01abd52312403ffde` (S002 recovery PR #3).
Decisions: ADR-0004, ADR-0005; evidence: E-S003-01.
Status: local gate passed; exact-head CI and permitted integration pending.

## Gap and implementation
Recovered untracked ledger drafts, preserved in named Git stash. No previous
scientific records or accepted models existed. Added a versioned custom JSON
record contract, empty production ledger, source-review checklist, fail-closed
validator, synthetic fixtures, unit tests and CI invocation. The inventory adds
only these governance/test artifacts and this report. State/log/handoff/blockers
are updated; no simulation implementation, external paper or physical parameter
is introduced. Contract is explicitly not JSON Schema.

Records require citation/DOI-or-reason/URL, version/location, source hash and
retained path, units/ranges, applicability, assumptions, uncertainty, calibration,
independent validation/sensitivity plans, implementation/config/test mapping,
and explicit verification and decision states. Accepted records require verified
review, eligible evidence class, matching source bytes and existing mapping.
Synthetic records are excluded from production. Review remains substantive:
structural validation cannot establish citation authenticity or domain validity.

## Actual validation and original failure
Linux x86_64, Python 3.11.15; standard library only.
- `python -m unittest discover -s tests -p test_evidence_ledger.py -v`: exit 1
  initially, 11 tests with one failing subcase. Reproducer:
  `test_mapping_path_and_pointer_attacks`, source_sha256 = 64 zeroes.
  Expected rejection; observed empty errors. Added retained-source hash check;
  did not weaken the test.
- `python -m unittest discover -s tests -v`: exit 0, 23 tests after fix.
- `python scripts/validate_evidence_ledger.py`: exit 0, 0 production records.
- `python scripts/validate_project_docs.py`: exit 0, 88 sprint contracts consistent.
- `git diff --check`: exit 0.
- Boundary validator run after inventory update; see E-S003-01 for outcome.

WB: required fields/types/enums/IDs/dates, units and variable uniqueness,
source hash, mapping paths/pointers and acceptance constraints. BB: public CLI
valid/invalid input and local synthetic source/config/reference tracing.
Adversarial: missing/empty/wrong fields, duplicate IDs/JSON keys, NaN/Infinity,
unsupported versions, invalid citation/DOI, missing units, unjustified domain
transfer, path traversal, broken mappings and corruption of source hash.
Metamorphic/reference: field-order invariance and synthetic identity value/unit
comparison; no physical reference result claimed. Interrupted/truncated JSON is
rejected without writes. Validator is read-only, so no partial output transaction.

## Self-audit and limits
Author self-audit under ADR-0005, not independent-person review: fields map to
S003 WB/BB/attack requirements, tests exercise fail-closed behavior, production
contains no synthetic citation, no hidden model defaults or copied legacy code.
Fixture hashes are computed from bytes in tests; Git commit provides fixture
provenance. Citation verification, licenses and dimensional/domain reasoning
still require source review; a verified flag alone cannot establish truth.
Windows, SUMO/ns-3 and scientific/empirical validation NOT RUN: no supported
runtime, adapter or physical model is implemented by S003. These are future gates.
Next sprint after acceptance: S004. Do not advance until exact-head CI and merge.
