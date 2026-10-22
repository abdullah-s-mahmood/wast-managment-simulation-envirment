# Reproducibility and Provenance

Each run retains run/scenario IDs; exact matrix row; resolved inputs and hashes; repository commit; dependency/OS/architecture/SUMO/ns-3 versions; all seeds/stream rules; time step and clock mappings; source IDs and transformations; exit status/warnings/errors; raw-output hashes/data dictionary; analysis version and filters.

Identical code/config/environment/seeds should reproduce deterministic outputs exactly where supported. If simulators, floating point, parallel scheduling, or platforms prevent bitwise identity, declare tolerances and compare key invariants/metrics.

Write outputs atomically and mark complete only after integrity checks. Preserve failed/partial runs. Never reuse stale files. Resume/checkpoint must validate configuration and software compatibility.

Proposed directory: `runs/<experiment-id>/<run-id>/`, containing `input_snapshot/`, `manifest.json`, `logs/`, `raw/`, `derived/`, `figures/`, and `validation/`. Final layout remains subject to an ADR.
