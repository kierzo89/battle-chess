# C4/C5 attribution cross-check

**Attribution correction:** fresh MSC5.00 `/AS /Zi` with no explicit `/O` option
exactly matches every formerly C4-registered helper, and also matches equality
`9448`. [Full evidence](../evidence/msc500_default_all_frames.json) supersedes
any suggestion below that these checked frames require C4 or mixed releases.
The C4 comparisons remain valid observations of compatible output; they do not
uniquely identify the historical compiler.

The 144-byte turn routine `7DDB` is **not a distinguishing compiler-version
fingerprint**: the same faithful source produces its entire original byte
sequence with both MSC4.00 and MSC5.00 under the tested configurations. Other
functions distinguish those configurations, but exact historical producer
versions remain an inference.

## Controlled method

The existing ordinary C sources for math, `8FCA`, and `7DDB` were copied to
ignored `build/compiler-cross-version/` probes. Only ANSI prototype declarations
and function-definition syntax were converted to C4-compatible K&R forms.
Expressions, statements and declared types were unchanged. The same transformed
sources were then compiled by both pinned backends.

[Retained evidence](../evidence/compiler-cross-version.json) contains each
original source hash, transformed source text/hash, compiler flags and command,
compiler/manifest/object hashes, complete linked function bytes, relocation
arithmetic, target bytes, and the original retained REA body extents and Evidence
IDs. Procedure extents come from the compiler's CodeView3 records. All generated
bytes are compared; no postprocessing, assembly substitution or truncation is
performed. The original target SHA-256 is
`c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd`.

## Results

All configurations below use `/AS /Gs /Zi`; the option column gives the
additional optimization option. “Default” means no explicit `/O` option while
retaining those three shared options.

| Function | Target | C4 `/Os` | C4 default | C5 `/Os` |
|---|---:|---:|---:|---:|
| `min_i16` | 16 | 23 mismatch | 25 mismatch | **16 exact** |
| `max_i16` | 16 | 23 mismatch | 25 mismatch | **16 exact** |
| `abs_i16` | 21 | 23 mismatch | 25 mismatch | **21 exact** |
| Search `8FCA` | 64 | 71 mismatch | 77 mismatch | **64 exact** |
| Turn `7DDB` | 144 | **144 exact** | **144 exact** | **144 exact** |

The transformed source also reproduces every original C5 match, which checks
that the dialect adaptation did not invalidate those positive controls. The
`7DDB` result includes the properly relocated original far-pointer alias
`0FBF:00F8`; its four-byte far relocation is compared in full.

## Interpretation and limits

The C4 generic-frame matches alone do not establish a uniform C4 build, and
`7DDB` must no longer be presented as unique evidence for C5. These bounded
experiments preserve a meaningful distinction for `8FCA` and the simple math
sources: C4 with the tested configurations fails while C5 succeeds. They do not
exclude other C4 flags, materially different faithful source expressions, an
intermediate release, or a mixed compiler build. A complete historical producer
attribution remains unresolved.
