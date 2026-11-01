# Exact C reconstruction of candidate generator A348

[generate_match.c](../src/generate_match.c), compiled with pinned MSC5.00
`/AS /Zi`, exactly matches the complete396-byte original function at image
`A348..A4D3`. The fresh CodeView3 procedure extent independently reports396
bytes; [fresh REA evidence](../evidence/rea_engine_a348.json) establishes the
same complete contiguous body. [Full build proof](../evidence/generate_a348_build.json)
retains the source/object/tool hashes, compiler command, all396 generated and
expected bytes, and every ordinary relocation. No code was patched, masked,
trimmed or inserted through assembly/byte-emission source.

The source resets the generated-list count/index, visits live opponent piece
records through A045, tests two castling candidates with9DB3, visits current
side piece records through A181, and handles the two neighbor candidates after
a previous long pawn move. Valid special candidates are appended through9FDF.
The8FB5 absolute-value helper supports the prior-move distance check. These are
static behavior inferences; no runtime execution is claimed.

The data declarations independently express the observed sizes and fields:
eight-byte move records,32-byte side piece tables, and a2-by2 table of four-byte
castling source/destination pairs. The final loop uses a signed square index
and the0x88 board-boundary test. The midpoint division is signed C division,
which emits the original CWD/SUB/SAR rounding sequence.

Three ordinary locals reproduce the observed stack allocation. The explicit
initial assignment of6 to the later castling-index local preserves an original
store which this default compiler leaves even though that value is replaced
before the loop; no historical variable name or reason for that redundant
initialization is claimed.

The final standalone source was freshly recompiled after documentation comments
were added, and every byte still matched. Canonical registration proposal:
`build/generate-a348-units.json`. Registry, checker and next-work were untouched.
