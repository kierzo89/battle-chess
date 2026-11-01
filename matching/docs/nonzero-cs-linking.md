# Separate CS offsets and physical image positions

The evaluator's original alias `0FDF:0D25` identifies physical image `10B15`.
Near calls use offsets within CS; file comparisons and MZ relocation positions
use physical image positions. Treating both as a single address produces wrong
near-call displacements once CS has a nonzero image base.

`link16.link_function` retains its strict 16-bit `origin` argument and accepts
an optional `image_origin`. Their difference must be a valid paragraph-aligned
real-mode segment base. The checker records explicit `code_address` segment
and offset for nonzero-CS C units, validates their physical mapping and full
extent, and passes both coordinates. Existing CS0 units keep their old behavior.
Every relocation records its physical location; nonzero-CS records also retain
the code offset and frame base. No reference bytes are masked or patched.

[nonzero-cs-link-experiment.json](../evidence/nonzero-cs-link-experiment.json)
independently checks this arithmetic against authentic pinned LINK 3.65.
The [reproducer](../evidence/nonzero-cs-link-probe.py) freshly compiles ordinary
C procedures and a separate initialized state source, assembles a meaningful
far XOR/rotate helper, and links them with pinned SLIBC. The isolated DOSBox
mounts contain only these objects and verified tools, without original CHESS
or expanded reference bytes. These control executables receive zero matching
credit.

Both ordinary LINK and `/DOSSEG` runs place the C segment at CS0001 and the
preceding helper at CS0000. All three complete generated C procedures match
authentic LINK after the restricted linker uses the real map placements.
The cross-CS far pointer's MZ segment field is at image0051, rather than
CS-relative0041. Main's near call encodes displacement FFD2. A negative control
deliberately substitutes the physical position for its CS offset and emits
FFC2, confirming the experiment distinguishes the two calculations.

Five focused tests cover nonzero-CS near arithmetic, own-CODE public targets,
physical MZ locations, invalid frame mappings and checker registry validation.
All150 repository tests pass. This establishes coordinate handling, not the
complete original object order, helper placements, DGROUP layout or full EXE.
