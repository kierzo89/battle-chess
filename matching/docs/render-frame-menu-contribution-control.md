# Enclosing frame preparation context

`src/render_frame_menu_contribution_probe.c` compiles with pinned MSC500
`/AS /Zi` into a complete2516-byte CODE contribution matching original image
42A0..4C73. All bytes belong to complete procedures at natural public offsets:

| Original image | Procedure | Complete bytes |
| --- | --- | ---: |
| 42A0 | render_42a0 | 725 |
| 4575 | prepare_color_4575 | 45 |
| 45A2 | configure_actor_45a2 | 201 |
| 466B | build_menu_466b | 1545 |

This encloses the formerly odd-based frame_prepare fragment with its genuine
predecessor and adjacent menu routine. There is no inserted padding, discarded
tail, artificial helper extraction, masked byte, or per-function profile change.
The result establishes a valid coherent source contribution, not unique
historical translation-unit identity or additional function credit.

A fresh original-CHESS REA dossier,
`evidence/rea_frame_context_render42a0.json`, confirms the complete predecessor
body ends4574 immediately before preparation4575. Complete retained REA
boundaries and independent CodeView extents verify for every procedure, as do
all linked bytes and exact MZ relocation sites, both individually and over
the complete2516-byte CODE span. No alternate analysis carrier was selected.

The unified source uses Frame8 with a huge pixel pointer, Blit32, and Actor28
with a near Frame pointer at20, far resource pointer at22, and next pointer
at26. Menu and input follow-on work independently corroborates the same
Menu{char *label;MenuItem *items} and MenuItem{char *label;int command;
Byte enabled,reserved} types. Text retains its four-byte colour/attribute/text
layout. Source bodies and local declaration order remain unchanged; unread
render/menu frame words retain their observed slots without invented values.
The separate worker owns menu follow-ons beginning4C74.

`evidence/render_frame_menu_contribution_control.json` retains the complete
source, compiler command/log/tool pins, source/object hashes and artifact,
all procedure metadata and bytes, raw resolved fixup logs, type layouts,
whole CODE comparison, and complete loader sites. The four-unit migration
proposal is `build/render-frame-menu-procedure-units.json`; reproducer
`build/render-frame-menu-contribution/probe.py`. No canonical source,
configuration, registry, or checker file was edited.
