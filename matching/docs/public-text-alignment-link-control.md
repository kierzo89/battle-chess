# Authentic LINK3.65 PUBLIC WORD alignment

An independent NASM OMF object defines `_TEXT public align=2 class=CODE use16`
with exactly three bytes, `nop; nop; ret`. Its SEGDEF attributes are48 hex,
the same PUBLIC/WORD alignment as the small-model C object. An ordinary pinned
MSC500 `/AS /Gs /Zi` main calls that procedure and returns zero. Authentic
pinned Microsoft Overlay Linker3.65 links both with the original SLIBC library.
No original game executable is read or mounted, and this control earns no
matching credit.

| Object order | Prefix offset | Main offset | Alignment gap |
| --- | --- | --- | --- |
| CRT0, PREFIX, MAIN | 00C4 | 00C8 | one00 after three-byte prefix |
| CRT0, MAIN, PREFIX | 00D2 | 00C4 | zero after C's14-byte CODE |
| PREFIX, MAIN; library startup | 0010 | 0014 | one00 after three-byte prefix |
| MAIN, PREFIX; library startup | 001E | 0010 | zero after C's14-byte CODE |

The exact segment:offset pairs and complete maps are retained in the evidence.
All four generated executables run successfully and exit zero. Every command
uses `/NOD /DOSSEG /MAP`. The explicit extracted CRT0 runs also use `/NOE`:
without it, the extended library dictionary attempted to pull CRT0 twice and
LINK reported multiply defined CRT symbols. The library-startup controls need
no `/NOE` and independently show the same one-byte alignment behavior.

Thus these authentic LINK commands align the following PUBLIC WORD contribution
to an even offset; they do not append it immediately at the odd byte following
the three-byte prefix. This establishes the tested configuration's behavior,
not all possible historical linker settings. An odd public address inside a
larger contribution remains possible; it must not be confused with an odd
WORD-aligned contribution base.

`evidence/public_text_alignment_link_control.json` retains NASM version/hash,
full sources, complete input object metadata and hashes, compiler commands/logs
and pinned tool manifests, authentic linker/library/CRT0 provenance, all link
commands/logs/maps, executable hashes, and full linked images. Actual input
objects and the four executable/map/log sets are preserved under
`build/public-text-alignment/`. The reproducible script is
`evidence/public-text-alignment-probe.py`. Canonical configuration, source,
registry, and parser files were not changed.
