; Register-oriented refill plus the original adjacent INT3 entry.
; One complete multi-entry allocation; the trap does not have a fabricated RET.
bits 16
cpu 8086
segment _TEXT public align=2 class=CODE use16
global _huff_refill_e3ea, _huff_depth_trap_e410
global _begin_asset_decode, _end_asset_decode
extern _huff_memory_mode, _huff_memory_cursor, _huff_input_buffer, _read_asset

_huff_refill_e3ea:
    cmp byte [_huff_memory_mode],0
    jnz short memory_copy
    push es
    push ax
    push bx
    push cx
    push dx
    db 0x2b,0xc0 ; sub ax,ax, original register-load direction
    push ax
    mov ax,512
    push ax
    push ds
    mov ax,_huff_input_buffer
    db 0x8b,0xf0 ; mov si,ax, original register-load direction
    push ax
    call _read_asset
    add sp,byte 8
    pop dx
    pop cx
    pop bx
    pop ax
    pop es
    ret
_huff_depth_trap_e410:
    int3
memory_copy:
    push es
    push ds
    push ax
    push cx
    push di
    mov ax,[_huff_memory_cursor]
    db 0x8b,0xf0 ; mov si,ax, original register-load direction
    mov cl,4
    shr ax,cl
    add ax,[_huff_memory_cursor+2]
    mov ds,ax
    and si,strict word 15
    mov ax,seg _huff_input_buffer
    mov es,ax
    mov di,_huff_input_buffer
    mov cx,256
    rep movsw
    mov [es:_huff_memory_cursor],si
    mov [es:_huff_memory_cursor+2],ds
    mov si,_huff_input_buffer
    pop di
    pop cx
    pop ax
    pop ds
    pop es
    ret

; Near cdecl wrapper consumes the caller's far-pointer words into the
; memory-source cursor, then restores SP to the caller-cleanup position.
_begin_asset_decode:
    pop cx
    pop word [_huff_memory_cursor]
    pop word [_huff_memory_cursor+2]
    mov byte [_huff_memory_mode],1
    sub sp,byte 4
    jmp cx
_end_asset_decode:
    mov byte [_huff_memory_mode],0
    ret
