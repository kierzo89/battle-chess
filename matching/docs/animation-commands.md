# Animation command queue contribution

`src/animation_commands_match.c` freshly compiles with pinned Microsoft C5.00
`/AS /Zi` to the complete426-byte CODE contribution at image5FBD..6166.
Three independent CodeView procedures cover it without gaps or padding:
append254 bytes, advance24 bytes, and begin148 bytes. All36 fixups have one
owner, the complete linked contribution equals the original, and every
procedure's emitted and original MZ sets are empty.

The ordinary C `Command` type is eight bytes: operation, state, child, next,
square, argument, extra and reserved. The queue has32 slots at DGROUP52F0;
the cursor at04BC wraps modulo32. Appending walks the child/next chain, while
begin creates a root at984F. Both helpers update capture and piece-state flags.
Their parameter types and field order follow actual byte accesses. The source
does not define or credit the queue's DATA allocation.

[animation-commands-match.json](../evidence/animation-commands-match.json)
retains complete procedure/contribution bytes, fresh source/object/tool hashes,
fixups, raw REA and original loader-site checks. The source now supplies all
three canonical units. Reproduce with `build/animation-commands-verify.py`.

BB0E's calls still need their historical variable-argument interface recovered.
Most append calls supply four words although the helper unconditionally copies
a fifth byte-valued argument into the extra field; begin is similar. The later
command consumer at6167 reads this field, but its observed uses are confined
to operation7. The complete retained dossier is
`evidence/rea_animation_driver_6167.json`; it is not a C match. No missing
arguments were added to BB0E to make it satisfy the helpers' fixed prototypes.

An independent ordinary-C old-style definition control reproduces all426 bytes
unchanged; see `src/animation_commands_kr_probe.c` and
`evidence/animation-commands-kr-control.json`. This provides a viable declaration
shape for historical unprototyped callers. It does not make reading absent
arguments defined modern C behavior or establish the original source spelling.
The exact compiler output and the unresolved caller behavior are kept separate.
