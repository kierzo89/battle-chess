; PREPARATION ONLY: authentic MASM emission and exact matching remain unobserved.
; Complete physical instruction stream, including real NOPs and dead JMPs.
; Zero C credit. WORD neighbor join and historical patch attribution remain held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _startup_offsets_9648:DWORD
EXTRN _menu_text:BYTE, _foreground:WORD, _menu_state:WORD
EXTRN _left_lists:WORD, _piece_controls:WORD, _left_controls:WORD
EXTRN _asset_table_53f8:WORD, _asset_table_8ae4:WORD
; Unresolved external views only: no source allocation, capacity or alias is defined.
EXTRN _animation_initial_stream_0f08:BYTE
EXTRN _animation_black_label_4d96:BYTE, _animation_white_label_4d9e:BYTE
_DATA ENDS
DGROUP GROUP _DATA
; Independently identified far resource view, outside DGROUP; no backing is defined.
EXTRN _splash_buffer:BYTE
EXTRN __chkstk:NEAR
EXTRN _begin_input_0fb0:NEAR
EXTRN _draw_text_e915:NEAR
EXTRN _end_input_102d:NEAR
EXTRN _fill_region_1780:NEAR
EXTRN _huff_frame_decode:NEAR
EXTRN _prepare_asset_decode:NEAR
EXTRN _rand:NEAR
EXTRN _restore_region_58b0:NEAR
EXTRN _seek_asset:NEAR
EXTRN _select_asset_file:NEAR
EXTRN _text_input_1064:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _init_animation
_init_animation PROC NEAR
L_6CB4:
    push bp ; native 6CB4
    mov bp,sp ; native 6CB5
    mov ax,03eh ; native 6CB7
    call NEAR PTR __chkstk ; native 6CBA
    push di ; native 6CBD
    push si ; native 6CBE
    mov WORD PTR [bp-04h],00h ; native 6CBF
    call NEAR PTR _begin_input_0fb0 ; native 6CC4
    sub ax,ax ; native 6CC7
    push ax ; native 6CC9
    call NEAR PTR _select_asset_file ; native 6CCA
    add sp,02h ; native 6CCD
    les bx,DWORD PTR _startup_offsets_9648 ; native 6CD0
    push WORD PTR ES:[bx+016h] ; native 6CD4
    push WORD PTR ES:[bx+014h] ; native 6CD8
    call NEAR PTR _seek_asset ; native 6CDC
    add sp,04h ; native 6CDF
    call NEAR PTR _prepare_asset_decode ; native 6CE2
    mov ax,07d00h ; native 6CE5
    cwd ; native 6CE8
    push dx ; native 6CE9
    push ax ; native 6CEA
    mov ax,OFFSET _splash_buffer ; native 6CEB
    mov dx,SEG _splash_buffer ; native 6CEE
    push dx ; native 6CF1
    push ax ; native 6CF2
    call NEAR PTR _huff_frame_decode ; native 6CF3
    add sp,08h ; native 6CF6
L_6CF9:
    push WORD PTR _menu_state ; native 6CF9
    mov ax,077h ; native 6CFD
    push ax ; native 6D00
    mov ax,012fh ; native 6D01
    push ax ; native 6D04
    mov ax,050h ; native 6D05
    push ax ; native 6D08
    mov ax,010h ; native 6D09
    push ax ; native 6D0C
    call NEAR PTR _fill_region_1780 ; native 6D0D
    add sp,0ah ; native 6D10
    lea ax,[bp-03ch] ; native 6D13
    mov WORD PTR _menu_text+2,ax ; native 6D16
    mov al,BYTE PTR _foreground ; native 6D19
    mov BYTE PTR _menu_text,al ; native 6D1C
    mov al,BYTE PTR _menu_state ; native 6D1F
    mov BYTE PTR _menu_text+1,al ; native 6D22
    call NEAR PTR _rand ; native 6D25
    cwd ; native 6D28
    mov cx,0204fh ; native 6D29
    idiv cx ; native 6D2C
    mov [bp-03eh],dx ; native 6D2E
    mov WORD PTR [bp-2],OFFSET DGROUP:_left_lists ; native 6D31
    mov ax,OFFSET DGROUP:_animation_initial_stream_0f08 ; native 6D36
    mov [bp-08h],ax ; native 6D39
    mov WORD PTR [bp-06h],ds ; native 6D3C
    sub si,si ; native 6D3F
    jmp SHORT L_6D44 ; native 6D41
L_6D43:
    inc si ; native 6D43
L_6D44:
    cmp si,048h ; native 6D44
    jnl L_6D7A ; native 6D47
    mov bx,[bp-02h] ; native 6D49
    add WORD PTR [bp-02h],02h ; native 6D4C
    mov ax,[bp-08h] ; native 6D50
    mov [bx],ax ; native 6D53
L_6D55:
    les bx,DWORD PTR [bp-08h] ; native 6D55
    cmp BYTE PTR ES:[bx],0ffh ; native 6D58
    jz L_6D6C ; native 6D5C
    add WORD PTR [bp-08h],01h ; native 6D5E
    sbb ax,ax ; native 6D62
    and ax,01000h ; native 6D64
    add [bp-06h],ax ; native 6D67
    jmp SHORT L_6D55 ; native 6D6A
L_6D6C:
    add WORD PTR [bp-08h],01h ; native 6D6C
    sbb ax,ax ; native 6D70
    and ax,01000h ; native 6D72
    add [bp-06h],ax ; native 6D75
    jmp SHORT L_6D43 ; native 6D78
L_6D7A:
    mov bx,[bp-03eh] ; native 6D7A
    ; LEA uses effective address only; the following ASSUME is not a runtime DS load.
    ASSUME DS:SEG _splash_buffer
    lea ax,[bx+OFFSET _splash_buffer] ; native 6D7D
    ASSUME DS:DGROUP
    mov dx,SEG _splash_buffer ; native 6D81
    mov [bp-08h],ax ; native 6D84
    mov [bp-06h],dx ; native 6D87
L_6D8A:
    les bx,DWORD PTR [bp-08h] ; native 6D8A
    cmp BYTE PTR ES:[bx],02ah ; native 6D8D
    jz L_6DA3 ; native 6D91
    add WORD PTR [bp-08h],-1 ; native 6D93
    sbb ax,ax ; native 6D97
    not ax ; native 6D99
    and ax,01000h ; native 6D9B
    sub [bp-06h],ax ; native 6D9E
    jmp SHORT L_6D8A ; native 6DA1
L_6DA3:
    add WORD PTR [bp-08h],01h ; native 6DA3
    sbb ax,ax ; native 6DA7
    and ax,01000h ; native 6DA9
    add [bp-06h],ax ; native 6DAC
    lea ax,[bp-03ch] ; native 6DAF
    mov [bp-0ch],ax ; native 6DB2
    mov WORD PTR [bp-0ah],ss ; native 6DB5
L_6DB8:
    les bx,DWORD PTR [bp-08h] ; native 6DB8
    add WORD PTR [bp-08h],01h ; native 6DBB
    jnc L_6DC6 ; native 6DBF
    add WORD PTR [bp-06h],01000h ; native 6DC1
L_6DC6:
    mov al,ES:[bx] ; native 6DC6
    xor al,06ah ; native 6DC9
    les bx,DWORD PTR [bp-0ch] ; native 6DCB
    add WORD PTR [bp-0ch],01h ; native 6DCE
    jnc L_6DD9 ; native 6DD2
    add WORD PTR [bp-0ah],01000h ; native 6DD4
L_6DD9:
    mov ES:[bx],al ; native 6DD9
    les bx,DWORD PTR [bp-08h] ; native 6DDC
    cmp BYTE PTR ES:[bx],046h ; native 6DDF
    jnz L_6DB8 ; native 6DE3
    add WORD PTR [bp-08h],01h ; native 6DE5
    jnc L_6DF0 ; native 6DE9
    add WORD PTR [bp-06h],01000h ; native 6DEB
L_6DF0:
    mov al,ES:[bx] ; native 6DF0
    xor al,06ah ; native 6DF3
    les bx,DWORD PTR [bp-0ch] ; native 6DF5
    add WORD PTR [bp-0ch],01h ; native 6DF8
    jnc L_6E03 ; native 6DFC
    add WORD PTR [bp-0ah],01000h ; native 6DFE
L_6E03:
    mov ES:[bx],al ; native 6E03
    les bx,DWORD PTR [bp-0ch] ; native 6E06
    mov BYTE PTR ES:[bx],00h ; native 6E09
    mov ax,058h ; native 6E0D
    push ax ; native 6E10
    mov ax,018h ; native 6E11
    push ax ; native 6E14
    mov ax,OFFSET DGROUP:_menu_text ; native 6E15
    push ax ; native 6E18
    call NEAR PTR _draw_text_e915 ; native 6E19
    add sp,06h ; native 6E1C
    lea ax,[bp-03ch] ; native 6E1F
    mov [bp-0ch],ax ; native 6E22
    mov WORD PTR [bp-0ah],ss ; native 6E25
    add WORD PTR [bp-08h],01h ; native 6E28
    sbb ax,ax ; native 6E2C
    and ax,01000h ; native 6E2E
    add [bp-06h],ax ; native 6E31
L_6E34:
    les bx,DWORD PTR [bp-08h] ; native 6E34
    cmp BYTE PTR ES:[bx],067h ; native 6E37
    jz L_6E60 ; native 6E3B
    add WORD PTR [bp-08h],01h ; native 6E3D
    jnc L_6E48 ; native 6E41
    add WORD PTR [bp-06h],01000h ; native 6E43
L_6E48:
    mov al,ES:[bx] ; native 6E48
    xor al,06ah ; native 6E4B
    les bx,DWORD PTR [bp-0ch] ; native 6E4D
    add WORD PTR [bp-0ch],01h ; native 6E50
    jnc L_6E5B ; native 6E54
    add WORD PTR [bp-0ah],01000h ; native 6E56
L_6E5B:
    mov ES:[bx],al ; native 6E5B
    jmp SHORT L_6E34 ; native 6E5E
L_6E60:
    les bx,DWORD PTR [bp-0ch] ; native 6E60
    mov BYTE PTR ES:[bx],00h ; native 6E63
    add WORD PTR [bp-08h],01h ; native 6E67
    sbb ax,ax ; native 6E6B
    and ax,01000h ; native 6E6D
    add [bp-06h],ax ; native 6E70
    mov ax,060h ; native 6E73
    push ax ; native 6E76
    mov ax,018h ; native 6E77
    push ax ; native 6E7A
    mov ax,OFFSET DGROUP:_menu_text ; native 6E7B
    push ax ; native 6E7E
    call NEAR PTR _draw_text_e915 ; native 6E7F
    add sp,06h ; native 6E82
    sub si,si ; native 6E85
    mov ax,[bp-08h] ; native 6E87
    mov dx,[bp-06h] ; native 6E8A
    mov [bp-0ch],ax ; native 6E8D
    mov [bp-0ah],dx ; native 6E90
L_6E93:
    mov bx,[bp-03eh] ; native 6E93
    ; LEA uses effective address only; the following ASSUME is not a runtime DS load.
    ASSUME DS:SEG _splash_buffer
    lea ax,[bx+OFFSET _splash_buffer] ; native 6E96
    ASSUME DS:DGROUP
    mov dx,SEG _splash_buffer ; native 6E9A
    cmp dx,[bp-06h] ; native 6E9D
    jc L_6ECC ; native 6EA0
    ja L_6EA9 ; native 6EA2
    cmp ax,[bp-08h] ; native 6EA4
    jna L_6ECC ; native 6EA7
L_6EA9:
    les bx,DWORD PTR [bp-08h] ; native 6EA9
    add WORD PTR [bp-08h],01h ; native 6EAC
    jnc L_6EB7 ; native 6EB0
    add WORD PTR [bp-06h],01000h ; native 6EB2
L_6EB7:
    cmp BYTE PTR ES:[bx],067h ; native 6EB7
    jnz L_6ECA ; native 6EBB
    inc si ; native 6EBD
    mov ax,[bp-08h] ; native 6EBE
    mov dx,[bp-06h] ; native 6EC1
    mov [bp-0ch],ax ; native 6EC4
    mov [bp-0ah],dx ; native 6EC7
L_6ECA:
    jmp SHORT L_6E93 ; native 6ECA
L_6ECC:
    mov di,si ; native 6ECC
; D1FF is SAR DI,1: retained REA/raw opcode override NDISASM3.01 erroneous 0 count.
    sar di,1 ; native 6ECE
    inc di ; native 6ED0
    lea ax,[bp-03ch] ; native 6ED1
    mov [bp-08h],ax ; native 6ED4
    mov WORD PTR [bp-06h],ss ; native 6ED7
    cmp di,09h ; native 6EDA
    jng L_6EFC ; native 6EDD
    mov ax,di ; native 6EDF
    cwd ; native 6EE1
    mov cx,0ah ; native 6EE2
    idiv cx ; native 6EE5
    add al,030h ; native 6EE7
    les bx,DWORD PTR [bp-08h] ; native 6EE9
    add WORD PTR [bp-08h],01h ; native 6EEC
    jnc L_6EF7 ; native 6EF0
    add WORD PTR [bp-06h],01000h ; native 6EF2
L_6EF7:
    mov ES:[bx],al ; native 6EF7
    jmp SHORT L_6F0E ; native 6EFA
L_6EFC:
    les bx,DWORD PTR [bp-08h] ; native 6EFC
    add WORD PTR [bp-08h],01h ; native 6EFF
    jnc L_6F0A ; native 6F03
    add WORD PTR [bp-06h],01000h ; native 6F05
L_6F0A:
    mov BYTE PTR ES:[bx],020h ; native 6F0A
L_6F0E:
    mov ax,di ; native 6F0E
    cwd ; native 6F10
    mov cx,0ah ; native 6F11
    idiv cx ; native 6F14
    add dl,030h ; native 6F16
    les bx,DWORD PTR [bp-08h] ; native 6F19
    add WORD PTR [bp-08h],01h ; native 6F1C
    jnc L_6F27 ; native 6F20
    add WORD PTR [bp-06h],01000h ; native 6F22
L_6F27:
    mov ES:[bx],dl ; native 6F27
    les bx,DWORD PTR [bp-08h] ; native 6F2A
    add WORD PTR [bp-08h],01h ; native 6F2D
    jnc L_6F38 ; native 6F31
    add WORD PTR [bp-06h],01000h ; native 6F33
L_6F38:
    mov BYTE PTR ES:[bx],02eh ; native 6F38
    les bx,DWORD PTR [bp-08h] ; native 6F3C
    add WORD PTR [bp-08h],01h ; native 6F3F
    jnc L_6F4A ; native 6F43
    add WORD PTR [bp-06h],01000h ; native 6F45
L_6F4A:
    mov BYTE PTR ES:[bx],020h ; native 6F4A
    test si,01h ; native 6F4E
    jz L_6F59 ; native 6F52
    mov ax,OFFSET DGROUP:_animation_black_label_4d96 ; native 6F54
    jmp SHORT L_6F5C ; native 6F57
L_6F59:
    mov ax,OFFSET DGROUP:_animation_white_label_4d9e ; native 6F59
L_6F5C:
    mov [bp-0eh],ax ; native 6F5C
L_6F5F:
    mov bx,[bp-0eh] ; native 6F5F
    cmp BYTE PTR [bx],00h ; native 6F62
    jz L_6F7F ; native 6F65
    inc WORD PTR [bp-0eh] ; native 6F67
    mov al,[bx] ; native 6F6A
    les bx,DWORD PTR [bp-08h] ; native 6F6C
    add WORD PTR [bp-08h],01h ; native 6F6F
    jnc L_6F7A ; native 6F73
    add WORD PTR [bp-06h],01000h ; native 6F75
L_6F7A:
    mov ES:[bx],al ; native 6F7A
    jmp SHORT L_6F5F ; native 6F7D
L_6F7F:
    les bx,DWORD PTR [bp-08h] ; native 6F7F
    mov BYTE PTR ES:[bx],00h ; native 6F82
    les bx,DWORD PTR [bp-08h] ; native 6F86
    mov al,048h ; native 6F89
    mul BYTE PTR ES:[bx] ; native 6F8B
    add ax,OFFSET DGROUP:_left_controls ; native 6F8E
    mov [bp-02h],ax ; native 6F91
    mov ax,WORD PTR _asset_table_53f8 ; native 6F94
    mov [bp-08h],ax ; native 6F97
    mov WORD PTR [bp-06h],ds ; native 6F9A
    sub si,si ; native 6F9D
    jmp SHORT L_6FA2 ; native 6F9F
L_6FA1:
    inc si ; native 6FA1
L_6FA2:
    cmp si,048h ; native 6FA2
    jnl L_6FD8 ; native 6FA5
    mov bx,[bp-02h] ; native 6FA7
    add WORD PTR [bp-02h],02h ; native 6FAA
    mov ax,[bp-08h] ; native 6FAE
    mov [bx],ax ; native 6FB1
L_6FB3:
    les bx,DWORD PTR [bp-08h] ; native 6FB3
    cmp BYTE PTR ES:[bx],0ffh ; native 6FB6
    jz L_6FCA ; native 6FBA
    add WORD PTR [bp-08h],01h ; native 6FBC
    sbb ax,ax ; native 6FC0
    and ax,01000h ; native 6FC2
    add [bp-06h],ax ; native 6FC5
    jmp SHORT L_6FB3 ; native 6FC8
L_6FCA:
    add WORD PTR [bp-08h],01h ; native 6FCA
    sbb ax,ax ; native 6FCE
    and ax,01000h ; native 6FD0
    add [bp-06h],ax ; native 6FD3
    jmp SHORT L_6FA1 ; native 6FD6
L_6FD8:
    mov ax,068h ; native 6FD8
    push ax ; native 6FDB
    mov ax,018h ; native 6FDC
    push ax ; native 6FDF
    mov ax,OFFSET DGROUP:_menu_text ; native 6FE0
    push ax ; native 6FE3
    call NEAR PTR _draw_text_e915 ; native 6FE4
    add sp,06h ; native 6FE7
    sub ax,ax ; native 6FEA
    push ax ; native 6FEC
    mov ax,0ah ; native 6FED
    push ax ; native 6FF0
    lea ax,[bp-03ch] ; native 6FF1
    push ax ; native 6FF4
    mov ax,068h ; native 6FF5
    push ax ; native 6FF8
    mov ax,070h ; native 6FF9
    push ax ; native 6FFC
    call NEAR PTR _text_input_1064 ; native 6FFD
    add sp,0ah ; native 7000
    lea ax,[bp-03ch] ; native 7003
    mov [bp-08h],ax ; native 7006
    mov WORD PTR [bp-06h],ss ; native 7009
L_700C:
    les bx,DWORD PTR [bp-0ch] ; native 700C
    mov al,ES:[bx] ; native 700F
    sub ah,ah ; native 7012
    xor al,06ah ; native 7014
    or al,020h ; native 7016
    les bx,DWORD PTR [bp-08h] ; native 7018
    mov cl,ES:[bx] ; native 701B
    sub ch,ch ; native 701E
    or cl,020h ; native 7020
    cmp ax,cx ; native 7023
    jnz L_7041 ; native 7025
    add WORD PTR [bp-08h],01h ; native 7027
    sbb ax,ax ; native 702B
    and ax,01000h ; native 702D
    add [bp-06h],ax ; native 7030
    add WORD PTR [bp-0ch],01h ; native 7033
    sbb ax,ax ; native 7037
    and ax,01000h ; native 7039
    add [bp-0ah],ax ; native 703C
    jmp SHORT L_700C ; native 703F
L_7041:
    les bx,DWORD PTR [bp-08h] ; native 7041
    cmp BYTE PTR ES:[bx],00h ; native 7044
    jnz L_7053 ; native 7048
    les bx,DWORD PTR [bp-0ch] ; native 704A
    cmp BYTE PTR ES:[bx],067h ; native 704D
    jz L_7061 ; native 7051
L_7053:
    mov ax,[bp-04h] ; native 7053
    inc WORD PTR [bp-04h] ; native 7056
    cmp ax,02h ; native 7059
    jnl L_7061 ; native 705C
    jmp NEAR PTR L_6CF9 ; native 705E
L_7061:
    mov ax,077h ; native 7061
    push ax ; native 7064
    mov ax,050h ; native 7065
    push ax ; native 7068
    mov ax,04bh ; native 7069
    push ax ; native 706C
    mov ax,04h ; native 706D
    push ax ; native 7070
    call NEAR PTR _restore_region_58b0 ; native 7071
    add sp,08h ; native 7074
    les bx,DWORD PTR [bp-08h] ; native 7077
    cmp BYTE PTR ES:[bx],00h ; native 707A
L_707E:
    nop ; native 707E
L_707F:
    nop ; native 707F
    les bx,DWORD PTR [bp-0ch] ; native 7080
    cmp BYTE PTR ES:[bx],067h ; native 7083
L_7087:
    jmp SHORT L_708D ; native 7087
L_7089:
    jmp SHORT L_7089 ; native 7089
L_708B:
    jmp SHORT L_70E6 ; native 708B
L_708D:
    les bx,DWORD PTR [bp-08h] ; native 708D
    mov al,030h ; native 7090
    mul BYTE PTR ES:[bx] ; native 7092
    add ax,OFFSET DGROUP:_piece_controls+48 ; native 7095
    mov [bp-02h],ax ; native 7098
    mov al,ES:[bx] ; native 709B
    sub ah,ah ; native 709E
    add ax,WORD PTR _asset_table_8ae4 ; native 70A0
    mov [bp-08h],ax ; native 70A4
    mov WORD PTR [bp-06h],ds ; native 70A7
    sub si,si ; native 70AA
    jmp SHORT L_70AF ; native 70AC
L_70AE:
    inc si ; native 70AE
L_70AF:
    cmp si,090h ; native 70AF
    jnl L_70E6 ; native 70B3
    mov bx,[bp-02h] ; native 70B5
    add WORD PTR [bp-02h],02h ; native 70B8
    mov ax,[bp-08h] ; native 70BC
    mov [bx],ax ; native 70BF
L_70C1:
    les bx,DWORD PTR [bp-08h] ; native 70C1
    cmp BYTE PTR ES:[bx],0ffh ; native 70C4
    jz L_70D8 ; native 70C8
    add WORD PTR [bp-08h],01h ; native 70CA
    sbb ax,ax ; native 70CE
    and ax,01000h ; native 70D0
    add [bp-06h],ax ; native 70D3
    jmp SHORT L_70C1 ; native 70D6
L_70D8:
    add WORD PTR [bp-08h],01h ; native 70D8
    sbb ax,ax ; native 70DC
    and ax,01000h ; native 70DE
    add [bp-06h],ax ; native 70E1
    jmp SHORT L_70AE ; native 70E4
L_70E6:
    call NEAR PTR _end_input_102d ; native 70E6
    pop si ; native 70E9
    pop di ; native 70EA
    mov sp,bp ; native 70EB
    pop bp ; native 70ED
L_70EE:
    ret ; native 70EE
_init_animation ENDP
_TEXT ENDS
END

; SECOND_AUTHORED_SOURCE_BOUNDARY
; Authored mnemonic reconstruction; original language/TU and C frame cause held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _asset_groups:BYTE, _frames:BYTE, _piece_controls:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _task_ready_772d:NEAR, _pop_value:NEAR
EXTRN _compose_frame_3b3a:NEAR, _attach_actor:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _turn_task_730c
_turn_task_730c PROC NEAR
    push bp ; native 730C
    mov bp, sp ; native 730D
    mov ax, 10h ; native 730F
    call NEAR PTR __chkstk ; native 7312
    push di ; native 7315
    push si ; native 7316
    mov si, word ptr [bp+4h] ; native 7317
    cmp word ptr [si+0ch], 0h ; native 731A
    jz SHORT turn_7330 ; native 731E
    push si ; native 7320
    call NEAR PTR _task_ready_772d ; native 7321
    add sp, 2h ; native 7324
    or ax, ax ; native 7327
    jnz SHORT turn_7330 ; native 7329
    sub ax, ax ; native 732B
    jmp NEAR PTR turn_7586 ; native 732D
turn_7330:
    mov ax, word ptr [si] ; native 7330
    mov word ptr [bp-0ch], ax ; native 7332
    mov di, word ptr [si+6h] ; native 7335
    mov al, byte ptr [si+0eh] ; native 7338
    sub ah, ah ; native 733B
    mov word ptr [bp-0eh], ax ; native 733D
    mov al, byte ptr [si+10h] ; native 7340
    mov byte ptr [bp-8h], al ; native 7343
    cmp word ptr [bp-0ch], 0h ; native 7346
    jz SHORT turn_734f ; native 734A
    jmp NEAR PTR turn_752d ; native 734C
turn_734f:
    cmp word ptr [si+0ch], 0h ; native 734F
    jnz SHORT turn_7358 ; native 7353
    jmp NEAR PTR turn_7451 ; native 7355
turn_7358:
    mov al, byte ptr [si+0ch] ; native 7358
    add al, byte ptr [bp-0eh] ; native 735B
    and al, 7h ; native 735E
    cmp al, byte ptr [si+0fh] ; native 7360
    jnz SHORT turn_736b ; native 7363
    mov ax, 1h ; native 7365
    jmp NEAR PTR turn_7586 ; native 7368
turn_736b:
    mov ax, word ptr [si+0ch] ; native 736B
    add ax, word ptr [bp-0eh] ; native 736E
    and ax, 7h ; native 7371
    mov word ptr [bp-0eh], ax ; native 7374
    cmp word ptr [si+0ch], 0h ; native 7377
    jle SHORT turn_7382 ; native 737B
    add ax, 8h ; native 737D
    jmp SHORT turn_7388 ; native 7380
turn_7382:
    mov ax, word ptr [bp-0eh] ; native 7382
    add ax, 10h ; native 7385
turn_7388:
    mov word ptr [bp-6h], ax ; native 7388
    cmp byte ptr [bp-8h], 3h ; native 738B
    jz SHORT turn_739d ; native 738F
    cmp byte ptr [bp-8h], 6h ; native 7391
    jz SHORT turn_739d ; native 7395
    cmp byte ptr [bp-8h], 1h ; native 7397
    jnz SHORT turn_73a0 ; native 739B
turn_739d:
    shr word ptr [bp-6h], 1h ; native 739D
turn_73a0:
    cmp byte ptr [bp-8h], 2h ; native 73A0
    jz SHORT turn_73b2 ; native 73A4
    cmp byte ptr [bp-8h], 5h ; native 73A6
    jz SHORT turn_73b2 ; native 73AA
    cmp byte ptr [bp-8h], 1h ; native 73AC
    jnz SHORT turn_740d ; native 73B0
turn_73b2:
    mov al, 14h ; native 73B2
    mul byte ptr [bp-8h] ; native 73B4
    mov bx, ax ; native 73B7
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 73B9
    mov ax, word ptr [bp-6h] ; native 73BD
    shl ax, 1h ; native 73C0
    add bx, ax ; native 73C2
    mov ax, word ptr [bx] ; native 73C4
    mov word ptr [bp-0ch], ax ; native 73C6
    add word ptr [bp-0ch], 4h ; native 73C9
    mov ax, word ptr [di+14h] ; native 73CD
    mov word ptr [bp-4h], ax ; native 73D0
    call NEAR PTR _pop_value ; native 73D3
    mov word ptr [bp-2h], ax ; native 73D6
    push ax ; native 73D9
    mov bx, word ptr [bp-0ch] ; native 73DA
    add word ptr [bp-0ch], 2h ; native 73DD
    push word ptr [bx] ; native 73E1
    push word ptr [bp-4h] ; native 73E3
    call NEAR PTR _compose_frame_3b3a ; native 73E6
    add sp, 6h ; native 73E9
    mov ax, word ptr [bp-2h] ; native 73EC
    mov word ptr [bp-4h], ax ; native 73EF
    push di ; native 73F2
    push ax ; native 73F3
    mov al, byte ptr [di+0ah] ; native 73F4
    sub ah, ah ; native 73F7
    push ax ; native 73F9
    push word ptr [di+6h] ; native 73FA
    push word ptr [di+4h] ; native 73FD
    call NEAR PTR _attach_actor ; native 7400
    add sp, 0ah ; native 7403
    mov word ptr [di+8h], 1h ; native 7406
    jmp SHORT turn_744e ; native 740B
turn_740d:
    mov al, 14h ; native 740D
    mul byte ptr [bp-8h] ; native 740F
    mov bx, ax ; native 7412
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 7414
    mov ax, word ptr [bp-6h] ; native 7418
    shl ax, 1h ; native 741B
    add bx, ax ; native 741D
    mov ax, word ptr [bx] ; native 741F
    mov word ptr [bp-0ch], ax ; native 7421
    mov bx, ax ; native 7424
    add word ptr [bp-0ch], 2h ; native 7426
    mov ax, word ptr [bx] ; native 742A
    mov cl, 3h ; native 742C
    shl ax, cl ; native 742E
    add ax,OFFSET DGROUP:_frames ; native 7430
    mov word ptr [bp-4h], ax ; native 7433
    push di ; native 7436
    push ax ; native 7437
    mov al, byte ptr [di+0ah] ; native 7438
    sub ah, ah ; native 743B
    push ax ; native 743D
    push word ptr [di+2h] ; native 743E
    push word ptr [di] ; native 7441
    call NEAR PTR _attach_actor ; native 7443
    add sp, 0ah ; native 7446
    mov word ptr [di+8h], 0h ; native 7449
turn_744e:
    jmp NEAR PTR turn_74fc ; native 744E
turn_7451:
    mov al, byte ptr [si+0fh] ; native 7451
    sub ah, ah ; native 7454
    cmp ax, word ptr [bp-0eh] ; native 7456
    jnz SHORT turn_7461 ; native 7459
    mov ax, 1h ; native 745B
    jmp NEAR PTR turn_7586 ; native 745E
turn_7461:
    mov al, byte ptr [si+0fh] ; native 7461
    sub al, byte ptr [bp-0eh] ; native 7464
    test al, 4h ; native 7467
    jz SHORT turn_7470 ; native 7469
    mov ax, 0ffffh ; native 746B
    jmp SHORT turn_7473 ; native 746E
turn_7470:
    mov ax, 1h ; native 7470
turn_7473:
    mov word ptr [si+0ch], ax ; native 7473
    or ax, ax ; native 7476
    jle SHORT turn_7482 ; native 7478
    mov ax, word ptr [bp-0eh] ; native 747A
    add ax, 8h ; native 747D
    jmp SHORT turn_7488 ; native 7480
turn_7482:
    mov ax, word ptr [bp-0eh] ; native 7482
    add ax, 10h ; native 7485
turn_7488:
    mov word ptr [bp-6h], ax ; native 7488
    cmp byte ptr [bp-8h], 3h ; native 748B
    jz SHORT turn_749d ; native 748F
    cmp byte ptr [bp-8h], 6h ; native 7491
    jz SHORT turn_749d ; native 7495
    cmp byte ptr [bp-8h], 1h ; native 7497
    jnz SHORT turn_74b9 ; native 749B
turn_749d:
    shl word ptr [si+0ch], 1h ; native 749D
    mov al, 14h ; native 74A0
    mul byte ptr [bp-8h] ; native 74A2
    mov bx, ax ; native 74A5
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 74A7
    mov ax, word ptr [bp-6h] ; native 74AB
    and al, 0feh ; native 74AE
    add bx, ax ; native 74B0
    mov ax, word ptr [bx] ; native 74B2
    mov word ptr [bp-0ch], ax ; native 74B4
    jmp SHORT turn_74d0 ; native 74B7
turn_74b9:
    mov al, 14h ; native 74B9
    mul byte ptr [bp-8h] ; native 74BB
    mov bx, ax ; native 74BE
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 74C0
    mov ax, word ptr [bp-6h] ; native 74C4
    shl ax, 1h ; native 74C7
    add bx, ax ; native 74C9
    mov ax, word ptr [bx] ; native 74CB
    mov word ptr [bp-0ch], ax ; native 74CD
turn_74d0:
    mov bx, word ptr [bp-0ch] ; native 74D0
    add word ptr [bp-0ch], 2h ; native 74D3
    mov ax, word ptr [bx] ; native 74D7
    mov cl, 3h ; native 74D9
    shl ax, cl ; native 74DB
    add ax,OFFSET DGROUP:_frames ; native 74DD
    mov word ptr [bp-4h], ax ; native 74E0
    push di ; native 74E3
    push ax ; native 74E4
    mov al, byte ptr [di+0ah] ; native 74E5
    sub ah, ah ; native 74E8
    push ax ; native 74EA
    push word ptr [di+6h] ; native 74EB
    push word ptr [di+4h] ; native 74EE
    call NEAR PTR _attach_actor ; native 74F1
    add sp, 0ah ; native 74F4
    mov word ptr [di+8h], 0h ; native 74F7
turn_74fc:
    cmp word ptr [si+0ch], 0h ; native 74FC
    jge SHORT turn_7506 ; native 7500
    sub bx, bx ; native 7502
    jmp SHORT turn_7509 ; native 7504
turn_7506:
    mov bx, 1h ; native 7506
turn_7509:
    mov ax, word ptr [bp-0eh] ; native 7509
    shl ax, 1h ; native 750C
    add bx, ax ; native 750E
    shl bx, 1h ; native 7510
    mov al, 30h ; native 7512
    mul byte ptr [bp-8h] ; native 7514
    add bx, ax ; native 7517
    mov ax, word ptr [bx+_piece_controls+10h] ; native 7519
    mov word ptr [si+4h], ax ; native 751D
    mov byte ptr [si+2h], 0h ; native 7520
    push si ; native 7524
    call NEAR PTR _task_ready_772d ; native 7525
    add sp, 2h ; native 7528
    jmp SHORT turn_756a ; native 752B
turn_752d:
    mov ax, word ptr [di+14h] ; native 752D
    mov word ptr [bp-4h], ax ; native 7530
    call NEAR PTR _pop_value ; native 7533
    mov word ptr [bp-2h], ax ; native 7536
    push ax ; native 7539
    mov bx, word ptr [bp-0ch] ; native 753A
    add word ptr [bp-0ch], 2h ; native 753D
    push word ptr [bx] ; native 7541
    push word ptr [bp-4h] ; native 7543
    call NEAR PTR _compose_frame_3b3a ; native 7546
    add sp, 6h ; native 7549
    mov ax, word ptr [bp-2h] ; native 754C
    mov word ptr [bp-4h], ax ; native 754F
    push di ; native 7552
    push ax ; native 7553
    mov al, byte ptr [di+0ah] ; native 7554
    sub ah, ah ; native 7557
    push ax ; native 7559
    push word ptr [di+2h] ; native 755A
    push word ptr [di] ; native 755D
    call NEAR PTR _attach_actor ; native 755F
    add sp, 0ah ; native 7562
    mov word ptr [di+8h], 1h ; native 7565
turn_756a:
    mov bx, word ptr [bp-0ch] ; native 756A
    cmp word ptr [bx], -1h ; native 756D
    jnz SHORT turn_7577 ; native 7570
    mov word ptr [bp-0ch], 0h ; native 7572
turn_7577:
    mov ax, word ptr [bp-0ch] ; native 7577
    mov word ptr [si], ax ; native 757A
    mov al, byte ptr [bp-0eh] ; native 757C
    mov byte ptr [si+0eh], al ; native 757F
    sub ax, ax ; native 7582
    jmp SHORT turn_7586 ; native 7584
turn_7586:
    pop si ; native 7586
    pop di ; native 7587
    mov sp, bp ; native 7588
    pop bp ; native 758A
    ret ; native 758B
_turn_task_730c ENDP
_TEXT ENDS
END
