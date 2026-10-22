# S009 — Legacy source inventory protocol (BLOCKED)

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
