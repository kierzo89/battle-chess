; BIOS INT1A function0 returns ticks in CX:DX; near C long result is DX:AX.
bits 16
cpu 8086
org 0xea5b
    db 0x2a,0xe4              ; sub ah,ah: original register-load direction
    int 0x1a
    db 0x8b,0xc2              ; mov ax,dx: original register-load direction
    db 0x8b,0xd1              ; mov dx,cx: original register-load direction
    ret
