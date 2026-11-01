; E3BA..E3E9. Restore the bit window; refill through the shared input helper.
bits 16
cpu 8086
org 0xe3ba
    mov dx,[0x30c2]
    mov cx,[0x30c4]
    cmp cl,8
    jg .ready
    rol dx,cl
    mov si,[0x30c6]
    cmp si,0x30c2
    jne .first_byte
    call 0xe3ea
.first_byte:
    lodsb
    db 0x8a,0xf0 ; mov dh,al, original register-load encoding
    cmp si,0x30c2
    jne .rotate_back
    call 0xe3ea
.rotate_back:
    ror dx,cl
    add cl,8
.ready:
    db 0x8a,0xe9 ; mov ch,cl, original register-load encoding
    ret
