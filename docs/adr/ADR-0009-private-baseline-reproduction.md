# ADR-0009 — Private baseline simulation reproduction

- Status: Accepted
- Date: 2026-10-25
- Related sprint(s): S012
- Decision authority/method: explicit owner yes to two bounded private simulation runs, with one corrective retry each
- Replaces: ADR-0007 normal-simulation prohibition only for this exact bounded exception

## Context
S011's validation-only audit is accepted. S012 asks for baseline reproduction, which
uses the normal simulation entrypoint excluded from the owner's approved exception.
Administrator access resolves sandbox setup, not this different execution scope.

## Options considered
Stop with a precise blocker; falsely infer permission from generic continuation;
or prepare a concrete bounded plan and seek explicit authority. Choose the last.

## Decision
Owner authorizes the exact hash-bound S012_BASELINE_EXECUTION_REVIEW.json
plan (SHA-256 5a8ef0be672f616bd9c40e68db4ea431e82dbb54c7dcea3ac31dd18bfb893187)
and unchanged existing private audit build/inputs for two private baseline runs,
with at most one retained corrective retry each. No additional source copying,
patching, source integration, historical campaign replay, training or redistribution.
Limits and prerequisites are explicit in the plan and S012_BASELINE_REVIEW.md.
Owner scope authority is received; no launch until all technical gates pass.

## Evidence and assumptions
S011 source/inputs/binary hashes and actual sandbox evidence remain traceable.
Two authorized normal attempts are now recorded in E-S012-03: both exit 3,
route incomplete; raw event replay differs. No successful baseline is accepted.
The unchanged static review JSON retains its historical NOT_RUN fields. The one summary projection exclusion is preregistered from
source-bound host-clock use; raw artifacts and all differences remain retained.
Third-party provenance/licensing limits still prohibit reuse/redistribution; no
scientific equations/parameters or physical validity are accepted by private replay.

## Consequences
B-S012-01 is closed by the explicit owner response. Evidence checker and
synthetic tests can proceed without executing legacy code. S012 remains incomplete,
and S013 cannot start. Preparing a plan or passing metadata tests is not authority.

## Validation and revisit conditions
Owner authority is bound to the unchanged review-plan hash; require tested bounded output exporter,
actual runtime enforcement probes, verified identities/dependencies, two run records
or genuine failed-reproduction evidence, required negative tests and exact-head CI/
permitted integration. Stop and retain evidence on any failure. Any broader scope,
new source/input hash or budget change needs a documented decision before use.
