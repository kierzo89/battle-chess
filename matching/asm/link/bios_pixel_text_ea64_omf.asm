; BIOS write-pixel helper. The colour byte belongs to the loaded graphics driver.
; Its external declaration supplies no backing allocation or guessed capacity.
.8086
EXTRN _graphics_driver_colour_110dc:BYTE
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT
PUBLIC _bios_plot_pixel_ea64
_bios_plot_pixel_ea64 PROC NEAR
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov ax, SEG _graphics_driver_colour_110dc
    mov es, ax
    mov ah, 0Ch
    mov al, es:_graphics_driver_colour_110dc
    mov bx, 0
    mov cx, [bp+4]
    mov dx, [bp+6]
    int 10h
    pop ds
    pop di
    pop si
    pop bp
    ret
_bios_plot_pixel_ea64 ENDP
_TEXT ENDS
END
