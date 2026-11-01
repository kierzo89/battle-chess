; E0D8..E196. Build the eight-bit fast lookup and extended leaf lists.
; 256 four-byte code records at30CC; fast lookup34CC; spill records38CC.
bits 16
cpu 8086
org 0xe0d8
    mov bx,0x30cc
    mov bp,0x38cc
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
    mov di,0x34cc
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
    mov [0x44d5],dh
    db 0x2b,0xc0 ; sub ax,ax, original register-load encoding
    db 0x8a,0xc6 ; mov al,dh, original register-load encoding
    shl ax,1
    shl ax,1
    mov di,0x34cc
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
    cmp dh,[0x44d5]
    jne .scan_next
    db 0x8b,0xfd ; mov di,bp, original register-load encoding
    mov [di+1],dl
    mov [di+2],ch
    sub al,8
    db 0x2a,0xe4 ; sub ah,ah, original register-load encoding
    mov [di+3],al
    mov si,0x44cc
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
