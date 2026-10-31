# S014 — source model extraction ledger

This ledger records bounded, read-only observations of the designated archive.
It accepts no scientific model, physical parameter, source reuse or redistribution.
Observed source, intended behavior and scientifically supported behavior remain
separate. Every extracted expression retains an immutable source reference;
no code is reconstructed or normalized into the clean-room implementation.

## Artifacts and exact traceability

- S014_REVIEW_PLAN.json: sanitized review observations, opaque archive entry IDs,
  source SHA-256 and one-based inclusive line ranges.
- S014_REVIEW_SUMMARY.json: counts and hashes of the private resolved ranges.
- S014_AUXILIARY_SUMMARY.json: source context and Python syntax extraction counts.
- S014_COVERAGE.json: cross-artifact coverage result for the explicit audit scope.
- Private Git metadata private-evidence/S014: resolved source byte ranges/span
  hashes, original names/numeric spellings, Python expression ranges, full source
  hashes, manifests, diagnostics and test transcripts. Source paths stay private.

The candidate index retains broad lexical matches. The reviewed ranges capture
multiline core expressions and non-Python orchestration. Static Python extraction
also retains assignment values, augmented assignments, function/keyword defaults,
guards, returns and calls (including unassigned calls with configuration arguments).
Python source is parsed as data; no imports, subprocesses, evaluation or execution
from that source occurs. Calls, aliases, imported libraries, external inputs and
conditional execution remain unresolved, not guessed.

## Observation families

| Family | Source anchors | Evidence interpretation |
|---|---|---|
| Sensor dynamics | entry-00010995 | Source stochastic initialization/update formulas and named streams; provisional, not calibrated. |
| Collection, fuel, encoding and masks | entry-00010855; entry-00010993 | Mass/capacity accounting, distance proxy, features and eligibility; not physical-model validation. |
| PLC capacity and packet outcomes | entry-00010844; entry-00010843; associated declarations | Shared service queue and separate embedded outcome tables; do not conflate capacity, goodput, packet latency and channel behavior. |
| Auxiliary field-trial curves | entry-00010845; entry-00010999; entry-00000149 | Digitized estimates and interpolation/perturbation assumptions, not raw measurements or a validated uncertainty interval. |
| Mobility and routing | entry-00010833; entry-00010848; related interfaces | External adapter settings, road costs, selection, stopping and arrival rules. |
| SLA and reward | entry-00010838; entry-00011005 | Policy state/time rules and objective weights, not law or empirical calibration. |
| Admission and identity | entry-00010840; entry-00010994 | Telemetry allow-list, deterministic simulation keys, signature/freshness/replay checks; not a deployment security certification. |
| Runtime orchestration | entry-00010836 | Defaults, seed mapping, time barriers, telemetry freshness, service/drain scheduling and derived counters; F-S012-01 retained. |
| Optional inference/training/export | entry-00010847; entry-00011025; entry-00011023 | Architecture, replay/sampling, objective/target updates and numerical parity settings; no training or inference executed here. |
| Scenarios and synthetic topology | entry-00000154; entry-00000165; entry-00000168 | Scenario defaults, geometry, sampling/rejection and provenance labels; not surveyed physical infrastructure or population calibration. |
| Statistics and tool behavior | entry-00011031; entry-00011032; Python syntax index | Aggregation, sample/paired statistics and guards observed in source; estimand/independence/distribution assumptions remain unvalidated. |
| Logging, provenance, build and launchers | remaining reviewed native/shell/build ranges | Interface/default/gating/monitoring semantics, distinct from physical equations. |

## Units, defaults, assumptions and support

Original names and unit spellings remain in exact source ranges; suffixes/comments
are source claims, not independently verified dimensions. Unstated units remain
unknown. No default, missing constant, distribution parameter or applicability
boundary is replaced by intuition. Original expressions are retained before any
future normalization; normalization is null in these artifacts.

Source-written defaults and software guards are E4 observations. They are not
accepted physical calibration values or a scientifically established domain.
Code comments naming references are not independent source verification. Intended
behavior is UNAVAILABLE without a separate requirements source; scientific support
remains UNVALIDATED. No new scientific evidence record or PLC source substitution
is accepted. Future model gates still require actual sources, units, domains,
uncertainty/calibration and independent/empirical validation.

Seed derivation, deterministic source-range hashing and reproducible audit outputs
are distinct from cross-library RNG replay and empirical distribution validity.
Passing extraction/reference tests establishes tested software properties only.
No legacy tests, campaign, hardware adapter, binary or archived script was run.

## Scope and residual limitations

The scope is the 83 hash-verified active-path source files identified by S013.
Eighteen test/probe files remain test evidence in S013, not scientific definitions.
All remaining Python files are parsed as data. Native/interface/shell/build sources
have selected reviewed ranges; broader lexical candidates remain linked. Coverage
checks reject missing/duplicate source IDs, source/plan hash disagreement, missing
ranges and substituting a model's classification with test evidence.

This is a bounded static extraction, not a proof of exhaustive program semantics.
Path contexts are hints; native preprocessing, arbitrary shell semantics, dynamic
calls, external configuration/data, imported libraries and transitive definitions
are not resolved. Retired/vendor/generated content remains in the full S009 index
and S010/S013 context; it is not silently promoted to the active target or cleared
for reuse. Whole-archive semantic analysis remains false. Linux is the actual
audit platform; Windows execution is NOT RUN and not claimed as verified here.

These limitations constrain future scientific/model acceptance; they do not turn
source extraction into a successful baseline reproduction. S012 remains a failed
baseline report and all historical trust findings remain intact.
