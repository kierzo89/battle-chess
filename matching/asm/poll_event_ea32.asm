; BIOS keyboard poll. Near cdecl: three DS-relative Byte* outputs.
; Only on success: [BP+4]=shift flags, [BP+6]=ASCII, [BP+8]=scan code.
; Returns AX=1 on success, AX=0 when no key is pending.
bits 16
cpu 8086
org 0xea32
    push bp
    db 0x8b,0xec              ; mov bp,sp: original register-load direction
    mov ah,1
    int 0x16
    jz .none
    db 0x2a,0xe4              ; sub ah,ah: original register-load direction
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
    db 0x2b,0xc0              ; sub ax,ax: original register-load direction
.done:
    pop bp
    ret
