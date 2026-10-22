# Private legacy inventory — quarantine policy version 2

Authority: owner amendment and ADR-0006. This replaces the historical version-1
stop-on-suspicious-entry inventory policy. It does not authorize filesystem
extraction, execution, archive reconstruction, copying/reuse or redistribution.

Designated LEGACY-CANDIDATE-001: compressed size 487062036 bytes; SHA-256
 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8.
Use the private locator in Git common metadata codex-legacy-candidates.json.
No alternate baseline may silently replace it. Copyright/source revision/license
remain unverified; source reuse and redistribution remain prohibited.

## Inspection and resource boundary
Run the Linux CLI with explicit docs/audit/intake_limits.json and both expected
identity arguments. Byte caps cover compressed data, each regular member,
expanded bytes including metadata/padding/skips and metadata headers. Counts,
wall-clock seconds, process CPU seconds and address-space bytes are bounded.
The CLI enforces process limits; library callers require equivalent isolation.
A 1 GiB member byte cap allows chunk hashing a measured 730476900-byte generated
output; memory stays capped at 256 MiB, cumulative expansion at 4 GiB, CPU and
wall-clock at 120 seconds each. This is resource policy, not scientific data.
Changing a cap requires documented measured need and retained exhaustion tests.

Inspect logical TAR entries through bounded GZIP/TAR streams. Hash regular
payloads in 65536-byte chunks; never extract/extractall. Every link and special
member is recorded and quarantined without payload access, target opening or
filesystem materialization. Record raw name, ordered unique entry ID, TAR type,
size, link target when relevant, lexical reasons, role/language hints and flags.
Names/targets are metadata only, never joined to an output filesystem path.
Traversal/absolute/Windows paths, duplicate/case-colliding names and suspicious
entries are quarantined; all colliding occurrences are marked. Continue with
later safely parseable entries, including consecutive quarantines.

Executable permissions/signatures, non-UTF-8/NUL binary content, bounded potential
secret signatures and nested-archive signatures are findings, not parse failures.
Never execute members or recursively open nested archives. Signatures cannot prove
absence of secrets or malware. Heuristic source/header/test/configuration/dataset/
output/cache/dependency/binary roles and suffix language hints need later review.
Read-only static inspection of regular bytes does not authorize executing or
reusing them; flagged private content must not appear in sanitized public reports.

Corruption/truncation, unsupported sparse encoding, unsafe metadata parsing,
resource exhaustion, archive changes or identity mismatch stop incomplete. Verify
two zero TAR end blocks, zero trailing padding and full GZIP CRC/footer; nonzero
trailing/concatenated TAR data cannot hide unexamined members. Bounded GNU/PAX name
metadata is parsed, never executed. Process limits contain parser recursion or
allocation failures. If the OS kills a budget-exhausted process before JSON output,
there is no completed manifest; the caller records failure and preserves logs.

## Manifest contract and integrity
Version 2 retains complete as a compatibility field, paired with inventory_status
completed/incomplete. Security findings, quarantined entries, security clearance,
reuse authorization and model validation are independent fields. security_clearance
is always not_granted, source_reuse_authorization prohibited, and
scientific_model_validation unvalidated. No finding is converted to clearance.
Per-member hashes cover regular bytes; links/special members have null hashes
because their targets/content were never read. Payloads missing due to a fatal
parse/budget stop are not represented as completely inventoried members.

Compute full archive SHA-256 before and after successful inventory; verify both
against the designation plus unchanged file size/stat identity. A manifest SHA-256
covers canonical sorted compact ASCII-escaped JSON excluding its digest field.
verify_manifest detects accidental modification, not malicious authorship.
All flags/counts are finalized deterministically after scanning, without timestamps.
Keep old evidence and failed prefixes; never overwrite them with a later success.

The CLI writes private JSON to stdout: redirect into restricted storage outside
tracked files. Private output contains raw paths/targets and MUST NOT be uploaded.
Exit 0 means completed technical inventory, including when findings/quarantine are
present; exit 1 means incomplete/invocation failure. Invalid syntax exits 2. Never
use exit status alone as permission to execute, copy, publish or accept science.
Invocation: python scripts/inventory_legacy.py <private-archive> --limits
 docs/audit/intake_limits.json --expected-sha256 <designated-hash> --expected-size
 487062036. No source member is written to disk. Only the private inventory report
and diagnostics are saved. Member timestamps are not simulation time.

## Acceptance and handoff
S009 needs full bounded inventory, verified unchanged identity, private manifest
integrity, preserved findings and passing applicable tests/CI/documentation. It
accepts the inventory protocol/evidence, not source safety or scientific models.
License/reuse restrictions stay recorded independently. B-S009-02's former stop
on a link is resolved by this authorized policy and verified continuation tests;
new fatal integrity/resource failures must be recorded honestly and resolved.
