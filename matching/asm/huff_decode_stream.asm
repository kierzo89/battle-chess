; Complete original E282..E393 stream decoder. Hand-written assembly credit.
; C stack: destination far pointer, requested count low/high, row width.
; DX/CH hold the bit window/count; DS:SI is buffered input; ES:DI output.
; BP becomes a row counter after the arguments have been read.
bits 16
cpu 8086
org 0xe282

    push bp
    db 0x8b, 0xec ; mov bp,sp (original register-load encoding)
    push si
    push di
    mov ax,[bp+8]
    mov dx,[bp+10]
    db 0x0b, 0xd2 ; or dx,dx (original register-load encoding)
    jz .count_ready
    call 0xe410
.count_ready:
    cmp ax,[0x30c8]
    jbe .bounded
    cmp dx,[0x30ca]
    jb .bounded
    mov ax,[0x30c8]
    mov dx,[0x30ca]
.bounded:
    sub [0x30ca],dx
    sbb [0x30c8],ax
    mov [0x44d8],ax
    mov [0x44d6],ax
    les di,[bp+4]
    mov si,[0x30c6]
    mov bp,[bp+12]
    mov [0x44d8],bp
    call 0xe3ba
    jmp short .decode
.done:
    mov [0x30c6],si
    mov [0x30c2],dx
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    db 0x2a, 0xed ; sub ch,ch (original register-load encoding)
    mov [0x30c4],cx
    db 0x8b, 0xc7 ; mov ax,di (original register-load encoding)
    mov dx,es
    pop di
    pop si
    pop bp
    ret
.row_end:
    mov byte [es:di],0
    mov ax,[0x44d8]
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
    dec word [0x44d6]
    jz .done
.decode:
    db 0x2b, 0xdb ; sub bx,bx (original register-load encoding)
    db 0x8a, 0xde ; mov bl,dh (original register-load encoding)
    shl bx,1
    shl bx,1
    mov ax,[bx+0x34cc]
    db 0x0a, 0xc0 ; or al,al (original register-load encoding)
    jz .long_code
    xchg al,ah
    stosb
    add [0x44df],al
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
    cmp si,0x30c2
    jnz .advance_row
    call 0xe3ea
    jmp short .advance_row
.long_code:
    db 0x8a, 0xf2 ; mov dh,dl (original register-load encoding)
    db 0x8a, 0xcd ; mov cl,ch (original register-load encoding)
    sub cl,8
    rol dx,cl
    lodsb
    cmp si,0x30c2
    jnz .long_bits_ready
    call 0xe3ea
.long_bits_ready:
    db 0x8a, 0xf0 ; mov dh,al (original register-load encoding)
    ror dx,cl
    mov bx,[bx+0x34ce]
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
    add [0x44df],al
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
