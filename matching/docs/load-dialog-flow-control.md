# CC72 bounded control-flow addendum

The complete original procedure is still unmatched: 610 bytes at CC72..CED3. This diagnostic uses the retained original native 42-block dossier `evidence/rea-root-cc72.json` and the authenticated complete 1626-byte procedure-plus-next context, without opening or changing an REA session. No source, registry, core verifier, or existing test was changed.

The original event poll at CD09 is followed by kind-7 and status-zero guards, then its complete navigation body at CD1D..CD5B; only then are kind-6 guards and its selection body emitted at CD5C onward. The original native source of these conditions remains unknown. Current faithful C5 `/AS /Gs /Os /Zi` instead puts kind-6 tests before the kind-7 body. The experiment tests ordinary alternate representations of this existing dispatch, with identical real locals and all original operations retained. `restore_ui_92ab(Byte *,Byte)` and `(int)ticks_ea5b()` are unchanged.

| New source form | CV procedure | Whole CODE | Full differences, including excess | Exact? |
| --- | ---: | ---: | ---: | --- |
| Independent kind-7/kind-6 `if` blocks, explicit navigation `continue` | 614 | 614 | 419 | no |
| Negated compound navigation guard to the other-event label | 614 | 614 | 419 | no |
| Navigation code expressed as `if`/`else if`, rather than switch | 620 | 620 | 445 | no |
| Separate explicit kind/status guards to event labels | 615 | 616 | 441 | no |

All four preserve the genuine 658-byte frame. The first output is byte-identical to the retained corrected-ABI 614-byte pending candidate. The fourth genuinely changes layout: the kind-7 body precedes the kind-6 body, but C5 places kind-6 and mouse-kind dispatch checks ahead of both bodies. This leaves incorrect condition placement and branch lengths, rather than recovering the original. Thus matching the source-level body order alone does not force the original optimized CFG layout. No inference that C5 cannot generate the target is justified by these bounded negatives.

The fourth CODE segment has a compiler-emitted final NOP beyond its 615-byte CV procedure. It is retained in full and given no matching credit. The other three complete CODE segments are exactly their CV sizes. Every function was linked in full, and all complete emitted/reference MZ site sets were compared; none match. The difference counts include each excess emitted byte, whereas the earlier 415 count compared only the common 610-byte span of the baseline.

Sources are `src/probes/load_dialog_flow_{sequential,guard,code_if,labeled}.c`. Full source/compiler/toolchain hashes, compiler command/log, fresh objects, complete CODE and linked bytes, all differences and relocation logs are retained in `evidence/load-dialog-flow-control.json` and `build/load-dialog-flow-control/`. Reproduce with `python3 matching/build/load-dialog-flow-control/probe.py` from the repository root. Target bytes are comparison inputs only. No helper, unused local, pragma, byte emission, trimming or modified metadata was used. No proposal or additional matching credit is produced.
