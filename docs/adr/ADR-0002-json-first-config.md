# ADR-0002 — JSON-first external configuration

- Status: Accepted in principle; exact schemas provisional
- Date: 2026-10-22

Researchers must vary maps, population, climate, bins, vehicles, depots, communication, policies, and experiment matrices without editing source. Use versioned JSON for structured data and GeoJSON for spatial features; validate before execution and preserve resolved inputs per run. Keep specification, scenario settings, runtime state, telemetry, and analysis separate. Exact filenames/schema tooling are decided in S025–S036.
