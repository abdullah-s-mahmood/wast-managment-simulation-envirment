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
