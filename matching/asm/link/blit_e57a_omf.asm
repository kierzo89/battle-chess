; Compatible symbolic reconstruction of the dependency-closed native blitter.
; The original source/module boundary is not claimed.
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _blit:BYTE
_DATA ENDS
DGROUP GROUP _DATA
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _blit_e57a
width_words DW 0
height_rows DW 0
source_skip DW 0
destination_skip DW 0
left_mask DW 0
right_mask DW 0
; For each packed byte, preserve destination nibbles whose source is zero.
transparency_mask LABEL BYTE
mask_index = 0
REPT 256
mask_value = 0
IF (mask_index AND 0F0H) EQ 0
mask_value = mask_value OR 0F0H
ENDIF
IF (mask_index AND 0FH) EQ 0
mask_value = mask_value OR 0FH
ENDIF
DB mask_value
mask_index = mask_index + 1
ENDM
; Exactly six actual mode/alignment targets. Native callers use modes zero..two.
dispatch_table DW OFFSET copy_aligned, OFFSET copy_shifted
               DW OFFSET transparent_aligned, OFFSET transparent_shifted
               DW OFFSET xor_aligned, OFFSET xor_shifted
_blit_e57a PROC NEAR
    push ds
    push si
    push di
    push bp
    mov dx, word ptr _blit
    mov cx, word ptr _blit+2
    mov ax, word ptr _blit+4
    or ax, ax
    jnz width_nonzero
    jmp restore
width_nonzero:
    mov cs:width_words, ax
    mov ax, word ptr _blit+6
    or ax, ax
    jnz height_nonzero
    jmp restore
height_nonzero:
    mov cs:height_rows, ax
    mov ax, word ptr _blit+8
    mov cs:source_skip, ax
    mov ax, word ptr _blit+10
    mov cs:destination_skip, ax
    les di, dword ptr _blit+16
    mov ax, word ptr _blit+12
    mov bx, word ptr _blit+14
    test dx, 2
    jz destination_ready
    inc di
destination_ready:
    mov cs:left_mask, ax
    mov cs:right_mask, bx
    lds si, dword ptr _blit+20
    shl cx, 1
    mov bx, dx
    and bx, word ptr 1
    or bx, cx
    shl bx, 1
    mov ax, si
    mov cx, ds
    shr ax, 1
    shr ax, 1
    shr ax, 1
    shr ax, 1
    add ax, cx
    sub ax, 800h
    mov ds, ax
    and si, word ptr 0fh
    add si, 8000h
    jmp word ptr cs:dispatch_table[bx]
copy_aligned:
    mov cx, cs:width_words
    lodsw
    and ax, cs:left_mask
    dec cx
    jz copy_aligned_last
copy_aligned_loop:
    stosw
    lodsw
    loop copy_aligned_loop
copy_aligned_last:
    and ax, cs:right_mask
    stosw
    add si, cs:source_skip
    add di, cs:destination_skip
    dec cs:height_rows
    jnz copy_aligned
    jmp restore
copy_shifted:
    mov cx, cs:width_words
    xor dx, dx
    lodsw
    and ax, cs:left_mask
    dec cx
    jz copy_shifted_last
copy_shifted_loop:
    ror ax, 1
    ror ax, 1
    ror ax, 1
    ror ax, 1
    mov dl, al
    and al, 0fh
    or al, dh
    mov dh, dl
    and dh, 0f0h
    stosw
    lodsw
    loop copy_shifted_loop
copy_shifted_last:
    and ax, cs:right_mask
    ror ax, 1
    ror ax, 1
    ror ax, 1
    ror ax, 1
    mov dl, al
    and al, 0fh
    or al, dh
    mov dh, dl
    and dh, 0f0h
    stosw
    add si, cs:source_skip
    add di, cs:destination_skip
    dec cs:height_rows
    jnz copy_shifted
    jmp restore
transparent_aligned:
    mov bx, OFFSET transparency_mask
transparent_aligned_row:
    mov cx, cs:width_words
    lodsw
    and ax, cs:left_mask
    dec cx
    jz transparent_aligned_last
transparent_aligned_loop:
    mov bp, ax
    xlat cs:transparency_mask
    xchg al, ah
    xlat cs:transparency_mask
    xchg al, ah
    and ax, es:[di]
    or ax, bp
    stosw
    lodsw
    loop transparent_aligned_loop
transparent_aligned_last:
    and ax, cs:right_mask
    mov bp, ax
    xlat cs:transparency_mask
    xchg al, ah
    xlat cs:transparency_mask
    xchg al, ah
    and ax, es:[di]
    or ax, bp
    stosw
    add si, cs:source_skip
    add di, cs:destination_skip
    dec cs:height_rows
    jnz transparent_aligned_row
    jmp restore
transparent_shifted:
    mov bx, OFFSET transparency_mask
transparent_shifted_row:
    mov cx, cs:width_words
    xor dx, dx
    lodsw
    and ax, cs:left_mask
    dec cx
    jz transparent_shifted_last
transparent_shifted_loop:
    ror ax, 1
    ror ax, 1
    ror ax, 1
    ror ax, 1
    mov dl, al
    and al, 0fh
    or al, dh
    mov dh, dl
    and dh, 0f0h
    mov bp, ax
    xlat cs:transparency_mask
    xchg al, ah
    xlat cs:transparency_mask
    xchg al, ah
    and ax, es:[di]
    or ax, bp
    stosw
    lodsw
    loop transparent_shifted_loop
transparent_shifted_last:
    and ax, cs:right_mask
    ror ax, 1
    ror ax, 1
    ror ax, 1
    ror ax, 1
    mov dl, al
    and al, 0fh
    or al, dh
    mov dh, dl
    and dh, 0f0h
    mov bp, ax
    xlat cs:transparency_mask
    xchg al, ah
    xlat cs:transparency_mask
    xchg al, ah
    and ax, es:[di]
    or ax, bp
    stosw
    add si, cs:source_skip
    add di, cs:destination_skip
    dec cs:height_rows
    jnz transparent_shifted_row
    jmp restore
xor_aligned:
    mov cx, cs:width_words
    lodsw
    and ax, cs:left_mask
    dec cx
    jz xor_aligned_last
xor_aligned_loop:
    xor ax, es:[di]
    stosw
    lodsw
    loop xor_aligned_loop
xor_aligned_last:
    and ax, cs:right_mask
    xor ax, es:[di]
    stosw
    add si, cs:source_skip
    add di, cs:destination_skip
    dec cs:height_rows
    jnz xor_aligned
    jmp restore
xor_shifted:
    mov cx, cs:width_words
    xor dx, dx
    lodsw
    and ax, cs:left_mask
    dec cx
    jz xor_shifted_last
xor_shifted_loop:
    ror ax, 1
    ror ax, 1
    ror ax, 1
    ror ax, 1
    mov dl, al
    and al, 0fh
    or al, dh
    mov dh, dl
    and dh, 0f0h
    xor ax, es:[di]
    stosw
    lodsw
    loop xor_shifted_loop
xor_shifted_last:
    and ax, cs:right_mask
    ror ax, 1
    ror ax, 1
    ror ax, 1
    ror ax, 1
    mov dl, al
    and al, 0fh
    or al, dh
    mov dh, dl
    and dh, 0f0h
    xor ax, es:[di]
    stosw
    add si, cs:source_skip
    add di, cs:destination_skip
    dec cs:height_rows
    jnz xor_shifted
restore:
    pop bp
    pop di
    pop si
    pop ds
    ret
_blit_e57a ENDP
_TEXT ENDS
END
