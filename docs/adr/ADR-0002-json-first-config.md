# ADR-0002 — JSON-first external configuration

- Status: Accepted in principle; exact schemas provisional
- Date: 2026-10-22

Researchers must vary maps, population, climate, bins, vehicles, depots, communication, policies, and experiment matrices without editing source. Use versioned JSON for structured data and GeoJSON for spatial features; validate before execution and preserve resolved inputs per run. Keep specification, scenario settings, runtime state, telemetry, and analysis separate. Exact filenames/schema tooling are decided in S025–S036.

S007 clarification addendum (2026-10-22): supplements record structure without
changing the accepted choice. Alternatives below are present review options, not
claims of undocumented historical evaluations.

## Context
Researchers need reproducible case changes without editing model implementation. Separate specifications, settings, state, telemetry and derived analysis.

## Options considered
Current alternatives: retain external versioned JSON/GeoJSON; embed settings in source; defer exact schemas. Embedded settings conflict with D-0003. Exact schemas remain deliberately deferred.

## Decision
Preserve the accepted principle in the original text above. Rationale: versioned resolved inputs can be validated and hashed. This does not accept any filename, schema tooling or physical parameter.

## Evidence and assumptions
D-0003, docs/JSON_DATA_CONTRACTS.md and reproducibility policy. Exact schemas remain provisional until S025–S036; no runtime validation demonstrated here.

## Consequences
Schema changes require version/migration review; per-run snapshots retain original inputs and units. Additional schema tooling is not silently chosen.

## Validation and revisit conditions
Negative schema tests, provenance/hash/replay checks in S025–S036 and later integration. Revisit if supported data cannot be represented reproducibly; new ADR must assess compatibility and migration.
