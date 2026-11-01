# Independently pinned integer helper library

The integer multiplication helper at image **F32E is now independently reproduced
in full by an archived MSC5.00 library member linked with authentic Microsoft
LINK**. It is 52 bytes of runtime code, not a C reconstruction. A dedicated [authentic helper backend](authentic-helper-backend.md) is now
implemented. Canonical registration and credit are taken from the generated
checker report, rather than this initial standalone probe.

The independent input is `/LIB/LIBH.LIB` from the already pinned PCjs preserved
MSC5.00 INCLIBS disk. `SLIBFP.LIB` was also pinned and examined, but does not
supply this integer helper. The stable provenance, pins, member inventory and
actual-linker results are in
[runtime-helper-libraries.json](../evidence/runtime-helper-libraries.json).

| Input | Bytes | SHA-256 |
|---|---:|---|
| `SLIBFP.LIB` | 37,795 | `0c5f88ec906adbaae285ea2cde9c0cc015acc377e9403be54b27bcfa816d24ae` |
| `LIBH.LIB` | 13,689 | `768bfe171ebcad6d44aeca830ec8d19b31f02ce84ab35c81fc48fcf3f1e14858` |

The source archive is
`https://miscdisks.pcjs.org/pcx86/lang/microsoft/c/5.00/MSC500-DISK4-INCLIBS.json`,
SHA-256 `18a0c57eadf4eea0eb236a0e16f57019c6fd05789dfc52d857b84f6bf7edf58c`.
The extracted files additionally agree with the independently preserved
`fileTable` MD5 values `53dee1f25798d490886767f282dbeffe` and
`ea643d65b497c7a33d14565e3cfa7730`. SLIBFP is a root FAT12 file; LIBH is in the
LIB directory. No target bytes participate in extracting these library inputs.
Both retain the archive's historical proprietary classification.

## Near multiplication, including accepted overlapping records

LIBH has several members with the same name for different calling conventions.
The near `LMUL` member is at library offset `0x1cd0`, 200 bytes, SHA-256
`b0e033a1674414d4a985ad87daee47357fc7730ed67800f20ab4de7f6384bb1d`.
It exports `__aNlmul` and `__aNulmul` at code offset zero. The complete declared
code SEGDEF is 52 bytes and has no unresolved fixups or MZ relocation fields.

The strict shared parser rejects its overlapping LEDATA records. The archive
contains three writes:

| Object code offset | LEDATA bytes | Overlap with previous write |
|---|---:|---|
| `0` | 25 | none |
| `24` | 26 | one byte at `24` |
| `49` | 3 | one byte at `49` |

The overlapping byte changes an earlier `C3` RET to `C2`, with immediate bytes
`08 00` supplied by the later write. The resulting instruction is RET8. This
interpretation is corroborated by **actual linker execution**, rather than a
new byte-repair rule: both independently pinned LINK3.61 and official LINK3.65
accept the unchanged extracted object and emit the exact same complete 52-byte
code image. No object record, checksum, code byte or returned immediate was
modified before linking.

The probe uses `/NOD` and a fresh output name, without a startup object or the
original executable as an input. LINK warns that there is no stack segment;
this diagnostic does not prevent producing the image. The map independently
reports `_TEXT` length `0x34`. No executable is run. The complete emitted image
has SHA-256
`402f81b146b28eb5f6af4a8bb40b0d186957f40485a1912a52ee15e05d4d3bc8`
and equals the original interval `[0xf32e,0xf362)` byte for byte. The far LMUL
member was also linked as a distinguishing negative case; it retains different
argument offsets and RETF8, and does not match.

REA Evidence
`ev_08d5e3c402fb25fa734635a20e2dd618528e6c07ac1615e555209ab4ba1792a1`
is a complete 52-byte raw read at original linear `0x1f32e`, retained in
`rea-runtime-helper-lmulf32e.json`. Its instructions implement multiplication,
including MUL; F32E must not be labelled as a division helper merely because an
earlier guessed C declaration used a divide name. The whole original MZ-site
set in this extent is empty, matching the independently linked member.

Probe files remain under `build/runtime-helper-link/`; the reproducible authentic
linker driver is `build/runtime-helper-link-probe.py`. LINK pins are those
already recorded in the far-call investigation. The strict parser and canonical
library backend were not relaxed for this investigation. The new dedicated backend consumes the independently pinned member through
authentic LINK while preserving the current strict C-source object policy.
It assigns zero authored-C credit.

## Shift helpers and bounded inventory

Two more independently supplied complete code segments already pass the current
strict reader and restricted linker:

| Export | Image | Bytes | Member offset | Member SHA-256 |
|---|---|---:|---|---|
| `__aNlshl` | `f362` | 11 | `1ee0` | `5b9131488ecf6f4cb12edbd99055fd000851a81acc4b742e67b6050db4ee8721` |
| `__aNlshr` | `f36e` | 11 | `1f60` | `6312cfc9cc193104ba978b613757b0749122a9aa8827b96785cd60c7c2b49839` |

Both have no fixups or MZ sites. Full original raw REA reads are retained in
`rea-runtime-helper-lshlf362.json` and `rea-runtime-helper-lshrf36e.json`.
The initial helper proposal covers 74 bytes; the dedicated backend now supports
this additional independently pinned library input. No intervening alignment byte
is included in that number.

The bounded inventory inspected all 45 SLIBFP members, finding no matching
complete original code segment, and all 48 LIBH members. Six LIBH members pass
the current strict parser; 42 are rejected for overlapping LEDATA records.
That count is a format boundary, not evidence that the rejected members are
corrupt or absent from the original. No other helper in those 42 members is
claimed as a match by this pass.
