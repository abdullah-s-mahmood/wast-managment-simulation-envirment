# ns-3 installation/build smoke — S020

This contract verifies a fresh Linux x86_64 C++ core build, toolchain/cache
configuration and minimal linked execution. It does not validate packets, radio/
propagation/traffic models, a Python binding, coupling, empirical accuracy, replay
or a full simulator target. Windows/WSL/native installation is NOT_RUN.

## Source and toolchain

ADR-0013 selects the published ns-3.47 mainline source archive, not allinone or a
claim of the latest release. Official HTTPS download/publisher SHA1 agree. The
profile additionally pins full size42929716bytes and observed SHA256
8b3adca956c834ea436b915986ab8fd053e90041acae7426895d595aaa3ccc39.
The publisher SHA1 is a weak checksum, not a signature; locally computing SHA256
adds reproducible identity, not independent authentication or scientific evidence.

Versioned3.47 release notes require GCC11.1+, Python3.10+ and CMake3.20+.
This project chooses Ninja>=1.10 as its smoke-contract floor (not an asserted
upstream requirement), GNU g++ and S018 isolated CPython3.12.16 for orchestration.
Actual local tools: GCC13.3.0, CMake3.28.3, Ninja1.11.1, Ubuntu24.04.5/glibc2.39.
Record actual versions on every build; no bitwise equivalence across toolchains
or machines is promised. No global tool/package is replaced by the helper.

## Fresh setup and observable result

Install the target's compiler/CMake/Ninja through its normal trusted route if absent,
then prepare S018 first. Choose a new owned parent (paths may contain spaces/Unicode):

```bash
wm_ns3_parent=$(mktemp -d)
curl --fail --location --proto '=https' --max-time 180 --max-filesize 67108864 https://www.nsnam.org/releases/ns-3.47.tar.bz2 --output "$wm_ns3_parent/ns-3.47.tar.bz2"
.venv/bin/python -I scripts/ns3_smoke.py --archive "$wm_ns3_parent/ns-3.47.tar.bz2" --work-dir "$wm_ns3_parent/build-evidence"
```

Explicit --cxx/--cmake/--ninja paths are available; defaults are the standard
/usr/bin paths above. Missing tools fail actionably without selecting alternatives.
Existing/dangling/symlinked work locations and stale caches are refused, not cleaned.
An ambient home .ns3rc is refused pending review; no user config is deleted.
Child Python/build/include/library/NS3 override variables are stripped, tool argv
are explicit, and no shell command is assembled from profile data. This is not a
host sandbox or attestation against arbitrary host/tool/source tampering.

Full archive size/SHA256 is checked before extraction, again before compilation
and after execution. Only that independent upstream release is eligible, never the
designated legacy archive. Preflight rejects foreign/traversal/duplicate/special
members; data-filter checks keep links inside the destination. Preserve all errors.
The verified release has3878 members/99928794 declared bytes/two links. Bounds:
20000 members,32MiB/member,512MiB cumulative,120s header preflight; extraction uses
Python's data filter. The accepted source hash binds those trusted dependency bytes.

CMake configures core only, Release/Ninja/two build jobs, explicit source/compiler/
build/output directories. Examples/upstream tests/Python bindings/build-version
embedding/ccache/precompiled headers/visualizer/GSL/SQLite/Eigen are OFF. Cache checks
verify source/compiler/modules/type and all those BOOL options, rejecting unused
or contradictory settings. Features of disabled modules are not runtime evidence.
Building uses target core; no contributed/network module is executed.

The independently written tests/fixtures/ns3_installation_smoke.cc compiles against
fresh generated headers/core library with C++20 and explicit runtime library path.
It schedules exactly one event1ns later, runs/destroys the scheduler and prints
an exact1ns result twice. This is a hand-calculated integer-time API/linkage check,
not physical calibration or project scheduler implementation. --negative-exit
intentionally returns7 before scheduling, solely to test command-status propagation.
The orchestration records nonzero/timeout as failure and preserves command/logs.

Wall limits: configure120s, build600s, other commands10s; two compiler jobs.
The helper requires512MiB remaining disk before extraction, not a promise of peak
space use on all systems. Commands have a separate Linux process group; timeout
kills the process group and reaps its direct child, retains logs and records TIMED_OUT_KILLED_REAPED.
This is trusted dependency tooling, not an untrusted-code resource sandbox.

## Evidence, limitations and updates

Private work retains archive/source/cache/generated artifacts/tool versions,
command argv/exit/duration/logs and both raw probe results. Public receipt contains
sanitized source/library/fixture hashes, actual tool versions, exact result and
NOT_RUN/UNVALIDATED flags; private paths are never published. Source LICENSE says
mostly GPLv2-only with component exceptions. No dependency implementation/binary
is committed or redistributed; review packaging/license obligations separately.
The designated legacy baseline remains unchanged and prohibited for reuse.

The installation gate runs only the independent probe, not the full upstream test
suite. Those tests and Python bindings are explicitly NOT_RUN; no claim is made
about their correctness/readiness. Later adapters/models/platform/replay acceptance
need their own requirements/evidence. Source/tool/profile/fixture/scope changes need
an ADR, full relevant checks and actual exact-head CI/permitted integration.

Primary sources accessed2026-11-01: [release](https://www.nsnam.org/releases/ns-3-47/),
[publisher download/checksum](https://www.nsnam.org/releases/ns-3-47/download/),
[versioned requirements](https://gitlab.com/nsnam/ns-3-dev/-/blob/ns-3.47/RELEASE_NOTES.md),
[subset guidance](https://www.nsnam.org/docs/release/3.44/manual/html/enable-modules.html),
and [installation approach](https://www.nsnam.org/docs/installation/html/quick-start.html).
The versioned release requirements take precedence over older generic guide minima.
