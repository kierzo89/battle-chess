# Recovered Battle Chess assets

The recovered original game data and a portable bank reconstruction package.
Asset recovery is complete for the inventoried assets, with the explicit context
limits below. This does not grant any rights to third-party artwork or audio.

## Browse the assets

- [recovered/images/](recovered/images/): 2,441 source frame instances in original
  and recoloured variants, plus four backgrounds. Variants are not unique sprites.
- [recovered/animations/](recovered/animations/) and [recovered/setups/](recovered/setups/):
  indexed pixels, dimensions, anchors and sequence metadata.
- [recovered/font/](recovered/font/): 128 physical 8×8 font blocks and atlas.
- [recovered/audio/](recovered/audio/) and [recovered/audio-context/](recovered/audio-context/):
  lossless audio commands/amplitudes and playback-context limits.
- [recovered/metadata/](recovered/metadata/): record, timing, task and display metadata.
- [recovered/rebuilt/](recovered/rebuilt/): the exact reconstructed game banks.
- [evidence/](evidence/): retained completion audit, catalog and bundle validation.

## Rebuild the game data

From the repository root, using Python 3 and a **new** output directory:

```sh
python3 -I -B assets/bank-rebuild/rebuild.py --output /tmp/battle-chess-banks-new
python3 tools/verify_asset_snapshot.py
```

The portable package reconstructs both files from decoded symbols, raw records
and retained codec metadata without reading the original banks. No proprietary
compiler is needed for this step. Put the rebuilt `ALLCANM1` and `ALLCANM2`
files beside `CHESS.EXE` in the game's runtime directory. The game loads them as
external data; the PNG previews are not compiled into the executable.

Expected SHA-256:

- ALLCANM1 (185,726 bytes): `aa50ef9fb55e5271526e25ccc6e60b2908f00440c3f33380d13d27ecd4cbc564`
- ALLCANM2 (339,592 bytes): `114a46f323f6766396eba42bd741768e415ded55685ee0778f127a48377c084d`

The repacker verifies the recovered original inputs. It is not a general editor
for changed artwork. Byte-exact executable compilation still needs the external
toolchain and evidence described in the repository's main README.

## Interpretation and evidence limits

Sprite index zero is transparent; background zero is opaque. Stored row padding,
nominal widths and signed anchors matter for placement. Audio is not presented as
WAV with an invented sample rate. Animation timing uses eligible task calls and
BIOS ticks, not a fixed FPS. Non-VGA BIOS palettes and physical display behaviour
need an external hardware profile; undefined audio tails need arena history.
Opaque fields are preserved exactly, without claiming their purpose is known.

The recovered run and evidence are copied unchanged, so reports retain original
workspace paths and may refer to native experiments outside this publication.
The snapshot verifier proves the published file hashes; it does not rerun every
native experiment. The standalone bank rebuilder is portable and independently
checks the exact bank hashes. No executable or C matching credit is added here.
