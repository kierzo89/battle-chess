; CHESS.EXE load-image [0x8fb5, 0x8fca), near cdecl signed absolute value.
BITS 16
CPU 8086
ORG 0x8fb5

abs_i16:
    push bp
    db 0x8b, 0xec              ; mov bp, sp (retail direction encoding)
    cmp word [bp + 4], 0
    jle short .nonpositive
    mov ax, [bp + 4]
    pop bp
    ret
.nonpositive:
    mov ax, [bp + 4]
    neg ax
    pop bp
    ret
