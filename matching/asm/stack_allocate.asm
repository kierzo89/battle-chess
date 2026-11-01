; REA ev_0da5e1b0877c65d102e7598d12a09dc187bad67ec47b6a57895c4b9866f14c66.
; AX=requested stack bytes. Consume return IP into CX, check unsigned
; subtraction and DS:4A00 limit; install SP and jump back to caller.
; Failure clears AX and tail-jumps to EB2A (error handler).
bits 16
cpu 8086
org 0xecaa

    pop cx
    db 0x8b, 0xdc              ; mov bx,sp, retail direction encoding
    db 0x2b, 0xd8              ; sub bx,ax, retail direction encoding
    jc .overflow
    cmp bx, [0x4a00]
    jc .overflow
    db 0x8b, 0xe3              ; mov sp,bx, retail direction encoding
    jmp cx
.overflow:
    db 0x33, 0xc0              ; xor ax,ax, retail direction encoding
    jmp near 0xeb2a
