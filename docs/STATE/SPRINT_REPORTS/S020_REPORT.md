# S020 — ns-3 installation and version smoke test (IN REVIEW)

## E-S020-01 — recovery, requirements and independent source

2026-11-01 Linux x86_64 Ubuntu24.04.5/glibc2.39. S019 acceptance PR47 head
67e4f8d3c0145f483062af3508077e3f53e14cfd passed exact-head CI41288653151,
merged deb41307de0627e9fbaef268da4a852771ff2283. Fetched authoritative state;
read complete S020 contract, selected lowest eligible sprint. Branch
sprint/S020-ns3-installation-smoke from final accepted main.19/88 complete.
Original IDE worktree ff-synced to accepted main only after tracked-clean check;
its single untracked .vscode file's hash unchanged. All checkpoints preserved.

Gap/plan: no ns-3 compiler/build/minimal execution accepted. Choose versioned
upstream source, verify identity/requirements, build only core, compile independent
1ns linkage fixture, test missing compiler/stale cache/nonzero/error/resource paths,
record exact tool/config/source/results, then exact-head CI/permitted integration.
No network model/empirical/replay/full-platform claims. ADR0013/D0017 qualified.

Available disk initially1701015552bytes. Cleaned ONLY task-created S018/S019
regenerable uv caches through pinned uv cache clean: all5 commands exit0,
free space1835536384bytes afterward. Installed venvs/runtimes, source archives,
private failure/proof logs, original/user data preserved. Private cleanup receipt
records exact cache paths/commands; no private paths published. No global cleanup.

Official HTTPS source https://www.nsnam.org/releases/ns-3.47.tar.bz2 downloaded
with64MiB/180s bounds;42929716bytes in46.684s. Full SHA1 matches publisher
897c3f2db2c6de6a8291e46b3020dbeb1af75269; independent observed SHA256
8b3adca956c834ea436b915986ab8fd053e90041acae7426895d595aaa3ccc39 pinned.
SHA1 is weak/not a signature; local SHA256 is identity, not independent authenticity.
Source VERSION reads3.47; LICENSE says mostly GPLv2-only with component exceptions.
No dependency/legacy code or license text redistributed. Versioned3.47 notes require
GCC11.1+/Python3.10+/CMake3.20+; Ninja1.10 is project floor, not upstream claim.
Primary release/checksum/requirements/module-source URLs in ADR/setup contract.

## E-S020-02 — tests and resource/failure contracts

Tests written before module; initial import failure exit1 retained.12 direct tests
then exit0; scoped Ruff/strict mypy1 module pass. Expanded to all241 regressions,
Ruff PASS, strict mypy PASS3 source files; all229 prior tests retained unchanged.
Coverage:100 generated numeric-version comparisons, schema/boolean/budget/fixture
errors, full-size corrupt source hash, missing tool, stale cache preservation,
nonzero7/timeout killed-group/direct-child reap, override stripping, cache source/
compiler/modules/type/disabled BOOL options, exact integer1ns output (rejectfloat/
bool/partial/duplicate/clearance additions), traversal/duplicate/link/special/large
archive header attacks with no extraction. Source-fixture newline escaping found
and corrected during inspection before build; fixture hash updated explicitly.

All compile/build/profile settings are tooling/diagnostic controls, not hidden
scientific parameters. tests/fixtures/ns3_installation_smoke.cc is independently
written and explicitly checks1ns API behavior, never legacy implementation.
NS3 profile/scoped lint/type coverage extension authorized by ADR0013. No application
dependency/tool version/uv.lock changed. No network module is implemented.

## E-S020-03 — actual clean configure/build/compile/run and attacks

`.venv/bin/python -I scripts/ns3_smoke.py --archive ARCHIVE --work-dir WORK` exits0
in fresh private Unicode/space path. Exact actual argv/durations/exits/logs preserved
in first-build-command.json and each WORK/*.command.json; sanitized public receipt
in docs/tooling/S020_BUILD_RECEIPT.json. Tools: GCC13.3.0/CMake3.28.3/Ninja1.11.1,
S018 CPython3.12.16 orchestration. Preflight3878 members/99928794 declared bytes/
two links; data-filter extraction. Archive fully rehashed before extraction,
after extraction/before compiler and after execution; unchanged/full digest matches.
Only independent upstream archive used, designated legacy archive untouched.

Commands (private paths substituted here; exact argv retained privately), all exit0:
- explicit GNU g++ -dumpfullversion -dumpversion; g++ --version; cmake --version;
  ninja --version, min-version and compiler-family checks
- cmake -S SOURCE -B CACHE -G Ninja -DCMAKE_BUILD_TYPE=Release,
  explicit CMAKE_CXX_COMPILER/CMAKE_MAKE_PROGRAM/NS3_OUTPUT_DIRECTORY,
  NS3_ENABLED_MODULES=core, and all documented disabled options OFF;5.331s
- cmake --build CACHE --target core --parallel2;69.474s/68 build steps
- g++ -std=c++20 -IARTIFACTS/include FIXTURE LIBCORE -Wl,-rpath,LIBDIR -o PROBE;
  1.267s; links actual freshly built core, generated headers and explicit rpath
- PROBE twice, each0.004s, each exact statusNS3_CORE_SMOKE_PASS/event_time_ns=1

Actual cache checked against source/compiler/modules/Release; later stricter
verification also checks every disabled feature is a recognized BOOL=OFF and
passes on the same fresh cache. Build behavior/source/fixture unchanged; no
unnecessary local rebuild. Library/fixture hashes and individual tool/check exits
in public receipt. Actual missing compiler CLI exits1 actionably before building;
actual reuse of existing cache/work exits1 and preserves it. Linked PROBE
--negative-exit exits7; checked runner surfaces failure/retains command/log rather
than fabricating a pass. Negative-and-cache receipt retained; full archive SHA256
rechecked afterward, exit0. No attempt rerun until green or upstream source repair.

Scope exclusions: upstream suites, Python bindings, optional/network/contributed
modules, Windows/WSL/native and adapter/physical/replay readiness NOT_RUN/OPEN.
Only installation/linkage integer-time reference accepted locally; no scientific
model or complete simulator platform validated. Final governance/diff checks,
exact-head CI/permitted source integration and durable acceptance still pending.
S020 in_progress19/88; S021 untouched.

## E-S020-04 — final local gates and self-audit

Added public CLI regression rejecting global/non-isolated/unpinned orchestration
before dependency build. Final `.venv/bin/python -I scripts/python_environment.py
check` exits0:242 regressions PASS, Ruff PASS, strict mypy PASS3 source files.
13 S020 tests plus all229 previous tests retained; final quality log private.
The added orchestration/cache guards strengthen checks only; compile/source/fixture
behavior and observed positive build inputs are unchanged. Exact-head CI will
exercise the final guarded route in a fresh environment.

Each `.venv/bin/python -I` command exits0 (individual output/argv retained in
private final-validator-results.json and final-validator-0..6.log):
- scripts/validate_project_docs.py
- scripts/validate_repository_boundary.py
- scripts/validate_evidence_ledger.py
- scripts/validate_change_control.py
- scripts/validate_risk_protocol.py
- scripts/validate_audit_freeze.py docs/audit/S016_AUDIT_FREEZE.json
- scripts/validate_platform_matrix.py check docs/platforms/S017_MATRIX.json

Material-change declaration schema1/adds_dependency=true/changes_public_contract=true/
changes_science=false/irreversible=false/decision_id=ADR-0013 returns[]/exit0.
`git diff --check` passes. Self-audit scope: ns-3 helper/profile/receipt/setup;
independent C++ test fixture/13 Python tests; explicit lint/type coverage expansion;
CI/ADR/inventory/decision/state/report records. No binary/private paths/secrets or
legacy implementation committed. No physical parameter/model or application
runtime dependency introduced. Source-only tested installation controls, NOT_RUN
limits preserved. S020 in_review19/88; exact-head CI/permitted integration and
acceptance records remain mandatory before S021.
