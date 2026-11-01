# Game-determined logical display selection

The verifier executes the original expanded executable's `initialize_video` at image offset11012h, including its actual far call to hardware detection. The immutable CHESS.EXE and expanded-carrier hashes are checked. It does not substitute reconstructed C for the native function. ROM bytes and BIOS interrupt responses are explicit fixture inputs. DOS critical-vector get/set operations are intercepted and checked.

Run `matching/build/test-env/bin/python -B asset_recovery/logical_display_selection_v1/verify.py`.

**182 native cases pass**, covering all five display choices and predicate boundaries. The report retains exact requested BIOS AX/BX values, input ROM/BIOS values, selected driver, and resulting asset-family byte. No direct port output occurs in this platform-init routine. First-copy driver requests and exact shipped translation tables are carried forward from the separately verified display_profiles_v1 stage.

## Determined by game data and native code

- `/comp` sets palette_mode3. Nonzero init argument skips adapter detection, requests BIOS mode04h and leaves the asset-family byte unchanged. Driver11's first copy requests mode06h and writes1Ah to3D8; subsequent copies do not repeat this initialization.
- ROM F000:FFFE=FDh, or F000:C000=21h, selects palette_mode2 and asset-family0, requests09h and selects startup10.
- Otherwise asset-family1 is selected. BIOS1A00h returning AL=1Ah selects palette_mode4 and mode13h/startup12. Every tested BL, including0 andFFh, is accepted by the native converging branches.
- Otherwise BIOS12h with input BL10h selects palette_mode1/mode0Dh/startup09 only if returned BL differs from10h and BH=0. Other responses select palette_mode0/mode04h/startup08.
- Driver08 and driver11 each supply two complete256-byte conversion tables at module offsets1A0h/2A0h. Their exact1024 total bytes are retained in report.json, with module and table hashes. These are packed-pixel transformations, not RGB triples.
- Driver09 maps original nibble bits to four EGA planes. Driver10 retains packed nibbles; driver12 expands each nibble to an index. These logical transformations were independently compared with native output in display_profiles_v1.

## Inputs supplied outside stored assets

The requested BIOS modes establish adapter defaults through that BIOS implementation. Default attribute registers, palette registers and DAC contents are not loaded as RGB triples by the traced platform-init or entry0 driver paths. Their concrete values require the chosen BIOS/adapter; the existing VGA capture stage supplies a separate concrete VGA environment. Composite display colour response is additionally a hardware/signal transfer function. It is not a missing recoverable sprite palette and must not be invented as asset data.

Logical asset indices, conversion tables and init requests are now recovered for all five profiles. Remaining other-entrypoint/alignment validation is renderer-engine coverage, not absent image indices. Physical-colour exports for other adapters can be offered only with an explicitly named external BIOS/display profile. This stage does not prove absence of palette operations on every unexecuted renderer path; it closes the finite init/entry0 selection and mapping scope only. Startup03's64-byte suffix remains opaque, without a demonstrated native palette consumer.

Frozen stages, original files, canonical admission and Workbench were not changed. REA session closed after collecting the preceding module evidence.
