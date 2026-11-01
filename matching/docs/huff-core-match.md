# Rebuilt Huffman core

Nine hand-authored NASM routines reproduce every byte of the contiguous
944-byte original core at E03A..E3E9. Five are new, totaling 786 bytes: lookup
construction191, byte-count decoding235, row decoding274, stack adaptor38 and
window initialization48. The preceding four routines already contributed158.
This is assembly credit and earns no C-function or C-code credit.

`evidence/huff-core-probe.py` freshly assembles each source before reading the
original, checks complete original REA function extents, and compares the entire
contiguous result with both the pinned file prefix and independent expanded
image. The full 944-byte REA raw read and zero original MZ sites are mandatory.
`evidence/huff-core-match.json` retains all source text, listings, hashes and
production results. Explicit two-byte register-direction encodings are ordinary
hand-authored assembly instructions, not compiler-emitted C bytes.

Five Unicorn tests execute only the newly assembled code and independently
encoded synthetic inputs. They cover short-code incremental reads, long codes
through depth16 and multiple input refills, output spanning64KiB, count clamping,
and odd/even row padding and returned pointers. A bounded synthetic512-byte
refill hook supplies input; it does not claim to implement the original DOS I/O
routine. The real refill has a separate discontiguous body around an INT3 and
is not counted as a reconstructed core procedure here.

The nine long-code masks, `{0,128,192,224,240,248,252,254,255}`, follow from their
prefix-mask role in lookup construction. REA reads exactly those nine initialized
bytes at DS:44CC in the pinned expanded carrier. An ordinary typed C initializer
independently reproduces the entire DATA contribution. See
`evidence/huff-mask-data-experiment.json`. It earns nine expanded-image DATA
bytes, no compressed-file coverage and no C-function credit. Original source
ownership and complete storage placement remain unresolved.
