# ADR-0010 — Platform targets and evidence boundaries

- Status: Accepted
- Date: 2026-11-01
- Related sprint(s): S017
- Decision authority/method: owner-authorized author self-audit under ADR-0005;
  acceptance limited to target planning, subject to exact-head CI/integration.
- Replaces / superseded by: none

## Context

The source audit is frozen. The new environment needs explicit OS/architecture
and runtime boundaries before dependency locks/installations. A Linux test result
cannot establish Windows support. Existing audit helpers include POSIX operations;
this decision does not declare them natively portable or weaken their tests.

## Options considered

Linux alone would omit the planned Windows workflow. Native Windows/MSVC alone
would conflict with documented ns-3 constraints. Requiring every optional platform
now would conflate planning with installation and expand scope. Defer all targets
would leave later environment gates undefined.

## Decision

Require Ubuntu 24.04 x86_64 and Windows 11 x86_64 with Ubuntu 24.04 under WSL2 as
release-validation targets. Native Windows 11 x86_64/MSYS2 MinGW64 is best effort.
Other tuples are unplanned until a new decision. This selects planned workflows;
it verifies no simulator target and pins no dependency release. S018–S024 retain
their own selection/build/smoke/adapter/replay gates. Windows host/guest and native
Windows remain separate identities with separate evidence.

The version1 matrix is a historical planning contract, not runtime configuration.
Do not rewrite its NOT_RUN fields as later success or silently inherit legacy audit
versions. Later qualified readiness evidence/locks get their own versioned records.
Consumers: platform-plan validator/tests, CI/governance and later setup sprints;
no current simulation API or scientific model behavior changes.

## Evidence and assumptions

Primary documents inspected 2026-11-01: [ns-3 overview](https://www.nsnam.org/docs/installation/html/overview.html),
[Linux prerequisites](https://www.nsnam.org/docs/installation/html/linux.html),
[Windows routes](https://www.nsnam.org/docs/installation/html/windows.html),
[Microsoft WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install),
and [SUMO installation](https://eclipse.dev/sumo/docs/Installing/index.html).

The guides document Linux builds and Windows WSL/MSYS2 routes. Their commands and
requirements are release-specific; this is not verification of our integration.
Project choice: use WSL2 as the required Windows runtime route, with native MSYS2
optional. WSL emulation features are outside this plan. No MSVC/ns-3 compatibility
or cross-platform stochastic replay is inferred. Host setup was not executed.

## Consequences

The required Windows workflow has an explicit Linux guest, not a claim about
native Windows binaries. Windows-host filesystem/process/clock/path behavior still
needs independent tests. Native toolchain/interpreter ABI boundaries must be
verified before optional native integration. Missing target evidence remains NOT_RUN
and cannot establish support; no unavailable platform gate is waived.

No paid VM, host reboot, Windows feature change, legacy execution or dependency
installation is performed by this planning sprint. Rollback: reject/supersede this
planning record through a focused ADR, preserving source evidence and test results.

## Validation and revisit conditions

Validate every target's install/verification routes; reject cross-platform/scope
receipt substitution and support/version promotion. Host observations have exact
platform/scope identity and artifact hash. CI validates the plan only, not all
runtime targets. Revisit on actual release/toolchain incompatibility, target access,
new required architecture, binding/ABI choice or changed Windows workflow needs.
All runtime readiness and scientific validity claims require their actual gates.
