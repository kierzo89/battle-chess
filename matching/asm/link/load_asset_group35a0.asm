; Whole native35A0..3652. Frame12/BP-12 preserved; C compiler explanation held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _asset_state:BYTE, _asset_groups:BYTE, _frame_directory:BYTE
EXTRN _asset_group_frame_counts:BYTE
EXTRN _frame_data_cursor:WORD, _frame_list_cursor:WORD, _frame_count:WORD, _arena_cursor:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _select_asset_file:NEAR, _load_group_frames:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _load_asset_group
_load_asset_group PROC NEAR
    push bp ; native 35A0
    mov bp,sp ; native 35A1
    sub sp,0Ch ; native 35A3
    push di ; native 35A6
    push si ; native 35A7
    mov si,WORD PTR [bp+4] ; native 35A8
    mov BYTE PTR _asset_state[si],01h ; native 35AB
    mov ax,014h ; native 35B0
    imul si ; native 35B3
    mov WORD PTR [bp-12],ax ; native 35B5
    mov bx,ax ; native 35B8
    mov ax,WORD PTR _frame_data_cursor ; native 35BA
    mov WORD PTR _asset_groups+12[bx],ax ; native 35BD
    mov bx,WORD PTR [bp-12] ; native 35C1
    mov ax,WORD PTR _frame_list_cursor ; native 35C4
    mov WORD PTR _asset_groups+8[bx],ax ; native 35C7
    mov bx,WORD PTR [bp-12] ; native 35CB
    mov ax,WORD PTR _frame_count ; native 35CE
    mov WORD PTR _asset_groups+14[bx],ax ; native 35D1
    mov bx,WORD PTR [bp-12] ; native 35D5
    mov ax,WORD PTR _arena_cursor ; native 35D8
    mov dx,WORD PTR _arena_cursor+2 ; native 35DB
    mov WORD PTR _asset_groups[bx],ax ; native 35DF
    mov WORD PTR _asset_groups+2[bx],dx ; native 35E3
    mov ax,01h ; native 35E7
    push ax ; native 35EA
    call NEAR PTR _select_asset_file ; native 35EB
    add sp,02h ; native 35EE
    sub di,di ; native 35F1
    jmp SHORT directory_test ; native 35F3
directory_fill:
    mov ax,di ; native 35F5
    mov BYTE PTR _frame_directory[di],al ; native 35F7
    inc di ; native 35FB
directory_test:
    mov al,BYTE PTR _asset_group_frame_counts[si] ; native 35FC
    sub ah,ah ; native 3600
    cmp ax,di ; native 3602
    ja SHORT directory_fill ; native 3604
    mov BYTE PTR _frame_directory[di],0FFh ; native 3606
    lea ax,[si+03h] ; native 360B
    push ax ; native 360E
    mov ax,di ; native 360F
    add ax,OFFSET DGROUP:_frame_directory+2 ; native 3611
    push ax ; native 3614
    mov ax,OFFSET DGROUP:_frame_directory ; native 3615
    push ax ; native 3618
    call NEAR PTR _load_group_frames ; native 3619
    add sp,06h ; native 361C
    mov ax,014h ; native 361F
    imul si ; native 3622
    mov WORD PTR [bp-12],ax ; native 3624
    mov bx,ax ; native 3627
    mov ax,WORD PTR _frame_list_cursor ; native 3629
    mov WORD PTR _asset_groups+10[bx],ax ; native 362C
    mov bx,WORD PTR [bp-12] ; native 3630
    mov ax,WORD PTR _frame_count ; native 3633
    mov WORD PTR _asset_groups+16[bx],ax ; native 3636
    mov bx,WORD PTR [bp-12] ; native 363A
    mov ax,WORD PTR _arena_cursor ; native 363D
    mov dx,WORD PTR _arena_cursor+2 ; native 3640
    mov WORD PTR _asset_groups+4[bx],ax ; native 3644
    mov WORD PTR _asset_groups+6[bx],dx ; native 3648
    pop si ; native 364C
    pop di ; native 364D
    mov sp,bp ; native 364E
    pop bp ; native 3650
    ret ; native 3651
_load_asset_group ENDP
_TEXT ENDS
END
