# Full source linker layout constraints

The 401,131-byte tested prepack image is mostly zero: 327,011 bytes (81.5%). This does not imply 401 KB of missing instructions. The 83,415-byte shipped executable retains a 69,852-byte prefix, then encodes the remaining expanded image with 249 EXEPACK packets. Zero-fill packets describe 319,466 output bytes; literal packets carry only 11,488 bytes. Other fills contribute 330 bytes. These are packing observations, not source completion credit. The exact counts, bounds, hashes, relocation target distribution and arithmetic are retained in [image-layout-constraints.json](../evidence/image-layout-constraints.json).

## Observed byte partition

All ranges are half-open image offsets before DOS relocation. A range label describes evidence inside it, not an assertion that every byte has the same original OMF class.

| Range | Bytes | Zero bytes | Meaning established so far |
| --- | ---: | ---: | --- |
| `00000–110dc` | 69,852 | 4,165 | Unchanged packed prefix: game code, runtime code, far modules and unclassified bytes |
| `110dc–11ef0` | 3,604 | 3,604 | Zero gap, including the unresolved target `11eed` of four jump stubs |
| `11ef0–120c2` | 466 | 39 | Input/device far code and remaining bytes requiring individual boundaries |
| `120c2–5cc20` | 306,014 | 306,014 | Large zero range containing several demonstrably referenced far/huge data bases |
| `5cc20–61eeb` | 21,195 | 13,189 | File-backed DGROUP range with independently located initialized runtime data, application data and zero runs |
| `61eeb–61ef0` | 5 | 5 | Paragraph padding omitted by the successful prepack experiment |

The 306,014-byte range alone is 76.3% of the prepack image. The maximal zero run actually continues to `5cc28`, eight bytes into DGROUP. Other large zero runs are `5d1ff–5d9c6` (1,991), `5d9c7–5dae6` (287), `5fae1–610ed` (5,644), `61463–6152c` (201), and `616bf–61741` (130). Their contents are proved; declarations, owners and initialization mechanisms are not.

## Far data allocations inside the large zero range

The 173 recovered MZ relocation words contain twelve distinct unrelocated paragraph values. The data-bearing bases `120d`, `1f09`, `270c`, `3823`, and `5cc2` have 12, 7, 2, 4, and 13 relocation sites respectively. A segment value alone does not prove an allocation; the following instruction uses establish data-pointer roles.

Fresh REA observations are retained in [the layout query bundle](../evidence/rea-image-layout-bundle.json), bound to analysis carrier SHA-256 `faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02`. Ghidra loads it at paragraph `1000`; displayed segment immediates therefore include `1000`, and displayed linear addresses include `10000`. The table below removes that known loader adjustment.

| Base | Distance to next base | Independent instruction constraint |
| --- | ---: | --- |
| `120d:0000` (`120d0`) | 53,184 to `1f090` | Function `28ae` builds a pointer at base zero and advances its offset by `0cb8` four times; it also initializes a second pointer to `120d:cc6c`. REA `ev_4643f1f10881530a74efbdef7a63257fb0c2e8e19f317edeee7b086bb57fbc17`. |
| `1f09:0000` (`1f090`) | 32,816 to `270c0` | Function `2741` reads bytes through this pointer, incrementing the segment by `1000` when its 16-bit offset wraps. This is huge-pointer traversal, not evidence of a function at the base. REA `ev_5e85a83f2ca27d5945a221681594615dc62520ba77d661df948ac6a161f8508e`. |
| `270c:0000` (`270c0`) | **70,000** to `38230` | Function `2525` checks a 32-bit accumulated size against `0001:1170` = 70,000 before constructing the destination pointer from this base. REA `ev_ded85acda5f623270e6e291850d8e5a58ff6b2710bfac673d420131cfa3f74b6`. |
| `3823:0000` (`38230`) | **150,000** to `5cc20` | Function `28ae` initializes the working pointer to this base; function `3713` subtracts its huge-pointer distance from the capacity at DGROUP `b0b4:b0b6`. Main initializes that capacity to `0002:49f0` = 150,000. |

The main initialization is independently read from the shipped original, unchanged prefix: image `13d` contains `c7 06 b4 b0 f0 49 c7 06 b6 b0 02 00`. See [raw main evidence](../evidence/rea-image-layout-main.json), `ev_4aba816b878362d4b997874e0841da7d25549b3705a8a7d4a7c66ed357c471e9`. The capacity calculation at `3713` is REA `ev_e6b5e5a98df42006f4b83bca2a0bb8bc070153e404e5db019b85cfe44e0db7f2`.

Thus two buffer capacities independently equal the adjacent placement distances exactly. A useful candidate linker order is far code ending before `120d0`, data based at `120d0`, data based at `1f090`, a 70,000-byte buffer at `270c0`, a 150,000-byte buffer at `38230`, then DGROUP at `5cc20`. The first two distances remain placement constraints rather than proved array sizes. Even the two stronger capacities do not reveal historical SEGDEF names, whether huge arrays were split across OMF segments, or whether zero bytes resulted from LEDATA, LIDATA, uninitialized segments before later initialized data, or linker gap materialization. Those choices require independently compiled objects and an authentic linker experiment.

## DGROUP, BSS and stack constraints

The independently archived CRT0 supplies actual segment/group and external-symbol evidence, beyond the decoded image. Its complete linked startup loads DGROUP `5cc2`, references `_edata` at offset `52cc`, and `_end` at offset `cbe0`; the separate CHKSTK data word initializes `_end+100` = `cce0`. See [runtime placements](../evidence/runtime500-placements.json) and [startup raw bytes](../evidence/rea_crt_startup_500.json).

These impose the following arithmetic:

- DGROUP image base: `5cc20`.
- `_edata`: `5cc20 + 52cc = 61eec`.
- `_end`: `5cc20 + cbe0 = 69800`.
- CRT0's `REP STOSB` clears `_end - _edata = 7914` hex = 30,996 bytes, from `61eec` through `697ff`.
- EXEPACK saved stack `6980:1000` has initial top `6a800`; its SS base `69800` equals `_end` exactly. Startup changes SS to DGROUP and adds `cbde` to SP, then aligns SP even. This preserves the stack top apart from its deliberate two-byte reserve.
- The inferred minimum allocation `0892` paragraphs past the paragraph image end `61ef0` reaches `6a810`, one paragraph beyond that saved stack top.

The tested prepack image ends at `61eeb`, one byte before `_edata`; the recovered paragraph image ends at `61ef0`, four bytes after `_edata`. Keep these quantities distinct. `_edata` is an even linker boundary, not proof of a byte present in the input file. The trimmed input and paragraph-zero tail together permit startup's clear boundary without inventing a source initializer. Likewise, the synthesized analysis carrier's loader-created uninitialized block starts at its file end; that label does not determine the original BSS start.

Nine whole archived initialized runtime DATA/MSG segments already constrain 170 bytes and specific positions in DGROUP. They include actual literal zero initializers, CHKSTK's fixup, the day/month tables and timezone names. Their independent boundaries are in [runtime-library-expansion.md](runtime-library-expansion.md). CRT0 `_DATA` has an 88-byte declared extent with incomplete LEDATA initialization, so it constrains allocation without establishing 88 independently initialized bytes. Existing data candidates must retain this distinction.

## Concrete next linker experiments

1. Recover the application-owned data objects behind bases `120d` and `1f09`, including the huge-pointer buffer initialized by external data input. Treat their adjacent-base distances as upper layout constraints until declarations or original file-format consumers prove sizes.
2. Compile independently authored 70,000- and 150,000-byte far/huge buffer declarations with the pinned compiler. Inspect the resulting SEGDEF, LIDATA/LEDATA and grouping records, then link with authentic LINK and later initialized DGROUP data. Compare allocation order, paragraph alignment and materialized zero lengths without giving those experiments target-byte coverage credit.
3. Reconstruct initialized DGROUP tables from their meanings and independent consumers; preserve the independently archived runtime member ordering and placements. Derive the BSS contribution from complete source object extents and linker `_edata`/`_end`, rather than appending a target-sized zero block.
4. Produce a whole-program map whose source objects explain the observed far bases, DGROUP `5cc20`, `_edata=52cc`, `_end=cbe0`, saved stack and all 173 relocation words. Only then use the established EXEPACK configuration to test the final file identity.

This document adds allocation constraints and an explicit byte partition. It does not supply a reference-derived executable skeleton, add zero-span matching credit, or establish the full-program segment order by itself.

## Completed independent C5 allocation experiment

The experiment above now has a reproducible implementation: [layout-allocation-probe.py](../evidence/layout-allocation-probe.py) compiles the new [probe sources](../src/probes/layout/huge_zero_allocation.c), records every object record/checksum and declared segment, and invokes pinned LINK 3.65 in fresh DOSBox drives. Run `python3 matching/evidence/layout-allocation-probe.py` from the repository. The runner never reads CHESS, an expanded image or target bytes; LINK receives only a fresh `UNIT.OBJ`, batch file and the independently hash-verified LINK executable. Results, full maps, source/object/tool hashes, compiler flags and mount inventory are in [layout-allocation-experiment.json](../evidence/layout-allocation-experiment.json). No generated allocation receives canonical matching credit.

MSC5.00 `/AS` accepts ordinary declarations:

```c
unsigned char huge buffer_70000[70000L];
unsigned char huge buffer_150000[150000L];
```

The corresponding `far` declarations fail with C2125, allocation exceeds 64K. Both uninitialized `huge` declarations compile to COMDEF records (`0xb0`) with the independently requested element counts and element size one. They do **not** produce two oversized SEGDEF records in the compiler object. LINK supplies `HUGE_BSS` segments and splits them at 65,536 bytes. With these names in this one translation unit, LINK orders the 150,000-byte communal before the 70,000-byte communal, reversing declaration order. That ordering is observed in the public map; its underlying selection rule is not established by this experiment.

Adding explicit `{0}` initializers gives a second, viable form:

```c
unsigned char huge buffer_70000[70000L] = { 0 };
unsigned char huge buffer_150000[150000L] = { 0 };
```

MSC5.00 emits five paragraph-aligned `FAR_DATA` SEGDEFs: 65,536 + 4,464 for the first array, then 65,536 + 65,536 + 18,928 for the second. Each whole-array extent is independently 70,000 or 150,000 bytes. Compiler-emitted LIDATA records (`0xa2`) encode zero repetitions, with a small LEDATA initializer at the first byte. Segment attributes `6a` use the OMF big-segment bit for the full 64-KB pieces; attributes `68` describe the remainders. LINK preserves this source order. No target-sized byte blob or manually emitted OMF record is involved.

Two tiny initialized near globals follow: marker `5a`, and a zero `__acrtused` support symbol, supplied in ordinary C to avoid a CRT library dependency. Initial runs omitted the support definition and LINK reported L2029 even though it left an output file. Those failed trials remain in [layout-allocation-initial-link-errors.json](../evidence/layout-allocation-initial-link-errors.json); they are not successful executable evidence. The final runner rejects LINK errors rather than trusting file existence. These allocation-only executables deliberately have no stack or application entry; LINK's sole remaining warning is L4021, no stack segment. They are inspected as allocation artifacts and are not executed.

| Compiler form | LINK ordering | Complete image bytes | DGROUP base | Meaning |
| --- | --- | ---: | --- | --- |
| Uninitialized huge | Default | 2 | `0000` | Marker/support only file-backed; huge buffers contribute additional allocation |
| Uninitialized huge | `/DOSSEG` | 220,018 | `35b7` | Huge BSS is placed before initialized DGROUP; LINK materializes the intervening zeros |
| Explicit `{0}` huge | Default | 220,016 | `0000` | Initialized FAR_DATA remains file-backed after DGROUP |
| Explicit `{0}` huge | `/DOSSEG` | 220,018 | `35b7` | Arrays precede DGROUP in source order, matching the observed 70,000-then-150,000 adjacency pattern |

For both `/DOSSEG` cases, LINK reserves the initial 16-byte CODE prefix, places the 220,000 array bytes in `[10,35b70)`, and places marker/support at `[35b70,35b72)`. The only nonzero byte anywhere in the complete image is marker `5a` at `35b70`. There are zero MZ relocations because these minimal declarations do not contain initialized pointers or generated pointer-access code. The explicit-zero case's public bases are `0001:0000` and `1118:0000`; its five `FAR_DATA` pieces meet exactly without extra inter-array padding, since 70,000 and 150,000 are paragraph multiples.

This establishes an authentic compiler/linker mechanism for a large zero-filled file region before later initialized DGROUP. It also shows why file bytes alone cannot distinguish an explicit zero initializer from a huge uninitialized allocation materialized by linker ordering. The successful initialized form is a reproducible allocation candidate; it does not prove that the original source used `{0}` or `/DOSSEG`. Neither experiment inserts the target's earlier unknown allocations or forces DGROUP to `5cc2`. Determining that full placement still requires independently reconstructed objects and ordering for those earlier regions.

## First two data ranges: consumer-derived constraints

A second audit of the regions based at `120d0` and `1f090` now gives smaller, independently justified allocations inside the adjacent-base distances. It does **not** establish that 53,184 and 32,816 are original array `sizeof` values. Full fresh function observations, raw data tables and negative queries are retained in [rea-first-allocations-bundle.json](../evidence/rea-first-allocations-bundle.json); [first-allocations-constraints.json](../evidence/first-allocations-constraints.json) records the derived ranges and exact evidence IDs.

For the first region, use offsets relative to `120d:0000`:

| Relative range | Independent constraint | Source candidate and remaining uncertainty |
| --- | --- | --- |
| `0000–32e0` | `28ae` assigns four buffer pointers, incrementing by `0cb8` = 3,256 each | `unsigned char slots[4][3256]` expresses the observed stride. It does not prove that each slot contains an eight-byte header plus 3,248 pixels; the eight-byte descriptors initialized by this routine live separately in DGROUP. |
| `32e0–3f90` | Assembly routine `e8cb` writes translated pixels at `120d:32e0`; the next scratch base is exactly 3,248 bytes later | A 3,248-byte translation scratch array is a candidate, with size supported by the corresponding checked redraw bound. The translation routine itself uses caller width/height and does not check its destination capacity. |
| `3f90–4c40` | `41a8` checks `row_bytes * rows <= 0cb0` = 3,248, then copies or clears at `120d:3f90` | A 3,248-byte redraw scratch buffer is strongly supported by this operation. Pixel routine `5a7c` uses `JLE 0cb0` for an index, permitting index 3,248 itself; preserve that observed one-byte boundary behavior instead of silently converting it into a stronger safe allocation proof. |
| `4c40–c940` | DGROUP `05ce` initializes `120d:4c40`; `2b81` requests 32,000 decoded bytes, processes 31,840 bytes offset by 160, and `3e4f` displays 160 by 200 byte units | A 200-row by 160-byte background image, or equivalent byte array of at least 32,000, follows independently from operation dimensions. Its original declared capacity could be larger. |
| `c940–cc6c` | Next observed pointer starts at `cc6c` | **812 bytes remain unclassified.** They are not assigned to the background declaration or padding. |
| `cc6c–ce10` | `28ae` assigns four pointers, advancing by `12 + 4*N`; initialized DGROUP bytes `05d2..05d5` are 16, 19, 32, 26 | Planned record extents are 76, 88, 140 and 116 bytes, totaling 420. This proves the initialization arithmetic and pointers, but does not by itself recover record field types or prove every byte is accessed. |
| `ce10–cfc0` | Difference to next observed paragraph base | **432 bytes remain unclassified.** |

The background pointer raw read is REA `ev_3efb4f1ef59946e905eac9c0195801de705c17ad0fa4abac3a3db2c530a101c4`; it includes `40 4c 0d 22`, with the analysis carrier's known `1000` paragraph relocation added. The four record counts are separately read in `ev_f95702bb79d46fd5acbd75208a43a81908097919937375d23caedfcb438fa1eb`. The full background operation is `ev_3d1e5915ef8ac9bb81226f6f0959486c063ebb9e8f5e886d3d61bcb909603d9d`; its display dimensions are `ev_0a6a53be0d0309fda6cd9658dbcb5c1425067efa5ed76c8383cc11864a984101`.

A fresh compiler experiment confirms that an ordinary C partial workspace containing just the four 3,256-byte slots, two 3,248-byte scratch arrays, and 32,000 background bytes has a complete FAR_DATA SEGDEF of `c940` = 51,520 bytes. See [partial_graphics_workspace.c](../src/probes/layout/partial_graphics_workspace.c) and [fresh build provenance](../evidence/partial-graphics-workspace-build.json). Its natural field offsets are exactly `0`, `32e0`, `3f90`, `4c40`. The object is an allocation probe; it does not assert the original aggregate type and receives no matching credit. In particular, it deliberately contains neither an 812-byte filler nor a 432-byte tail. The confirmed four variable record reservations add another 420 meaningful bytes, leaving 1,244 bytes unresolved across the two gaps.

The second region at `1f09:0000` is reused for resources rather than identified as executable code. Main and `6cb4` each request 32,000 decoded bytes into it. Routine `2741` consumes coordinate bytes followed by zero-terminated strings; `6cb4` consumes sentinel-delimited encoded text, using bytewise huge-pointer arithmetic. This supports byte storage, but traversal syntax alone does not imply a declared size above 64 KB: the pinned compiler also uses that arithmetic for huge pointers into smaller buffers.

There is an independent raw-file consumer as well. `82a5` passes `1f09:0000` to `cb8f`, whose loop copies input bytes in chunks no larger than 512. The count comes from `2bca[2]`, the 32-bit word at DGROUP `2bd2`: the retained table read contains `00 7d 00 00` = 32,000. These observations are REA `ev_d05f16b26a5bde766b0542d237132a4ad61f87a9cb999f3185fab93392e1c82c`, `ev_2ea200a2a724f752bde0d1721b2f21085db09879e93e27d188a7b6a2249f2f93`, and `ev_b4f3aca183c8038afc63ff93da83945a75095c691762726bbf30823e251f21de`. The asset opener names `allcanm1` and `allcanm2`, independently read in `ev_5b1a8c806ea6abed9df56beabd24be143207d8133cef9f888374362d817f066f`.

A 32,000-byte buffer is therefore an independently justified minimum candidate for this region. The additional **816 bytes** before base `270c0` are unresolved, not proved padding. Neither an attractive 32,768-byte declaration nor a 32,812-byte declaration is established by these consumers. Similarly, the first region's `cc6c - 4c40 = 32,812` is only an address difference across a known 32,000-byte operation plus an unknown 812-byte area. It must not become a source array length solely because it fills the layout.

The next useful source/link test is to compile these proved partial workspace fields and a separate minimum resource buffer, inspect their names/classes/alignment and ordering, then recover consumers of the unexplained areas before attempting the full link. Resource decoding can establish actual maximum payloads and formats; declarations larger than those payloads still require additional allocation evidence. The remaining unknowns cannot be repaired by a reference-derived zero array.

The previously unresolved CRT0 `_DATA` initializer holes now have a separate [record ownership and authentic LINK study](runtime-crt0-data.md): twelve initializer bytes plus seventy-six linker-materialized reserved bytes inside an 88-byte DATA contribution. This adds allocation evidence without canonical matching credit.

## Fresh authored object readiness audit

`evidence/source-contribution-inventory.py` validates current source/registry/OMF
hashes against fresh checker artifacts before inspecting every canonical C
object. The current58 objects contain all113 credited functions and no extra
uncredited CV procedures. Three fragment containers imply incompatible object
placements: empty_callbacks_msc400_match.c, frames_match.c and ui_helpers_match.c.
They require independently placed source contributions before a complete link.
The evaluator is now a complete independently checked3,902-byte natural
contribution; the audit itself grants no complete-contribution/alignment credit.
Full external definitions, layout and source-link manifest remain unresolved.

The subsequent audit removes those three inconsistent source containers and
now records58 C objects/all115 procedures with coherent implied bases.
The actual LINK control in public-text-alignment-link-control.md confirms
WORD2 padding;25 remaining odd-based fragments need real enclosing source.
See source-contribution-layout.md for the complete5,350B search and1,016B
board/move contributions and the distinction between function equality and
complete link readiness.

The evaluator table is now backed by a genuine2,880-byte near COMDEF control,
not initialized zeros. Original CRT0 clears DGROUP52CC..CBE0; the typed grid
B0DC..BC1C lies inside that uninitialized range. The source definition and
required final map are retained in config/uninitialized-definitions.json.
Authentic C5/LINK/SLIBC harnesses verify allocation, zero clearing and both
stack sizes. The original saved SP1000 agrees with the /STACK:4096 control;
unique historical invocation and allocation order remain unproven. No BSS
file-byte credit or initialized-DATA backend relaxation is introduced.

## Current allocation and layout evidence

The current source audit covers53objects/all120procedures: zero inconsistent
bases or extra procedures,22 with full CODE/MZ/alignment equality,19 requiring
enclosing context for WORD alignment, and23 unequal complete CODE spans
(overlapping categories). Canonical graphics1,136B and history/input340B are
now integrated complete contributions; older proposal-only counts above are
historical. Full source-link ownership remains unresolved.

Authentic C5 /AS compilation of uninitialized huge arrays and LINK3.65 controls
materialize all220,000 zero bytes in file-backed FAR_DATA without initializers.
Public COMMON controls sort150,000 before70,000 regardless of object order,
which does not reproduce the original order. Separate-source static huge arrays
instead follow input object order and reproduce the relative70,000/150,000
sequence. Their FAR_DATA segments have PUBLIC combine; C static describes
internal symbol linkage, not OMF PRIVATE combine. Neither historical filenames,
actual game consumer ownership nor original absolute anchors are recovered.
See config/far-storage-requirements.json and
 evidence/private-capacity-allocation-findings.md. These controls earn zero
matching credit; no invented allocation or zero filler enters the game build.

The archived CRT0 contains COMMENT009E (DOSSEG). Removing only that record
causes unresolved _end/_edata in an explicit-CRT0 control; explicit /DOSSEG
restores success and the identical complete image. Therefore a DOSSEG-compatible
ordering is supported, while an explicit historical /DOSSEG command option is
not uniquely implied. See evidence/far-capacity-allocation-findings.md and its
complete causal experiment. Archived runtime and original game bytes remain
unchanged.

The134-function source audit now covers56 objects, with23 satisfying complete
CODE/MZ/alignment context,21 requiring enclosing context for alignment and23
unequal whole CODE spans (overlap allowed). The canonical5,356-byte graphics/menu
source resolves earlier menu/frame tail and alignment conflicts. Actual70k-bank
C consumers are now matched at2525/3652; see the allocation contract and
 evidence/far-storage-consumer-ownership.json. Original buffer-definition
linkage/source ownership remains unresolved even though its consumers match.
