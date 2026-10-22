# Release Gates

A demo that runs is not sufficient.

A. **Requirements/evidence:** model contracts and sources are traceable; assumptions/limits are labelled.
B. **Configuration:** inputs validate before run; IDs, units, CRS, timestamps, defaults, references are explicit; invalid input fails closed.
C. **Modules:** applicable WB/BB/adversarial/reference/regression tests pass; physical/accounting invariants and randomness are tested.
D. **Integration:** SUMO/ns-3 versions and smoke tests recorded; clock/route/packet/entity correlations validated; collection-only mode tested; failures isolated.
E. **Data/statistics:** raw output complete and unit-labelled; metrics have definitions/reference fixtures; analysis plan, diagnostics, effect sizes, uncertainty, exclusions recorded.
F. **Portability/UI:** each claimed platform setup works; UI controls map to versioned JSON and defaults are visible.
G. **Release report:** exact commands/exit codes, tests not run, limitations, known issues, and recovery instructions disclosed. No critical gate is silently waived.
