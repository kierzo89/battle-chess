# Coherent graphics/menu contribution42A0..578B

`src/graphics_menu_large_contribution_probe.c` freshly compiles with pinned
MSC500 `/AS /Zi` into one complete5356-byte CODE contribution matching the
original. Every byte belongs to a complete procedure; there are no gaps,
discarded tails, authored padding, artificial helpers, masks, or patches.

| Original image | Procedure | Complete bytes |
| --- | --- | ---: |
| 42A0 | render_42a0 | 725 |
| 4575 | prepare_color_4575 | 45 |
| 45A2 | configure_actor_45a2 | 201 |
| 466B | build_menu_466b | 1545 |
| 4C74 | close_menu_4c74 | 489 |
| 4E5D | initialize_menu_bar_4e5d | 472 |
| 5035 | finish_menu_5035 | 122 |
| 50AF | title_menu_50af | 126 |
| 512D | track_menu_512d | 337 |
| 527E | draw_menu_row_527e | 259 |
| 5381 | advance_menu_5381 | 185 |
| 543A | outline_square_543a | 850 |

All twelve publics occur at their original natural offsets within the same
object. Each complete retained REA extent and independent CodeView extent
verifies, as do every linked procedure byte and exact original MZ relocation
set. The complete CODE comparison and aggregate loader-site set also match.
This directly replaces multiple odd-based fragment contexts with one valid
WORD-aligned source contribution. It does not uniquely identify the historical
translation-unit boundary or prove the whole executable link.

The source shares genuine Frame8, Actor28 with far resource at22, Blit32,
Menu4, MenuItem6 and Text4 definitions across all routines. The menu types were
coordinated with the worker reconstructing4C74..527D. Its menu_selected047E
identifier is unified with the already used selected_menu047E; the underlying
placement and int type do not change. Far graphics declarations remain separate
so both graphics_begin and graphics_end retain their real far call ABI.
All original statement/local orders and observed unread frame slots remain.

`evidence/graphics_menu_large_contribution_control.json` retains the complete
source, compiler command/log/tool pins, source/object hashes and artifact,
all PUBDEF and EXTDEF records, raw CODE FIXUPP records and resolved logs,
complete procedure metadata/bytes, type layouts, whole CODE bytes, and loader
sites. The twelve-unit migration proposal is
`build/graphics-menu-large-procedure-units.json`; reproducer
`build/graphics-menu-large-contribution/probe.py`.

No canonical source, configuration, registry, or checker file was edited.
This is source/layout consolidation and adds no duplicate function credit.
