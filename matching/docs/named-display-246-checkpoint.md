# C246 named-display checkpoint

The goal remains exact reproduction of the original 83,415-byte CHESS.EXE from genuine source. A complete independent executable is still absent.

This checkpoint verifies **246 complete functions / 46,405 bytes**, **103 C DATA contributions / 1,977 bytes**, 11 assembly functions / 994 bytes, a separate complete 120-byte assembly CODE contribution, 896 assembly DATA bytes and 4,240 reviewed runtime bytes. All 411 units pass. The complete-executable check exits 1 because the full executable remains unmatched.

All 1032 tests pass in one run, in 945.730 seconds, with zero skips and all direct input hashes unchanged. Exact IDs, interpreter and log are retained in the regression coverage record. Earlier regressions are historical evidence, not this run.

Four genuine C functions contribute 507 bytes in one 508-byte allocation, with the original final 90 byte retained and excluded from credit. `DISPLAY.C` compiled with `/AM /Gs /Zi` creates `DISPLAY_TEXT`; the complete contribution, fields and MZ set match. The actual helper frame is CS 0FBF and remains distinct from evaluator CS 0FDF. The inert 8.3 filename validation and source-name-sensitive cache/artifact identities are tested; default UNIT.C behavior remains unchanged. No source slicing, object edits or padding arrays generate the byte match. This matching configuration does not prove unique historical compiler flags or translation-unit ownership.

Two typed packet DATA contributions add 61 initialized bytes. Assembly/runtime credit is unchanged. Seven source-only COMMON objects provide 47 definitions / 134 allocation bytes with zero initialized-byte or matching credit; final original placement remains unresolved.

Verified original-file spans total 51,589 bytes (61.846191%); expanded-image spans total 54,632 bytes. These are span-coverage figures, not whole-program completion. The 116 verified MZ sites comprise 113 C, one assembly and two runtime sites.

Authentic Microsoft LINK consumes 175 real source objects and the pinned runtime libraries. It fails solely with L2029 for 268 missing providers, resolving four prior display requirements and adding none. The actual missing-name set agrees exactly with the dependency manifest. The diagnostic uses no stubs, automatic aliases, original-target mounts, object edits or execution of its incomplete output.

The initialized DATA audit checks 102 physical allocations / 103 units / 1,977 bytes, with zero native/emitted MZ sites and zero individual WORD-alignment obligations. The original global DATA map remains unproved. CODE retains 13 alignment obligations, 13 unequal whole spans and five confirmed non-CodeView collisions; 39 complete CODE contexts verify. Four compiler-owned CONST pools retain 443 uncredited bytes without duplicate DATA credit.

The inherited native arena erratum remains explicit: image 2CDF is C3, and four native 51-byte bodies occupy a 205-byte original span. The 204-byte diagnostic SNAP allocation is not a complete 205-byte native-context reconstruction. The archive resolver distinguishes lowercase 64-hex hashes from 64-character path references, follows both path references and genuine hash maps, and rejects wrong digests. Its original C242 failure/control provenance remains immutable.

All 21 previous checkpoint records, 63 historical producer/output files and 64,960 archived paths verify unchanged. The actual diagnostic producers in `build/named-display-246-preparation` consume complete fresh report object artifacts, including the named source, without recompiling C. This checkpoint retains genuine sources, profiles, complete OMF artifacts, primary native evidence, frozen composition/API/negative controls and regression/publication provenance. Pinned README/integration/next-work files remain unchanged during publication.

See [the immutable checkpoint](../evidence/verification-246-named-display-checkpoint.json), [regression coverage](../evidence/regression-246-named-display-coverage.json), [actual LINK](../build/named-display-246-preparation/outputs/actual-LINK.json) and [dependency inventory](../build/named-display-246-preparation/outputs/manifest.json).
