# JSON and GeoJSON Data Contracts

## Separation
1. **Specification:** stable design attributes (bin material/geometry; vehicle class/capacity).
2. **Scenario input:** map, population, climate, locations/counts, depots, policy, experiment factors.
3. **Runtime state:** fill, mass, fuel, payload, position, sensor readings, lifecycle, events.
4. **Telemetry payload:** allow-listed subset sampled/transmitted by the selected communication model.
5. **Derived output:** reachability, environmental calculations, metrics, and summaries with method/version/provenance.

An installed sensor is not necessarily sampled or transmitted. Full internal bin state is not transmitted by default.

## Proposed files
| Family | Contents | Validation focus |
|---|---|---|
| city/map | CRS, geometry, road restrictions/IDs | geometry, CRS, legal road references |
| population.json | blocks, counts/density, method/seed | area units, overlaps, totals |
| climate.json | temperature/humidity grids or series, source/interpolation | units, coverage, timestamps |
| bins.json | every bin ID/location/profile/dimensions/sensors/internal state/derived context | capacity, units, source IDs, telemetry separation |
| vehicles.json | instances/profiles, payload/tank/current fuel/model references | bounds, units, model IDs |
| depots.geojson/json | points, capabilities, assignments | road access, route-based semantics |
| communications.json | LTE/LoRa/Wi-Fi/Bluetooth/fiber/no-connection, PLC, telemetry profile | source refs, units, no-connection invariants |
| policies.json | policy ID/version and tunable parameters | allowed fields and hard constraints |
| experiment.json | factors, levels, repetitions, seeds, pairing/blocking | unique IDs, coverage/run count |
| run-manifest.json | resolved config hashes, versions, seeds, status, outputs | provenance |

Filenames are proposals; S025–S036 finalize them. Every schema is versioned. Every entity has a stable ID. Units and timestamp/timezone semantics are explicit. Missing, null, zero, unknown, and not-applicable are distinct. Reject NaN/Infinity, duplicate IDs, invalid references, unsupported versions, and contradictions. GeoJSON is for spatial geometry with CRS documented. Resolved inputs are preserved/hashed per run. Defaults are visible in resolved configuration.

## Custom variables/equations
A future extension may declare variable, units, update cadence, dependencies, model ID, parameters, evidence ID, and tests. Do not evaluate arbitrary executable expressions unsafely. Detect cycles, missing inputs, invalid units, and numerical failures.
