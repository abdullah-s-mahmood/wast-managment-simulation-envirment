# S009 — Legacy source inventory protocol

Current: in_review; full quarantine inventory completed, replay/CI/integration
recorded below. Earlier blocked reports are historical evidence, retained intact.

Date 2026-10-22 Asia/Baghdad. Branch sprint/S009-legacy-intake.
Base 072c6d55ea4979a0c263edc61a0efcdbf827abbe. Evidence E-S009-01;
blocker B-S009-01, monitored risk R-LEGACY. S009 is NOT completed.

## Entry and source check
S008 implementation PR #14 head 87d26f2c10b9616dcb70d264a77962b07bda300d
passed CI run 39712069254 and merged cd5a5ce51e67885f35db3939478d8b6af8171969.
Acceptance PR #15 head 76caaf3d75a345da5b8f38e7fc1335b92fa4fa88 passed run
39712172260, merged 072c6d55ea4979a0c263edc61a0efcdbf827abbe. S001–S008
are completed (8/88), so S009 entered in_progress legitimately.

Read complete S009 and CLEAN_ROOM_BOUNDARY.md. Exact gap: no owner-designated
immutable legacy baseline or verified audit/publication handling record exists.
Read-only searches found local candidate archives/trees; a dated audit archive
has a checksum sidecar. Availability is established for that candidate, not its
selection, provenance/license status or complete safe intake. Do not conflate
“located candidate” with “accepted source”. No source code was extracted/copied,
executed, scientifically interpreted or published.

## Exact metadata observations
- Opaque evidence reference LEGACY-CANDIDATE-001 (private locator retained only
  in Git metadata file codex-legacy-candidates.json; no workstation path published).
- Compressed size: 487062036 bytes.
- Archive SHA-256 computed with hashlib.file_digest and matching local sidecar:
  da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8.
- Read-only tarfile r|gz header inspection bounded to 1000 members and 512 MiB
  declared total. Stopped at 1000-member limit; NOT a complete inventory or safety
  verdict. The candidate mixes source/test headers, generated results and nested
  archived outputs. No member contents were read/extracted. No unknown binary,
  secret, license or traversal clearance is claimed. Initial console listing was
  truncated by output limit; summary above is bounded observed metadata only.
- Local facts command (metadata only, no legacy execution):
  python - <<'PY'
  from pathlib import Path
  import hashlib, json, subprocess, tarfile
  gitdir=Path(subprocess.check_output(['git','rev-parse','--git-dir'],text=True).strip())
  entry=json.loads((gitdir/'codex-legacy-candidates.json').read_text())['LEGACY-CANDIDATE-001']
  path=Path(entry['local_path'])
  print(path.stat().st_size)
  with path.open('rb') as stream: print(hashlib.file_digest(stream,'sha256').hexdigest())
  with tarfile.open(path,'r|gz') as archive:
      total=0
      for count, member in enumerate(archive):
          if count>=1000: break
          total+=member.size
          if total>512*1024*1024: break
  PY
  Original equivalent metadata probe exited 0; no extraction was requested.
  The checksum read printed a local locator in console only; it is not committed.

## Blocker and next safe action
B-S009-01: owner must identify which candidate repository revision/archive is the
intended legacy execution baseline and specify access/publication restrictions.
Verify source-owner/provenance and declared license before reuse; unknown reuse
rights prohibit copying, and private material cannot be committed just because it
is locally readable. This is a source/handling ambiguity, not a routine request
to continue or a requirement for a second reviewer. Owner asked asynchronously.

Stop intake at metadata; preserve candidate bytes and sidecar. No deletion,
permission change, extraction or legacy execution. Resume only after designation
and handling evidence is recorded; then implement/test bounded safe inventory
manifest/checklist with traversal/duplicate/secret/unknown-binary attacks and
full per-file hashes/sizes/language/role/provenance classification. S010–S088
remain not_started. No synthetic success can replace missing real intake evidence.

## Verification status and changed scope
Only progress, handoff, blockers, validation log, inventory, R-LEGACY trigger status
and this report change.
No new behavior, ADR or scientific parameters. Local regression commands/results
E-S009-01. WB/BB/attack/reference/integration tests for actual S009 inventory:
NOT RUN — no implementation or designated/cleared source intake. Gate remains
open. Existing governance regression is not proof of archive safety or license.
Linux x86_64/Python 3.11.15; no Windows/simulator/scientific validation run.

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

Current amendment file scope: scripts/inventory_legacy.py;
tests/test_inventory_quarantine.py; docs/audit/INTAKE_PROTOCOL.md and
intake_limits.json; docs/adr/ADR-0006-quarantine-only-inventory.md;
docs/CLEAN_ROOM_BOUNDARY.md; docs/REPOSITORY_INVENTORY.json;
docs/quality/risks.json; STATE/PROGRESS.json, AGENT_HANDOFF.md, BLOCKERS.md,
DECISION_LOG.md, VALIDATION_LOG.md and this report. No legacy content included.
Final local suite 63 tests, all five validators (169 inventory artifacts), and
whitespace check exit 0. Author verdict: local S009 technical gates satisfied;
exact-head CI and permitted integration required before completed. Next: S010.

## E-S009-06 — Accepted technical inventory integration
PR #19 head 0c42f4300c62d7870b2b60caa7f382e880e4da6f passed CI run
39743742012, completed/success; permitted merge 6ad9e513bcfa239b702eac10f74773702e52076b.
Local checkpoint ac9fd71 tree equals published f20b55ab3ff297acbe372d52668dcf47e6ceabab.
Author self-audit under ADR-0005: S009 technical inventory/protocol criteria met;
9/88 completed, S010 next. Full inventory/replay, 63 tests and five validators pass.
No archive safety, execution, reuse, licensing or scientific validation is accepted.
B-S009-02 resolved; security findings and quarantine dispositions remain recorded.
