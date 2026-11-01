; Original image E0A8..E0B6. Accumulate eight MSB-first input bits into DI.
; AX, CX and SI carry the bit-reader state; CH is the loop counter.
bits 16
cpu 8086
org 0xe0a8

    db 0x2b, 0xff              ; sub di,di: retail uses reg<-r/m direction
    mov ch, 8
.next:
    call 0xe0b6
    rcl di, 1
    dec ch
    jnz .next
    ret
