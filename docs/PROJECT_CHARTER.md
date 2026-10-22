# Project Charter

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
