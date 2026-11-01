# SUMO installation smoke contract — S019

This is an installation/API smoke for Linux x86_64 with glibc>=2.28 and the
S018 isolated CPython3.12.16 environment. It does not verify a full simulator target,
traffic dynamics, empirical accuracy, collection policy, coupling or replay.
Windows/WSL/native installation is NOT_RUN and S017 runtime gates stay open.

## Independent profile and installation

ADR-0012 selects eclipse-sumo, sumo-data, traci and sumolib, all1.28.0. The JSON
profile records the four exact wheel URLs, compressed sizes and SHA256 digests
from public PyPI metadata. The requirements file must agree byte-for-byte with
those pins/hashes. This is separate from pyproject.toml/uv.lock: simulator packages
must not be installed in the development .venv or supplied by global packages.
The observed system SUMO1.27.1 is deliberately not accepted by this profile.

Prepare S018 first, then choose a new owned parent and nonexistent prefix/work-dir:

```bash
wm_sumo_parent=$(mktemp -d)
.venv/bin/python -I scripts/sumo_smoke.py --install --prefix "$wm_sumo_parent/venv" --work-dir "$wm_sumo_parent/installation-evidence"
```

The command validates the platform/profile, requires isolated pinned Python,
checks the S018 uv manager version, creates a standard-library venv and runs pinned
uv pip sync with only binary wheels, require-hashes, no cache/config, and explicit
public PyPI. It strips inherited Python/PIP/UV/active-environment/SUMO_HOME and
alternate-binding overrides. Existing prefixes are refused rather than repaired
or deleted. Failed partial installations and evidence remain for inspection; use
a separately reviewed fresh owned location for a later attempt.

To smoke a previously prepared dedicated environment, omit --install and choose
a fresh evidence directory. Existing evidence directories are never overwritten.
All paths are explicit argv elements: no shell assembly or ambient executable
lookup. Spaces and Unicode paths are supported by the tested Linux route. Venv
Python may point to the pinned base interpreter; the worker checks exact Python,
isolated startup, venv prefix and binding module locations before API use.

## Observable checks and limits

The smoke verifies the SUMO stable first-line version, all four installed package
versions, in-venv TraCI/sumolib imports, client protocol22, a real server getVersion
response with protocol22/release1.28.0, and successful close/exit. stdout is a
sanitized JSON receipt with profile hash and executable entry-point hash (a console
wrapper hash is not claimed to be the native engine's hash). Installation hashes
identify wheel bytes. No receipt is a security clearance or model validation.

The worker uses netgenerate to create a diagnostic empty2x2 grid,100m spacing,
1 lane,10m/s diagnostic speed setting and seed19. These explicit JSON values are
installation fixtures, not calibration or adopted scenario parameters. Other
netgenerate internals are upstream defaults, not accepted project model choices.
TraCI connects over local127.0.0.1 to an ephemeral port, queries version and closes;
**no simulationStep call** or scientific measurement is made. This is not a network
namespace/security sandbox; do not use it to execute untrusted archives/binaries.
A concurrent port bind or protocol failure rejects the attempt, not a partial pass.

Profile budgets are wall-clock seconds: installation300 per installation command,
version/network command10, worker20, socket/close3. Profile validation caps setup
at600 and other budgets at60 seconds; invalid/non-integer/boolean budgets fail.
The Linux worker has its own process group: timeout kills/reaps that group and
preserves captured diagnostics. Worker finally kills/reaps a still-running SUMO.
Trusted small generated outputs are retained privately; this is not an untrusted
archive parser or a guarantee against arbitrary host/package tampering.

Private evidence includes generated network, installer/version/generator/server
logs and worker receipt/stdout/stderr. Failure records are FAILED_NOT_ACCEPTED.
Do not publish absolute paths, host data or raw legacy results. Public evidence
contains only sanitized versions/hashes/test outcomes and disclosed limitations.

## Provenance and future changes

Primary sources accessed2026-11-01: [official download/install route](https://eclipse.dev/sumo/docs/Downloads.html),
[TraCI connection/close API](https://eclipse.dev/sumo/docs/TraCI/Interfacing_TraCI_from_Python.html),
[client/server version guidance](https://eclipse.dev/sumo/docs/FAQ.html),
[versioned protocol constant](https://raw.githubusercontent.com/eclipse-sumo/sumo/v1_28_0/tools/traci/constants.py),
and [release metadata](https://pypi.org/project/eclipse-sumo/1.28.0/).
PyPI metadata reports EPL-2.0 OR GPL-2.0-or-later for all four packages; no third-party
source/binary is committed or redistributed by this sprint. Review redistribution
obligations separately before any packaging. The designated legacy archive remains
unchanged, private, scientifically unvalidated and prohibited for source reuse.

Release/profile/scope changes need an ADR and all relevant tests, real installation
smoke and exact-head CI. Future simulator adapters/dynamics remain separate sprints.
