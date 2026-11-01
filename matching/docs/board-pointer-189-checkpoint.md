# Board pointer:189 C checkpoint

One new genuine C function adds513 matching bytes, bringing the registry to
189 C functions /36,523 bytes. `src/error_pointer_match.c` contains the two
previous error-message helpers31/34B followed by the board-pointer routine513B.
Pinned Microsoft C5.00 `/AS /Zi` emits one complete578-byte CODE contribution
at imageD6E..FAF. All three CodeView extents cover every compiler byte, with
65 raw fixups and two original MZ relocations, checked at four load bases.
There are no compiler tails or other loaded allocations. Standalone pointer
CODE514 retains its actual90 tail, which conflicts with the next55 and earns
no credit. The natural combined source resolves that mismatch without trimming.

The routine maps pointer x/y coordinates through the board's row thresholds,
updates hover/selection outlines, and clears marks outside the board. Its two
automatic values and two used register locals naturally account for the8-byte
local frame; no unread variables or artificial helpers reserve stack space.
Unsigned selected/cursor/hover declarations preserve the full output and use
the existing dispatcher's view; historical storage signedness remains unknown.

The original analyzer reports only93 live bytes across94 and treats E0D as a
separate function. These observations remain preserved. Its missing DE6 byte
lies inside `MOV AX,0012` atDE5; E0D is an internal `JG`. Four apparent far-call
references actually target20DE6/20E0D after DOS relocation. The independently
expanded carrier has one contiguous513-byte function with44 closed reachable
CFG blocks, followed by a complete125-byte function with four closed blocks.
The strict fixed boundary gate validates original and expanded full638-byte
reads, all loader adjustments at F35/F64, the false-reference lists and decoded
instruction boundaries, complete fresh CV513 and all60 compiler fields. It
admits only this identity and reviewed source offsets0/65; it offers no general
span override. See [match proof](../evidence/board-pointer-0daf-match.json) and
[integration journal](../evidence/integrate-189-board-pointer.json).

The full394-test regression passed without skips before189 admission, in
672.182s, and is preserved in the
[188 ownership checkpoint](../evidence/verification-188-owned-data-checkpoint.json).
After admission, all16 new boundary tests and all16 PUBLIC-DATA tests pass.
The latter include an additional negative requiring each CODE PUBLIC to remain
outside DGROUP. The final full registry checker verifies all341 units. A new
full411-test suite was not run; the final tests target the changed gates, and
all registered original bytes are rebuilt and compared again.

Verified file spans total41,587/83,415B (49.856%); expanded spans42,994/401,131B.
These are byte-coverage measures, not whole-program completion. MZ sites total
61/173:59 source and2 runtime. An independent complete executable is absent;
`--require-complete` must still exit1. The full byte matching goal stays active.

The adjacent0FB0/102D candidates remain uncredited. Their genuine output is
124/54B versus original125/55B: zero local-frame bytes versus the original four.
C4.00 with valid K&R source, C5.00 and C5.10 reproduce that mismatch; used-local
and optimizer controls introduce additional differences. The whole756-byte
candidate retains all compiler output versus original758. Shifted post-frame
comparisons are diagnostics only. See
[negative controls](../evidence/board_coordinates_negative_controls.json).
