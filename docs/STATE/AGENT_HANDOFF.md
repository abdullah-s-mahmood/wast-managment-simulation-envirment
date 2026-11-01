# Agent Handoff — S020 accepted;20/88 complete

2026-11-01: S001–S020 completed. PR48 initial5bc7efb3 failed CI41289914827 at
missing default tool path; retained/corrected. Final3351c47e01f1342c652b55c3e23ee17254d1e872
matches local7d940041 tree65c206b9f4be38a937b040e6ad7666dc73d7373b.
Exact-head CI41290178155 all steps success including actual fresh core build and
both1ns runs; expected-head merge3559650a1102ec8cbc27c36b92a416741476cd8d.
Acceptance records still require own CI/integration before starting S021.

Read S020_REPORT/ADR0013/profile/setup/receipt. Independent ns-3.47 archive hash/
size verified; fresh core-only Release build with explicit tool/cache/disabled
feature checks and independent C++ reference probe.242 tests/Ruff/strict mypy3
files pass; all229 prior tests retained. Local GCC13.3.0/CMake3.28.3/Ninja1.11.1;
CI GCC13.3.0/CMake3.31.6/Ninja1.13.2 via explicit installed paths. Native library
hashes differ; root cause unknown, no binary-replay claim. Source/fixture hashes
match and exact1ns software outputs pass. No physical/network model validated.

Original IDE worktree ff-synced through accepted S019, .vscode file hash unchanged;
all checkpoint branches preserved. Task-owned regenerable caches only cleaned;
installed environments/archives/evidence/user data preserved. Disk headroom limited;
avoid unnecessary duplicate builds/simulations. Private Git common metadata
private-evidence/S020 stores full source/build/negative/failed+passed CI logs and
integration receipt; codex-s020-toolchain.json locator, never publish path values.

Next: integrate acceptance records after exact-head CI, fetch/read complete S021,
then execute it alone. Upstream suites/Python bindings/other modules/Windows/WSL/
native/adapter/full simulator/scientific/replay gates OPEN/NOT_RUN. Science
UNVALIDATED/source reuse PROHIBITED. No legacy archive/source/run touched.
