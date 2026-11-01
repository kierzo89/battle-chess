# Exact C reconstruction of queue_move at77AF

[queue_move_match.c](../src/queue_move_match.c), compiled by pinned MSC5.00
`/AS /Zi`, exactly reproduces every327 bytes at original image77AF..78F5.
The [fresh REA dossier](../evidence/rea_queue_move_77af.json) establishes the
complete contiguous body. The compiler independently emits a327-byte CodeView3
procedure. [Full build evidence](../evidence/queue_move_77af_build.json) retains
source/object/tool hashes, normal relocation arithmetic, and both complete byte
sequences. The final source was freshly rebuilt after comments were added.
No byte patching, masking, truncation or assembly/source-byte emission is used.

The function accepts an eight-byte move through a register pointer. For a
castling move, it recursively queues the original king movement using a local
ordinary move record, then queues the corresponding rook movement. It converts
board squares to display-board positions, detaches the relevant28-byte actors,
and calls7AA7 with the mapped piece kind, display color, actor index and source
square. A special pawn move clears the captured actor on the intermediate row.
These are static behavior inferences; no runtime execution is claimed.

The original checked allocation is18 bytes. The observed accesses use an
eight-byte move record and two byte locals in compiler word slots; six frame
bytes have no observed reads or writes. Three unused ordinary `int` locals
express that observed allocation in the reconstruction. Their names and
historical purpose are unknown; no claim is made that these were the original
source declarations. Their values are never read. The source stays within the
ordinary-C policy and lets the independent historical compiler generate all
frame instructions and offsets.

The self-recursive call is linked through the object's own code-segment target.
External placements identify actor/cell tables and the independently
reconstructed7AA7 helper. Proposal: `build/queue-move-units.json`. Canonical
registry and checker remain unchanged by this worker.
