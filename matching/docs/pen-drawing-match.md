# Pen movement and integer line drawing

`src/pen_drawing_match.c` compiles with Microsoft C 5.00 `/AS /Zi` to the complete
24-byte move routine at5B3D and 310-byte line routine at5B55. The two functions
emit all334 CODE bytes at5B3D..5C8A without padding. All30 fixups, complete
CodeView extents, contiguous REA bodies and original bytes match. Both original
and emitted MZ relocation sets are empty.

The line routine is an integer Bresenham rasterizer. It obtains absolute deltas
and signs, follows the dominant axis, updates an error term, and invokes the
near plotting callback with both coordinates. The reconstructed C preserves
all indirect calls and the original final pen-position updates. REA's initial
pseudocode loses arguments around indirect calls; the raw instructions and
complete byte comparison establish the actual call sequence.

The original contribution starts at an odd address despite WORD-aligned CODE.
It still requires genuine enclosing source before a full link. The preceding
pen-colour selector has not matched: ordinary far-pointer reconstruction trials
emit different instructions. The following sign helper has a non-contiguous
reachable body and currently has no accepted complete-extent proof. Neither
receives matching credit. No boundary or byte is trimmed to conceal these gaps.

See `evidence/pen-drawing-match.json`,
`evidence/pen_drawing_match-contribution.json` and the retained REA evidence.

## Complete sign helper now included

Canonical src/pen_drawing_sign_match.c now contains the move and line routines
plus the42-byte sign helper at5C8B: all376 emitted CODE bytes at5B3D..5CB4 match.
There are31 fixups and no MZ sites. The original odd start still needs enclosing
source context. The earlier334-byte source remains retained as a historical
control; its former unproved-sign limitation is now resolved.

The signed_signum_return_gaps_v1 validator is restricted to this exact C5 unit,
profile, symbol, address and42-byte extent. It requires all instructions, the
single compiler stack-probe fixup, all six closed CFG blocks, three reachable
ranges, and four distinct empty global xref results for the two dead jumps.
Its raw span must also contain the complete147-byte adjacent copy routine,
authenticated by an independently pinned original digest. Every sign instruction
and every mandatory adjacent context byte has a mutation rejection test.
Original code execution agrees with ordinary C for all65,536 signed inputs.

The selector5B18 remains uncredited after bounded C4/C5 formulation/profile
controls; see pen-selector-extension-control.md. A separate147-byte C match
now reconstructs copy5CB5, preserving huge-pointer carries. Its emitted final
NOP conflicts with the original5D4855 and earns no credit. See
 evidence/copy-region-match.json. Current whole pen proof is
 evidence/pen_drawing_sign_match-contribution.json.
