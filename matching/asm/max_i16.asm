; CHESS.EXE load-image [0x8fa5, 0x8fb5), near cdecl signed maximum.
BITS 16
CPU 8086
ORG 0x8fa5

max_i16:
    push bp
    db 0x8b, 0xec              ; mov bp, sp (retail direction encoding)
    mov ax, [bp + 4]
    cmp ax, [bp + 6]
    jge short .done
    mov ax, [bp + 6]
.done:
    pop bp
    ret
