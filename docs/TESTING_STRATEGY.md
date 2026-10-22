# Verification and Test Strategy

## Required layers
- **White-box (WB):** internal invariants, state transitions, conservation/accounting, deterministic branches, error handling, random-stream separation, adapter boundaries.
- **Black-box (BB):** observable CLI/API/UI behavior and generated artifacts.
- **Adversarial/negative:** malformed, missing, contradictory, duplicated, boundary, extreme, reordered, unsupported, interrupted, corrupted inputs.
- **Property/metamorphic:** capacity bounds, conservation, deterministic replay, and run isolation across generated inputs.
- **Reference/differential:** hand calculations or source-backed values where available.
- **Integration/cross-platform:** actual SUMO/ns-3 boundaries and every advertised platform.
- **Statistical validation:** design checks, justified distribution checks, sensitivity, and analysis correctness.

## Attack checklist
Try minimum/maximum/exact boundaries; negative/NaN/Infinity/wrong units; missing/unknown fields; duplicate IDs; stale references; invalid geometry; unreachable locations; zero/negative duration; repeated/out-of-order events; restart; missing executable; timeout/nonzero exit; malformed traces; partial outputs; deterministic replay; state/RNG leakage; extreme valid climate/traffic; no-network mode; failed-run preservation.

## Scientific validity is distinct
A software test proves only its assertion, not that it represents nature. Empirical validation requires suitable measurements, uncertainty, calibration/holdout separation, and applicability limits. Do not call a model scientifically validated based only on code coverage or plausible plots.

## Exit rules
Critical invariant failure fails the sprint. Missing dependencies are NOT RUN and keep the gate open. Investigate flaky tests; never hide failure by retrying. Stochastic criteria are predeclared. Tolerances state units and rationale. Every pass links to an executed command, exit code, and evidence.
