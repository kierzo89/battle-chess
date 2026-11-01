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
EXTRN	_actor_map:BYTE
EXTRN	_kind_map:BYTE
EXTRN	_detach_actor:NEAR
EXTRN	_queue_piece:NEAR
EXTRN	_restore_active_arena:NEAR
EXTRN	_manage_asset_arena:NEAR
EXTRN	_remove_actor_5934:NEAR
EXTRN	_attach_actor:NEAR
EXTRN	_dispatch_c83a:NEAR
EXTRN	__chkstk:NEAR
EXTRN	_pop_value:NEAR
EXTRN	_compose_frame_3b3a:NEAR
EXTRN	_animation_counter:BYTE
EXTRN	_frame_index:WORD
EXTRN	_command_active:WORD
EXTRN	_frame_lists:BYTE
EXTRN	_actors:BYTE
EXTRN	_frames:BYTE
EXTRN	_asset_state:BYTE
EXTRN	_cells:BYTE
EXTRN	_capture_pending:BYTE
_TEXT      SEGMENT
	ASSUME	CS: _TEXT
; Line 28
	PUBLIC	_transfer_task_758c
_transfer_task_758c	PROC NEAR
	push	bp
	mov	bp,sp
	xor	ax,ax
	call	__chkstk
	push	di
	push	si
	mov	si,WORD PTR [bp+4]	;task
;	register si = task
; Line 29
	push	WORD PTR [si+6]
	mov	bx,WORD PTR [si+12]
	mov	bl,BYTE PTR _cells[bx]
	and	bx,WORD PTR 63
	mov	di,_frame_index
	mov	al,[bx][di]
	sub	ah,ah
	mov	cl,3
	shl	ax,cl
	add	ax,OFFSET _frames
	push	ax
	mov	bx,WORD PTR [si+6]
	mov	al,BYTE PTR [bx+10]
	sub	ah,ah
	push	ax
	push	WORD PTR [bx+6]
	push	WORD PTR [bx+4]
	call	_attach_actor
	add	sp,10
; Line 30
	cmp	WORD PTR [si+14],255
	je	$I200
	mov	ax,28
	imul	WORD PTR [si+14]
	add	ax,OFFSET _actors
	push	ax
	call	_remove_actor_5934
	add	sp,2
; Line 31
$I200:
	mov	bx,WORD PTR [si+6]
	mov	WORD PTR [bx+8],0
	mov	ax,1
	jmp	SHORT $EX199
; Line 32
$EX199:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret	

_transfer_task_758c	ENDP
; Line 34
	PUBLIC	_capture_task_75f6
_capture_task_75f6	PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,10
	call	__chkstk
	push	di
	push	si
	mov	si,WORD PTR [bp+4]	;task
;	register si = task
;	a = -2
;	b = -4
;	c = -6
;	register di = d
;	e = -10
; Line 36
	cmp	BYTE PTR _capture_pending,1
	jne	$I209
	sub	ax,ax
	jmp	$EX203
; Line 37
$I209:
	cmp	BYTE PTR [si+2],255
	jne	$I214
; Line 38
	cmp	BYTE PTR _capture_pending,4
	jne	$I211
; Line 39
	cmp	BYTE PTR [si+14],0
	je	$I213
; Line 40
	mov	al,_capture_pending
	add	_animation_counter,al
; Line 41
	cmp	WORD PTR _command_active,0
	jne	$I213
	call	_restore_active_arena
	mov	bl,BYTE PTR _asset_state+13
	sub	bh,bh
	mov	BYTE PTR _asset_state[bx+5],1
	mov	al,255
	mov	BYTE PTR _asset_state+13,al
	mov	BYTE PTR _asset_state+12,al
	call	_manage_asset_arena
; Line 42
$I213:
; Line 43
	mov	ax,1
	jmp	$EX203
; Line 44
	jmp	SHORT $I214
$I211:
	sub	ax,ax
	jmp	$EX203
$I214:
; Line 45
; Line 46
	push	si
	call	_task_ready_772d
	add	sp,2
	or	ax,ax
	jne	$I215
	sub	ax,ax
	jmp	$EX203
; Line 47
$I215:
	mov	ax,WORD PTR [si]
	mov	WORD PTR [bp-10],ax	;e
	mov	di,WORD PTR [si+6]
	mov	ax,WORD PTR [si+12]
	mov	WORD PTR [bp-2],ax	;a
; Line 48
	cmp	WORD PTR [bp-10],0	;e
	jne	$I216
; Line 49
	mov	bx,ax
	cmp	BYTE PTR [bx],255
	jne	$I217
	mov	BYTE PTR [si+2],255
	inc	BYTE PTR _capture_pending
	sub	ax,ax
	jmp	$EX203
; Line 50
$I217:
	mov	bx,WORD PTR [bp-2]	;a
	inc	WORD PTR [bp-2]	;a
	mov	bl,BYTE PTR [bx]
	sub	bh,bh
	shl	bx,1
	mov	ax,WORD PTR _frame_lists[bx]
	mov	WORD PTR [bp-10],ax	;e
	mov	bx,ax
	add	WORD PTR [bp-10],2	;e
	mov	ax,WORD PTR [bx]
	mov	cl,3
	shl	ax,cl
	add	ax,OFFSET _frames
	mov	WORD PTR [bp-6],ax	;c
	push	di
	push	ax
	mov	al,BYTE PTR [di+10]
	sub	ah,ah
	push	ax
	push	WORD PTR [di+2]
	push	WORD PTR [di]
	call	_attach_actor
	add	sp,10
	mov	WORD PTR [di+8],0
; Line 51
	jmp	SHORT $I218
$I216:
; Line 52
	mov	ax,WORD PTR [di+20]
	mov	WORD PTR [bp-6],ax	;c
	call	_pop_value
	mov	WORD PTR [bp-4],ax	;b
	push	ax
	mov	bx,WORD PTR [bp-10]	;e
	add	WORD PTR [bp-10],2	;e
	push	WORD PTR [bx]
	push	WORD PTR [bp-6]	;c
	call	_compose_frame_3b3a
	add	sp,6
	mov	ax,WORD PTR [bp-4]	;b
	mov	WORD PTR [bp-6],ax	;c
; Line 53
	push	di
	push	ax
	mov	al,BYTE PTR [di+10]
	sub	ah,ah
	push	ax
	push	WORD PTR [di+2]
	push	WORD PTR [di]
	call	_attach_actor
	add	sp,10
	mov	WORD PTR [di+8],1
; Line 54
$I218:
; Line 55
	mov	bx,WORD PTR [bp-10]	;e
	cmp	WORD PTR [bx],-1
	jne	$I219
	mov	WORD PTR [bp-10],0	;e
; Line 56
$I219:
	mov	ax,WORD PTR [bp-10]	;e
	mov	WORD PTR [si],ax
	mov	ax,WORD PTR [bp-2]	;a
	mov	WORD PTR [si+12],ax
	sub	ax,ax
	jmp	SHORT $EX203
; Line 57
$EX203:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret	

_capture_task_75f6	ENDP
; Line 59
	PUBLIC	_task_ready_772d
_task_ready_772d	PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,2
	call	__chkstk
	push	si
	mov	si,WORD PTR [bp+4]	;task
;	register si = task
;	a = -2
; Line 61
	cmp	BYTE PTR [si+2],0
	je	$I223
	dec	BYTE PTR [si+2]
	sub	ax,ax
	jmp	SHORT $EX221
; Line 62
$I223:
	cmp	WORD PTR _command_active,0
	jne	$I224
; Line 63
$FC226:
	mov	bx,WORD PTR [si+4]
	mov	al,BYTE PTR [bx]
	mov	BYTE PTR [bp-2],al	;a
	cmp	al,127
	jbe	$FB227
	cmp	al,255
	je	$FB227
; Line 64
	mov	bx,WORD PTR [si+4]
	mov	al,BYTE PTR [bx+1]
	sub	ah,ah
	sub	ax,64
	push	ax
	mov	bx,WORD PTR [si+6]
	mov	al,BYTE PTR [bx+10]
	sub	ah,ah
	push	ax
	mov	al,BYTE PTR [bp-2]	;a
	and	ax,15
	push	ax
	call	_dispatch_c83a
	add	sp,6
	add	WORD PTR [si+4],2
; Line 65
	jmp	SHORT $FC226
$FB227:
; Line 66
	mov	bx,WORD PTR [si+4]
	cmp	BYTE PTR [bx],255
	jne	$I228
	mov	BYTE PTR [si+2],0
; Line 67
	jmp	SHORT $I229
$I228:
	mov	bx,WORD PTR [si+4]
	inc	WORD PTR [si+4]
	mov	al,BYTE PTR [bx]
	mov	BYTE PTR [si+2],al
$I229:
; Line 68
	jmp	SHORT $I230
$I224:
	mov	BYTE PTR [si+2],0
$I230:
; Line 69
	mov	ax,1
	jmp	SHORT $EX221
; Line 70
$EX221:
	pop	si
	mov	sp,bp
	pop	bp
	ret	

_task_ready_772d	ENDP

PUBLIC _undo_animation
_undo_animation PROC NEAR
    PUSH BP ; native 77AF
    MOV BP, SP ; native 77B0
    MOV AX, 012h ; native 77B2
    CALL NEAR PTR __chkstk ; native 77B5
    PUSH DI ; native 77B8
    PUSH SI ; native 77B9
    MOV SI, word ptr [BP + 04h] ; native 77BA
    CMP word ptr [SI + 04h], 00h ; native 77BD
    JZ SHORT code_7831 ; native 77C1
    CMP byte ptr [SI + 06h], 01h ; native 77C3
    JNZ SHORT code_7831 ; native 77C7
    MOV AX, word ptr [SI] ; native 77C9
    MOV word ptr [BP-012h], AX ; native 77CB
    MOV AX, word ptr [SI + 02h] ; native 77CE
    MOV word ptr [BP-010h], AX ; native 77D1
    MOV word ptr [BP-0Eh], 00h ; native 77D4
    MOV AL, byte ptr [SI + 06h] ; native 77D9
    MOV byte ptr [BP-0Ch], AL ; native 77DC
    MOV byte ptr [BP-0Bh], 00h ; native 77DF
    LEA AX, [BP-012h] ; native 77E3
    PUSH AX ; native 77E6
    CALL NEAR PTR _undo_animation ; native 77E7
    ADD SP, 02h ; native 77EA
    MOV AL, byte ptr [SI] ; native 77ED
    AND AL, 07h ; native 77EF
    CMP AL, 06h ; native 77F1
    JNZ SHORT code_780c ; native 77F3
    MOV AX, word ptr [SI] ; native 77F5
    AND AX, 0F0h ; native 77F7
    OR AL, 05h ; native 77FA
    MOV word ptr [BP-012h], AX ; native 77FC
    MOV AX, word ptr [SI + 02h] ; native 77FF
    AND AX, 0F0h ; native 7802
    OR AL, 07h ; native 7805
    MOV word ptr [BP-010h], AX ; native 7807
    JMP SHORT code_781f ; native 780A
code_780c:
    MOV AX, word ptr [SI] ; native 780C
    AND AX, 0F0h ; native 780E
    OR AL, 03h ; native 7811
    MOV word ptr [BP-012h], AX ; native 7813
    MOV AX, word ptr [SI + 02h] ; native 7816
    AND AX, 0F0h ; native 7819
    MOV word ptr [BP-010h], AX ; native 781C
code_781f:
    MOV byte ptr [BP-0Ch], 03h ; native 781F
    MOV byte ptr [BP-0Bh], 00h ; native 7823
    MOV word ptr [BP-0Eh], 00h ; native 7827
    LEA AX, [BP-012h] ; native 782C
    MOV SI, AX ; native 782F
code_7831:
    MOV AX, word ptr [SI + 02h] ; native 7831
    SAR AX, 01h ; native 7834
    AND AL, 038h ; native 7836
    XOR AL, 038h ; native 7838
    MOV CL, byte ptr [SI + 02h] ; native 783A
    AND CL, 07h ; native 783D
    OR AL, CL ; native 7840
    MOV byte ptr [BP-0Ah], AL ; native 7842
    MOV AX, word ptr [SI] ; native 7845
    SAR AX, 01h ; native 7847
    AND AL, 038h ; native 7849
    XOR AL, 038h ; native 784B
    MOV CL, byte ptr [SI] ; native 784D
    AND CL, 07h ; native 784F
    OR AL, CL ; native 7852
    MOV byte ptr [BP-08h], AL ; native 7854
    SUB AH, AH ; native 7857
    MOV DI, AX ; native 7859
    CMP byte ptr _cells[DI], AH ; native 785B
    JZ SHORT code_7871 ; native 785F
    MOV AL, 01Ch ; native 7861
    MUL byte ptr _actor_map[DI] ; native 7863
    ADD AX, OFFSET DGROUP:_actors ; native 7867
    PUSH AX ; native 786A
    CALL NEAR PTR _detach_actor ; native 786B
    ADD SP, 02h ; native 786E
code_7871:
    MOV BL, byte ptr [BP-0Ah] ; native 7871
    SUB BH, BH ; native 7874
    MOV AL, 01Ch ; native 7876
    MUL byte ptr _actor_map[BX] ; native 7878
    ADD AX, OFFSET DGROUP:_actors ; native 787C
    PUSH AX ; native 787F
    CALL NEAR PTR _detach_actor ; native 7880
    ADD SP, 02h ; native 7883
    MOV AL, byte ptr [BP-0Ah] ; native 7886
    SUB AH, AH ; native 7889
    MOV DI, AX ; native 788B
    MOV AL, byte ptr [BP-08h] ; native 788D
    PUSH AX ; native 7890
    MOV AL, byte ptr _actor_map[DI] ; native 7891
    PUSH AX ; native 7895
    MOV AL, byte ptr _cells[DI] ; native 7896
    AND AX, 040h ; native 789A
    PUSH AX ; native 789D
    MOV BL, byte ptr [SI + 06h] ; native 789E
    SUB BH, BH ; native 78A1
    MOV AL, byte ptr _kind_map[BX] ; native 78A3
    SUB AH, AH ; native 78A7
    PUSH AX ; native 78A9
    CALL NEAR PTR _queue_piece ; native 78AA
    ADD SP, 08h ; native 78AD
    MOV BL, byte ptr [BP-0Ah] ; native 78B0
    SUB BH, BH ; native 78B3
    MOV byte ptr _cells[BX], BH ; native 78B5
    CMP word ptr [SI + 04h], 00h ; native 78B9
    JZ SHORT code_78f0 ; native 78BD
    CMP byte ptr [SI + 06h], 06h ; native 78BF
    JNZ SHORT code_78f0 ; native 78C3
    MOV AL, byte ptr [BP-0Ah] ; native 78C5
    AND AL, 038h ; native 78C8
    MOV CL, byte ptr [BP-08h] ; native 78CA
    AND CL, 07h ; native 78CD
    OR AL, CL ; native 78D0
    MOV byte ptr [BP-0Ah], AL ; native 78D2
    MOV BL, AL ; native 78D5
    MOV AL, 01Ch ; native 78D7
    MUL byte ptr _actor_map[BX] ; native 78D9
    ADD AX, OFFSET DGROUP:_actors ; native 78DD
    PUSH AX ; native 78E0
    CALL NEAR PTR _detach_actor ; native 78E1
    ADD SP, 02h ; native 78E4
    MOV BL, byte ptr [BP-0Ah] ; native 78E7
    SUB BH, BH ; native 78EA
    MOV byte ptr _cells[BX], BH ; native 78EC
code_78f0:
    POP SI ; native 78F0
    POP DI ; native 78F1
    MOV SP, BP ; native 78F2
    POP BP ; native 78F4
    RET ; native 78F5
_undo_animation ENDP

; Finalize WORD alignment after three genuine C PROCs and authored undo PROC.
	EVEN
_TEXT	ENDS
END
