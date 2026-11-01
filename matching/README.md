# Matching reconstruction: final status

The complete source-derived executable match was verified on 1 November 2026.
See the [repository README](../README.md) for final status, source locations,
external dependencies and reproducibility limits. The older checkpoint report
below is historical and does not describe the final executable result.

---

# Battle Chess matching decompilation

The goal is an independent working game reproducing all **83,415 original CHESS.EXE bytes**, including the DOS header, all 173 native relocation sites and EXEPACK output. Every external name resolves. A working rebuilt game and full binary identity remain unproved.

All **522 registered comparisons pass** in the closed fresh SOURCE286 build. Accepted coverage is **69,039/83,415 original-file bytes (82.7657%)** and **173/173 native relocation sites**. There are 255 genuine C functions /48,482 CODE bytes, 159 C DATA contributions /13,228 bytes, 35 authored ASM CODE contributions /19,199 bytes and 7 ASM DATA contributions /92,348 bytes. Expanded-image coverage is 179,035/401,131 bytes. This explicitly reviewed checkpoint adds **586 authored ASM CODE bytes and one native relocation site**, with no new C credit.

**SOURCE286 =211 C +31 ASM +37 COMMON +6 MIXED +1 BSS.** Evaluator3902 combines nine preserved genuine C procedures (3315 bytes), two authored ASM procedures (586 bytes), and the genuine one-byte EOF NOP in one complete object. The NOP is not extra procedure credit. Its full C5 object remains separately retained as a typed sidecar. All 285 other whole SOURCE objects retain their bytes and order; all prior 520 native hashes/sizes/statuses and all 37 providers are unchanged. Authentic LINK closes with zero unresolved names.

**869 targeted regression tests passed**, with no failures, errors, skips or changed pinned inputs. This is not a full-suite rerun. Independent evaluator audits verify every one of 3902 native and actual linked bytes, all223 fixup fields and both native relocation sites at four load bases. Retained graphics7262 verifies all639 fields and24 native relocation sites; tail874 verifies all53 fields at four bases. Ten retained actual-link scopes also pass: history, BIOS, motion, prior mixed decoder, scratch storage, code, data, BSS, CRT and far storage. All five prior mixed sidecars are preserved. The symbolic bank has **2641 fields =2136 CODE +4 DATA +501 discarded DEBUG**; exactly17 evaluator raw-only DEBUG views moved to its unchanged C5 sidecar. These are not additional FILE bytes.

Absolute layout, literal DS accesses, complete source/data order, header, packing and working-game validation remain open. All native relocation sites are covered by verified contributions, but this does not establish the complete executable layout or hash. No generated partial EXE has been executed.

See [current mixed6 checkpoint](evidence/verification-255-c522-mixed6-data13228-p37-targeted869-source286-link0-checkpoint.json), [authoritative build](build/reworkbench-1843e6c71e744150/build-report.json), [generated progress](build/PROGRESS.md) and [previous mixed5 checkpoint](evidence/verification-255-c520-mixed5-data13228-p37-targeted869-source286-link0-checkpoint.json). Earlier checkpoints below retain their historical scopes.

The [241 promotion checkpoint](docs/promotion-241-checkpoint.md) verifies
**241 C functions / 45,656 bytes** and **98 C DATA contributions / 1,898 bytes**.
All 401 units and all 933 tests pass in one fresh zero-skip regression.
Four compiler-owned CONST allocations retain 443 uncredited bytes. COMMON storage
has 30 definitions / 94 allocation bytes with zero matching credit. Original-file
spans cover **60.948%**; 113/173 MZ sites verify.
Actual LINK of 167 real source objects still fails with **298 missing providers**.
No complete independent executable exists yet. See the
[immutable checkpoint](evidence/verification-241-promotion-checkpoint.json).

The earlier188 checkpoint adds [four complete C functions totaling1558 bytes](docs/source-layout-188-checkpoint.md).
The input dispatcher matches all1439 bytes inside a natural2094-byte main/input/exit
source contribution. Two dialog row helpers and serial initialization add119 bytes;
whole452/344-byte source contributions also verify. The earlier
[six-function184 checkpoint](docs/source-layout-184-checkpoint.md), typed filename
initializer, medium-model evaluator and uncredited CONST24 remain preserved.
Earlier [menu DATA definitions](docs/menu-data-definition-checkpoint.md),
[pointer-DATA validation](docs/pointer-data-backend.md),
[complete C main](docs/main-0010-extent.md) and
[LINK configuration controls](docs/main-link-configuration.md) remain verified.
The [frame audit](docs/unexplained-frame-audit.md)
withdraws fourteen older padding-dependent C matches. Use the fresh registry and
generated report for current credit; earlier exact-output records retain their
historical source assumptions. Remaining work is tracked in [next work](docs/next-work.md).

## Build and verify

Python 3.10+, NASM and DOSBox are needed. Install the independently pinned
Microsoft C 5.00 profile once, then run fresh builds:

```sh
python3 matching/setup_toolchain.py --compiler msc500
python3 matching/setup_toolchain.py --compiler msc510
python3 matching/setup_runtime.py
python3 matching/setup_libh.py
make -C matching build OUTPUT=build/local-run-001
matching/build/test-env/bin/python -m unittest discover -s matching/tests -v
```

The normal build also runs via `make -C matching build OUTPUT=build/local-run-001`.
Make prefers the existing project Python3.11 environment; use PYTHON=/path/to/venv/bin/python to override.
Use a new output directory each time. The Python command returns1 for a checked
but incomplete game and2 for a failed phase or invalid inputs. GNU Make reports
a nonzero recipe result using its own exit status. The current deferred runtime row is
verified from the same fresh aggregate LINK before final reports. See
[building instructions](docs/building.md). The strict `check.py` diagnostic retains
its independent raw-hole rejection.

The original-8086 execution tests use the pinned Unicorn2.1.4 dependency in
`requirements-dev.txt`. The188 checkpoint runs all379 tests without skips in an
isolated `build/test-env` Python3.11.9 environment. Exact logs and limits are in
[evidence/verification-188-contexts-checkpoint.json](evidence/verification-188-contexts-checkpoint.json).

The explicit installer checks archive and extracted-file hashes. The checker
never downloads tools. The compiler is a historical proprietary distribution
preserved by PCjs, kept under ignored `toolchains/msc400/` and `toolchains/msc500/`; its provenance is
separate from the Microsoft MS-DOS repository's MIT-licensed 5.10 tools.
The 5.10 profile also supplies the independently pinned LINK 3.65 used for
five compiler-support library members; current authored C uses C 5.00.

The current C reconstruction is reproducible with **Microsoft C 5.00, small
model for near code and medium model for the far evaluator, with its ordinary
16-bit C calling conventions**. `/AS /Gs /Os` reproduces many
game helpers; bare `/AS` with no explicit `/O` option reproduces the checked BP
frames and equality wrapper. `/AS /Os` retains stack probes for the matched
flag setter. `/Zi` both supplies compiler-reported extents and affects code
generation: without explicit `/O`, C5 suppresses code motion while retaining
simple optimizations. The input dispatcher requires this tested configuration;
[14 compiler controls](docs/obtain-input-compiler-controls.md) retain the complete
outputs. This does not prove the original shipped with debug symbols. Main retains
stack probes, so `/Gs` must not be assumed for every module. Per-function
records are in [config/units.json](config/units.json).

Far evaluator procedures use canonical `/AM /Gs /Zi` with explicit CS-relative addresses,
with physical image positions tracked separately. An independent authentic LINK
experiment verifies this arithmetic, including a failing negative control.
Fresh `/AM /Gs /Zi` compilation preserves all3902 emitted CODE bytes and
fixup/CV semantics while producing the source-specific segment UNIT_TEXT. This
removes the conflicting near/far PUBLIC _TEXT frame requirement. It does not
uniquely establish the original command. See [coordinate verification](docs/nonzero-cs-linking.md)
and [memory-model evidence](docs/evaluator-memory-model-control.md).
The later [named-segment LINK control](docs/medium-segment-linking.md) compiles
two distinct medium-model source files with a small-model main and genuine
SLIBC startup. Both object orders link and execute successfully, with complete
function and relocation agreement. This is configuration evidence, with zero
target matching credit.

Recent search-loop and graphics helpers also reproduce complete function bytes
with the default C5.00 configuration. See [search reconstruction](docs/search-loop-matches.md)
and [graphics helpers](docs/fill-next-matches.md). Shared structure layouts and
contiguous source contributions are checked separately from function coverage.

C4 also reproduces several functions, but fresh default-C5 comparisons reproduce
every formerly C4-registered function and the equality wrapper. Those matches
therefore provide no reason to infer separately compiled C4/C5 modules. The
search helper and runtime startup support C5.00 as a compatible reconstruction
baseline; exact historical producer commands remain unresolved. See [C4 investigation](docs/msc400-investigation.md),
[cross-version evidence](evidence/compiler-cross-version.json),
[compiler comparison](docs/msc500-comparison.md),
[configuration evidence](docs/compiler-fingerprints.md), and
[packing layout](docs/exepack-layout.md). Exact original flags for every module,
linker ordering, and all types remain work in progress.

The large animation stage now matches all3,371 bytes, and the full evaluator
matches all2,803 bytes. The earlier eleven-function3,902-byte evaluator
contribution depended on two unread locals. Current evaluator credit covers
nine procedures/3,316 bytes, including103/130-byte pawn helpers; complete CODE
context remains unresolved after their removal. See [full evaluator evidence](docs/full-evaluation-match.md), [frame audit](docs/unexplained-frame-audit.md), and
[animation checkpoint](docs/stage-bb0e-checkpoint.md). Eight new typed DATA
contributions add114 separately verified initialized bytes without function or
packed-file credit.

Earlier search and board/move experiments reproduced complete5,350/1,016-byte
contributions. Their unread local assumptions are now withdrawn: current credit
excludes search_window80 and apply_move246, and their complete source context
remains unresolved. The compositor matches its full789-byte procedure.
[Source layout evidence](docs/source-contribution-layout.md) separates CODE
context from individual function credit; consult the fresh source inventory
after the [frame audit](docs/unexplained-frame-audit.md). Authentic
LINK alignment and uninitialized COMMON allocation controls establish concrete
constraints for the eventual whole-source link; neither adds file-byte credit.

## What earns matching credit

The checker pins the original executable hash and independently verifies each
function's complete boundary against retained REA MCP evidence. An explicit
proof also admits a compiler-emitted unreachable return omitted from REA's
reachable body: it requires complete raw bytes, the retained CFG, the adjacent
next function and the fresh CodeView extent. See [the repetition proof](docs/repetition-9c34.md).
A second narrow proof covers a six-entry inline switch table and a duplicate
unreachable branch. It requires the bounded dispatcher, retained CFG, seven
fresh CODE-offset fixups, complete raw span, adjacent entry and full CodeView
extent. See [the switch proof](docs/inline-switch-a181.md).
For C units it:

1. Validates the compiler distribution against independent checked-in hashes.
2. Compiles ordinary C in a fresh DOSBox scratch directory; no inline assembly,
   byte emission, included prebuilt objects, or original executable bytes enter
   the compiler input. Source fingerprints must agree across the build.
3. Parses the emitted OMF object and CodeView procedure length. Alignment bytes
   outside that compiler-reported procedure are recorded as module padding;
   no expected target length is used to trim generated code.
4. Applies supported OMF relocations using explicit code/DGROUP placements.
   Own public-CODE offsets also support inline switch tables. Every changed
   address field is logged. Unsupported fixups fail the build.
5. Compares every emitted function byte, including all resolved address fields,
   against the original. Different bytes or lengths fail. No fields are masked.

Matched C and runtime extents must also reproduce the complete original MZ
loader-relocation set inside their boundaries. Symbolic far-data OFFSET16 and
BASE16 fields are linked separately; only BASE16 earns a loader site. Explicit
absolute ABI symbols, including the archived `__AHSHIFT=12`, earn no loader
site. See [far-data linking](docs/far-data-linking.md).

`c_matched` counts actual compiler output; `asm_matched` counts separately
assembled sources. `runtime_matched` counts independently supplied, pinned
library code and initialized data linked from complete OMF segments, with zero authored-C or ASM
credit. [Runtime linking](docs/runtime-link-plan.md) records the input library,
placements and MZ relocation checks. The checker generates these bytes afresh
from the library and verifies their full extents. Old math assembly references and portable semantic
[math16.c](src/math16.c) receive no additional credit when a routine is C-matched.
The Rust engine, autogenerated pseudocode and recovered original bytes receive
no compiler matching credit. The compiler-only workflow reads source and tools;
the original supplies expected comparison bytes and established link addresses.

Three pinned LIBH members are linked with authentic Microsoft LINK in fresh
DOSBox directories. This preserves legitimate overlapping library records
without relaxing the strict C object parser. The entire emitted MZ image and
relocation set must match the independent segment metadata and original bytes;
there is no target-length trimming. See [the helper backend](docs/authentic-helper-backend.md).

Exit 0 means all currently claimed units match. `--require-complete` exits 1
until an independently source-built complete executable matches all original
bytes. Exit 1 also reports a failed unit; exit 2 reports an invalid target or
verification configuration. `--target`, `--output` and `--nasm` select an original
path, report directory and assembler. All runs rebuild; object reuse is limited
to identical source/profile/flags within a single run.

Standalone authored C data has a separate `c-data` backend and `c_data_matched`
status. The first contribution is an 80-byte typed game lookup aggregate.
Fresh C compilation must emit its complete initialized DATA allocation, with
no code, BSS, holes, fixups or padding substitutions. It receives zero function
credit; compressed-region data contributes only to expanded-image coverage.
See [the data reconstruction](docs/game-move-lookup-data.md) and
[the search continuation](docs/quiet-search-switch.md).

The graphics workspace uses the separate closed
`masm510-graphics-workspace-physical-data-omf` assembly backend. It assembles
explicit zero-valued DATA from source into two complete private PARA segments,
validates every record and bounded LIDATA tree, and compares all86,000 bytes with
the original EXEPACK-decoded image and a complete independent REA read. Its
engineering65520+20480 split does not claim historical segment boundaries,
source ownership or C capacity. The generic OMF and NASM DATA contracts remain
unchanged. See [the source](src/data/graphics_workspace.asm),
[backend](graphics_workspace_data16.py),
[independent layout review](build/graphics-workspace456-independent-native-layout-review/README.md)
and [canonical audit](build/screen-carrier457-canonical-admission/candidate-review.json).

## Generated reports

- [PROGRESS.md](build/PROGRESS.md): readable status.
- [report.json](build/report.json): per-function bytes, source/object/tool hashes,
  compiler flags, compiler-reported extents, relocation arithmetic and first differences.
- [functions.csv](build/functions.csv): legacy entries, pseudocode and C/assembly status.
- [analysis_candidates.csv](build/analysis_candidates.csv): r2 versus REA/Ghidra entries.
- [file_coverage.json](build/file_coverage.json): every verified and remaining file range.
- [image_coverage.json](build/image_coverage.json): separate uncompressed image spans,
  including initialized runtime data. Data inside the compressed region earns
  no packed-file byte credit. Its REA evidence is bound to the independently
  regenerated, hash-pinned analysis carrier; it is never a reconstruction input.

The old r2 inventory has 371 candidates and REA/Ghidra finds 386 in the packed
artifact. Some are compressed data misidentified as code. A whole-program
function count and code-byte denominator remain unknown. The expanded original
image must be inventoried as well. File-span coverage has a known 83,415-byte
denominator, but source coverage of a few functions is not a full executable build.
DAZZLE.COM and TUNNEL.COM are outside this initial target.

## Full-byte pipeline

The verified final stage is Microsoft EXEPACK 4.06. A controlled analysis
round-trip from recovered original bytes reproduces all 83,415 target bytes.
That experiment gets **zero reconstruction credit**. A genuine source/link build
must generate the 401,131-byte prepack image, its 173 relocation sites and
compatible MZ metadata before packing. No recovered code placeholders may turn
that experiment into a claimed completed decompilation.

Next: grow the C matches with the verified C5.00 configurations; classify the
expanded image; reconstruct data and remaining modules; establish full linker
layout; and feed a source-built image through the verified packer. [Evidence
ledger](docs/evidence.md) distinguishes observations, inferences and unknowns.

The workflow takes inspiration from [Halo 2's checker](https://github.com/kirklandsig/halo2-decompiled/blob/main/tools/check.py):
pin the original, rebuild source, compare functions, record failures and derive
progress from verification. No Halo 2 implementation code was copied.

Optional Unicorn tests execute original 8086 bytes and compare math semantics
with portable C, exhaust all 65,536 absolute-value inputs, and check stack
allocation and a segment-load disassembly discrepancy. Install
`matching/requirements-dev.txt` in a virtualenv to run those tests; without
Unicorn/host cc they explicitly skip. The byte checker has no Python package
dependencies. OMF, CodeView, relocation, compiler integrity, failure handling,
source-change, and EXEPACK parser tests accompany the build workflow.

The current menu/frame matches and their boundaries are documented in
[menu-panel-match.md](docs/menu-panel-match.md). The
[complete source contribution audit](docs/source-contribution-layout.md)
distinguishes exact function bytes from whole-object link readiness. Authentic
huge-buffer and CRT0/DOSSEG controls are recorded in the
[image layout plan](docs/image-layout-plan.md); they add configuration evidence
and receive no game byte credit.

The [complete graphics/menu reconstruction](docs/graphics-menu-match.md) now
reproduces one continuous 7,262-byte, twenty-two-function C contribution. The
[pen movement/line matches](docs/pen-drawing-match.md) retain their remaining
source-context limits. [Asset consumer findings](evidence/far-storage-consumer-findings.md)
identify real uses of the 70k compressed bank and 150k decoding arena without
claiming original allocation ownership.

The sign helper now has a complete42-byte C proof including both unreachable
return jumps, with byte-mutation tests and exhaustive16-bit execution checks.
The [arena consumer findings](evidence/arena-next-consumer-findings.md) document
new initialization/checkpoint C matches and their remaining allocation limits.
