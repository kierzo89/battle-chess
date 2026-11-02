# Rebuilding the original DOS executable

This guide targets the 16-bit DOS `CHESS.EXE`, **not** the native Linux port.
For Linux use [native/README.md](../native/README.md).

The recorded fresh source-derived DOS build matches all **83,415 bytes** of the
original executable. This guide describes that verified recipe; writing this
guide does not constitute a new executable rebuild.

## Compiler and tools

| Role | Verified tool/input | Repository specification |
| --- | --- | --- |
| C compilation | **Microsoft C 5.00**, 16-bit DOS `CL.EXE` with its matching C1/C2/C3 passes | [`msc500.json`](../matching/config/msc500.json) |
| Assembly of generated/retained Microsoft assembly | `MASM.EXE` from the pinned Microsoft C 5.10 profile | [`msc510.json`](../matching/config/msc510.json) |
| Original linker and packer | `LINK.EXE` and `EXEPACK.EXE` from that same pinned 5.10 profile | [`msc510.json`](../matching/config/msc510.json) |
| Other authored assembly providers | Pinned NASM, with each provider's recorded output format | [`manifest.json`](../matching/build_pipeline/manifest.json) |
| C/runtime libraries | Pinned `SLIBC.LIB`, `LIBH.LIB`, original `LIB.EXE` and `BINMODE.OBJ` | [runtime derivation](../.reworkbench/staging/exact-build-driver-v2/runtime_library.py) |
| Host orchestration | Linux, Python 3, pinned DOSBox and NASM binaries | [build manifest](../matching/build_pipeline/manifest.json) |

Use the **file hashes**, not just version labels, to identify tools. The 5.10
profile supplies auxiliary tools; it is not an instruction to compile the
matching C with Microsoft C 5.10. C 4.00 is supported by historical experiments
but is not required by the final descriptor's C profiles. Modern MSVC, GCC,
Clang, Turbo C and Open Watcom are not substitutes for this matching recipe.

These are configurations that reproduce the binary. They are not proof of the
exact command lines used by the game's original developers.

## Compiler flags

The [base source descriptor](../matching/build_pipeline/engine_v1/descriptor.json)
records `compiler`, `compiler_flags`, source hashes and DOS source filenames.
The final [ordinary overrides](../.reworkbench/staging/exact-build-driver-v2/source-overrides.json)
and [compound recipes](../.reworkbench/staging/exact-build-driver-v2/compound-recipes.json)
then replace selected providers. Keep all three layers: compiling every `.c`
file in `matching/src` together is not the build procedure.

C flag profiles present in the base descriptor are:

```text
/AS /Zl /Zi
/AS /Zi
/AS /Gs /Os /Zi
/AS /Zl
/AM /Gs /Zi
/AS /Os /Zi
```

| Switch | Purpose |
| --- | --- |
| `/c` | Compile to an object; do not link |
| `/AS` | Small memory model |
| `/AM` | Medium memory model, for the explicitly designated units |
| `/Gs` | Suppress stack probes/checking |
| `/Os` | Favour code size |
| `/Zi` | Emit symbolic debugging information retained by the recipe |
| `/Zl` | Omit the default-library name record from the object |
| `/Fo...` | Select object output path |
| `/Fa...` | Emit the assembly listing used by compound-source recipes |

Do not add a global `/Ox`, strip `/Zi`, change memory models, rename compiler
inputs or reorder declarations to "clean up" the build. Source grouping,
compiler input names, object records, symbol ordering and relocation ordering
are part of the matching work.

For illustration, ordinary units are compiled with commands of this form inside
DOSBox, where `T:` is the pinned compiler directory and `C:` the isolated work
directory. **Select the actual flags and filename from the relevant recipe:**

```bat
T:\CL.EXE /c /AS /Zl /Zi /FoC:\UNIT.OBJ C:\UNIT.C
T:\CL.EXE /c /AS /Gs /Os /Zi /FoC:\UNIT.OBJ C:\UNIT.C
```

Some final ordinary workers instead rely on the default `UNIT.OBJ` output.
Compound providers generate a listing and assemble its reviewed transformed
form, for example:

```bat
T:\CL /c /AS /Zi /FaC:\UNIT.ASM C:\UNIT.C
T:\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;
```

`/Mx` preserves case for public/external names. The recipe-controlled listing
normalization and contribution placement are essential; those two commands
alone do not replace the compound worker. Ordinary NASM overrides use:

```sh
nasm -f obj -o UNIT.OBJ UNIT.ASM
```

## Prepare the build environment

**The public checkout is not a turnkey DOS build environment.** The frozen
driver contains `/home/kierzo/chess` paths, expects output directly under
`/home/kierzo/chess/matching/build`, and checks exact dependency hashes.
There is currently no supported one-command build entirely inside real DOS.
The Python driver runs the historical DOS tools under DOSBox and produces a
DOS executable that can subsequently be run under DOS.

1. Preserve any existing workspace. Restore the verified workspace at its
   recorded path, including the inputs listed in
   [`verification/external-inputs.json`](../verification/external-inputs.json).
   Cloning the public repository at that path alone does not restore them.
2. Supply the original `CHESS.EXE` at the workspace root for independent
   comparison, and restore the pinned tools, libraries, binary evidence and
   omitted bundle files. In particular, the runtime driver expects original
   `LIB.EXE` at `matching/build/probes/LIB.EXE` and `BINMODE.OBJ` under the final
   bundle's `source-inputs/`. Do not substitute prebuilt game objects.
3. Prepare Python at `matching/build/test-env/bin/python`, with the project's
   [development requirements](../matching/requirements-dev.txt). The driver
   requires `/usr/bin/python3`, `/usr/bin/dosbox` and `/usr/bin/nasm`; the latter
   two must match the manifest hashes, not simply any distribution versions.
4. Run the published source and asset integrity checks:

   ```sh
   python3 tools/verify_source_snapshot.py
   python3 tools/verify_asset_snapshot.py
   ```

The existing acquisition helpers are available for the pinned tool profiles:

```sh
python3 matching/setup_toolchain.py --compiler msc500
python3 matching/setup_toolchain.py --compiler msc510
python3 matching/setup_runtime.py
python3 matching/setup_libh.py
```

These helpers download/validate their specified historical inputs; they do not
restore every omitted evidence file, install the pinned host binaries, or make
the whole build portable. Read their provenance and obtain any required rights
to the historical distributions. Proprietary tools/libraries are not bundled.

## Run the verified driver

From the restored `/home/kierzo/chess` workspace, choose a **new** output name.
Both that directory and its `-source269` sibling must not exist:

```sh
cd /home/kierzo/chess
/usr/bin/python3 -B matching/build_exact.py \
  --output /home/kierzo/chess/matching/build/dos-rebuild-001 \
  --preflight-only

/usr/bin/python3 -B matching/build_exact.py \
  --output /home/kierzo/chess/matching/build/dos-rebuild-001
```

Preflight validates the bundle and base inputs without generation; it does not
prove all subsequent phases will succeed. The full run generates the base
source cohort, builds 38 final override jobs, seals **225 ordered objects**,
derives the runtime library, then links and packs. It uses eight compile
workers and serial final linking. Do not run overlapping full builds.

The final linker and packer commands are:

```bat
T:\LINK /NOD /NOEXTDICTIONARY /DOSSEG /NOFARCALLTRANSLATION /MAP /STACK:4096 @INPUTS.RSP
T:\EXEPACK PARTIAL.EXE PACKED.EXE
```

`INPUTS.RSP` contains the exact ordered object list, then `PARTIAL.EXE`,
`PARTIAL.MAP` and `T:\SLIBC.LIB;`. The last name refers to the freshly derived
runtime library. The driver merges the authentic libraries and replaces
`TXTMODE` with `BINMODE.OBJ`; do not bypass that step or sort the object list.
The actual commands are in [link_pack.py](../.reworkbench/staging/exact-build-driver-v2/link_pack.py).

## Verify and run the DOS game

Inspect `matching/build/dos-rebuild-001/build-report.json` and
`matching/build/dos-rebuild-001/final/verification.json`. Success requires:

- `status`: `PASS_FRESH_SOURCE_DERIVED_EXACT_EXECUTABLE`
- `whole_expanded_image_equal`, `relocation_order_exact`, `packed_bytes_equal`: true
- Expanded image: **401,131 bytes**; relocations: **173**
- Packed executable: **83,415 bytes**, SHA-256:

```text
c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd
```

The runnable result is `final/PACKED.EXE`. After verification, copy it to a
separate game directory as `CHESS.EXE`. Place `ALLCANM1` and `ALLCANM2` alongside
it, following the [asset-bank rebuild instructions](../assets/README.md#rebuild-the-game-data).
Run `CHESS.EXE` from that directory in DOS or DOSBox. PNG previews are not DOS
runtime inputs; the two asset banks remain external to the executable.

If verification fails, inspect `base.log`, the override logs, `LINK.LOG`,
`PACK.LOG` and the reports. Do not refresh hashes or disable guards to turn a
mismatch into a pass. Moving the pipeline to another root or tool distribution
requires a separately reviewed portability change and a fresh full comparison.
