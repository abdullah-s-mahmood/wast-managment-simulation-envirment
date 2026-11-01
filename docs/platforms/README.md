# Platform targets and acceptance plan

S017 chooses targets; no simulator platform is verified yet. ADR-0010 accepts this
planning scope only. S017_MATRIX.json version1 records install/verification routes
and NOT_RUN gates. Dependency versions remain unselected until their own sprints.

| Target | Priority | Current evidence | Runtime support |
|---|---|---|---|
| Ubuntu24.04 x86_64 Linux runtime | Required | Sanitized local host probe only | NOT_RUN |
| Windows11 x86_64 + WSL2 Ubuntu24.04 | Required | Host/guest execution NOT_RUN | NOT_RUN |
| Windows11 x86_64 + native MSYS2/MinGW64 | Best effort | Native execution NOT_RUN | NOT_RUN |

These are release-validation targets, not advertised verified simulator support.
Linux governance checks do not establish Windows parity. Current POSIX audit
helpers are not declared native-Windows compatible; their tests remain intact.
A Linux kernel probe cannot verify a Windows host/distro/WSL2 pairing.

## Routes and provenance

Each target lists Git, Python, C++ compiler, CMake, build driver, SUMO and ns-3
installation/verification routes. No installer is run here. Refer to release-specific
upstream guidance before selecting versions or optional bindings:

- [ns-3 Linux](https://www.nsnam.org/docs/installation/html/linux.html) and
  [Windows](https://www.nsnam.org/docs/installation/html/windows.html) prerequisites.
- [SUMO installation](https://eclipse.dev/sumo/docs/Installing/index.html).
- [Python Unix](https://docs.python.org/3/using/unix.html) and
  [Windows](https://docs.python.org/3/using/windows.html) documentation.
- [Git installation](https://git-scm.com/install/).
- [WSL host setup](https://learn.microsoft.com/en-us/windows/wsl/install).

Sources accessed2026-11-01. ns-3's Windows page includes version-specific examples;
copying their package versions is not a dependency lock. Any selected native
Python/toolchain binding must get an explicit ABI verification. No physical-model
support follows from vendor platform documentation.

## Independent acceptance gates

1. Capture target OS/architecture/runtime identity. Windows/WSL requires both host
   version and WSL distribution/version2 evidence, not a Linux-only receipt.
2. S018 selects/locks Python tooling; S019/S020 install and smoke-test selected
   SUMO/ns-3 versions, source/binary hashes and build options for required targets.
3. S021–S024 exercise actual adapters, paths (including spaces/non-ASCII), process
   lifecycle, clock alignment, deterministic replay and integration per target.
4. Map each claimed pass to its exact target, scope, command/exit and artifact hash.
   Missing/failed tests stay open. Best effort does not bypass scientific/data gates.

S017_LINUX_PROBE.json contains observed distro/kernel/architecture/interpreter,
not a toolchain lock or simulator test. Its UTC observation date is host-probe
provenance, not simulated time. The collector does not install or launch dependencies,
read private legacy inputs or publish hostname/credentials/local paths.

`python scripts/validate_platform_matrix.py check docs/platforms/S017_MATRIX.json`
checks plan/evidence boundaries. `probe` prints sanitized current-host observations;
unknown/Windows/WSL contexts are not automatically assigned a Linux target receipt.
The validator prints VALID_PLATFORM_PLAN_UNVERIFIED_RUNTIME. Its success means a
consistent plan, while runtime platform gates remain open. A future readiness
record must not silently rewrite this version's historical NOT_RUN values.

Version1 accepts only the recorded Linux host-observation schema. Receipt target
labels must agree with observed OS/distribution/architecture/kernel fields; changing
an ID cannot relabel Linux observations as Windows. Independent Windows host/guest
receipts need a later qualified evidence-schema revision, not a forged version1
record. Hashes check consistency; they are not signatures authenticating arbitrary
self-reported observations. Actual command execution/self-audit remains required.
