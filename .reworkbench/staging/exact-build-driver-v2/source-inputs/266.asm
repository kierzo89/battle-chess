; Authored mutable data. CONST is native OMF class/name, not a C const qualifier.
bits 16
segment _TEXT public align=2 class=CODE use16
segment _DATA public align=2 class=DATA use16
segment CONST public align=2 class=CONST use16
global _dialog_actions_516c
_dialog_actions_516c:
db "Load", 0
db "Save", 0
segment _BSS public align=2 class=BSS use16
group DGROUP CONST _BSS _DATA
