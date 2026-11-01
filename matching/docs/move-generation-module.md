# Contiguous C reconstruction of move-list generation

`src/move_generation_match.c` compiles with pinned Microsoft C 5.00 `/AS /Zi`
into a complete 418-byte CODE segment. It covers original image offsets
`9FDF..A180`: list append (50 bytes), promotion choices (52), and capture
candidates (316). Every segment byte belongs to those three compiler-reported
procedure extents; there are no holes, alignment bytes or original-code inputs.
All ordinary relocations are resolved and every byte matches the original.
The independent SEGDEF length and procedure offsets are retained with fresh
source/object/tool hashes in `evidence/move-generation-module.json`.

This was the initial three-function module experiment. The twelve-function
`src/move_engine_9a50_full_match.c` now supplies these canonical units as part of
an exact2692-byte CODE contribution; see [the larger module](move-engine-9a50.md).
The earlier sources remain investigation records and receive no duplicate credit. Internal
calls use the compiler's own segment references, removing external placements
between these three functions. This establishes a compatible contiguous module;
it does not prove these were the complete historical translation-unit contents.

REA's complete bodies agree with the compiler extents. At A011, the decompiled
pseudocode incorrectly replaces the loop increment with an address assignment;
the retained instruction stream clearly increments the local word and iterates
from two through five. The C source follows those instructions.

The A045 candidate generator uses an eight-byte move record, four-byte board
cells and two-byte piece records. Its bitwise boolean expressions preserve the
original evaluation and branch sequence. These types and behavioral names are
analyst reconstructions; byte matching does not recover historical identifiers.
