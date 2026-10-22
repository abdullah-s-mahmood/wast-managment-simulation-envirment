# S004 — Hypotheses versus experiment settings

Date: 2026-10-22 (Asia/Baghdad); branch sprint/S004-classification.
Base e1c0f3dc7309950341df4001647ad37eebde8fce. Evidence E-S004-01;
ADR-0003/ADR-0005, D-0002. Local checks pending final recorded run; not accepted.

## Gap, scope and self-audit
ADR-0003 required separation but lacked a full classification table and observable
scenario-change attack. Added docs/HYPOTHESES_AND_SETTINGS.md with 14 classified
concepts and verification requirements, a read-only governance proposal checker,
synthetic model fixture, and five tests. Inventory/state/report/log updates only.
No runtime schema, simulation implementation or scientific relationship accepted.

The five case selectors are opaque synthetic labels. Exact-byte model hash is
checked against a separately supplied baseline, so case changes cannot override
hypotheses through this boundary. Experiment roles are explicit; raw measurement
and derived outcome IDs remain distinct. The checker does not classify natural
language, validate physical case values, authorize baseline changes or establish
causality. Future runtime schemas/design/empirical gates remain open.

Author self-audit: table maps every example to a classification, source/units or
future contract gate, and verification method. Existing ADR honored; mixed
statements must split rather than silently become models. Test changes of each
setting compare actual baseline bytes and hash, while attacks inject overrides
and corrupt model bytes/hash. No physical defaults, copied legacy or credentials.

## Actual commands and failures
Linux x86_64, Python 3.11.15, standard library only.
- python -m unittest discover -s tests -p test_study_separation.py -v:
  exit 1 before implementation (missing module, expected test-first red); exit 1
  after initial implementation (ModuleNotFoundError importing sibling validator
  through importlib); corrected package-aware/direct-CLI imports, exit 0, 5 tests.
  Reproducer remains the same command; CLI/import boundaries both exercised.
- Final regression commands/results: see E-S004-01.

WB: exact shape/version, roles, lists, baseline identity, errors.
BB: public CLI valid/invalid proposal; all five case selectors vary without edits.
Adversarial: missing/extra fields, bool/unknown versions, missing roles, duplicate
outcomes, invalid roles, observation/outcome collision, overrides, model/hash
corruption, malformed/truncated/duplicate-key/NaN JSON. Read-only failure leaves
input bytes unchanged. Metamorphic: setting field reorder preserves verdict.
Reference: independent SHA-256/byte comparison of explicitly synthetic fixture.
Windows/SUMO/ns-3/physical empirical tests NOT RUN and outside this governance
boundary. No advertised runtime support or scientific model introduced.
Next eligible after exact-head CI/merge/acceptance: S005.

## E-S004-02 — Accepted integration
- PR #6 exact head 62f6de561540d7ef07a3bfb2c9173775745f0b02 passed CI run
  39710355019 (completed/success). Normal merge permitted: 707e7a37cfd36752b382665c9926e4f095198454.
- Published tree 0ec78ca2c5b8abfc5b91f07815dc0e473ba0d52b equals local checkpoint
  b8d8f8f tree; preserved branch. 28 tests and all three validators passed.
- Author self-audit accepted under ADR-0005: S004 completed (4/88); S005 next.
- Scope remains governance-only; no scientific/causal or runtime validity claim.
