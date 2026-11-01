# Toolchain evidence and initial reconstructed functions

## Current result

Microsoft C **5.00** is now pinned and running, with actual C byte matches.
The original CRT startup matches its era and a search routine distinguishes
its `/AS /Gs /Os` output from 5.10. Current configuration and controlled
comparisons are in [msc500-comparison.md](msc500-comparison.md); use
`python3 matching/setup_toolchain.py --compiler msc500` to provision the pinned
local compiler. The bounded tool search below records the earlier baseline,
before these tools were obtained. Exact original settings for every module
and full linker layout remain unresolved.

`CHESS.EXE` contains the ASCII string `MS Run-Time Library - Copyright (c) 1987, Microsoft Corp` at executable file offset **0x114c9** (70857). The `R6000`, `R6003`, `R6009`, `R6002`, and `R6001` diagnostics and the stack-check helper at load-image offset `0xecaa` support Microsoft C runtime provenance. Microsoft C 5.x is a candidate family; the exact compiler version, linker, memory model, optimization flags, and any mixed-toolchain modules remain unverified. A runtime copyright date alone cannot prove the compiler version.

The DOS header is 0x200 bytes. Image offsets below therefore map to file offsets by adding 0x200. `disasm/chess/chess_image_bytes.bin` is that disk load image. In the existing `unpacked/chess_code.bin`, which starts at captured linear address 0x8000, the main image starts at offset 0x240 (captured linear address 0x8240). Original main-image offset `x` maps to dump offset `x + 0x240` and captured address `x + 0x8240`. These are capture-specific runtime addresses, not universal load addresses.

The executable has a real decompression/relocation stub at file offset 0x14342 (header CS:IP = 1413:0012), including the `!Packed file is corrupt` diagnostic. Nevertheless, the three functions below already occur verbatim on disk, and most of the main code can be compared directly. Many disk/runtime differences are segment relocations: for example, image offset 0x98 contains segment 0x10e3 on disk and 0x1907 in the capture, a difference of 0x824 paragraphs. The whole captured memory region must not be treated as an independently reproducible disk image.

## Manually checked bounds

All bounds are half-open. These functions contain no relocation operands, imported original byte slices, or calls. Their conditional branches and both return paths were checked directly in the original load-image disassembly.

| Function | Image range | File range | Dump range | Captured linear range | Bytes |
| --- | --- | --- | --- | --- | ---: |
| `min_i16` | 0x8f95–0x8fa5 | 0x9195–0x91a5 | 0x91d5–0x91e5 | 0x111d5–0x111e5 | 16 |
| `max_i16` | 0x8fa5–0x8fb5 | 0x91a5–0x91b5 | 0x91e5–0x91f5 | 0x111e5–0x111f5 | 16 |
| `abs_i16` | 0x8fb5–0x8fca | 0x91b5–0x91ca | 0x91f5–0x920a | 0x111f5–0x1120a | 21 |

NASM sources in `../asm/` reconstruct the instruction sequences independently. NASM selects opcode `89 e5` for `mov bp, sp`, whereas the original uses the equivalent `8b ec`; that single instruction uses an explicit two-byte encoding with its mnemonic documented. No complete function or original byte slice is embedded. `../src/math16.c` records their signed 16-bit semantics; it is not matching C compiler output. `abs_i16(INT16_MIN)` returns `INT16_MIN`, as 8086 `NEG` wraps that input. The C implementation explicitly handles the boundary without signed overflow or implementation-defined narrowing.

The existing `tools/build_function_index.py` stops function sizes at the first return. This undercounts functions with multiple returns: it reports 14 bytes for the 21-byte absolute-value function. Another example is image offset 0x3ac2, reported as 22 bytes although a conditional branch reaches its second return at 0x3ae2, requiring 33 bytes. Existing inferred function counts and byte totals are therefore inventory estimates, not authoritative completion denominators.

## Available tools: bounded local search

During this investigation, `command -v` found `/usr/bin/nasm` and `/usr/bin/dosbox`, but no `bcc`, `wcc`, or `ia16-elf-gcc`. A filename search under `/home/kierzo`, `/opt`, and `/usr/local` found no `cl.exe`, `c1.exe`, `bcc.exe`, `wcc`, or `wcc.exe`. This is a bounded search, not proof that no compiler exists elsewhere or inside an archive. The installed host GCC targets x86-64 and does not establish the original Microsoft compiler's code generation.

A genuine C matching claim requires a reproducible 16-bit compiler configuration and comparison of its resulting machine code against the original function bytes, with explicit relocation handling where applicable. NASM instruction matches and portable semantic C are tracked separately.
