# S010 — Source-backed static module and dependency map

Classification: observed in legacy source syntax; not executed or scientifically
validated. Source: designated archive identity and accepted S009 manifest. Full
member paths/symbols stay in private-evidence/S010/static-module-graph.json under
Git common metadata. No legacy implementation, campaign data or binary is copied
into this repository. Source reuse/redistribution remains prohibited.

## Observable graph and lookup
Each node binds S009 entry_id, private member path, SHA-256, language and parse
status. Parsed nodes have definition names/line spans, entrypoint candidates,
edges with target/source line/kind/resolution, and explicit unknowns. Entry IDs
are unique in the archive; a line is 1-based in the UTF-8 source payload. No
simulation time, physical units, parameters, model defaults or seeds introduced.

A reviewer resolves any definition/call/import to the private source by node entry
ID, source SHA-256 and line, cross-checking the accepted inventory. Never resolve
an archive name to a filesystem extraction path or execute it. Nodes with unsafe
paths/duplicates/secret/binary/nested flags are excluded from content parsing;
links/special members are never read. Executable-permission regular text may be
read as source data, with no execution permission implied. Nonselected languages
are outside this tool's scope; selected unsupported/invalid/over-budget files
remain explicitly unknown. No behavior is inferred from a plausible filename.

| Observed source anchor | Source hash | Line | Independent source check |
|---|---|---|---|
| entry-00000003 | 288314ad60ce3e0644a3c18b131a7dc4d31aaf729fb1bbcef3355128bd46936d | 3 | Import declaration starts at recorded line. |
| entry-00000006 | e5bb4d22ff672926752c57095aaea4f41c326d0d16305de24c1a2cead81d116c | 1 | Include target occurs in recorded source directive. |
| entry-00000161 | 69b06c6b14eb48e00c0b775b2c2b9a43d5072340fb57a08150d6df8ae344e978 | 45 | Dynamic-loading call syntax occurs at recorded line; not run. |
| entry-00003736 | 92f0bb7c63ff3acc9fade0337db563fd20ed0c5dcaae56cbf88e0af1d018b351 | 8 | Build declaration occurs at recorded line; not configured/built. |

## Actual coverage
3752 nodes: Python 67, native C/C++ 2971, CMake 714. 3750 parsed statically,
one invalid/unsupported Python entry (entry-00003715), and one quarantined
entry (entry-00005890). Both unknowns remain in the graph; no substitute behavior.
Definitions: 359 Python function/class declarations; 270 entrypoint candidates.
Edges: imports 520, AST call syntax 9297, includes 10428, native lexical call
candidates 59114, dynamic loading 2, build declarations 148 (79509 total).
These are syntax counts, not runtime calls, verified installations or unique
external packages. Native function bodies/overloads/templates are not resolved.

Source-role hints: source 279, headers 2725, tests 22, generated outputs 310,
document/unknown 416. The graph deliberately retains historical/generated scopes
instead of pretending every archived source file is an active production module.
Ownership/transitive third-party dependencies require separate evidence; path
and import names alone do not establish them. No dependency is invented or installed.

## Semantics and limitations
Python uses ast.parse only, never import/eval/exec of source. Imports and call
expressions are observed syntax; runtime branches, alias shadowing, monkey-patching,
plugin dispatch and dynamic module availability remain unresolved. Explicit main
guards are candidates, not a claim the script runs successfully.

Native includes are read after comment removal; quoted strings are masked before
lexical call patterns. Candidates may include declarations, casts, macros or
constructors. Main-pattern candidates and explicit dynamic loader syntax have
source anchors. No C++ compiler/preprocessor, binary loader or runtime is invoked.
Raw-string/conditional/preprocessor semantics remain limitations of this lexical
view; candidates must not become verified call edges without further evidence.

CMake records explicit find_package/add_subdirectory/link/library/executable
syntax, excluding line comments. Conditionals, variables, transitive dependencies
and real configure/build resolution remain unknown. This does not accept build
instructions for execution. Runtime startup/dataflow belongs to S011; reproduction
requires its own later gates and applicable execution authorization.

## Reproduction, integrity and failures
scripts/audit_source_graph.py takes a private archive, accepted --inventory,
--policy docs/audit/static_graph_policy.json and --expected-manifest-sha256
61b494e1d921464f980714d0a916dff12856acc2058421da091ce959751c2daf.
The Linux CLI enforces 512 MiB address space/120 CPU seconds; source reads cap at
1 MiB, with per-file/total edge budgets and a 120-second wall deadline. All member
names/sizes are cross-checked; selected payload hashes and full archive hashes
before/after must match S009 evidence. No links or unsafe targets are accessed.
Private output is a graph, not extracted source. Never upload it.

Exit 0 means structural audit completed with explicit unknowns; malformed inventory,
hash mismatch, archive-parser/resource failure or truncated archive fails rather than
emitting plausible partial success. Graph digest covers sorted compact canonical
JSON before its digest field, without volatile timestamps. It detects accidental
corruption, not authenticity. No archive safety, source reuse or scientific model
acceptance follows from successful source mapping. Independent source-line checks
and synthetic adversarial/reference/generated tests are reported in S010 evidence.
