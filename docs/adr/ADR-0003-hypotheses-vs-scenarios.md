# ADR-0003 — Separate hypotheses from scenario settings

- Status: Accepted
- Date: 2026-10-22

A hypothesis describes testable module behavior or a relationship. A scenario setting defines the case under study: city geometry, population heatmap, bin count, fleet size, depot location, climate input, or policy choice. Varying a scenario must not rewrite the model contract. Analysis states which factors are manipulated, held fixed, blocked, or measured.
