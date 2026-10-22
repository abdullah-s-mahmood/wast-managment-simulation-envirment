# S006 — Quality gates and definition of done

Date 2026-10-22 Asia/Baghdad; branch sprint/S006-quality-gates.
Base 583adb7d6583368585230672065b82730beccb7c; evidence E-S006-01.
Authority ADR-0005/AGENTS.md; exact-head CI/integration still required.

Gap: release gates were broad categories without criterion/command/assertion/
artifact mapping or an executable missing/failing evidence attack. Added
quality/DEFINITION_OF_DONE.md and gates.json, validate_quality_gates.py, five
tests, inventory/state/report/log updates. No simulation/science implementation.
The optional manifest checks completeness, never authenticity or authorization;
reports may retain the same criterion matrix without duplicating prior records.

Author self-audit: 13 criteria map to commands/procedures, assertions and retained
artifacts. Eight gates cannot be declared inapplicable. Other gates require
contract/scope evidence; unavailable mandatory dependencies cannot be waived.
Mandatory FAIL/NOT RUN, missing command, nonzero/bool exit, stale head,
missing/corrupt/escaping artifact, duplicate IDs and unknown versions reject.
Actual GitHub exact-head checks and permitted merge remain external mandatory
gates; synthetic metadata is labelled and never represented as executed commands.
No fake review, physical threshold, coverage target or scientific claim.

Linux x86_64/Python 3.11.15, standard library. Focused command:
python -m unittest discover -s tests -p test_quality_gates.py -v
initial exit 1 (test-first missing module); after implementation exit 0, 5 tests.
Final regression commands/results in E-S006-01. WB: state/version/status/exit and
artifact identity. BB: public CLI decision from synthetic records alone.
Adversarial: required failing/missing/unrecorded attacks plus corruption/stale
head/truncation/version/duplicate/applicability bypass. Metamorphic: check order
invariance. Independent reference: SHA-256 recomputed from retained fixture bytes.
NOT RUN: physical/empirical, Windows, simulators and runtime integration; no model,
runtime or advertised platform is introduced. Limits: checker cannot prove a run
occurred, a source is real, or N/A rationale is valid; author audit/API checks must.
Next eligible after accepted integration: S007.

## E-S006-02 — Accepted integration
- PR #10 exact head 98c77038423f834970f74dea8db2c0bab7e67e0d passed CI run
  39711264161, completed/success. Permitted merge 6119885cfa11b44acdf49e4cde5f1f30793f59ab.
- Published tree a365286d5b3bd211db33601850277951d65fc151 matches local checkpoint
  9b89e31 tree, preserved branch. 39 tests/three validators pass.
- Author self-audit under ADR-0005 accepted S006 (6/88); S007 next.
- No scientific/model/runtime validity claim; completeness checks do not authenticate evidence.
