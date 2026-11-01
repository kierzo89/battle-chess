# C240 source-context checkpoint

The goal remains exact reproduction of the original 83,415-byte CHESS.EXE from genuine source. A complete independent executable is still absent.

This checkpoint verifies **240 complete functions / 45,166 bytes**, **97 C DATA contributions / 1,881 bytes**, 11 assembly functions / 994 bytes, a separate complete 120-byte assembly CODE contribution, 896 assembly DATA bytes, and 4,240 reviewed runtime bytes. All 399 matching units pass. The required complete-executable check exits 1 because the full executable remains unmatched.

All 933 tests pass in one run, in 902.283 seconds, with zero skips. Their exact IDs, interpreter, unchanged direct input hashes and log are retained in the regression coverage record. Earlier interrupted C233 attempts remain historical non-PASS evidence; this is a new complete C240 run.

Seven genuine C procedures add 736 C bytes. The assembly source-window contribution grows by 25 bytes without adding function credit. One complete typed 61-byte dialog DATA contribution replaces a 10-byte filename contribution: net initialized DATA increases by 51 bytes. Six source-only COMMON objects provide 30 definitions / 94 allocation bytes, with zero initialized-byte or matching credit. Historical storage order, translation-unit ownership and compiler flags remain nonunique.

Verified original-file spans total 50,350 bytes (60.360846%); verified expanded-image spans total 53,297 bytes. These are span coverage figures, not whole-program completion. The 113 verified MZ sites comprise 110 C, one assembly and two runtime sites.

Actual Microsoft LINK receives 165 real source objects and the pinned runtime libraries. It fails solely with L2029 unresolved externals: **298 missing providers**, seven fewer than C233, with no newly required names, stubs, automatic aliases, original-target mounts, object edits or execution of the incomplete output. No provided-callee alias remains.

The independent initialized DATA audit checks all 96 physical allocations / 97 units / 1,881 bytes and zero native or emitted MZ sites. No individual DATA allocation now requires enclosing WORD alignment. This does not prove the original global DATA map. CODE still has 13 alignment obligations, 13 unequal whole spans and five confirmed non-CodeView collisions. 36 complete CODE contexts verify independently. The anonymous compiler-owned pools total 443 uncredited bytes across four allocations: asset 112, arena 65, editor/state 264 and selector two. Retiring the prior button CONST24 does not add separate pool credit.

The actual manifest producer is `build/source-contexts-240-preparation/manifest_actual_segments.py`; the DATA audit producer is `data_alignment_current.py` in that directory. Original draft producers, exact earlier payloads, failure logs and the narrowly scoped metadata corrections remain archived. The diagnostic corrections change read-only metadata interpretation and a stale expected-byte assertion, without changing canonical validators or matching credit.

All 18 previous checkpoint records, 54 historical producer/output files and 35,930 archived paths are rehashed unchanged. The new checkpoint archives current source/configuration, actual objects, native evidence, compiler/backend profiles, complete frozen composition dependencies, focused 229-test evidence and full regression provenance.

See [the immutable checkpoint](../evidence/verification-240-source-contexts-checkpoint.json), [full regression coverage](../evidence/regression-240-source-contexts-coverage.json), [actual LINK](../build/source-contexts-240-preparation/outputs/actual-LINK.json), and [dependency inventory](../build/source-contexts-240-preparation/outputs/manifest.json).
