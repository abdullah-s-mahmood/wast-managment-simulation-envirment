# S014 model extraction — working protocol

Status: candidate indexing verified; expression-level review INCOMPLETE. This is
not S014 acceptance, source reuse authorization or scientific validation.

The independent extractor reuses the S013 bounded read-only TAR/GZIP traversal.
Only hash-verified UTF-8 source payloads reach a trusted observer. Nothing from
the archive is imported, evaluated, compiled or executed. Unsafe entries remain
quarantined by accepted intake. Nested archives are not opened. Exact full
archive identity is checked before and after traversal, with member/accounting,
CRC, termination and file-stat checks. Existing 1MiB per-text, 8MiB source,
16MiB result, compressed/expanded/member/count/metadata/time limits are retained.
The Linux CLI adds 256MiB address space and 120 CPU seconds; invoke under a
120-second external wall timeout. Library callers must supply equivalent limits.

Each private candidate has an opaque archive entry ID, full source SHA-256,
one-based inclusive line range, zero-based UTF-8 byte offsets (exclusive end),
span SHA-256, original identifier spellings, source scopes and lexical tags.
The ledger does not reconstruct source files. Original names are tokens, not
resolved symbols. A single line can contain several expressions or part of a
multiline expression. Strings/comments may match; indirect expressions may not.
Tests/tools/build context must not be treated as runtime model definitions.

Every candidate retains these separate labels:

- Observed: STATIC_SOURCE_CANDIDATE, not executed behavior.
- Intended: UNAVAILABLE until a separate traceable requirements review.
- Scientific support: UNVALIDATED; comments and software tests cannot promote it.
- Original units: null means unresolved, never dimensionless by default.
- Normalized expression: null; no normalization precedes original-unit review.
- Missing constants: NOT_FILLED; no physical value is supplied by intuition.
- Review: PENDING. Traversal completion does not complete semantic extraction.

The record verifier recomputes anchors/names/tags from exact source bytes and
rejects metadata tampering, guessed normalization, inferred units and unsupported
trust upgrades. Integer coordinates reject booleans. The manifest digest checks
artifact consistency, not authenticity, licensing or physical correctness.

Private output resides only in Git common metadata private-evidence/S014, with
owner-only permissions. Public reports contain counts/hashes/methodology only;
no source snippets, private archive paths or historical output values.

## Remaining acceptance work

Review exact equation boundaries against immutable source, associate original
variables/units (including explicit unknowns), defaults, random distributions,
seed/time semantics and protocol parameters. Separate runtime implementation,
auxiliary models, scenario/tool settings and test expectations. Reconcile
multiline/indirect definitions and document coverage beyond lexical matches.
Keep observed, intended and scientifically supported evidence separate. Verify
primary references before any claim about what they report; code comments are
E4 observations, not scientific evidence. Retain the approved PLC source set.
No model is accepted for implementation by this protocol. S015 cannot start
until the actual S014 ledger review, tests, exact-head CI and integration pass.

## Reviewed ranges (E-S014-02)

The separate S014_REVIEW_PLAN.json selects multiline source ranges by immutable
entry ID/source hash and one-based inclusive lines. review_model_spans.py binds
each range to zero-based UTF-8 byte offsets, a span hash, original identifier
spellings and numeric lexical spellings. Apostrophe/underscore digit separators
and scientific notation are preserved. No expression is evaluated or normalized;
exact formulas remain addressable in the designated archive rather than copied
into executable source. Source unit spellings remain in identifiers/ranges;
physical units are not inferred from names or comments.

The plan's English observations are reviewer interpretations of E4 source. Hash
verification establishes which bytes were inspected, not the truth of a reviewer's
interpretation. Intended behavior remains UNAVAILABLE and scientific support
UNVALIDATED. Source-defined input boundaries are software observations, not
established scientific applicability domains. RNG seed/source replay is separate
from distribution calibration and cross-library stochastic reproducibility.

Every selected range must resolve. Invalid schemas, duplicate IDs, guessed units,
extra trust/normalization fields, changed sources, boolean/out-of-range coordinates,
and spans over8KiB fail closed. Plans allow at most1024 ranges, each under80 lines.
CLI budgets inherit the candidate scanner's archive/CPU/address-space policy.
The public plan and summary contain only sanitized observations and opaque source
anchors. Private manifests retain original names/numeric spellings and exact
source-range hashes. There is no executable legacy implementation in this project.

Coverage now includes reviewed core dynamics/collection/encoding/masks, network
capacity/packet outcomes, auxiliary field-trial interpolation, mobility/routing,
SLA/reward, runtime scheduling/defaults, admission/identity rules, optional ONNX
and training/export formulas. It remains a partial review: remaining active-path
scenario generators, campaign/analysis/tool scripts and their hidden parameters
need classification and review before claiming whole-project model extraction.
Retired-context models retain S009/S013 pointers, not silent exclusion from future
scientific review. No currently approved PLC source set is changed.
