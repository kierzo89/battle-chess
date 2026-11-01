# Complete source contexts and typed interfaces

Five new C procedures add902 verified code bytes: splash364, table selector44,
drive-file probing134, and two audio-asset routines188+172. Two complete typed
int definitions add the original COM1 values IRQ4/base03F8, totaling4 initialized
DATA bytes. None of this counts supplied runtime or assembly as authored C.
Current credit is172 C functions/33047B,89 DATA definitions/1211B,11 ASM/994B and
48 supplied runtime units/4206B. See generated progress and
`evidence/verification-172-contexts-checkpoint.json` for the verified run.

The canonical argument/splash source is src/argument_splash_flow_match.c. Its
complete432-byte CODE contribution consists of the existing67-byte argument
routine, new364-byte splash routine, and the genuine final90 at28AD. All29
compiler fields and the single MZ site2778 agree. The final byte earns no
function credit. Main now declares the same backing byte array far; its local
huge-pointer consumers retain correct advancement. The full580-byte main,
80 compiler fields and seven MZ sites remain unchanged. Both C5.00 and C5.10
reproduce the combined432 bytes; these bytes do not identify a unique producer.
Backing buffer allocation and historical ownership remain unresolved.

Three actual source contributions reproduce the contiguous1034-byte region
C868..CC71. src/audio_assets_flow_match.c emits360 bytes with188/172-byte native
procedures,27 fields and MZ sitesC91B/C9C6. Its byte cursor reads the binary
header through typed word casts; this explains the original register-loading
order without editing instructions. Actual far callback aliases10E3:0000 and
10E3:00F1 are retained even where automatic native target naming is misleading.

src/asset_drive_file_flow_match.c emits630 bytes for six complete procedures
fromC9D0 throughCC45, with58 fields and one MZ siteCC21. Its first public is
load_asset_index, matching the existing main caller atC9D0. The source preserves
actual zero/one-word calls through the legacy exit_07f3 declaration; no fully
typed whole-program exit ABI claim is made. The separate table selector in
src/asset_table_select_match.c emits44 bytes and nine fields with no MZ sites.
All three contributions begin/end at legal even WORD boundaries. There are no
inserted gaps, padding locals, SEGDEF edits or output patches.

The first two contributions use C5 `/AS /Os /Zi`; the table selector uses
`/AS /Zi`. The bounded controls matter: default drive probing is140 rather than
134 bytes; the five file helpers emit528 rather than496 default bytes. Applying
/Os to the final selector instead emits42 rather than44 bytes. Six natural
procedures can therefore share630 exact CODE bytes; the selector remains a
separate genuine contribution. This is reproducible source configuration,
not proof of historical filenames or original object ordering.

The graphics fill declarations now match the actual char formal. Both original
calls pass zero; complete graphics CODE, all22 procedure extents and15 credited
functions/2761B remain unchanged. The move probe and its state caller now pass
the real Move8 record by value; apply_9749 receives that record plus undo2. The
original pushes and cleanup prove exactly this word layout. Both complete CODE
contributions,14 credited functions/1299B and all their fields/MZ sites remain
unchanged. This does not restore the uncredited apply routine or other frame
candidates. All14 retired padding-dependent procedures remain uncredited.

Initial170-state production/test runs were deliberately interrupted with exit130
when the C9D0 naming mismatch was found. Those logs are preserved. C360 and the
natural630 source grouping were incorporated before fresh172-state checks.
The canonical sources and registry stayed frozen during the final full run.
The earlier17-test targeted main qualifier check also passes independently.

All339 regression tests pass in543.136seconds. The ledger now derives all89
DATA definitions from the registry and authenticates their coordinates against
the pinned CRT0 frame; it no longer carries forward the earlier87-entry list.
This bookkeeping repair changes no compiled game bytes.

The full checker verifies320 entries and correctly exits1 because no complete
independently source-built executable exists. File spans38077/83415=45.648% and
expanded spans39458/401131 are partial coverage, not a whole-program completion
percentage. Source MZ sites44 plus runtime2 give46/173. Initialized DATA gains
no packed-file credit. Independent source-link controls/inventories likewise
receive no extra matching credit.

Root's two typed clipping mask arrays16B pass exact whole DATA and native
index/word-width checks but remain unregistered. Their actual renderer native
body proves index&3 and word loads; it receives no restored C credit. See
`evidence/clipping-mask-data-match.json`. Other pending work and unresolved full
source layout are recorded in next-work.md.

The actual audio source also passes authentic LINK in two object orders with
genuine SLIBC+LIBH, complete360-byte CODE/27-field/two-MZ agreement and executed
far recording callbacks. Independent raw pointer-word observations agree with
actual MAP coordinates across64KiB. Driver callbacks and synthetic storage are
explicit fixtures, not a real sound-device or original allocation claim. See
audio-source-link-control.md. Two more matching dialog helpers326B are pending;
D551 needs enclosing alignment context. The main dialogCC72 stays uncredited
with a retained614-versus610-byte negative.
