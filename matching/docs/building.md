# Build Battle Chess from the reviewed source cohort

Run a fresh build with an explicit new output directory:

```sh
make -C matching build OUTPUT=build/local-run-001
```

The equivalent command from the repository root is:

```sh
matching/build/test-env/bin/python -B matching/build_game.py --output build/local-run-001
```

Relative outputs are resolved under `matching`; this example writes to
`matching/build/local-run-001`. Existing outputs are refused. Use a new name for
each run. Make prefers the existing project environment at
`matching/build/test-env/bin/python`. If it is absent, Make falls back to
`python3`; that fallback must provide a compatible Python3.11 environment.
Python3.11.9 is validated. The system default Python3.14 here is not a supported
project dependency environment. An explicit override always takes precedence:

```sh
make -C matching build OUTPUT=build/local-run-001 PYTHON=/path/to/venv/bin/python
```

When the project environment is absent, it can be prepared with Python3.11;
the pinned test dependency is needed for semantic regressions:

```sh
python3.11 -m venv matching/build/test-env
matching/build/test-env/bin/python -m pip install -r matching/requirements-dev.txt
```

NASM, DOSBox and the pinned Microsoft tools/libraries must also be installed.
The existing setup commands install their independently pinned distributions:

```sh
python3 matching/setup_toolchain.py --compiler msc500
python3 matching/setup_toolchain.py --compiler msc510
python3 matching/setup_runtime.py
python3 matching/setup_libh.py
```

Every normal build generates the complete reviewed C/ASM/COMMON cohort fresh,
links those whole objects with authentic LINK/full libraries, then verifies the
CRT0 DATA88 contribution from that same closed LINK result before writing final
component reports. The manifest fixes sources, flags, DOS basenames, ownership,
order, tools and engine files. A changed input requires an explicit reviewed
manifest/descriptor rebase. There is no agent release file or agent terminal
receipt required to start a build. Existing backend-owned comparison evidence
checks remain in place. The original executable supplies comparison evidence
outside generation; it is never a source compiler or aggregate LINK payload.

For the direct Python command, the following exit codes apply. GNU Make reports
a nonzero recipe result using its own exit status.

Exit0 means the complete original executable has been independently verified.
Exit1 means the build/verification ran and the game is still incomplete. The
validated490 cohort currently has65 unresolved names; full layout, header and
EXEPACK bytes remain open. Exit2 means invalid inputs/output or a failed phase.
Make reports a nonzero result for both incomplete and failed builds; inspect the
report and command message to distinguish them.

The new output contains:

- `build-report.json`: final status and unresolved names.
- `components/report.json`: all registered native comparisons and coverage.
- `source-seal.json`: complete fresh SOURCE ownership/order/raw hashes.
- `LINK/PARTIAL.EXE`, `LINK/PARTIAL.MAP`, response/config/logs and copied inputs.
- `components/runtime/runtime_data_crt0_s3.*`: comparison-only CRT88 artifacts.
- `HELD.json`: failure detail when a phase cannot finish.

The partial EXE is diagnostic output and is never executed by the build.
Runtime comparison objects stay outside SOURCE. One aggregate SOURCE LINK runs;
ordinary runtime helper calibrations retain their existing independent LINK
processes. Fine source-process and total-LINK counts remain untraced/null.

`matching/check.py` remains the independent strict low-level diagnostic, with
its original raw-hole rejection. The documented normal build uses the lifecycle
entrypoint above so deferred runtime verification finishes before final reports.
Current component matches and partial LINK output do not establish historical
compiler commands, original capacities/TUs, complete layout or original packed
file identity.
