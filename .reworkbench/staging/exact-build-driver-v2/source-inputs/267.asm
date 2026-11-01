; Authored mutable data. CONST is native OMF class/name, not a C const qualifier.
bits 16
segment _TEXT public align=2 class=CODE use16
segment _DATA public align=2 class=DATA use16
segment CONST public align=2 class=CONST use16
global _dialog_strings
_dialog_strings:
db "Load", 0
db "---------", 0
db "Done", 0
db "Cancel", 0
db "Chess.sav", 0
db "Cancel", 0
db "Done", 0
db "Cancel", 0
db "Done", 0
segment _BSS public align=2 class=BSS use16
group DGROUP CONST _BSS _DATA
