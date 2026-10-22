# Wast Management Simulation Environment

A clean-room, research-oriented environment for reproducible waste-management simulations integrating city context, waste bins, collection vehicles, depots, communication models, SUMO mobility, and ns-3 network simulation.

> **Current phase: documentation and verification planning only.** No simulation model, physical equation, protocol parameter, or scientific claim is considered validated merely because it is described here. Implementation must be gated by source audit, explicit evidence, deterministic tests, and recorded decisions.

## Project principles

1. **Clean-room build:** do not copy the current/legacy implementation into this repository. Inspect it only as evidence when a separately approved audit is performed.
2. **JSON-first experiment inputs:** all experiment-specific data and model parameters must be externalized, versioned, schema-validated, and included in each run's provenance.
3. **Models are not scenarios:** equations and module behavior are distinct from scenario settings such as city, population, bin count, fleet size, or depot placement.
4. **Evidence before equations:** no scientific model or parameter is locked without a traceable source, a stated applicability domain, units, assumptions, and validation plan.
5. **One run, many scenarios:** the eventual runner should execute a declared experiment matrix across city forms, densities, policies, vehicle models, and communication settings while preserving run-level independence and seeds.
6. **Raw data first:** retain event-level and time-step observations, explicit units, identifiers, configuration snapshots, and provenance before deriving metrics.
7. **Statistics are independent:** analysis must consume immutable exported data and a preregistered analysis plan; it must not silently change the simulator or select favorable runs.
8. **No false certainty:** tests can establish bounded correctness for specified cases, not guarantee that every possible run or scientific assumption is correct.
9. **White-box, black-box, and adversarial testing:** each sprint requires relevant internal invariants, observable behavior, boundary cases, malformed inputs, failure injection, and regression checks.
10. **Cross-platform by design:** supported Windows and Linux workflows must be documented and tested independently.

## Start here

1. Read [AGENTS.md](AGENTS.md) before doing any work.
2. Read [the project charter](docs/PROJECT_CHARTER.md), [architecture](docs/ARCHITECTURE.md), and [evidence policy](docs/RESEARCH_AND_EVIDENCE_POLICY.md).
3. Follow the [sprint index](docs/SPRINT_INDEX.md) in order. Do not skip a dependency gate.
4. Check [progress state](docs/STATE/PROGRESS.json), [agent handoff](docs/STATE/AGENT_HANDOFF.md), and [blockers](docs/STATE/BLOCKERS.md).
5. Complete exactly the next eligible sprint unless the sprint explicitly authorizes a tightly coupled set.
6. Run the sprint's tests and the repository documentation validator. Record actual commands, exit codes, evidence, and failures.
7. Update state only after verification. Under the owner's sole-maintainer policy, an authorized agent may merge its own PR after required exact-head CI and all sprint gates pass; no second reviewer is required. Never bypass GitHub protections or falsify evidence.

## Repository map

- `docs/sprints/`: one detailed Markdown execution contract per micro-sprint.
- `docs/STATE/`: machine-readable progress and human-readable handoff, decisions, blockers, and validation log.
- `docs/adr/`: architectural decisions and their status.
- `docs/templates/`: reusable sprint and decision templates.
- `scripts/`: repository-governance validation utilities, not simulation logic.
- `.github/`: pull-request conventions and CI checks.

## What this repository does not claim yet

- It does not claim that any bin, vehicle, waste-generation, pollutant, odor, liquid leakage, rollover, fuel-consumption, or communication model is scientifically validated.
- It does not claim that SUMO or ns-3 is installed, integrated, or reproducible on every platform.
- It does not preselect a statistical causal model before the estimand, design, dependence structure, and data-generating process are specified.
- It does not promise zero defects or 100% guaranteed scientific results.

## Current status

The initial deliverable is the governance and verification plan. See `docs/STATE/PROGRESS.json` for actual sprint state; a PR or passing code alone is not proof of completion.
