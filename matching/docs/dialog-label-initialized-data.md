# Dialog label definitions and a genuine literal-producing consumer

Fresh exact primary REA reads on the pinned full expanded EXE confirm writable label storage at DS519B (Cancel + NUL,7bytes), DS51A2 (Done + NUL,5bytes), DS51A7 (Cancel + NUL,7bytes), DS51AE (Done + NUL,5bytes). An independent full24-byte primary read confirms the exact consecutive sequence. Each read is compared against the deterministic expansion of the unchanged pinned original. No extra bytes, terminator capacity or unrelated surrounding ownership is assumed.

The complete375-byte native D9C6 consumer loads all four starts and passes lengths6/4/6/4 to canonical D551. Native D551 reads `text[limit]`, temporarily writes NUL there, draws the string, then restores the saved byte. Thus every terminal storage byte is demonstrably consumed, including writes, and the faithful minimal definitions are writable arrays rather than const-qualified arrays. Native evidence does not recover the original declaration's capacity or aggregate identity.

Four separate minimal char-array definitions emit exact standalone7/5/7/5-byte initialized DATA segments/public0/DGROUP without fixups, holes, tails, BSS or other allocations. Their diagnostic proposal remains `build/dialog-label-data/proposed-units.json`; the parent requested these not be canonicalized. Every object is WORD aligned, while two actual target addresses are odd. Complete original source/LINK placement is unresolved. Four named arrays in one genuine source emit27bytes, with publics0/8/14/22 and holes7/13/21, under both default and `/Os`. Strict extraction correctly rejects this natural layout. No hole was synthesized, filled, removed or credited.

A stronger actual-consumer-derived source is `src/probes/dialog-label-data/dialog_button_d9c6_literals.c`. This reconstructs all observed D9C6 logic and calls D551 with its actual four `"Cancel"`/`"Done"` literal arguments. No helper or runtime call exists solely to force storage. Three pinned C5 controls yield:

| Flags after /AS | Full CV | Whole CODE | Whole literal CONST |
| --- | ---: | ---: | ---: |
| /Zi | 401 | 402 | 27, holes |
| /Os /Zi | 380 | 380 | 24, exact |
| /Gs /Os /Zi | 375 | 376 | 24, exact |

Size optimization packs the literal bytes at0/7/12/19 within the real CONST SEGDEF, retaining four distinct literal occurrences. It does not pool away either duplicate. This naturally reproduces the actual24-byte initializer with the genuine consuming function, while named writable-array declarations do not. A single arbitrary packed backing array or aggregate was not introduced.

The `/Gs /Os` source also matches all375 original D9C6 function bytes after an isolated full-CV raw OMF relocation check:40fields, four internal CONST pointers and four MZ segment sites atD9F6/DA66/DA8D/DB33, all exact. Internal fields are at object97/142/248/321, OFFSET16 width2, segment-relative, frame(1,1 DGROUP), target(0,3 CONST), no displacement, with addends0/7/12/19. Explicit CONST placement5CC2:519B yields actual addresses519B/51A2/51A7/51AE. The remaining36fields are existing external/frame5 forms. All arithmetic uses untouched compiler object fields; neither object nor fixup metadata nor target bytes are edited.

The current production `link16` rejects frame(1,1), so this is a reviewed-backend candidate rather than registered credit. `build/dialog-label-data/consumer-proposed-unit.json` records the unit and required explicit internal-segment placement separately. The complete CODE segment has an emitted trailing90 at object375, versus the real following DB3D55: that byte is retained and uncredited. This is full375-function plus literal24 evidence, not a whole376-CODE or authentic complete-source LINK proof. The WORD-aligned CONST segment's actual odd519B base also requires genuine enclosing source context before a full link claim.

Proofs and reproducers:

- `evidence/dialog-label-data-match.json`, `evidence/dialog-label-named-Os-control.json`: standalone arrays and complete four-named-array negatives.
- `evidence/dialog-label-literal-consumer-control.json`: full source/tool/object/segment/fixup records for all three literal-consumer profiles.
- `evidence/dialog-label-consumer-raw-link-control.json`: all375bytes, all40relocations, exact MZ sets, and explicit production limitation.
- `python3 matching/evidence/dialog-label-data-probe.py`.
- `python3 matching/build/dialog-label-data/literal_probe.py` then `python3 matching/build/dialog-label-data/raw_link_control.py`.
- `evidence/rea-dialog-label-*.json`: fresh primary exact reads; retained complete D9C6/D551 native consumer dossiers are referenced in the proofs.
- Own session snapshots `build/rea-dialog-label-data.snapshot.json` and `build/rea-dialog-label-data-complete.snapshot.json`, both saved and closed.

No canonical source, registry, backend, core or test was changed. No function or DATA matching credit is assigned by these diagnostics pending parent review.
