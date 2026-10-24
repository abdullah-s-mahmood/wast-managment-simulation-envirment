# S010 — Legacy module and dependency graph

Report finalized 2026-10-24 Asia/Baghdad. Branch sprint/S010-static-module-graph.
Base 969eec59de95a5efa7b9dedc396a7a282c53b7e6 (S009 acceptance PR #20).
Evidence E-S010-01; ADR-0001/0004/0005/0006; D-0009/0010.

## Gap and narrow implementation
S009 inventoried bytes but did not locate imports, entrypoints, calls or external
build declarations. Independently authored audit_source_graph.py parses regular
source as data, tests/test_source_graph.py provides nine fixtures/property groups,
and STATIC_MODULE_GRAPH.md/static_graph_policy.json define the private interface,
source anchors, scope/unknowns and resource policy. Inventory/state/report/log
updates only. No legacy code, private manifest or raw results committed; no new
simulation or scientific behavior. Existing ADRs cover read-only audit; no new
material architecture/science decision. Source ownership/license/reuse unknowns
remain separate from static-inspection ability.

## Actual commands and source evidence
Linux x86_64/Python 3.11.15, standard library only.
- python -m unittest discover -s tests -p test_source_graph.py -v: exit 1 initially
  (test-first missing module); then exit 0. Final nine tests include generated
  import/line invariants, explicit unknowns and no execution of hostile source.
- python -m unittest discover -s tests -v: exit 0, 72 tests.
- Real CLI audit source graph with private archive, accepted S009 --inventory,
  --policy docs/audit/static_graph_policy.json and --expected-manifest-sha256
  61b494e1d921464f980714d0a916dff12856acc2058421da091ce959751c2daf: exit 0.
  Parent timeout 135 seconds; CLI process memory/CPU and stream/source budgets
  enforced. Full archive hashes before/after and each selected payload match S009.
- Output: private-evidence/S010/static-module-graph.json in Git common metadata.
  Canonical graph SHA-256 01f0a10ce7059aa732f754bd47e492f9cac4b36b542492af5c0d119812730b62.
- 3752 nodes/79509 syntax edges; 3750 parsed, one invalid/unsupported Python and
  one quarantined unknown. 359 definitions/270 entrypoint candidates. Precise
  counts, four independently checked source anchors, scope and limits in
  STATIC_MODULE_GRAPH.md; cross-check.json stays private. Source-line check exit 0.

## Self-audit, gate map and residual limits
WB: imports/AST calls/main guards, comment-filtered includes/build declarations,
node/source identity and explicit unknowns. BB: actual CLI output/private graph
and archive fixture mapping; reviewer finds each recorded behavior candidate by
entry ID/hash/line, without narrative inference. Adversarial: plausible filename
without source evidence, comments naming fake dependencies, malformed Python,
hostile import syntax never executed, links, wrong manifest/hash and source budget.
Generated property checks: 24 import-count/line invariants; reference fixtures and
four independent real source-line/hash checks. Regression: original 63 intact.

Native lexical candidates are not resolved runtime calls; definitions count is
Python only. Transitive/native/dynamic/conditional behavior and installation
availability remain unknown. Generated/historical source scopes retained; no claim
all are active modules. A graph can map recorded source without accepting its
physical correctness. NOT RUN: legacy execution, Windows hostile-input CLI,
SUMO/ns-3 and empirical/physical validation, outside static-audit scope.

Changed files: audit_source_graph.py, test_source_graph.py, STATIC_MODULE_GRAPH.md,
static_graph_policy.json, repository inventory, progress, handoff, blockers,
validation log and this report. Actual final governance commands, exact-head CI
and permitted integration recorded in E-S010-01/02; no acceptance before CI/merge.
Next eligible after acceptance: S011.

Final real CLI replay exit 0, byte-identical private graph; raw artifact SHA-256
6c593ea9b766f642162e56e493bf316eb3dba91588b17e8e82bb26e527e33ec3.
All five governance validators and diff checks exit 0; 174 approved artifacts.
Author verdict: static source graph and explicit-unknown contract locally met;
exact-head CI/permitted integration still required. No runtime graph claimed.
