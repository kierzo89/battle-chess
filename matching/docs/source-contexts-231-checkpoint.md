# Selection, board codecs and editor validation

Matching C totals **231 complete functions / 44,188 bytes**. This batch adds
five genuine procedures totaling 866 bytes: selection (123), validation (89),
board packing (121), dispatch/unpacking (195) and editor validation (338).
Reviewed caller declaration and name migrations preserve existing complete
CODE bytes. The observed extra-word animation call remains explicit without
inventing a historical prototype.

Initialized C DATA totals **104 contributions / 1,946 bytes**. One complete
16-byte UI scalar allocation replaces three contributions totaling the same
16 bytes. A real arena diagnostic adds 25 initialized bytes. The editor's
complete 213-byte compiler-owned CONST allocation is validated through the
existing single-owner backend and earns **zero separate DATA or matching-byte
credit**. The earlier two-owner literal pool of 112 bytes and selector CONST2
remain separate, deduplicated and uncredited. No constant pool is counted as a
second DATA contribution.

Four genuine COMMON objects still supply 25 definitions / 84 allocation bytes
with zero initialized or matching-byte credit. Assembly credit remains 11
functions / 994 bytes, one separate 95-byte CODE allocation with zero function
credit, and 896 DATA bytes. Runtime credit remains 4,240 bytes. Historical final
MAP, allocation order, compiler flags and translation-unit ownership remain
unproven.

## Verification and remaining work

All **397 current units** pass fresh native comparison.
**All 834 tests pass in one run with zero skips**, in 887.728
seconds, with 3514 unchanged input pins. Earlier regression
results retain their original scope. All 16 previous checkpoints retain
24,487 immutable archive paths, and all 48 prior versioned
source-link files remain unchanged, including the custom storage and C226 trios.

The current interface audit covers 165
syntax paths, with no actionable provided-definition type conflicts or duplicate
functions. All 59 CODE source paths pass the local-use
diagnostic. There are zero mismatched call names at currently provided native entries.

Original-file spans cover **49,347/83,415
(59.158%)**; expanded spans total
52,359/401,131. These are verified spans in distinct
coordinate systems, not whole-program completion. Verified MZ sites total
113/173; uncredited compiler-owned CONST loader sites remain excluded.

Actual aggregate LINK consumes 169 real
source objects plus SLIBC and LIBH, then fails with linker L2029 and **303
missing providers**. The undefined names agree exactly with the dependency
inventory. The failed partial executable remains unexecuted. No original target
bytes, stubs or object edits supply missing definitions. The layout audit retains
35 verified contexts,
13 CODE alignment constraints,
13 unequal CODE spans and
5 concrete byte collisions. The separate
[DATA audit](../build/231-source-contexts-preparation/outputs/DATA-alignment.md) checks 103
complete initialized allocations and records 7
DATA alignment constraints. Native and emitted DATA MZ sites are empty. It adds
no credit and does not prove the complete original global DATA map.

See [dependency findings](../build/231-source-contexts-preparation/outputs/findings.md), [actual LINK](../build/231-source-contexts-preparation/outputs/actual-LINK.json),
[diagnostic release](../build/231-source-contexts-preparation/outputs/release.json),
[regression coverage](../evidence/regression-231-source-contexts-coverage.json) and the
[immutable checkpoint](../evidence/verification-231-source-contexts-checkpoint.json).

The full-byte goal remains incomplete. Recover genuine missing providers,
settle source contexts and final allocations, independently link the complete
image with its original header and all 173 relocations, apply genuine EXEPACK,
and require every original file byte and SHA256. Matching emitted bytes does
not uniquely establish historical flags or translation-unit ownership.
