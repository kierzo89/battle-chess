# C251 packet and serial checkpoint

The goal remains exact reproduction of the original 83,415-byte CHESS.EXE from genuine source. A complete independent executable is still absent.

This checkpoint verifies **251 complete functions / 47,218 bytes**, **104 C DATA contributions / 1,978 bytes**, 11 assembly functions / 994 bytes, two separate complete assembly CODE contributions / 302 bytes, 896 assembly DATA bytes and 4,240 reviewed runtime bytes. All 418 units pass. The complete-executable check exits 1 because the full executable remains unmatched.

All 1130 tests pass in one run, in 984.108 seconds, with zero skips and every direct input hash unchanged. Exact IDs, interpreter and raw outcomes are retained in the regression coverage record. Neither an earlier run nor focused controls are relabelled as this complete regression.

The packet source contributes six genuine functions / 855 bytes in whole CODE 856, retaining one original final 90 byte with zero credit. Five new functions add 813 bytes. The existing 42-byte input reset moves into this context and is counted once. One initialized refresh_stop byte adds one C DATA byte. The receive buffer has a native-consumed 39-byte minimum; its 42-byte frame includes a used pointer home and compiler WORD rounding. Historical buffer capacity and safety of the native unbounded ASCII path remain unproved.

The required symbolic MASM 182 allocation is separately reported as assembly CODE. It has two genuine far PUBLIC entry labels, an internal 71-byte raw IRQ CFG ending in IRET, and a saved DS word of two bytes inside CODE. The internal handler is not claimed as an ordinary REA function; no additional C function, ASM function or DATA credit is assigned. Actual segment 2 is SERIAL_TEXT with native frame 10D3; empty _DATA of length zero and DGROUP carry comparison frame 5CC2, not a final original MAP claim. Field 150 uses the actual empty _DATA segment frame; its equality with DGROUP in the native comparison remains a layout constraint, not a proved global linker map. All 17 actual fields, original bytes, MZ set and four load bases remain checked.

Seven source-only COMMON objects provide 47 definitions / 134 allocation bytes, with zero initialized-byte or matching credit. The historical allocation order and final original MAP remain unproved.

Verified original-file spans total 52,584 bytes (63.039022%); expanded-image spans total 55,628 bytes. These are span-coverage figures, not whole-program completion. Actual verified MZ sites comprise 113 C, 1 assembly and 2 runtime sites.

Authentic Microsoft LINK consumes 177 real source objects and pinned runtime libraries. It fails solely with L2029 for 263 missing providers. Names resolved since the last checkpoint are `['_enable_serial_irq_10d3_0023', '_receive_packet_ddd3', '_record_dfac', '_record_kind_dfe3', '_refresh_stop_11a6', '_reset_df71', '_set_serial_format_10d3_0000']`; newly required names are `['_serial_irq_flags_b0d4', '_serial_ring_end_2eba']`. The actual missing-name set agrees exactly with the independently derived manifest. No stubs, automatic aliases, target mounts, object edits or execution of the incomplete output enter the diagnostic.

The DATA audit checks all complete initialized allocations with zero duplicate credit; the original global DATA map remains unproved. CODE retains 12 alignment obligations, 13 unequal whole spans and five confirmed non-CodeView collisions; 40 complete CODE contexts verify. Four compiler-owned CONST pools retain 443 uncredited bytes. DISPLAY.C /AM/Gs/Zi and its distinct 0FBF frame remain preserved, without claiming unique historical compiler flags or translation-unit ownership.

All 22 previous checkpoint records, 66 historical producer/output files and 76,014 archived paths verify unchanged. C246 publication provenance identifies its successful standalone streaming resume, preserves the terminated watcher exit 143 and the original 11,046 payloads, and leaves the termination cause unproved. This fresh checkpoint streams individual files from the start; it does not resurrect that watcher or hold the entire archive payload in RAM. Current pinned README/integration/next-work files remain unchanged during publication.

See [the immutable checkpoint](../evidence/verification-251-packet-serial-checkpoint.json), [regression coverage](../evidence/regression-251-packet-serial-coverage.json), [authentic LINK](../build/packet-serial-251-preparation/outputs/actual-LINK.json) and [dependency inventory](../build/packet-serial-251-preparation/outputs/manifest.json).
