# Provisional Architecture

This is a proposed architecture, not approval of equations or parameter values. Interfaces are finalized in their assigned sprints.

## Layers
1. Configuration/schema validation and resolved run manifest.
2. Domain contracts/state for bins, waste, vehicles, depots, environment, communications, and policies.
3. Source-backed scientific model adapters with units, domain, uncertainty, and fixtures.
4. SUMO mobility adapter for road network, routes, traffic, position, and travel time.
5. ns-3 network adapter for packet events/traces and time/correlation mapping.
6. Orchestrator for deterministic time steps, experiment expansion, isolated runs, failure state, and recovery.
7. Append-only raw event/time-series output and data dictionary.
8. Independent metrics/statistics/diagnostics/plots/CSV export.
9. UI for configuration, validation, run monitoring, and export.
10. Governance: tests, evidence ledger, ADRs, CI, provenance, sprint gates.

## State transition
A model update receives immutable prior state, versioned model config, scenario inputs, environment values valid for the requested time, explicit time interval, and named random stream if stochastic. It returns new state and typed events. No hidden global state, wall-clock dependency, mutable UI state, or uncontrolled randomness.

## Proposed files
`city.json` + road GeoJSON/SUMO network; `population.json`; `climate.json`; `bins.json` (per-bin ID/location/profile/dimensions/sensors/internal state/derived environment fields); `vehicles.json`; `depots.geojson` or `depots.json`; `communications.json`; `policies.json`; `experiment.json`; `run-manifest.json`. These are proposals; S025–S036 finalize them. GeoJSON is for spatial features; JSON is for structured settings/state. Avoid duplicate authoritative values without precedence rules.

## Integration rules
SUMO/ns-3 stay behind adapters; domain modules are testable without them. Cross-layer events carry run ID, simulation time, subsystem, entity/packet IDs, and units. Simulation time differs from wall time. Each experiment row has isolated state and seed streams. Failed runs remain recorded. Network metrics in collection-only mode are NA with a reason, not zero. UI defaults appear in resolved config.

## Open decisions
Toolchain versions, coupling, event ordering, checkpointing, parallelism, schema implementation, statistical family, and physical equations remain gated by sprint/evidence reviews.
