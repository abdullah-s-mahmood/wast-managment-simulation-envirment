# Statistical Analysis Plan — Provisional Framework

This is a guardrail, not a preselected final model. Methods follow the declared design and data structure.

## Before confirmatory runs
Specify primary/secondary outcomes and units; estimands; factors (city form, density, policy, vehicle/fleet, communication, justified climate factors); randomization/blocking/pairing; independent experimental unit and dependence; independent repetitions and precision/power rationale; seeds/common-random-number policy; exclusions/failure/missingness/stopping/multiplicity; planned comparisons and sensitivity analyses.

## Data integrity
Preserve every planned run, including failures and exclusions with reason codes. Keep run/scenario/replicate/seed IDs, config hashes, versions, and source revision. Do not treat ticks, packets, or bins as independent replicates when nested/serially correlated. Define aggregation level before analysis. Raw data are immutable; derived tables record formulas, filters, and analysis version.

## Descriptive analysis
Report counts/missingness, mean/SD where meaningful, median/IQR for skewed distributions, quantiles and uncertainty, distribution shape, per-run variation, and failure rates. Avoid only pooled means.

## Inferential analysis
Depending on estimand/design, candidates include paired comparisons, factorial models, generalized linear models, mixed-effects models for nested/repeated data, robust/clustered uncertainty, permutation tests, or bootstrap intervals. These are candidates, not defaults. Report effect sizes and confidence intervals with p-values; address multiplicity; diagnose model fit, residuals, influence, heteroscedasticity, and assumptions; conduct sensitivity analysis.

## Causality and leakage
Association is not causation. Causal claims require a defined estimand, identification strategy, assumptions, and suitable design. Freeze primary analysis before confirmatory outcomes are inspected. Label post hoc analysis exploratory. Do not tune assumptions/select favorable models without disclosure or remove runs because they weaken a desired conclusion.

## Reproducible deliverables
Raw hashes, data dictionary, metric definitions, analysis code/version, environment, model specification, diagnostics, effect sizes, uncertainty, exclusions, figures/tables, and limitations.
