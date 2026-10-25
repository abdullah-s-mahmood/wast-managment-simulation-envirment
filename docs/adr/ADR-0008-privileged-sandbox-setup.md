# ADR-0008 — Privileged setup, unprivileged audit target

- Status: Accepted
- Date: 2026-10-25
- Related sprint(s): S011
- Decision authority/method: owner supplied administrator authentication to resolve B-S011-02; self-audit under ADR-0005
- Replaces: no scope expansion of ADR-0007; records its execution mechanism

## Context
Unprivileged user/network namespace creation is denied on the current host.
The owner provided administrator authentication after the precise blocker was
explained. Authentication is used interactively only; no credential is written to
commands, repository, reports or private artifacts. Existing host policy remains.

## Options considered
Stop; relax host security globally; or use existing privileged Bubblewrap setup
then drop privileges before the audited process. Choose the last; no global
policy/sysctl/AppArmor changes, sudoers changes or service changes are needed.

## Decision
Use sudo only for a trusted installed timeout/Bubblewrap namespace setup. Isolate
mount/network/PID/IPC/UTS namespaces, mount selected audit inputs, sources and
libraries read-only, then use trusted setpriv to drop to the owner's nonzero UID,
clear supplementary groups/capability bounding/inheritable/ambient sets and enable
no-new-privileges before any compiler or target. Temporary setup capabilities are
not target capabilities. No legacy process runs as root. Preserve private evidence.

Validation additionally uses installed strace 6.8 syscall injection: deny all
observed execve/execveat, fork/vfork/clone/clone3, network syscalls and namespace/
ptrace/io_uring setup; keep kill-on-exit. The initial target launch precedes the
injection counter. Never add an occurrence delay: a trusted regression probe
showed that when=2+ permits an extra exec. This is bounded Linux x86_64 audit
instrumentation, not a general verified sandbox or ordinary production execution.

Keep ADR-0007's 300-second build and each case's 10-second wall/5-second CPU/
256-MiB address-space caps. Build inherits one CPU affinity so cumulative command
wall bounds aggregate compiler CPU; all compiler processes inherit 1-GiB address
space. Preserve every build attempt and subtract its duration before retries.
Unknown prior consumption blocks retries. Validation streams have 1-MiB file
limits and private regular-file capture; each disposable writable tmpfs is 16 MiB.
These are not aggregate cgroup memory guarantees. No guard may silently loosen.

Operational environment sets OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1 after
an observed dependency-initialization failure under denied clone3. This changes
trusted dependency concurrency, not source bytes or scientific inputs. Retain the
failed attempt. Authorized failure recovery may retry the same five case IDs in a
separate retained bounded batch; max_cases=5 is per batch, not permission for new
case IDs or unbounded attempts. Current recovery permits one specific serial-deps
retry after the recorded ABS_A exit 130; every attempt retains the original caps.

## Evidence and assumptions
Owner authorizes the exact source-copy/build/five-case scope in ADR-0007, plus
routine failure correction/retesting. Trusted probe verifies target non-root UID,
zero effective capabilities/no-new-privileges, read-only mounts, denied network/
fork/exec calls and CPU/address-space/file/wall limits. Probe receipts bind raw
logs to current wrapper and fixture hashes. Private target results are separate.

Dependencies are separately downloaded authenticated package-index candidates:
SUMO/sumo-dev 1.28.0-1 and nlohmann-json3-dev 3.11.3-1, verified against repository
package SHA-256 values and unpacked privately without installing/upgrading host
SUMO. Existing compiler/OpenSSL/Catch2/strace are installed system tools. Record
copyright metadata/provenance separately; no legacy reuse/redistribution clearance.
strace behavior reference: https://github.com/strace/strace/blob/master/doc/strace.1.in
and installed 6.8 manual/observed trusted probes. Future versions need revalidation.

## Consequences
B-S011-02 can close on actual enforcement evidence, not privilege possession or a
successful true command alone. Legacy archive is immutable. Private approved text
copies do not enter the implementation repository. All scientific models remain
unvalidated; no normal simulation, model training, campaign replay or redistribution.

## Validation and revisit conditions
Require synthetic adversarial copy/receipt/wrapper tests plus actual trusted C
security/resource probes before target execution. Changed wrapper/fixture bytes
invalidate probe evidence. Retain failures, source/input/binary/archive hashes and
all raw streams, including tracer-added stderr. Accept S011 only after its actual
mandatory cases, exact-head CI and permitted integration; no skipping S012's gates.
