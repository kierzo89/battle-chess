# QuickC 1.00 hypothesis: bounded negative result

The bundled QuickC 1.00 compiler was investigated as a possible source of
functions whose target code retains BP/SP epilogues but has optimized inner
instructions. Six controlled compilations did not reproduce these functions.

## Inputs and primary documentation

The [PCjs Microsoft C 5.00 catalog](https://www.pcjs.org/software/pcx86/lang/microsoft/c/5.00/)
lists `QCL.EXE` on the SETUP disk and `QC.EXE` on the QUICKC disk. The complete
machine-readable catalog identifies QUICKC as **disk 8**, rather than disk 9.
Selected files were extracted with the existing checked FAT12 reader from:

* `MSC500-DISK1-SETUP.json`, SHA-256
  `f92365026481c3b8ca987af4414d598e0c8546ec32376d6db20adf7d3b04b97e`.
* `MSC500-DISK8-QUICKC.json`, SHA-256
  `76613fc73018fe64d25fb5302da79760f31eccfbca269c654552d693ad050a89`.

The [experimental manifest](../build/probes/qc/manifest.json) records each
extracted file's hash and size. The tools remain in the ignored local
`toolchains/qc100` directory; no production compiler profile was registered.
This is a historical proprietary distribution preserved by PCjs; no MIT
license or redistribution permission is claimed.

The bundled `QCL.HLP` is primary documentation for this executable's options:
`/O` and `/Ot` enable its default optimization, `/Od` disables optimization,
`/Ol` enables loop optimization, `/Ox` combines `/Ot` and `/Ol`, and `/Gs`
disables stack checks. `README.QC` explains that `/Ol` places frequently used
loop variables in registers. This QuickC 1.00 behavior must not be inferred
from later QuickC 2.x or modern MSVC options.

## Controlled output

The [probe source](../build/probes/qc/PROBE.C) contains ordinary C for an empty
function with an unused argument, a one-bit mask, the equality wrapper, and
the board-clear wrapper. All compilations used `/c /AS /Zi` and DOSBox with
the extracted QCL/QC tools. No inline assembly or source byte emission was used.

| Function | Target bytes | Default / `/Od` / `/Ot` | `/Ox` |
|---|---:|---:|---:|
| Empty unused-argument function, 5A2B | 12 | 17 | 15 |
| Low-bit result, A514 | 20 | 26 | 24 |
| Equality wrapper, 9448 | 39 | 53 | 51 |
| Board-clear wrapper, 946F | 29 | 35 | 33 |

All outputs differ materially: QuickC saves/restores SI and DI and emits
unoptimized frame setup. `/Ox` suppresses the probe but leaves a zero-sized
stack subtraction and the generic register saves. An explicit `/O` compilation
and another `/O` compilation with the full C5.00 compiler passes on PATH both
produce the **identical entire object file** as the default command, SHA-256
`9c8b0ad83cf2f023275f44e2b85bdb3d5a91986094cbba347ef63ca9907d219b`.
The missing optimizer-pass executable hypothesis therefore does not explain
the result. No QuickC byte matches were claimed.

[Exploratory result records](../build/probes/qc/RESULTS.json) retain the linked
bytes. QuickC uses target threads with method encodings 4–6 and direct segment
fixups in its CodeView procedure records. The existing production CodeView
reader deliberately rejects the latter instead of assuming a function size.
Exploratory inspection used complete next-public extents and normalized thread
methods, without editing the production parser or stripping bytes. These
diagnostic comparisons are not registered production matching units.
The thread normalization is corroborated by the
[TIS 1.1 OMF specification](https://refspecs.linuxfoundation.org/elf/TIS1.1.pdf),
which specifies that only the low two method bits are used for target threads
and the displacement bit comes from the individual FIXUP.

## Conclusion

The six runs exclude these straightforward source shapes under the tested
QuickC 1.00 configurations. They do not exclude every QuickC release or source
constraint. The target's unusual frame epilogues remain unexplained; an
additional first-class QuickC profile would currently add complexity without
a demonstrated matching function.
