# S020 — ns-3 installation and version smoke test (COMPLETED)

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

## E-S020-05 — retained CI failure and explicit runner tool paths

PR48 initial head5bc7efb3b349df6a9c3bbf328d8892a2d9d7d9ce/tree7c60f746 matches
local9124c180. Exact-head CI41289914827 fails at ns-3 step exit1 before extraction/
configure/build: a requested default /usr/bin build-tool path is absent. All242
regressions (4.394s), lint/strict types/governance/SUMO smoke passed on that run;
this partial success is NOT overall CI acceptance. Original generic diagnostic
does not identify which tool, so no specific missing tool is invented. Full75,174byte
job log retained privately as ci-41289914827-failed.log, job124798829671.
Runner observation Ubuntu24.04.5/image20261025.353.1, not a platform mismatch claim.

Moved in_review -> in_progress for investigation. Correction: CI pins ubuntu-24.04
consistent with S017 and explicitly resolves/logs installed g++/cmake/ninja with
command -v, passing those paths through existing --cxx/--cmake/--ninja contract.
The helper retains fail-closed requested/default paths; missing-tool error now
names the basename without leaking private path. No compiler/version/source/budget/
warning/test gate relaxed. Source/fixture/build flags unchanged; no unnecessary
local rebuild. Local `.venv/bin/python -I scripts/python_environment.py check`
again exits0/242 tests/Ruff/strict mypy3 files after correction. State returns to
in_review for new exact-head CI; old failed head is not accepted or silently rerun.
ADR0013/setup/handoff/log document the correction. Source PR remains unmerged.

## E-S020-06 — corrected exact-head CI, integration and qualified acceptance

PR48 final head3351c47e01f1342c652b55c3e23ee17254d1e872 matches local
7d940041c559ed4f8b1ef5499a5c04bbd9df64cb at tree
65c206b9f4be38a937b040e6ad7666dc73d7373b (fetched/verified). Exact-head
CI41290178155 completes success, all242 tests/lint/strict types/governance/SUMO
smoke plus real fresh ns-3 core build/compile/two1ns runs. Source PR48 permitted
expected-head merge3559650a1102ec8cbc27c36b92a416741476cd8d.

CI logs actual explicit tool paths /usr/bin/g++, /usr/local/bin/cmake,
/usr/local/bin/ninja and versions GCC13.3.0/CMake3.31.6/Ninja1.13.2. This confirms
why assuming all runner tools lived under /usr/bin was unsound; the original generic
failure log remains uninterpreted as to which check first failed. Full corrected
job log124799607348 retained as ci-41290178155-success.log and sanitized receipt.
CI source/fixture SHA256 match local, reference runs pass. CI core-library hash
6888f176f7f3383c5145b6cabb7096538ad9ee8852bc4085d6bf6166c1196279 differs from
local4b66465a...; root cause NOT_ESTABLISHED, no causal attribution or normalization
invented. Bitwise binary equivalence is not this gate; different actual tool versions
are recorded, functional software probe only. No replay/physics acceptance inferred.

Author self-audit accepts S020 installation/compiler/build/minimal-run scope under
ADR0005, not an independent review. No protection bypass/fake approval. All objective,
WB/BB/adversarial/property/reference/integration/regression and documentation gates
have evidence; no hidden critical blocker. Failed initial CI preserved and corrected,
not waived. Upstream suite/Python bindings/other modules/platforms and full simulator/
scientific/replay gates remain NOT_RUN/OPEN. Source reuse PROHIBITED.

20/88 completed; next S021 only after this focused acceptance-record PR also passes
exact-head CI/permitted integration.18 source files changed: CI, inventory/state/
report/decision, ADR0013/setup/profile/receipt, tooling coverage contract/guards,
new ns-3 helper/13 Python tests/independent C++ fixture. No runtime model, source
reuse, global tool replacement or tool version/application dependency change.
