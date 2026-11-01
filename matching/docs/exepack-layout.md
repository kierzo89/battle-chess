# EXEPACK layout and exact analysis round-trip

The pinned Microsoft `EXEPACK.EXE` reports **Version 4.06** and reproduces
the entire local `CHESS.EXE` byte for byte when fed an analysis MZ synthesized
from the recovered original image and relocation sites. Both files are
83,415 bytes with SHA-256
`c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd`.
This identifies a working final packing stage. **It is not a source rebuild
and receives zero matching credit**: its input contains recovered target bytes.

The round-trip proves compatibility, not that this exact historical binary of
EXEPACK was the original producer. The prepacking MZ synthesized here is one
working input, not proof of the original linker's header padding or relocation
segment aliases. Source reconstruction, linking, and original compiler release
identification remain separate work.

## REA observations and decoding

REA MCP Ghidra assembly of original OS entry `0x24142` produced Evidence
`ev_1a42185d782d60768a8b023ef98731b9e61cb05bd2f76b057d83234dbd6e0eb0`.
The whole 679-byte packing block was read at `0x24130`, Evidence
`ev_d623526f86443487ff5c3c4478af7511bbafbd6702ca18424ae7b1295dbf9635`,
retained in [the local analysis evidence](../build/exepack/rea-packed-block.json).
The unpacking interpretation below comes from those actual instruction bytes,
decoded independently with `ndisasm -b16`. Ghidra's Listing text reverses some
segment-register MOV directions, so bytes take precedence over that text.
REA static analysis does not execute the unpacker or expose unpacked memory.

The 283-byte embedded unpacker is identical to the pinned official packer at
file `0x35e2`, as already recorded in
[the stub comparison](../evidence/rea_compiler_exepack_comparison.json).
Its SHA-256 is
`3c2ecf0c7854abfe0390cfa2482fc3941cf255546ce1629132eb62bb08f3d435`.
The analysis decoder [exepack.py](../exepack.py) accepts this exact profile,
validates all stream and relocation bounds, and returns unrelocated bytes.

## On-disk regions

All ranges are half-open. Image offsets exclude the 512-byte MZ header;
file offsets add `0x200`. Ghidra linear addresses add `0x10000` to image offsets.

| Region | File offsets | Size | Meaning |
|---|---|---:|---|
| Packed MZ header | `0x00000–0x00200` | 512 | OS metadata; zero DOS-loader relocations |
| Unchanged image prefix | `0x00200–0x112dc` | 69,852 | Original unrelocated image bytes |
| Compressed tail stream | `0x112dc–0x14329` | 12,365 | 249 backward fill/literal commands |
| Alignment | `0x14329–0x14330` | 7 | `ff` bytes skipped by decompressor |
| EXEPACK header | `0x14330–0x14342` | 18 | Saved entry/stack, lengths, signature |
| Unpacker and error string | `0x14342–0x1445d` | 283 | Identical official EXEPACK stub |
| Packed relocations | `0x1445d–0x145d7` | 378 | 16 group counts plus 173 offsets |

There is no appended overlay: the MZ-declared length equals the physical file
length. The executable contains compressed data after the readable prefix;
disassembling that disk tail as ordinary code would create fictitious routines.
Any whole-image inventory must classify the expanded image, not simply every
byte after the original MZ header as original program code.

The packed MZ header has CS:IP `1413:0012`, SS:SP `621a:0080`, minimum
allocation `0x5643` paragraphs, maximum allocation `0xffff`, relocation-table
offset `0x001e`, and zero relocation entries. Word `0x1c` is `1`.

## Packing header and algorithm

| Header offset | Value | Observed use |
|---|---|---|
| `0x00` | `ea86` | Saved original IP |
| `0x02` | `0000` | Saved original CS; runtime adds load segment |
| `0x04` | `0000` | Scratch; runtime stores original load segment |
| `0x06` | `02a7` | Copy 679-byte packing block out of expansion's way |
| `0x08` | `1000` | Saved SP |
| `0x0a` | `6980` | Saved SS; runtime adds load segment |
| `0x0c` | `61ef` | Expanded image paragraphs; packing block copied here |
| `0x0e` | `0001` | Source/destination backward-window adjustment |
| `0x10` | `4252` | `RB` signature |

After relocating its own 679-byte block above the expanded image, the stub
walks backward from just below its original header, skips up to a paragraph
of `ff` alignment, and reads a command byte followed backward by a little-endian
16-bit count. Commands `b0`/`b1` repeat the preceding byte; `b2`/`b3` copy the
preceding count literal bytes. An odd command is the final command. Segment
windows are normalized as needed; the Python decoder uses equivalent linear
coordinates. The final decoded destination and compressed source both end at
image offset `0x110dc`, leaving that leading prefix untouched.

The expanded paragraph image is 401,136 bytes (`0x61ef0`), SHA-256
`54262c45a01c80f20418fb37c8a5adca39d877bcea3f913ee40fa53175837e20`.
It includes zero spans `0x110dc–0x11ef0`, `0x120c2–0x5cc28`, and
`0x5fae1–0x610ed`. The large middle zero span is stored as five fill packets.
Expanded bytes are initialized load-image contents, not a claim that they all
represent code or that every zero was a source-level initialized object.

Relocations start at packing-header offset `0x12d`. Sixteen groups correspond
to consecutive 64 KiB image windows. Each has a 16-bit count followed by that
many 16-bit offsets. Counts are
`[151,17,0,0,0,1,4,0,0,0,0,0,0,0,0,0]`, totaling 173 sites ranging from
image `0x98` to `0x619c6`. The runtime adds the original load segment to each
word. Its special case for offset `ffff` handles a word crossing a 64 KiB
boundary; the decoder's linear addresses naturally preserve that case.
These runtime relocations explain why a DOS memory capture can differ from
on-disk readable code even though the packed MZ reports zero loader relocations.

## Exact packing experiment

The first synthesized MZ retained all `0x61ef0` expanded bytes, used a
1,024-byte header and relocation offset `0x1c`, and repacked to the correct
file length with only nine differing bytes. Seven differences were in the last
compressed commands; two were header metadata.

The exact successful input uses:

| Property | Working value |
|---|---|
| Uncompressed input image length | `0x61eeb` = 401,131 bytes |
| Paragraph padding | Omit final five zero bytes from input |
| MZ header size | `0x400` = 1,024 bytes |
| Relocation count and offset | 173 at `0x1e` |
| Relocation aliases | Offset within 64 KiB, segment in multiples of `0x1000` |
| Saved entry | `0000:ea86` |
| Saved stack | `6980:1000` |
| Minimum/maximum allocation | `0x0892` / `0xffff` paragraphs |
| Reserved word at `0x1c` | `1` |
| Checksum/overlay number | `0` / `0` |

The original input length is inferred through this controlled round-trip:
including five explicit zeros produces a different final literal packet;
omitting them lets the packer emit its separate five-byte zero-padding fill,
exactly as the target does. The paragraph-level expanded image alone cannot
distinguish intentional trailing zeros from packer-generated padding.
The inferred original minimum allocation follows the tested relationship
`ceil(packed_image_size/16) + packed_minalloc - expanded_paragraphs = 0x892`.

Reproduce the analysis input with Python from the repository root:

```python
from pathlib import Path
import sys
sys.path.insert(0, 'matching')
from exepack import unpack_exepack
decoded = unpack_exepack(Path('CHESS.EXE').read_bytes())
Path('/YOUR/FRESH/SCRATCH/UNPACK.EXE').write_bytes(decoded.analysis_mz(trim_padding=5))
```

Run DOSBox with a fresh scratch `C:` and read-only pinned compiler directory
as `T:`. The only DOS command required is
`T:\EXEPACK C:\UNPACK.EXE C:\REPACK.EXE`.
Compare **all** output bytes and lengths to the target, without relocation
masking, header normalization, or postprocessing.

Local outputs in `matching/build/exepack/` include `TRIM5_UNPACK.EXE`,
`TRIM5_REPACK.EXE`, `TRIM5_PACK.LOG`, and [ROUNDTRIP.json](../build/exepack/ROUNDTRIP.json).
The analysis input SHA-256 is
`faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02`.
These local artifacts contain recovered original bytes and must stay outside
any reconstructed build or completion numerator.

For the full-byte goal, a future genuine compiler/linker build must generate
the same 401,131-byte uncompressed image, all 173 relocation sites, and the
relevant MZ metadata. The now-verified official packer can then produce the
83,415-byte final comparison artifact. The round-trip eliminates packer
compatibility as a speculative blocker; it does not solve those source/link
requirements.
