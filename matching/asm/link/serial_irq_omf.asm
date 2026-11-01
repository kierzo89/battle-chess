; Genuine contiguous serial context: two far API entries, IRQ body and saved DS word.
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _serial_irq:WORD, _serial_base:WORD
EXTRN _byte_write_cursor:WORD, _byte_read_cursor:WORD
EXTRN _byte_ring_buffer:BYTE, _serial_ring_end_2eba:WORD
EXTRN _serial_irq_flags_b0d4:BYTE
_DATA ENDS
DGROUP GROUP _DATA
SERIAL_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:SERIAL_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _set_serial_format_10d3_0000, _enable_serial_irq_10d3_0023
_set_serial_format_10d3_0000 PROC FAR
    push bp
    mov bp, sp
    push si
    push di
    sub dx, dx
    cmp _serial_base, 3f8h
    je serial_bios_ready
    mov dl, 1
serial_bios_ready:
    mov al, [bp+6]
    sub ah, ah
    int 14h
    mov dx, _serial_base
    mov dl, 0f8h
    in al, dx
    pop di
    pop si
    pop bp
    retf
_set_serial_format_10d3_0000 ENDP
_enable_serial_irq_10d3_0023 PROC FAR
    push ds
    push si
    push di
    mov cs:_serial_saved_ds_10d3_00b4, ds
    mov si, _serial_irq
    shl si, 1
    shl si, 1
    add si, 20h
    mov dx, _serial_base
    sub ax, ax
    mov ds, ax
    mov word ptr [si], OFFSET _serial_irq_handler_10d3_006d
    mov [si+2], cs
    mov bx, dx
    mov dl, 0fbh
    in al, dx
    and al, 7fh
    out dx, al
    mov dl, 0f9h
    mov al, 1
    out dx, al
    mov dl, 0fch
    mov al, 8
    out dx, al
    mov cx, ss:_serial_irq
    mov ah, 1
    shl ah, cl
    not ah
    in al, 21h
    and al, ah
    out 21h, al
    sti
    pop di
    pop si
    pop ds
    retf
_enable_serial_irq_10d3_0023 ENDP
_serial_irq_handler_10d3_006d PROC FAR
    sti
    push ds
    push ax
    push bx
    push dx
    mov ax, cs:_serial_saved_ds_10d3_00b4
    mov ds, ax
    mov bx, _byte_write_cursor
    mov dx, _serial_base
    mov dl, 0fdh
    in al, dx
    and al, 0eh
    or _serial_irq_flags_b0d4, al
    mov dl, 0f8h
    in al, dx
    mov [bx], al
    inc bx
    cmp bx, _serial_ring_end_2eba
    jb serial_ring_inside
    mov bx, OFFSET _byte_ring_buffer
serial_ring_inside:
    cmp bx, _byte_read_cursor
    jne serial_ring_publish
    or _serial_irq_flags_b0d4, 40h
    mov bx, _byte_write_cursor
serial_ring_publish:
    mov _byte_write_cursor, bx
    mov al, 20h
    out 20h, al
    pop dx
    pop bx
    pop ax
    pop ds
    iret
_serial_irq_handler_10d3_006d ENDP
_serial_saved_ds_10d3_00b4 DW 0
SERIAL_TEXT ENDS
END
