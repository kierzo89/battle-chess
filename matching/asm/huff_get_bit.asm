; Original image E0B6..E0D8. Input AX=shift register, CL=bits left,
; DS:SI=next input word; output bit in carry, updated AX/CL/SI.
; DF must be clear. At SI=30C2, refill the input via E3EA.
bits 16
cpu 8086
org 0xe0b6

    db 0x0a, 0xc9              ; or cl,cl: retail uses reg<-r/m direction
    jz .empty
    dec cl
    shl ax, 1
    ret
.empty:
    cmp si, 0x30c2
    jz .refill
    lodsw
    xchg al, ah
    mov cl, 15
    shl ax, 1
    ret
.refill:
    call 0xe3ea
    lodsw
    xchg al, ah
    mov cl, 15
    shl ax, 1
    ret
