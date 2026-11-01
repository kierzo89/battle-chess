# Separate _animate_move363 one-MASM control proposal

Whole native78F6..7A61 exclusive,363 bytes/143 instructions, RET7A60; prior77AF327 and next7A61 body are outside this source. Existing complete primary and independently decoded original agree; nativeMZ0 including crossing boundaries. Source uses WORD PUBLIC CODE (even nativeentry), emptyWORD DATA/DGROUP and sole real PUBLIC _animate_move. No DB/DW/opcode data, padding, NOP, ORG, source variants or aliasdefinitions.

All14 fields are real external targets: __chkstk, _detach_actor, _queue_piece and still-genuine _undo_animation; _cells/_actor_map/_kind_map/_actors. Group-relative address immediates use OFFSET DGROUP explicitly. Real Actor WORD+20 field is encoded as _actors+20, not a fake PUBLIC. No ownCODE field is expected; all local branches are exact short displacements. Whole363 and every143instruction/field/sourceaddend must match, not maskedCODE. Four loadbases and no emitted/nativeMZ are strict.

ABI: near void(Move8*), oneWORD BP+4 nearpointer/caller cleanup2; savesSI/DI/BP, chkstk AX20 frame. Calls detach_actor with oneWORD Actor pointer, queue_piece with four lowBYTE values in actual pushedWORDs/cleanup8, and undo_animation with one nearpointer to localMove/cleanup2. Actual WORD offsets0/2/4 and BYTE6/7 are retained without historical field-name inference. All native highregister/uninitialized local states and the actor-loop index32 outcome remain unchanged. No all-path actor/map bounds or original capacities are claimed.

Three current selected CALL fields in shared-turn CODE are pinned with raw/current native owner identities. Current closed495 SOURCE272 plus four reviewed frame/loader components show no samePUBLIC collision. Completed499 pipeline outputs were not needed/read by this assessment; the bridge uses preserved old272 objects and known four actual controls. Separate327 _undo_animation proposal is unadmitted here, so its call remains honest genuine dependency; never rename to synthetic _queue_move.

Legacy exactC363 report is preserved with its source's unused_a/unused_b locals, unpadded and frame-assumption source controls. It is not new canonicalC matching credit or original source proof; no C matrix is rerun. AuthoredASM makes no claim originalASM or C unrepresentability.

Asset-frame DATA160 hold is unchanged. This routine accesses _actors WORD+20 (DS05F4), not asset_frames finalWORD8 atDS0E28. No new read/writer/extent for that table was discovered or supplied as filler.

After independent root review, copy and bind rootfalse GEN-release schema:

```
python3 assemble_once.py /absolute/GEN-release.json /home/kierzo/chess/matching/build/animate-move78f6-authored363-one-MASM-root-actual
```

At most one actual pinnedMASM5.10 /Mx, source/tools/freshscratch only with20denials and real Popen PID/terminal/reaped receipt. No retry/source/flag changes, oldOBJ injection, LINK or EXEexecution. Parent writes root-terminal-receipt using actual hashes/PID, then binds CMP-release schema:

```
python3 compare_closed.py /absolute/CMP-release.json
```

Pure whole-object/native comparison retains every difference/negative. No sourceGEN, tests, queries, canonical writes, production/admission or credit were performed by worker. Zero Cfunction/standaloneASMfunction credit.
