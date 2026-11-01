; Faithful authored ASM84. C store-only-local/driver-frame questions remain held.
; BYTE alignment preserves the odd native entry17F9 without filler or leading NOP.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _input_mode_0046:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR
; Existing canonical PUBLICs, not synthetic input_select/input_init aliases.
EXTRN _graphics_begin:FAR, _graphics_end:FAR
_TEXT SEGMENT BYTE PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _select_mode
_select_mode PROC NEAR
    push bp                         ; native17F9
    mov bp,sp                       ; native17FA
    mov ax,8                        ; native17FC
    call NEAR PTR __chkstk           ; native17FF
    push si                         ; native1802
    mov si,WORD PTR [bp+4]           ; native1803
    mov ax,si                       ; native1806
    cmp ax,WORD PTR _input_mode_0046 ; native1808
    je SHORT mode_done              ; native180C
    mov WORD PTR [bp-4],-1           ; native180E
    mov WORD PTR [bp-2],-1           ; native1813
    mov WORD PTR [bp-8],-1           ; native1818
    mov WORD PTR [bp-6],-1           ; native181D
    mov WORD PTR _input_mode_0046,ax ; native1822
    cmp ax,4                        ; native1825
    jne SHORT mode_calls            ; native1828
    mov WORD PTR [bp-4],-7           ; native182A
    mov WORD PTR [bp-2],-1           ; native182F
    mov WORD PTR [bp-8],-24          ; native1834
    mov WORD PTR [bp-6],-1           ; native1839
mode_calls:
    call _graphics_begin            ; native183E
    call _graphics_end              ; native1843
mode_done:
    pop si                          ; native1848
    mov sp,bp                       ; native1849
    pop bp                          ; native184B
    ret                             ; native184C
_select_mode ENDP
_TEXT ENDS
END
