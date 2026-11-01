# Main and authentic LINK prefix configuration

The original image starts with16 zero bytes before main0010. A full expanded
REA read confirms all16 bytes, and native analysis has no procedure at image0.
This observation alone does not establish the owner or a source definition.

`evidence/link-dosseg-prefix-probe.py` independently compiles a minimal ordinary
C main, then uses pinned LINK3.65 and the genuine independently supplied SLIBC
and helper libraries. Its temporary drives contain only fresh objects and the
pinned tools/libraries. It neither reads nor mounts the original, an unpacked
image or a REA carrier. Both executables link and run successfully.

The explicit `/DOSSEG` trial and the trial omitting that option both place
`_main` at0000:0010. Both produce exactly16 zero image bytes before it. The
entire fresh main CodeView body also agrees with the independently relocated
LINK output. Full headers, maps, logs, response files, source/object/tool hashes
and executables are retained under `build/link-dosseg-prefix/`; the complete
proof is `evidence/link-dosseg-prefix-experiment.json`.

This is a concrete legal mechanism for main's original origin without dummy
source declarations or target-derived filler. Since both trials agree, the
experiment does not uniquely identify whether the original command explicitly
used `/DOSSEG`. It does not establish the original linker version or complete
link order. No additional16-byte matching credit is claimed; complete source
linking and exact header/relocations/packing remain required.

The typed graphics function-address cast emits Microsoft OMF location5. The
[TIS OMF1.1 specification, page45](https://sininenankka.dy.fi/~sami/watcom_mirror/devel/omf.pdf)
defines this as a16-bit loader-resolved offset with OFFSET16 arithmetic. The
restricted backend admits only segment-relative external far placements,
retaining the original location type in logs. Its independent authentic LINK
control uses target offsets2/4 in distinct nonzero code segments; complete
CODE/CV and MZ sets agree in both object orders. The offset field itself earns
no MZ site. Seven regression tests reject unsupported field shapes and missing
bindings. This expands verified source-link capability without masking output.

Main's first C probe also demonstrates that meaningful local names can affect
C5 frame allocation. The descriptive-name version has580 complete bytes and13
different frame displacements; the a/b/c/d version has580 identical bytes. All
four locals have real operations or pointer-output uses. This gives a viable
source reconstruction, while leaving original identifiers unknown. No unused
locals, discarded compiler bytes or adjusted segment metadata are involved.

`main-compiler-profile-experiment.json` checks the unchanged canonical source
with C4/C5.00/C5.10. C4 rejects its ANSI function-definition syntax; that alone
does not exclude C4. A second bounded comparison changes only the main definition
to equivalent K&R parameter declarations and compiles all three profiles with
`/AS /Zi`. C4 emits582 bytes and differs; both C5.00 and C5.10 emit580 exact bytes.
The complete outputs, extents, fields, commands and tool hashes are retained in
`main-compiler-knr-profile-experiment.json`. This supports the C5 configuration
while leaving its exact historical version and commands unresolved. Other C4
source forms/flags are not exhaustively excluded by this bounded experiment.

The named Menu reference also has a separate typed20-byte DATA diagnostic and
two authentic LINK/execution controls. All eight pointer fields relocate to the
actual named backing definitions in each map, and the five-record sentinel
layout is preserved. Those backing definitions are explicit synthetic fixtures;
the table itself is the actual proposed source. Current strict DATA extraction
still rejects fixups. No credit is granted until a complete pointer-DATA backend
and its mutation controls are integrated. See main-menu-pointer-data-experiment.json
and menu-pointer-authentic-link-experiment.json.
