# Register qualification of existing live ray-initializer values

A bounded follow-up uses retired `init_rays_9840`, whose original complete185-byte body already saves SI and DI. Current source has exactly three meaningful locals: direction index, inner-loop index, and current Ray pointer. No object or type is added; each register trial qualifies only an existing live value. The original retained REA evidence is `rea_init_rays_9840.json`.

| Source control, all C5 AS/Zi | Frame bytes | Procedure bytes | Complete CODE bytes | Original differences |
| --- | ---: | ---: | ---: | ---: |
| Current unread-free baseline |6|185|186|12|
| Same declarations split, no register hint |6|185|186|12|
| Existing direction index qualified register |8|183|184|156|
| Existing Ray pointer qualified register |8|189|190|123|

Both register hints cause the original eight-byte reservation while preserving the original SI/DI save set, without any added source objects. This is positive evidence that qualification/allocator policy can enlarge the reservation. The split-declaration control reproduces the baseline complete CODE exactly, excluding mere declaration splitting as the cause.

Neither complete procedure matches. Promoting direction_index puts the counter in SI and changes loop instructions that the original performs through BP-8. Promoting the entry pointer holds it in SI and changes its address calculation and memory accesses; the original stores and reloads entry through BP-2. The original's two counters and pointer remain frame-based in the retained assembly. The extra allocation alone therefore cannot identify a historical register declaration or restore matching credit. No particular reserved word is asserted to be a decoded source-object home: internal allocator/spill details remain inferred from controlled output differences.

The complete emitted CODE segments, including final NOPs, remain unsliced and uncredited as enclosing contributions. `evidence/existing-register-frame-control.json` retains all four ordinary sources, source/tool/object hashes, compiler logs/commands, full independent CV extents, all CODE and full linked/original bytes, raw and resolved fixups, every differing position, and complete empty MZ-set equality. Reproducer: `build/existing-register-frame-control/probe.py`; supplying a control name repeats just that row.

Zero new matching credit. Frozen nine-control evidence from the preceding scope is unchanged. No canonical source, registry, core, policy or test file was edited. This scope reused retained original REA; no session or mutable metadata was opened.
