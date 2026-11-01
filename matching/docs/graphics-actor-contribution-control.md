# Compositor, graphics wrapper, and actor contribution

`src/graphics_actor_contribution_probe.c` freshly compiles with pinned MSC500
`/AS /Zi` into a complete1124-byte CODE contribution matching original image
3B3A..3F9D. All seven publics occupy their original natural offsets:

| Original image | Procedure | Complete bytes |
| --- | --- | ---: |
| 3B3A | compose_frame_3b3a | 789 |
| 3E4F | reset_graphics_3e4f | 50 |
| 3E81 | clear_actor_3e81 | 48 |
| 3EB1 | insert_actor | 94 |
| 3F0F | attach_actor | 58 |
| 3F49 | detach_actor | 54 |
| 3F7F | detach_all | 31 |

Every complete retained REA extent, independent CodeView extent, linked byte,
and exact original MZ relocation set verifies. The aggregate whole CODE set
also verifies. All1124 bytes belong to complete procedures; there is no
uncredited compositor tail, inserted padding, trimming, or masked byte.

The source uses one genuine eight-byte Frame with four-byte huge pixels,
one32-byte Blit, and one28-byte Actor. Actor's known fields include x/y,
old_x/old_y, flag, colour/square, bounds, near Frame pointer at20, and next
pointer at26. This unifies the former opaque/partial Actor and Frame views
inside the contribution, preserving every call ABI without artificial
extracted helpers. No per-function compiler pragma or mixed profile is used.
An exact source-built contribution does not uniquely identify the historical
translation-unit boundary or settle every remaining whole-program type issue.

The compositor's observed unwritten local word remains uninitialized and is
still copied into blit.saved_word. Its original source-level purpose and
deterministic value are unknown. This control preserves the bytes and retains
that limitation; it does not invent an initialization or claim runtime behavior
that the static evidence cannot establish.

`evidence/graphics_actor_contribution_control.json` retains the complete source,
compiler command/log/tool pins and hashes, object hash/artifact, all function
bytes and metadata, field layouts, whole CODE comparison, and loader sites.
The seven-unit source migration proposal is
`build/graphics-actor-procedure-units.json`, with reproducer
`build/graphics-actor-contribution/probe.py`. No new function credit or
canonical source/configuration/registry/checker edit is introduced here.

The earlier profile matrix was stopped when the coordinator corrected its
profile assumption: the current canonical actor units already use `/AS /Zi`.
That incomplete matrix is not presented as completed configuration evidence.

## Canonical integration

The seven-function trial above is preserved as historical evidence. The live
registry now uses src/graphics_actor_full_match.c with the genuine adjacent
12-byte empty_3b2e: eight complete functions and all1,136 CODE bytes at3B2E..3F9D.
Actor bytes22..25 are now a void far *resource, also used by the typed frame/menu
sources. All50fixups and MZ sites3E5A/3E73/3E7B verify in the production build
and independent raw-OMF pass. The current complete proof is
 evidence/graphics_actor_full_match-contribution.json. The unwritten compositor
local's semantic purpose remains unresolved.
