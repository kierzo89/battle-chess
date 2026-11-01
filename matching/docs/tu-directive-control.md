# Diagnostic C5 source controls and mixed profile boundaries

These controls earn zero new C credit and make no canonical source, backend, configuration, or registry changes. They distinguish a historically available mechanism from evidence that CHESS actually used it.

## Target-free compiler controls

The reproducer `build/tu-directive-control/probe.py` compiles new arithmetic/call-loop functions using the independently pinned Microsoft C 5.00 distribution. It never reads the original CHESS file. All complete sources, compiler logs/commands/tool pins, object hashes, segment attributes, publics, function extents, raw procedure bytes and fixups are retained in `evidence/tu-directive-control.json`.

The diagnostic runner makes an explicit process-local exception to ordinary-source policy: it allows only the enumerated pragma lines and applies the unchanged source validator to everything else. Pinned toolchain/flag checks remain active. The production runner and config files are fingerprinted before and after and remain unchanged. These directive-bearing sources remain ineligible for canonical matching under current policy.

Microsoft documented `check_stack(on)`, `check_stack(off)`, and reset-to-command-line behavior in C5. Its manual also documents `loop_opt` and identifies `alloc_text` as a C5 segment-management facility. [Microsoft C 5.0 Optimizing Compiler User Guide, sections 3.3.13 and B.2.3](https://www.bitsavers.org/pdf/microsoft/msdos_c/Microsoft_C_5.0_1987/410840001-500-R04-0887A_Microsoft_C_5.0_Users_Guide_1987.pdf).

Actual C5 controls show:

- Three identical ordinary functions under `/AS /Zi` each emit 55 bytes at public offsets 0, 55, and 110. The WORD-aligned CODE segment ends at 166 bytes, including its final compiler alignment byte.
- Stack checking on/off/reset yields 55, 52, and 55 bytes at offsets 0, 55, and 107. First and third raw complete procedures are unchanged from the ordinary control. Only the middle stack-probe call disappears; no per-function alignment padding appears.
- `/AS /Gs /Os /Zi` with the same on/off/reset directives emits a checked 51-byte function followed by two unchecked 48-byte functions. Reset follows `/Gs`, as documented.
- `loop_opt` is accepted without warning. The chosen simple loop has unchanged output when toggled, both with and without `/Zi`; this is not proof that the pragma has no effect on every loop.
- `optimize("s",on)` and `optimize("t",on)` both produce C4068 unknown-pragma warnings, with unchanged output. Microsoft's C6 manual explicitly says the general `optimize` pragma was new in C6; it cannot be assumed to provide a C5 per-function `/Os` switch. [Microsoft C 6.0 Advanced Programming Techniques, section 1.3](https://www.pcjs.org/documents/books/mspl13/c/cadvprg/).
- `alloc_text` accepts genuine far definitions and emits separate named ALPHA and BETA CODE segments. Both retain attributes `48`, meaning PUBLIC combine and WORD alignment. It also warns about near stack-probe calls across segments. This is segment partitioning, not evidence of a BYTE-alignment escape or a safe complete far-runtime link.

These results establish that mixed stack-probe presence and odd internal function starts are possible within one authentic C5 translation unit. They do not override the independently observed WORD alignment between separately linked PUBLIC CODE contributions, and they do not establish original source directives.

## Requested actual-source profile controls

`build/tu-directive-control/actual-controls.py` uses unchanged canonical source files and the unchanged ordinary-source policy. Its separate evidence `evidence/tu-actual-profile-control.json` retains full sources, fresh compiler/object provenance, every complete CV extent, linked/original bytes, fixups and MZ sets. Only this second experiment reads the pinned original comparison target.

| Source/profile | Original procedure sizes | Fresh sizes | Complete equality |
| --- | --- | --- | --- |
| copy `/AS /Os /Zi` | 147 | 147 | No; loop control diverges at +3A |
| event `/AS /Gs /Zi` | 50, 80, 78 | 50, 80, 82 | First two only |
| board display `/AS /Os /Zi` | 164, 257 | 160, 231 | Neither |

All original interval MZ sets are still accounted for in the retained results. Size equality of the copy is not a byte match. The default-profile decimal conversion adds four epilogue/jump bytes; `/Os` changes both board procedures and the copy loop.

Thus these unchanged source definitions do not form the requested complete 776-byte region under a uniform size/default preference plus only a stack-check transition. A diagnostic combined source is not presented as a solution. The useful configuration constraint is narrower: local C5 stack-probe control was real, but it alone does not resolve this observed boundary and the available evidence does not justify generalizing C6 optimizer pragmas backward. Further faithful source context or a separately corroborated historical build mechanism is still needed; no alignment bytes are removed, fabricated helpers inserted, or SEGDEF metadata altered.

## Bounded default-profile decimal return-flow control

The follow-up reproducer `build/tu-directive-control/decimal-control.py` uses four straightforward ordinary C variants in new copies of the event source, all with `/AS /Gs /Zi`. Results are retained in `evidence/decimal-default-return-control.json`, with complete fresh source/compiler/object/CodeView/linked-byte/fixup evidence. Both 50- and 80-byte event waits remain exact regression controls in every trial.

| Decimal formulation | Complete emitted extent | Original extent | Exact |
| --- | ---: | ---: | --- |
| Early zero-case return | 85 | 78 | No |
| Explicit returns in both conditional arms | 87 | 78 | No |
| Inverted condition with shared return | 82 | 78 | No |
| Conditional expression with comma expressions | 85 | 78 | No |

The ordinary shared-return default control retained all original first 76 bytes, then emitted `JMP +0; MOV SP,BP; POP BP; RET` instead of the original `POP BP; RET`. These bounded return-flow changes do not recover the shorter original epilogue. No complete default-profile 78-byte decimal function was found, so a hypothetical all-default combined region with only local stack-check directives is still unproved. No directive-bearing game source or relaxed canonical policy is proposed.
