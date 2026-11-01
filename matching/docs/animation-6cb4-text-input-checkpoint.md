# Animation challenge and text input checkpoint

Original CHESS.EXE SHA256 c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd. REA Ghidra profile 894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8. Addresses below are image coordinates; REA default-space addresses add 0x10000.

## 6CB4: bounded, uncredited finding

Fresh procedure metadata and complete instruction list report entry6CB4, ranges6CB4..7088 and708D..70EE inclusive, span1083, reachable1079. Evidence: `evidence/rea_animation_6cb4_info.json`, `evidence/rea_animation_6cb4_instructions.json`, and complete outgoing-reference dossier `evidence/rea_animation_6cb4_references.json`. The composed decompiler request fails twice with Ghidra AddressOutOfBoundsException (offset0x770050); both error envelopes are retained separately, not represented as successful function Evidence.

Observed behavior includes asset file selection/seek/decode into a far buffer, challenge-text decoding by XOR0x6A, text drawing and entry, a case-insensitive response comparison with up to three attempts, and reconstruction of control-pointer tables. Static analysis does not establish execution or the original source.

Focused raw Evidence ev_aa00eed839d72da2782816c7d92e91fa5925139a3a013604379a8df8abf2677f, retained as `evidence/rea_animation_6cb4_patch_tail.json`, reads35 original bytes at7077. After `CMP BYTE ES:[BX],0`, bytes707E/707F are9090; after a second comparison with67h,7087 containsEB04 to708D. The four omitted bytes7089..708C areEBFE EB59: an unreachable self-loop followed by an unreachable jump. These facts support the inference that response-validation branches were patched; they do not identify an author or patch history. No ordinary-C match, bytes-as-C, NOP insertion, or assembly exception is claimed for this1083-byte procedure. Primitive metadata/CFG and raw bytes remain available for future reviewed reconstruction.

## 1064: genuine complete C match, boundary review required

`src/text_input_match.c` reconstructs the text-entry loop, underscore cursor, optional initial character, printable-character limit, backspace erase, Return termination, and DS0055 activity flag. Its only automatic local is the used length word; x/y are register parameters. No unread frame words, artificial helper calls, source bytes, inline assembly, or target-driven truncation are present.

Fresh genuine MSC5.00 `/AS /Zi` emits one complete256-byte CV procedure and one complete256-byte CODE SEGDEF, exactly equal to both original on-disk image1064..1163 and the independently unpacked image. All10 CODE fixup fields are independently reapplied from the complete raw segment and equal the production linker output. Both emitted and original interval MZ relocation sets are empty; all function bytes consequently remain exact at load paragraphs0,1,1234h,EE10h. Full compiler/object/CV/fixup/MZ evidence: `evidence/text-input-1064-match.json`; reproducible verifier and unregistered proposal: `build/text-input/verify.py` and `build/text-input/units.json`.

The provider reports an incomplete107-byte body at1064 and a spurious overlapping function10D3. Raw source call evidence at0694 is9A03000D11: far pointer110D:0003, whose actual image address is110D3 (loaded210D3). REA instead associates it with loaded110D3, splitting the true input routine's AND AX,F000 instruction beginning image10D2. The provider's overlapping body is therefore not accepted as an independent true entry. Complete original dossiers are `rea_input_1064.json`, `rea_input_10d3_overlap.json`, `rea_input_next_1164.json`; full562-byte original context covers the entire256-byte procedure and entire306-byte next procedure (`rea_input_full_next_context.json`); raw far call and global xrefs are separately retained. An independent strict boundary reviewer owns the decision to register this unit. Although current production build_unit returns c_matched, this checkpoint does not use that result to settle the provider boundary defect.

DS0055 is named text_input_active, distinct from canonical input_state at9854. It is an external byte view; initialization ownership and data credit are not claimed.
