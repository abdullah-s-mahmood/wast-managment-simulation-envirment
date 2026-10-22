# Definition of Done and global quality gates

Authority: AGENTS.md, ADR-0005, sprint contract, evidence policy. This elaborates
existing acceptance rules; it does not waive stronger sprint-specific gates.
A passing checker is evidence about recorded structure, not sprint acceptance.

## Entry, review, acceptance and integration
1. Select the first incomplete sprint; prerequisites completed, contract read,
   tree/diff inspected, scope and test plan recorded. Preserve unrelated work.
2. Add tests before relying on changes, implement only the contract, preserve
   original failing cases and verify fixes. Do not weaken tests to pass.
3. Map every acceptance criterion to a command, assertion, retained artifact and
   evidence ID. Record time/timezone, platform/versions, inputs/hashes, command,
   exit code, expected/observed output, failures, limitations and NOT RUN reasons.
4. Review changed files for units, identifiers, hidden defaults, undocumented
   assumptions, evidence, licensing, secrets, partial writes and scope creep.
5. Move in_progress to in_review after local gates. Obtain actual GitHub checks
   for the exact published head and verify mandatory checks succeeded. Recheck
   after every head change. Never substitute a previous run or local green test.
6. Record author self-audit, requirements traceability and acceptance rationale.
   No independent-person review or fake APPROVE needed. Normal merge must be
   permitted by GitHub protections. Never bypass checks, force-push or change
   protections to escape a gate.
7. Only after permitted integration record completed, PR/head/merge SHAs and CI
   URLs/results in progress, report, validation log, handoff and blockers. Validate
   documentation and acceptance records in CI. Advance strictly in order.

A mandatory FAIL or NOT RUN keeps its gate open; investigate or record a blocker.
NOT_APPLICABLE is a reasoned scope judgment with evidence, never a synonym for
unavailable dependency/platform/data. The sprint contract and claimed support
control applicability. Strong scientific/high-risk requirements remain mandatory.
Any authenticity/applicability doubt must be resolved before acceptance.

## Criterion-to-evidence matrix
Each row names a stable criterion, example command, observable assertion and
retained evidence. Sprint reports name the actual commands and exact outputs;
these examples are not claims of execution and cannot replace sprint requirements.

| ID | Command or evidence-producing procedure | Assertion | Retained reviewer-visible artifact |
|---|---|---|---|
| WB | focused unittest or module test command from sprint | invariants, branches, state/error transitions pass | captured output, input/fixture hashes and regression reproducer |
| BB | public CLI/API invocation through a deterministic fixture | output IDs, units, status and errors satisfy contract | inputs, output bytes and expected/observed comparison |
| ADVERSARIAL | negative/fuzz/boundary tests named in report | malformed/unsupported/extreme/corrupt inputs fail closed without plausible partial success | failing inputs, exact failures and fixed regressions |
| REGRESSION | python -m unittest discover -s tests -v (plus later required suites) | all applicable prior tests pass; no weakened assertions | complete suite output/count and exit code |
| DOCS | python scripts/validate_project_docs.py | 88 contracts and actual progress remain coherent | validator output and progress/report/handoff diff |
| INTEGRITY | python scripts/validate_repository_boundary.py; git diff --check; applicable raw-data checks | allowed scope, no prohibited artifacts/signatures; atomic/fail-closed integrity where applicable | inventory/diff output, raw-data manifests and failure evidence |
| SELF_AUDIT | inspect full staged/published diff and requirement matrix; record evidence-producing git diff commands | each criterion satisfied within domain; no false scientific/reviewer claims | author identity/method, explicit verdict, known limits and changed-file list |
| CI | GitHub checks/runs query at the exact PR head | all mandatory checks completed/success on integrated head | GitHub run URLs, checked SHA, conclusions and permitted merge SHA |
| CONFIGURATION | applicable schema/negative/provenance tests | no hidden scenario defaults, wrong units, invalid IDs/CRS/time, unsupported versions or unvalidated references | resolved input/schema versions, hashes and diagnostics |
| SCIENCE | source audit and independent/empirical reference validation procedure | source/equation/units/domain/calibration/uncertainty and required validation supported; E4/E5 not promoted | ledger/source locations, calculations, calibration/holdout data and negative results |
| REFERENCE_PROPERTY | independent exact/reference and generated/metamorphic tests | dimension/accounting/replay invariants or documented reference tolerances hold | expected calculations, seeds, tolerances/units and observed results |
| INTEGRATION_PLATFORM | actual version/smoke and adapter runs on every claimed platform | real boundaries, clocks, data correlations and recovery match contract | OS/tool versions, commands, stdout/stderr, input/output hashes |
| DATA_STATISTICS | raw-data validation and preregistered independent analysis | no partial/corrupt run analyzed; metrics/design/exclusions/diagnostics traceable | immutable raw data, analysis plan, scripts and diagnostics |

WB/BB/adversarial/regression/docs/integrity/self-audit/CI are always required.
Other rows require scope-specific applicability evidence. Governance-only work
may document why no physical model, adapter, advertised runtime or analysis exists;
a missing required dependency/data/platform can never become inapplicable.
Thresholds/tolerances come from the owning contract/source, not a universal
coverage percentage, invented physical bound or statistical significance shortcut.

## Optional evidence manifest and read-only checker
`gates.json` enumerates criterion IDs and whether scope review may deem them
inapplicable. It is policy, not observed results. Manifest version 1 contains
schema_version, head_sha, checks; each check contains id, status, command,
assertion, artifact, sha256, exit_code, platform, versions, rationale, head_sha.
All text fields are nonempty. Each ID appears exactly once. PASS requires integer
exit 0; NOT_APPLICABLE requires null exit and a retained applicability rationale.
FAIL/NOT_RUN, absent commands, missing/corrupt artifacts and stale SHAs reject.
For a manual criterion, command is the actual evidence-producing command; a
zero exit does not encode or replace the separately recorded human/author judgment.

`python scripts/validate_quality_gates.py manifest.json --head <exact-sha>`
checks completeness and artifact SHA-256 against a caller-supplied head. It
neither runs commands nor contacts GitHub, accepts science, changes progress or
merges. Synthetic tests explicitly label all fabricated metadata and never call
it real execution. A malicious author can forge internally consistent metadata;
actual observation/source review and GitHub API verification are still mandatory.
Reports may use the same matrix directly; this optional manifest is not a new
requirement to manufacture duplicate records for earlier accepted sprints.

CLI is read-only; invalid/truncated/duplicate-key/nonfinite inputs exit 1, syntax
errors exit 2. Evidence paths stay within the selected root, and mismatched hashes
fail. Preserve failed records and original artifacts; never overwrite failures
with success. Authorized publication must omit private data/secrets. No new
physical units, simulation time semantics or stochastic settings are introduced.
