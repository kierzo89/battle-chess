# BB0E next-stage checkpoint

This is read-only reverse-engineering preparation. No C source, compiler extent, proposed unit, or matching credit is asserted for BB0E.

REA observes **one contiguous 3,371-byte body at image BB0E..C838**, not the legacy inventory's 2,547 bytes. The complete retained dossier has 197 CFG blocks and 1,379 decoded instructions; its high p-code reports no truncation or omitted operations. A separate 3,393-byte REA read, BB01..C841, matches the original EXE and independently unpacked unchanged prefix byte for byte. The next known entry is C83A. C839 is a separate `90` alignment byte; BB0D is another `90` between the already matched twelve-byte BB01 function and BB0E. Neither byte belongs to the observed function. No disjoint ranges, switch tables, CALLF instructions, FPU instructions, or interval MZ relocation sites were observed.

The raw epilogue C833..C838 is `5E 5F 8B E5 5D C3`. The routine saves DI/SI and requests a 42-byte frame from `__chkstk`. A future independent MSC5 CV3 procedure must establish its actual generated extent; REA's 3,371-byte body is not a compiler match.

## Behavior supported by the instructions

This routine constructs a move-animation command sequence and then waits for completion while polling input. It returns a word in AX. The animation description is inferred from board-square conversion, piece-specific paths, the command queues, and the final input/completion loop; exact command-opcode names still need recovery.

1. BB19 onward sets byte9852. When `modes[current_side] == 2`, the byte11B3 latch and the final argument decide whether to call DFAC with the address of the by-value move. DFAC's record-move role is already used by `finish_move_match.c`.
2. BB56..BC5D handles special moves recursively. There are two recursive call sites, each pushing four move words plus a final zero and cleaning ten stack bytes. The pawn case constructs a move whose first square is `(move.word1 & 0x70) | (move.word0 & 7)`, with flag0 and kind/capture6/6, then adjusts the original stack copy. The other special case first animates the underlying move, then rewrites the local move's squares and kind3 to handle a rook-like secondary move. These are consistent with en passant and castling, respectively; retain the observed field operations rather than trusting the decompiler's informal types.
3. BC5E onward converts both 0x88 squares into 0..63 screen squares with `(((square >> 1) & 56) ^ 56) | (square & 7)`. It tests for an unchanged square, counts a path for captures, or uses the sentinel200 for the longer sequence. Direction bytes use row mask38 and file mask7.
4. BD21 onward creates or appends command records. Kind3 and kind5 receive special path setup; kind6 remaps two directions. Several long opcode sequences repeat around a short-path threshold. The main traversal advances one rank/file step at a time and queues commands for intermediate occupancy and the destination.
5. C7F5 onward initializes a returned-key word to0, calls 8AAA with1, clears byte0DA6, then calls0254 until0DA6 becomes nonzero. It remembers nonzero input values whose F000 bits are clear. At C829 it clears byte9852 and returns the remembered word. Transitive callback/timer behavior that changes0DA6 was not analyzed here.

## Argument and local layout

The most useful candidate source ABI is `unsigned function(Move move, int suppress_record)`, with a real eight-byte Move passed by value. The extra argument name is inferred. Raw BP offsets are definitive:

| BP displacement | Observed contents |
| --- | --- |
| +4, +6, +8 | move's first square, second square, special flag |
| +10/+11 | move kind/capture bytes |
| +12 | final word tested before recording |
| -26 | near pointer to the stack Move, initialized with `&[BP+4]` |
| -36..-29 | temporary eight-byte Move for recursive calls |
| -14 | result word, also reused during special-move preparation |
| -38 | polled key word |
| -22 | path/threshold counter, initialized0 or200 |
| -2 | word selecting begin versus append behavior |
| -6, -8, -28 | screen-square/path bytes |
| -18, -20, -24 | command handles and intermediate handle bytes |
| -40 | direction byte0..7 |
| -10, -12, -16, -42 | additional occupancy/type/state bytes; exact roles need assembly-led naming |
| -4 | saved traversal byte |

Ghidra's `Stack[-...]` local labels are offset from its own convention and should not replace these raw BP displacements. Its five word parameters are the flattened representation of Move8 plus a final word. The long pseudocode also loses argument pushes and variable identities around command calls; it is not reliable source text.

## Dependencies and calling convention pitfalls

All calls are near. Counts from the complete body:

| Target | Calls | Actual caller cleanup |
| --- | ---: | --- |
| 5FBD | 59 | 53 calls clean8B; six calls clean10B |
| 60D3 | 5 | every call cleans6B |
| BB0E | 2 | every recursive call cleans10B |
| DFAC | 1 |2B |
| 8AAA | 1 |2B |
|0254 |1 | no arguments |
| ECAA |1 | stack-probe ABI |

Fresh complete dependency dossiers establish that5FBD appends an eight-byte command to a linked queue at DGROUP52F0, and60D3 starts one. Byte04BC is a modulo32 allocation cursor, link fields useFF, and byte984F records the new root. They also touch cells1166, per-piece flags0EC5, and capture-kind bytes0ECC/0ECD. Their decompiler signatures read five and four byte-valued stack parameters respectively, while BB0E demonstrably supplies only four/five and three words. Extra trailing fields are command-dependent, and some stored trailing bytes may come from stack positions that callers do not supply. Do not silently add arguments to every call: that changes the original bytes. Before reconstruction, recover command-specific reads and use a faithful C5 ABI model, potentially typed minimum arguments plus a variadic tail. No final prototype is established by this checkpoint.

The trailing read is unconditional in both retained helper bodies: append5FBD
copies `[BP+0C]` into command byte+6, and begin60D3 copies `[BP+0A]` into byte+6.
Thus command-specific consumption of that stored field must be distinguished
from whether the helper itself reads it. A variadic declaration alone does not
make reading an absent argument defined C behavior. The original may rely on
an unprototyped variable-argument convention or an ignored indeterminate field;
this remains an ABI/source-recovery question, not permission to invent a zero
argument or silently change the caller pushes.

There are no direct FPU/helper arithmetic dependencies in BB0E. Only the stack probe is a direct runtime dependency. Input and command handlers have their own transitive dependencies, which this checkpoint does not claim to exhaust. The CS0FDF evaluation reconstruction is unrelated to this scope.

## Ordinary C reconstruction plan

Start with MSC5 `/AS /Zi`, Move8 with the canonical union kind/capture member, a near pointer to the actual by-value parameter, byte locals, the eight-byte recursive temporary, and the raw42-byte frame target. Preserve integer promotions, byte truncations, signed comparisons, and the exact declaration/name-dependent local allocation. Give the recursive function its real Move8-plus-word prototype.

Recover and annotate each command call from pushes and ADD SP, rather than copying Ghidra's changing argument counts. Establish command-opcode argument usage in5FBD/60D3 before choosing declarations. Then reconstruct the recursion/recording prefix, screen conversion/path setup, command chains, traversal, and final polling loop as one complete ordinary C function. Helpers can be analyzed first, but extracting chunks into new C functions would change this function's call/control-flow bytes.

Compare an entire independently emitted CV3 extent against BB0E..C838. If the compiler emits3,372 bytes with a trailing alignment90, credit only the independently established function body and document the segment context; do not infer the boundary from the desired target length. A complete match also needs the empty interval MZ relocation set and full reference-byte equality. No current source or proposal has been prepared.

## Retained evidence

- `evidence/rea_moves_stage_bb0e.json`: complete function dossier and CFG.
- `evidence/rea_moves_stage_bb0e_raw_context.json`: complete raw context through the next entry.
- `evidence/rea_moves_stage_bb0e_command_5fbd.json`: complete254-byte append helper.
- `evidence/rea_moves_stage_bb0e_begin_60d3.json`: complete148-byte begin helper.
- `evidence/rea_moves_next_c83a.json`: next function entry/body.
- `evidence/moves-stage-bb0e-checkpoint.json`: independently checked hashes, ranges, call/cleanup inventory, empty MZ set.
- `build/bb0e-stage.asm`: convenient assembly extraction; the retained REA JSON remains authoritative.
- `build/bb0e-checkpoint.py`: reproduces the raw-context/hash/boundary/call inventory checks.

## Matching checkpoint

The complete3,371-byte procedure now matches ordinary Microsoft C5.00
`/AS /Zi` in `src/animation_stage_match.c`. Fresh canonical production proof
is `evidence/animation-stage-canonical-migration.json`; the detailed ABI, all70
calls,94 fixups and independent3,371-byte CV extent are retained in
`evidence/animation-stage-bb0e-match.json`. Whole emitted CODE3,372 bytes also
matches; its final90 alignment byte remains outside function credit.
The canonical `_capture_types_11ac` name distinguishes this actual global
from another source global at DGROUP0F00. Missing original trailing call
arguments remain preserved. The earlier read-only checkpoint above is historical.
