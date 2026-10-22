# ADR-0005 — Risk-based sprint review

- Status: Proposed (inactive)
- Date: 2026-10-22
- Related sprint: S001; future procedural ownership S006–S007

## Context
AGENTS.md requires a focused PR, prohibits self-approval/self-merge and permits
completion only after accepted review. README requires a reviewed charter. Current
CI checks document structure only; it is not an independent acceptance mechanism.
The owner requested a proposal for routine autonomy without bypassing these rules.

## Options considered
1. Retain independent review for every sprint (current effective policy).
2. Permit bounded automated acceptance for low-risk changes after adoption.
3. Treat the implementing agent's audit as independent review (rejected).

## Proposed decision
After independent adoption and any required protection changes, classify routine
documentation/software changes as eligible only when they change no scientific
model, research method, security boundary, irreversible operation, resource
commitment or release authorization. All other work retains independent/owner
approval. Ambiguous classifications retain independent review.

Eligible changes would require passing sprint-specific tests and CI at the exact
reviewed commit, a separate reviewer identity that did not implement the change,
recorded findings/resolutions, and a durable acceptance record naming scope,
commit, test identities and reviewer. Automated reviews must be labelled automated.
The implementing agent cannot approve or merge its own PR. An independently
authorized integration mechanism must enforce repository protections. Material
changes invalidate prior review/checks. Failed or unavailable checks block acceptance.

## Evidence and assumptions
Authority: AGENTS.md sections 3–4 and README Start here. GitHub protections and
available independent reviewer identities must be verified before adoption; no
capability or reviewer is presumed available. This proposal grants no authority.

## Consequences and adoption
Current rules remain effective. Independent reviewers must approve this proposal
through a focused PR and explicitly adopt the corresponding AGENTS.md/procedure
changes before any automated acceptance. S001 remains independently reviewed.

## Validation and revisit conditions
Before adoption, demonstrate rejection of self-review, missing/stale/failed checks,
high-risk and ambiguous changes, and changed commits. Record reviewer separation
and protection evidence. Revisit after a misclassification or protection change.
