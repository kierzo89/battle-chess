# C242 source-context checkpoint

The goal remains exact reproduction of the original 83,415-byte CHESS.EXE from genuine source. A complete independent executable is still absent.

This checkpoint verifies **242 complete functions / 45,898 bytes**, **101 C DATA contributions / 1,916 bytes**, 11 assembly functions / 994 bytes, a separate complete 120-byte assembly CODE contribution, 896 assembly DATA bytes and 4,240 reviewed runtime bytes. All 405 units pass. The complete-executable check exits 1 because the full executable remains unmatched.

All 981 tests pass in one run, in 928.517 seconds, with zero skips. The exact IDs, interpreter, log and unchanged direct input hashes are retained in the regression coverage record. No historical regression is relabelled as this run.

One genuine C input-dialog function adds 242 bytes. Three typed initialized DATA contributions add 18 bytes. Assembly/runtime credit is unchanged. Seven source-only COMMON objects provide 47 definitions / 134 allocation bytes, including seventeen new definitions / 40 bytes, with zero initialized-byte or matching credit. Original placement and CRT/layout constraints remain unresolved.

Verified original-file spans total 51,082 bytes (61.238386%); expanded-image spans total 54,064 bytes. These figures describe span coverage, not whole-program completion. The 116 verified MZ sites comprise 113 C, one assembly and two runtime sites.

Authentic Microsoft LINK consumes 172 real source objects and pinned runtime libraries. It fails solely with L2029 for 272 missing providers, resolving 27 old requirements and exposing `_command_words_8d2c` as one newly required provider. The manifest independently agrees with the exact missing-name set. The diagnostic uses no stubs, automatic aliases, original-target mounts, object edits or execution of the incomplete output.

The DATA audit checks 100 complete physical allocations / 101 units / 1,916 bytes, with zero native/emitted MZ sites and zero individual WORD-alignment obligations. Global DATA order and the original map remain unproved. CODE retains 13 alignment obligations, 13 unequal whole spans and five confirmed non-CodeView collisions; 38 complete CODE contexts verify. Four compiler-owned CONST pools retain 443 uncredited bytes without duplicate DATA credit.

The native arena erratum is explicit: image 0x2CDF is C3. Four native 51-byte bodies occupy a 205-byte original span because that byte intervenes. The 204-byte diagnostic SNAP contribution is not a reconstruction of the entire 205-byte context; retained individual comparisons and source-only allocation proofs have their original bounded scope.

The actual manifest producer is `build/source-contexts-242-preparation/manifest.py`. The actual DATA-audit producer is `data_alignment_current.py`; its predecessor and failed stale-count log remain preserved. That diagnostic-only correction changes the expected unit count from 98 to 101 and preserves all actual byte/segment/native comparisons. Canonical matching inputs were unchanged.

All 20 previous checkpoint records, 60 historical producer/output files and 54,589 archived paths are verified unchanged. Historical compiler flags, translation-unit ownership, final global layout and complete EXEPACK reproduction remain unproved.

See [the immutable checkpoint](../evidence/verification-242-source-contexts-checkpoint.json), [regression coverage](../evidence/regression-242-source-contexts-coverage.json), [actual LINK](../build/source-contexts-242-preparation/outputs/actual-LINK.json) and [dependency inventory](../build/source-contexts-242-preparation/outputs/manifest.json).
