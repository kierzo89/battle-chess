# Microsoft C 4.00 checked-frame investigation

**Attribution correction:** fresh MSC5.00 `/AS /Zi` with no explicit `/O` option
exactly matches every formerly C4-registered helper, and also matches equality
`9448`. [Full evidence](../evidence/msc500_default_all_frames.json) supersedes
any suggestion below that these checked frames require C4 or mixed releases.
The C4 comparisons remain valid observations of compatible output; they do not
uniquely identify the historical compiler.

Microsoft C 4.00 **`/AS /Zi`** reproduces three complete original functions:
`5A2B` (12 bytes), `A514` (20 bytes), and `946F` (29 bytes). This explains a
previously unresolved BP-frame code-generation family. It is evidence for a
compatible producer, not proof that every game module used this release.

## Provenance and reproducibility

The [PCjs catalog](https://www.pcjs.org/machines/pcx86/diskettes.json), key
`lang/microsoft/c/@versions/4.00`, identifies compiler disk 1:
[MSC-048014-400-DISK1-COMPILER.json](https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/4.00/MSC-048014-400-DISK1-COMPILER.json).
Its SHA-256 is
`75f9510af9a2dc9c6e21861729b7938c18c54c02e350ae0fe6b821d8bf51b520`.
The extracted MSC/C1/C2/C3 files also match the catalog's per-file MD5s.
[config/msc400.json](../config/msc400.json) pins their sizes and SHA-256s.
This is a historical proprietary distribution preserved by PCjs; no MIT license
or redistribution permission is claimed. Tools and downloaded archives remain
ignored. Setup is explicit: `python3 matching/setup_toolchain.py --compiler msc400`.
The normal compile path validates installed pins and never downloads tools.

C4 uses the legacy comma-separated driver interface, with options before the
semicolon: `MSC /AS /Zi C:\UNIT.C,C:\UNIT.OBJ;`. `/c /Fo` is the later CL
interface and causes an interactive filename prompt here. The runner executes
`Z:\LOADFIX.COM T:\MSC.EXE /AS /Zi C:\UNIT.C,C:\UNIT.OBJ;` in DOSBox.
K&R function definitions are required by this front end; ANSI-style parameter
definitions failed syntax analysis. No compiler executable was modified.

## Exact results

[frames_msc400_match.c](../src/frames_msc400_match.c) contains ordinary C.
The [retained build evidence](../evidence/msc400_frames_build.json) pins the
source, complete fresh object, tool manifest, compiler command, full linked
function bytes, relocations and original REA evidence IDs. The unchanged OMF
parser independently reads `codeview3_procedure` extents; the unchanged linker
resolves normal external references. No expected-size truncation, byte
postprocessing, inline assembly, or original game code is used as build input.

| Function | Target | C4 `/AS /Zi` | C4 `/AS /Os /Zi` |
|---|---:|---:|---:|
| Empty unused argument, 5A2B | 12 | **12 exact** | **12 exact** |
| Low bit, A514 | 20 | **20 exact** | 18 |
| Board clear, 946F | 29 | **29 exact** | 26 |
| Equality wrapper, 9448 | 39 | 41, mismatch | 39, mismatch |

The [six-configuration matrix](../evidence/msc400_frame_matrix.json) also records
`/Ot`, `/O`, `/Od` and `/Ox`. Default optimization retains the checked zero-size
allocation, general `mov sp,bp` epilogue, explicit caller cleanup and the
low-bit return's `jmp +0`, as observed in the original. `/Os` and `/Ot` remove
some of those instructions. `/Zi` supplies trustworthy procedure lengths; this
is not evidence that the original was a debug build.

## Remaining equality mismatch

The target equality wrapper moves AX to CX, compares CX with 1, executes
`SBB AX,AX; NEG AX`, then `JMP +0` to its general epilogue. C4's faithful
`compare(a,b,8)==0` emits a conditional branch producing 0/1 instead.
A [further controlled matrix](../evidence/msc400_equality_matrix.json) tried
unsigned external return types, unsigned casts, unsigned wrapper returns,
logical negation, comparison with 1 and an explicit local under `/Os` and
`/Ot`. None produced the target boolean conversion. These are bounded negative
results, not an exclusion of all source shapes or older compiler releases.

## Verification

`python3 -m unittest discover -s matching/tests -p test_msc.py -v` passed all
11 tests, including a genuine fresh MSC400 compile, CodeView procedure extent,
full 20-byte low-bit result, and rejection of a corrupted compiler pass.
The three-match registration proposal is `build/msc400-units.json`; canonical
unit/checker integration is coordinated by the main worker.

## Additional checked-frame matches

A subsequent fresh MSC4 `/AS /Zi` build also matches the complete 39-byte input
flag routine at `083E`, and three complete 12-byte empty callbacks at `5A37`,
`5A43`, and `BB01`. The input routine tests byte DS:0061, calls E00F, clears
that byte, calls 0886, and returns the observed code B082; otherwise it returns
zero. The meaning of B082 remains unresolved. Ordinary C sources are
[input_083e_msc400_match.c](../src/input_083e_msc400_match.c) and
[empty_callbacks_msc400_match.c](../src/empty_callbacks_msc400_match.c).

[Full build evidence](../evidence/msc400_more_build.json) retains the four
complete linked byte sequences, fresh object/source/tool hashes, normal
relocations and independent CodeView3 boundaries. Fresh REA dossiers for
[5A37](../evidence/rea_more_empty_15a37.json),
[5A43](../evidence/rea_more_empty_15a43.json), and
[BB01](../evidence/rea_more_empty_1bb01.json) each establish an inclusive 12-byte
body bound to the original executable. The registration proposal is
`build/msc400-more-units.json`; the registry owner received it directly.
