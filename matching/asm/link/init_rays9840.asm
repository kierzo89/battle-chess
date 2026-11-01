; Faithful mnemonic reconstruction of native9840..98F8, not a C match.
; The real eight-byte frame and its unused word remain explicit machine state.
; Providers are the existing 80-byte lookup structure and 239 genuine Ray cells.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _move_lookup_tables:BYTE, _rays:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _fill_8a96:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _init_rays
_init_rays PROC NEAR
    push bp ; native 9840
    mov bp,sp ; native 9841
    mov ax,8 ; native 9843
    call NEAR PTR __chkstk ; native 9846
    push di ; native 9849
    push si ; native 984A
    sub ax,ax ; native 984B
    push ax ; native 984D
    mov ax,956 ; native 984E
    push ax ; native 9851
    mov ax,OFFSET DGROUP:_rays ; native 9852
    push ax ; native 9855
    call NEAR PTR _fill_8a96 ; native 9856
    add sp,6 ; native 9859
    mov WORD PTR [bp-8],7 ; native 985C
    jmp SHORT direction_test ; native 9861
direction_next:
    dec WORD PTR [bp-8] ; native 9863
direction_test:
    cmp WORD PTR [bp-8],0 ; native 9866
    jge SHORT direction_body ; native 986A
    jmp NEAR PTR rays_done ; native 986C
direction_body:
    mov WORD PTR [bp-6],1 ; native 986F
    jmp SHORT distance_test ; native 9874
distance_next:
    inc WORD PTR [bp-6] ; native 9876
distance_test:
    cmp WORD PTR [bp-6],7 ; native 9879
    jg SHORT knight_and_pawn ; native 987D
    mov bx,WORD PTR [bp-8] ; native 987F
    shl bx,1 ; native 9882
    mov ax,WORD PTR _move_lookup_tables[bx] ; native 9884
    imul WORD PTR [bp-6] ; native 9888
    shl ax,1 ; native 988B
    shl ax,1 ; native 988D
    add ax,OFFSET DGROUP:_rays+476 ; native 988F
    mov WORD PTR [bp-2],ax ; native 9892
    cmp WORD PTR [bp-8],4 ; native 9895
    jge SHORT diagonal_mask ; native 9899
    mov bx,ax ; native 989B
    mov ax,WORD PTR _move_lookup_tables+38 ; native 989D
    add ax,WORD PTR _move_lookup_tables+40 ; native 98A0
    mov WORD PTR [bx],ax ; native 98A4
    jmp SHORT store_step ; native 98A6
diagonal_mask:
    mov bx,WORD PTR [bp-2] ; native 98A8
    mov ax,WORD PTR _move_lookup_tables+38 ; native 98AB
    add ax,WORD PTR _move_lookup_tables+42 ; native 98AE
    mov WORD PTR [bx],ax ; native 98B2
store_step:
    mov bx,WORD PTR [bp-2] ; native 98B4
    mov si,WORD PTR [bp-8] ; native 98B7
    shl si,1 ; native 98BA
    mov ax,WORD PTR _move_lookup_tables[si] ; native 98BC
    mov WORD PTR [bx+2],ax ; native 98C0
    jmp SHORT distance_next ; native 98C3
knight_and_pawn:
    mov si,WORD PTR [bp-8] ; native 98C5
    shl si,1 ; native 98C8
    mov bx,WORD PTR _move_lookup_tables[si] ; native 98CA
    shl bx,1 ; native 98CE
    shl bx,1 ; native 98D0
    mov ax,WORD PTR _move_lookup_tables+36 ; native 98D2
    add WORD PTR _rays[bx+476],ax ; native 98D5
    mov di,WORD PTR _move_lookup_tables[si+16] ; native 98D9
    mov cl,2 ; native 98DD
    shl di,cl ; native 98DF
    mov ax,WORD PTR _move_lookup_tables+44 ; native 98E1
    mov WORD PTR _rays[di+476],ax ; native 98E4
    mov ax,WORD PTR _move_lookup_tables[si+16] ; native 98E8
    mov WORD PTR _rays[di+478],ax ; native 98EC
    jmp NEAR PTR direction_next ; native 98F0
rays_done:
    pop si ; native 98F3
    pop di ; native 98F4
    mov sp,bp ; native 98F5
    pop bp ; native 98F7
    ret ; native 98F8
_init_rays ENDP
_TEXT ENDS
END
