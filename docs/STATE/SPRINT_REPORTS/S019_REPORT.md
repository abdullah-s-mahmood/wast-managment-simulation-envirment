# S019 — SUMO installation and version smoke test (IN REVIEW)

## E-S019-01 — scoped installation choice and contract

2026-11-01, Linux x86_64 Ubuntu24.04.5. S018 acceptance PR45 head
1facb189e3fbba93650cf3303c6ab3c9e79a812f passed exact-head CI41287499046,
merged b5cff0f9b2711814ec9923002b29134f7831077d. Fetch/clean status and complete
S019 contract read before changes. Branch sprint/S019-sumo-installation-smoke.
S001–S018 accepted18/88; S019 in_progress, S020 untouched.

Gap/plan: installed system SUMO1.27.1 is not a project contract. Select a current
matching upstream release with source evidence; isolate it from S018 tools/global
packages; verify executable/imports/protocol handshake/close; attack missing/wrong
versions, malformed profiles, pollution, interrupted/bounded setup and artifact
claims. Keep minimal installation scope, zero simulation time steps.

ADR-0012/D0016 qualifies SUMO1.28.0, matching eclipse-sumo/sumo-data/traci/sumolib,
Linux x86_64/glibc>=2.28 only. Metadata from public PyPI1.28.0 endpoints provides
four wheel sizes/SHA256 values and dependencies. Profile/requirements agree exactly.
Observed metadata license expression EPL-2.0 OR GPL-2.0-or-later for all four;
no binary/source redistribution, legacy reuse or scientific acceptance. Primary
SUMO downloads/TraCI/FAQ and versioned protocol22 source linked in ADR/setup guide.
No equations, calibration or traffic model accepted. Installation fixture2x2/100m/
1lane/10m/s/seed19 is explicitly diagnostic, no simulationStep calls.

## E-S019-02 — tests, failures and actual installation smoke

Tests written first; initial import failure exit1 retained before implementation.
Initial10-test run has1 fixture error (missing companion requirements file), exit1;
correct fixture copies the actual companion input instead of skipping validation.
Corrected10 tests exit0. Full check with expanded installation guard passes223
regressions/lint/strict mypy2 source files. Later added negative tests initially
hit Ruff I001 import ordering, exit1 before tests; imports organized without
changing rules. Final full228 tests/lint/strict types exit0. Original212 tests
retained;16 SUMO tests include100 generated neighboring-version checks, bool/schema/
profile/hash/duplicate/budget attacks, foreign platforms/paths, existing-data
preservation, actual missing-executable CLI and timeout diagnostics/cleanup.

Initial isolated private setup: pinned S018 Python `-I -m venv PREFIX`, then pinned
uv `--no-config pip sync --python PREFIX/bin/python --require-hashes --only-binary
:all: --default-index https://pypi.org/simple docs/tooling/requirements-sumo-linux.txt`,
all exit0. No global system package/executable replaced; no S018 packages added.
Private installation-receipt.json records exact argv/logs, not public absolute paths.

Actual `.venv/bin/python -I scripts/sumo_smoke.py --prefix PREFIX --work-dir WORK`
exits0 with SUMO_INSTALLATION_SMOKE_PASS, all four1.28.0 packages, protocol22,
zero simulation steps, scientific_validation=UNVALIDATED and simulator_support_verified=false.
Private first-smoke-command.json/stdout/stderr/network/server/generator logs retained.
The initial profile hash d7dc6e1784bf2b93163b4cdf87fb94ea4d5adbf484815af66f396dd8baed7326
precedes the explicit300-second installation-budget addition; wheel pins unchanged.
Current profile repeat smoke also exits0. Wrong-system-prefix `/usr` smoke exits1
with actionable executable-version mismatch (observed system1.27.1). Missing
explicit profile executable exits1 actionably. Neither falls back to PATH/global
bindings or accepts a partial receipt. Private smoke-negative-and-repeat.json
contains all expected/observed exit codes.

The final one-command `--install` route sanitizes inherited environment, refuses
existing prefixes, checks manager, installs all four hash-pinned wheels without
source builds/cache and performs actual smoke. Its clean/polluted Unicode-path
proof, final sanitized receipt, governance checks, exact-head CI/integration and
qualified acceptance remain pending at this checkpoint. Do not claim this pending
route completed from the earlier manual setup. Source-reuse prohibition and all
Windows/WSL/native/adapter/physical/replay gates remain unchanged/NOT_RUN.

## E-S019-03 — clean one-command setup and reproducibility observations

Fresh nonexistent dedicated prefix in a Unicode/space path: `.venv/bin/python -I
scripts/sumo_smoke.py --install --prefix PREFIX --work-dir WORK` exits0. Inherited
PYTHONPATH/SUMO_HOME/LIBSUMO_AS_TRACI/LIBTRACI_AS_TRACI and UV/PIP invalid indexes
are deliberately set for this child process; setup strips them before dependencies.
All wheels downloaded/hash-checked with no cache/config/source build. Version,
imports, protocol22/getVersion/clean close pass, zero simulation steps. Private
clean-setup-command.json/stdout/stderr/installation/network/server logs retained.
Current profile SHA2561a80904955f0d9353bf84af45d50ce01f9e9d4b4d0db440fb7aa481df70a0044.

Separate isolated Python probes of each installed upstream sumo.SUMO_HOME/bin/sumo
hash the actual native engine; both match (sanitized receipt records hash/size).
Console entry-point hashes differ because generated wrappers contain venv paths;
this is recorded, not misrepresented as differing native builds or hidden by
normalizing wrappers. Receipt docs/tooling/S019_SMOKE_RECEIPT.json distinguishes
native hash, path-dependent wrapper hashes, software smoke and unvalidated science.

A record-update helper initially addressed nonexistent inventory group `tests`,
raising KeyError/exit1 before writing that JSON or subsequent state files. Inspected
actual keys and used existing `test_source`; no schema change or invented group.
Existing reports/logs preserved. Full final governance/diff/CI gates still required.

## E-S019-04 — final local gates and self-audit

Path review adds a regression for dangling prefix symlinks: reject them before
resolution/install, preserve the link and absent target. Symlinked evidence
locations rejected too. Final `.venv/bin/python -I scripts/python_environment.py
check` exits0:229 tests PASS, Ruff PASS, strict mypy PASS2 source files. All212 prior
regressions retained plus17 S019 tests. Final actual smoke against clean installed
prefix exits0 after those guards; private final-smoke-command.json/outputs retained.

Each `.venv/bin/python -I` command exits0, exact argv/output in private
final-validator-results.json and final-validator-0..6.log:
- scripts/validate_project_docs.py
- scripts/validate_repository_boundary.py
- scripts/validate_evidence_ledger.py
- scripts/validate_change_control.py
- scripts/validate_risk_protocol.py
- scripts/validate_audit_freeze.py docs/audit/S016_AUDIT_FREEZE.json
- scripts/validate_platform_matrix.py check docs/platforms/S017_MATRIX.json

`check_change` declaration schema1, adds_dependency=true, changes_public_contract=true,
changes_science=false, irreversible=false, decision_id=ADR-0012 returns[]/exit0.
`git diff --check` passes. Source-only scope review: setup/smoke/profile/pins/receipt,
17 tests, explicit lint/type scope extension, CI, ADR/setup and governance records.
No binary/legacy implementation/private path/secret committed, no prior tests weakened.
Generated diagnostics/private dependencies excluded by repository boundary. No
platform simulator readiness or scientific accuracy inferred. Status in_review;
exact-head GitHub CI/permitted integration mandatory before acceptance. S020 untouched.
