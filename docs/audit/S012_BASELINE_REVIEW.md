# S012 — Private baseline reproduction review

Status: review only, normal simulation NOT RUN and not yet authorized. S011 is
accepted (PR #29, acceptance PR #30); 11/88 sprints completed. The prepared plan
is S012_BASELINE_EXECUTION_REVIEW.json. Approval must bind its exact hash and
accepted ADR-0009; changing metadata alone never grants execution permission.

## Concrete proposed execution
Use the unchanged, fresh S011 private sw_cosim build and the same hash-bound
configuration/city/network. No archive change, new source copy, source patch,
archived binary, .deps, script, model training or historical campaign replay.
The archived scenario has 12 bins/two trucks, 600-second horizon and 0.1-second
step; these are observed owner scenario inputs, not calibrated or accepted models.
Keep the exact configured seed; no new default seeds or physical parameters.

Run the same argv twice from /A:
`/build/sw_cosim /inputs/config.json /A/city_fixture /outputs/baseline`.
Each invocation has a separate fresh bounded private output tmpfs mounted at the
same namespace path, so output basename/run ID is baseline in both. Source
entry-00010836:181,870 binds the output basename to run identity. No old output
can be overwritten. Existing binary and all 35 copied files remain read-only.

Each target: 120-second wall watchdog, 60 CPU seconds, 1-GiB address space;
output tmpfs 64 MiB, individual artifact file cap 16 MiB, export at most 64 regular
entries/64 MiB total. Exactly two case IDs; at most one retained corrective retry
each (maximum four invocations), stopping on identity/security/unknown-consumption
failure. Do not expand budgets silently or retry until green. Every failure stays.

Before any normal run: develop/test a trusted bounded export supervisor with
synthetic adversarial fixtures, demonstrate non-root/no-capability/no-new-privilege
execution, readonly inputs/binary/CWD, denied network/fork/exec, resource limits and
private capture. The target gets no writable host mount; trusted exporter runs
only after target termination, rejects links/special/traversal/duplicates and size/
count violations, then preserves regular data privately. Such a supervisor is not
implemented or verified yet; this plan's approval alone will not clear those gates.
Existing validation-only runner must never be used to launch a normal simulation.
Operational dependency environment remains explicit single-thread OpenBLAS/OMP.

## Result and reproducibility checks
Retain full commands, versions/dependency hashes, input/source/binary/archive
hashes before/after, process exit/signal, stdout/stderr-with-trace and every output
hash. Expected outputs are nonempty events.jsonl and run_summary.json. Exit 0
alone is insufficient: require route_complete=true, validation_only=false, matching
seed/run identity and valid finite event time_s representations; reject failure.json,
missing/empty/corrupt outputs, links, partial runs and over-budget artifacts.
Never call NOT_RUN a failed reproduction attempt or a successful baseline.

Compare raw event bytes exactly. Preserve raw summary hashes/differences and compare
an explicitly separate canonical summary projection excluding only
/simulation_runtime_seconds. Source entry-00010836:27–28,197,950 binds this value
to the steady-clock microsecond helper divided by 1e6 (host wall seconds), not
simulated time. Do not drop any other summary field or add tolerance after seeing
results. Optional host timing profiles remain retained/reported separately.
Unexpected semantic differences are failures to explain, not permission to weaken
comparison. A software replay result still establishes no physical-model validity.

## Independent evidence checker
`python scripts/validate_baseline_result.py PRIVATE_EXECUTION_RECORD PRIVATE_OUTPUT_DIR`
never launches code or grants permission. It requires attempted=true, actual normal
exit 0, verified dependencies/inputs and the reviewed binary hash, then validates
real regular output files, budgets, JSON duplicate/nonfinite rejection, event/summary
identity and completion flags. Metadata alone cannot pass with absent outputs.
Outputs must be in a trusted private directory without concurrent writers.
A record is evidence to verify, not proof of authorship or an independent operator.

Eleven synthetic tests cover positive/negative outcomes, missing dependencies,
nonzero/signal/nonattempt, absent outputs, validation-only results, wrong identity,
links/failure artifacts, corrupt JSON, duplicates/nonfinite values, byte/entry/
line budgets and preservation of all raw bytes when comparing host-time projection.
These do not satisfy S012's actual baseline reproduction gate. A second operator
can attempt the documented plan after the same owner authority and prerequisites;
no independent human review is required by ADR-0005.

Review JSON SHA-256:
5a8ef0be672f616bd9c40e68db4ea431e82dbb54c7dcea3ac31dd18bfb893187.
This proposes a current-code audit baseline with separately supplied SUMO 1.28.0-1,
not a claim to recreate unknown original campaign environments or measurements.
No normal invocation has been attempted; this is an authorization/preparation
blocker, not observed simulation failure. All proposed limits require their own
actual enforcement tests before any target launch.
