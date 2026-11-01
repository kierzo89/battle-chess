# Decoder directory and group-loader source controls

The separate genuine decoder candidate at2D13 remains uncredited. Existing `decode_frame_directory_probe.c` reproduces the full289-byte instruction layout in length, but its C5 `/AS /Gs /Os /Zi` stack allocation is18 rather than1C, and local offsets differ.

The new `evidence/decode-directory-type-control.json` retains three complete source/compiler/object/full-CV/full-byte controls: scalar4-byte postincrement words, a genuine FrameWord union with header/pixel-pointer members, and pointer-word representation. All are289 bytes and37 bytes differ, primarily frame/local references. The input/directory postincrements naturally restore the observed scheduling. The typed-input variants preserve the near-pointer machine argument width, but they would require compatible declarations/casts in existing callers before being a whole-program C interface; that distinction is explicit in the evidence.

`evidence/decode-directory-stride-control.json` retains three additional meaningful dataflow variants: explicit row-byte temporary, explicit row-stride temporary, and both. All remain289 bytes with18-byte frames. No unused local, inflated type, extra storage or byte patch was introduced to force a frame size.

The actual adjacent loader at35A0 was independently analyzed as one contiguous178-byte function (`evidence/rea_asset_loader_35a0.json`). `src/load_asset_group_probe.c` implements its observed asset-group boundaries, active state, frame-index list and real callee calls with the shared AssetGroup20 and AssetState14 definitions. Its first fresh C5 source output is178 bytes but allocates4 frame bytes versus the originalC; it is uncredited. Complete source/compiler/object/CV/linked bytes are in `evidence/load-group-35a0-control.json`. The new group_frame_counts binding atB8 is an observed byte-array role; naming/whole-program ownership is not claimed recovered.

These are bounded retained negatives, paused in favor of the exact task-dispatch extent work. Existing canonical sources and registry were not changed. There is no claim that the correct historical C declaration or source context has been ruled out.
