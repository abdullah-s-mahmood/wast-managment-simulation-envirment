# S015 discrepancy register and reproduction boundary

The machine-readable register prioritizes observed discrepancies, not a claim to
have found every defect. Register acceptance does not resolve its open issues.
P1 blocks confidence in baseline/analysis eligibility; P2 blocks raw replay claims;
P3 would indicate a lower-impact documentation mismatch. Priority does not imply
physical severity or establish a scientific causal mechanism.

D-S015-001 is a failed reproduction, not proof of a legacy code bug: a finite
scenario can legitimately fail to finish. D-S015-002 is a metadata/criterion
compatibility conflict with unresolved intended behavior. D-S015-003 is a raw
replay mismatch at host timing fields; it does not establish simulated-state or
random-stream divergence. Each has a source/test/evidence reference, minimal
reproducer, observable consequence and state/RNG/output/metric impact mapping.
Unknown effects remain explicit. Open questions are not promoted to confirmed
defects, calibration failures or source-supported scientific facts.

## Reproducer

`python scripts/audit_discrepancies.py reproduce PRIVATE_RETAINED_S012_ROOT`
reads only the accepted S012 artifacts through their recorded hashes. The CLI's
reference outcome is the committed S012_BASELINE_OUTCOME.json, not an arbitrary
historical campaign's self-reported success. Result receipts bind actual exits;
raw summaries and events bind observable outcomes and exact difference locations.
Files are bounded regular files, final symlinks rejected, file identity checked
across reads. No source patch, launch, shell execution, reconstruction or result
normalization occurs. The CLI has no repair/import option.

The same original two failed normal runs are rechecked; zero new simulation runs
are implied. This is a copyable reproducer for the retained discrepancy evidence,
not a new execution of the unavailable disposable S011 target. A fresh simulation
reproducer would need a new concrete preparation/isolation plan within authorized
scope; do not rebuild or run unknown legacy code merely to repeat this audit.

`python scripts/audit_discrepancies.py check
 docs/audit/S015_DISCREPANCY_REGISTER.json` validates the register's evidence fields,
priorities, explicit impact mapping, audit-only/no-change scope and trust labels.
It checks structure, not whether an arbitrary written interpretation is true.
The actual retained-evidence run and checksum receipts supply that separate gate.

Raw event equality remains failed even if a JSON structural comparison isolates
host fields. There is no event projection or repaired result. The original frozen
summary exclusion remains historical S012 evidence, not a new normalization policy.
No old historical campaign values are imported into the new project's results.

## Integrity and limits

CLI limits are 256MiB address space and60 CPU seconds; use an external60-second
wall timeout. Each evidence file is at most16MiB; event count at most100000 and
line length at most1MiB. Strict JSON rejects duplicates/nonfinite numbers; actual
exit types are integers and summary flags are booleans. Missing, corrupt, changed,
unverified or oversized evidence fails closed before a success artifact.

Original archive identity remains owner-designated and unchanged. These tools
read retained audit artifacts; they do not alter the source or resolve source
reuse/licensing. All science remains UNVALIDATED. Source/library/RNG calibration,
physical model acceptance, exhaustive bug discovery and Windows execution are
not established by the register. S014 source-audit limitations remain in force.
