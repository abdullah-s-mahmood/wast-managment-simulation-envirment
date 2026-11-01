# S017 — Supported platform matrix (IN REVIEW)

## E-S017-01 — platform targets and scoped acceptance plan, 2026-11-01

Basef862fd188d75ca9c8d15c8131e63554c2680a4ef; branch sprint/S017-platform-matrix.
Fetched latest, inspected both worktrees and read governing state/contracts.
S016 source PR40 head0b45478cf6b5ca4359352f86138c7fb9bb1f0805 passed
CI41155020470, merged0d8fd9ba54a73dc1c4c19b62adf4f26360dd8a0d;
acceptance PR41 heade72523f1524fa4fc58d42f5746542aa3069ed3ae passed
CI41155148323 and merged current base. S001–S016 accepted16/88; S017 next,
no competing work/completion found. Original checkout at reviewed main with only
untracked .vscode; isolated worktree preserved. No source archive/legacy run touched.

Gap/plan: no explicit target priority/runtime/evidence matrix existed. Define
required Linux and Windows/WSL2 tuples, best-effort native Windows, dependency
installation/verification routes, scoped evidence and later acceptance gates.
Never infer Windows parity from Linux, pin private-audit tool versions as new
runtime dependencies or call a planning matrix verified simulator support.

ADR-0010/D-0014 accepts target planning only. Required: Ubuntu24.04 x86_64 Linux;
Windows11 x86_64 with WSL2/Ubuntu24.04 guest. Best effort: native Windows11 x86_64
MSYS2/MinGW64. Architecture/toolchain alternatives remain unplanned. The matrix
lists seven dependency routes per target (Git/Python/C++/CMake/build driver/SUMO/
ns-3), source URLs/access dates and verification routes. Version pins null;
installation, adapter, replay and Windows gates NOT_RUN. Only a sanitized local
Linux host probe passes its own scope; zero verified simulator targets.

Primary vendor docs opened2026-11-01: ns-3 overview/Linux/Windows installation,
SUMO Installing, Microsoft WSL, CPython Unix/Windows and Git installation. Links
and interpretation boundaries in ADR/README/matrix. Version-specific examples are
not copied as accepted release locks. No source-derived scientific model accepted.
No dependency/Windows feature installed; host restart/paid resource not invoked.

Files: independently authored scripts/validate_platform_matrix.py; ten synthetic/
CLI tests in tests/test_platform_matrix.py; ADR0010; matrix/host-probe/README in
docs/platforms; CI matrix-check step; inventory/decision/progress/handoff/blocker/
validation/report records. Public JSON contract v1 affects governance/setup only,
no scientific equation, scenario, runtime state or legacy behavior changes.
No external dependency added. check_change declaration uses changes_public_contract
true, other material flags false, ADR-0010 with qualified planning rationale.

Actual platform observation (host_probe only): /etc/os-release Ubuntu24.04.5 LTS,
IDubuntu/VERSION_ID24.04; platform Linux/x86_64/kernel7.0.0-38-generic;
Python3.11.15. This is observed tooling, not a selected S018 interpreter. Kernel/
OS evidence does not identify a Windows host/WSL pairing or prove hardware/native
execution context. Receipt publishes no hostname, credentials or local paths.

Commands/results:
- `git fetch origin`, status/worktree/log inspection: exit0; clean isolated tracked
  tree before work, original .vscode retained. Progress16/88/S016 completed verified.
- `python scripts/validate_platform_matrix.py probe`: actual exit0; sanitized
  S017_LINUX_PROBE.json, UTC observation metadata, HOST_OBSERVATION_ONLY.
- `python -m unittest discover -s tests -p test_platform_matrix.py -v`: initial9
  tests exit0. Added stronger receipt-relabel attack:10 tests exit1/one failure;
  simply changing platform_id while keeping Linux observations could pass as a
  Windows receipt. Preserved exact failing process transcript under private Git
  metadata private-evidence/S017/relabel-attack-before-fix.log.
- Fixed receipt schema/observed OS/distribution/architecture/kernel cross-check;
  v1 host receipts limited to actual Linux observation vocabulary. Same10 tests
  exit0. No real Windows claim published before correction. No test weakened.
  Retained tests reject Linux-to-Windows ID reuse, relabelled Linux profile, host-
  probe-as-adapter/replay evidence, wrong tuples, missing/duplicate dependencies,
  guessed versions, support/status promotion, bad artifact hashes/private paths.
- WB: route/target/priority completeness and explicit NOT_RUN gates. BB CLI check
  from another CWD needs no simulator/private archive.100 seeded permutation cases
  preserve target/route invariants and zero runtime support. Synthetic non-Linux
  host remains UNCLASSIFIED, not automatically assigned Linux evidence.
- `python -m unittest discover -s tests -v`: final195 tests exit0,6.470seconds
  (all185 prior plus10). Earlier194 suite passed before stronger attack; it is
  retained as historical, not final proof. Tests establish plan/provenance software
  behavior, not physical validity or target ABI/install compatibility.
- `python scripts/validate_platform_matrix.py check docs/platforms/S017_MATRIX.json`:
  actual exit0; VALID_PLATFORM_PLAN_UNVERIFIED_RUNTIME, three targets/two required,
  zero verified simulators, later platform gates OPEN, versions UNSELECTED.

Linux governance is executed, not full simulator/platform integration. Windows
host/WSL2/native install/build/smoke, target-specific ABI/paths/clocks/adapters/replay
are NOT_RUN. Their real gates remain open for S018–S024; no unavailable platform
accepted as supported merely to finish S017. This sprint accepts a target plan,
not their runtime readiness. Existing POSIX audit tests remain intact.

Private evidence Git common metadata private-evidence/S017 contains original
failure/final regression transcripts; host receipt and matrix are sanitized public
artifacts. Legacy archive/source/private baseline not opened or executed. Frozen
AUDIT-FREEZE-001 remains valid; scientific models UNVALIDATED/reuse PROHIBITED,
S015 findings open. No independent reviewer fabricated or protection bypass.

S017 not_started -> in_progress on planning -> in_review after local plan/test/
governance checks. Count stays16 until exact-head CI/permitted integration and
acceptance records. Final validators/change declaration and head CI still need
recording. S018 not_started; no dependency-lock work begun out of order.
