# S008 — Risk register and escalation rules

Date 2026-10-22 Asia/Baghdad; branch sprint/S008-risks.
Base 5f6e0130afe6e241dba6730b13930ed7812cd68f; E-S008-01, ADR-0004/0005.

Gap: future evidence dependencies were listed without a complete risk/action/
resume record or executable no-guess/no-irreversible-bypass attack. Added eight
monitored risks in quality/risks.json, RISK_AND_ESCALATION.md, read-only
validate_risk_protocol.py, four tests and inventory/state/report/log updates.
Risk records map to existing authorities/affected sprints, impact, trigger,
mitigation, responsible action and exact unblock conditions. No invented risk
probabilities, physical constants or unsupported source claims.

Author self-audit: a resumed agent has an explicit next safe action. Corrupt
results stop dependent work; missing scientific evidence/guesses stop the gate;
missing required specific authority cannot be bypassed; test failures require
investigation/retest; routine actions continue autonomously. Precedence preserves
all coexisting blockers. Declarations are not evidence authentication or permission.
No second-human review or new external-message permission is introduced.

Linux x86_64/Python 3.11.15, standard library. Focused command:
python -m unittest discover -s tests -p test_risk_protocol.py -v
initial exit 1 missing module (test-first); after implementation exit 0, 4 tests.
Final regression results E-S008-01. WB: register fields/IDs/sprint ranges/status
and strict explicit fact types. BB: public CLI completeness and next_action code
from observed declarations. Adversarial: guessed value plus irreversible/authorized
flags cannot override missing evidence; missing/unknown/wrong-type facts, missing
risk fields, duplicate IDs and bool version reject. Property/reference: exhaustive
64 six-boolean combinations independently assert action precedence; no numerical
scientific reference applies. Read-only checks cannot leave partial output state.
NOT RUN: Windows/simulator/physical/empirical validation, outside governance scope.
Limits: software cannot detect undeclared risks, verify source authenticity or
prove an external authorization exists; agent/source/diff review remains mandatory.
Next eligible after accepted CI/integration: S009; legacy intake needs actual
source/provenance/license evidence, not assumed availability.

## E-S008-02 — Accepted integration
- PR #14 exact head 87d26f2c10b9616dcb70d264a77962b07bda300d passed CI run
  39712069254, completed/success; normal merge cd5a5ce51e67885f35db3939478d8b6af8171969.
- Published tree 265f2e41e09e7dd7787492665c6cc59df863ac2b equals local checkpoint
  59aa7fa tree, preserved branch. 48 tests/five validators pass.
- Author self-audit accepted S008 under ADR-0005 (8/88); S009 next.
- No model/runtime/scientific acceptance. Legacy source not designated in records;
  S009 must check source availability and stop if required evidence unavailable.
