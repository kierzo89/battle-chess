# Modal-region C checkpoint

This checkpoint adds one complete121-byte `fill_region_1780` procedure from
ordinary C, compiled by the pinned Microsoft C5.00 with `/AS /Zi`. The function
fills a modal region and draws three inset border rectangles. The colour
parameter supplies the real loop counter; there are no automatic variables or
invented stack allocations. The register parameter hints reproduce SI/DI use.

The complete original native extent and independent compiler CodeView extent
are both121 bytes. All eight actual relocation fields and the complete three
original MZ sites (1793,17A9,17F1) match at four DOS load bases. The full205-byte
native read includes the following complete84-byte select-mode procedure. The
actual CODE SEGDEF is122 bytes and retains its compiler90 tail, which conflicts
with the following native55 byte. That tail earns zero credit. This does not
establish the original translation unit or a complete source layout.

Current verification has193 C functions/37,401 bytes,98 initialized C DATA
contributions/1,436 bytes,11 ASM procedures/994 bytes and49 runtime units/4,240
bytes. All351 reviewed units pass the final fresh checker. Verified file spans
are42,465/83,415 (50.908%); expanded spans are44,071/401,131. Source relocation
coverage is64 plus two runtime MZ sites, totaling66/173. These coverage measures
are not a whole-program completion percentage.

The complete444-test regression passed at the immediately preceding C192
checkpoint with253 implementation/source/config inputs pinned throughout. This
addition changes only one C source and the registry. The verifier and tests
remain unchanged; the final all351-unit checker recompiles and validates the
new registry. A second full444-test suite after this source-only admission was
not run. The verification record preserves this distinction explicitly.

See [the immutable record](../evidence/verification-193-fill-region-checkpoint.json),
[full444-test baseline](../evidence/verification-192-input-storage-checkpoint.json),
and [dependency findings](../evidence/source-link-dependency-findings-193.md).
Earlier immutable checkpoints and the C192 manifest are unchanged. No complete
independent source-built executable exists. Remaining definitions, source
ownership/layout, true source/runtime link, header/all173 MZ sites and authentic
EXEPACK output to the original SHA256 remain the active full-byte goal.
