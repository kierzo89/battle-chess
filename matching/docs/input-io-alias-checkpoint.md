# Input, byte I/O and call-name reconciliation

This checkpoint adds five ordinary C procedures totaling533 bytes: four byte-I/O
routines at DBB5..DCC9 (277 bytes) and a complete256-byte text-input helper at
1064..1163. Microsoft C5.00 `/AS /Zi` generates every complete procedure. The
registry separately includes the one-byte initialized input-active flag. There
is no new ASM credit in this checkpoint.

## Source naming and prototypes

Thirteen provisional call aliases now use the matched callee's definition name.
Six changed sources contain49 credited functions; independent fresh compilation
preserves all49 complete original bodies. The migration also makes the
animation-stage return unsigned, makes the low-bit parameter/result unsigned,
and uses a correctly typed byte-fill pointer conversion. The former
`draw_progress` call is the far `evaluate_full` call at0FDF:0069, corroborated
by original raw `9A6900DF0F` atA55C and the complete native search dossier.

All original zero/one-word shutdown calls are preserved through the existing
old-style declaration. No argument is added or removed to manufacture a match.
Their historical prototype, and variable argument counts at the command
append/begin interfaces, remain unresolved. This is naming/type reconciliation,
not a claim to recover original identifiers or establish a full source link.

`c-call-alias-migration-experiment.json` retains all new source text, original
hashes, compiler/tool/object provenance, complete generated functions and
fixups. `c-call-alias-migration-before.json` preserves the exact source versions
before cleanup. Unused comparison-binding aliases are merged only when their
addresses agree. The final fresh call inventory checks the resulting names
against actual encoded near/far call operands and current body hashes.

## Complete text-input source

`text_input_match.c` matches its entire256-byte CODE segment, all ten fixups and
the empty MZ-site set. Its WORD alignment is satisfied and there is no compiler
tail. The editor keeps the actual two-byte length local, uses register x/y
parameters, edits the caller's buffer and updates the activity flag. No unread
padding locals, assembly or target-dependent output slicing are used.

Packed-file Ghidra analysis created a false entry at10D3 inside the immediate
of `AND AX,F000`. Authenticated full expanded-image analysis recovers the
complete native256-byte body and18 closed reachable CFG blocks. The fixed
`text_input_expanded_1064_v1` policy requires both original/expanded562-byte raw
contexts, the full next306-byte procedure, all eight false far-reference sources
and loader arithmetic, the independently decoded AND/interior addresses, and
the complete fresh compiler extent/fixups. Seventeen mutation tests challenge
these requirements. See text-input-1064-boundary.md; ordinary extent rules are
unchanged. Build-unit equality alone did not earn canonical credit before this
boundary review passed.

The actual activity set/clear operands are bytes. The typed `unsigned char`
zero initializer is independently compiled
and compared with the full one-byte REA expanded read at DS0055. It receives
one DATA byte and no compressed-file/function credit. Historical source
ownership and final source-link placement are still unknown.

## Byte I/O

`byte_io_flow_match.c` rebuilds write46, read156, discard18 and availability57.
The writer calls the actual far target10D3:00B6; the reader uses the real
time-call ABI with two used32-bit locals for an eight-second deadline and a
128-byte ring wrap. The availability routine's genuine result local preserves
the original57-byte body; the shorter ternary-return candidate remains a
negative control. Only the original segment relocation atDBD6 is credited.

Its278-byte complete CODE segment retains an unequal final NOP outside the
277 procedure bytes. The odd originalDBB5 start still needs genuine enclosing
WORD-aligned source context; neither compiler tail nor alignment is hidden.
See byte-io-flow-experiment.json and byte-io-flow-findings.md.

An independent authentic LINK control executes all four routines with the two
real output wrappers and28 real DATA bytes. The complete278-byte compiler CODE
segment, wrappers, DATA and MZ sets agree with each newly linked executable.
The real-clock fixture independently relocates and verifies the complete87-byte
SLIBC TIME member, then tests output order, ring wrap, guarded reads, availability,
discard and zero counts. A separate controlled-clock fixture forces0/4/8 seconds
to exercise the deadline branch. Its clock and far byte collector are explicit
harness code. Original files are neither read nor mounted; synthetic COMMON
definitions and map placements grant no historical storage or matching credit.
See byte-io-authentic-link-experiment.json and byte-io-authentic-link-findings.md.

## Remaining source questions

The6CB4 routine remains uncredited. Original raw evidence contains unusual
NOP/dead-jump sequences consistent with a validation patch, while the original
provider's decompiler fails on its control flow. This is a bounded inference,
not an assertion that a particular crack or original compiler is identified.
The complete source/required ASM and genuine native boundaries still need work.

Expanded REA also recovers main0010's575-byte reachable native body. A separate
uncredited ordinary C probe emits580 complete CV/CODE bytes identical to the
original, with the exact original MZ sites. Its additional five bytes are the
compiler's unreachable epilogue, also present verbatim in the original. All
four locals have actual argument-index/key/coordinate uses. Local names affect
this compiler's frame allocation: the descriptive-name control differs at13
local displacements; a/b/c/d produce the original frame without padding locals.
Historical identifiers remain unknown. Full original/expanded raw and native
epilogue/next-body/xref proof and a strict mutation-tested boundary policy remain
required before canonical credit. See main-0010-full-extent-probe.json.

Bit-count lifetime controls also remain negative: useful parity temporaries
create real four-byte frames but add instructions, while expression variants
keep two-byte frames. None restores the withdrawn48-byte function. See
bitcount-lifetime-control.md. The fourteen earlier padding-dependent routines
remain uncredited. Full independent linking, all storage placements/header/MZ
sites and source-built EXEPACK output are still required for the full-byte goal.
