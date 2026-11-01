# Complete far min/max procedures

Ordinary C in `src/evaluation_minmax_probe.c`, compiled by pinned Microsoft
C5.00 with `/AS /Gs /Zi`, reproduces both complete31-byte procedures: max at
imageFE0C (CS0FDF:001C) and min at FE2B (CS0FDF:003B). Their fresh CodeView
lengths are31 each; together they cover the entire62-byte CODE contribution.
Neither procedure has fixups or an original MZ field. The source uses signed
comparisons and ordinary register parameters, with no embedded machine bytes.

Ghidra reports29 reachable bytes in each31-byte span because it omits a dead
two-byte short jump. Crediting only its reachable instructions would truncate
the compiler procedure. The separate `unreachable_forward_jump_gap_v1` proof
requires the exact far signed-comparison return shape, a closed four-block CFG,
and two jumps to the same shared epilogue. No CFG block or successor may enter
the gap. Separate global REA xref observations for both gap bytes must be empty.

Complete raw reads include the entire adjacent function, whose start, body
ranges, totals and span must agree. Max's adjacent min is itself noncontiguous;
the proof retains that observation. Min's adjacent parity helper is contiguous.
The fresh independent CodeView extent and complete linked bytes must match the
entire raw procedure. This narrow profile permits no general unaccounted gaps,
padding, truncation, masking or arbitrary extent expansion.

[evaluation-minmax-extent-proof.json](../evidence/evaluation-minmax-extent-proof.json)
retains complete bytes, OMF/compiler provenance and proof identities. Reproduce
with [evaluation-minmax-extent-probe.py](../evidence/evaluation-minmax-extent-probe.py).
Nine focused tests mutate the retained CFG, xrefs, raw bytes, adjacent-function
metadata, compiler extent and fixups. The canonical registry includes both
procedures, and `check.py` applies the full proof after fresh compilation.

These are complete function and contribution comparisons, not proof of the
original translation-unit identity or full executable layout. Automatic xrefs
describe the analyzed static graph; the independent compiler and adjacent-entry
evidence are also required. The full source-built executable remains unfinished.
