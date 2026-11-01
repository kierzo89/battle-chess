# Exact C candidate validator AB58

[moves_validator_match.c](../src/moves_validator_match.c), compiled by pinned
MSC5.00 `/AS /Zi`, exactly reproduces the complete697-byte original span
AB58..AE10. The [fresh REA dossier](../evidence/rea_validator_ab58.json) establishes
a complete contiguous body. The independent CodeView3 procedure extent is697;
the [canonical production build proof](../evidence/validator_ab58_canonical_build.json) reports
`c_matched`, retains both complete byte sequences and source/object/tool hashes,
and verifies the complete original MZ relocation set in the span (empty).
No code masking, patches, assembly, byte emission or target-size trimming is used.

Integration preserves the canonical global bindings. The observed check-state
word at `9246 + 2*history_index` is expressed as
`check_state[history_index+1]` with the established base `9244`. The flag at
`CBD2` is named `finished`; the existing `input_state` symbol is a different
word at `9854`. The score and window at `8DE0` and `8B2C` use `best` and
`window_limit`. Runtime copy and existing callbacks use their shared names and
prototypes. A fresh complete build after these corrections still matches all
697 bytes. The earlier worker proof is retained as an experiment; the generated
canonical report supplies current source and object hashes.

The source expands the222-byte search frame into its observed18-byte prefix,
child depth and child-options fields, re-search flag, phase word and192-byte
principal-variation array. It initializes the candidate state, optionally
searches with swapped sides and a narrow/full bound window, restores the move,
services input/timer state, updates best/alpha and decides whether to re-search
or stop. These behavior labels are static inferences; no runtime execution or
historical variable naming is claimed.

The original saves a status local before returning constant1 in two branches.
The source retains those separate ordinary statements. The final interrupted
status instead uses the observed assignment expression on return. Calls pass
the eight-byte Move record and SearchOptions aggregate by value, reproducing
the original argument-push order; flattening the move argument into independent
scalars changes register allocation and is not used for this match.

The canonical unit now uses
[search_engine_a528_b5ea_full_match.c](../src/search_engine_a528_b5ea_full_match.c),
sharing these types and globals with fourteen adjacent functions. The complete
4,290-byte segment and all 404 fixups match in the
[full contribution proof](../evidence/search-engine-a528-b5ea-full.json).
The standalone proof remains a useful controlled precursor. Consolidation
receives no duplicate credit and does not establish historical module identity.
