; Authored ASM reconstruction; original source language and C frame reason unknown.
; BYTE CODE alignment permits actual odd6BF9, not a recovered historical SEGDEF.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _motion_x:WORD, _motion_y:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR
EXTRN _interpolate_position_5ebc:NEAR, _attach_actor:NEAR
_TEXT SEGMENT BYTE PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _special_task_6bf9
_special_task_6bf9 PROC NEAR
    push bp ; native 6BF9
    mov bp,sp ; native 6BFA
    mov ax,0ch ; native 6BFC
    call NEAR PTR __chkstk ; native 6BFF
    push di ; native 6C02
    push si ; native 6C03
    mov si,WORD PTR [bp+4] ; native 6C04
    cmp BYTE PTR [si+2],0 ; native 6C07
    je SHORT ready_task ; native 6C0B
    dec BYTE PTR [si+2] ; native 6C0D
    sub ax,ax ; native 6C10
    jmp NEAR PTR finish_task ; native 6C12
ready_task:
    mov BYTE PTR [si+2],0 ; native 6C15
    mov di,WORD PTR [si+6] ; native 6C19
    cmp BYTE PTR [si+12h],0 ; native 6C1C
    jne SHORT interpolate_task ; native 6C20
    mov ax,WORD PTR [di+4] ; native 6C22
    mov WORD PTR [si+0eh],ax ; native 6C25
    mov ax,WORD PTR [di+6] ; native 6C28
    mov WORD PTR [si+10h],ax ; native 6C2B
    mov BYTE PTR [si+12h],6 ; native 6C2E
    mov BYTE PTR [si+13h],0 ; native 6C32
interpolate_task:
    mov ax,WORD PTR [di+14h] ; native 6C36
    mov WORD PTR [bp-4],ax ; native 6C39
    mov al,BYTE PTR [si+13h] ; native 6C3C
    inc BYTE PTR [si+13h] ; native 6C3F
    sub ah,ah ; native 6C42
    push ax ; native 6C44
    mov al,BYTE PTR [si+12h] ; native 6C45
    push ax ; native 6C48
    mov al,BYTE PTR [si+15h] ; native 6C49
    cbw ; native 6C4C
    add ax,WORD PTR [si+10h] ; native 6C4D
    push ax ; native 6C50
    mov al,BYTE PTR [si+14h] ; native 6C51
    cbw ; native 6C54
    add ax,WORD PTR [si+0eh] ; native 6C55
    push ax ; native 6C58
    push WORD PTR [si+10h] ; native 6C59
    push WORD PTR [si+0eh] ; native 6C5C
    call NEAR PTR _interpolate_position_5ebc ; native 6C5F
    add sp,0ch ; native 6C62
    push di ; native 6C65
    push WORD PTR [bp-4] ; native 6C66
    mov al,BYTE PTR [di+0ah] ; native 6C69
    sub ah,ah ; native 6C6C
    push ax ; native 6C6E
    push WORD PTR _motion_y ; native 6C6F
    push WORD PTR _motion_x ; native 6C73
    call NEAR PTR _attach_actor ; native 6C77
    add sp,0ah ; native 6C7A
    mov WORD PTR [di+8],0 ; native 6C7D
    mov al,BYTE PTR [si+12h] ; native 6C82
    sub ah,ah ; native 6C85
    inc ax ; native 6C87
    mov cl,BYTE PTR [si+13h] ; native 6C88
    sub ch,ch ; native 6C8B
    cmp ax,cx ; native 6C8D
    jne SHORT pending_task ; native 6C8F
    mov al,BYTE PTR [si+14h] ; native 6C91
    cbw ; native 6C94
    add ax,WORD PTR [si+0eh] ; native 6C95
    mov WORD PTR [di+4],ax ; native 6C98
    mov al,BYTE PTR [si+15h] ; native 6C9B
    cbw ; native 6C9E
    add ax,WORD PTR [si+10h] ; native 6C9F
    mov WORD PTR [di+6],ax ; native 6CA2
    mov ax,1 ; native 6CA5
    jmp SHORT finish_task ; native 6CA8
pending_task:
    sub ax,ax ; native 6CAA
    jmp SHORT finish_task ; native 6CAC
finish_task:
    pop si ; native 6CAE
    pop di ; native 6CAF
    mov sp,bp ; native 6CB0
    pop bp ; native 6CB2
    ret ; native 6CB3
_special_task_6bf9 ENDP
_TEXT ENDS
END
