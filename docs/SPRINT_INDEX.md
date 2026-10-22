# Micro-Sprint Index

Execution order is strict: one sprint at a time, ascending ID, each dependent on its predecessor. All begin as `not_started`.

| ID | Sprint | Phase | Depends on |
|---|---|---|---|
| [S001](sprints/S001-project-charter-and-non-goals.md) | Project charter and non-goals | P0 — Governance and scientific controls | None |
| [S002](sprints/S002-clean-room-repository-boundary.md) | Clean-room repository boundary | P0 — Governance and scientific controls | S001 |
| [S003](sprints/S003-scientific-evidence-ledger.md) | Scientific evidence ledger | P0 — Governance and scientific controls | S002 |
| [S004](sprints/S004-hypotheses-versus-experiment-settings.md) | Hypotheses versus experiment settings | P0 — Governance and scientific controls | S003 |
| [S005](sprints/S005-terminology-units-and-identifier-conventions.md) | Terminology, units, and identifier conventions | P0 — Governance and scientific controls | S004 |
| [S006](sprints/S006-quality-gates-and-definition-of-done.md) | Quality gates and definition of done | P0 — Governance and scientific controls | S005 |
| [S007](sprints/S007-change-control-and-architecture-decisions.md) | Change control and architecture decisions | P0 — Governance and scientific controls | S006 |
| [S008](sprints/S008-risk-register-and-escalation-rules.md) | Risk register and escalation rules | P0 — Governance and scientific controls | S007 |
| [S009](sprints/S009-legacy-source-inventory-protocol.md) | Legacy source inventory protocol | P1 — Legacy audit and evidence extraction | S008 |
| [S010](sprints/S010-legacy-module-and-dependency-graph.md) | Legacy module and dependency graph | P1 — Legacy audit and evidence extraction | S009 |
| [S011](sprints/S011-legacy-execution-path-and-data-flow.md) | Legacy execution path and data flow | P1 — Legacy audit and evidence extraction | S010 |
| [S012](sprints/S012-legacy-baseline-reproduction.md) | Legacy baseline reproduction | P1 — Legacy audit and evidence extraction | S011 |
| [S013](sprints/S013-legacy-tests-and-results-inventory.md) | Legacy tests and results inventory | P1 — Legacy audit and evidence extraction | S012 |
| [S014](sprints/S014-legacy-model-and-parameter-extraction.md) | Legacy model and parameter extraction | P1 — Legacy audit and evidence extraction | S013 |
| [S015](sprints/S015-legacy-discrepancy-and-defect-register.md) | Legacy discrepancy and defect register | P1 — Legacy audit and evidence extraction | S014 |
| [S016](sprints/S016-legacy-audit-freeze.md) | Legacy audit freeze | P1 — Legacy audit and evidence extraction | S015 |
| [S017](sprints/S017-supported-platform-matrix.md) | Supported platform matrix | P2 — Runtime and simulator integration | S016 |
| [S018](sprints/S018-python-tooling-and-environment-lock.md) | Python tooling and environment lock | P2 — Runtime and simulator integration | S017 |
| [S019](sprints/S019-sumo-installation-and-version-smoke-test.md) | SUMO installation and version smoke test | P2 — Runtime and simulator integration | S018 |
| [S020](sprints/S020-ns3-installation-and-version-smoke-test.md) | ns-3 installation and version smoke test | P2 — Runtime and simulator integration | S019 |
| [S021](sprints/S021-sumo-headless-deterministic-smoke.md) | SUMO headless deterministic smoke | P2 — Runtime and simulator integration | S020 |
| [S022](sprints/S022-ns3-minimal-packet-smoke.md) | ns-3 minimal packet smoke | P2 — Runtime and simulator integration | S021 |
| [S023](sprints/S023-simulator-adapter-boundary.md) | Simulator adapter boundary | P2 — Runtime and simulator integration | S022 |
| [S024](sprints/S024-environment-reproducibility-smoke.md) | Environment reproducibility smoke | P2 — Runtime and simulator integration | S023 |
| [S025](sprints/S025-json-naming-units-and-versioning-conventions.md) | JSON naming, units, and versioning conventions | P3 — JSON contracts and configuration | S024 |
| [S026](sprints/S026-run-manifest-schema.md) | Run manifest schema | P3 — JSON contracts and configuration | S025 |
| [S027](sprints/S027-city-and-road-map-schema.md) | City and road-map schema | P3 — JSON contracts and configuration | S026 |
| [S028](sprints/S028-population-grid-schema.md) | Population-grid schema | P3 — JSON contracts and configuration | S027 |
| [S029](sprints/S029-temperature-and-humidity-schema.md) | Temperature and humidity schema | P3 — JSON contracts and configuration | S028 |
| [S030](sprints/S030-bin-physical-model-schema.md) | Bin physical-model schema | P3 — JSON contracts and configuration | S029 |
| [S031](sprints/S031-vehicle-model-schema.md) | Vehicle model schema | P3 — JSON contracts and configuration | S030 |
| [S032](sprints/S032-depot-and-coverage-schema.md) | Depot and coverage schema | P3 — JSON contracts and configuration | S031 |
| [S033](sprints/S033-communication-and-plc-schema.md) | Communication and PLC schema | P3 — JSON contracts and configuration | S032 |
| [S034](sprints/S034-collection-policy-schema.md) | Collection policy schema | P3 — JSON contracts and configuration | S033 |
| [S035](sprints/S035-seeds-repetitions-and-experiment-matrix-schema.md) | Seeds, repetitions, and experiment matrix schema | P3 — JSON contracts and configuration | S034 |
| [S036](sprints/S036-schema-validation-and-negative-tests.md) | Schema validation and negative tests | P3 — JSON contracts and configuration | S035 |
| [S037](sprints/S037-road-network-import-and-coordinate-reference.md) | Road-network import and coordinate reference | P4 — City, population, and climate | S036 |
| [S038](sprints/S038-road-graph-integrity-and-legal-locations.md) | Road graph integrity and legal locations | P4 — City, population, and climate | S037 |
| [S039](sprints/S039-population-density-generation-interface.md) | Population-density generation interface | P4 — City, population, and climate | S038 |
| [S040](sprints/S040-manual-heatmap-and-block-editor-contract.md) | Manual heatmap and block editor contract | P4 — City, population, and climate | S039 |
| [S041](sprints/S041-automatic-population-distribution-contract.md) | Automatic population distribution contract | P4 — City, population, and climate | S040 |
| [S042](sprints/S042-climate-spatial-interpolation-and-source.md) | Climate spatial interpolation and source | P4 — City, population, and climate | S041 |
| [S043](sprints/S043-time-varying-environmental-context.md) | Time-varying environmental context | P4 — City, population, and climate | S042 |
| [S044](sprints/S044-map-population-climate-integration.md) | Map-population-climate integration | P4 — City, population, and climate | S043 |
| [S045](sprints/S045-bin-model-evidence-dossier.md) | Bin model evidence dossier | P5 — Bin physical/environmental models | S044 |
| [S046](sprints/S046-bin-state-lifecycle-contract.md) | Bin state lifecycle contract | P5 — Bin physical/environmental models | S045 |
| [S047](sprints/S047-fill-and-waste-accumulation-model.md) | Fill and waste accumulation model | P5 — Bin physical/environmental models | S046 |
| [S048](sprints/S048-waste-properties-moisture-and-composition.md) | Waste properties, moisture, and composition | P5 — Bin physical/environmental models | S047 |
| [S049](sprints/S049-pollutant-odor-and-leachate-model.md) | Pollutant, odor, and leachate model | P5 — Bin physical/environmental models | S048 |
| [S050](sprints/S050-rollover-tilt-and-liquid-event-model.md) | Rollover, tilt, and liquid-event model | P5 — Bin physical/environmental models | S049 |
| [S051](sprints/S051-sensor-inventory-and-telemetry-separation.md) | Sensor inventory and telemetry separation | P5 — Bin physical/environmental models | S050 |
| [S052](sprints/S052-time-step-bin-state-transition.md) | Time-step bin state transition | P5 — Bin physical/environmental models | S051 |
| [S053](sprints/S053-stochastic-process-and-uncertainty.md) | Stochastic process and uncertainty | P5 — Bin physical/environmental models | S052 |
| [S054](sprints/S054-bin-physics-and-environmental-validation-tests.md) | Bin physics and environmental validation tests | P5 — Bin physical/environmental models | S053 |
| [S055](sprints/S055-vehicle-model-evidence-dossier.md) | Vehicle model evidence dossier | P6 — Vehicles, fuel, routing, and depots | S054 |
| [S056](sprints/S056-payload-and-loading-invariants.md) | Payload and loading invariants | P6 — Vehicles, fuel, routing, and depots | S055 |
| [S057](sprints/S057-fuel-tank-and-consumption-components.md) | Fuel tank and consumption components | P6 — Vehicles, fuel, routing, and depots | S056 |
| [S058](sprints/S058-traffic-dependent-speed-and-consumption.md) | Traffic-dependent speed and consumption | P6 — Vehicles, fuel, routing, and depots | S057 |
| [S059](sprints/S059-safe-return-fuel-and-reachable-service-logic.md) | Safe-return fuel and reachable-service logic | P6 — Vehicles, fuel, routing, and depots | S058 |
| [S060](sprints/S060-road-constrained-routing-interface.md) | Road-constrained routing interface | P6 — Vehicles, fuel, routing, and depots | S059 |
| [S061](sprints/S061-vehicle-state-and-trip-lifecycle.md) | Vehicle state and trip lifecycle | P6 — Vehicles, fuel, routing, and depots | S060 |
| [S062](sprints/S062-depot-reachability-and-coverage.md) | Depot reachability and coverage | P6 — Vehicles, fuel, routing, and depots | S061 |
| [S063](sprints/S063-fleet-size-estimation-policy.md) | Fleet-size estimation policy | P6 — Vehicles, fuel, routing, and depots | S062 |
| [S064](sprints/S064-vehicle-and-fleet-adversarial-tests.md) | Vehicle and fleet adversarial tests | P6 — Vehicles, fuel, routing, and depots | S063 |
| [S065](sprints/S065-communication-evidence-inventory.md) | Communication evidence inventory | P7 — Communications and PLC | S064 |
| [S066](sprints/S066-plc-source-and-parameter-freeze.md) | PLC source and parameter freeze | P7 — Communications and PLC | S065 |
| [S067](sprints/S067-communication-technology-abstraction.md) | Communication technology abstraction | P7 — Communications and PLC | S066 |
| [S068](sprints/S068-delay-loss-bandwidth-and-range-model.md) | Delay, loss, bandwidth, and range model | P7 — Communications and PLC | S067 |
| [S069](sprints/S069-telemetry-sampling-and-payload-construction.md) | Telemetry sampling and payload construction | P7 — Communications and PLC | S068 |
| [S070](sprints/S070-network-versus-collection-only-mode.md) | Network versus collection-only mode | P7 — Communications and PLC | S069 |
| [S071](sprints/S071-ns3-trace-integration-and-time-alignment.md) | ns-3 trace integration and time alignment | P7 — Communications and PLC | S070 |
| [S072](sprints/S072-communication-adversarial-tests.md) | Communication adversarial tests | P7 — Communications and PLC | S071 |
| [S073](sprints/S073-collection-policy-interface.md) | Collection-policy interface | P8 — Collection policies and orchestration | S072 |
| [S074](sprints/S074-collection-eligibility-constraints.md) | Collection eligibility constraints | P8 — Collection policies and orchestration | S073 |
| [S075](sprints/S075-safety-constraints-and-priority-rules.md) | Safety constraints and priority rules | P8 — Collection policies and orchestration | S074 |
| [S076](sprints/S076-baseline-collection-policies.md) | Baseline collection policies | P8 — Collection policies and orchestration | S075 |
| [S077](sprints/S077-user-defined-policy-extension-contract.md) | User-defined policy extension contract | P8 — Collection policies and orchestration | S076 |
| [S078](sprints/S078-experiment-matrix-and-replication.md) | Experiment matrix and replication | P8 — Collection policies and orchestration | S077 |
| [S079](sprints/S079-deterministic-time-step-scheduler.md) | Deterministic time-step scheduler | P8 — Collection policies and orchestration | S078 |
| [S080](sprints/S080-integrated-one-run-multi-scenario-executor.md) | Integrated one-run multi-scenario executor | P8 — Collection policies and orchestration | S079 |
| [S081](sprints/S081-raw-event-log-and-time-series-schema.md) | Raw event log and time-series schema | P9 — Data, statistics, UI, and release | S080 |
| [S082](sprints/S082-run-provenance-and-recovery.md) | Run provenance and recovery | P9 — Data, statistics, UI, and release | S081 |
| [S083](sprints/S083-metric-catalogue-and-unit-tested-derivations.md) | Metric catalogue and unit-tested derivations | P9 — Data, statistics, UI, and release | S082 |
| [S084](sprints/S084-descriptive-statistics-and-independent-analysis.md) | Descriptive statistics and independent analysis | P9 — Data, statistics, UI, and release | S083 |
| [S085](sprints/S085-inferential-model-selection-and-preregistration.md) | Inferential model selection and preregistration | P9 — Data, statistics, UI, and release | S084 |
| [S086](sprints/S086-plots-csv-export-and-report-provenance.md) | Plots, CSV export, and report provenance | P9 — Data, statistics, UI, and release | S085 |
| [S087](sprints/S087-frontend-workflow-and-cross-platform-packaging.md) | Frontend workflow and cross-platform packaging | P9 — Data, statistics, UI, and release | S086 |
| [S088](sprints/S088-end-to-end-acceptance-and-release-gate.md) | End-to-end acceptance and release gate | P9 — Data, statistics, UI, and release | S087 |

Each sprint file specifies objective, scope, prerequisites, steps, deliverables, WB/BB/adversarial tests, acceptance, evidence, failure handling, stop conditions, and handoff. If scientific evidence or an irreversible decision is unresolved, log a blocker instead of guessing.

`docs/STATE/PROGRESS.json` is authoritative. File existence or a commit does not imply completion.
