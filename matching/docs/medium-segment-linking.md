# Named medium-model code and the small-model runtime

The compiler runner now accepts an explicit `source_name`, defaulting to its
existing `UNIT.C`. A named source such as EVALA.C produces EVALA_TEXT with
MSC5.00 `/AM`; `/AS` still produces _TEXT. Names are validated uppercase8.3
C filenames, with paths, batch syntax and device names rejected before running
tools. All existing source restrictions and compiler hash pins remain active.
The actual DOS source name is recorded in CompileResult and the compiler command.

[medium-segment-link-experiment.json](../evidence/medium-segment-link-experiment.json)
checks a meaningful complete three-object executable. MAIN.C uses `/AS /Gs /Zi`,
defines real shared state initialized to3, and checks the result of a far call.
EVALA.C and EVALB.C use `/AM /Gs /Zi`; A calls B across source files and both
read the shared DATA definition. Genuine pinned SLIBC supplies the small-model
startup and runtime. No original CHESS or expanded reference is read or mounted
during generation. These controls receive zero target matching credit.

Authentic LINK3.65 `/NOD /DOSSEG /MAP` succeeds in both object orders, and both
generated DOS executables return zero after their arithmetic check. The three
complete CodeView procedures have33,24 and19 bytes; every byte equals the
restricted linker's output using actual map placements. Their complete MZ-site
sets also agree. The source segment names remain distinct, while exchanging
the objects changes placements and the encoded cross-source far pointer:

| Object order after MAIN | A address | B address |
| --- | --- | --- |
| EVALA, EVALB |0052:0008 |0054:0000 |
| EVALB, EVALA |0053:000C |0052:0008 |

Those nonzero offsets show why a CODE contribution's physical start must be
kept separate from its CS frame base. Both objects resolve the same real
shared-state definition at DGROUP0042, whose complete initializer is0300.
The proof retains maps, commands, execution logs, fixups, MZ sites, complete
input inventories and all source/object/tool/library hashes. Reproduce with
[medium-segment-link-probe.py](../evidence/medium-segment-link-probe.py).

This establishes a working mixed small/medium source-link configuration with
the actual compiler/runtime family, and corroborates the placement arithmetic
needed for the game's far evaluation segment. The separate original-evaluator
control preserves its bytes under either model. Neither experiment uniquely
recovers original source filenames, per-module switches, object order, complete
DGROUP allocation or the complete original executable layout.
