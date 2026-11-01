; Complete assembly reconstruction; no C credit for this PROC.
; Symbolic binding scaffold from fresh compiler listing; native stack from REA
; ev_7758eba41fb96e2b6e32b4c70eab530f9b1a4f14602977a63525a47a26926417
_commit_turn_810c	PROC NEAR
	push	bp
	mov	bp,sp
	sub	sp,4
	push	di
	push	si
	mov	di,OFFSET _history_tail
	mov	si,OFFSET _working_move
	push	ds
	pop	es
	movsw
	movsw
	movsw
	movsw
	mov	di,OFFSET _hint_line
	mov	si,OFFSET _initial_move
	movsw
	movsw
	movsw
	movsw
	mov	di,OFFSET _history_tail+8
	mov	si,OFFSET _initial_move
	movsw
	movsw
	movsw
	movsw
	cmp	BYTE PTR _history_tail+6,0
	jne	$I341
	mov	di,OFFSET _hint_line
	mov	si,OFFSET _initial_move
	movsw
	movsw
	movsw
	movsw
	mov	ax,WORD PTR _modes+2
	cmp	WORD PTR _modes,ax
	jne	$L20004
	mov	ax,1
	jmp	SHORT $L20005
$L20004:
	sub	ax,ax
$L20005:
	cmp	ax,1
	jne	$I342
	call	_no_move
	mov	WORD PTR _setup_word_934a,0
	jmp	$EX339
$I342:
	cmp	BYTE PTR _history+6,0
	je	$JCC1305
	jmp	$I344
$JCC1305:
	call	_setup_state
	mov	WORD PTR _state_57cc,0
	jmp	$EX339
$I341:
	mov	bx,_history_index
	mov	cl,3
	shl	bx,cl
	push	WORD PTR _history_tail[bx+14]
	push	WORD PTR _history_tail[bx+12]
	push	WORD PTR _history_tail[bx+10]
	push	WORD PTR _history_tail[bx+8]
	call	_notify_wrapper_861b
	add	sp,8
	call	_shift_state
	mov	ax,WORD PTR _modes+2
	cmp	WORD PTR _modes,ax
	jne	$L20006
	mov	ax,1
	jmp	SHORT $L20007
$L20006:
	sub	ax,ax
$L20007:
	cmp	ax,1
	je	$JCC1374
	jmp	$I345
$JCC1374:
	cmp	WORD PTR _history_move_counter,120
	jge	$I347
	call	_count_9bfd
	cmp	ax,100
	jge	$I347
	sub	ax,ax
	push	ax
	call	_repetition_9c34
	add	sp,2
	cmp	ax,3
	jge	$I347
	cmp	WORD PTR _best,-2176
	jg	$I346
$I347:
	cmp	WORD PTR _current_side,0
	jne	$I348
	sub	ax,ax
	push	ax
	mov	ax,12
	push	ax
	mov	ax,OFFSET DGROUP:$SG349
	push	ax
	call	_prompt_1296
	add	sp,6
	call	_reset_df71
	mov	ax,13
	push	ax
	mov	ax,OFFSET DGROUP:$SG350
	jmp	SHORT $L20014
$I348:
	sub	ax,ax
	push	ax
	mov	ax,12
	push	ax
	mov	ax,OFFSET DGROUP:$SG352
	push	ax
	call	_prompt_1296
	add	sp,6
	call	_reset_df71
	mov	ax,12
	push	ax
	mov	ax,OFFSET DGROUP:$SG353
$L20014:
	push	ax
	call	_write_bytes_dbb5
	add	sp,4
	call	_refresh_1446
	call	_setup_state
	jmp	SHORT $EX339
$I346:
	mov	WORD PTR _setup_word_934a,0
	call	_promote_ui_9371
	or	ax,ax
	je	$I354
	call	_finish_move_93d6
	jmp	SHORT $EX339
$I354:
	sub	ax,ax
	push	ax
	push	WORD PTR _history_tail+6
	push	WORD PTR _history_tail+4
	push	WORD PTR _history_tail+2
	push	WORD PTR _history_tail
	call	_animation_stage
	add	sp,10
	mov	WORD PTR [bp-4],ax
	or	ax,ax
	je	$EX339
	mov	_ready_9856,ax
	jmp	SHORT $EX339
$I345:
	mov	WORD PTR _setup_word_934a,2
	call	_promote_ui_9371
	or	ax,ax
	je	$I357
	call	_finish_move_93d6
	jmp	SHORT $I359
$I357:
	sub	ax,ax
	push	ax
	push	WORD PTR _history_tail+6
	push	WORD PTR _history_tail+4
	push	WORD PTR _history_tail+2
	push	WORD PTR _history_tail
	call	_animation_stage
	add	sp,10
	mov	WORD PTR [bp-4],ax
	or	ax,ax
	je	$I359
	mov	_ready_9856,ax
$I359:
	call	_search_state_8fca
	or	ax,ax
	jne	$EX339
$I344:
	call	_no_move
$EX339:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_commit_turn_810c	ENDP
