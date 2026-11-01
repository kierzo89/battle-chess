; Relocatable source-link form of the nine already credited Huffman functions.
; No ORG, storage definitions, target aliases or binary inclusion.
; Narrow annotated DB pairs select individual register-load instruction encodings
; that NASM cannot select by mnemonic; no address operand is emitted with DB.
bits 16
cpu 8086
group DGROUP
segment _TEXT public align=2 class=CODE use16
global _prepare_asset_decode
global _huff_tree_build_recursive
global _huff_read_byte
global _huff_get_bit
global _huff_build_lookup
global _huff_frame_decode
global _huff_decode_stream
global _huff_window_save
global _huff_window_init
extern _huff_refill_e3ea
extern _huff_depth_trap_e410
extern _huff_shift_word
extern _huff_bits_left
extern _huff_input_cursor
extern _huff_remaining
extern _huff_code_table:wrt DGROUP
extern _huff_fast_lookup:wrt DGROUP
extern _huff_long_records:wrt DGROUP
extern _huff_long_masks
extern _huff_prefix_byte
extern _huff_pending_count
extern _huff_saved_extent
extern _huff_checksum

_prepare_asset_decode:
    push bp
    push si
    push di
    call _huff_refill_e3ea
    lodsw
    mov [_huff_remaining], ax
    lodsw
    mov [_huff_remaining+2], ax
    add si, byte 4
    mov ax, ds
    mov es, ax
    mov di, _huff_code_table
    db 0x2b, 0xc0 ; sub ax,ax, retail direction encoding
    mov cx, 0x200
    rep stosw
    lodsw
    xchg al, ah
    db 0x2b, 0xdb ; sub bx,bx, retail direction encoding
    mov cl, 16
    db 0x2b, 0xd2 ; sub dx,dx, retail direction encoding
    call _huff_tree_build_recursive
    mov [_huff_input_cursor], si
    mov [_huff_shift_word], ax
    mov [_huff_bits_left], cl
    call _huff_build_lookup
    pop di
    pop si
    pop bp
    ret

_huff_tree_build_recursive:
    call _huff_get_bit
    jc .leaf
    shl dx, 1
    inc bx
    call _huff_tree_build_recursive
    call _huff_get_bit
    or dl, 1
    call _huff_tree_build_recursive
    shr dx, 1
    dec bx
    ret
.leaf:
    call _huff_read_byte
    db 0x03, 0xff ; add di,di: retail uses reg<-r/m direction
    db 0x03, 0xff ; add di,di: same alternate encoding
    add di, _huff_code_table
    mov [di], dx
    mov [di+2], bx
    cmp bx, byte 16
    jle .done
    call _huff_depth_trap_e410
.done:
    ret

_huff_read_byte:
    db 0x2b, 0xff ; sub di,di: retail uses reg<-r/m direction
    mov ch, 8
.next:
    call _huff_get_bit
    rcl di, 1
    dec ch
    jnz .next
    ret

_huff_get_bit:
    db 0x0a, 0xc9 ; or cl,cl: retail uses reg<-r/m direction
    jz .empty
    dec cl
    shl ax, 1
    ret
.empty:
    cmp si, _huff_shift_word
    jz .refill
    lodsw
    xchg al, ah
    mov cl, 15
    shl ax, 1
    ret
.refill:
    call _huff_refill_e3ea
    lodsw
    xchg al, ah
    mov cl, 15
    shl ax, 1
    ret

_huff_build_lookup:
    mov bx,_huff_code_table
    mov bp,_huff_long_records
    mov cx,8
    mov ax,ds
    mov es,ax
.next_code:
    mov al,[bx+2]
    db 0x0a,0xc0 ; or al,al, original register-load encoding
    jz .advance
    db 0x3a,0xc1 ; cmp al,cl, original register-load encoding
    jg .extended
    db 0x8a,0xd0 ; mov dl,al, original register-load encoding
    db 0x2a,0xc8 ; sub cl,al, original register-load encoding
    inc cl
    inc cl
    db 0x2b,0xc0 ; sub ax,ax, original register-load encoding
    mov al,[bx]
    shl ax,cl
    mov di,_huff_fast_lookup
    db 0x03,0xf8 ; add di,ax, original register-load encoding
    mov [di],dl
    mov [di+1],ch
    mov word [di+2],0
    db 0x8a,0xd5 ; mov dl,ch, original register-load encoding
    db 0x2a,0xed ; sub ch,ch, original register-load encoding
    dec cl
    dec cl
    mov ax,1
    shl ax,cl
    db 0x8b,0xc8 ; mov cx,ax, original register-load encoding
    dec cx
    jz .short_done
    db 0x8b,0xf7 ; mov si,di, original register-load encoding
    add di,byte 4
    shl cx,1
    rep movsw
.short_done:
    db 0x8a,0xea ; mov ch,dl, original register-load encoding
    mov cl,8
.advance:
    add bx,byte 4
    inc ch
    jnz .next_code
    ret
.extended:
    push bx
    push cx
    mov dx,[bx]
    mov cl,16
    db 0x2a,0xc8 ; sub cl,al, original register-load encoding
    shl dx,cl
    mov [_huff_prefix_byte],dh
    db 0x2b,0xc0 ; sub ax,ax, original register-load encoding
    db 0x8a,0xc6 ; mov al,dh, original register-load encoding
    shl ax,1
    shl ax,1
    mov di,_huff_fast_lookup
    db 0x03,0xf8 ; add di,ax, original register-load encoding
    mov word [di],0
    mov [di+2],bp
.scan:
    mov al,[bx+2]
    cmp al,8
    jle .scan_next
    mov dx,[bx]
    mov cl,16
    db 0x2a,0xc8 ; sub cl,al, original register-load encoding
    shl dx,cl
    cmp dh,[_huff_prefix_byte]
    jne .scan_next
    db 0x8b,0xfd ; mov di,bp, original register-load encoding
    mov [di+1],dl
    mov [di+2],ch
    sub al,8
    db 0x2a,0xe4 ; sub ah,ah, original register-load encoding
    mov [di+3],al
    mov si,_huff_long_masks
    db 0x03,0xf0 ; add si,ax, original register-load encoding
    mov al,[si]
    mov [di],al
    mov word [bx+2],0
    add bp,byte 4
.scan_next:
    add bx,byte 4
    inc ch
    jnz .scan
    pop cx
    pop bx
    jmp near .next_code

_huff_frame_decode:
    push bp
    db 0x8b, 0xec ; mov bp,sp (original register-load encoding)
    push si
    push di
    mov ax,[bp+8]
    mov dx,[bp+10]
    db 0x0b, 0xd2 ; or dx,dx (original register-load encoding)
    jz .count_ready
    call _huff_depth_trap_e410
.count_ready:
    cmp ax,[_huff_remaining]
    jbe .bounded
    cmp dx,[_huff_remaining+2]
    jb .bounded
    mov ax,[_huff_remaining]
    mov dx,[_huff_remaining+2]
.bounded:
    sub [_huff_remaining+2],dx
    sbb [_huff_remaining],ax
    mov [_huff_saved_extent],ax
    mov [_huff_pending_count],ax
    les di,[bp+4]
    mov si,[_huff_input_cursor]
    call _huff_window_init
    jmp short .decode
.done:
    mov [_huff_input_cursor],si
    mov [_huff_shift_word],dx
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    db 0x2a, 0xed ; sub ch,ch (original register-load encoding)
    mov [_huff_bits_left],cx
    pop di
    pop si
    pop bp
    db 0x2b, 0xd2 ; sub dx,dx
    mov ax,[_huff_saved_extent]
    ret
.advance_count:
    dec word [_huff_pending_count]
    jz .done
.decode:
    db 0x2b, 0xdb ; sub bx,bx (original register-load encoding)
    db 0x8a, 0xde ; mov bl,dh (original register-load encoding)
    shl bx,1
    shl bx,1
    mov ax,[bx+_huff_fast_lookup]
    db 0x0a, 0xc0 ; or al,al (original register-load encoding)
    jz .long_code
    xchg al,ah
    stosb
    add [_huff_checksum],al
    db 0x0b, 0xff ; or di,di (original register-load encoding)
    jnz .short_output_ready
    mov di,es
    add di,strict word 0x1000
    mov es,di
    db 0x2b, 0xff ; sub di,di (original register-load encoding)
.short_output_ready:
    db 0x8a, 0xcc ; mov cl,ah (original register-load encoding)
    rol dx,cl
    db 0x2a, 0xe9 ; sub ch,cl (original register-load encoding)
.refill_if_needed:
    cmp ch,8
    jge .advance_count
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    rol dx,cl
    lodsb
    db 0x8a, 0xf0 ; mov dh,al (original register-load encoding)
    ror dx,cl
    add ch,8
    cmp si,_huff_shift_word
    jnz .advance_count
    call _huff_refill_e3ea
    jmp short .advance_count
.long_code:
    db 0x8a, 0xf2 ; mov dh,dl (original register-load encoding)
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    sub cl,8
    rol dx,cl
    lodsb
    cmp si,_huff_shift_word
    jnz .long_bits_ready
    call _huff_refill_e3ea
.long_bits_ready:
    db 0x8a, 0xf0 ; mov dh,al (original register-load encoding)
    ror dx,cl
    mov bx,[bx+_huff_fast_lookup+2]
.find_leaf:
    mov ax,[bx]
    db 0x22, 0xc6 ; and al,dh (original register-load encoding)
    db 0x3a, 0xc4 ; cmp al,ah (original register-load encoding)
    jz .leaf
    add bx,4
    jmp short .find_leaf
.leaf:
    mov ax,[bx+2]
    stosb
    add [_huff_checksum],al
    db 0x0b, 0xff ; or di,di (original register-load encoding)
    jnz .long_output_ready
    mov di,es
    add di,strict word 0x1000
    mov es,di
    db 0x2b, 0xff ; sub di,di (original register-load encoding)
.long_output_ready:
    db 0x8a, 0xcc ; mov cl,ah (original register-load encoding)
    rol dx,cl
    db 0x2a, 0xec ; sub ch,ah (original register-load encoding)
    jmp short .refill_if_needed

_huff_decode_stream:
    push bp
    db 0x8b, 0xec ; mov bp,sp (original register-load encoding)
    push si
    push di
    mov ax,[bp+8]
    mov dx,[bp+10]
    db 0x0b, 0xd2 ; or dx,dx (original register-load encoding)
    jz .count_ready
    call _huff_depth_trap_e410
.count_ready:
    cmp ax,[_huff_remaining]
    jbe .bounded
    cmp dx,[_huff_remaining+2]
    jb .bounded
    mov ax,[_huff_remaining]
    mov dx,[_huff_remaining+2]
.bounded:
    sub [_huff_remaining+2],dx
    sbb [_huff_remaining],ax
    mov [_huff_saved_extent],ax
    mov [_huff_pending_count],ax
    les di,[bp+4]
    mov si,[_huff_input_cursor]
    mov bp,[bp+12]
    mov [_huff_saved_extent],bp
    call _huff_window_init
    jmp short .decode
.done:
    mov [_huff_input_cursor],si
    mov [_huff_shift_word],dx
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    db 0x2a, 0xed ; sub ch,ch (original register-load encoding)
    mov [_huff_bits_left],cx
    db 0x8b, 0xc7 ; mov ax,di (original register-load encoding)
    mov dx,es
    pop di
    pop si
    pop bp
    ret
.row_end:
    mov byte [es:di],0
    mov ax,[_huff_saved_extent]
    db 0x8b, 0xe8 ; mov bp,ax (original register-load encoding)
    and ax,strict word 1
    jz .advance_count
    db 0x03, 0xf8 ; add di,ax (original register-load encoding)
    jnz .advance_count
    mov di,es
    add di,strict word 0x1000
    mov es,di
    db 0x2b, 0xff ; sub di,di (original register-load encoding)
    jmp short .advance_count
.advance_row:
    dec bp
    jz .row_end
.advance_count:
    dec word [_huff_pending_count]
    jz .done
.decode:
    db 0x2b, 0xdb ; sub bx,bx (original register-load encoding)
    db 0x8a, 0xde ; mov bl,dh (original register-load encoding)
    shl bx,1
    shl bx,1
    mov ax,[bx+_huff_fast_lookup]
    db 0x0a, 0xc0 ; or al,al (original register-load encoding)
    jz .long_code
    xchg al,ah
    stosb
    add [_huff_checksum],al
    db 0x0b, 0xff ; or di,di (original register-load encoding)
    jnz .short_output_ready
    mov di,es
    add di,strict word 0x1000
    mov es,di
    db 0x2b, 0xff ; sub di,di (original register-load encoding)
.short_output_ready:
    db 0x8a, 0xcc ; mov cl,ah (original register-load encoding)
    rol dx,cl
    db 0x2a, 0xe9 ; sub ch,cl (original register-load encoding)
.refill_if_needed:
    cmp ch,8
    jge .advance_row
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    rol dx,cl
    lodsb
    db 0x8a, 0xf0 ; mov dh,al (original register-load encoding)
    ror dx,cl
    add ch,8
    cmp si,_huff_shift_word
    jnz .advance_row
    call _huff_refill_e3ea
    jmp short .advance_row
.long_code:
    db 0x8a, 0xf2 ; mov dh,dl (original register-load encoding)
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    sub cl,8
    rol dx,cl
    lodsb
    cmp si,_huff_shift_word
    jnz .long_bits_ready
    call _huff_refill_e3ea
.long_bits_ready:
    db 0x8a, 0xf0 ; mov dh,al (original register-load encoding)
    ror dx,cl
    mov bx,[bx+_huff_fast_lookup+2]
.find_leaf:
    mov ax,[bx]
    db 0x22, 0xc6 ; and al,dh (original register-load encoding)
    db 0x3a, 0xc4 ; cmp al,ah (original register-load encoding)
    jz .leaf
    add bx,4
    jmp short .find_leaf
.leaf:
    mov ax,[bx+2]
    stosb
    add [_huff_checksum],al
    db 0x0b, 0xff ; or di,di (original register-load encoding)
    jnz .long_output_ready
    mov di,es
    add di,strict word 0x1000
    mov es,di
    db 0x2b, 0xff ; sub di,di (original register-load encoding)
.long_output_ready:
    db 0x8a, 0xcc ; mov cl,ah (original register-load encoding)
    rol dx,cl
    db 0x2a, 0xec ; sub ch,ah (original register-load encoding)
    jmp short .refill_if_needed

_huff_window_save:
    pop dx
    pop cx
    push si
    call _huff_refill_e3ea
    lodsw
    xchg al,ah
    rol ax,cl
    sub cx,byte 16
    neg cx
    mov [_huff_shift_word],ax
    mov [_huff_bits_left],cx
    mov [_huff_input_cursor],si
    mov byte [_huff_checksum],0
    pop si
    sub sp,byte 2
    jmp dx

_huff_window_init:
    mov dx,[_huff_shift_word]
    mov cx,[_huff_bits_left]
    cmp cl,8
    jg .ready
    rol dx,cl
    mov si,[_huff_input_cursor]
    cmp si,_huff_shift_word
    jne .first_byte
    call _huff_refill_e3ea
.first_byte:
    lodsb
    db 0x8a,0xf0 ; mov dh,al, original register-load encoding
    cmp si,_huff_shift_word
    jne .rotate_back
    call _huff_refill_e3ea
.rotate_back:
    ror dx,cl
    add cl,8
.ready:
    db 0x8a,0xe9 ; mov ch,cl, original register-load encoding
    ret
