# ADR-0007 — Bounded private validation authority

- Status: Accepted
- Date: 2026-10-25
- Related sprint(s): S011
- Decision authority/method: explicit owner response “yes” to the scoped execution question; self-audit under ADR-0005
- Replaces: ADR-0006 execution/copy prohibition only for the exact exception below

## Context
S011 static tracing is complete but its actual runtime adversarial gate is NOT RUN.
The owner answered yes to isolated private build and five validation-only cases in
the prepared plan, explicitly retaining archive immutability and no simulation or
redistribution. This authorization persists across sessions.

## Options considered
Retain an authorization blocker; interpret approval as unrestricted execution; or
record the exact bounded exception. Only the last matches the owner's response.

## Decision
Authorize private disposable preparation of exactly the 32 native/build text entries
and three inputs listed in docs/audit/S011_EXECUTION_REVIEW_PLAN.json, SHA-256
6a3ee7bc8ae61c8d1060fd9a197e012d9e680f1387e2dd787988b267f2960a41.
Copies must be outside the implementation repository and archive, verified against
accepted member hashes. Build only fresh sw_cosim with trusted dependencies using
the two commands in that plan. Execute only ABS_A, ABS_B, REL_A, REL_B and
MISSING_CITY. No archived binaries, scripts, dependencies, links, nested archives,
historical results, source patches, full simulation, source reuse or redistribution.
Build limits: wall/CPU 300 s, address space 1 GiB; each of at most five validation
cases: wall 10 s, CPU 5 s, address space 256 MiB. Require verified network isolation,
read-only binary/inputs/CWD, private logs and denial of child execution before target
execution. No unsandboxed fallback or host security-policy changes are authorized.

## Evidence and assumptions
Owner response applies to the immediately preceding scoped question. The original
static packet remains unchanged with historical false/NOT_RUN fields; it is not an
execution record. LEGACY-CANDIDATE-001 remains 487062036 bytes at SHA-256
da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8.
Identity was reverified; checksum is neither security nor scientific clearance.
Dependency provenance/licenses and sandbox enforcement must still be verified.

## Consequences
B-S011-01 is resolved by owner authority. Technical prerequisites can still block
execution; do not ask again for this same exception. No legacy files were prepared,
built or executed during the current failed isolation preflight. Scientific models
remain unvalidated and source reuse/redistribution prohibited.

## Validation and revisit conditions
Retain actual commands, failure diagnostics and NOT_RUN cases. Complete S011 only
after mandatory tests, exact-head CI and permitted integration. Stop on isolation,
identity, dependency/license or resource failures. Broader execution needs a new
explicit decision. See E-S011-04 and B-S011-02 for current technical evidence.
