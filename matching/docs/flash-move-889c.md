# Exact C reconstruction of the move-flash helper

The complete 160-byte function at image `889C` now matches ordinary C compiled
by pinned MSC5.00 `/AS /Gs /Os /Zi`.
[Source](../src/flash_move_match.c), [fresh full build record](../evidence/flash_move_889c_build.json),
and [fresh REA body evidence](../evidence/rea_frame_next_1889c.json) retain the
independent source/object/tool hashes, CodeView3 extent, every byte and normal
relocation arithmetic. The original was used only for comparison and symbolic
placement evidence, with no output patches or target-size trimming.

The function checks the low byte of the fourth move word. If nonzero, it
transforms the first two squares by flipping their row bits, flashes both
squares twenty times using signed remainder modulo six plus two as the color,
waits two timer units between calls, then clears both highlights. It calls
image543A and941B. No runtime execution was inferred from the static evidence.

The initial source already emitted160 bytes, but three stack slots differed.
Declaration permutations did not change allocation in this compiler. Renaming
the three ordinary locals to `a`, `b`, and `c` reproduced the original allocation
(source square at BP-2, iteration at BP-4, destination square at BP-6). Those
names have no recovered historical attribution; comments identify their roles.
The final standalone source was freshly compiled and compared in full after
that change. No synthetic register/frame manipulation was introduced.

A separate fresh dossier for `872A` exposes236 instruction bytes in a266-byte
span with a30-byte internal jump table. The checker currently expects contiguous
REA function bodies, so this investigation claims no match for that function.
Its retained evidence is [rea_frame_next_1872a.json](../evidence/rea_frame_next_1872a.json).
