# Complete 2692-byte C engine contribution

`src/move_engine_9a50_full_match.c`, compiled with pinned Microsoft C5.00
`/AS /Zi`, reproduces the complete original region9A50..A4D3. All twelve
independent CodeView procedure extents are contiguous and cover every byte of
the declared2692-byte CODE SEGDEF. The contribution begins at an even address,
matching its word-alignment requirement; there are no holes or alignment bytes.
Fresh source/object/tool hashes, fixups, exact bytes and full-segment checks are
retained in `evidence/move-engine-9a50-full.json`.

The canonical registry now builds attacked-square checking, castling flags,
original-piece checking, quiet-move checking, count/repetition helpers, move
legality, list append, promotion choices, capture/quiet candidate generation
and the candidate dispatcher from this one source. Shared declarations express
the actual eight-byte Move representation, its two-byte kind/capture union,
four-byte board cells and two-byte piece entries. The far castling helper is
defined in the same translation unit, preserving the compiler's four-byte
PUSH CS/CALL near sequence in legality checking. Most calls between these
functions now resolve through compiler-emitted internal segment references.

The existing repetition-gap and inline-switch proofs still validate their
complete independently emitted extents, now at nonzero object offsets. Neither
omitted region is trimmed or masked. This consolidation adds no duplicate byte
credit; all twelve functions already matched independently.

An intermediate five-function source covered1269 matching procedure bytes,
but its SEGDEF was1270 bytes because of end alignment. That extra byte was
not accepted as a match or a full contribution. Extending the reconstruction
to9A50 accounts for a complete even-sized contribution without target-size
truncation. The earlier418-byte three-function experiment remains valid as a
standalone output comparison; its odd target placement did not establish a
historical object boundary.
The negative five-function experiment is reproducible from
`src/move_generation_full_match.c`; its fresh source/object/tool pins and
uncredited alignment byte are in `evidence/move-generation-1269-padding.json`.

This is a compatible reconstructed CODE contribution, not proof that9A50 was
an original translation-unit boundary. A whole-program link must still provide
the preceding/following code, external data and functions, true group ordering,
MZ relocations and final packing. No reference-derived code skeleton is used.
