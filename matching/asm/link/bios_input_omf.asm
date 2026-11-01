; Relocatable source-link form of the two already credited BIOS wrappers.
; Explicit two-byte encodings select the original register-load direction
; for the annotated individual 8086 instructions, as in canonical BIN source.
bits 16
cpu 8086
segment _TEXT public align=2 class=CODE use16
global _poll_event, _ticks_ea5b

; int near poll_event(Byte *shiftflags, Byte *ascii, Byte *scancode)
_poll_event:
    push bp
    db 0x8b,0xec              ; mov bp,sp (register-load encoding)
    mov ah,1
    int 0x16
    jz .none
    db 0x2a,0xe4              ; sub ah,ah (register-load encoding)
    int 0x16
    mov bx,[bp+6]
    mov [bx],al
    mov bx,[bp+8]
    mov [bx],ah
    mov ah,2
    int 0x16
    mov bx,[bp+4]
    mov [bx],al
    mov ax,1
    jmp short .done
.none:
    db 0x2b,0xc0              ; sub ax,ax (register-load encoding)
.done:
    pop bp
    ret

; long near ticks_ea5b(void): BIOS CX:DX becomes C DX:AX.
_ticks_ea5b:
    db 0x2a,0xe4              ; sub ah,ah (register-load encoding)
    int 0x1a
    db 0x8b,0xc2              ; mov ax,dx (register-load encoding)
    db 0x8b,0xd1              ; mov dx,cx (register-load encoding)
    ret
