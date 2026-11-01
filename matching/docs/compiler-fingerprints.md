# Compiler configuration fingerprints

This pass used REA MCP/Ghidra on SHA-256
`c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd`.
REA addresses use image offset + `0x10000`. Retained evidence is linked below;
each JSON contains the complete inline Evidence, profile, and limitations.

## Complete input-dispatcher control

The [fourteen compiler controls](obtain-input-compiler-controls.md) now distinguish
pinned C5.00 `/AS /Zi` from the tested C5.10 alternatives for the complete
1439-byte dispatcher at image0254. Explicit `/G0` and `/Zl` leave its complete
CODE output unchanged. C4's syntax rejection of the unchanged source is not a
version exclusion.

`/Zi` is part of code generation here: plain `/AS`, `/AS /Zd`, and `/AS /O /Zi`
all generate the same different1402-byte CODE contribution. The matching
configuration emits1439 procedure bytes plus its genuine standalone alignment
NOP. Microsoft's original manual section3.3.12 explains the effect: `/Zi`
without explicit `/O` suppresses code motion while retaining simple
optimizations. Exact flags matter beyond compiler boundary metadata. These
controls identify a compatible producer configuration, not a unique historical
command or evidence that debug symbols shipped in the executable.

## Observations and configuration constraints

* [Runtime copyright bytes](../evidence/rea_compiler_copyright_bytes.json),
  `ev_60f1de174462ea426b0287bdbf96df68077edda583c285c735fd672a801e9c11`:
  REA reads `MS Run-Time Library - Copyright (c) 1987, Microsoft Corp` at
  `0x212c9` (file `0x114c9`). This independently corroborates Microsoft runtime
  provenance. The string does not identify the compiler front end or patch release.
* [Startup bytes](../evidence/rea_compiler_startup_bytes.json),
  `ev_635da755c1e157dc195b86a6a69738ee27510874ce1c9e3017f9155cc5efe9d2`:
  image `ea86` begins DOS version handling; `eaa3` sets SS; `eafa` performs
  `push ss; pop ds`. At `eb08`–`eb14`, three 16-bit values are pushed and a near
  call reaches image `0010`. This supports a common data/stack group and a near
  main entry. Segment immediates are linker/packer values, not universal runtime
  linear addresses. The EXE is packed and its literal segment operands cannot
  be treated as a measured executing memory layout.
* [Main prologue bytes](../evidence/rea_compiler_prologue_main.json),
  `ev_18ca699d95ab49e6dc4054df69e9327cffbcbddf8def5201b5f3e6b0979e440c`:
  `push bp; mov bp,sp; mov ax,8; call ecaa; push si` reserves locals through the
  checked stack helper. Stack probing is enabled for this module. A baseline
  using `/Gs` would remove that defining feature.
* [Caller at 8fca](../evidence/rea_compiler_near_caller.json),
  `ev_d2defdcc03c0c31563f6e9d150ae644cbf5a766282982da05003f397f8ac5fac`:
  four globals are pushed in reverse order, the call is near, and the caller
  adds 8 to SP. This is direct instruction evidence for the ordinary 16-bit C
  caller-cleanup convention. Ghidra's inferred signature alone is not the basis.
* Existing math routines use signed comparisons, 16-bit arguments at BP+4/BP+6,
  AX results, and near returns. Multiple epilogues/returns survive. Default
  near code and near data are consistent with the small model. Explicit far
  graphics routines and far asset pointers do not require a large default model.

The first controlled compilation baseline should therefore be **Microsoft C
5.x, `/AS /G0`, ordinary C calling convention, stack checks enabled**, and
optimize-for-speed/default optimization as the first hypothesis. The model and
flags are constraints to test, not a recovered original command line. The
absence of a stack frame in 8fca and duplication of returns favor optimization
over a fully unoptimized build; they do not select every optimization subflag.
The initial candidates contain no instructions requiring an 80186.

The later timed-wait reconstruction at image 941b is an actual additional
44-byte C match using `/AS /Gs /Ot /Zi`, with only the near timer call resolved
at ea5b. [Its REA dossier](../evidence/rea_search_1941b.json) establishes the
inclusive 941b–9446 body. [The controlled build record](../evidence/rea_search_wait_build.json)
retains the exact linked digest and relocation log. The same ordinary C source
under `/Ox` produces 77 bytes because its loop optimizer changes the loop.
This further constrains the practical baseline to `/Gs /Ot` for that source,
and demonstrates why a universal `/Ox` assumption is insufficient.

The initial Microsoft C 5.10 experiments for 8fca remained unmatched: ordinary
`while` syntax was optimized to 55 or 57 bytes, while guarded `do/while` or
equivalent goto syntax produced 65 bytes. The latter has an extra internal
alignment NOP after the early return, plus corresponding branch displacement
changes. Nine further C5.10 flag/prefix experiments, including `/Zp1`, `/On`,
and legitimate preceding C functions, did not remove this discrepancy;
[negative experiment record](../evidence/rea_search_8fca_flag_prefix_experiments.json).

A subsequent controlled C5.00 matrix found that **`/AS /Gs /Os /Zi` builds the
complete 64-byte 8fca function exactly**, using the existing ordinary C
candidate and proper external relocation. [The matrix](../build/msc500/FLAGS.json)
records that `/Ot` and `/Ox` still produce 65 bytes, and adding `/O` before
`/Os` also changes the outcome. Thus option order/combinations must be retained
exactly, and this match is stronger evidence than a broad default-optimization
label. No NOP removal, code masking, or assembly insertion was used.

The 11-byte function at cb50 also matches C5.10 `/AS /Ot /Zi` exactly with
stack checks enabled: it sets byte DS:11b8 to ff and returns.
[REA dossier](../evidence/rea_search_1cb50.json) and
[controlled linked build](../evidence/rea_flag_11b8_build.json) retain its
complete extent, compiler identity, and both relocations. Its subsystem
meaning remains unresolved.

### Bounded frame-generation experiments

Some remaining functions use a BP frame, zero-size checked stack allocation,
and `mov sp,bp; pop bp; ret` even when the recovered body needs no locals.
In nine focused C5.00 compile runs, an unused ordinary argument, K&R argument,
and variadic argument did retain BP, but generated only `pop bp; ret` (10
bytes for the empty argument function, versus 12 originally). `/Oy` and
`/Oy-` did not produce objects in this compiler. `/Or /Os`, `/Or /Ot`,
`/Os /Or`, and `/Ot /Or` all retained the same mismatch: empty argument
10/12 bytes, low-bit return 16/20, equality wrapper 35/39, and board-clear
wrapper 23/29. [Controlled matrix](../evidence/rea_frame_or_flag_matrix.json).
Consequently `/Or` has not explained these epilogues. Unrecovered source
constraints, function-specific settings, or modules built by another compiler
remain possible; the bounded experiment does not select between them.

**Correction from a fresh bare-default C5.00 experiment:** `/AS /Zi`, with no
explicit `/O` option, exactly reproduces the checked BP-frame family, including
all ten formerly C4-registered functions and the 39-byte equality wrapper.
[Complete retained comparisons](../evidence/msc500_default_all_frames.json)
record full compiler extents and relocations. The earlier bounded matrices
above describe their tested explicit-optimization settings; they did not test
this successful configuration. These functions do not establish a mixed C4/C5
build, and no extra source constraints are needed to explain their epilogues.

The contemporary Microsoft C 5.0 User's Guide documents `/AS` as small model,
`/Gs` as removing probes, and `/G2` as selecting 80286 instructions:
[Microsoft's 1987 manual scan](https://www.bitsavers.org/pdf/microsoft/msdos_c/Microsoft_C_5.0_1987/410840001-500-R04-0887A_Microsoft_C_5.0_Users_Guide_1987.pdf).
Modern MSVC options are not interchangeable with this historical compiler.

## Useful C candidates beyond min/max/abs

### 7da8: initialize an eight-byte structure, 23 bytes

[Dossier](../evidence/rea_compiler_candidate_7da8.json),
`ev_489431e4e30362e8136be0f11684216db9031ca78cd09f157e29e0a49c802e31`.
Complete inclusive range `0x17da8`–`0x17dbe`. It stores `-1` at DS:9880,
then copies eight bytes from DS:04e2 to DS:88dc with four MOVSW instructions,
preserving DI and SI and setting ES=DS. A plausible ordinary C reconstruction
uses assignment between two eight-byte structs after a scalar assignment.
This exercises a useful code-generation fingerprint (inline aggregate copy),
but the original record type is unknown. Do not count a handcrafted opcode
macro or inline assembly version as a C match.

### 3ac2: bounded array consumption, 33 bytes

[Dossier](../evidence/rea_compiler_candidate_3ac2.json),
`ev_ca292558e81f0da68187cba92fa62c89a62f4c1b5d70edbec523974bdd51d05f`.
Complete inclusive range `0x13ac2`–`0x13ae2`. If signed DS:008e is less than 4,
it returns the word at DS:8d1a indexed by the old value and increments the
index. Otherwise it calls image 0d8d with near pointer 4d6b. Candidate C:
`if (index < 4) return values[index++]; else return error(message);`.
The error routine's return meaning and message text remain unresolved.
This tests direct global addressing, signed comparison, postincrement order,
array indexing, and a relocated call. Its call displacement must be fixed by
normal linking before exact bytes can match.

### 8fca: iterate a generated four-word state, 64 bytes

The caller dossier above includes a scalar increment/decrement around one
call, a preparation call, then a loop over four DS words until byte DS:8d18
becomes zero or a predicate returns zero. It returns 1 on the latter outcome
and 0 on exhaustion. This is larger than the first two candidates and should
follow successful simple compiler matches.

## Controlled Microsoft C 5.10 probes and EXEPACK identity

The compiler recovered by the main investigation from Microsoft's own MS-DOS
repository is pinned by [its manifest](../toolchains/msc510/manifest.json).
This is a working compatible code generator; finding compatible bytes does
not by itself prove that the historical executable used exactly this release.

[Struct-copy matrix](../evidence/rea_compiler_struct_copy_matrix.json) compiles
the ordinary `counter=-1; dst=src;` source with symbolic extern globals.
`/AS /Ox` produces the exact 7da8 instruction skeleton (23 bytes), followed by
a segment-alignment NOP. Its only unresolved fixups are counter, destination,
and source offsets. `/O`, `/Ot`, and `/Os` without `/Gs` add a five-byte
zero-byte stack probe; `/Od` additionally preserves a BP frame. A probe using
constant pointer dereferences produced different addressing instructions,
which illustrates why matching source shape matters.

[Array-pop matrix](../evidence/rea_compiler_array_pop_matrix.json) compiles
`if (index < 4) return values[index++]; return error(message);`.
`/AS /Gs /O` and `/AS /Ox` both produce the exact 3ac2 instruction skeleton
(33 bytes) followed by a NOP. All differences are unresolved proper global/call
relocations. `/Gs /Os` emits a shared return with an extra short jump, and
`/Gs /Od` emits a substantially different BP-framed function. Thus these
controlled candidates support speed/default optimization and disabled probes
for these modules. They exclude `/Os` and `/Od` for this source shape; they
cannot distinguish `/Gs /O` from `/Ox`. A skeleton comparison receives no C
byte-match credit until the relocations are resolved by a validated build.

The source tree under pinned Microsoft MS-DOS commit
`2d04cacc5322951f187bb17e017c12920ac8ebe2` was searched through its complete
1,644-entry Git tree for `crt0`, `chkstk`, `cstart`, `rterr`, `c0.asm`,
`crtlib`, and `cstartup` paths. None were present. The compiler tools do not
by themselves establish a runtime-source comparison between C 5.00 and 5.10.
The exact historical release remains unresolved.

There is stronger direct evidence for the packer implementation:
[REA stub bytes](../evidence/rea_compiler_exepack_stub.json),
`ev_98db1ade26066d2e553c32273c4f9e700a36bc8506b0bf9b913c5152a098aa97`,
read all 283 bytes from original entry `0x24142`. These bytes are **identical**
to file offsets `0x35e2`–`0x36fc` inclusive in the pinned Microsoft
`EXEPACK.EXE`. They include the entire decompressor instruction sequence and
the corrupt-file diagnostic. The shared range SHA-256 is
`3c2ecf0c7854abfe0390cfa2482fc3941cf255546ce1629132eb62bb08f3d435`.
[Comparison record](../evidence/rea_compiler_exepack_comparison.json) records
the artifact hashes and offsets. Other EXEPACK releases may embed the same
stub, so this establishes exact compatible unpacker code, not unique producer
version attribution.

[REA packer header bytes](../evidence/rea_compiler_exepack_header.json) at
`0x24130` decode as nine words:
`ea86 0000 0000 02a7 1000 6980 61ef 0001 4252`.
The final word spells the `RB` signature, and the first two words identify the
saved original CS:IP as `0000:ea86`. This agrees with the independently
inspected C startup at image ea86; the operating-system entry instead points
to the EXEPACK wrapper. The unpacker reads header fields directly: final
transfer uses the first far-pointer pair; stack restoration uses the words at
offsets 8 and 10. The remaining header fields need full format verification
before reconstructing a complete packed file.

## Coverage and unknowns

| Question | Status |
|---|---|
| Runtime family | Microsoft provenance corroborated by literal bytes and existing R600x diagnostics |
| Default memory/call model | Small/near C baseline strongly supported; mixed far modules observed |
| Stack probes | Present in main; enabled for that module |
| Instruction target | Initial candidate set compatible with 8086; whole-program target not proven |
| Compatible compiler | Pinned Microsoft C 5.00 reproduces all currently authored C matches; unique historical release remains unproved |
| Verified C configurations | `/AS /Zi` with probes and its documented debug/code-motion interaction; `/AS /Gs /Os /Zi` for optimized helpers; `/AS /Os /Zi` for the flag setter |
| Linker/packer command | LINK 3.65 verified for bounded independent experiments; EXEPACK 4.06 reproduces the original from recovered image only; complete source link remains missing |
| Whole-program uniform flags | Unresolved; do not generalize from one module |

REA's Ghidra assembly text reverses segment MOV operand direction in some
locations (also seen in the earlier Huffman evidence). For example, the EA64
[dossier](../evidence/rea_compiler_ea64.json) prints `MOV AX,ES` at EA6D while
the original `8e c0` encodes `MOV ES,AX`. Use bytes and an independent decoder
for compiler fingerprints. Pseudocode is analysis output, not original source
or a compile-and-match result.
