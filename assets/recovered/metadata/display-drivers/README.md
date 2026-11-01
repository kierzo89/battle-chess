# Native display profiles

`report.json` and `rea-08.json` through `rea-12.json` inventory every driver selected by the original `startup[8 + palette_mode]` loader. Each full module is hash-checked against the exact ALLCANM1 partition and a fresh REA provider read. The four far entry jump targets are recorded, without misclassifying embedded tables as instructions.

Reproduce: `matching/build/test-env/bin/python -B asset_recovery/display_profiles_v1/verify.py`.

Five bounded native entry-0 executions pass independent output comparisons for all 256 packed source byte values (512 input bytes/four aligned rows). This is an asset-index/driver proof, not an RGB monitor capture. No palette, matching or canonical credit is granted.

| palette_mode | bank record | loader BIOS mode | verified entry-0 operation |
|---|---|---|---|
| 0 | startup08 | 04h | Two retained 256-byte tables combine two packed source bytes into one CGA byte; banked B800 destinations |
| 1 | startup09 | 0Dh | Four separate bitplanes selected through 3C4/3C5 and 3CE/3CF; source nibbles preserved as four plane bits |
| 2 | startup10 | 09h | Packed bytes copied unchanged to four-way banked B800 destinations |
| 3 | startup11 | 04h initially | First copy calls BIOS mode06h and writes 1Ah to port3D8; two conversion tables produce composite bit patterns; second call does not reinitialize |
| 4 | startup12 | 13h | High nibble then low nibble copied unchanged as individual A000 pixel indices |

CGA, EGA, Tandy/PCjr and VGA names describe the corresponding native address/port/mode conventions. The actual physical adapter, display and analogue colour response are not asserted by these fixtures. In particular `/comp` is **not merely another RGB palette**: entry0 changes the video mode and CGA mode-control register, and its converted bit patterns need a composite signal/display model.

The matched main sets `palette_mode=3` for `/comp`, otherwise starts at0 and lets `initialize_video(0)` detect hardware. The matched hardware routine selects mode2 for its ROM test, otherwise sets `mode_11aa=1` and probes BIOS1A00h before EGA12h/BL10h. Native VGA detection accepts AL=1Ah regardless of BL (the compare branches converge); this behaviour must not be silently replaced with a modern capability check. `mode_11aa` also selects asset/audio bank families and is distinct from display `palette_mode`.

Remaining finite obligations:

1. Obtain the actual default BIOS palette/register state after modes04h,0Dh and09h for a specified target BIOS; bind it to adapter identity. The supplied module fixtures neither execute BIOS nor assign physical RGB values. VGA mode13h capture is a separate existing parent stage.
2. Bind the startup11 mode06h/3D8=1Ah bit patterns to a documented or captured composite decoder/monitor profile. Preserve raw bit patterns independently of any chosen visualization.
3. Exercise the other three driver entrypoints and alignment/clipping branches with device-aware fixtures. EGA proof here uses aligned whole-byte rows and reconstructs plane writes from native port selection; it does not claim full latch/read-map emulation.
4. End-to-end capture of loader selection and first display call on each supported hardware/BIOS configuration. Current loader selection is tied to matched source hashes rather than a fresh BIOS execution.

The separate startup03 64-byte suffix remains opaque: this stage supplies no consumer establishing that it is a palette. Source-index recovery and exact container recovery do not depend on inventing that interpretation.
