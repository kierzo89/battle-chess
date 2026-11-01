; Independent far-call mixing function in a distinct leading CODE segment.
BITS 16
SEGMENT FRAME_TEXT PUBLIC ALIGN=16 CLASS=CODE USE16
GLOBAL _frame_prefix
_frame_prefix:
    push bp
    mov bp, sp
    push bx
    mov ax, [bp+6]
    mov bx, ax
    xor ax, 0x5a5a
    rol ax, 1
    add ax, bx
    xor ax, 0x1357
    ror ax, 1
    sub ax, bx
    neg ax
    pop bx
    pop bp
    retf
