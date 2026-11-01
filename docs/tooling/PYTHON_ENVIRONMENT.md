# Locked Python development environment — S018

This contract selects development tooling, not scientific runtime libraries or a
verified simulator platform. ADR0011 defines the qualified scope. Application
runtime dependencies remain empty. S017 Windows/WSL/native and future simulator/
adapter/replay readiness gates remain open; actual setup here is Linux only.

## Versions and files

CPython3.12.16 is the development interpreter, uv0.13.6 the manager, Ruff0.17.3 the
linter and mypy2.4.1 the type checker. unittest remains the complete test runner.
These choices are explicit in .python-version/pyproject.toml. uv.lock pins all
resolved transitive releases and SHA256 artifact metadata from public PyPI.
requirements-bootstrap.txt contains only the pinned uv wheel hashes from that lock.
The environment verifier checks their agreement. No private registry or source URL
may silently replace those lock sources.

The bootstrap interpreter needs Python3.11+ standard-library tomllib/venv support;
it is not the development interpreter and cannot run development checks as a
fallback. Python3.11, another patch, PyPy, global Python, user/system site packages,
non-isolated startup and unlisted environment packages are rejected by doctor.
A managed interpreter's executable SHA256 is reported to distinguish binary builds.
No scientific validity or cross-platform bitwise replay follows from this fingerprint.

## Prepare a fresh checkout

Install the target's standard-library venv support if absent. Choose a new owned
bootstrap directory outside the checkout; preserve any unrelated existing one.
On Linux/WSL, the reproducible bootstrap is:

```bash
wm_bootstrap_dir=$(mktemp -d)
python3 -I -m venv "$wm_bootstrap_dir"
"$wm_bootstrap_dir/bin/python" -I -m pip install --isolated --no-cache-dir --only-binary=:all: --no-deps --require-hashes --index-url https://pypi.org/simple -r requirements-bootstrap.txt
python3 -I scripts/python_environment.py sync --uv "$wm_bootstrap_dir/bin/uv"
.venv/bin/python -I scripts/python_environment.py doctor
.venv/bin/python -I scripts/python_environment.py check
```

Pinned uv must be bootstrapped; an old uv on PATH is not automatically upgraded.
CI uses the official setup-uv action pinned to an inspected commit and the same
manager release. No existing global Python or uv installation is replaced.

The sync mode ignores inherited Python/PIP/UV/active-environment overrides, selects
the exact managed interpreter and performs locked exact sync with source builds
disabled. Runtime/cache downloads stay in this checkout's Git common metadata;
packages stay in .venv. It uses sync rather than an explicit uv python-install
command, avoiding user-bin Python alias installation. No shell command is assembled
from model/config data. None of this accesses or executes the legacy archive.

Only a fresh .venv or one with this project's S018 ownership marker can be synced;
unknown environments and symlinks are refused. Exact sync can remove extraneous
packages from this managed environment. Doctor is read-only and never repairs it.
A failed partial preparation is not readiness: preserve its logs/prefix and inspect
before retrying; do not clear an unknown environment to get green output.

## Check scope and pollution defenses

All existing unittest tests run with isolated Python startup and an explicit trusted
project root. PYTHONPATH/user-site cannot supply missing dependencies. uv checks
that the environment exactly matches the lock in offline, check-only mode; no
package gets installed or removed by doctor. The venv must disable system sites.
This is dependency/isolation verification, not a sandbox or package-file attestation
against arbitrary host/venv tampering.

At S018 acceptance, Ruff covered scripts/python_environment.py and its tests;
strict mypy covered that tooling module only. ADR-0012/S019 extends Ruff to the
SUMO smoke module/tests and strict mypy to that smoke module. ADR-0013/S020 adds
ns-3 smoke module/tests to Ruff and its module to strict mypy (three source files). Scope and rules are checked as contract data;
weakening them requires an explicit revision. No old regression is skipped or
weakened. This is a declared initial lint/type rollout, not a claim that older
untyped governance code or future simulation modules have full static coverage.
New domain modules must add appropriate lint/type checks in their owning sprints.

The public source remains text only. .venv, manager binaries, caches and interpreter
builds are uncommitted development artifacts; private diagnostics use Git metadata.
Package lock metadata may list candidate wheels for other targets; that is not
execution or compatibility evidence for Windows/WSL/native/ARM platforms.

## Update, provenance and failure behavior

Change exact pins/lock only through a reviewed dependency/contract decision and
rerun clean setup, isolation attacks, lint/types/regressions and exact-head CI.
No floating update, --inexact or system-site fallback is part of this contract.
Timestamps identify real setup observations, not simulation time. Hashes identify
source/artifact bytes, not physical correctness or authentic empirical data.

Primary sources accessed2026-11-01: [CPython release](https://www.python.org/downloads/release/python-31216/),
[uv project sync](https://docs.astral.sh/uv/concepts/projects/sync/),
[managed Python provenance](https://docs.astral.sh/uv/concepts/python-versions/),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/),
[mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) and
[official CI integration](https://docs.astral.sh/uv/guides/integration/github/).
Actual selected package metadata and managed setup logs are retained separately;
release documentation alone is not our environment test evidence.
