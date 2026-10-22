# Research and Evidence Policy

## Evidence classes
- **E1:** direct primary measurements, validated standards, or authoritative specifications in the intended domain.
- **E2:** systematic review/meta-analysis or synthesis useful for discovery and context.
- **E3:** adjacent-domain evidence requiring a transferability argument.
- **E4:** observed legacy behavior; not scientific proof.
- **E5:** provisional assumption/calibration target; never call it a published fact.

## Required record
For every equation, parameter, distribution, protocol behavior, or claim record: stable evidence ID; full citation and DOI/URL; version/access date; exact page/table/equation/figure/code location; variable definitions and units; range; applicable material/vehicle/network/climate/scale; source conditions and calibration; uncertainty/limitations; target module/config field; unit/reference test; empirical validation plan; decision status and rationale.

## Acceptance gate
Accept a model only after documenting intended use, exact equation, dimensions, parameter source, calibration domain, uncertainty, boundary behavior, reference tests, independent/empirical validation strategy, and out-of-domain behavior. Software tests and scientific validation are separate. If no defensible model exists, mark the quantity provisional/unavailable.

## Project cautions
- Keep currently approved PLC sources unless an evidence-backed ADR changes them.
- Stochastic fill variation requires distribution, parameters, units, source/calibration rationale, seed stream, and sensitivity analysis.
- Vehicle fuel models distinguish motion, idle, stop/start, load, and traffic only where supported; avoid double-counting traffic.
- Safe return uses feasible road routes and a declared reserve/uncertainty rule.
- Odor, pollutants, leachate, and rollover outputs require supported submodels.
- Manufacturer specifications are not automatically duty-cycle data; software docs are not physical evidence.
- Never invent citations, DOI values, equations, or parameter values.
