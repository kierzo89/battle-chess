# Initialized save-game filename at DS5191

The initialized string consumed by canonical D65A is `Chess.sav`, followed immediately by NUL. Its ten bytes are `43686573732e73617600`, at image61DB1..61DBA = original DGROUP5CC2:5191..519A. The next byte, DS519B, starts a separately addressed `Cancel` string.

Fresh original REA D65A loads5191 at D65D, pushes it as the second argument to F142, and passes the caller's destination as the first argument. Fresh expanded native F142 scans for zero (`REPNE SCASB`, then `NOT CX`) and copies that many bytes, including the terminating NUL. Thus the observed consumed initializer has ten bytes; no guessed capacity or unbounded read of adjacent labels is used. Fresh expanded D9C6 independently loads519B at DA26 as a Cancel-label base and51A2 at DA53 as the following Done-label base. It also addresses a second Cancel/Done pair at51A7/51AE. Those labels are contextual boundary evidence only and receive no proposal/ownership credit.

The packed original provider cannot read initialized DATA at loaded71DB1: its retained query explicitly returns0/64 bytes, incomplete. The actual initializer comes from an exact ten-byte REA read on the pinned, deterministically generated full expanded EXE, SHA256faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02. The whole128-byte primary expanded context is checked against the independently decoded original image, original SHA256c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd. Its start/reference formula, complete initialized range and absence of MZ sites are authenticated by the existing expanded-reference validator.

The ordinary definition `char save_game_filename[] = "Chess.sav";` emits a complete ten-byte initialized DATA SEGDEF, public0 and one DGROUP. Fresh pinned C5 `/AS /Zl /Zi` extraction confirms no fixups, holes, uninitialized tail, BSS or other nondebug allocation. The complete emitted segment matches the exact primary read and decoded original. This reconstructs a minimal complete initialized C array sufficient for the observed consumer. The historical source's declared capacity, surrounding aggregate and actual translation-unit/storage ownership remain unknown. There is no function or packed-file matching claim and no claim that the surrounding literals belong to this declaration.

Artifacts:

- Source: `src/probes/save-name-data/save_game_filename.c`.
- Proposal only: `build/save-name-data/proposed-units.json` (10DATAbytes, `_save_game_filename`, no existing registered overlap).
- Full source/tool/object/SEGDEF/reference proof: `evidence/save-name-data-match.json`.
- Reproducer: `python3 matching/evidence/save-name-data-probe.py`.
- Primary raw/native records: `evidence/rea-save-name-*.json`.
- Saved closed own sessions: `build/rea-save-name-original.snapshot.json`, `build/rea-save-name-expanded.snapshot.json`.

Canonical sources, registry, core and tests were unchanged.
