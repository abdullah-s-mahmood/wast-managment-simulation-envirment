# ADR-0013 — Isolated ns-3 core build and execution smoke

- Status: Accepted
- Date: 2026-11-01
- Related sprint(s): S020
- Decision authority/method: owner-authorized author self-audit under ADR-0005;
  installation scope only, mandatory tests/exact-head CI/integration still required.

## Context

S019 installs SUMO separately; no ns-3 build has been accepted. Local GCC13.3.0,
CMake3.28.3/Ninja1.11.1 and S018 CPython3.12.16 are observed available. A full
simulator/module build would add unnecessary optional dependencies for this gate.
Disk space is limited; regenerable task-owned dependency caches were cleaned,
with installed environments, source archives, private evidence and user data kept.

## Options considered

An unpinned package or stale build directory obscures source/tool provenance.
Allinone adds contributed modules outside S020. A binary wheel alone omits the
required compiler/build evidence. Building all network models now is unnecessary.
Reusing any legacy source/build would violate the clean-room scope.

## Decision

Choose the published ns-3.47 mainline source release, not a claim it is the latest.
Official HTTPS source bytes match publisher SHA1; additionally pin the observed
SHA256/size. SHA1 is a weak publisher checksum, not a signature or physical evidence.
Keep dependency source/build/logs private, and extract only that verified independent
release using Python's data filter plus path/resource preflight. This is unrelated
to the designated legacy archive, which remains untouched/prohibited for reuse.

Pin CI to the S017 Ubuntu24.04 target. Discover its installed build-tool paths
and pass them explicitly; helper defaults remain fail-closed standard /usr/bin.
Build core only, Release, Ninja/two parallel jobs, explicit compiler and output
paths, no examples/tests/Python bindings/optional scientific libraries/ccache/PCH.
Document those exclusions; do not claim upstream test suites were executed.
Compile an independently written tiny C++ scheduler/linkage fixture against the
fresh library and run twice against an exact hand-calculated1ns expectation.
No packets, wireless/propagation/traffic models, coupling or empirical claims.
Existing build/evidence locations are refused, never cleaned or reused silently.

Extend scoped Ruff/type checks to this helper (and Ruff its tests), without
changing S018 releases/application dependencies. Windows/WSL/native/adapter/replay
and full platform gates stay OPEN/NOT_RUN.

## Evidence and assumptions

Primary sources accessed2026-11-01: [release](https://www.nsnam.org/releases/ns-3-47/),
[publisher download/checksum](https://www.nsnam.org/releases/ns-3-47/download/),
[versioned requirements](https://gitlab.com/nsnam/ns-3-dev/-/blob/ns-3.47/RELEASE_NOTES.md),
and [module subsets](https://www.nsnam.org/docs/release/3.44/manual/html/enable-modules.html).
Versioned3.47 notes require GCC11.1+/Python3.10+/CMake3.20+ (Clang alternative not
selected). Ninja1.10 is a project smoke-contract floor, not an upstream
minimum claim. Archive VERSION reads3.47; LICENSE describes mostly GPLv2-only with
component exceptions. No third-party implementation/license text is redistributed.
Actual hashes/build/cache/library/linkage checks must substantiate acceptance.

## Consequences

Each attempt records actual source/tool versions/configuration and preserves failed
logs. Matching hashes and passing software probes do not validate network physics.
This is not a hostile-host sandbox, reproducible-binary guarantee or redistribution
decision. Compiler/header/system-library variation remains observed environment
provenance. New platforms/modules/bindings need their own acceptance evidence.

## Validation and revisit conditions

Test wrong source/version, missing compiler, stale work/cache, malformed/bounded
profile, nonzero commands, timeout cleanup and deterministic output mismatch.
Verify a clean core build and actual fixture execution, retain all regressions,
require exact-head CI and permitted integration. Revisit release/toolchain changes,
scientific/dependency scope, build incompatibility or new platform evidence.
