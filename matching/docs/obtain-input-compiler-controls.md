# Compiler controls for the input dispatcher at image 0254

Fourteen bounded controls reused the same C source and external placements,
with no source-level changes between runs. No canonical source, configuration,
checker, contribution policy, or matching credit was changed by these controls.

The full [evidence index](../evidence/obtain-input-0254-compiler-controls.json)
pins the tools, source, scripts, raw objects, relocations, complete CODE bytes,
real compiler procedure boundaries, and comparison results. The exact compiled
source is frozen as [CONTROL_SOURCE.C](../build/obtain-input-controls/CONTROL_SOURCE.C),
SHA-256 `7193e7f78e0116ba0f8f13ac63ac39e826d3e992b200915efe32bf13ef47840e`.
Root subsequently improved its receiver declaration/comment in the canonical
source; the frozen control input retains the hash recorded by every run.

## Results

| Compiler | Flags | Compiler procedure bytes | Entire CODE bytes | Result |
|---|---|---:|---:|---|
| C 5.00 | `/AS /Zi` | 1439 | 1440 | Complete procedure matches; final CODE NOP differs |
| C 5.00 | `/AS /G0 /Zi` | 1439 | 1440 | Identical complete CODE to baseline |
| C 5.00 | `/AS /Zi /Zl` | 1439 | 1440 | Identical complete CODE to baseline |
| C 5.00 | `/AS` | No CV procedure; extent 1402 | 1402 | Differs |
| C 5.00 | `/AS /Zd` | No CV procedure; extent 1402 | 1402 | Identical complete CODE to `/AS` |
| C 5.00 | `/AS /O /Zi` | 1402 | 1402 | Identical complete CODE to `/AS` |
| C 5.00 | `/AS /Od /Zi` | 1732 | 1732 | Differs |
| C 5.00 | `/AS /Os /Zi` | 1367 | 1368 | Differs; final CODE NOP retained |
| C 5.00 | `/AS /Gs /Zi` | 1436 | 1436 | Differs |
| C 5.00 | `/AS /Ox /Zi` | 1422 | 1422 | Differs |
| C 5.10 | `/AS /Zi` | 1436 | 1436 | Differs |
| C 5.10 | `/AS /O /Zi` | 1400 | 1400 | Differs |
| C 5.10 | `/AS /Os /Zi` | 1364 | 1364 | Differs |
| C 4.00 | `/AS /Zi` | None | None | Unchanged source rejected at a prototype declaration |

The baseline's real CodeView procedure is 1439 bytes and uses 181 ordinary
relocation fields covering 370 distinct bytes. All 1069 other bytes and all
relocated fields agree with the entire native procedure span. The linked
procedure SHA-256 is
`2432bdd2e49be5fe9d753bed31505d9b0c70e175706480b87fc42482907a80e7`.

The standalone CODE segment is nevertheless **1440 bytes**: it ends in `90`
at image 07f3, where the original next function begins with `55`. The control
retains that byte and records the whole-CODE mismatch. It does not truncate
the contribution to turn the standalone object into credited output. The
separate grouped main/input/exit contribution proof belongs to its own
registration work.

## Why `/Zi` changes the code

The observed effect is documented by Microsoft's *C Optimizing Compiler
User's Guide* (1987), section **3.3.12, printed page 87 / PDF page 99**:
[original manual scan](https://www.bitsavers.org/pdf/microsoft/msdos_c/Microsoft_C_5.0_1987/410840001-500-R04-0887A_Microsoft_C_5.0_Users_Guide_1987.pdf#page=99).
The page was independently extracted and visually checked. The downloaded
public mirror's PDF SHA-256 is
`e5ac6adce704046d8958d86a4d8130dbbaa735b070838772e389c04134cc9062`.

The manual explains that `/Zi` without an explicit `/O` option suppresses
code motion and rearrangement while keeping simple optimizations. An explicit
`/O` option restores the requested optimizations. That explains this source's
1439-byte versus 1402-byte result; `/Zi` is materially part of the tested code
generation configuration. It is insufficient to describe it as verification
metadata alone. No inference that debug symbols shipped in CHESS.EXE follows.

## Limits of the conclusion

Pinned C 5.00 `/AS /Zi` is a demonstrated compatible configuration for this
complete reconstructed procedure. The tested C 5.10 alternatives fail, and
removing stack checks fails. Explicit `/G0` and `/Zl` cannot be distinguished
from their omission here, because the complete emitted CODE bytes are equal.
C 4.00's syntax rejection does not exclude another C4-compatible source form;
its source was deliberately not rewritten for this control. Other compiler
patches, untested options, per-function settings, and equivalent source shapes
remain possible. These controls narrow compatible configurations without
claiming a unique historical command line.

## Final canonical declaration cross-check

After the return-type/name cleanup, a separate [final-source C5.10 control](../evidence/final-main-input-c510-control.json)
compiles the exact canonical main/input/exit source. C5.00 emits2094 CODE bytes;
C5.10 emits2092, including its retained final90. Main580 and shutdown75 would
match individually at their original slots, but the dispatcher remains1436
versus1439 and the complete source contribution differs. This independently
checks that the earlier frozen control input's declaration details do not
explain away the C5.10 mismatch. It grants no credit and still does not exclude
untested compilers, flags or different equivalent source forms. Reproduce with
`python3 matching/evidence/final-main-input-c510-control.py`.
