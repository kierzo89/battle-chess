# Bounded bit-count frame/lifetime control

Fresh REA on original CHESS confirms the complete48-byte far function at image1094C..1097B allocates4 stack bytes, uses only BP-4 for its counter, passes the input parameter directly to parity, and tests the returned AX directly. BP-2 has no observed read/write in this function. Decompiler locals do not establish the original source declarations.

Six fresh genuine C5.00 `/AS /Gs /Zi` source variants start from the unread-local-free evaluation source. All retain full source, pinned compiler provenance, raw OMF object/fixups, complete independent CodeView boundaries, complete linked/original bytes and exact negative positions in `evidence/bitcount-lifetime-control.json`. New REA dossier: `evidence/rea_pawn_bitcount_frame_control.json`. Reproducer: `build/bitcount-lifetime-control/probe.py`.

| Meaningful source form | Frame bytes | Function bytes |
| --- | --- | --- |
| Explicit parity-result local consumed by condition |4|51|
| Register parity-result local consumed by condition |4|52|
| Block-scoped parity-result local consumed by condition |4|51|
| Accumulate boolean call result |2|50|
| Equivalent for loop with shift iteration expression |2|50|
| Accumulate conditional expression `call?1:0` |2|50|

No variant matches the complete original48 bytes. Explicit live parity objects explain a real4-byte source frame, but retain store/register operations absent from original. Expression variants do not establish an extra compiler-generated frame temporary. All source objects have meaningful dataflow; no unused padding locals were introduced.

For enlarged variants the complete natural object layout changes. Linking uses natural imageFDF2 plus each actual PUBDEF offset, and comparisons retain these placement differences; no function is moved back to a convenient original address. CODE becomes3904 or3906 bytes, versus original matched baseline3902. These are diagnostic negatives with zero restored credit. The separate unread `e` removal remains in every probe; candidate therefore remains negative independently. Own REA original session was closed after saving evidence. Canonical sources, registry, policies and tests remain untouched.
