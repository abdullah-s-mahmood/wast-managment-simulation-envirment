# Project Charter

Status: Proposed S001 scope freeze, eligible for owner-authorized single-maintainer
acceptance after tests and exact-head CI. This charter specifies intended outcomes,
not implemented or scientifically validated behavior.

## Purpose
Build a clean-room, cross-platform research environment for reproducible waste-management simulations. Researchers configure scenarios through versioned files/UI rather than editing source. The environment separates domain models, SUMO mobility, ns-3 network simulation, collection policies, raw outputs, and independent statistical analysis.

## Outcomes
1. Versioned JSON/GeoJSON contracts for settings and model parameters.
2. Independently testable bin, vehicle, depot, environment, communication, and policy modules.
3. Explicit SUMO/ns-3 adapters and collection-only mode.
4. One orchestration request expands a declared experiment matrix with isolated state and recorded seeds.
5. Raw event/time-series outputs, metric definitions, data dictionary, and provenance.
6. Independent descriptive/inferential analysis with documented design, diagnostics, uncertainty, and exports.
7. Cross-platform setup, tests, and release gates.
8. UI for maps, population heatmaps, climate, bin/vehicle profiles, depots/fleet, communication, policy, execution, and export.

## Scope
City roads/CRS, population density, temperature/humidity, bin geometry/state/fill/waste properties and evidence-supported pollutant/odor/leachate/rollover behavior, sensors/telemetry, vehicle payload/fuel/consumption/traffic/routing/safe return, depot reachability/fleet sizing, LTE/LoRa/Wi-Fi/Bluetooth/fiber/no-connection, PLC restricted to current approved sources, baseline/custom policies, experiment matrices and independent repetitions, raw data and statistical outputs.

## Non-goals in the initial phase
No copying/refactoring legacy implementation in place; no unverified equations/parameters; no hard-coded city, bin count, or fleet as a scientific assumption; no universal-accuracy/zero-defect promise; no causal claims without a valid design.

## Principles
Clean-room separation; evidence before equations; JSON-first; explicit units and stable IDs; deterministic random streams; fail closed on invalid configuration; preserve raw and failed runs; separate software correctness from scientific validity.

## Success criteria
A clean supported environment runs a declared test matrix, preserves inputs/provenance, validates invariants, exports complete raw records, independently reproduces specified metrics/summaries, and discloses limitations and tests not run.

## Users and decisions
- Researchers declare scenarios, hypotheses, experiment factors, and analysis plans before comparing collection policies.
- Model developers implement isolated contracts and provide source, unit, boundary, and reference evidence.
- Independent reviewers reconstruct runs and metrics from retained inputs, code versions, raw observations, and test evidence.
- Scenario operators configure maps, fleets, sensors, and policies through validated inputs and later UI controls.

## Scope map and observable acceptance
The IDs below identify charter requirements, not accepted implementation. Sprint ranges
assign ownership; no downstream work is authorized before its prerequisites pass.

| ID | Intended outcome and boundary | Observable artifact and acceptance criterion | Roadmap |
|---|---|---|---|
| C01 | Evidence and clean-room governance | Source inventory, evidence ledger, and decisions distinguish legacy observations from accepted models; no reuse without licensing review and ADR. | S002–S016 |
| C02 | Reproducible external adapters | Recorded platform/version smoke tests and adapter failure fixtures; unavailable platforms remain NOT RUN. | S017–S024 |
| C03 | Versioned configuration | JSON/GeoJSON contracts, valid/invalid fixtures, normalized snapshots and hashes; invalid settings fail before execution. | S025–S036 |
| C04 | Configurable city/environment | Road/CRS, population and climate artifacts with provenance; illegal locations and unsupported inputs are rejected. | S037–S044 |
| C05 | Bin state and sensors | Evidence dossiers and transition/reference tests; internal state and transmitted telemetry have distinct contracts. | S045–S054 |
| C06 | Vehicles and depots | Payload, fuel, legal routing and safe-return fixtures demonstrate declared constraints; no reward can override feasibility. | S055–S064 |
| C07 | Communications | Approved-source dossier and packet traces; collection-only mode delivers no hidden current telemetry and reports network metrics as unavailable with a reason. | S065–S072 |
| C08 | Policies and execution | Observation/action traces, isolated matrix rows and named seed streams; replay and failure fixtures verify bounded determinism and run isolation. | S073–S080 |
| C09 | Auditable data and analysis | Complete raw records, metric reference fixtures and independent analysis outputs; specified metrics reproduce from exported data under declared tolerances. | S081–S086 |
| C10 | Operator interface and release | UI controls map to resolved configuration; every advertised platform and end-to-end release gate has executed evidence or remains open. | S087–S088 |

## Scenario settings and hypothesis boundary
City size, bin count, fleet size, depot locations, population maps, climate inputs,
and policy choices are scenario settings. They may be manipulated factors in a
declared experiment; their chosen values are not universal scientific hypotheses.
A hypothesis specifies a testable relationship or model behavior, with applicability
and evidence requirements. No equation, distribution, or numerical physical value
is accepted by this charter. PLC retains its approved source constraint; source
identification and verification remain future evidence gates.

## Contract conventions and failure semantics
Future contracts must carry stable entity/run/scenario IDs, schema versions,
explicit quantity units, coordinate reference systems, simulation time and interval
units, and separate wall-clock execution timestamps. Exact field names, supported
versions, units and tolerances are deferred to their owning contract sprints;
this document supplies no implicit numerical defaults. UI defaults must appear
in the resolved configuration. Invalid, unsupported, contradictory or incomplete
inputs fail closed with diagnostics. Failed/interrupted runs retain inputs, logs
and partial artifacts labelled incomplete; they cannot enter successful-run analysis
silently. Provenance links code, configuration hashes, seeds, environment and sources.

## Exclusions and approval boundary
Initial work excludes production deployment, paid resources, real-time municipal
control, and claims of universal physical accuracy. A plausible plot or passing
software test does not establish empirical validation. Statistical association
does not establish causality; causal claims require a defined estimand and justified
design. Scientific acceptance and final release require their independent gates.
S001 acceptance requires recorded WB/BB/adversarial tests, a charter comprehension
self-audit, exact-head CI success, and truthful acceptance evidence. The sole
maintainer has waived the second-person review requirement. S002 remains ineligible
until S001's technical gate and integration are complete.
