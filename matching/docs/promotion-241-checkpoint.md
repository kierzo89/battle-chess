# C241 source-context checkpoint

The goal remains exact reproduction of the original 83,415-byte CHESS.EXE from genuine source. A complete independent executable is still absent.

This checkpoint verifies **241 complete functions / 45,656 bytes**, **98 C DATA contributions / 1,898 bytes**, 11 assembly functions / 994 bytes, a separate complete 120-byte assembly CODE contribution, 896 assembly DATA bytes, and 4,240 reviewed runtime bytes. All 401 matching units pass. The required complete-executable check exits 1 because the full executable remains unmatched.

All 933 tests pass in one run, in 901.281 seconds, with zero skips. Their exact IDs, interpreter, unchanged direct input hashes and log are retained in the regression coverage record. Earlier interrupted C233 attempts remain historical non-PASS evidence; this is a new complete C241 run.

One genuine C procedure adds 490 bytes, and one minimal consumed prompt adds 17 initialized DATA bytes. Assembly and runtime credit are unchanged. Six source-only COMMON objects provide 30 definitions / 94 allocation bytes, with zero initialized-byte or matching credit. Historical storage order, translation-unit ownership and compiler flags remain nonunique.

Verified original-file spans total 50,840 bytes (60.948271%); verified expanded-image spans total 53,804 bytes. These are span coverage figures, not whole-program completion. The 113 verified MZ sites comprise 110 C, one assembly and two runtime sites.

Actual Microsoft LINK receives 167 real source objects and the pinned runtime libraries. It fails solely with L2029 unresolved externals: **298 missing providers**, resolving `_select_promotion` while exposing `_promotion_choices` as a new required storage provider. The diagnostic uses no stubs, automatic aliases, original-target mounts, object edits or execution of the incomplete output. No provided-callee alias remains.

The independent initialized DATA audit checks all 97 physical allocations / 98 units / 1,898 bytes and zero native or emitted MZ sites. No individual DATA allocation now requires enclosing WORD alignment. This does not prove the original global DATA map. CODE still has 13 alignment obligations, 13 unequal whole spans and five confirmed non-CodeView collisions. 37 complete CODE contexts verify independently. The anonymous compiler-owned pools still total 443 uncredited bytes across four allocations: asset 112, arena 65, editor/state 264 and selector two. No extra DATA credit is assigned to those pools. The new unresolved choices view does not establish an array capacity or adjacent-pointer ownership.

The actual manifest producer is `build/promotion-241-preparation/manifest.py`; the DATA audit producer is `data_alignment.py` in that directory. Current native evidence and actual source objects are retained separately from historical C240 baseline config/report bytes. The earlier README-only publication repair remains immutable; historical test mirrors now hold their exact regular-file README payloads and cannot alias the live documentation.


All 19 previous checkpoint records, 57 historical producer/output files and 45,186 archived paths are rehashed unchanged. The new checkpoint archives current source/configuration, actual objects, native evidence, compiler/backend profiles, complete frozen composition dependencies, frozen promotion/API/semantic-negative evidence and full regression provenance.

See [the immutable checkpoint](../evidence/verification-241-promotion-checkpoint.json), [full regression coverage](../evidence/regression-241-promotion-coverage.json), [actual LINK](../build/promotion-241-preparation/outputs/actual-LINK.json), and [dependency inventory](../build/promotion-241-preparation/outputs/manifest.json).
