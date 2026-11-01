# ADR-0012 — Isolated SUMO installation and API smoke

- Status: Accepted
- Date: 2026-11-01
- Related sprint(s): S019
- Decision authority/method: owner-authorized self-audit, ADR-0005; qualified
  installation choice, test/CI/integration gates still mandatory.

## Context

S018 locks development tools but introduces no simulator. S019 requires an actual
SUMO executable and compatible Python API. System SUMO1.27.1 is an observation,
not an accepted project pin. Legacy dependencies/source are not reused.

## Options considered

An unpinned system executable can drift independently of bindings. Installing
SUMO into the development venv would mix tooling and simulator dependencies.
Building the full source now adds an unnecessary toolchain and resource burden.
Using only version strings would omit a real API compatibility observation.

## Decision

Select SUMO1.28.0 with matching eclipse-sumo, sumo-data, traci and sumolib wheels,
all exact pins with public PyPI SHA256 metadata. Keep a separate isolated simulator
venv, using S018's interpreter. Initial supported installation profile is Linux
x86_64/glibc2.28+ only. Do not replace system executables or add packages to S018.
Version checks, imports, API protocol handshake and clean close are installation
smoke only. Use a tiny generated empty network; never advance simulation time or
claim traffic/collection/physical behavior. Explicit diagnostic fixture values are
not calibrated scenario parameters. No legacy archive content is involved.

Extend S018's scoped lint/type coverage to the new smoke module and its unit tests
(Ruff) and smoke module (strict mypy). Interpreter/tool versions stay unchanged.
S017 Windows/WSL/native runtime and later integration/replay gates stay open.

## Evidence and assumptions

Primary sources accessed2026-11-01:
[official downloads](https://eclipse.dev/sumo/docs/Downloads.html) supports wheel
installation; [TraCI interface](https://eclipse.dev/sumo/docs/TraCI/Interfacing_TraCI_from_Python.html)
describes connection and close; [FAQ](https://eclipse.dev/sumo/docs/FAQ.html)
requires matching client/server versions. Public PyPI1.28.0 release metadata lists
all selected package hashes and dependencies. Upstream
[versioned protocol constants](https://raw.githubusercontent.com/eclipse-sumo/sumo/v1_28_0/tools/traci/constants.py)
identify protocol22. These references support software choices, not physical validity.
Package metadata reports EPL-2.0 OR GPL-2.0-or-later; local dependency installation
is not a decision to redistribute wheel contents. Redistribution needs a separate
license/artifact review. No legacy reuse permission is granted.

## Consequences

Missing/wrong executables, bindings, protocol, platform or interpreter fail visibly.
Private generated network/logs and installed binaries are excluded from Git.
Only sanitized hashes/versions/status receipts are published. Bounded smoke commands
must terminate subprocesses on failure. Locks describe a single initial profile;
other platforms are NOT_RUN, not inferred from available wheels.

## Validation and revisit conditions

Run actual clean install plus API handshake/close, negative mismatch/missing path
checks, generated version properties, timeout/invalid receipt regressions and all
prior tests. Verify exact-head CI before integration. Revisit on dependency updates,
platform evidence, API changes or future model/integration requirements. Rollback
through reviewable commits, never replace unrelated user environments or history.
