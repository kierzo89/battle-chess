# Microsoft C 5.00 comparison: a distinguishing exact C match

**Microsoft C 5.00 with `/AS /Gs /Os /Zi` compiles the existing
`src/search_state_match.c` into the exact original 64 bytes at image `0x8fca`.**
The independently validated OMF CodeView procedure length is 64, and the
restricted linker resolves every external call and data address before a
full-byte comparison. No bytes, padding, or relocation fields are removed,
masked, or copied from the target. Microsoft C 5.10 with the same flags
produces 65 bytes and fails that comparison.

The target's startup CRT also matches the **5.00-era** library implementation
rather than the archived stock 5.10 implementation. Together these findings
make Microsoft C 5.00 a materially stronger reconstruction candidate than the
earlier general C 5.x identification. They do not prove that every module was
built with one release or one option string; compatible later tools and mixed
libraries remain possible.

The C5.00 backend is now separately pinned in `config/msc500.json`, and the
64-byte routine is integrated into the main checker. The same `/AS /Gs /Os`
configuration also matches the previously recovered C helpers. The flag setter
uses `/AS /Os` with stack probes enabled. The official Microsoft MS-DOS C5.10
profile remains available for independent comparison. Current completion
counts come from `build/report.json`, not the earlier experimental ledger.


A later controlled comparison found `/AS /Zi` with **no explicit `/O` option**
exactly matches every helper previously registered under C4, including the
checked BP-frame, state-iterator, input, count and castle routines. It also
matches the 39-byte equality wrapper which C4 did not reproduce. The
[complete fresh matrix](../evidence/msc500_default_all_frames.json) preserves
full CodeView extents, relocations and source/tool hashes. No mixed-version
build is needed to explain those functions; the original command lines still
remain unknown.

## Sources and extraction

The [PCjs disk manifest](https://www.pcjs.org/machines/pcx86/diskettes.json)
lists Microsoft C 5.00 disk images. The compiler was extracted from these
preserved installation disks:

- [5.00 SETUP](https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK1-SETUP.json): `CL.EXE`, `CL.ERR`, `C1.EXE`.
- [5.00 COMPILER](https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK2-COMPILER.json): `C1.ERR`, `C2.EXE`, `C3.EXE`, `C23.ERR`.
- [5.00 UTILITY1](https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK3-UTILITY1.json): archived tools examined separately.
- [5.00 INCLIBS](https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK4-INCLIBS.json): `SLIBC.LIB` runtime comparison.

PCjs metadata identifies WinWorld as the 5.00 media source. This is a
preserved historical proprietary distribution, **not the MIT-licensed
Microsoft MS-DOS tools release**. Experimental compiler files remain in
ignored `matching/toolchains/msc500/`; the library and archived media remain
under ignored `matching/build/`. No claim of relicensing or redistribution
permission is made.

The sector format stores little-endian signed dwords and compresses repeated
sector tails by retaining their final dword. Extraction reconstructs full
sectors, reads the DOS BPB, traverses FAT12 chains, and truncates each file to
its directory size. Every extracted file's MD5 was checked against PCjs's
`fileTable` before use; SHA-256 pins and full archive URLs are retained in
[msc500-experiment.json](../build/msc500-experiment.json). The driver literally
contains `C Optimizing Compiler Version 5.00` and the 1987 runtime copyright.

## Controlled compiler comparisons

Both toolchains compiled the **same unchanged C sources**, in fresh DOSBox
scratch drives. `C:` held only candidate sources and newly generated objects;
`T:` mounted the selected compiler directory read-only. The objects were
parsed with the existing strict OMF parser and linked with explicit original
code/DGROUP placements using `link16.link_function`. The target supplied only
the final expected byte sequence and previously established external
addresses; no target bytes were used as compiler inputs or output patches.

With `/AS /Ox /Zi`, these outputs were identical across releases:

| Function | Target size | C 5.00 | C 5.10 |
|---|---:|---|---|
| `min_i16` | 16 | Exact | Exact |
| `max_i16` | 16 | Exact | Exact |
| `abs_i16` | 21 | Exact | Exact |
| `init_state` | 23 | Exact | Exact |
| `reset_state` | 13 | Exact | Exact |
| `pop_value` | 33 | Exact | Exact |
| `search_state_8fca` | 64 | 65 bytes, fails | 65 bytes, fails |

Those six positive probes establish compatibility but do not distinguish
the compiler releases. The search function does distinguish them when
optimization settings change. All following runs also use `/AS /Gs /Zi`:

| Optimization flags | C 5.00 | C 5.10 |
|---|---|---|
| `/O` | 65 bytes, fails | 65 bytes, fails |
| `/Ot` | 65 bytes, fails | 65 bytes, fails |
| **`/Os`** | **64 bytes, exact** | 65 bytes, fails |
| `/Ox` | 65 bytes, fails | 65 bytes, fails |
| `/O /Ot` | 65 bytes, fails | 65 bytes, fails |
| `/O /Os` | 65 bytes, fails | 65 bytes, fails |
| `/Oa /Os` | 64 bytes, exact | 65 bytes, fails |
| `/Ox /Os` | 65 bytes, fails | 65 bytes, fails |
| `/Ox /Ot` | 65 bytes, fails | 65 bytes, fails |
| `/Od` | 100 bytes, fails | 100 bytes, fails |

The distinguishing extra instruction is a `90` NOP at candidate address
`0x8ffd`, aligning the next call to `0x8ffe`. The original instead calls
directly at `0x8ffd`. Microsoft C 5.00's `/Os` output naturally omits this
internal alignment and emits the correct call displacement and all adjusted
branch displacements. The exact match is **not** obtained by stripping that
byte afterward. `/Zi` supplies the independent procedure extent; it is a
verification setting, not a claim that the original executable had debug
records.

The checked placements for the successful search function are:

| Symbol | Offset |
|---|---|
| `_counter_9880` | DGROUP `0x9880` |
| `_state_8d12` | DGROUP `0x8d12` |
| `_generate_a348` | code `0xa348` |
| `_advance_a4d4` | code `0xa4d4` |
| `_predicate_86d6` | code `0x86d6` |

Detailed byte strings, extents, objects, and results are in
`matching/build/msc500/COMPARISON.json` and `FLAGS.json`. The successful object
is `msc500-flags-2.OBJ`; provenance and source/object/compiled-byte hashes are
in `matching/build/msc500-experiment.json`.

## Independent CRT startup evidence

REA MCP read original image `0xea86`, linear address `0x1ea86`, for 179 bytes:
Evidence
`ev_587bfb28c9071a17199d532d2342ac7b6aa29f64a05a4e424d5af57686e6d032`,
retained in [rea-crt-startup.json](../build/msc500/rea-crt-startup.json).
This is a static shipped-artifact read, not observed runtime execution.

`CRT0` in the 5.00 `SLIBC.LIB` contains 179 code bytes. Every one of the
131 bytes outside its 24 two-byte relocation fields equals the corresponding
original startup byte. `CHKSTK` contains 22 code bytes; its 18 non-relocation
bytes also agree with the original `0xecaa` routine. These are **opcode
fingerprints only**, with no matching credit because the library relocation
fields have not been linked by a verified full runtime build.

For a direct version comparison, the
[archived 5.10 LIBSM disk](https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.10/MSC510-01527-LIBSM.json)
supplies `SLIBCR.LIB`. Its `dos\crt0.asm` member contains **178** code bytes.
At startup-relative `0x36`, it encodes `AND SP,0xfffe` as `83 e4 fe`, whereas
the 5.00 member and the original at image `0xeabc` encode `81 e4 fe ff`.
That one-byte instruction-length difference shifts the remaining startup.
The stock archived 5.10 CRT therefore does not fit the original startup
layout; the 5.00 CRT does. `CHKSTK` has identical 22-byte unlinked code in both
libraries, so the stack checker alone cannot distinguish them.

The archived 5.10 CRT0 member has one invalid checksum in an OMF COMMENT
record at member offset `0x1d2` (record byte sum is `0xff`). All its remaining
records pass their checksums. For **analysis only**, that metadata COMMENT
record was excluded from a transient parser input so the existing strict
parser could inspect the code and fixups. Original archive/member bytes were
preserved unchanged. This exception is not used in the compiler byte-match
workflow, whose generated objects pass strict checksums as emitted.
The archived library file itself passes its PCjs per-file MD5, and archive
and library SHA-256 hashes are retained in `runtime510-provenance.json`.

The current evidence supports a **Microsoft C 5.00-era runtime and a C 5.00
`/AS /Gs /Os` build for at least the search-state module**. It does not yet
establish original flags for every source file, exact library ordering,
the original linker's identity/options, or a complete linked reconstruction.

## Pinned backend and broader option checks

The archived compiler now has a separate checked-in profile,
`matching/config/msc500.json`. Install it explicitly with
`python3 matching/setup_toolchain.py --compiler msc500`. The installer checks
archive SHA-256 hashes before FAT12 extraction, checks each extracted compiler
file against its independent SHA-256 pin, stages the complete installation,
and retains archive files and accurate provenance. A fresh installation was
tested successfully. The checker does not fetch tools automatically.
`msc.compile_c(source, flags, compiler='msc500')` selects this profile;
omitting `compiler` preserves the official 5.10 default. Both profiles share
the same standalone-C, flag, clean-scratch, error-sentinel, and no-stale-object
restrictions. The nine compiler tests pass, including real 5.00/5.10 execution,
forged-manifest rejection, and synthetic FAT12 repeated-tail/loop checks.

A broader 5.00 `/AS /Gs /Os /Zi` matrix also reproduces the 44-byte wait loop
at `0x941b` and the 28-byte board-cell setter at `0x7dbf`, alongside all six
prior C matches and the new 64-byte search match. The 11-byte flag setter at
`0xcb50` instead matches with stack checks enabled, `/AS /Os /Zi`; disabling
checks reduces it to six bytes. This is concrete evidence that one global
option string does not yet describe all matching source files.

The provisional equality wrapper at `0x9448` and board-clear wrapper at
`0x946f` remain unmatched. With stack checks enabled, both 5.00 and 5.10
produce 35 and 23 bytes respectively, versus original lengths 39 and 29.
`/Od` produces 45 and 35 bytes, also failing. Their remaining differences
need source/flag investigation; neither partial opcode agreement nor an
apparently redundant original epilogue earns match credit. Full fresh-build
results and proposed 5.00 unit entries are in `matching/build/msc500/MATRIX.json`,
`EXTRA.json`, and `matching/build/msc500-units.json`.
