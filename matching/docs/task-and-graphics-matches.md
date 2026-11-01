# Task allocator and graphics wrapper

Two ordinary C procedures now match complete original instruction spans:

| Entry | Source | Bytes | Compiler flags | MZ sites |
| --- | --- | ---: | --- | --- |
|3B0C | animation_task_allocate_match.c |33 | C5.00 /AS /Gs /Os /Zi | none |
|3E4F | graphics_reset_3e4f_match.c |50 | C5.00 /AS /Zi |3E5A,3E73,3E7B |

The allocator uses a signed cursor and four near AnimationTask pointers. The
opaque task type is never emitted as a byte array or arbitrarily sized object;
its pointer use follows the actual task consumer. Exhaustion calls the observed
error routine/message. Its final compiler alignment byte lies outside the
independent33-byte CV procedure and receives no credit.

The graphics wrapper passes the canonical huge screen pointer and160-by200
region to the existing far graphics interfaces. Exact far aliases are retained;
all50 bytes and the complete CODE SEGDEF match. The three original loader
sites also agree at four independent load paragraphs. A fresh58-byte REA read
includes the next matched procedure as context. Whole-source/link placement
remains a separate requirement.

Complete source/tool/object provenance, REA boundaries, byte strings and MZ
proofs are `evidence/animation-task-allocate-match.json` and
`evidence/graphics-reset-3e4f-match.json`. Fresh reproducers are retained beside
them as `animation-task-allocate-probe.py` and `graphics-reset-probe.py`.

The adjacent3B3A routine has a fresh complete789-byte REA dossier, retained in
`evidence/rea_animation_task_driver_3b3a.json`. Its framebuffer/huge-pointer
compositing logic is still being reconstructed; it earns no matching credit.

The3B3A compositor now also matches all789 bytes with C5.00 `/AS /Zi`.
`src/frame_compositor_match.c` describes eight-byte Frame records and the
observed32-byte blit prefix. Two huge-pointer additions remain left-associated,
preserving segment carries; combining their integer offsets changes emitted
instructions. All32 fixups, including the two absolute __AHSHIFT12 words,
match. The complete source/original MZ sets are empty.

The original reads a BP-relative word without an observed assignment and
stores it to the blit state. The source retains an uninitialized local to
reproduce that exact C5 machine behavior; the word's semantic purpose remains
unresolved. No initialized placeholder is introduced. Complete proof is
`evidence/frame-compositor-3b3a-match.json`, with a fresh reproducer
`evidence/frame-compositor-probe.py`. CODE is790 bytes: the final compiler90
collides with the next original procedure's55, so only the independently
bounded789-byte function earns credit. It still needs enclosing real source
context for a complete contribution.

## Complete enclosing source recovered

The preceding standalone790-byte compositor trial is retained as a negative
layout result. The canonical src/graphics_actor_full_match.c now joins the
actual adjacent empty, compositor and six actor/graphics helpers: all1,136 CODE
bytes at3B2E..3F9D match, with no tail conflict. See
 evidence/graphics_actor_full_match-contribution.json. The original unwritten
BP-word behavior remains preserved and its purpose remains unknown.
