# Clock/history source-only continuation

The current source set verifies **214 complete C functions / 41,282 bytes** and
**103 initialized C DATA contributions / 1,984 bytes**. Eight new routines share
one genuine 274-byte compiler contribution with all 40 actual fields, two
compiler-resolved internal calls, complete native/CV spans, no tail and no MZ
words. The earlier pending five-function / 110-byte proposal is a subset and is
not credited separately. A separate initialized unsigned byte supplies the real
input-reset state with value 1; no neighboring gap is claimed as storage.

The existing timer consumer now uses the reviewed incomplete `timer_b` array
view. Its second consumed long is represented by the compiler's actual +4
addend, replacing the unbacked interior scalar alias. This preserves the complete
133-byte function, all actual operands and the honest 134-byte object ending in
an uncredited `90` byte. No historical array capacity or final layout is inferred.

## Validation scope

All **379 current matching units** pass the fresh strict checker.
The current interface audit covers 163 source paths,
with zero actionable provided-definition type conflicts or duplicate functions.
All 61 CODE source paths pass the host syntax/local diagnostic with
zero unread local declarations. The actual LINK uses 167 whole
source objects plus genuine SLIBC and LIBH, and fails with linker L2029 and
**356 unresolved providers**. The partial executable remains unexecuted.

**The 658-test suite was not rerun on 214.** Its zero-skip PASS belongs to the
immutable [206 checkpoint](huff-input-206-checkpoint.md), which supplies the core
regression baseline. Among those 844 input pins, only the reviewed registry and
`set_limit_match.c` consumer changed. All other 842 files, including core, tests,
tools and source-allocation configuration, remain unchanged. Current 379 native
byte checks, current AST/LINK proofs and the explicit timer controls validate
this source-only continuation. They do not imply a new 214 full-suite run.

The source-layout audit retains 33 verified CODE contexts,
16 enclosing-alignment cases,
15 unequal whole CODE spans and
7 concrete byte collisions. Original-file spans cover
46,441/83,415 (55.675%); expanded spans
cover 49,491/401,131. The existing MZ total remains 110/173:
107 C-source, one separate assembly-CODE and two runtime sites.
Assembly function credit remains 11 / 994 bytes, with a separate 95-byte multi-entry
CODE contribution; assembly DATA remains 896 bytes and runtime credit 4,240 bytes.

Three proposed long COMMON scalar definitions are retained as **unadmitted,
zero-credit evidence**. They are not LINK inputs or supplied providers. The
canonical source-allocation set remains the previous eight selector pointers;
BSS and COMMON allocations receive no matching-byte credit. Historical ownership,
allocation order and complete original MAP remain unresolved.

See [current dependency findings](../evidence/source-link-dependency-findings-214-clock-context.md),
[current LINK proof](../evidence/source-link-attempt-214-clock-context-final.json),
[current interface audit](../evidence/c214-clock-context-source-interface-audit.json) and
[immutable continuation record](../evidence/verification-214-clock-context-checkpoint.json).
Earlier checkpoint archives and all 30 versioned source-link files remain unchanged.

A complete independent executable remains absent. Recover missing providers and
real storage, resolve every source layout conflict and final allocation, reproduce
the original header/all 173 MZ and genuinely EXEPACK the independently linked image,
then compare every original file byte and SHA256. Full-byte matching is incomplete.
