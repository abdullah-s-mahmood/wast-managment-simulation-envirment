# S009 read-only private intake

Owner designated LEGACY-CANDIDATE-001, SHA-256
 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8,
487062036 compressed bytes, for local read-only auditing. This resolves baseline
selection; it does not permit extraction, execution, reuse or redistribution.
License and source revision provenance remain unverified; no reuse permitted.

1. Use private locator in Git common metadata codex-legacy-candidates.json.
   Verify exact size/hash before any intake. Do not silently substitute a source.
2. Use inventory_legacy.py with explicit intake_limits.json. For hostile inputs
   additionally enforce process CPU=120 seconds/address space=256 MiB on Linux;
   the tested wrapper is recorded privately. No Windows support claimed here.
3. Read gzip/tar streams only, never filesystem extraction, link following,
   nested-archive opening or source execution. Reject traversal/absolute/Windows
   paths, duplicates/case collisions and every link/special member. Count expanded
   bytes including skipped data and headers; member/count/time/compressed limits
   fail closed. Memory/CPU hard limits contain parser extended-header risks.
4. Hash every inspected regular file; retain ordered private path/size/hash,
   heuristic role, suffix language hint, content/binary/signature flags and
   archive-hash provenance. Source/header/test/configuration/dataset/output/cache/
   dependency roles are distinct. Heuristics require later substantive review.
5. Detect bounded key/token signatures without snippets; potential secrets,
   executables, nested archives and binary content prohibit source acceptance.
   A clean signature scan cannot prove absence of secrets. Never publish manifests
   containing paths, raw historical data or source content. No nested expansion.
6. A rejected or limited scan is complete=false; retain original bytes and partial
   private evidence. No partial manifest is accepted as a full inventory. A
   complete scan with findings still exits 1 and is not accepted. Output is JSON
   to stdout; caller redirects into restricted storage outside tracked files.
7. CLI: python scripts/inventory_legacy.py <private-archive> --limits
   docs/audit/intake_limits.json. Exit 0 only for complete/no-findings; 1 for
   quarantine/incomplete. Malformed policy is an error, never defaulted.

Current scan encountered prohibited link/special member after 1282 entries and
stopped. B-S009-02 remains open. Original archive is preserved; changing policy
or creating a filtered replacement must not silently change the owner baseline.
Safe source intake needs a documented handling decision resolving this finding,
then full bounded checks and provenance review. Do not advance to S010.
Time limits are wall-clock seconds, sizes bytes, hashes SHA-256; no simulation
parameters or scientific validity assertions are introduced. Archive checksum
identity is separate from content safety and physical validity.
