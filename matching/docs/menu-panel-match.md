# Complete menu builder and graphics preparation

Three new ordinary C routines match their full original instruction spans:

| Entry | Role | Complete procedure bytes | Source |
| --- | --- | ---: | --- |
|4575 | Prepare packed frame colours |45 | frame_prepare_match.c |
|45A2 | Configure an actor from a frame |201 | frame_prepare_match.c |
|466B | Construct a multi-row menu panel |1545 | menu_panel_match.c |

All use pinned Microsoft C5.00 `/AS /Zi`, independent complete CodeView lengths,
retained contiguous REA bodies, full relocation-resolved byte comparison and
complete original/emitted MZ-set equality. The two preparation routines cover
the entire246-byte CODE contribution and all8 fixups. Their loader-site sets
are empty. This fragment's odd original start still requires enclosing source
context for a full link.

The menu builder has164 fixups and two original far-call segment fields,
467C and4C6C, retaining graphics aliases11EF:001E and11EF:0000. All1545 bytes
also match at four load paragraphs. The old923-byte extent and internal4A06
candidate are rejected by the complete function/CFG/raw evidence. Its emitted
CODE is1546 bytes: the final90 is outside the function and collides with the
next original4C74 instruction55, so it receives no byte credit or whole-CODE
claim. No trimming or masking is used.

The genuine C types include Frame8, Actor28, MenuItem6, Menu4 and Text4.
Actor's formerly opaque four-byte field at22..25 is a far resource pointer;
Frame* remains near and the actor chain pointer remains at26. The canonical
graphics/actor contribution now uses the same recovered field type. Menus,
geometry, text and row arrays keep their original unshifted bindings.

Fresh proofs are `evidence/frame-prepare-4575-45a2-match.json` and
`evidence/menu-panel-466b-match.json`. Reproducers are retained alongside them
as frame-prepare-probe.py and menu-panel-probe.py. Standalone padding, remaining
menu routines and the full source link remain separate obligations.

## Canonical enclosing source

The standalone padding/alignment limitations above are now resolved in the live
registry by src/graphics_menu_match.c: twelve genuine neighbouring routines
emit the full5,356-byte contribution at42A0..578B, including every menu byte.
See graphics-menu-match.md and its independent complete raw-OMF proof. The old
standalone trials remain retained negative controls; consolidation adds no
duplicate function credit.
