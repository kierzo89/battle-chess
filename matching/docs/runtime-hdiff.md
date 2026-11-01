# Authentic huge-pointer subtraction helper

The independently archived MSC5.00 SLIBC HDIFF member supplies `__aNahdiff`,
used by the arena manager and group compactor. Its complete CODE SEGDEF is45
bytes. It contains a43-byte LEDATA write followed by a three-byte write at42:
the one-byte overlap replaces RET with RET8. The strict ordinary C-object
reader continues to reject overlapping CODE records.

The existing authentic-LINK backend now accepts a member explicitly selected
from the already pinned runtime500 profile. It validates that profile's
installation manifest, complete library digest, member digest/offset, sole
initialized CODE segment, public0 and complete declared length. Unknown
library profiles are rejected before launching LINK. It neither merges writes
nor accepts reference bytes; unchanged object records go to pinned LINK3.65
inside an isolated DOSBox drive. The full emitted MZ image must be exactly45
bytes, with no relocations, and its map must agree with the complete segment.

REA's complete original function and raw45-byte extent atF1D6 agree with that
output. `evidence/hdiff-authentic-link.json` retains the independent library,
tool, write-overlap and map provenance; `hdiff-production-match.json` retains
the production match. Targeted tests check full equality, strict-reader
rejection, wrong runtime pins and unsupported profiles. This is45 additional
runtime bytes and zero authored C/ASM credit. Source-policy rules remain
unchanged. Runtime500's configuration hash is retained alongside the helper
registry hash in each applicable build's provenance.
