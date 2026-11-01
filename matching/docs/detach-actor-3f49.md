# Exact C reconstruction of detach_actor at3F49

[detach_actor_match.c](../src/detach_actor_match.c) compiled by pinned MSC5.00
`/AS /Zi` reproduces all54 bytes at original image3F49..3F7E. The
[fresh REA dossier](../evidence/rea_detach_actor_3f49.json) establishes the
complete contiguous body, while the compiler independently emits a54-byte
CodeView3 procedure. [Full build proof](../evidence/detach_actor_3f49_build.json)
retains source/object/tool hashes, complete generated/reference bytes and
normal relocation arithmetic. No trimming, masks, patches, inline assembly or
source-byte emission is used.

The ordinary C function keeps its actor pointer in a register, calls3E81,
passes the actor's coordinates/color/frame and pointer to3F9E, then clears the
frame pointer at byte20 and square byte at11. The actor layout uses the28-byte
size corroborated by the independently reconstructed queue helpers. Other
padding fields remain explicitly unnamed. Static instruction evidence supports
these accesses; the exact drawing effects of the two callees remain inferred.

Proposal: `build/detach-actor-units.json`. Registry/checker are unchanged.
