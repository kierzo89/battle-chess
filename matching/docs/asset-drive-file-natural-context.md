# Drive probe and file helpers: natural source context

The current five-function selector/file source is already C5 AS/Os/Zi. Six fresh existing-source controls show:

| Source | AS/Zi | AS/Os/Zi |
| --- | --- | --- |
| Drive probe C9D0 |140 bytes, wrong|134 bytes, exact|
| Selector plus four file helpers CA56..CC45 |528 CODE, all five wrong|496 CODE, all five exact|
| Near table selector CC46 |44 bytes, exact|42 bytes, wrong|

The table selector's two-byte profile discrepancy is a real control-flow difference. Default output shares a final `MOV SP,BP; POP BP; RET`; Os replaces the true-arm jump with its own `POP BP; RET` and omits the final stack restoration. Neither uniform default nor uniform Os reproduces all seven current function forms. No per-function pragma, padding object, synthetic helper or code edit was attempted.

A genuine six-function merge at `src/probes/asset_drive_file_flow_match.c` naturally emits the complete630-byte CODE contribution at imageC9D0..CC45 under AS/Os/Zi. All six independent CV extents and PUBLIC offsets equal their observed placements from one contribution baseC9D0. Every one of58 actual CODE fixups is owned and reapplied; the complete emitted and original MZ site sets both contain onlyCC21. No CODE byte is sliced or omitted.

Keeping the actual44-byte table-selector source as a second AS/Zi contribution gives complete674-byte equality for imageC9D0..CC71. It has nine CODE fixups and no MZ fields. Both contributions have PUBLIC WORD2 `_TEXT` shape, even starts, even complete sizes630/44 and no inserted padding. The complete concatenation equals both the unrelocated EXEPACK reference and unchanged original file prefix. This is comparison/layout evidence for two independently compiled source contributions, not an actual final LINK manifest, historical translation-unit ownership or a complete source-built executable.

For contrast, the natural seven-function uniformOs candidate is retained separately at `src/probes/asset_startup_uniform_Os_candidate.c`: its complete CODE is672 bytes. All first six functions remain exact; the last42-byte function does not equal original44. Its entire output is retained without appending or trimming anything.

The six-function merge preserves the existing selector's historical unprototyped declaration `exit_07f3()`: real call sites pass zero or one argument. This scope does not claim typed whole-program exit ABI closure. Other shared declarations and symbol placements are consistent; no shifted global aliases or new definitions are introduced. The separate table unit in the proposal keeps root's canonical source `src/asset_table_select_match.c`.

Primary records are `evidence/asset-profile-context-control.json` (six source/profile controls) and `evidence/asset-drive-file-natural-context.json` (whole630, uniform672 negative, separate44, full674 concatenation, full source/tool/object/CV/bytes/fixup/MZ provenance). New proposal: `build/asset-profile-context/merged-six-plus-table-units.json`. Reproducers: `build/asset-profile-context/probe.py` and `merge.py`. No new matching function credit is requested: this is source-context consolidation of six existing/pending procedures plus the separate already-matched table selector.

Original REA dossiers from the registered/pending unit proofs are reused. No new binary boundary question or REA session was needed. Canonical sources, registry, core and tests remain untouched; the separately reconstructed C868..C9CF worker source is outside this scope.
