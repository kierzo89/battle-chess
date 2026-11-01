# Authentic four-byte same-segment far calls

Microsoft C 5.00 with `/AS /Zi` emits the original four-byte `PUSH CS; CALL near`
sequence itself when the far callee is defined in the same translation unit.
No linker shortening is required. A reconstructed ordinary-C translation unit
now reproduces the complete **608-byte CODE SEGDEF** covering all six contiguous
functions from image `0x95df` through `0x983e`, including the formerly unmatched
246-byte `apply_9749` and its real 61-byte far helper. All six independent CV3
procedure extents also compare byte for byte. No opcode rewriting, target
trimming, inline assembly, fake callee or copied target code is used.

The stable source is [move_module_match.c](../src/move_module_match.c).
Full fresh compiler provenance, object hash, complete segment comparison,
individual independent extents and every fixup are retained in
[move-module-500-default.json](../evidence/move-module-500-default.json).
The source SHA-256 is
`297e20776de31e3194ff33c9a7283bb371b024017d7c2420cadfad701a85e913`;
the object SHA-256 is
`6e44e4c6f026849b8bf0f697a1414a4a9f1906e6b0225a741f868b46277b249c`;
the complete linked segment SHA-256 is
`7260afbb41927a446920fada19eace747620d3453e873768cb7982186c4f2e15`.

## Original bytes and the compiler/linker distinction

REA MCP read the original instruction neighborhood at linear `0x197af`:
Evidence `ev_843f53ccb765a552f4ca3de2676616b8456052bc7892c1e8820d69546a8387ef`,
retained in [rea_farcall_97b4.json](../evidence/rea_farcall_97b4.json).
The original call at image `0x97b4` is `0e e8 27 fe`, targeting `0x95df`.
Immediately afterward is `83 c4 06`, the caller's argument cleanup. There is
no NOP before or after the four-byte call in that instruction neighborhood.
The target hash is
`c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd`.
This is static shipped-artifact evidence, not a record of execution.

The original far helper has a complete 61-byte REA body `0x195df–0x1961b`,
ending in RETF. Evidence
`ev_7c18bbee1907abce67c396b62de13a60e0f969a15280dff56b124cd5f8f88d14`
is retained in [rea_castle_95df.json](../evidence/rea_castle_95df.json).
The caller has a complete 246-byte body in `rea_moves_19749.json`.

Fresh independent compiler experiments tested an external far declaration and
a real far function definition in the same translation unit, both before and
after the caller, with both global and static linkage. Every source was ordinary
C and compiled under `/AS /Zi`; all objects passed strict OMF parsing.

| Compiler | Far callee declared externally | Far callee defined in same TU |
|---|---|---|
| MSC4.00 | `9a offset16 segment16`, 5 bytes | Same 5-byte FAR16 form in all four cases |
| MSC5.00 | `9a offset16 segment16`, 5 bytes | `0e e8 relative16`, 4 bytes in all four cases |

The corresponding sample caller has an independently emitted 25-byte CV3 extent
for the external case and a 24-byte extent for the MSC5.00 same-TU case. The
four-byte sequence is already present in unlinked LEDATA. Its OMF fixup is an
ordinary self-relative OFFSET16 referring to the callee, so the existing
restricted linker can resolve it without any new optimization or byte surgery.
The differing call length is reflected naturally in compiler branch layout.

The earlier same-TU experiment that still emitted a five-byte far call used
MSC4.00. It was a valid negative result for that compiler/configuration, but
could not rule out MSC5.00's default code generator. Optimization settings also
matter: `/Os` changes these full functions substantially and does not reproduce
the original checked bodies. Bare default `/AS /Zi` does.

## Actual Microsoft LINK behavior

Both authentic linkers were tested using fresh objects and clean output names:

| Tool | Provenance | SHA-256 |
|---|---|---|
| LINK3.61 | PCjs MSC5.00 UTILITY1 disk | `1d80eab0f7828e4fa42b387892fa40d38d656b96ee4d6aed6b2100fb8ae3d31a` |
| LINK3.65 | Pinned official MS-DOS tools repository, `config/msc510.json` | `124a3c800edc16b60f696d35a9dfec798b68b78fe2ca90c5988ea76bdeab1a8a` |

The archived disk is
`https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK3-UTILITY1.json`,
SHA-256 `bc4090208c04c6ac12f0ebb1bdcb4a76726d99db802a4ff80c82b486c8fccd52`.
The tool banners identify versions 3.61 and 3.65 respectively; compiler version
numbers must not be confused with these linker versions.

The decisive probe links an actual MSC5.00 external far-call object containing
a single FAR16 FIXUPP with a controlled same-segment far callee. These are
calling-convention diagnostics, not reconstructed game functions or completion
credit. `/NOD` suppresses unrelated default libraries. Options tested were
none, `/FARCALLTRANSLATION`, `/NOFARCALLTRANSLATION`, and translation combined
with `/PACKCODE` or `/NOPACKCODE`.

Both linkers produce the same outcomes:

- Default and `/NOFARCALLTRANSLATION`: retain `9a offset16 segment16`.
- `/FARCALLTRANSLATION`: emit **`90 0e e8 relative16`**, preserving five bytes.
- `/PACKCODE` and `/NOPACKCODE`: do not change that five-byte result.

The complete linked probe image remains 36 bytes in every case. Thus authentic
LINK translation does not account for the original four-byte sequence. A
preliminary NASM OMF probe used separate OFFSET16/BASE16 fixups and was not
translated even with the option; that narrower negative result should not be
mistaken for the authentic compiler FAR16 case.

The retained independent records are
[far-call-compiler-linker-probes.json](../evidence/far-call-compiler-linker-probes.json).
The complete probe sources, fresh objects, response files, logs, maps and
executables remain under `build/far-call-probe/` and `build/far-call-link/`;
reproduction scripts are `build/far-call-probe.py` and
`build/far-link-compiler-probe.py`.

## Complete reconstructed move module

Combining the actual helper with the four already matching board mutators and
the apply routine in original order yields these compiler-established offsets:

| Function | Object offset | Image offset | CV3 bytes |
|---|---:|---:|---:|
| `castle_95df` | 0 | `95df` | 61 |
| `swap_cells` | 61 | `961c` | 96 |
| `remove_piece` | 157 | `967c` | 51 |
| `add_piece` | 208 | `96af` | 74 |
| `change_piece` | 282 | `96f9` | 80 |
| `apply_9749` | 362 | `9749` | 246 |

The complete emitted code segment is 608 bytes, exactly the sum of those
independent procedure lengths, and matches the whole original interval
`[0x95df,0x983f)`. No inter-function gaps or omitted bytes are hidden by per-function
comparisons. The next original byte at `0x983f` is `90`; it is **not** emitted by
this segment and earns no padding credit. This establishes one matching
translation-unit grouping and code-generation configuration, not proof of the
historical source-file boundaries or the original linker's segment placements.

After using the real same-TU helper, the remaining apply differences were only
five local BP offsets. Harmless local identifier choices reproduce the required
stack allocation; declaration order by itself did not fix it. The final K&R
locals `u`, `t`, `s`, `q` have explanatory comments for rook source, rook
destination, unused original-frame slot and en-passant capture square. The
compiler allocates the eight-byte frame and emits all references itself. The
unused local is ordinary C; no padding bytes or assembler constructs are used.

The canonical source was recompiled from scratch after comments were added.
The whole-segment and all six per-procedure exact results are in the retained
fresh evidence. A migration proposal for the four existing cell units plus the
two new functions is `build/move-module-units.json`. No shared OMF parser or
restricted-linker changes are needed, and none were made for this solution.
