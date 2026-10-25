# S011 — Source trace and bounded validation review plan

Status: static review prepared; legacy execution NOT RUN and NOT AUTHORIZED.
This completes a source-bound planning step, not S011 acceptance. The owner still
prohibits archive/source extraction, reconstruction, execution and redistribution.
No source was prepared, built, patched, executed or copied into this repository.
The archive remains LEGACY-CANDIDATE-001 at the designated immutable SHA-256.

## Exact source binding
Public metadata lives in S011_EXECUTION_REVIEW_PLAN.json. Raw paths, source and
private JSON/XML inputs stay restricted. Entry IDs resolve through the accepted
S009 manifest, whose canonical digest is
61b494e1d921464f980714d0a916dff12856acc2058421da091ce959751c2daf.
Every reviewed regular payload was hash-checked; no link target was accessed.
The root build declaration identifies sw_cosim and its source entry-00010836;
the two other native main candidates are separate tools, not interchangeable
simulation entrypoints. This conclusion comes from source declarations and bodies,
not filenames. Compilation/linkage has not been tested.

## Static execution/data-flow map
All ranges are inclusive, 1-based source lines in the designated archive.
Statements below mean observed in legacy source, not validated physics/runtime.

| Stage | Source anchor | Observed flow and limits |
|---|---|---|
| Build target | entry-00011035:36–48 | sw_cosim links the local engine library; it links core/OpenSSL and libsumo/sumocpp. Catch2 and JSON headers are required by the inspected configure path. No explicit ns-3 link is declared here. Transitive/dynamic linkage remains unverified. |
| CLI split | entry-00010836:124–154 | Normal invocation has configuration, city-directory and fresh-output-directory arguments. --validate-config takes configuration/city only and returns before the event/network/mobility objects in main. Other argument counts take usage exit 2. Library/global initialization has not been tested. |
| Validation/input reads | entry-00010836:34–122,125–166 | Loads configuration JSON and city.json, checks source-declared fields/profile/bounds. Optional feeder path is opened directly from its configured string. city_directory is not used to rebase it. Invalid JSON/files/validation errors are caught. |
| State setup | entry-00010836:170–245 | Takes seed/time/truck settings, constructs output events and dynamics; initializes bins, separate observations, security identities and SLA state. Sensor state is distinct from network-admitted observations. |
| Seeds/randomness | entry-00010855:37–46; entry-00010995:10–24; main:213–216,441–464 | Source derives named seeds via hashing; dynamics owns separate stochastic streams, traffic seed reaches libsumo, attack selection uses its own generator. These observations do not prove cross-platform/random-distribution validity. Logged names alone do not prove use. |
| Security identity | entry-00010840:30–62 | Source derives an Ed25519 key input from seed and identity, hashes/serializes payloads and signs envelopes. No cryptographic audit or execution performed. |
| Network boundary | entry-00010844:36–139,181–183; main:346–435 | The inspected implementation is a local shared-service priority queue, not an ns-3 adapter. It dispatches due payloads to a callback and tracks its own time. Seed/run arguments in its internal constructor are unnamed/unused; modeled channel-drop/outage methods return zero. This is implementation scope, not measured loss or physical PLC validation. |
| Mobility boundary | entry-00010833:10–36,59–78; main:441–454 | Constructs a libsumo simulation from city.net.xml, timestep and derived traffic seed; reads vehicle state/road distances. Trucks' positions are copied directly into communication endpoint state, not transmitted as truck messages. |
| Per-tick order | entry-00010836:519–573 | Computes simulation time from tick/timestep; advances queue then mobility; compares clocks/positions; advances dynamics at sensor periods, creates bin events and conditionally sends telemetry. Observed checks/thresholds are not accepted models or new-project defaults. |
| Wire/receive path | entry-00010836:347–435,470–509 | Builds a JSON payload/envelope, serializes a message and schedules transport; callback parses, verifies/admission-checks and updates observations/SLA. Transport arrival and security acceptance are distinct lifecycle states. |
| Decisions/collection | entry-00010836:598–711; entry-00010855:21–30 | Selects policy branches, destination/return states and collection; adjusts payload/fill and logs outcomes. DQN may require ONNX/model/parity files; training-IPC uses stdin/stdout. The reviewed validation plan does not exercise these branches. |
| Completion/drain | entry-00010836:735–829 | Records collection completion separately from simulation end; optional drain continues clocks; classifies message outcomes and checks accounting. This is code order, not observed convergence or determinism. |
| Writers/metrics | entry-00011002:14–38; main:869–967 | Event writer creates a new directory, refuses an existing one and writes events.jsonl with run/seed/time. Summary includes collection/network/proxy metrics; fuel is labeled a proxy, not a calibrated model. Optional timing output and run_summary.json are written. |
| Failure/results | entry-00010836:962–973 | Source returns 0 on route completion, 3 on noncompletion, 1 on caught failure; after output construction it attempts failure.json. Summary/failure ofstream expressions lack the event writer's post-write error check. Therefore exit code alone cannot establish artifact integrity. |

Wall-clock steady_clock diagnostics (microsecond/millisecond/second report fields)
are separate from simulated time and event seconds. Full normal-run byte equality
must not be promised solely from a master seed: outputs contain host timing data.
Any later semantic projection/tolerance requires an explicit preregistered rule;
retain raw hashes and differences rather than hiding them. No reported unit,
formula, stochastic parameter, PLC reference or proxy is scientifically accepted.

## Selected immutable input references
The planned small input pair is configuration entry-00011013 and city JSON
entry-00000089; the corresponding road network is entry-00000088. Their exact
hashes are in the JSON review packet. No physical/scenario values were copied
into new simulation settings. The chosen configuration has no feeder-path key.
An independent static checklist found the inspected validation branch's required
keys/types/profile/basic bounds present; that is not a program validation result.
city.net.xml is part of the normal-run contract but the validation-only branch
does not open it; validation success would not demonstrate simulator readiness.

The optional feeder path, optional model/parity files and city/config/output
arguments can depend on process CWD when relative; main contains no uniform
input-root resolution. The five proposed cases use absolute config, plus absolute
and deliberately relative city paths. A separate feeder-path mutation would need
a new reviewed input hash; it is not included in these five cases.

## Exact proposed cases — none executed
Token bindings are deliberately non-shell data:
- BIN_ABS: fresh verified private build/sw_cosim, never an archived executable.
- CFG_ABS: private read-only configuration fixture bound to entry-00011013.
- CITY_ABS: private read-only city_fixture directory under CWD A, with the city
  JSON/network references above; CITY_REL is the literal city_fixture.
- CWD A: private fixture root containing city_fixture. CWD B: a different fresh
  directory without city_fixture. Both use the same absolute executable/config.

| Case | CWD | argv after BIN_ABS | Predicted exit, pending actual verification |
|---|---|---|---|
| ABS_A | A | --validate-config CFG_ABS CITY_ABS | 0 if source/dependency/input preconditions hold |
| ABS_B | B | --validate-config CFG_ABS CITY_ABS | 0; stable validation metadata should match ABS_A |
| REL_A | A | --validate-config CFG_ABS CITY_REL | 0 if preconditions hold |
| REL_B | B | --validate-config CFG_ABS CITY_REL | 1 because the relative city JSON is absent in B |
| MISSING_CITY | A | --validate-config CFG_ABS | 2 for usage/argument count |

These are hypotheses from inspected control flow, not fabricated results. For
future authorized execution retain every stdout/stderr, exit/signal, executable/
dependency/input hash and observed filesystem effect. Reject missing/corrupt JSON,
wrong status/profile/seed/map/bin-count, unexpected writes, timeout or nonzero exits
where success was predicted. For ABS_A/B compare raw validation stdout and parsed
metadata; do not discard unexpected differences. No normal simulation, world
advance, training, ONNX inference or historical campaign replay is proposed.

## Preparation and permission boundary
This packet is reviewable metadata only: execution_authorized=false,
working_copy_prepared=false and all cases NOT_RUN. Approval cannot be inferred
from a successful linter or a changed boolean. Actual execution authority must
come from the owner and be recorded separately.

A future exception would be needed to create a disposable private working copy
of exactly the 32 nonquarantined native text/build entries listed in the packet,
plus the three referenced JSON/XML fixtures, outside both the archive and this
implementation repository. Verify copied bytes against every S009 source hash.
Do not copy symlinks, scripts, binaries, .deps, nested archives, secrets or old
results. Do not patch or redistribute the source. Use trusted separately supplied
OpenSSL, Catch2 3, JSON headers, C++17 toolchain and libsumo dependencies; record
actual provenance/versions. No archived library or executable may be substituted. Build authority does not
resolve source/package provenance or license restrictions: record those and stop
if the proposed private use cannot be evidenced as permitted.

Only after explicit preparation/build authority, proposed trusted-tool commands
are cmake -S SOURCE_COPY -B BUILD_DIR -DSW_BUILD_COSIM=ON, then
cmake --build BUILD_DIR --target sw_cosim --parallel 2. No ctest/install, archived
script or normal simulator command is authorized by this document. Build budgets:
300 seconds wall/CPU, 1 GiB address space. Validation: at most five cases, each
10 seconds wall, 5 CPU seconds, 256 MiB address space. These are proposed resource
bounds, not proof of feasibility or permission to increase them silently.

The future harness must first verify no-network isolation, read-only binary/input/
CWD mounts, private stdout/stderr capture and denial of child-process execution.
Library/global initialization may have effects outside main; source comments are
not a security guarantee. If isolation/dependency/source identity cannot be
verified, stop; no unsandboxed fallback. Archive hash must match before/after.
Current source execution, source preparation, fixtures and sandbox have NOT occurred.

## Independent review-packet validation
validate_execution_review_plan.py is an independently authored read-only metadata
linter. It binds source/input references to the accepted inventory, checks this
five-case argv/CWD scope, rejects stale/quarantined references and refuses claimed
execution/reuse/scientific success in the static packet. It does not copy, build,
launch commands, enforce a sandbox or grant authorization. Canonical inventory
hashes detect changes, not authenticity; source interpretation was manually read.

Run python scripts/validate_execution_review_plan.py
 docs/audit/S011_EXECUTION_REVIEW_PLAN.json --inventory <private-S009-manifest>.
Exit 0 means VALID_STATIC_PLAN only; runtime_status remains NOT_RUN. Invalid JSON,
unknown/missing fields, changed scope, bad identities and false result claims
fail closed. Tests with synthetic metadata run the linter from another CWD;
these are NOT the mandatory legacy runtime attack. S011 remains blocked until
its remaining actual gates and permitted integration are evidenced. S012 is
not eligible. Licensing, archive safety and scientific validity remain separate.
