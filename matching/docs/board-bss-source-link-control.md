# Meaningful board BSS definition and authentic consumer LINK control

A near `Cell board[120];` is a genuine minimum source definition supported by the existing native consumers. This is a missing-definition/link investigation, not initialized DATA, BSS, file-byte or new function matching credit.

The analyzed Cell ABI is four bytes: unsigned-byte kind at0, unsigned-byte side at1, signed16-bit index at2. Native add_piece96AF scales the square by4, reads the word atA8BC, and writes bytes atA8BA/A8BB. Native reset_pieces948C loops inclusively0..119 (`CMP ...,77h` followed by JG), writing the index word atA8BC+4*square. The last word is DSAA98..AA99. Native clear_board946F independently clears480bytes startingDSA8BA, also endingAA99. Thus the observed minimum initialized/used region is A8BA..AA99,120Cell values. This does not prove the historical declared capacity was exactly120 or establish bounds for every possible invalid input.

Pinned authentic CRT startup raw bytes contain `MOV DI,52CC; MOV CX,CBE0; SUB CX,DI; XOR AX,AX; REP STOSB`, establishing the original exclusive zero range DS52CC..CBE0. The minimum board interval lies wholly within it. The retained primary native dossiers are referenced by evidence ID/file hash in `evidence/board-bss-native-source-control.json`; no fresh REA question was needed, and no session was opened.

Fresh pinned C5 `/AS /Zl /Zi` compilation of the actual tentative definition emits one near COMDEF `_board`, datatype62h,480bytes, numeric leaf81h E0h01h. The full raw COMDEF payload is `065f626f61726482076281e001`. All nondebug CODE/DATA/CONST/BSS SEGDEF lengths are zero. There is no480-byte initialized segment or fabricated source initializer. Complete source/tool/object/debug/segment provenance is retained.

A separate target-free harness links this BOARD object with a real typed clear_board definition, the genuine fill8A96 implementation and a minimal main. The clear source uses the same compatible Cell type and casts its board argument to char*. Fill forwards to actual SLIBC memset using its correct prototype, with the original argument order preserved. It does not fake a runtime symbol or replace memset with a harness stub. The independently compiled full clear29 and fill20 functions remain byte-exact to their original native bodies after an explicitly separate comparison step.

Pinned authentic LINK3.65 plus real SLIBC links and executes two actual object orders:

| Actual order | clear CS offset | fill CS offset | Board allocation | CRT zero range, exclusive |
| --- | ---: | ---: | --- | --- |
| BOARD+CLEAR+FILL+MAIN |0010|002E|0176:07B0..098F|0176:037E..0990|
| MAIN+FILL+CLEAR+BOARD |00E8|00D4|0176:07B0..098F|0176:037E..0990|

The actual MZ image has6877 initialized file-image bytes. Board's linear allocation begins7952, beyond that initialized image. The actual CRT's `BF7E03B990092BCF33C0F3AA` zeroing sequence is verified against the real MAP `_edata`/`_end` placements, rather than inferring startup semantics only from initially zero memory. All complete fresh clear/fill CV bytes and relocation fields independently equal the actual linked EXE in both orders.

The main checks sizeof(Cell)=4, sizeof(board)=480 and field offsets1/2, then examines every field of all120cells after genuine CRT startup. It populates every field with nonzero data, invokes actual clear_board/fill/memset, and checks all120cells again. Both executions return success and log the passed checks. No original executable/reference/carrier or target address is read or mounted during source compilation, authentic LINK or execution. Target bytes enter only the separate native comparison reproducer. Harness main and its test patterns have no original storage or code ownership claim.

Artifacts:

- New standalone sources: `src/probes/board-bss-link/{board,clear,fill,main}.c`.
- Definition proposal only: `build/board-bss-link/definition-proposal.json`.
- Complete target-free source/compiler/COMDEF/MAP/EXE/runtime proof: `evidence/board-bss-authentic-link-control.json`.
- Native bounds, original CRT range and original clear/fill regression proof: `evidence/board-bss-native-source-control.json`.
- Reproduce target-free generation: `python3 matching/evidence/board-bss-link-probe.py`.
- Then reproduce the separate original comparison: `python3 matching/evidence/board-bss-native-probe.py`.
- All actual objects and each order's response/batch files, complete LINK/MAP/EXE/execute logs are retained in `build/board-bss-link/`.

Original object/aggregate ownership and the link inputs/order yielding original DS A8BA remain unknown. The control demonstrates that the meaningful source definition allocates real BSS and works with genuine consumers/CRT; it does not place the original board or claim whole-program closure. No canonical source, core, test or registry was changed; no BSS/file-byte credit is assigned.
