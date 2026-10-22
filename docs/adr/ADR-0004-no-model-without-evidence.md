# ADR-0004 — No scientific model without traceable evidence

- Status: Accepted
- Date: 2026-10-22

A physical, environmental, vehicle, fuel, or network equation is not accepted solely because it is plausible or exists in legacy code. Record source, equation, variables, units, applicability, uncertainty, validation plan, and limits. Unsupported quantities remain provisional/unavailable. Software completion and scientific validation are separate statuses.

S007 clarification addendum (2026-10-22): supplements record structure without
changing the accepted choice. Alternatives below are present review options, not
claims of undocumented historical evaluations.

## Context
Plausible equations or observed legacy behavior can otherwise be mistaken for scientific validation.

## Options considered
Require traceable sources and independent/empirical gates; accept plausible behavior; use software tests alone. Latter choices cannot establish applicability or physical accuracy.

## Decision
Keep the original evidence gate. Rationale: source, domain, units and validation limits must precede model acceptance; unsupported quantities remain provisional/unavailable.

## Evidence and assumptions
D-0006, research/evidence policy and S003 report. Production ledger is empty; its structural checks do not verify source authenticity or empirical fit.

## Consequences
Missing evidence may block a model sprint. Failed runs, uncertainty and unsupported domains remain visible. No parameter is guessed to satisfy a demo.

## Validation and revisit conditions
Run evidence-ledger tests/validator; owning model sprint must independently reproduce references and meet empirical gates. Revisit only by evidence-backed ADR, without fabricating sources.
