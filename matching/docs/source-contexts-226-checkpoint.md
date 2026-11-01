# Poll input and compiler-owned literal context

Matching C now totals **226 complete functions / 43,322 bytes**, including the
new genuine 380-byte poll-input function. Reviewed caller migrations preserve
their existing complete CODE bytes; an observed legacy unprototyped one-word
call remains explicit without inventing a historical prototype.

Initialized C DATA totals **105 contributions / 1,921 bytes**. The UI storage
context adds 11 bytes relative to its replaced contribution, and dialog state
adds six bytes. Six formerly separate asset-string arrays totaling 112 bytes
are retired. Their actual compiler-owned literal pool remains in one genuine
object, with two independently validated owners, complete 1,036-byte CODE,
89 actual fields and three native CODE MZ sites. Its complete 112-byte CONST
allocation earns **zero separate DATA or matching-byte credit**. The net credited
DATA change is minus 95 bytes; no literal bytes are counted twice.

Four genuine COMMON objects still supply 25 definitions / 84 allocation bytes,
with zero initialized or matching-byte credit. Assembly credit remains 11
functions / 994 bytes, one separate 95-byte CODE allocation with zero function
credit, and 896 DATA bytes. Runtime credit remains 4,240 bytes. Historical final
MAP, allocation order, compiler flags and translation-unit ownership remain
unproven.

## Verification and remaining work

All **393 current units** pass fresh native comparison.
**All 834 tests pass in one run with zero skips**, in 867.346
seconds, with 3216 unchanged input pins. This is a fresh
regression after promotion of the literal-ownership gate. All 15 previous
checkpoint archives retain 21,160 immutable paths, and all
45 previous versioned source-link files remain unchanged.

Current interfaces cover 164 syntax
paths with no actionable provided-definition type conflicts or duplicate
functions. All 57 CODE source paths pass the local-use
diagnostic. No mismatched call names remain at currently provided native entries.

Original-file spans cover **48,481/83,415
(58.120%)**; expanded spans total
51,468/401,131. These are verified spans in distinct
coordinate systems, not whole-program completion. Verified MZ sites total
113/173: 110 C,
1 separate assembly CODE and
2 runtime. Uncredited compiler-owned CONST
loader sites remain excluded from matching credit.

Actual aggregate LINK consumes 168 source
objects plus SLIBC and LIBH, then fails with linker L2029 and **307
missing providers**. Its undefined names agree exactly with the dependency
inventory. The failed partial executable remains unexecuted. No original target
bytes, stubs or object edits supply missing definitions. The layout audit retains
33 verified contexts,
13 CODE alignment constraints,
13 unequal CODE spans and
5 concrete byte collisions. The separate
[DATA alignment audit](../build/226-source-contexts-preparation/outputs/DATA-alignment.md) checks complete initialized
104 allocations and records 8 DATA alignment constraints; native and emitted
DATA MZ sites are empty. It adds no credit and does not prove the complete
original global DATA map.

See [dependency findings](../build/226-source-contexts-preparation/outputs/findings.md), [actual LINK](../build/226-source-contexts-preparation/outputs/actual-LINK.json),
[diagnostic release](../build/226-source-contexts-preparation/outputs/release.json),
[regression coverage](../evidence/regression-226-source-contexts-coverage.json) and the
[immutable checkpoint](../evidence/verification-226-source-contexts-checkpoint.json).

The full-byte goal remains incomplete. Recover genuine missing providers,
settle source contexts and final allocations, independently link the complete
image with its original header and all 173 relocations, apply genuine EXEPACK,
and require every original file byte and SHA256. Matching emitted bytes does
not uniquely establish historical flags or translation-unit ownership.
