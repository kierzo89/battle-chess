; CHESS.EXE load-image [0x8f95, 0x8fa5), near cdecl signed minimum.
BITS 16
CPU 8086
ORG 0x8f95

min_i16:
    push bp
    db 0x8b, 0xec              ; mov bp, sp (retail direction encoding)
    mov ax, [bp + 4]
    cmp ax, [bp + 6]
    jle short .done
    mov ax, [bp + 6]
.done:
    pop bp
    ret
