# ADR-0006 — Quarantine and continue for private inventory

- Status: Accepted
- Date: 2026-10-22
- Related sprint(s): S009; later read-only audit consumers
- Decision authority/method: explicit owner policy amendment; author self-audit under ADR-0005
- Replaces: stop-on-first-suspicious-entry inventory policy only; extraction/reuse prohibitions remain

## Context
The designated immutable archive contains an escaping symlink. Stopping metadata
inventory at that point hides later members without improving isolation when no
link can be opened. Owner explicitly authorizes recording/quarantining such
entries and continuing whenever parsing stays safe. No new baseline is authorized.

## Options considered
Keep stopping on suspicious metadata; extract/filter/rebuild the source; or keep
the original bytes and quarantine entries in a private streaming inventory. The
first leaves technical inventory incomplete, the second violates authorization.
The third supplies evidence without executing, extracting or redistributing code.

## Decision
Continue parsing bounded regular payloads and member metadata after suspicious
entries. Every link and special member is metadata-only, quarantined and never
passed to payload access. Traversal names, duplicates/case collisions, executable
flags, nested archives, binary/signature findings quarantine entries without
ending a parseable inventory. All colliding entries are marked, including earlier
occurrences. Nested archives are never opened. No filesystem member is created.

Manifest version 2 separates completed/incomplete inventory, security findings,
entry quarantine, security clearance (not granted), reuse (prohibited) and model
validation (unvalidated). CLI 0 means completed inventory even with quarantine;
CLI 1 means incomplete or invocation failure. This is an intentional public-tool
contract change from version 1; old private evidence remains immutable. Consumers
must check these distinct fields, not infer permission from complete/exit 0.

## Evidence and assumptions
Owner scope: read-only local audit of LEGACY-CANDIDATE-001, expected SHA-256
 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8
and compressed size 487062036 bytes, unchanged. Existing E-S009-02/03 preserve
the prior stop and rejected link. New tests exercise beginning/middle/end links,
consecutive quarantines and valid later payloads, corruption and resource limits.
No checksum or passing software test establishes scientific validity or license.

Only Linux hostile-input CLI is supported here. It enforces CPU/address-space
hard limits and expanded/compressed/member/metadata/count/wall-time limits from
external JSON. Unit-level library callers must supply equivalent process limits.
Standard TAR logical entries are inventoried; bounded GNU/PAX metadata may change
the resolved name. Sparse reconstruction is unsupported and stops incomplete.
Corrupt parsing, unverified TAR termination/CRC, resource exhaustion, baseline
mismatch or before/after hash/stat mismatch are fatal incomplete results, never
ignored as quarantine. No guess about an unparseable member's payload is made.

## Consequences
Raw names/targets and member metadata stay in restricted private manifests.
Canonical JSON SHA-256 detects accidental manifest changes, not forged authorship.
Hash every regular member within budgets; link/special hashes remain null with
explicit type. Immutable archive hash and unique ordered entry IDs preserve
provenance even for duplicate names. Quarantine is an audit disposition, never
security clearance. License/source provenance gaps prohibit reuse/redistribution
and are tracked separately from technical ability to inspect privately.

## Validation and revisit conditions
Require the original 54 regression tests plus white-box, public CLI, adversarial,
generated property/reference and archive-immutability checks. Real inventory must
complete under limits, verify designated identity before and after, retain private
integrity-protected evidence and disclose all findings. Exact-head CI and permitted
merge are required for sprint acceptance. Revisit on parser/resource bypass,
manifest inconsistency, unexpected source changes or any proposed extraction,
execution/reuse/publication. Such actions remain outside this authorization.
