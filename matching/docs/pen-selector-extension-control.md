# Pen selector: bounded compiler-extension control

Image `5B18..5B3C` remains unmatched. This investigation adds no C credit and does not change canonical source, compiler settings, registry, or checker policy.

The retained original REA dossier is `evidence/rea_pen_select_5b18.json`. Its 37-byte complete body is independently compared against the unpacked, hash-pinned original CHESS.EXE. It contains a zero-frame stack check followed by `MOV ES,[4D94]`, byte accesses at fixed ES offset 12, and a packed nibble store at DGROUP offset `8172`. The target bytes are retained in `evidence/pen-extension-control.json`.

The new reproducer is `build/pen-extension-control/probe.py`. It uses the unchanged pinned production compiler runner and ordinary C source validation. The evidence retains every complete source text/hash, compiler command/log/tool hashes, successful object hash/artifact, complete CodeView procedure extent, full linked bytes and resolved fixups. Parser failures retain their full logs and independently validated toolchain hashes. Successful functions were linked with only the established bindings `pen_segment=4D94`, `packed_pen=8172`, and `__chkstk=ECAA`; no guessed external was added.

| Formulation | Compiler | Default `/AS /Zi` | `/AS /Ox /Zi` |
| --- | --- | ---: | ---: |
| Long-shift far-pointer cast, K&R definition | C4.00 | 59 | 45 |
| Local union of pointer and offset/segment words | C4.00 | 54 | 42 |
| Local union of pointer and offset/segment words | C5.00 | 54 | 42 |
| Register-qualified local far pointer | C4.00 | 61 | 49 |
| Register-qualified local far pointer | C5.00 | 61 | 49 |

All sizes are complete fresh `codeview3_procedure` extents, and none equals the target. These are additional controls; the earlier C5 default/`/Os` 57-byte and `/Ox` 44-byte cast negatives remain separately retained in `evidence/pen-selector-negative.json`. The K&R C4 control makes the source parseable by that compiler rather than repeating a rejected ANSI declaration.

The shortest new output still allocates four stack bytes, stores the offset and segment words there, and uses `LES BX,[BP-4]`. Its nibble operations match the intended behavior, but its addressing and prologue differ. No byte removal, relocation masking, assembly source, or instruction emission was used.

A separate source declaring `_segment` and a `_based(pen_segment)` pointer was rejected by both actual C4 and C5 parsers. This is a syntax control, not evidence of behavior for a program those compilers accepted. Microsoft's C6 manual explicitly identifies based pointers as new to version 6.0 and lists `_based`, `_segment`, and `_segname` among its new facilities: [Microsoft C 6.0 Advanced Programming Techniques, sections 2.2 and B.2.2](https://www.pcjs.org/documents/books/mspl13/c/cadvprg/). That documented later mechanism cannot be assumed available in these C4/C5 controls. No C6 toolchain was installed or substituted.

The bounded conclusion is that the tested C4/C5 formulations do not reproduce the direct segment-word load. A hand-written assembly implementation is plausible, but neither these negatives nor the documented introduction of based pointers proves that attribution or rules out every other authentic compiler/source context. The original function therefore remains unresolved and uncredited. The existing retained REA evidence was reused; this scope made no new target or analysis changes and closed its own REA session.
