# Consumed register locals and unexplained frames

This bounded control tests a source/configuration interaction absent from the earlier default-profile local-lifetime matrix: whether a genuinely consumed register local can leave a reserved stack slot while its operations stay in registers. No unread declaration, inflated type or artificial helper is introduced. The fresh original REA A799 dossier confirms the complete80-byte function; the fresh far bitcount dossier confirms48 bytes. Original stack use remains an observation, not an original source declaration.

| Complete ordinary C control | Profile after AS | Bytes | Result |
| --- | --- | ---: | --- |
| Search-window baseline, only genuine result local | Zi |80|3 byte differences|
| Search-window consumed register boolean | Zi |82|67 differences|
| Same consumed register boolean | Os Zi |80|61 differences|
| Same consumed register boolean | Ox Zi |77|76 differences|
| Search-window consumed ordinary boolean | Os Zi |81|62 differences|
| Same consumed ordinary boolean | Ox Zi |78|20 differences|
| Unread-free whole-evaluation bitcount baseline | Gs Zi |48|4 differences|
| Consumed register parity-result local | Gs Os Zi |50|43 differences|
| Same consumed register parity-result local | Gs Ox Zi |53|Complete CV length already differs; original placement cannot link the complete object|

The controls establish one real compiler behavior: the consumed register boolean uses SI, with a4-byte reservation and the result at BP-4, while BP-2 is not accessed. Therefore, an unaccessed frame word need not imply an unread C variable. However, the additional SI saves/moves and changed argument pushes are visible in the generated instructions and absent from original A799. A consumed ordinary boolean emits its store at BP-2, also absent from the original. Size optimization does not remove the operations needed to explain these extra declarations. No full target function matches, and no withdrawn credit is restored.

The last Ox control preserves the entire genuine evaluation source. Its CODE becomes4090 bytes, and the bitcount public is at object offset3100, after its original CS offset2908. The strict linker correctly rejects a negative contribution origin. The complete53-byte CV extent, full CODE bytes, object, source and tool provenance remain retained; no rebasing, expected-size cropping or relocation-resolved equality is claimed for this row. The first failed artifact-collection run was recovered with a fresh final-only compilation, not counted as another hypothesis.

`evidence/register-frame-source-optimizer-control.json` contains all nine full sources/compiler commands/logs/tool pins/object hashes, complete CODE bytes, independent CV extents, raw and resolved fixups, original and complete linked bytes, and all differing positions for the eight linkable controls. It explicitly records the unsupported final placement. Reproducer: `build/register-frame-control/probe.py`; a single trial can be repeated by supplying its exact name. Comparison bindings are explicit observations, not a complete source-link layout. All emitted and original MZ sets are empty in the eight linked controls. The separate AS standalone search object retains its enclosing WORD-alignment obligation.

The own original REA session was saved and closed as `build/rea-register-frame-control.snapshot.json` (24 observations,20 primitive entries). No canonical source, registry, core backend or test file was changed. Historical compiler flags and source forms remain nonunique; further progress requires another independently meaningful source relationship or type/call interface, not reintroduction of unread padding declarations.
