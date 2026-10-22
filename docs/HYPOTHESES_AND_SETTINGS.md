# Hypotheses and experiment settings

Authority: ADR-0003, D-0002, evidence policy and S004. These classifications
express design requirements; no physical hypothesis or causal effect is accepted.

## Classification rules
A hypothesis states a falsifiable relationship or module behavior. It requires
an evidence ID, applicability domain, variables/units, reference test and empirical
validation plan before scientific acceptance. A value chosen to define a case is
a setting; changing it must not rewrite that relationship. Split mixed statements
into separate IDs. Ambiguous statements remain unresolved until their provenance,
role and acceptance test are explicit; do not infer categories from a number alone.

A control is an experimental role of a setting held fixed, not a second physical
model. A setting can instead be manipulated or used for blocking. Record its role
per experiment, before results. A measurement is a raw observation of an event or
state; an outcome is a predefined result computed from observations with a named
method and units. The separation is not a causal inference: later causal claims
still need estimands, identification assumptions, experimental units and diagnostics.

## Classification table
| Stable concept ID | Statement or example | Classification | Verification or required evidence |
|---|---|---|---|
| model_relationship | A proposed relationship specifies module response to its inputs. | hypothesis | Evidence ledger record, exact equation/domain, reference and independent validation; unavailable until sourced. |
| population | Choose a population grid for this case. | scenario setting | Validate grid provenance/units and vary its reference without model edit (synthetic separation test now; S028/S039–S044 later). |
| map | Select city road geometry. | scenario setting | Vary map reference without model edit; road/CRS validation S027/S037–S038. |
| bin_count | Choose the number of bin instances. | scenario setting | Count/IDs validated in future schema; immutable model identity under alternative labels tested now. |
| fleet_size | Choose the number of vehicle instances. | scenario setting | Vary fleet reference without model edit; capacity assumptions need separate evidence, S031/S063. |
| depot_placement | Choose depot locations. | scenario setting | Vary location reference without model edit; legal road reachability S032/S062. |
| climate_input | Select source-backed temperature/humidity context. | scenario setting | Units, provenance and time/space coverage S029/S042–S044; response relationships remain separate hypotheses. |
| policy_choice | Select a policy and documented tuning values. | scenario setting | Versioned policy reference and constraints S034/S073–S077; no silent policy implementation rewrite. |
| fixed_map | Hold map fixed while varying population. | control (role of map) | Experiment roles explicitly held_fixed/manipulated/blocked; actual design S035/S078. |
| bin_geometry | State a bin's stable dimensions/capacity. | specification | Explicit units, manufacturer/source provenance, S030; not a derived outcome. |
| current_fill | Store current fill or payload at a time step. | runtime_state | Lifecycle/accounting tests S046/S052/S056; changing observations cannot rewrite model or inputs. |
| sensor_sample | Retain a time-stamped observation with units. | measurement | Source/time/sensor provenance and raw-data validation S051/S081. |
| transmitted_fields | Select allowed sensor fields for transmission. | telemetry | Explicit allow-list S051/S069, distinct from full runtime_state; transmission is not implied by installation. |
| total_collected | Compute a predefined total from retained events. | outcome | Formula, units, event accounting, missing/failed-run handling S083/S084; do not select favorable results. |

A concept ID is stable within this classification table, not a runtime entity ID.
Missing, zero, unknown and not applicable differ. No numeric scenario defaults,
physical equations, units, seeds or time cadence are introduced by these examples.
Future contracts must specify each quantity's units and time semantics explicitly.

## Observable governance example
`tests/fixtures/classification/model.json` is an explicitly synthetic software
identity hypothesis. `scripts/validate_study_separation.py` checks a governance
proposal against a separately selected baseline file's exact-byte SHA-256. This
is a boundary illustration, not a runtime schema, model evaluator or simulator.
Proposal version 1 has exactly governance_version, model_sha256, settings,
factor_roles, measurements and outcomes. The five required settings are opaque
nonempty synthetic labels; no label is interpreted as physical data. Each requires
an explicit manipulated, held_fixed or blocked role. Observation and derived
outcome IDs are separate, nonempty and unique. There are no implicit defaults.

Changing population, map, bin_count, fleet_size or depot_placement leaves baseline
bytes and model hash unchanged. Injecting a hypothesis override, changing model
bytes/hash, omitting a role or mixing observation/outcome IDs fails closed. A new
model version requires an explicit evidence/ADR review and baseline change; a hash
does not certify the baseline's scientific validity. Choosing a different baseline
is a review action, not something this checker can authorize.

Run `python -m unittest discover -s tests -p test_study_separation.py -v` for the
public CLI and independent byte comparisons. CLI usage is
`python scripts/validate_study_separation.py proposal.json --model model.json`.
Malformed/unsupported/truncated/duplicate-key input exits 1 without rewriting
inputs or creating outputs. This read-only check has no partial-write state.
