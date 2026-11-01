# Expanded independent runtime library reconstruction

The pinned MSC5.00 `SLIBC.LIB` now supplies **35 complete CODE SEGDEFs, 3,917 bytes** that link exactly to the original. The new pass adds 33 members and 3,716 bytes beyond CRT0/CHKSTK, resolves 161 additional fixups, and verifies the entire MZ-site set for every extent. Every added code extent has an empty MZ-site set; the original two CRT0 code sites remain separately verified. This is independent runtime-library credit, never authored C or ASM credit.

The new inputs and unit proposals are retained in `build/runtime-more-members.json`; a standalone merged generation profile is `build/runtime500-expanded-profile.json`. Canonical configuration and registration are maintained in `config/runtime500.json` and `config/units.json`. Whole comparisons, member pins, explicit placements, original operand constraints and generated fixup arithmetic are in [runtime-more-link-verification.json](../evidence/runtime-more-link-verification.json). Each member also has a complete original-target REA raw-byte read in `evidence/rea-runtime-more-*.json`.

## Complete new code extents

| Member | Image offset | Complete bytes | Fixups |
|---|---:|---:|---:|
| `CRT0DAT` | `0xeb3a` | 367 | 43 |
| `CRT0MSG` | `0xf470` | 32 | 4 |
| `CRT0FP` | `0xf490` | 6 | 1 |
| `CHKSUM` | `0xf496` | 34 | 2 |
| `STDARGV` | `0xf4b8` | 398 | 12 |
| `STDENVP` | `0xf646` | 102 | 3 |
| `NMSGHDR` | `0xf6ac` | 84 | 2 |
| `STDALLOC` | `0xf920` | 66 | 7 |
| `DOSRET` | `0xf700` | 84 | 7 |
| `CLOSE` | `0xecc0` | 32 | 3 |
| `LSEEK` | `0xece0` | 122 | 3 |
| `OPEN` | `0xed5a` | 420 | 13 |
| `READ` | `0xeefe` | 219 | 9 |
| `WRITE` | `0xefda` | 296 | 13 |
| `STACKAVAIL` | `0xf754` | 18 | 1 |
| `STRCAT` | `0xf102` | 63 | 0 |
| `STRCPY` | `0xf142` | 50 | 0 |
| `STRCMP` | `0xf174` | 43 | 0 |
| `STRLEN` | `0xf1a0` | 27 | 0 |
| `STRNCPY` | `0xfae6` | 40 | 0 |
| `STRNCMP` | `0xfb68` | 58 | 0 |
| `ATOX` | `0xfba2` | 84 | 0 |
| `tolower.c` | `0xf1bc` | 26 | 1 |
| `getenv.c` | `0xfb12` | 86 | 3 |
| `TIME` | `0xf204` | 87 | 1 |
| `tzset.c` | `0xf962` | 388 | 16 |
| `statconv.c` | `0xf766` | 278 | 10 |
| `MEMCMP` | `0xf25c` | 39 | 0 |
| `MEMCPY` | `0xf284` | 44 | 0 |
| `MEMSET` | `0xf2b0` | 45 | 0 |
| `rand.c` | `0xf2de` | 56 | 7 |
| `B_EQUIPL` | `0xf316` | 3 | 0 |
| `GETDRIVE` | `0xf31a` | 19 | 0 |

The discovery inventory scanned all 302 independently archived members. Opcode comparisons with fixup fields omitted were used only to locate candidates. Every credited candidate was then extracted afresh by library/member SHA-256, linked with explicit addresses, and compared in full without excluded bytes. The complete nonzero-sized code SEGDEF, including all its publics and internal helpers, is retained. No procedure is truncated at a next-public boundary.

All selected fixup forms were already supported by the restricted linker. Library extraction needed one container improvement: SLIBC contains two distinct objects named `MEMCPY`. The mandatory independently pinned member SHA-256 now selects the unique matching member. Multiple identical copies still fail closed. Object checksum checks remain strict. The test suite includes actual duplicate-name extraction and a synthetic ambiguous identical-copy library.

The code scan has bounded omissions: `CMISCDAT` is rejected because its fixup follows iterated data, and two `HDIFF` members contain overlapping LEDATA records. No checksums, records or bytes were removed to admit them. Small ambiguous aliases such as OLDNORM were not registered from opcode similarity. No full matching SLIBC member was established for image F32E. Its raw bytes indicate long multiplication, rather than division, and include MUL and RET8 (REA Evidence `ev_6e902f5d76d432db7c8061e609a793bca129edccc002cb05698b73e0f992fcac`, retained in `rea-runtime-f32e-multiply.json`). SLIBC references the corresponding `__aNlmul` symbol but does not define it; the separate [integer-helper investigation](runtime-helper-libraries.md) subsequently identifies and pins LIBH and reproduces this complete52-byte helper with authentic LINK. Its canonical backend integration remains separate.

## Independently initialized runtime data

Nine whole initialized DATA/MSG SEGDEFs independently generate **170 bytes** matching the expanded original. They are not direct packed-file spans and must not contribute 170 compressed-file bytes. Their profiles are [runtime-data-members.json](../evidence/runtime-data-members.json); the exact comparisons, initialized/unsupported distinctions, anchors and REA provenance are [runtime-data-candidates.json](../evidence/runtime-data-candidates.json).

| Member / segment | Image offset | Bytes | Public at zero | Fixups |
|---|---:|---:|---|---:|
| `CRT0MSG / _DATA` | `0x61626` | 2 | `__adbgmsg` | 0 |
| `CHKSTK / _DATA` | `0x61620` | 2 | `STKHQQ` | 1 |
| `STDARGV / _DATA` | `0x61628` | 2 | none (segment/code anchor) | 0 |
| `NMSGHDR / HDR` | `0x61e12` | 8 | none (segment/code anchor) | 0 |
| `DOSRET / _DATA` | `0x6162a` | 20 | none (segment/code anchor) | 0 |
| `days.c / _DATA` | `0x61742` | 52 | `__lpdays` | 0 |
| `tzset.c / _DATA` | `0x61776` | 3 | none (segment/code anchor) | 0 |
| `timeset.c / _DATA` | `0x6177a` | 77 | none (segment/code anchor) | 2 |
| `rand.c / _DATA` | `0x61622` | 4 | none (segment/code anchor) | 0 |

The day tables provide a substantial nonzero public-at-zero example: `days.c` DATA segment 2 is 52 initialized bytes at image `0x61742`, with `__lpdays` at object zero and `__days` at offset 26. CHKSTK data contains the independently linked `_end+0x100` stack boundary. The two literal zero words in CRT0MSG and STDARGV are actual complete archived LEDATA initializers; they are distinct from uninitialized BSS. No BSS, inferred zero-filled hole or copied original zero span receives credit.

The initialized-data scan deliberately excludes CRT0 `_DATA` (88-byte segment with a hole), CRT0DAT CDATA (14-byte segment with holes), and CRT0DAT `_DATA` / CTYPE (iterated-data forms not admitted by the existing parser). TXTMODE has a complete initializer but differs from the original, so it is retained as a mismatch rather than normalized.

The derived analysis carrier is reconstructed deterministically from the hash-checked original using `unpack_exepack(original).analysis_mz(trim_padding=5)`. Its SHA-256 is `faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02`. All nine raw data reads are bound to that exact carrier and Ghidra load segment `0x1000`. None of these 170 bytes intersects an original MZ relocation, so the exact forward loader-adjustment list is empty.

[reference.py](../reference.py) creates this provenance-bound comparison context and validates exact full REA reads against both independent linked bytes and the unrelocated expanded image. It currently rejects any MZ field overlapping an expanded unit, including a word crossing its beginning. It never masks or normalizes relocation fields, and never generates reconstructed bytes.

## Independent generation and validation

```sh
python3 matching/library16.py \
  --library matching/toolchains/runtime500/SLIBC.LIB \
  --profile matching/evidence/runtime-data-members.json \
  --output matching/build/runtime-data-linked
python3 -m unittest discover -s matching/tests -p test_library16.py -v
python3 -m unittest discover -s matching/tests -p test_reference.py -v
```

The generator never reads the reference EXE. CODE and DATA profile entries can use distinct `id` values for output artifacts from the same archive member. It rejects duplicate/path-escaping artifact IDs before publishing files. The reference checker is a separate comparison step. Full executable construction remains unfinished: more game functions, additional runtime/support inputs, complete data layout and packing still have to be independently generated.
