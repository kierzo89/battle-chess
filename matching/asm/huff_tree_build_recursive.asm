; Original image E077..E0A8. Preorder Huffman tree: zero=branch, one=leaf.
; DX holds the code, BX its depth; each leaf reads a byte into DI and
; stores (code, depth) at DS:30CC+4*DI. Depth >16 calls the INT3 at E410.
bits 16
cpu 8086
org 0xe077

    call 0xe0b6
    jc .leaf
    shl dx, 1
    inc bx
    call 0xe077
    call 0xe0b6
    or dl, 1
    call 0xe077
    shr dx, 1
    dec bx
    ret
.leaf:
    call 0xe0a8
    db 0x03, 0xff              ; add di,di: retail uses reg<-r/m direction
    db 0x03, 0xff              ; add di,di: same alternate encoding
    add di, 0x30cc
    mov [di], dx
    mov [di+2], bx
    cmp bx, byte 16
    jle .done
    call 0xe410
.done:
    ret
