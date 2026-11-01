# S018 — Python tooling and environment lock (IN REVIEW)

## E-S018-01 — exact tooling and isolated preparation, 2026-11-01

Base47b77eff7ee8e4acfece228c1ab162248a4ed8e1; branch sprint/S018-python-environment-lock.
S017 PR42 head065551c64504000de089461056db84284129b192 passed CI41284148273,
mergef3ab84b08f115bbf7e4ae76edf8eb1ded6d4d462; acceptance PR43
head2c4eff85b930dfd4e6b16dd92ff894fb9e8a0914 passed CI41284252337,
merged current base. Complete S018 read before development; S001–S017 accepted17/88.
Original checkout/.vscode preserved; isolated worktree tracked changes inspected.

Gap/plan: no Python version/venv/dependency/tooling lock existed. Select exact
releases with current primary evidence; prepare an isolated, repeatable environment;
verify wrong-interpreter/global pollution; retain all195 existing tests. No science,
legacy reuse, SUMO/ns-3 release or Windows-runtime claim added.

ADR0011 qualifies CPython3.12.16, uv0.13.6, Ruff0.17.3/mypy2.4.1, unittest.
Runtime/application dependencies empty. Exact direct pins and hashed transitive
release metadata in uv.lock. uv also lives in the venv, avoiding reliance on an
unversioned global manager. Bootstrap requirements contain only its18 wheel hashes
from that lock. Ruff covers new environment module/tests; strict mypy covers that
module only, explicit rollout scope. Config weakening rejected; old tests intact.

Actual evidence so far:
- Primary release/tool documentation checked2026-11-01; direct public HTTP metadata
  returns uv0.13.6/Ruff0.17.3/mypy2.4.1. Python3.12.16 source URL HEAD200,
 20839652bytes. This verifies availability, not binary/source-build equivalence.
- Original shell Python3.11.15, system Python3.12.3, uv0.11.14 observed; existing
  uv catalog lacked3.12.16. Pinned manager installed privately, no global uv replaced.
- Private manager/bootstrap, managed Python download, public-index lock and exact
  sync exit0. No runtime model/dependency stack inherited from legacy.
- Initial explicit uv python-install created a new user-bin Python3.12 shim despite
  a private runtime directory. Detected by command resolution; verified its target
  inside this task's managed runtime, moved only that newly created symlink into
  private evidence. Original system command resolution restored and default shell
  Python remains3.11.15. No unrelated user file deleted. Receipt records correction.
  Setup now uses sync (no explicit Python-bin installation), Git-owned caches/runtime
  and project-owned .venv. Actual owned sync exit0; original command resolution stable.
- A read-only doctor invocation overlapped ongoing preparation and reported
  DEVELOPMENT_ENVIRONMENT_REJECTED; standalone exit was not captured (wrapper
  continued to git status/exit0). This was not counted as readiness. After sync
  completed, direct doctor exited0. Checks must run after successful preparation.
- `python_environment.py doctor` enforces exact CPython, project venv, -I, no
  user/system sites, public hashed locks, pinned manager, exact offline uv check
  and exact dev releases. It reports interpreter binary SHA256 without local paths.
  Doctor never synchronizes or repairs a polluted environment.
- `python_environment.py sync` prepares fresh or marked S018-owned venv only;
  unrecognized/symlink prefixes refused. Inherited Python/PIP/UV/active-environment
  overrides removed. Exact lock/managed Python/public index/no-build used; failed
  partial setup is not accepted and unrecognized data is not deleted.
- Initial full check: Ruff pass, strict mypy pass on1 source file,207 tests exit0.
  Expanded tests include unknown ownership/booleans, scope weakening, bootstrap
  hash binding and100 generated override cases; full211 tests exit0. Final code
  and fresh-checkout reproduction still require final verification below.

Lock SHA25692b7b5ebb2e68f88c271719a9db4ed61eaaf4893bf67e671f3a8f845118bde72.
Private Git metadata private-evidence/S018 stores bootstrap/install/doctor/sync logs
and shim-restoration evidence; private-tools/runtime paths are never public. Global
Python/uv packages untouched, original Python3.12 resolution restored. No legacy
archive/source/execution touched. Existing science/reuse/platform restrictions persist.

Pending: actual two fresh checkouts with empty project caches and one polluted
bootstrap environment; full checks/lock stability; final source/diagnostic artifacts,
all governance validators, exact-head CI/permitted integration and acceptance records.
S018 remains in_progress,17/88; S019 not_started. Windows/WSL/native setup NOT_RUN;
no platform readiness or physical validity claimed by this tooling lock.

## E-S018-02 — checkpoint verification and command corrections

Checkpoint73fd00c4a2433a2b306dc09632783a981e45b73f preserves the implementation
before fresh-clone proof. Fetch confirms main47b77eff7ee8e4acfece228c1ab162248a4ed8e1.
Two manual validator commands omitted required arguments: audit-freeze and platform
matrix argparse each exited2; wrapper continued/exit0 is not a pass. Corrected
`.venv/bin/python -I scripts/validate_audit_freeze.py docs/audit/S016_AUDIT_FREEZE.json`
and `.venv/bin/python -I scripts/validate_platform_matrix.py check docs/platforms/S017_MATRIX.json`
each exit0. Freeze hash/conclusions unchanged; zero verified simulator targets.
Private validator-invocation-correction.json preserves commands/diagnostics.

Actual `/usr/bin/python3.12 -I scripts/python_environment.py doctor` under3.12.3
exits1 with DEVELOPMENT_ENVIRONMENT_REJECTED (expected incompatible interpreter).
Negative Ruff stdin fixture `print(wm_s018_undefined)` exits1/F821. Inline mypy
fixture initially conflicts with project-configured files, exits2/CLI usage (not
accepted as a type check); wrapper's expectation assertion failed and was preserved.
Corrected independent strict config plus inline `x: int = "bad"` exits1/assignment
error. Neither accepted code nor tests changed to accommodate these command errors.
Private static-negative receipts/logs preserve original and corrected observations.

## E-S018-03 — independent fresh checkout proof and final local checks

Two `git clone --no-local` checkouts of checkpoint73fd00c4 were created with
full history, absent .venv and empty Git-owned project caches. Each independently
ran `/usr/bin/python3.12 -I -m venv BOOTSTRAP`, hash-checked/no-cache/only-binary/
no-deps public-PyPI pip installation from requirements-bootstrap.txt, then
`/usr/bin/python3.12 -I scripts/python_environment.py sync --uv BOOTSTRAP/bin/uv`,
`.venv/bin/python -I scripts/python_environment.py doctor`, and
`.venv/bin/python -I scripts/python_environment.py check`. All commands exit0.
Both pass Ruff, strict mypy1 source file and211 regressions. The second checkout
has spaces/Unicode in its private path and inherited PYTHONPATH/PYTHONUSERBASE,
PIP_INDEX_URL, UV_INDEX_URL/UV_EXTRA_INDEX_URL, UV_PROJECT_ENVIRONMENT and VIRTUAL_ENV
pointing to deliberately foreign/invalid locations. No foreign environment target
was created. Both doctor JSON objects match exactly, including Python executable
SHA25623bc148d2b48964b621c5561ff2b81c1d9c7b717967a7491efbf12f4304882b5 and
lock hash above. Original global Python3.12.3 and uv0.11.14 command resolution stable.
Sanitized receipt: docs/tooling/S018_ENVIRONMENT_RECEIPT.json. Full private per-command
argv/exit/log/timestamps/locators: fresh-clone-proof.json and clean/polluted logs.

Final isolated-validator exercise exposed a real compatibility failure:
`.venv/bin/python -I scripts/validate_risk_protocol.py` exits1 because its direct
CLI sibling import relied on implicit script-directory sys.path. Added a regression
first: isolated CLI from unrelated cwd fails1 (risk-isolated-before-fix.log retained).
Fix inserts only resolved trusted repository root and imports the qualified scripts
module, matching existing governance helpers' pattern. No isolation or risk check
weakened. `.venv/bin/python -I scripts/python_environment.py check` now exits0:
Ruff PASS, strict mypy PASS1 source file,212 tests PASS. All previous195 tests retained.

Each of these final commands exits0 (individual logs/argv in private
final-validator-results.json): `.venv/bin/python -I` followed by
- scripts/validate_project_docs.py
- scripts/validate_repository_boundary.py
- scripts/validate_evidence_ledger.py
- scripts/validate_change_control.py
- scripts/validate_risk_protocol.py
- scripts/validate_audit_freeze.py docs/audit/S016_AUDIT_FREEZE.json
- scripts/validate_platform_matrix.py check docs/platforms/S017_MATRIX.json

Changed-file scope: Python pin/project/lock/bootstrap files; environment helper and
16 tests; isolated risk CLI/import regression; CI; ADR0011/setup/receipt; inventory,
decision/progress/handoff/blockers/validation/sprint report. No scientific equations,
parameters/units/defaults changed; timestamps are wall-clock observations only.
Declared adds_dependency=true, changes_public_contract=true, changes_science=false,
irreversible=false under accepted ADR-0011. No second-human approval claimed.
Windows/WSL/native setup NOT_RUN, no simulator support/physical validation accepted.
S018 enters in_review only; exact-head CI/permitted integration still required.
