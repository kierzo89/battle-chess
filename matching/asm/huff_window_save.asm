; E394..E3B9. Internal stack adaptor: pop return IP and bit count,
; initialize input state, restore a stack slot, and jump to saved IP in DX.
bits 16
cpu 8086
org 0xe394
    pop dx
    pop cx
    push si
    call 0xe3ea
    lodsw
    xchg al,ah
    rol ax,cl
    sub cx,byte 16
    neg cx
    mov [0x30c2],ax
    mov [0x30c4],cx
    mov [0x30c6],si
    mov byte [0x44df],0
    pop si
    sub sp,byte 2
    jmp dx
