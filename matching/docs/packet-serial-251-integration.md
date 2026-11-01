# C251 packet and serial integration

The packet context adds five genuine C functions totaling 813 bytes and retains
an existing 42-byte reset function. All six functions compile together in a
complete 856-byte CODE contribution: 855 function bytes and one native alignment
byte that earns no C credit. Microsoft C 5.00 with `/AS /Zi` reproduces this
context. The receive buffer's 39-byte minimum is consumed by valid binary input;
its 42-byte frame includes a used pointer home and compiler WORD rounding.
Historical buffer capacity and safety of the native unbounded ASCII path remain
unproved.

A genuine initialized `unsigned char refresh_stop_11a6 = 0` supplies one missing
DATA byte. The actual canonical 417-unit checker passed all comparisons:
251 C functions / 47,218 bytes, 104 C DATA contributions / 1,978 bytes, and
52,402 verified original-file bytes. See the preserved
[417 checker record](../evidence/checker-251-packet-data.json).

The serial extension adds one complete 182-byte assembly CODE contribution,
assembled by authentic Microsoft MASM 5.10 with `/Mx`. Its two public entry
points, internal interrupt body and saved-DS word belong to one allocation.
All 17 OFFSET16 fields and four load-base comparisons must verify. This earns
zero C, ordinary assembly-function or separate DATA credit. The field at offset
150 uses the actual empty `_DATA` frame; its equality with DGROUP in the native
comparison is a layout constraint, not a proved global linker map.

The canonical serial, existing Huffman allocation and packet tests pass together:
142 tests, zero skips. The fresh global comparison passes all 418 units with zero failures. Verified
original-file spans total 52,584 / 83,415 bytes (63.039%); expanded-image spans
total 55,628 / 401,131 bytes. The checker still rejects `--require-complete`,
as expected, because no complete independent executable exists. All 1,130 tests
are discovered with zero import errors; the full regression remains pending.
See the [418 checker record](../evidence/checker-251-packet-serial.json). The [serial admission record](../evidence/integrate-251-serial182.json)
records the exact reviewed changes. The [C246 checkpoint](named-display-246-checkpoint.md)
remains the durable complete regression: 1,032 tests passed with zero skips.

A full source-built executable is still unavailable. Missing storage providers,
whole-program segment order, the DOS header, all 173 MZ sites and final
source-built EXEPACK output must be established before claiming a complete match.
Compiler and assembler settings reproduce the admitted contributions but do not
prove unique historical command lines or source file grouping.

The actual aggregate LINK consumes 177 real source objects and fails with L2029
for 263 missing providers. Seven names are supplied since C246; the serial module
introduces the real `_serial_ring_end_2eba` and `_serial_irq_flags_b0d4` storage
requirements. Source checks find zero actionable provided-type conflicts, duplicate
function bodies or provider aliases. Of 63 C CODE contexts, 40 match completely,
12 need enclosing alignment and 13 have unequal whole spans; these categories
can overlap. All 103 physical initialized DATA contributions match completely,
but their global order is unproved. Seven COMMON objects allocate 47 definitions
and 134 bytes with zero matching credit.
