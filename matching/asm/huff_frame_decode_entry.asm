; REA ev_33bd61ebfc0b5f3015d68638aa016599921bdd95176bfaa204c0ffa3184e0df2.
; E03A..E077. Refill; read output count; skip four header bytes; clear
; code/depth table, build tree, persist bit-reader state, build lookup.
bits 16
cpu 8086
org 0xe03a

    push bp
    push si
    push di
    call 0xe3ea
    lodsw
    mov [0x30c8], ax
    lodsw
    mov [0x30ca], ax
    add si, byte 4
    mov ax, ds
    mov es, ax
    mov di, 0x30cc
    db 0x2b, 0xc0              ; sub ax,ax, retail direction encoding
    mov cx, 0x200
    rep stosw
    lodsw
    xchg al, ah
    db 0x2b, 0xdb              ; sub bx,bx, retail direction encoding
    mov cl, 16
    db 0x2b, 0xd2              ; sub dx,dx, retail direction encoding
    call 0xe077
    mov [0x30c6], si
    mov [0x30c2], ax
    mov [0x30c4], cl
    call 0xe0d8
    pop di
    pop si
    pop bp
    ret
