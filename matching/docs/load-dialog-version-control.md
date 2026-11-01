# CC72 corrected-source compiler-version control

Changing to the pinned Microsoft C5.10 or C4.00 does not reproduce the complete 610-byte CC72 procedure or its original event-body layout under `/AS /Gs /Os /Zi`.

| Compiler and source | Independent CV length | Whole CODE length | Complete differences | Match |
| --- | ---: | ---: | ---: | --- |
| C5.00, corrected typed source | 614 | 614 | 419 | no |
| C5.10, identical corrected typed source | 618 | 618 | 426 | no |
| C5.00, K&R declaration control | 614 | 614 | 419 | no |
| C4.00, identical K&R declaration source | 593 | 593 | 551 | no |

Differences include all excess or missing emitted bytes, without clipping either function. All four retain the 658-byte genuinely used frame and emit 41 relocation fields, including six MZ segment fields. None has the complete original MZ-site set. The C5.00 typed/K&R functions are byte-identical. This isolates the declaration-only syntax adaptation from the C4 comparison, while avoiding any claim that an unspecified prototype is a completed typed whole-program interface.

The corrected typed source is `src/probes/load_game_dialog_cc72_pending.c`. C5.10 receives that exact file, including the proper `restore_ui_92ab(Byte *,Byte)` formal and explicit `(int)ticks_ea5b()` truncation. The C4 diagnostic copy `src/probes/load_dialog_version_kr.c` removes only extern prototype parameter lists and changes the argument-free definition from `(void)` to `()`. Every local declaration, statement, expression and real control flow remains unchanged. No padding locals, artificial helper, pragma or byte manipulation was introduced.

The original native poll at CD09 has navigation kind-7/status-zero tests followed by its body at CD1D; kind-6 checks follow that complete body at CD5C. C5.00 instead tests kind 6 at CD17 before the kind-7 body. C5.10 retains the same early kind-6 test at CD17 and adds a four-byte `MOV BX,[BP-88]` at its kind-7 status check (CD3F), accounting for its four-byte growth over C5.00. C4.00 likewise emits early kind-6 checks, while also allocating the real locals differently. Therefore none of these concrete version controls resolves the source/layout question. They do not establish that the original could not have been built by one of these versions from a different faithful source formulation.

The pinned C4 toolchain was already installed; its historical proprietary provenance in `config/msc400.json` is preserved, with no new licensing claim or download. All compiler files are hash-checked by the existing compiler runner. Source/compiler/toolchain/object hashes, exact commands/logs, independent CV metadata, complete CODE and linked bytes, every mismatch, all relocation logs and full MZ sets are retained in `evidence/load-dialog-version-control.json`. Fresh complete objects, binaries and diagnostic disassemblies are under `build/load-dialog-version-control/`. Run `python3 matching/build/load-dialog-version-control/probe.py` from the repository root to reproduce the compiler comparisons.

The retained primary native dossier and complete original 1626-byte procedure-plus-next context are reused and checked against the pinned unchanged original/reference bytes. No REA session was opened. All previous negative evidence is unchanged. No canonical source, registry, core verifier or test was edited, and no new matching credit or proposal is produced.
