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

## E-S011-02 — Read-only trace and review-packet verification (2026-10-25)
- Branch sprint/S011-source-bound-plan, base 401b9dd5f1f43de93f5ceb8a82fd0c5956e9a8a4.
- Source regular-payload probes: exit 0, bytes hashed against accepted inventory,
  in-memory source reading only. Reviewed ten source-anchor boundaries plus
  security/dynamics/IPC and JSON input checklist; private metadata retained.
- Packet SHA-256 6a3ee7bc8ae61c8d1060fd9a197e012d9e680f1387e2dd787988b267f2960a41.
  32 native text/build refs, three inputs, five planned cases. No preparation,
  extraction, execution or build; all runtime statuses NOT_RUN.
- python -m unittest discover -s tests -p test_execution_review_plan.py -v:
  exit 1 test-first missing module; then exit 0, seven tests. Original failure
  class/command and source-bound scope documented in S011 report.
- python scripts/validate_execution_review_plan.py
  docs/audit/S011_EXECUTION_REVIEW_PLAN.json --inventory <private S009 manifest>:
  exit 0; VALID_STATIC_PLAN only, execution_authorized=false/runtime_status=NOT_RUN.
- python -m unittest discover -s tests -v: exit 0, 79 tests (prior 72 unchanged).
- python scripts/validate_project_docs.py, python scripts/validate_repository_boundary.py
  (179 approved artifacts), python scripts/validate_evidence_ledger.py,
  python scripts/validate_change_control.py, python scripts/validate_risk_protocol.py
  and git diff --check: each exit 0. Linux x86_64/Python 3.11.15.
- B-S011-01 remains open; preparation/execution scope not expanded by generic
  continuation or a metadata linter. Mandatory legacy runtime gate NOT RUN.
  Source flow/limits/findings and exact proposed cases in S011 source-plan document.
  No S011 completion, later sprint start or scientific/cleared source claim.
- This focused partial-work PR still requires exact-head CI before normal merge.
- Final full-archive verification exit 0: exact designated size/SHA-256 unchanged.
  Private source-boundary metadata SHA-256
  8e2cf68969c6449f2458c7a4bd4baac3a86ec33c4777a64e9af38d9d436d6cec;
  private input-checklist SHA-256
  8a8139c4ddb9ef9f286553186597063189dc3eb03d5917180790d654cfd7d9f2.
  Combined evidence retained in private-evidence/S011/review-packet-evidence-20261025.json.
  Final regression repeat exit 0, 79 tests; all five validators/diff check exit 0.

## E-S011-03 — Review-packet integration and pending authority (2026-10-25)
PR #24 exact head 0b8f37da14ac8bc8b390b4f4724b78ffdf9cce09 passed CI run
40217362016 (completed/success); permitted merge
709ceba97c6a2c34d4d8f31fed0467dc8f93c281. Local checkpoint 523e938 and
published tree both a2184aa687d23f1049e05ce8e414b296fccda28d, equality checked.
79 tests/five validators passed. This integrates static tracing/plan tooling only;
S011 remains blocked, S012+ untouched, 10/88 completed.

Owner was asked for the specific exception described in the review packet:
private disposable preparation of exactly 32 native/build source entries and
three input references outside the implementation repository, trusted-dependency
build of only sw_cosim, and five bounded validation/argument cases. No simulation
or redistribution. No answer/authorization received at this checkpoint; request
acceptance by the question UI is NOT an approval. Source preparation/build/legacy
execution remains prohibited. The published static packet stays historically
false/NOT_RUN even if a later separate execution authority is received.

Prospective host-tool presence checked read-only: cmake, c++, bwrap, unshare and
pkg-config are present. Versions, dependency provenance, actual sandbox behavior
and license permissions are NOT verified by presence. Nothing was installed,
prepared, built or executed from the archive. No unsandboxed fallback is allowed.

If authority is granted later, first record its precise scope, complete prerequisite
source/dependency/license/isolation checks, preserve the archive identity and
execute only approved cases with separate actual execution records. A static-plan
linter is not a permission source or runtime result. Any remaining mandatory gate
keeps S011 incomplete. Original worktree/.vscode and private historical evidence
remain untouched. This checkpoint needs its own exact-head CI for integration.

## E-S011-04 — Owner authority recorded; isolation preflight failed (2026-10-25)

Base origin/main cfcc1e0d8516ca9d1d0e8fd4d701cfbfe16dfd77; branch
sprint/S011-authorized-validation. Original worktree and untracked settings preserved.
Owner explicitly answered yes to the exact isolated private build/five-case plan.
ADR-0007 resolves B-S011-01. State transition: blocked -> in_progress on authority,
then in_progress -> blocked on B-S011-02. Completed count remains 10/88.

Archive full size/SHA-256 and plan SHA-256 reverified with Python hashlib (exit 0).
No source preparation, build, target execution or simulation occurred. All five
legacy cases remain NOT_RUN; source reuse prohibited, models unvalidated.

Trusted-host probes (no archived executable/code):
- `bwrap --version`: exit 0, 0.9.0.
- `bwrap --unshare-user --unshare-net --unshare-pid --unshare-ipc --unshare-uts --die-with-parent --new-session --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind /lib64 /lib64 --proc /proc --dev /dev --tmpfs /tmp --chdir /tmp -- /usr/bin/true`: exit 1, loopback `Failed RTM_NEWADDR: Operation not permitted`.
- Same probe with `--uid 0 --gid 0`: exit 1, same loopback failure.
- Same initial probe without `--unshare-net`: exit 1, `setting up uid map: Permission denied`.
- `unshare --user --map-root-user --net -- /usr/bin/true`: exit 1, `write failed /proc/self/uid_map: Operation not permitted`.
- `docker version --format '{{.Server.Version}}'`: exit 1, daemon socket absent.
- Python shutil.which for firejail/nsjail/podman/runsc: exit 0, all absent.
- Read-only kernel metadata: unprivileged_userns_clone=1, max_user_namespaces=25657,
  apparmor_restrict_unprivileged_userns=1; effective capabilities zero. These are
  observations, not definitive attribution of the denial. No policy changes made.
- Python header/library presence probe: exit 0; OpenSSL header, Catch2 CMake config
  and sumocpp library present; nlohmann/json.hpp and libsumo/Simulation.h absent at
  standard inspected paths. Presence does not verify versions/provenance/licenses.

Platform: Linux 7.0.0-38-generic x86_64, glibc 2.39; Python 3.11.15.
No alternative sandbox backend was found. The approved plan explicitly requires
isolation before any target run; no unsandboxed fallback was attempted. A compliant
execution host is required. Missing dependency provenance remains a prerequisite.
Changed scope: ADR, decision/blocker/handoff/report/validation records and inventory.
No runtime-test success or S011 acceptance is claimed. CI is pending this checkpoint.

Checkpoint verification: `python -m unittest discover -s tests -v` exit 0,
79 tests passed. `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`,
`python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, and
`python scripts/validate_risk_protocol.py` each exit 0; `git diff --check` exit 0.
No production/test code changed; runtime legacy tests remain NOT_RUN.
Full size/SHA-256 verification repeated after preflight, exit 0, unchanged.
Restricted diagnostic/regression records: private-evidence/S011/
authorized-preflight-20261025.md and authorized-preflight-regression-20261025.log.
PROGRESS.json remains accurate: S011 blocked, 10 completed; no completion change.

## E-S011-05 — Authorization/preflight checkpoint integrated
PR #26 head a049f049359dd13739bc415469590a2e1ec400a7 passed exact-head
GitHub Actions run 40219535165 (completed/success). Permitted merge
8b9e1176d2fff33c16cb7962f3ffb44ed58b3810. Local checkpoint bfd5fad and
published tree both 1c40c09e115cb90fe7548d7cd45fcf00a018b67a, equality verified.
Self-audit accepted recovery documentation only, not S011. Owner authority under
ADR-0007 persists. B-S011-02 remains open; all five legacy cases NOT_RUN.
Next executable sprint remains S011 on a compliant execution host; S012 untouched.

## E-S011-06 — Repeatable trusted namespace preflight (2026-10-25)

Base origin/main cc626b34bcc21dd03f39f9c7cfcfbe1ed09fb9d8, branch
sprint/S011-isolation-recheck. PR #27 previously passed exact-head CI run
40219621481 at 564884627219acbe4acd4ab60082e3763b9fbd32 and merged as this
base. Original worktree and settings preserved. S011 remains blocked, 10/88.

Gap: previous isolation failures were manual probes. Added independently authored
scripts/check_execution_isolation.py and ten tests, inventory registrations and
source-flow/handoff/report/validation documentation. The fixed trusted namespace
probe never accepts a legacy target or prepares/runs archive content. A successful
namespace probe cannot set readiness true. Raw diagnostics stay in a new private
mode-0600 report; existing reports/symlinks are refused. All other isolation,
dependency/license and target identity requirements remain unverified.

Commands and observed results:
- `git fetch origin`: exit 0, current main cc626b3; lowest incomplete sprint S011.
- Repeated E-S011-04 Bubblewrap command: exit 1, loopback namespace denial persists.
- `sudo -n -l`: exit 1, password required; no elevated action attempted.
- `flatpak --version`: exit 0, 1.14.6; `flatpak list --columns=application,runtime`:
  exit 0, no installed applications. Packaged flatpak-bwrap helpers absent at the
  two inspected standard paths. No alternative sandbox ready for this plan.
- `pkg-config --modversion nlohmann_json libsumo`: exit 1, packages not found in
  pkg-config search path; this does not prove absence at all possible locations.
- Initial private-parent permission assertion: FAILED before report generation;
  evidence directories were not owner-only. Verified directory ownership/no
  symlinks, set only private-evidence and S011 evidence directory modes to 0700,
  then reran successfully. No archive/source permissions or host policy changed.
- `python scripts/check_execution_isolation.py --report PRIVATE_NEW_REPORT`:
  exit 1, namespace_probe_status BLOCKED, failure_kind NONZERO_EXIT,
  ready_for_legacy_execution false, legacy_cases_status NOT_RUN. Raw error is
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Restricted artifact private-evidence/S011/namespace-preflight-recheck-20261025.json,
  SHA-256 0a32171d13d1e071f973bbf45f29f9c9b1fa405423b392c8d38e1bd9e06f515c.
- Full archive size and SHA-256 reverified by hashlib.file_digest after probe:
  exit 0, designated 487062036 bytes/SHA-256 unchanged.
- `python -m unittest discover -s tests -p test_execution_isolation_preflight.py -v`:
  exit 0, ten tests passed. White-box branch/no-fallback/readiness invariants;
  black-box CLI from another CWD and unsupported target rejection; adversarial
  missing/denied tool, simulated timeout/signals, invalid UTF-8/oversized diagnostic,
  private report overwrite/symlink attacks; seeded generated nonzero-exit cases.
  These are trusted helper tests, not the mandatory legacy runtime attack.

Linux 7.0.0-38-generic x86_64/glibc 2.39, Python 3.11.15, Bubblewrap 0.9.0.
No host security changes, source preparation/build/execution, simulation or reuse.
All five approved actual legacy cases remain NOT_RUN. Owner's ADR-0007 authority
persists. Resume only with demonstrated plan-compliant isolation and verified
trusted dependencies/provenance/licenses. S012 not eligible. CI pending checkpoint;
integration of preflight tooling is not acceptance of S011 or scientific validity.

Final local verification: `python -m unittest discover -s tests -v` exit 0,
89 tests passed, including all previous 79. All five commands
`python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`,
`python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`,
`python scripts/validate_risk_protocol.py` exit 0; `git diff --check` exit 0.
Restricted regression transcript: private-evidence/S011/namespace-preflight-regression-20261025.log.
Initial assertion failure summary retained as namespace-preflight-initial-permission-failure-20261025.txt.
The failing Python helper exited 1; its original combined shell returned 0 because
the subsequent regression command passed. No failed preflight was treated as ready.
PROGRESS.json remains unchanged and accurate: S011 blocked, S012 not_started.

Preflight implementation checkpoint: PR #28 head
cec2c03170463197c8a063159f50a651ee21c436 passed exact-head GitHub Actions run
40220194016 (completed/success). Local implementation checkpoint 7ebc395 and
published tree ff3deb2afddac9591cb99518f113acd49dab480b are identical.
Self-audit found no scope expansion or false execution/scientific claims; accepts
preflight tooling only. This evidence update requires its own exact-head CI before
merge. Integration status and final merge SHA are recorded by PR #28 on GitHub.
B-S011-02 remains OPEN; next required action is a namespace-enabled execution host
and the remaining ADR-0007 prerequisite checks. Do not repeat owner authorization.

## E-S011-07 — Isolated private build and actual validation (2026-10-25)

Base 7440183035c154f79a8a89556f2e1a46bf94876d, branch
sprint/S011-privileged-isolation. Original worktree/settings untouched. State:
blocked -> in_progress after B-S011-02 resolution -> in_review after technical
checks; completed count remains 10 pending exact-head CI/integration/acceptance.

Owner supplied administrator authentication for the disclosed sandbox blocker.
Only sudo/timeout/Bubblewrap setup is privileged; setpriv drops to the owner's
nonzero UID, clears groups/capabilities and sets no-new-privileges before any
compiler/legacy target. No password is saved; no host security settings, services,
sudoers or installed SUMO packages changed. ADR-0008 records this implementation.
Existing policy still blocks the old unprivileged helper; it is not the runner.

Trusted prerequisites:
- `apt-get download sumo=1.28.0-1 sumo-dev=1.28.0-1 nlohmann-json3-dev=3.11.3-1`:
  exit 0, package-index SHA-256 verified; `dpkg-deb --extract` each into a private
  dependency prefix: exit 0. No maintainer scripts or archived dependency binaries.
- Package digests: sumo 53f808c42bd001337de22914a6802117d9dccacda20c1be94ddda2ef919011af;
  sumo-dev 62615b2e9502ec14db5b7e1e7498c12fade4364510f535886d45bd941ae7e78b;
  JSON 85e4e95dc4bdc6034d593e1933ee88e085319fee36cae83c178e8ddc1a66e8fd.
  Configured sources: SUMO stable Launchpad PPA and Ubuntu noble archive; no
  unauthenticated override. Package copyright metadata retained privately (SUMO
  EPL-2.0; JSON MIT metadata). Existing Catch2 3.4.0/OpenSSL 3.0.13 system packages
  supply separate dependencies. Third-party/legacy provenance remains unapproved
  for redistribution/reuse; private owner-authorized audit is the only purpose.
- `python scripts/probe_private_sandbox.py PRIVATE_ROOT --label verified5`: exit 0.
  Trusted independent C fixture: security/memory probes exit 0; CPU probe exit 137,
  file-size probe 153, watchdog probe -9. Those signals are expected enforcement,
  not successful target executions. Evidence binds wrapper/fixture and raw hashes.
  Fork/vfork/clone/clone3, repeated execve, execveat, networking all denied; actual
  target UID nonzero, effective caps zero, no-new-privileges, mounts read-only.

Preparation/build:
- Bounded private copy helper under `prlimit --as=268435456 --cpu=120 --core=0`
  and `timeout --signal=KILL 120`: exit 0, exactly 32 approved native/build texts
  plus three approved JSON/XML inputs. Full archive hash before/after, gzip CRC,
  TAR membership, payload hashes and output paths verified; links never copied.
  Archive is unchanged. Private locator remains only in Git metadata.
- `python scripts/execute_private_validation.py build PRIVATE_ROOT`: configure
  command `cmake -S /source -B /build -DSW_BUILD_COSIM=ON` exit 0; build command
  `cmake --build /build --target sw_cosim --parallel 2` initially exit 2.
- Cause: BLAS/LAPACK links traverse /etc/alternatives; missing/unsearchable sandbox
  /etc caused linker dependency errors. First mount-only retry also exit 2;
  explicit sandbox /etc traversal permission correction resolved it. No source
  patch. `python scripts/execute_private_validation.py resume-build PRIVATE_ROOT`
  final retry exit 0 (make exit 0). Original logs/receipts preserved.
- All build attempts combined: 13.137115927 seconds, below cumulative 300-second
  wall/CPU budget; one CPU affinity, per-process 1-GiB address space. Binary SHA-256
  939c2bd50379e557936f0adb944dfe1e38fbad9428be8c738b6493b198097fd3.

Runtime results (exact commands after binary; all under guarded_target):

| Case | CWD | Arguments | Actual exit | Result |
|---|---|---|---|---|
| ABS_A | /A | --validate-config /inputs/config.json /A/city_fixture | 0 | PASS |
| ABS_B | /B | --validate-config /inputs/config.json /A/city_fixture | 0 | PASS |
| REL_A | /A | --validate-config /inputs/config.json city_fixture | 0 | PASS |
| REL_B | /B | --validate-config /inputs/config.json city_fixture | 1 | expected missing-city error |
| MISSING_CITY | /A | --validate-config /inputs/config.json | 2 | expected usage error |

`python scripts/execute_private_validation.py cases PRIVATE_ROOT --attempt serialdeps`:
exit 0. Exact five case IDs, one corrected bounded batch, not new test scope.
Each case used 10-second root watchdog, 5-second CPU, 256-MiB address space,
1-MiB captured-stream file limit; /tmp and /dev/shm each bounded 16 MiB. Raw stderr
includes tracer lines and is preserved as stderr-with-trace, not misrepresented
as target-only stderr. No host-writable target mounts. Hash checks after every
case found all 35 copied input/source files and binary unchanged.

Three successful stdout bytes are identical, SHA-256
5ff2ec170631e7e921f468e13e0101bc55f2047ebd3fd05d3703c5318a177c32.
Parsed status/policy/seed/map-default/bin-count/profile fields match private input
and source-bound predictions. This tests input-to-validation-artifact flow and
actual CWD attack; it does not test ordinary simulation dynamics or clock coupling.

Failures retained (never counted as passing): initial ABS_A exited 130 because
OpenBLAS initialization attempted denied clone3 and raised SIGINT. Set only trusted
dependency environment OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1, retained all
denials, reran probes and the same five cases under authorized failure recovery.
Five distinct case IDs, six total legacy invocations including the failed attempt;
max_cases=5 per batch and every per-attempt cap unchanged. No unbounded retries.
Earlier trusted probe found occurrence-delayed exec injection permitted an extra
exec; removing the delay fixed it before any legacy target. Another probe exposed
non-writable /tmp and an expected watchdog -9 misclassified by the probe checker;
fixed namespace tmpfs permissions/explicit signal expectations, kept failed logs.
All these are engineering findings, not scientific evidence.

Evidence: public docs/audit/S011_VALIDATION_EXECUTION_SUMMARY.json contains only
sanitized counts/status/hashes. Private Git common metadata private-evidence/S011/
runtime20261025 holds original build/probe/case logs and receipts; runtime summary,
copy/dependency bootstraps and regression transcript also retained privately.
Private worktree locator codex-s011-execution.json is never committed. Hashes of
principal receipts are in the public summary; canonical hashes prove consistency,
not authorship, security clearance, licensing or model accuracy.

Verification: `python -m unittest discover -s tests -v` exit 0, 105 tests passed
(all prior 89 plus 16 new synthetic white-box/black-box/adversarial/generated/
regression tests). Tests cover links/traversal/case-collision, CRC/hash corruption,
staging/decompression limits, immutable sources, private capture, stale enforcement
receipts and cumulative retry accounting. Actual trusted probes independently
exercise namespace/runtime boundaries. Full archive size 487062036 and SHA-256
reverified after execution (exit 0), unchanged. No archived binaries/scripts,
normal simulation, ONNX/training or historical campaign replay executed.

Platform Linux 7.0.0-38-generic x86_64 GNU/Linux, Python 3.11.15 (CMake finds system
Python 3.12.3), GCC 13.3.0, CMake 3.28.3, Bubblewrap 0.9.0, strace 6.8, setpriv
util-linux 2.39.3. Scope is tested Linux x86_64 only; Windows runtime NOT RUN and
not advertised as validated by this audit. Scientific models remain UNVALIDATED;
source reuse/redistribution PROHIBITED. Full-run seed replay/empirical validity,
comprehensive malformed-input coverage and simulation metrics remain untested.
Next sprint S012 is ineligible until S011 permitted acceptance/integration.

Final governance verification: `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`, `python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, `python scripts/validate_risk_protocol.py`
all exit 0; `git diff --check` exit 0. Self-audit checked changed-file scope,
no source/binary/private paths/credentials, parameter separation and no scientific
clearance claims. All mandatory S011 gates pass locally; CI/integration pending.

## E-S011-08 — Sole-maintainer acceptance after CI/integration (2026-10-25)
PR #29 exact head 6b198976a62be198ad6265012024c98cc0ed94e6 passed GitHub
Actions run 40224316143 (completed/success), including 105 tests and mandatory
repository checks. Permitted merge 4339fae73884632126303e1a520fc27847f87182.
Local checkpoint 5b0bc99eb3db6c798194894fafb20e342d9e2edf and published tree
695345cbb28ec2a06c167cbd6366f8ac1cb65a59 verified equal before merge.
Author self-audit under ADR-0005 accepts S011's source execution/data-flow map and
bounded actual validation contracts. No independent-person review is claimed.

Acceptance: source/hash/line-bound entry/input/state/clock/RNG/serializer/writer
map reviewed; actual deterministic fixture output matches source/input predictions;
ABS_A/B exercises different CWD with invariant absolute inputs, REL_B exposes
relative-path failure; usage error observable. Synthetic negative/property and
actual security/resource tests pass. Original failures and residual risks remain
in E-S011-07. Full archive and 35 copied files/binary unchanged. No source reuse,
redistribution, normal simulation or physical/scientific validation accepted.
All applicable S011 gates satisfied; in_review -> completed; 11/88 completed.
Next eligible sprint S012 (not_started); fetch and read its complete contract.
This acceptance-record commit still needs its own exact-head CI before integration.

## E-S012-01 — Concrete scope review and fail-closed evidence checker (2026-10-25)

Base 7bfa6c45afe1058bf6c2e99156f88f73ac7c7e30; branch
sprint/S012-baseline-review. S011 acceptance PR #30 exact head
979fb80ddc14227e4b3d15ab3831ff62f3199de1 passed CI run 40224443484
(completed/success), merged as this base; tree f4fdb54bcd39aeae53314450ec948d9e6b7cda32
matches local checkpoint 8cedd4b. S001–S011 completed, 11/88. S012 transitions
not_started -> in_progress on contract review -> blocked on B-S012-01.
Original worktree/settings/historical progress preserved; S013+ untouched.

Exact gap: full S012 contract requires actual baseline reproduction or a genuine
failed-reproduction attempt and a second operator's copyable evidence. S011 only
executed configuration/argument validation. ADR-0007 explicitly excludes normal
simulation; administrator authentication does not expand that scope. No normal
baseline was attempted and NOT_RUN cannot be called failed reproduction.

Changed files: proposed ADR-0009; audit review Markdown/JSON; independently written
scripts/validate_baseline_result.py and tests/test_baseline_result.py; this report,
progress/handoff/blockers/validation log and repository inventory. No legacy source,
archived results/private paths/credentials/binaries are published. No simulator or
scientific model implemented. Current runtime evidence remains S011 only.

The plan binds the unchanged S011 binary/source/input identities and proposes two
same-seed normal runs with isolated fresh output tmpfs at one namespace path,
120-second wall/60-second target CPU/1-GiB address-space caps per attempt, 64-MiB
output/count/file limits and at most one preserved corrective retry per run.
No launch authority or baseline-ready sandbox/exporter is claimed. Existing
validation-only runner is not an authorized normal-run fallback. Read plan and
ADR-0009 for full prerequisites/exclusions before any execution.
Plan SHA-256 5a8ef0be672f616bd9c40e68db4ea431e82dbb54c7dcea3ac31dd18bfb893187.
Observed scenario shape is 12 bins/two trucks, 600 simulated seconds/0.1-second
step. These are owner archived scenario settings, not calibrated physical facts.
Current-code audit would use trusted private SUMO 1.28.0-1, not recreate unknown
historical campaign environments. No historical output or measurement invented.

White-box/source reference: entry-00010836:181,870 binds run ID to output basename;
27–28,197,950 binds simulation_runtime_seconds to a steady-clock microsecond helper
scaled by 1e6. A preregistered comparison excludes ONLY that host-duration summary
field; raw bytes/hashes/differences remain retained. All other summary fields and
all raw event bytes compare without removals/tolerances. Event header source has
run_id, seed, kind, time_s keys. These are source observations, not actual normal
runtime proof or physical-model acceptance.

Tests/commands:
- `git fetch origin`: exit 0, verified accepted S011 and no competing S012 work.
- `python -m unittest discover -s tests -p test_baseline_result.py -v`: exit 0,
  eleven synthetic tests pass. Negative cases: missing dependency, no attempt,
  nonzero/signal/timeout exit, absent/empty/failure artifacts, links, wrong IDs,
  validation-only flag, duplicates/nonfinite/malformed JSON and resource budgets.
  Property/reference checks retain all raw bytes and distinguish only the stated
  host-runtime projection from an altered semantic field. Black-box CLI tested
  from another CWD; it never launches legacy code. These are NOT normal-run tests.
- `python -m unittest discover -s tests -v`: exit 0, 116 tests passed (all prior
  105 plus eleven new). Raw transcript private-evidence/S012/review-regression.log.
- Normal BASELINE_A/B, baseline sandbox/exporter adversarial probes and full-run
  determinism: NOT RUN. Required S012 gate remains open; no fake second operator
  or independent review and no scientific/physical validation claimed.

Environment: Linux 7.0.0-38-generic x86_64 GNU/Linux, Python 3.11.15. Windows
normal-baseline NOT RUN. Blocker B-S012-01 requires explicit owner authority for
proposed normal-run scope; then implement/verify all remaining technical gates,
retain actual outcomes, run checks/exact-head CI and integrate before acceptance.
Do not start S013. Original source archive remains unchanged; no new legacy target
execution/copy/source patch during S012 preparation. Self-audit accepts only the
review artifact/checker, not sprint completion. Publication CI pending checkpoint.

Final local governance checks: `python scripts/validate_project_docs.py`,
`python scripts/validate_repository_boundary.py`, `python scripts/validate_evidence_ledger.py`,
`python scripts/validate_change_control.py`, `python scripts/validate_risk_protocol.py`
all exit 0; `git diff --check` exit 0. Scope audit found only S012 preparation,
synthetic tests and governance records; no private material or claimed normal run.

## E-S012-02 — Review/checker CI provenance
PR #31 initial exact head 5879de1f9fc2d301da70a2701248bca7566a9865 passed
GitHub Actions run 40225369631 (completed/success), including 116 tests. Local
checkpoint 5be922133fb64bb3395c382a898d45d21954c215 and published tree
9688dd4915026d6f330a57a918710fee27af4f54 match. Owner scope question was
presented for the exact plan, but no owner answer at this checkpoint; a queued
question is not approval. ADR-0009 remains Proposed and all normal runs NOT_RUN.
This receipt needs its own exact-head CI before integration; final status/merge
SHA is recorded on PR #31. Integrating preparation does not accept S012.

## E-S012-03 — Authorized attempts; explicit failed-reproduction report (2026-10-26)

Base 4865de107d4e4be3b77e2e07240b2769de8e18f0, branch
sprint/S012-authorized-baseline. PR #31 final head
9cef239ed7c087d57551dcf02e1da8d3d7f2b454 passed exact-head CI run 40225464063,
then merged as this base. Owner explicitly answered yes to two bounded private
baseline runs/one corrective retry each; ADR-0009 Accepted, D-0013/B-S012-01
resolved. Approval persists; static review JSON remains historically false/NOT_RUN.
S012 blocked -> in_progress -> in_review; completed count stays 11 pending CI and
integration. Original worktree/settings and historical evidence remain preserved.

Deliverable selection: S012 explicitly permits a “Baseline reproduction record or
explicit failed-reproduction report.” This checkpoint supplies the latter. A normal
baseline has NOT passed. No route, determinism or scientific acceptance is claimed.
The original success criteria/checker remain unchanged despite failing outcomes.

Files changed: accepted ADR-0009; independently authored baseline_commands.py,
baseline_supervisor.py, baseline_transport.py, run_private_baseline.py; synthetic
C fixture and transport/runner tests; sanitized S012_BASELINE_OUTCOME.json; progress,
handoff/blockers/decision/report/validation/inventory records. No legacy source,
binary, raw events/metrics, private paths or credential is published.

Execution mechanism: unchanged S011 read-only input/source/binary and trusted
private dependencies. Privileged trusted timeout/Bubblewrap setup then nonroot UID,
zero capabilities, cleared groups/no-new-privileges. No host security policy or
service changes. Target cannot network/fork/exec/create threads, use ptrace,
unshare/setns/io_uring setup. Only /outputs (64MiB tmpfs), /tmp and /dev/shm (16MiB
each) are writable; no writable host target mounts. Target AS 1GiB, CPU 60s, file
16MiB. Supervisor child deadline 100s leaves export reserve under outer 120s wall
watchdog. One CPU affinity inherited. Address-space bounds are not aggregate
cgroup RSS guarantees. Export has 64-entry/64MiB data bounds; encoded packet cap
90,000,000 bytes accounts for base64 metadata overhead, never additional target
data. Private regular-file capture prevents unbounded parent pipe-memory growth.

Trusted exporter waits for target termination, rejects traversal/duplicates/case
collisions/links/special files/changed members/oversized data, checks hashes, and
exclusively publishes into a fresh owner-only evidence directory. Complete export
is separate from successful target exit/artifact validation. All raw failures stay.

Commands/results (PRIVATE_ROOT resolves only through Git common metadata locator):
- `python -m unittest discover -s tests -p 'test_baseline*.py' -v`: exit 0, 21 tests.
  New transport/runner tests plus existing eleven baseline-result negatives.
- `cc -O0 -Wall -Wextra -Werror ... tests/fixtures/baseline_fixture.c`: exit 0.
  Trusted fixture only; no legacy implementation copied into tests.
- `python scripts/run_private_baseline.py probes PRIVATE_ROOT`: initial exit 1;
  quota actually enforced but final marker could not be written into full tmpfs.
  A mistakenly zero-size last-file cleanup freed no space. Readiness packet absent.
  Initial BASELINE_A CLI preflight then failed before attempt marker/legacy launch;
  this is NOT a normal simulation attempt. Full original failed probe/code retained.
- Corrected fixture frees its known 8MiB quota0 file after ENOSPC before marking
  success, without weakening the quota or expected outcome. Rerun with new labels,
  preserving originals: seven probes pass. Fixture/security/memory/quota target
  exits 0; CPU/file signals -9/-25 and inner timeout -9 are expected enforcement,
  not successful baseline results. Corrected readiness packet binds all tool and
  fixture hashes. Actual namespace and raw-export round trip exercised.
- Preflight full archive size/SHA-256 verified before normal attempts (exit 0).
  S011 source/input/binary and trusted package digests checked before/after each.
  129 actually loaded shared-library hashes captured and unchanged after both.
- `python scripts/run_private_baseline.py run PRIVATE_ROOT --run-id BASELINE_A`:
  runner exit 1; actual normal target exit 3, termination exited; complete export;
  wall 0.465345662s. `... --run-id BASELINE_B`: runner exit 1, target exit 3,
  complete export, wall 0.365409602s. Exact argv for each:
  `/build/sw_cosim /inputs/config.json /A/city_fixture /outputs/baseline`, CWD /A.
  Separate fresh output tmpfs, same namespace basename/run ID and configured seed.
- Exactly two normal invocations, zero corrective retries. No input/source patch,
  changed horizon/fleet, rebuilt target, expanded resource limit or campaign replay.

Observed failed outcomes:
Both return route_complete=false and emit run_summary.json/events.jsonl. No
failure.json; this is source-declared noncompletion exit 3, not a hidden successful
run. The prepared validation_only=false criterion was an incorrect assumption:
normal source entry-00010836:952 emits true literally. Keep this conflict recorded;
actual normal CLI/loop execution is distinct from that summary label. Never change
the output/test merely to fit the assumption. Scientific models remain UNVALIDATED.

Each event file contains 2261 JSON rows. Raw bytes/hashes differ. Row-aligned JSON
diff found only /signing_wall_us (25 transmissions), /crypto_verification_wall_us
(25 receives), and /simulation_runtime_seconds (one summary event). Source anchors
entry-00010836:498,394,950 respectively identify host timing fields. Raw-event
replay criterion FAILED; no post-hoc event normalization was introduced. Summary
raw hashes differ only at simulation_runtime_seconds; the preregistered projection
matches (cc96a4022ec4214d594216f977210049e46fce0f74219b70f80f17bfdcb11606).
This explains bounded software differences, not physical accuracy or robustness.

Raw event hashes A de3031373087b688c6344d61aad1f3ee63da33eebb99275589a134222b3a52f4,
B a8eb0e2a232b099971f0de52466c5f57628c1068243deec5162d48edddcb12e3.
Full sanitized hashes/status/difference inventory: docs/audit/S012_BASELINE_OUTCOME.json.
Raw packets/streams/source fixtures/results are restricted under Git common
metadata private-evidence/S012/runtime20261026; root locator remains private.
Hash/diff/dependency manifests also private-evidence/S012. Never commit raw outputs.

Failure/report integrity: actual checker returns false for both nonzero targets,
so their complete exports are NOT accepted as successful simulations. Synthetic
negative tests also reject missing dependencies, absent outputs, nonattempts,
malformed/duplicate/nonfinite JSON, invalid identifiers, links and size budgets.
No fake second operator/reviewer; documented protocol lets a second operator attempt
independently if supplied the private designated inputs and same approved authority.

`python -m unittest discover -s tests -v`: exit 0, 128 tests passed (all prior 116
plus twelve new transport/runner/property tests). Actual trusted enforcement probes supplement
unit tests. Normal success/replay criteria failed as above; the failed-report
alternative remains subject to self-audit, exact-head CI and permitted integration.
Archive after normal runs: full 487062036-byte SHA-256 unchanged (exit 0); source,
inputs and binary unchanged. Existing package provenance/license constraints stay;
no source reuse or redistribution authorization. Linux x86_64 only; Windows actual
baseline NOT RUN. Python 3.11.15 supervisor system Python3.12.3; compiled S011 GCC
13.3.0/SUMO1.28.0-1/OpenSSL3.0.13; tool versions retained from S011 and private logs.

Known findings F-S012-01 must carry to later audit/model gates. S012 is not a
successful-model acceptance. Next S013 only after this sprint's report gates and
integration; do not run archived tests/scripts or historical campaigns under the
baseline-only exception. No new approval needed for already authorized work.

Final scope/self-audit: tests now include seeded arbitrary-byte transport/member
order invariance and parent-directory case collisions. All 128 tests pass; both
normal baseline attempts remain failed, not reclassified. Five governance commands
`python scripts/validate_project_docs.py`, `python scripts/validate_repository_boundary.py`,
`python scripts/validate_evidence_ledger.py`, `python scripts/validate_change_control.py`,
`python scripts/validate_risk_protocol.py` exit 0; `git diff --check` exit 0.
No source copy/patch, secret, private path, raw legacy output or false scientific
claim found in publication scope. Accept only the contract's failed-report
alternative after exact-head CI/permitted integration. Successful-baseline/model
acceptance remains absent. Final regression transcript retained separately.

## E-S012-04 — Acceptance of failed-reproduction audit deliverable (2026-10-26)
PR #32 exact head cdafda62f5106a621fa958c7e02e094761b39c68 passed CI run
40369769249 (completed/success; 128 tests/mandatory checks) and permitted merge
2cdc1b8d4bf69d7197b59975cdee38a63be8f33a. Local checkpoint
c13533025b682f1248f1220e209f767a22852a19 and published tree
77efec03ae5dc9d28d526b54ceccb7b5772a43d8 matched before merge.

Owner-authorized self-audit under ADR-0005 accepts S012's explicitly allowed
“failed-reproduction report” alternative. All report-integrity/security/unit/
negative/reproducible-command evidence gates pass. Both normal attempts still
FAIL successful-baseline criteria: exit3/incomplete route/true validation marker/
raw event differences. No failed simulation is relabelled passing, criterion
weakened or physical model accepted. F-S012-01 stays a known negative finding for
later source/model/defect audits. A successful normal baseline remains absent.
S012 in_review -> completed as audit deliverable; 12/88 sprints completed.
Next S013 not_started; fetch/review its contract before proceeding. This acceptance
record needs its own exact-head CI before permitted integration.
