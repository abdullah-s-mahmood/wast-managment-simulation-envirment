# Clean-room boundary and legacy intake protocol

Authority: ADR-0001, AGENTS.md sections 5–8, accepted ADR-0005. This is a
repository separation protocol, not a legal certification or scientific validation.
No legacy bundle has been inspected by S002.

## Repository classes
`REPOSITORY_INVENTORY.json` version 1 explicitly lists each permitted path:
governance documents/configuration, governance Python source, synthetic tests,
and reserved-layout README files. No domain implementation, measured dataset,
legacy source, binary, cache or generated simulation result is admitted at S002.
Later sprint additions must update the inventory with scope/provenance rationale;
listing a path alone never approves its content, license or scientific claims.
Git ignore rules prevent accidental staging only; they do not authorize contents.

`python scripts/validate_repository_boundary.py` checks tracked plus nonignored
untracked files, including explicitly tracked ignored paths. It rejects unknown
paths, missing inventory entries, symlinks, binary/non-UTF-8 content, forbidden
artifact locations/types and a bounded set of credential/local-path signatures.
Errors name the file and finding class without printing matched values. The check
is read-only and exits 1 on invalid inventory or content; it creates no results.
It cannot identify every copied algorithm or every credential format. Self-audit
of diffs/provenance remains mandatory. Do not broadly exempt test/source files.

## Intake sequence (later source audit; S009 owns bundle inventory)
1. Register an intake ID, authorized public/private handling, source owner,
   acquisition date in UTC, source version/commit, archive SHA-256, file hashes
   and declared license status. Missing license means reuse is unavailable.
2. Keep the original bundle outside the implementation repository in a
   separately controlled read-only evidence location. Use an opaque evidence
   reference in public records; never publish workstation paths or private data.
   Do not run legacy executables, scripts or hooks merely to inspect an archive.
3. Inspect archive names/types before extraction. Reject traversal, absolute paths,
   symlinks/hardlinks, special devices, encrypted/unsupported contents or unexpected
   size expansion. Bound storage/time before any authorized sandbox extraction.
   This protocol does not implement an archive extractor.
4. Audit source read-only. Record exact file/function/line and source hash for
   each finding. Separate “observed in legacy code” from “reported by a source”,
   mathematical derivation, scenario input, provisional assumption and tested result.
   Record a minimal factual description, not copied implementation text.
5. Quarantine suspected secrets/private data; do not print, commit or execute them.
   Preserve original evidence under its access policy. Log a redacted blocker and
   stop affected intake; do not delete the owner's source bundle.
6. Translate findings into requirements and independently written contracts/tests.
   Observed legacy outputs are not calibrated physical reference measurements.
7. Any proposed reuse requires an explicit ADR with origin/hash, license and
   attribution review, minimal scope, alternatives, behavioral comparison and
   acceptance evidence. Until adopted through permitted checks/integration,
   copying remains prohibited. Scientific models retain their separate evidence gate.

## Failure, recovery and dimensions
Incomplete intake remains incomplete; no partial extraction or missing provenance
is relabelled accepted. Preserve failure diagnostics and hashes in the restricted
evidence store. Resume only after the recorded blocker is resolved. Roll back
repository changes with a normal revert, not deletion/history rewriting.
File hashes are SHA-256 hex; file sizes use bytes; dates are UTC acquisition
timestamps, not simulation time. Exact runtime schemas remain future sprint work.
No physical units, equations, seeds or numeric scenario defaults are introduced.

## Bounded S002 self-audit
Inventory checks classify bootstrap/governance source, data/configuration and
reserved layout. Synthetic attacks cover legacy source, generated results,
credentials, machine paths, binary artifacts, corrupt manifests and symlinks.
CI checks an actual checkout. All tests are author-run software checks under
ADR-0005; no independent-person review or empirical validation is claimed.
