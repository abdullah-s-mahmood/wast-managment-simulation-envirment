# Validation Log

## E-S002-01 — Clean-room boundary (2026-10-22)
- Linux x86_64 / Python 3.11.15; branch sprint/S002-boundary, base e2ba34a.
- `python -m unittest discover -s tests -v`: exit 0; 12 tests passed,
  including 7 boundary tests and 5 charter regressions.
- Scope/provenance, exact commands and not-run limits: [S002 report](SPRINT_REPORTS/S002_REPORT.md).
- `python scripts/validate_repository_boundary.py`: exit 0, 130 approved artifacts;
  `python scripts/validate_project_docs.py` and `git diff --check`: exit 0.
- Actual legacy audit, scientific validation and simulator/platform integration NOT RUN;
  not applicable to this governance sprint. Exact-head CI/integration still required.

Append entries; do not rewrite history to hide failures.

## Bootstrap
- Date: 2026-10-22
- Scope: governance and sprint plan.
- Simulation tests: NOT RUN — no simulator implementation exists.
- SUMO/ns-3 integration tests: NOT RUN — versions/runtime not verified.
- Scientific validation: NOT RUN — no equations accepted.
- Documentation validator: defined at `scripts/validate_project_docs.py`; CI is configured to run on push/PR after commit.
- These are explicit not-run statuses, not passes.

## Entry template
- Date/time/timezone:
- Commit and sprint:
- Platform/environment:
- Command and exit code:
- Expected/observed:
- Artifacts/evidence:
- Pass/fail/not-run and reason:
- Limitations:

## E-S001-01 — Charter and scope verification
- Date: 2026-10-22; session timezone Asia/Baghdad.
- Branch: `sprint/S001-charter`; base `5bbfff0b4a72a03d2e7ab0cd15259126bbefe22d`.
- Linux x86_64 / Python 3.11.15.
- `python -m unittest discover -s tests -p test_s001_charter.py -v`: first exit 1
  (arbitrary test-length constraint); corrected test specification, second exit 0,
  five tests passed. Failure reproducer retained in report.
- `python scripts/validate_project_docs.py`: exit 0.
- `git diff --check`: exit 0.
- WB/BB structural and adversarial fixtures passed within their stated domain.
- Independent contributor comprehension/approval: NOT RUN, pending review.
- Windows, simulator integration and scientific validation: NOT RUN; no runtime
  implementation or physical model in this sprint.
- Evidence and exact command outcomes: [S001 report](SPRINT_REPORTS/S001_REPORT.md).
- CI/PR outcomes will be recorded separately after publication; local checks do
  not establish independent acceptance. ADR-0005 remains proposed.

## E-S001-02 — Publication and review gate
- Published implementation `8f24dd20cb4628d976949acebfafd842d19ff8b1`, PR #1:
  https://github.com/abdullah-s-mahmood/wast-managment-simulation-envirment/pull/1
- GitHub Actions PR run 39706731111 completed/success at that implementation SHA.
- Local/published tree equality verified: `41095acb3ad9d0e60ec3f80d4393a40ffd7bf67f`.
- Connector review listing: zero reviews; S001 transitions in_progress -> in_review.
- Shell push exit 128 (no HTTPS username); connector publication succeeded.
- Check the record-update commit's own CI before acceptance. Independent review
  remains pending; complete publication provenance is in the S001 report.

## E-S001-03 — Sole-maintainer policy amendment (2026-10-22)
- Owner explicitly removed mandatory independent-person sprint reviews.
- ADR-0005 accepted, AGENTS.md §4A updated, charter and bounded charter tests updated.
- Historical test runs, review requests and failed commands are preserved above.
- Exact-head GitHub CI for the amended PR is still required before integration;
  this entry does NOT claim the amended commit's checks have passed.
- This governance change does not verify scientific models, SUMO, ns-3 or Windows.

## E-S001-04 — Final single-maintainer S001 acceptance (2026-10-22)

- Scope: S001 charter, C01–C10 map, document-only tests and owner governance amendment.
- Exact PR head: `8687c54551d16684cdaf95988aa5f840621a1b27`.
- GitHub Actions run: https://github.com/abdullah-s-mahmood/wast-managment-simulation-envirment/actions/runs/39707882302 — completed/success.
- CI steps: documentation and 88-sprint progress validation PASSED;
  `python -m unittest discover -s tests -p test_s001_charter.py -v` PASSED (5 charter tests).
- Self-audit: charter C01–C10 maps to S002–S088, clear distinction between
  hypothesis vs scenario settings, explicit invalid-input and provenance semantics,
  test mutation cases documented; no physical model or baseline-result claim.
- Owner explicitly waived second-person review via ADR-0005. No GitHub APPROVE
  review was invented. PR #1 merged successfully through authorized GitHub API.
- Merge commit: `7aaa0b8ee76fb276506bbaf0a97b65101583901b`.
- Acceptance status: **S001 COMPLETED, 1/88**. S002 becomes next eligible.
- Not run: Windows, SUMO/ns-3, physical/empirical scientific validation; not
  applicable to S001 charter. Future required gates remain open.
- This progress-record update requires its own GitHub CI; a failing post-merge
  state check must reopen S001 rather than be ignored.

## E-S002-02 — Accepted integration
- PR #2: https://github.com/abdullah-s-mahmood/wast-managment-simulation-envirment/pull/2
- Exact head: `be95738cda892134c75c8a7cbf878580e01c91be`.
- Both exact-head validate checks completed/success: runs 39708732669 (PR) and
  39708729229 (push). Original main acceptance record e2ba34a also has green CI,
  run 39708111039. No mandatory check failed or remained unavailable.
- GitHub permitted normal merge, commit `c96fd0b3a114d3c6088adab481e94177edc884cc`.
- Self-audit verdict: S002 accepted under ADR-0005; 2/88 accepted; S003 next.
- Protection-detail read returned 403 (integration lacks administration scope).
  No protection/settings changes attempted; normal merge API enforced permissions.
- Connector publication tree `4d46652efa594aed864305ec671483fe87624853`
  equals local committed tree (local checkpoint 81f75d0). No scientific validation claimed.
- This acceptance-only state commit must pass its own CI before S003 implementation.

## E-S002-03 — Acceptance-state recovery checks (2026-10-22)
- Recovered main at da78022f53ed157f35fdd79d4852b93b21cb8986; acceptance-state
  commit has no workflow runs or combined statuses in GitHub connector queries.
- Reconfirmed implementation be95738cda892134c75c8a7cbf878580e01c91be has
  completed/success PR run 39708732669. S001/S002 are not reimplemented.
- Linux x86_64, Python 3.11.15: python -m unittest discover -s tests -v
  exit 0 (12 tests); python scripts/validate_project_docs.py exit 0;
  python scripts/validate_repository_boundary.py exit 0 (130 approved artifacts).
- Existing untracked S003 drafts preserved in a named Git stash before checks;
  no S003 implementation started. Source/physical/simulator/Windows validation
  NOT RUN and outside this documentation-only recovery scope.
- gh auth status exit 1 (invalid local credential); GitHub connector remains usable.
- This focused recovery PR requests CI on the acceptance-state tree plus this log.
  No green exact-head CI or merge is claimed by this entry. S003 remains next.

## E-S003-01 — Evidence contract local verification (2026-10-22)
- Branch sprint/S003-evidence-ledger; base b591b2339f3e5b2b87bc26f01abd52312403ffde.
- Linux x86_64 / Python 3.11.15. S002 acceptance-state recovery PR #3 exact head
  aadb9b332f16e7bc42ec3e2ee0462048ba5afc45 passed CI run 39709574639 and merged.
- python -m unittest discover -s tests -p test_evidence_ledger.py -v: initially
  exit 1 (bad hash accepted); retained regression, added source-byte hash check.
- python -m unittest discover -s tests -v: exit 0, 23 tests after correction.
- python scripts/validate_evidence_ledger.py: exit 0, empty production ledger.
- python scripts/validate_project_docs.py and git diff --check: exit 0.
- Scope, exact failure reproducer, source trace and NOT RUN rationale: S003 report.
- python scripts/validate_repository_boundary.py: exit 0, 138 approved artifacts.
- CI and merge pending; S003 in_review, S004 not started.

## E-S003-02 — Accepted integration
- PR #4: https://github.com/abdullah-s-mahmood/wast-managment-simulation-envirment/pull/4
- Exact head ec4296b6deb1e7b7c4a27913ccc4f6df13a632d1 passed CI run 39709929916.
- GitHub permitted merge f7ee3973d59aef5469d6d29bc108dfeb7416b492.
- Published tree 7861823613f8fa9c6de1564d03c9b517f96ee225 equals local checkpoint
  a59f5ba tree; checkpoint branch preserved. 23 tests/all three validators passed.
- Author self-audit accepted under ADR-0005. S003 completed (3/88), S004 eligible.
- No scientific model accepted. External citation authenticity, Windows and
  simulator/scientific validation remain future gates, not claimed passes.

## E-S004-01 — Classification and separation verification (2026-10-22)
- Branch sprint/S004-classification; base e1c0f3dc7309950341df4001647ad37eebde8fce.
- Linux x86_64 / Python 3.11.15. ADR-0003/ADR-0005; synthetic fixture only.
- python -m unittest discover -s tests -p test_study_separation.py -v:
  exit 1 missing module (test-first); exit 1 sibling import; fixed import; exit 0, 5 tests.
- python -m unittest discover -s tests -v: exit 0, 28 tests.
- python scripts/validate_project_docs.py: exit 0, 88 sprint contracts.
- python scripts/validate_evidence_ledger.py: exit 0, empty production ledger.
- python scripts/validate_repository_boundary.py: exit 0, 143 approved artifacts.
- git diff --check: exit 0. S004 report records scopes, failures and NOT RUN tests.
- S004 local acceptance gates pass; exact-head CI and merge still pending.

## E-S004-02 — Accepted integration
- PR #6 exact head 62f6de561540d7ef07a3bfb2c9173775745f0b02 passed CI run
  39710355019 (completed/success). Normal merge permitted: 707e7a37cfd36752b382665c9926e4f095198454.
- Published tree 0ec78ca2c5b8abfc5b91f07815dc0e473ba0d52b equals local checkpoint
  b8d8f8f tree; preserved branch. 28 tests and all three validators passed.
- Author self-audit accepted under ADR-0005: S004 completed (4/88); S005 next.
- Scope remains governance-only; no scientific/causal or runtime validity claim.

## E-S005-01 — Unit/time/ID conventions verification (2026-10-22)
- Branch sprint/S005-conventions, base 3799b5cdf9a2e5355885d93a86c492490cb1aced.
- Linux x86_64 / Python 3.11.15. Primary source locations in S005 report/policy.
- python -m unittest discover -s tests -p test_conventions.py -v: exit 1 test-first
  missing module; exit 0 implemented; exit 1 added +01:99 attack; fixed strict
  offset validation; exit 0 with all six tests and retained attack.
- python -m unittest discover -s tests -v: exit 0, 34 tests, including 101-value
  exact-rational equivalent-unit sweeps and independent reference conversions.
- python scripts/validate_project_docs.py: exit 0, 88 sprint contracts consistent.
- python scripts/validate_evidence_ledger.py: exit 0, no scientific records accepted.
- python scripts/validate_repository_boundary.py: exit 0, 148 approved artifacts.
- git diff --check: exit 0. S005 report records failures and NOT RUN rationale.
- Exact-head CI and permitted integration pending; S006 not started.

## E-S005-02 — Accepted integration
- PR #8 exact head 6053e6eb463d2474191c7eb20022953232739d3a passed CI run
  39710844432 (completed/success), merged dcaefcfc7ab19d07898dfc8a83ec8b1cd53ef0e0.
- Published tree e9d2dfffacafa68f61f8242f8a4ed9edffc55165 equals local checkpoint
  4d746d7 tree, preserved branch. 34 tests/all three validators pass.
- Author self-audit accepted under ADR-0005: S005 completed (5/88), S006 next.
- No scientific/empirical/runtime/Windows/simulator or geodesy validity claim.

## E-S006-01 — Definition of Done/evidence attacks (2026-10-22)
- Branch sprint/S006-quality-gates, base 583adb7d6583368585230672065b82730beccb7c.
- Linux x86_64/Python 3.11.15. python -m unittest discover -s tests -p
  test_quality_gates.py -v: exit 1 test-first missing module; then exit 0, 5 tests.
- python -m unittest discover -s tests -v: exit 0, 39 tests.
- python scripts/validate_project_docs.py: exit 0, 88 contracts consistent.
- python scripts/validate_evidence_ledger.py: exit 0, empty production ledger.
- python scripts/validate_repository_boundary.py: exit 0, 153 approved artifacts.
- git diff --check: exit 0. Failures/NOT RUN/limits documented in S006 report.
- Actual GitHub exact-head CI and normal integration pending; S007 not started.

## E-S006-02 — Accepted integration
- PR #10 exact head 98c77038423f834970f74dea8db2c0bab7e67e0d passed CI run
  39711264161, completed/success. Permitted merge 6119885cfa11b44acdf49e4cde5f1f30793f59ab.
- Published tree a365286d5b3bd211db33601850277951d65fc151 matches local checkpoint
  9b89e31 tree, preserved branch. 39 tests/three validators pass.
- Author self-audit under ADR-0005 accepted S006 (6/88); S007 next.
- No scientific/model/runtime validity claim; completeness checks do not authenticate evidence.

## E-S007-01 — ADR and change-control verification (2026-10-22)
- Branch sprint/S007-change-control; base bd86e49e69e93f8d7e2a2ca527f962d22e180326.
- Linux x86_64/Python 3.11.15. python -m unittest discover -s tests -p
  test_change_control.py -v: exit 1 missing module; exit 1 two tests/24 missing
  ADR sections; dated clarifications preserve choices; exit 0, 5 focused tests.
- python -m unittest discover -s tests -v: exit 0, 44 tests.
- python scripts/validate_project_docs.py: exit 0, 88 contracts.
- python scripts/validate_evidence_ledger.py: exit 0, empty production ledger.
- python scripts/validate_repository_boundary.py: exit 0, 157 approved artifacts.
- python scripts/validate_change_control.py and git diff --check: exit 0.
- Actual failures/limits/NOT RUN rationale in S007 report. Exact-head CI/merge pending.

## E-S007-02 — Accepted integration
- PR #12 exact head 0fa70fb0d21b4fced9239fe87dda5c8e2cb21503 passed CI run
  39711665684, completed/success; permitted merge 86326c298ccadd19bf2df3e78aec407db5ce5d6d.
- Published tree 62af707d8f1388c797b0ab93759a67f96a43e51b equals local checkpoint
  ecf99e9 tree, preserved branch. 44 tests/four validators pass.
- Author self-audit accepted S007 under ADR-0005 (7/88); S008 next.
- No change to prior accepted decisions or scientific/runtime validity claim.

## E-S008-01 — Risks and escalation attacks (2026-10-22)
- Branch sprint/S008-risks, base 5f6e0130afe6e241dba6730b13930ed7812cd68f.
- Linux x86_64/Python 3.11.15. python -m unittest discover -s tests -p
  test_risk_protocol.py -v: exit 1 test-first missing module; then exit 0, 4 tests.
- python -m unittest discover -s tests -v: exit 0, 48 tests, including exhaustive
  64-combination explicit-fact escalation checks and no-guess/authorization attacks.
- python scripts/validate_project_docs.py: exit 0, 88 consistent contracts.
- python scripts/validate_evidence_ledger.py: exit 0, no scientific records accepted.
- python scripts/validate_repository_boundary.py: exit 0, 162 approved artifacts.
- python scripts/validate_change_control.py: exit 0.
- python scripts/validate_risk_protocol.py and git diff --check: exit 0.
- Failure/NOT RUN/residual limitations in S008 report; exact-head CI/merge pending.

## E-S008-02 — Accepted integration
- PR #14 exact head 87d26f2c10b9616dcb70d264a77962b07bda300d passed CI run
  39712069254, completed/success; normal merge cd5a5ce51e67885f35db3939478d8b6af8171969.
- Published tree 265f2e41e09e7dd7787492665c6cc59df863ac2b equals local checkpoint
  59aa7fa tree, preserved branch. 48 tests/five validators pass.
- Author self-audit accepted S008 under ADR-0005 (8/88); S009 next.
- No model/runtime/scientific acceptance. Legacy source not designated in records;
  S009 must check source availability and stop if required evidence unavailable.

## E-S009-01 — Source-candidate check and blocked intake (2026-10-22)
- Branch sprint/S009-legacy-intake, base 072c6d55ea4979a0c263edc61a0efcdbf827abbe.
- Linux x86_64/Python 3.11.15. Read full S009 contract and clean-room intake policy.
- rg -n -i 'legacy.*(https|zip|tar|path|location|commit|bundle)|source.bundle|intake.id'
  README.md docs/STATE docs/CLEAN_ROOM_BOUNDARY.md docs/adr: exit 0; no designated
  immutable source reference. git remote -v and git branch --all: exit 0, current
  implementation/governance refs only. Tracked archives list empty; sibling-name
  metadata probe located candidate archives/trees (exit 0); no contents published.
- Read-only hashlib/tarfile metadata probe: exit 0, LEGACY-CANDIDATE-001 bytes
  487062036; SHA-256 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8
  matches sidecar. Header scan limited to 1000 members/512 MiB declared total,
  stopped at member cap; console output truncated. Exact safe repro/report in S009.
- No extraction, execution, source copying, deletion or scientific interpretation.
  Full source manifest/hash/secret/license/binary/traversal checks NOT RUN.
- python -m unittest discover -s tests -v: exit 0, 48 prior governance tests.
- python scripts/validate_project_docs.py: exit 0, 88 contracts consistent.
- python scripts/validate_evidence_ledger.py: exit 0, no scientific models accepted.
- python scripts/validate_repository_boundary.py: exit 0, 163 approved artifacts.
- python scripts/validate_change_control.py and python scripts/validate_risk_protocol.py:
  exit 0. git diff --check: exit 0.
- B-S009-01/R-LEGACY triggered: candidate available but intended immutable baseline,
  provenance/handling not resolved. Owner asked for source designation/restrictions.
  S009 in_progress -> blocked; S010+ untouched. No completion or archive safety claim.
- This blocked-state PR must pass its own exact-head CI before normal integration;
  integrating recovery records does not accept S009. Resume only with resolving evidence.

## E-S009-02 — Authorized candidate, bounded scanner and safety stop
Owner now explicitly designates candidate 001 for read-only local audit only;
no archive/source/data redistribution, copying or unknown-code execution.
Size/hash verified exactly against expected values (exit 0). B-S009-01 source
selection resolved; blocked -> in_progress. A new safety stop then requires
in_progress -> blocked, B-S009-02. No later sprint started.

Independent tooling: scripts/inventory_legacy.py, external resource policy,
private intake checklist and six synthetic test groups. Scanner never extracts
filesystem objects, follows links or opens nested archives. Per-member private
paths/hashes/size/role/language hints/binary/signature flags preserve provenance.
Full manifest is restricted to Git common metadata private-evidence/S009; never
committed. Process wrapper set RLIMIT_AS=268435456 bytes and RLIMIT_CPU=120 seconds.
Actual bounded scan: complete=false, 1282 members, 504463360 expanded bytes read;
17 executable permissions, 20 executable signatures, 78 binary-content findings,
44 nested archives, then one rejected link/special member. Inspection stopped;
source not accepted. No potential-secret signature found in inspected prefix;
uninspected bytes remain unchecked. No claim of absent secrets or license clearance.
Original archive and prior evidence preserved. Resolve prohibited member handling
without altering baseline or executing/extracting it; full safe inventory remains
mandatory. Licensing/provenance permits no code reuse. B-S009-02 is a content-
safety blocker, not a request for routine continuation or second-person review.

Linux x86_64/Python 3.11.15. Test-first focused unittest initially exit 1 missing
module; after implementation six tests pass. python -m unittest discover -s tests
-v exit 0, 54 tests. WB/BB/negative tests cover classification/hash/replay, limits,
corruption, traversal, duplicates, case collisions, links/special files, executable,
binary/nested archive/secret signatures and public CLI no-extraction failure.
Independent SHA-256 fixture references pass. Actual scan wrapper exit 0 means
manifest saved, NOT source accepted: manifest complete=false records rejection.
Windows, full source inventory, legacy execution and scientific validation NOT RUN.
New implementation is partial S009 work, not completion. Mandatory gates stay open.

Boundary check initially exit 1: docs/legacy is prohibited by the clean-room path
policy. Moved independently authored protocol/policy to docs/audit (no exemption).
Final local verification: python -m unittest discover -s tests -v exit 0 (54);
python scripts/validate_project_docs.py, validate_repository_boundary.py (167
approved artifacts), validate_evidence_ledger.py, validate_change_control.py,
validate_risk_protocol.py and git diff --check each exit 0. All ran under Python
3.11.15/Linux x86_64. No mandatory full-intake check is represented as passed.

## E-S009-03 — Verified partial-work integration and refined safety finding
PR #17 exact head 47cfb49101a771e21e73cb76c18bece25f7feb76 passed CI run
39741085230 (completed/success). Normal merge acbeb27c1d8157be6878f53be9c05bcf3a7c4de6.
Local checkpoint de61a34 and published tree both
74adf19528bec2cdb6b23a1e93189553fb6dd895; equality checked before merge.
Repeat private scan exit 0 (wrapper saved rejected manifest): same 1282 members,
complete=false. Rejected TAR type hex 32 is a symlink. Private lexical target
resolution against bundle root reports escapes=true, target never followed.
This is an escaping-link finding, not merely an in-bundle link disallowed by policy.
Read-only normalized-path check exited 0; no target/member path published.
Restricted reproducible wrapper private-evidence/S009/run_inventory.py accepts
worktree root as argument and returns exit 1 for this incomplete/flagged scan.
S009 remains blocked/B-S009-02; full inventory NOT RUN. S010+ untouched.
Action: resolve unsafe baseline handling without silent substitution; preserve
archive, private manifest and rejected-link metadata. No extraction or execution.
No licensing, source reuse, archive safety or scientific acceptance claimed.

## E-S009-04 — Quarantine-only inventory policy and full run
- Owner expressly authorizes quarantine-and-continue for private metadata inventory.
  ADR-0006/D-0010 document the contract change; no extraction/execution/reuse or
  redistribution permission. B-S009-02 blocked -> in_progress with this evidence.
- Branch sprint/S009-quarantine-continue, base 6df64debe48469726c2e6ee5ea4f67d221eb0676.
- Linux x86_64, Python 3.11.15; no new third-party dependency.
- `python -m unittest discover -s tests -p test_inventory_quarantine.py -v`:
  first exit 1, 7 tests with 16 failing subcases/2 errors (version-1 stop semantics
  and absent v2 states). Private test-first transcript retained; assertions not
  weakened. New compressed-budget fixture checks hash only when hashing is within
  its explicit compressed-byte budget, rather than requiring a prohibited read.
- `python -m unittest discover -s tests -p '*inventory*.py' -v`: exit 0, 15 tests.
  Includes beginning/middle/end links, relative/absolute targets, hard links,
  traversal, duplicates/case collisions, 64 generated consecutive-quarantine
  sequences, later valid files, truncated/corrupt payload/header/footer/CRC,
  memory/size/count/time exhaustion, baseline mismatch, manifest tampering,
  split secret signatures, non-UTF-8 binary and public CLI no-extraction checks.
- `python -m unittest discover -s tests -v`: exit 0, 63 tests; original 54 retained.
- Real run 1 CLI exit 1: member-size limit after 3367 entries, complete=false.
  Private header check exit 0: generated-output entry declares 730476900 bytes.
  External per-member cap raised 128 MiB -> 1 GiB for chunk hashing; memory 256 MiB,
  expanded 4 GiB, CPU/wall 120 seconds unchanged; exhaustion tests still pass.
- Real run 2 child exit -9/no manifest; shortly before, process CPU time observed
  at 114 seconds under 120-second hard CPU cap. Failure artifacts retained. Added
  byte-prefix guard before signature regex; signature detection tests retained.
- Real run 3 CLI exit 0, 35.878 seconds, inventory completed, identity_verified=true.
  11049 members; 3545374720 expanded bytes (headers/padding included); 1130 entries
  quarantined. Findings: executable permissions 73, binary content 831, executable
  signatures 731, nested archives 58, links 281, unsafe-link-target flags 235.
  No potential-secret pattern observed; this is not evidence that secrets are absent.
- Roles (heuristics, not verified ownership): document/unknown 2131, tests 45,
  generated outputs 5650, configuration 56, source 279, binary 163, headers 2725.
  Synthetic fixtures separately exercise dataset/cache/dependency categories.
- Archive hashes before/after both equal designated
  da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8;
  compressed bytes 487062036. No source archive/member written or reconstructed.
- Canonical v2 manifest SHA-256:
  61b494e1d921464f980714d0a916dff12856acc2058421da091ce959751c2daf.
  Private evidence: Git common metadata private-evidence/S009/quarantine-v2-run3.json;
  failed runs 1/2 preserved. Run commands: Linux CLI with --limits
  docs/audit/intake_limits.json --expected-sha256 <designated hash> --expected-size
  487062036; archive locator resolved privately, stdout/stderr redirected to
  restricted mode-0600 files. Library/CLI contains no source execution.
- Software-tested property: complete inventory with findings is distinct from
  clearance. security_clearance=not_granted, source_reuse_authorization=prohibited,
  scientific_model_validation=unvalidated. Unknown license/source commit and
  uncertain ownership remain limitations; neither blocks private technical inventory.
- Windows/source execution/physical reference and empirical validation NOT RUN:
  no supported Windows hostile-input CLI or physical model introduced by S009.
- Self-audit: every logical entry hashed or typed metadata-only; duplicate prior
  records also quarantined; parser/CRC/termination/identity/resource failures stay
  incomplete. No target access, nested expansion, source/data upload or partial-run
  acceptance. Standard-library parser is bounded by metadata and OS process limits;
  unsupported sparse encoding stops incomplete. Manifest digest is not authenticity.
- Exact-head CI/integration and actual replay results are recorded separately below.

## E-S009-05 — Real replay and final local gates
Repeat CLI run 4 exit 0: byte-for-byte identical private JSON to run 3.
verify_manifest=true; both designated archive hashes unchanged; complete=true.
Private JSON artifact SHA-256 8ef06f34a5538fcbcb7b884f1c9e25c1c752d3e9634773fec60e6e2c2682ebbb;
canonical manifest digest 61b494e1d921464f980714d0a916dff12856acc2058421da091ce959751c2daf.
This verifies reproducible inventory/immutability, not source or scientific safety.
Final commands observed exit 0: python -m unittest discover -s tests -v (63 tests),
python scripts/validate_project_docs.py, python scripts/validate_repository_boundary.py
(169 approved artifacts), python scripts/validate_evidence_ledger.py,
python scripts/validate_change_control.py, python scripts/validate_risk_protocol.py,
and git diff --check. Exact-head GitHub CI and permitted integration pending.

## E-S009-06 — Accepted technical inventory integration
PR #19 head 0c42f4300c62d7870b2b60caa7f382e880e4da6f passed CI run
39743742012, completed/success; permitted merge 6ad9e513bcfa239b702eac10f74773702e52076b.
Local checkpoint ac9fd71 tree equals published f20b55ab3ff297acbe372d52668dcf47e6ceabab.
Author self-audit under ADR-0005: S009 technical inventory/protocol criteria met;
9/88 completed, S010 next. Full inventory/replay, 63 tests and five validators pass.
No archive safety, execution, reuse, licensing or scientific validation is accepted.
B-S009-02 resolved; security findings and quarantine dispositions remain recorded.

## E-S010-01 — Static source module/dependency graph (2026-10-24)
- Branch sprint/S010-static-module-graph, base 969eec59de95a5efa7b9dedc396a7a282c53b7e6.
  Fetch verified no competing/newer sprint completion before implementation/publication.
- Linux x86_64/Python 3.11.15. python -m unittest discover -s tests -p
  test_source_graph.py -v initially exit 1 (test-first missing module); final focused
  nine tests pass. python -m unittest discover -s tests -v exit 0, 72 tests.
- Public Linux CLI: python scripts/audit_source_graph.py <private-archive> --inventory
  <private S009 manifest> --policy docs/audit/static_graph_policy.json
  --expected-manifest-sha256 61b494e1d921464f980714d0a916dff12856acc2058421da091ce959751c2daf:
  exit 0; full archive before/after hash and selected payload hashes match S009.
  3752 nodes/79509 syntax edges; 2 explicit unparsed/quarantined unknowns. Graph
  canonical digest 01f0a10ce7059aa732f754bd47e492f9cac4b36b542492af5c0d119812730b62.
- Independent source-line check exit 0: four entry ID/hash/line anchors for import,
  include, dynamic loading syntax and build declaration. No source code executed.
  Private graph/cross-check under Git common metadata private-evidence/S010.
- python scripts/validate_project_docs.py, python scripts/validate_repository_boundary.py
  (174 approved artifacts), python scripts/validate_evidence_ledger.py,
  python scripts/validate_change_control.py, python scripts/validate_risk_protocol.py
  and git diff --check: each exit 0.
- Scope/commands/failure evidence and NOT RUN rationale: S010 report and static
  graph policy. Native lexical calls/import/build resolution remain unverified;
  no installed dependency, active-runtime or physical/causal validity claim.
- Exact-head CI and permitted merge pending; S011 not started.
- Final real CLI replay exit 0, byte-identical graph JSON. Private graph artifact
  SHA-256 6c593ea9b766f642162e56e493bf316eb3dba91588b17e8e82bb26e527e33ec3.

## E-S010-02 — Accepted static-map integration (2026-10-24)
PR #21 exact head 6326d61fcc8e64bbc869e6394810184026bb9937 passed CI run
40105464672, completed/success; normal merge 1c56b13d66cd68bca6a7763846a0916fae7026ff.
Published tree ee2f5297fca09457e8a1715162791c17e65d9169 equals local checkpoint
8199633 tree, preserved branch. 72 tests and five validators pass. Real graph
replay byte-identical; independent source anchors verified. Author self-audit
under ADR-0005 accepts S010 source-backed static graph with explicit unknowns;
10/88 completed, S011 next. No runtime/dependency/license/scientific acceptance.

## E-S011-01 — Read-only source leads and runtime boundary (2026-10-24)
- Branch sprint/S011-readonly-flow, base cd8c4445024efff28ef2be79faf1de624cccdf58.
  S010 acceptance PR #22 exact head 2a1c2fdf8558bed0c8f2457fb95504e74bfe8b2a
  passed run 40105633489 and merged before S011 entered in_progress.
- Read full S011 contract and owner restrictions. Read-only source-anchor probe
  exit 0: three regular native main candidates, payload hashes match S009, private
  lexical leads saved. No source execution/extraction, target access or dataflow claim.
- Independent full current archive size/SHA-256 check exit 0: designated identity
  unchanged. Private source-lead artifact SHA-256
  0e9e1e28ab6b3987e001983de37a9a8f26b41a97116d61924db9eec364a2e8be.
- Linux x86_64/Python 3.11.15. python -m unittest discover -s tests -v exit 0,
  72 existing regression tests. python scripts/validate_project_docs.py,
  python scripts/validate_repository_boundary.py (175 approved artifacts),
  python scripts/validate_evidence_ledger.py, python scripts/validate_change_control.py,
  python scripts/validate_risk_protocol.py and git diff --check each exit 0.
- Actual legacy working-directory/omitted-input attack NOT RUN: explicit owner
  execution prohibition. Static flow/seed/clock/serializer/outputs not yet verified;
  no synthetic or audit-tool execution substituted. S011 report states missing gates.
- S011 in_progress -> blocked, B-S011-01/R-AUTH triggered. Further static planning
  can be prepared in this sprint, but completion needs the mandatory runtime gate
  with resolving authority/evidence. S012+ untouched. No routine approval requested.
- Blocked-state PR CI/integration does not accept S011. Exact PR/head/merge evidence
  remains available through focused GitHub recovery record. Original worktree intact.
