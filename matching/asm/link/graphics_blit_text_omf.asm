; Compatible symbolic reconstruction of the dependency-closed native blitter.
; The original source/module boundary is not claimed.
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _blit:BYTE
EXTRN _text_colour_words:WORD, _text_glyph_pixels:BYTE
EXTRN _text_cursor:WORD, _font_glyphs:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _color_buffer:BYTE
EXTRN _graphics_begin:FAR, _graphics_end:FAR, _graphics_copy:FAR
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
; Compatible symbolic graphics context, not a historical source boundary claim.
; The complete lookup domain is the byte consumed by CS:XLAT.
colour_index = 0
colour_translation LABEL BYTE
REPT 256
colour_result = colour_index
IF (colour_index AND 0FH) EQ 1
colour_result = (colour_result AND 0F0H) OR 4
ENDIF
IF (colour_index AND 0F0H) EQ 10H
colour_result = (colour_result AND 0FH) OR 40H
ENDIF
IF (colour_index AND 0FH) EQ 9
colour_result = (colour_result AND 0F0H) OR 0CH
ENDIF
IF (colour_index AND 0F0H) EQ 90H
colour_result = (colour_result AND 0FH) OR 0C0H
ENDIF
DB colour_result
colour_index = colour_index + 1
ENDM
PUBLIC _prepare_pixels_e8cb, _draw_text_e915
_prepare_pixels_e8cb PROC NEAR
    push bp
    mov bp, sp
    push si
    push di
    mov ax, SEG _color_buffer
    mov es, ax
    mov di, OFFSET _color_buffer
    mov ax, [bp+8]
    mul word ptr [bp+10]
    shr ax, 1
    mov cx, ax
    lds si, [bp+4]
    mov ax, si
    mov bx, ds
    shr ax, 1
    shr ax, 1
    shr ax, 1
    shr ax, 1
    add ax, bx
    sub ax, 800h
    mov ds, ax
    and si, WORD PTR 0fh
    add si, 8000h
    mov bx, OFFSET colour_translation
translate_pair:
    lodsb
    xlat cs:colour_translation
    stosb
    lodsb
    xlat cs:colour_translation
    stosb
    loop translate_pair
    mov ax, ss
    mov ds, ax
    pop di
    pop si
    pop bp
    ret
_prepare_pixels_e8cb ENDP
_draw_text_e915 PROC NEAR
    call _graphics_begin
    push bp
    mov bp, sp
    push si
    push di
    mov ax, ds
    mov es, ax
    mov ax, [bp+6]
    shr ax, 1
    mov _text_cursor, ax
    mov ax, [bp+8]
    mov _text_cursor+2, ax
    mov si, [bp+4]
    mov dx, [si]
    mov bx, dx
    shl bx, 1
    shl bx, 1
    shl bx, 1
    shl bx, 1
    mov di, OFFSET _text_colour_words
    mov ah, dh
    or ah, bh
    mov al, ah
    stosw
    mov ah, dl
    or ah, bh
    stosw
    mov ah, dh
    or ah, bl
    stosw
    mov ah, dl
    or ah, bl
    stosw
    mov al, dl
    or al, bh
    mov ah, dh
    or ah, bh
    stosw
    mov ah, dl
    or ah, bh
    stosw
    mov ah, dh
    or ah, bl
    stosw
    mov ah, dl
    or ah, bl
    stosw
    mov al, dh
    or al, bl
    mov ah, dh
    or ah, bh
    stosw
    mov ah, dl
    or ah, bh
    stosw
    mov ah, dh
    or ah, bl
    stosw
    mov ah, dl
    or ah, bl
    stosw
    mov al, dl
    or al, bl
    mov ah, dh
    or ah, bh
    stosw
    mov ah, dl
    or ah, bh
    stosw
    mov ah, dh
    or ah, bl
    stosw
    mov ah, dl
    or ah, bl
    stosw
    mov si, [si+2]
next_character:
    lodsb
    test al, al
    jnz draw_character
    pop di
    pop si
    pop bp
    call _graphics_end
    ret
draw_character:
    push si
    xor ah, ah
    sub al, 20h
    shl ax, 1
    shl ax, 1
    shl ax, 1
    mov bx, OFFSET _font_glyphs
    add bx, ax
    mov di, OFFSET _text_glyph_pixels
    mov dx, OFFSET _text_colour_words
    mov cx, 4
glyph_pair:
    mov ax, [bx]
    inc bx
    inc bx
    mov si, ax
    shr si, 1
    shr si, 1
    shr si, 1
    and si, WORD PTR 1eh
    add si, dx
    movsw
    mov si, ax
    shl si, 1
    and si, WORD PTR 1eh
    add si, dx
    movsw
    mov al, ah
    mov si, ax
    shr si, 1
    shr si, 1
    shr si, 1
    and si, WORD PTR 1eh
    add si, dx
    movsw
    mov si, ax
    shl si, 1
    and si, WORD PTR 1eh
    add si, dx
    movsw
    loop glyph_pair
    push ds
    mov ax, OFFSET _text_glyph_pixels
    push ax
    mov ax, 8
    push ax
    mov ax, 4
    push ax
    push _text_cursor+2
    mov ax, _text_cursor
    push ax
    add ax, 4
    mov _text_cursor, ax
    call _graphics_copy
    add sp, 12
    pop si
    mov ax, ds
    mov es, ax
    jmp next_character
_draw_text_e915 ENDP

_TEXT ENDS
END
