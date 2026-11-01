;	Static Name Aliases
;
	TITLE   C:\UNIT.C
	NAME    UNIT

	.8087
_TEXT	SEGMENT  WORD PUBLIC 'CODE'
_TEXT	ENDS
_DATA	SEGMENT  WORD PUBLIC 'DATA'
_DATA	ENDS
CONST	SEGMENT  WORD PUBLIC 'CONST'
CONST	ENDS
_BSS	SEGMENT  WORD PUBLIC 'BSS'
_BSS	ENDS
DGROUP	GROUP	CONST, _BSS, _DATA
	ASSUME  CS: _TEXT, DS: DGROUP, SS: DGROUP
EXTRN	__acrtused:ABS
EXTRN	_attach_actor:NEAR
EXTRN	__chkstk:NEAR
EXTRN	_task_ready_772d:NEAR
EXTRN	_pop_value:NEAR
EXTRN	_compose_frame_3b3a:NEAR
EXTRN	_interpolate_position_5ebc:NEAR
EXTRN	_screen_x:WORD
EXTRN	_screen_y:WORD
EXTRN	_command_active:WORD
EXTRN	_motion_x:WORD
EXTRN	_motion_y:WORD
EXTRN	_frame_lists:BYTE
EXTRN	_frames:BYTE
_TEXT      SEGMENT
	ASSUME	CS: _TEXT
; Line 24
	PUBLIC	_move_task_68ea
_move_task_68ea	PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,16
	call	__chkstk
	push	di
	push	si
	mov	si,WORD PTR [bp+4]	;task
;	register si = task
;	a = -2
;	b = -4
;	register di = c
;	d = -8
;	e = -10
;	f = -12
; Line 26
	push	si
	call	_task_ready_772d
	add	sp,2
	or	ax,ax
	jne	$I190
	sub	ax,ax
	jmp	$EX183
; Line 27
$I190:
	mov	ax,WORD PTR [si]
	mov	WORD PTR [bp-8],ax	;d
	mov	di,WORD PTR [si+6]
	mov	ax,WORD PTR [si+12]
	mov	WORD PTR [bp-10],ax	;e
; Line 28
	cmp	BYTE PTR [si+16],0
	je	$JCC48
	jmp	$I191
$JCC48:
; Line 29
	mov	bx,ax
	shl	bx,1
	mov	ax,WORD PTR _frame_lists[bx]
	mov	WORD PTR [bp-8],ax	;d
; Line 30
	cmp	WORD PTR _command_active,0
	jne	$I192
; Line 31
	mov	WORD PTR [bp-12],0	;f
	jmp	SHORT $F193
$FC194:
	inc	WORD PTR [bp-12]	;f
	add	WORD PTR [bp-8],2	;d
$F193:
	mov	bx,WORD PTR [bp-8]	;d
	cmp	WORD PTR [bx],-1
	je	$FB195
	jmp	SHORT $FC194
$FB195:
; Line 32
	mov	al,BYTE PTR [bp-12]	;f
	mov	BYTE PTR [si+16],al
	mov	bx,WORD PTR [bp-10]	;e
	shl	bx,1
	mov	ax,WORD PTR _frame_lists[bx]
	mov	WORD PTR [bp-8],ax	;d
; Line 33
	jmp	SHORT $I196
$I192:
	mov	BYTE PTR [si+16],8
$I196:
; Line 34
	mov	BYTE PTR [si+17],1
; Line 35
	cmp	WORD PTR _command_active,0
	je	$L20001
	mov	ax,WORD PTR [bp-10]	;e
	mov	cl,3
	shl	ax,cl
	add	ax,OFFSET _frames
	jmp	SHORT $L20002
$L20001:
	mov	bx,WORD PTR [bp-8]	;d
	add	WORD PTR [bp-8],2	;d
	mov	ax,WORD PTR [bx]
	mov	cl,3
	shl	ax,cl
	add	ax,OFFSET _frames
$L20002:
	mov	WORD PTR [bp-4],ax	;b
; Line 36
	mov	bl,BYTE PTR [si+14]
	sub	bh,bh
	shl	bx,1
	add	bx,_screen_x
	mov	ax,WORD PTR [bx]
	mov	_motion_x,ax
	mov	bl,BYTE PTR [si+14]
	sub	bh,bh
	mov	cl,3
	shr	bx,cl
	shl	bx,1
	add	bx,_screen_y
	mov	ax,WORD PTR [bx]
	mov	_motion_y,ax
; Line 37
	push	di
	push	WORD PTR [bp-4]	;b
	mov	al,BYTE PTR [di+10]
	sub	ah,ah
	push	ax
	push	WORD PTR _motion_y
	push	WORD PTR _motion_x
	call	_attach_actor
	add	sp,10
	mov	WORD PTR [di+8],0
; Line 38
	jmp	$I197
$I191:
; Line 39
	mov	al,BYTE PTR [si+16]
	cmp	BYTE PTR [si+17],al
	jb	$I198
; Line 40
	mov	bl,BYTE PTR [si+15]
	sub	bh,bh
	shl	bx,1
	add	bx,_screen_x
	mov	ax,WORD PTR [bx]
	mov	WORD PTR [di+4],ax
	mov	bl,BYTE PTR [si+15]
	sub	bh,bh
	mov	cl,3
	shr	bx,cl
	shl	bx,1
	add	bx,_screen_y
	mov	ax,WORD PTR [bx]
	mov	WORD PTR [di+6],ax
	mov	ax,1
	jmp	$EX183
; Line 41
; Line 42
$I198:
	mov	ax,WORD PTR [di+20]
	mov	WORD PTR [bp-4],ax	;b
; Line 43
	cmp	WORD PTR _command_active,0
	jne	$I199
	call	_pop_value
	mov	WORD PTR [bp-2],ax	;a
	push	ax
	mov	bx,WORD PTR [bp-8]	;d
	add	WORD PTR [bp-8],2	;d
	push	WORD PTR [bx]
	push	WORD PTR [bp-4]	;b
	call	_compose_frame_3b3a
	add	sp,6
	mov	ax,WORD PTR [bp-2]	;a
	mov	WORD PTR [bp-4],ax	;b
; Line 44
$I199:
	mov	al,BYTE PTR [si+14]
	sub	ah,ah
	mov	WORD PTR [bp-14],ax
	mov	al,BYTE PTR [si+15]
	mov	WORD PTR [bp-16],ax
	mov	al,BYTE PTR [si+17]
	inc	BYTE PTR [si+17]
	push	ax
	mov	al,BYTE PTR [si+16]
	push	ax
	mov	bx,WORD PTR [bp-16]
	mov	cl,3
	shr	bx,cl
	shl	bx,1
	add	bx,_screen_y
	push	WORD PTR [bx]
	mov	bx,WORD PTR [bp-16]
	shl	bx,1
	add	bx,_screen_x
	push	WORD PTR [bx]
	mov	bx,WORD PTR [bp-14]
	shr	bx,cl
	shl	bx,1
	add	bx,_screen_y
	push	WORD PTR [bx]
	mov	bx,WORD PTR [bp-14]
	shl	bx,1
	add	bx,_screen_x
	push	WORD PTR [bx]
	call	_interpolate_position_5ebc
	add	sp,12
; Line 45
	push	di
	push	WORD PTR [bp-4]	;b
	mov	al,BYTE PTR [di+10]
	sub	ah,ah
	push	ax
	push	WORD PTR _motion_y
	push	WORD PTR _motion_x
	call	_attach_actor
	add	sp,10
	cmp	WORD PTR _command_active,1
	sbb	ax,ax
	neg	ax
	mov	WORD PTR [di+8],ax
; Line 46
$I197:
; Line 47
	mov	ax,WORD PTR [bp-8]	;d
	mov	WORD PTR [si],ax
	sub	ax,ax
	jmp	SHORT $EX183
; Line 48
$EX183:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret	

_move_task_68ea	ENDP
; Line 51
	PUBLIC	_effect_task_6ab1
_effect_task_6ab1	PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,12
	call	__chkstk
	push	di
	push	si
	mov	si,WORD PTR [bp+4]	;task
;	register si = task
;	a = -2
;	b = -4
;	register di = c
;	d = -8
;	e = -10
;	f = -12
; Line 53
	push	si
	call	_task_ready_772d
	add	sp,2
	or	ax,ax
	jne	$I209
	sub	ax,ax
	jmp	$I216
; Line 54
$I209:
	mov	ax,WORD PTR [si]
	mov	WORD PTR [bp-8],ax	;d
	mov	di,WORD PTR [si+6]
	mov	ax,WORD PTR [si+12]
	mov	WORD PTR [bp-10],ax	;e
; Line 55
	cmp	WORD PTR [bp-8],0	;d
	jne	$I210
; Line 56
	mov	bx,ax
	shl	bx,1
	mov	ax,WORD PTR _frame_lists[bx]
	mov	WORD PTR [bp-8],ax	;d
	mov	ax,WORD PTR [di+4]
	mov	WORD PTR [si+14],ax
	mov	ax,WORD PTR [di+6]
	mov	WORD PTR [si+16],ax
; Line 57
	mov	WORD PTR [bp-12],0	;f
	jmp	SHORT $F211
$FC212:
	inc	WORD PTR [bp-12]	;f
	add	WORD PTR [bp-8],2	;d
$F211:
	mov	bx,WORD PTR [bp-8]	;d
	cmp	WORD PTR [bx],-1
	je	$FB213
	jmp	SHORT $FC212
$FB213:
; Line 58
	mov	ax,WORD PTR [bp-12]	;f
	shr	ax,1
	mov	BYTE PTR [si+18],al
	mov	BYTE PTR [si+19],1
	mov	bx,WORD PTR [bp-10]	;e
	shl	bx,1
	mov	ax,WORD PTR _frame_lists[bx]
	mov	WORD PTR [bp-8],ax	;d
	mov	bx,ax
	add	WORD PTR [bp-8],2	;d
	mov	ax,WORD PTR [bx]
	mov	cl,3
	shl	ax,cl
	add	ax,OFFSET _frames
	mov	WORD PTR [bp-4],ax	;b
; Line 59
	push	di
	push	ax
	mov	al,BYTE PTR [di+10]
	sub	ah,ah
	push	ax
	push	WORD PTR [di+6]
	push	WORD PTR [di+4]
	call	_attach_actor
	add	sp,10
	mov	WORD PTR [di+8],0
; Line 60
	jmp	SHORT $I214
$I210:
; Line 61
	mov	ax,WORD PTR [di+20]
	mov	WORD PTR [bp-4],ax	;b
	call	_pop_value
	mov	WORD PTR [bp-2],ax	;a
	push	ax
	mov	bx,WORD PTR [bp-8]	;d
	add	WORD PTR [bp-8],2	;d
	push	WORD PTR [bx]
	push	WORD PTR [bp-4]	;b
	call	_compose_frame_3b3a
	add	sp,6
; Line 62
	mov	al,BYTE PTR [si+19]
	inc	BYTE PTR [si+19]
	sub	ah,ah
	push	ax
	mov	al,BYTE PTR [si+18]
	push	ax
	mov	al,BYTE PTR [si+21]
	cbw	
	add	ax,WORD PTR [si+16]
	push	ax
	mov	al,BYTE PTR [si+20]
	cbw	
	add	ax,WORD PTR [si+14]
	push	ax
	push	WORD PTR [si+16]
	push	WORD PTR [si+14]
	call	_interpolate_position_5ebc
	add	sp,12
; Line 63
	mov	ax,WORD PTR [bp-2]	;a
	mov	WORD PTR [bp-4],ax	;b
	push	di
	push	ax
	mov	al,BYTE PTR [di+10]
	sub	ah,ah
	push	ax
	push	WORD PTR _motion_y
	push	WORD PTR _motion_x
	call	_attach_actor
	add	sp,10
	mov	WORD PTR [di+8],1
; Line 64
$I214:
; Line 65
	mov	al,BYTE PTR [si+18]
	sub	ah,ah
	inc	ax
	mov	cl,BYTE PTR [si+19]
	sub	ch,ch
	cmp	ax,cx
	jne	$I215
; Line 66
	mov	al,BYTE PTR [si+20]
	cbw	
	add	ax,WORD PTR [si+14]
	mov	WORD PTR [di+4],ax
	mov	al,BYTE PTR [si+21]
	cbw	
	add	ax,WORD PTR [si+16]
	mov	WORD PTR [di+6],ax
	mov	ax,1
	jmp	SHORT $I216
; Line 67
	jmp	SHORT $I216
$I215:
	mov	ax,WORD PTR [bp-8]	;d
	mov	WORD PTR [si],ax
	sub	ax,ax
	jmp	SHORT $I216
$I216:
; Line 68
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret	

_effect_task_6ab1	ENDP

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

; Finalize WORD module after two real C procedures and authored ASM.
	EVEN
_TEXT	ENDS
END
