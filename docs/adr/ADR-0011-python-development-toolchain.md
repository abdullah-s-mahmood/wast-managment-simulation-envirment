# ADR-0011 — Isolated Python development toolchain

- Status: Accepted
- Date: 2026-11-01
- Related sprint(s): S018
- Decision authority/method: owner-authorized author self-audit under ADR-0005;
  qualified tooling decision, exact-head CI/integration still required.
- Replaces / superseded by: none

## Context

S017 defines targets but locks no versions. Current shell Python3.11.15 and system
Python3.12.3 are observations, not the selected development runtime. Setup must be
repeatable without global/user site packages or inherited package-index settings.
The existing195 regression tests use standard-library unittest.

## Options considered

Global pip installation would obscure isolation. A floating interpreter/package
set would not reproduce. A full scientific stack now would import unaccepted
future model/analysis choices. Keeping only compile checks would omit requested
lint/type tooling. Migrating every governance module's style/types in this sprint
would expand scope and risk accepted audit behavior.

## Decision

Select CPython3.12.16, uv0.13.6, Ruff0.17.3 and mypy2.4.1 for development tooling.
Use .python-version, pyproject.toml and uv.lock with exact direct pins and hashed
transitive artifacts. No application/runtime dependencies are introduced.
Create an isolated .venv through a pinned uv manager; exact locked sync, no system
site packages and no inherited private indexes. Do not replace global Python/uv.

Use unittest for the complete regression suite. Ruff and strict mypy initially
cover the new environment-verification module (and Ruff its tests), an explicit
rollout boundary rather than a claim that all older governance code is typed.
Do not weaken or skip the existing tests. Future domain modules must extend their
own lint/type coverage. Run project checks with isolated Python startup and an
explicit trusted project root, not ambient PYTHONPATH/user-site resolution.

## Evidence and assumptions

Primary sources inspected2026-11-01: [CPython3.12.16 release](https://www.python.org/downloads/release/python-31216/),
[uv Python management](https://docs.astral.sh/uv/concepts/python-versions/),
[locked/exact synchronization](https://docs.astral.sh/uv/concepts/projects/sync/),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/),
and [mypy getting started](https://mypy.readthedocs.io/en/stable/getting_started.html).
PyPI metadata independently reports the selected uv/Ruff/mypy versions. Direct
HTTP verification of the Python source artifact succeeds. uv-managed interpreters
are Astral builds, not a claim that CPython publishes this binary distribution.

The existing uv0.11.14 catalog lacks the selected Python patch, so install the
pinned manager privately before preparing the project environment. This is a
trusted development dependency, not execution/reuse of the designated legacy
archive. Interpreter/tool compatibility still needs actual clean setup/tests.

## Consequences

Updates require a reviewed pin/lock change and full relevant checks. Lint/type
coverage is scoped and never establishes scientific validity. Global packages
cannot supply missing declared dependencies; incompatible interpreter or polluted
environment must fail validation. Locked sync may remove extraneous packages from
its managed development environment, never unrelated user data.

Initial actual environment verification is Linux only. Windows/WSL/native readiness
is not certified here; S017 platform and future adapter/replay gates remain open.
No SUMO/ns-3 release or physical model is chosen by this Python-tooling decision.
Consumers are developer setup, environment checks/tests and CI; simulation APIs
and scientific configuration remain unchanged.

## Validation and revisit conditions

Verify clean setup from a fresh checkout, lock stability, isolated sys.path/user
site, exact interpreter/tools, and all existing regressions. Attack incompatible
Python, inherited indexes/PYTHONPATH and extra environment packages. Preserve
failures and fail closed, with no fallback to global packages or guessed versions.
Revisit on security/release requirements, upstream/tool incompatibility, new domain
modules, platform/ABI evidence or dependency additions. Rollback through a scoped
commit/ADR/lock revision while preserving evidence; no global environment reset.
