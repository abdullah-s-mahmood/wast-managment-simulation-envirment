# S013 — Read-only test and historical-result evidence protocol

Inventory status is distinct from source coverage, test execution, historical
reproduction, licensing and scientific validity. The public summary contains only
counts/IDs/digests. Raw paths, test source references and metric field names stay
in restricted private manifests. No raw historical campaign results are published.

## Scope and identities
Use the immutable designated archive and accepted S009 inventory; find the project
prefix from the hash-bound root CMake entry-00011035. Every selected logical member
matches ordered ID/path/size; every read regular payload matches its S009 SHA-256.
Full compressed archive hash/stat, gzip CRC/TAR termination and cumulative expanded
bytes are verified before/after. Never follow member links, extract members to a
filesystem, import/evaluate source, run archived tests/scripts or open nested archives.

`python scripts/inventory_test_evidence.py PRIVATE_ARCHIVE PRIVATE_INTAKE --project-root PRIVATE_PREFIX`
prints a PRIVATE manifest: capture stdout in a fresh mode-0600 file under an
owner-only evidence directory. Exit 0 means bounded inventory completed, not tests
passed. Linux-only process limits: 256MiB address space, CPU/wall 120s; existing
S009 compressed/expanded/member/metadata/count limits apply. Content selection:
1MiB per text member, 8MiB total source and 16MiB result text. Oversize, quarantined,
unsupported or unselected payloads keep explicit metadata-only/unknown status.
Resource/path/hash/parser corruption is fatal incomplete, never ignored as success.

Directory/suffix scopes are candidate hints, not proof of authorship or provenance.
Build/vendored contexts stay separate. A top-level archive/retired/historical scope
is tracked separately; its non-test source/result payloads stay metadata-only.
This does not discard those files from future scientific source review or change
currently approved PLC sources. Source under active project paths is fully read;
retired test source is statically read to catalog assertion syntax, never executed.

## Assertion and fixture evidence
Python AST records test-definition, assert, process-return check, subprocess-check,
unchecked process-call and common fixture-string line candidates. Trivial constant
asserts are separate. Native assert/CHECK/REQUIRE/TEST_CASE forms are lexical sites;
strings/comments do not count. Macros/templates/conditional compilation and runtime
assertion meaning remain unresolved. CMake add_test syntax is only a declaration,
not registration/execution proof. Shell runner references are lexical and explicitly
unresolved. Dynamic tests, aliases, fixture paths and conditional execution are not
fully resolved. A count of assertion-bearing lines is not a test-case/coverage count.

Python/native source classification distinguishes behavioral assertion syntax from
execution-status-only checks. It never says an assertion is effective or passed.
Fixture literals are common JSON/XML/CSV/YAML path hints, not resolved fixture
existence/units/validity. Every runtime status remains NOT_RUN for this audit.

## Historical trust labels
Every result candidate has one of reproduced/unreproduced/unverifiable. This tool
never grants reproduced status: no fresh authorized comparison is performed here.
A syntactically complete JSON source/config/dependency hash + seed + command record
can be labelled unreproduced; its self-reported provenance is not authenticated.
All other, unparsed, quarantined, retired-context, image or screenshot-only evidence
is unverifiable by this audit. A filename or status=passed/validated/reproduced
cannot change this rule. Earlier S012 failed normal attempts reproduce no archived
result and confer no scientific trust on historical artifacts.

JSON top-level metric field names and CSV headers may be cataloged privately;
values are not copied into the inventory. Units stay UNVERIFIED. No empirical
measurement, calibration, causal inference or physical accuracy is established.
Source reuse remains PROHIBITED and scientific validation UNVALIDATED throughout.

## Observed coverage and limitations
Final manifests v6/v7 are byte-identical and match v3/v4/v5. They cover 9,035 candidate records,
83 active source payloads, 18 active and four retired test-path files. Active test
files contain 299 nontrivial assertion-bearing line candidates and 20 common fixture
literal lines; 17 have behavioral assertion syntax and one no observed assertion.
These are source observations only, not test passes or proven behavioral coverage.

All 2,369 historical result candidates are unverifiable: 34 active-context texts
were inspected for schema/header hints; 2,335 retired-context payloads remain
metadata-only. Do not claim all historical provenance is absent or all payloads
parsed. The candidate selectors may miss dynamically generated tests/fixtures or
outputs outside declared result contexts; the complete S009 member index remains
available to future focused review. Existing result failures/unknowns remain visible.
