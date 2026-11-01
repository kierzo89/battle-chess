# Unpacked analysis inventory: useful baseline, unresolved denominator

REA/Ghidra reports **390 candidate procedures** in the canonical unpacked
analysis MZ. This provides a better baseline than disassembling the packed
disk image, but it is **not an exhaustive function count**. Three reported
targets are demonstrable 16-bit segment-context errors in zero-filled memory;
another starts in zero padding and causes a real direct-call entry to be
missed. Some automatic bodies also merge separate runtime modules or attach
shared return instructions to unrelated routines.

The whole-file goal still compares all **83,415 packed bytes**. The verified
packing experiment establishes a **401,131-byte prepacking image** and 173
relocation sites as a genuine source/link build's intermediate target.
Neither recovered bytes nor this function inventory add completion credit.

## Artifact identity and provenance

| Artifact | SHA-256 | Role |
|---|---|---|
| Original `CHESS.EXE` | `c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd` | Shipped packed comparison target |
| `build/exepack/TRIM5_UNPACK.EXE` | `faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02` | Derived analysis carrier, synthesized header plus recovered image |

The second artifact comes from
`unpack_exepack(original).analysis_mz(trim_padding=5)` in
[exepack.py](../exepack.py). Its 1,024-byte header is a synthesized working MZ
header, not a recovered original linker header. Its 401,131 image bytes and
173 relocation sites are recovered original contents. The
[provenance record](../evidence/rea_unpacked_provenance.json) pins the decoder
and both identities; [EXEPACK layout](exepack-layout.md) explains the exact
analysis round-trip through official EXEPACK 4.06.

All `rea_unpacked_*.json` analysis records refer to the **derived** hash.
REA's generic `authority: shipped-artifact` label describes its local-binary
analysis route; it does not make this synthesized carrier an original shipped
executable. It must not replace the original target hash in matching checks.

Ghidra imports at load segment `0x1000` and applies the carrier's relocation
table. Its linear address is `image_offset + 0x10000`; the derived file offset
is `image_offset + 0x400`. Original packed file offset `image_offset + 0x200`
is valid only within the unchanged leading image prefix `[0,0x110dc)`.
Beyond that prefix, use expanded-image coordinates and decoder provenance.
Loader-relocated words differ from the unrelocated image bytes at the 173
sites by design.

## Retained inventory and reconciliation

The fresh REA overview is
[rea_unpacked_overview.json](../evidence/rea_unpacked_overview.json), Evidence
`ev_4a26f4d112bb361f83286e6d2171f7a410353fdc9d05b237f630ae280fa5690b`.
The complete automatic procedure list is
[rea_unpacked_procedures.json](../evidence/rea_unpacked_procedures.json), Evidence
`ev_db5eb98373ac623255fa435bf78be012b8ead420e7203bf1964f73066ff55359`.
Ghidra 12.1.4 completed its default auto-analysis before these reads.

| Inventory | Candidate entries | Shared with unpacked list | Only in that older list |
|---|---:|---:|---:|
| Derived unpacked Ghidra | 390 | 390 | — |
| Original packed Ghidra | 386 | 362 | 24 |
| Legacy r2 | 371 | 349 | 22 |

There are 28 unpacked-only entries versus packed Ghidra and 41 versus r2.
The unpacked/r2 union contains 412 locations, not 412 proven functions.
Membership and classifications are in
[unpacked-functions.csv](../build/unpacked-functions.csv), one row per each
of the 390 automatic candidates. The separate
[extra-entry table](../build/unpacked-extra-entries.csv) records a real direct
far-call entry missed by the function manager. Exact set differences and
original/derived identities are retained in
[unpacked-inventory-summary.json](../build/unpacked-inventory-summary.json).

The packed entry `0x14142` is the EXEPACK stub and disappears from original
program inventory. The original startup `0xea86` and application entry
`0x10` become reachable through their real relocation/entry context. Many
older low-offset candidates disappear or move to the corresponding far
module context; equal entry offsets alone do not validate equal extents.

## Main and far module contexts

The imported names retain segment contexts. Subtracting load segment `0x1000`
gives these candidate module bases:

| Unrelocated image base | Loaded CS context | Automatic entries | Evidence/interpretation |
|---|---|---:|---|
| `0x00000` | `1000` | 347 including startup | Main small-model code and runtime candidates |
| `0x0fbf0` | `1fbf` | 4 | Additional far module context |
| `0x0fdf0` | `1fdf` | 11 | Far-frame routines; near branches cross the linear `0x20000` boundary |
| `0x10d30` | `20d3` | 4 | BIOS/serial routines; first inspected body is 35 bytes and ends `RETF` |
| `0x10e30` | `20e3` | 9 | Further far routines; first inspected body is 130 bytes and ends `RETF` |
| `0x110d0` | `210d` | 5 | Four 3-byte jump stubs plus an unvalidated zero-padding target |
| `0x11ef0` | `21ef` | 7 | Input/device far routines, plus an additional missed direct entry at the base |
| `0x1f090` | `2f09` | 3 | Spurious zero-region targets from wrong near-branch contexts |

These are observed contexts and entry counts, not recovered source-file or
linker segment declarations. The original can mix near C calls, far calls,
handwritten assembly, library routines, and runtime-modified code.

Useful retained bounds/call examples include:

- Application `0x10`: automatic body `[0x10,0x24f)`, 575 bytes;
  [main outgoing references](../evidence/rea_unpacked_extra_0.json) include
  stack checking, graphics/setup calls, and far input calls.
- Far routine `0xfdf2`: 26-byte body ending `RETF`,
  [instruction evidence](../evidence/rea_unpacked_extra_3.json).
- Far routines `0x10d30` and `0x10e30`: 35 and 130 bytes ending `RETF`,
  [serial instructions](../evidence/rea_unpacked_extra_1.json) and
  [further far instructions](../evidence/rea_unpacked_extra_2.json).
- Input routine `0x11f3e`: contiguous 107-byte body ending `RETF`,
  [instructions](../evidence/rea_unpacked_detail_5.json); original application
  instruction at `0x1ef` is `CALLF`, with loaded bytes `9a 4e 00 ef 21`,
  [exact instruction](../evidence/rea_unpacked_final_0.json).
- Search `0x8fca`: the new view independently reports the expected contiguous
  64-byte body `[0x8fca,0x900a)`,
  [bound evidence](../evidence/rea_unpacked_bounds_2.json).

## Concrete automatic-analysis failures

### Wrong 16-bit near-branch context

At image `0x10c20`, the actual bytes `e8 cf f1` encode a near call. Under
the containing far module's original CS base `0xfdf0`, its signed displacement
lands at **image `0xfdf2`**, where the 26-byte far routine exists. Ghidra instead
uses a generic `2000` alias for the source instruction, wraps the 16-bit IP,
and reports linear `0x2fdf2`, or **image `0x1fdf2`**, 64 KiB too high.
[Exact instruction evidence](../evidence/rea_unpacked_bad_near_call.json),
`ev_ffc22fdc365b566541020b6cdbc3097bf565a8b70770601d3ad65ac4dd53a185`,
preserves both the actual bytes and the incorrect reported destination.

The same problem creates these three candidate entries:

| Source image | Bytes | Correct image target | Reported image target |
|---|---|---|---|
| `0x10c20` | `e8 cf f1` | `0x0fdf2` | `0x1fdf2` |
| `0x10961` | `e8 e6 f4` | `0x0fe4a` | `0x1fe4a` |
| `0x1001e` | `e9 66 ff` | `0x0ff87` | `0x1ff87` |

All reported targets lie in a verified zero-fill span. Ghidra lists a
34-byte body at each, decoded as repeated `ADD [BX+SI],AL`, without a genuine
return. The last source opcode is a **JMP**, although the provider labels its
reference `CALL_TERMINATOR`; this is another reason to inspect raw instruction
bytes before relying on call classifications. Incoming references and exact
instructions are retained in `rea_unpacked_detail_3.json`,
`rea_unpacked_alias_0.json`, `rea_unpacked_alias_1.json`, and
`rea_unpacked_final_3.json`/`final_4.json`.

### A zero target swallows a real entry

The jump stubs at image `0x110d0`, `0x110d3`, `0x110d6`, and `0x110d9`
really point to `0x11eed`. The image contains three zero bytes there before
the next module starts at `0x11ef0`. Ghidra begins decoding in those zeros,
then consumes the first byte of the actual next instruction into a fictitious
cross-boundary instruction. Its function manager consequently omits entry
`0x11ef0` and gives the zero-started body a noncontiguous 32-byte extent.
[Zero-byte evidence](../evidence/rea_unpacked_extra_5.json) and
[misdecoded body](../evidence/rea_unpacked_final_2.json) retain this behavior.

The application's actual instruction at image `0x245` is a direct far call
to **`11ef:0000` before relocation**, or loaded `21ef:0000`:
[exact call evidence](../evidence/rea_unpacked_final_1.json),
`ev_b5d6ed8a59278e5191c7941429e5495e3108ec40715ce9f8bdf54e806e088fcd`.
The independently decoded real routine begins with `a0 52 49` and reaches a
`RETF` at `0x11f0d`. The four stubs' zero target may be reserved or modified
at runtime; this static investigation does not establish the intended later
contents or claim that the zero-filled region can never execute.

### Runtime boundaries merge

The derived startup entry `0xea86` receives an automatic 375-byte,
noncontiguous body spanning parts of CRT0 and CRT0DAT. The archived 5.00 CRT0
comparison independently establishes a 179-byte module contribution.
The stack checker `0xecaa`, known as 22 bytes, acquires an extra shared `RET`
at image `0xeb3a`, making its automatic body 23 bytes with a 390-byte span.
[Startup references](../evidence/rea_unpacked_detail_0.json) and
[stack-checker body](../evidence/rea_unpacked_bounds_3.json) preserve this.
Summing Ghidra function spans would therefore overstate code coverage.

## Code/data gaps and the remaining denominator work

The expanded reference establishes zero initialization in these ranges:
`[0x110dc,0x11ef0)`, `[0x120c2,0x5cc28)`, and
`[0x5fae1,0x610ed)`. These are byte facts, not a blanket declaration that
all such addresses are forever non-code. In particular the first contains
the unresolved jump-stub target described above. Regions containing other
unclassified bytes likewise must not be discarded as data merely because
the function manager did not discover a procedure there.

The original startup loads the relocated segment `0x6cc2` into DI, before
using it for the program's stack/data context:
[instruction evidence](../evidence/rea_unpacked_bounds_0.json).
Its unrelocated counterpart is `0x5cc2`, placing DGROUP's beginning at
image `0x5cc20`. A direct
[64-byte read](../evidence/rea_unpacked_bounds_1.json) there observes initial
zero words and the `MS Run-Time Library` copyright string. Individual
global references and strings support data classifications; the whole
remaining tail has not been exhaustively classified byte by byte.

Ghidra labels nearly the entire initialized load image `CODE_0` through
`CODE_11`, including huge zero spans and this data context. Those labels do
not prove executable-code content. Its extra `DATA` block begins at image
`0x61eeb` and extends beyond the file-backed image; it represents loader
uninitialized memory and adds no bytes to the executable comparison target.

Before publishing a source/function completion percentage, the inventory
needs corrected per-module CS contexts, audited incoming direct and indirect
edges, compiler/assembly extents for shared tails, runtime evidence for the
jump-stub area, and a classified map of initialized code/data/padding. The
390 candidates and the 412-location union support that audit; neither is a
valid denominator yet.
