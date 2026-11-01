_evaluate_candidate	PROC FAR
	push	bp
	mov	bp,sp
	sub	sp,10
	push	di
	push	si
	mov	WORD PTR [bp-2],6
	mov	WORD PTR _evaluation_delta,0
	cmp	WORD PTR [bp+10],0
	jne	$JCC3386
	jmp	$I426
$JCC3386:
	cmp	BYTE PTR [bp+12],1
	jne	$I421
	lea	ax,WORD PTR [bp-6]
	push	ax
	lea	ax,WORD PTR [bp-8]
	push	ax
	push	WORD PTR [bp+6]
	call	FAR PTR _castle_95df
	add	sp,6
	push	WORD PTR [bp-6]
	push	WORD PTR _current_side
	mov	ax,3
	push	ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	push	WORD PTR [bp-8]
	push	WORD PTR _current_side
	mov	cx,3
	push	cx
	mov	si,ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	sub	ax,si
	mov	_evaluation_delta,ax
	mov	ax,WORD PTR [bp+8]
	cmp	WORD PTR [bp+6],ax
	jle	$I422
	mov	ax,WORD PTR _castle_bonus+2
	add	_evaluation_delta,ax
	jmp	SHORT $I423
$I422:
	mov	ax,WORD PTR _castle_bonus
	add	_evaluation_delta,ax
$I423:
	jmp	SHORT $I426
$I421:
	cmp	BYTE PTR [bp+12],6
	jne	$I425
	mov	ax,WORD PTR [bp+6]
	mov	bx,_current_side
	shl	bx,1
	sub	ax,WORD PTR _move_lookup_tables[bx+32]
	mov	WORD PTR [bp-4],ax
	push	ax
	push	WORD PTR _opponent
	mov	ax,6
	push	ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	mov	_evaluation_delta,ax
	jmp	SHORT $I426
$I425:
	mov	ax,WORD PTR [bp+8]
	and	ax,WORD PTR 7
	push	ax
	push	WORD PTR _current_side
	push	cs
	call	_evaluation_pawn_remove
	add	sp,4
	push	WORD PTR [bp+8]
	push	WORD PTR _current_side
	mov	cx,6
	push	cx
	mov	si,ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	push	WORD PTR [bp+8]
	push	WORD PTR _current_side
	mov	cl,BYTE PTR [bp+12]
	sub	ch,ch
	push	cx
	mov	di,ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	sub	ax,di
	add	ax,si
	mov	_evaluation_delta,ax
$I426:
	cmp	BYTE PTR [bp+13],0
	je	$I428
	push	WORD PTR [bp+6]
	push	WORD PTR _opponent
	mov	al,BYTE PTR [bp+13]
	sub	ah,ah
	push	ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	add	_evaluation_delta,ax
	push	WORD PTR _best
	push	cs
	call	_evaluation_abs
	add	sp,2
	cmp	ax,256
	jl	$I428
	cmp	BYTE PTR [bp+13],6
	je	$I428
	cmp	WORD PTR _best,0
	jl	$L20036
	mov	ax,1
	jmp	SHORT $L20037
$L20036:
	sub	ax,ax
$L20037:
	mov	cx,_opponent
	mov	si,ax
	cmp	_temporary,cx
	jne	$L20034
	mov	ax,1
	jmp	SHORT $L20035
$L20034:
	sub	ax,ax
$L20035:
	cmp	ax,si
	jne	$I428
	sub	WORD PTR _evaluation_delta,16
$I428:
	mov	si,_history_index
	mov	cl,3
	shl	si,cl
	mov	ax,WORD PTR _pawn_state[si]
	mov	dx,WORD PTR _pawn_state[si+2]
	mov	WORD PTR _pawn_state[si+8],ax
	mov	WORD PTR _pawn_state[si+10],dx
	mov	ax,WORD PTR _pawn_state[si+4]
	mov	dx,WORD PTR _pawn_state[si+6]
	mov	WORD PTR _pawn_state[si+12],ax
	mov	WORD PTR _pawn_state[si+14],dx
	cmp	BYTE PTR [bp+12],6
	jne	$L20038
	mov	ax,1
	jmp	SHORT $L20039
$L20038:
	sub	ax,ax
$L20039:
	cmp	BYTE PTR [bp+13],1
	sbb	cx,cx
	inc	cx
	or	cx,WORD PTR [bp+10]
	test	cx,ax
	je	$I429
	mov	ax,WORD PTR [bp+8]
	and	ax,WORD PTR 7
	push	ax
	mov	ax,WORD PTR [bp+6]
	and	ax,WORD PTR 7
	push	ax
	push	WORD PTR _current_side
	push	cs
	call	_evaluation_pawn_move
	add	sp,6
	add	_evaluation_delta,ax
$I429:
	cmp	BYTE PTR [bp+13],6
	jne	$L20044
	mov	ax,1
	jmp	SHORT $L20045
$L20044:
	sub	ax,ax
$L20045:
	mov	si,ax
	cmp	BYTE PTR [bp+12],6
	jne	$L20042
	mov	ax,1
	jmp	SHORT $L20043
$L20042:
	sub	ax,ax
$L20043:
	and	ax,WORD PTR [bp+10]
	or	ax,si
	je	$I430
	mov	ax,WORD PTR [bp+6]
	and	ax,WORD PTR 7
	push	ax
	push	WORD PTR _opponent
	push	cs
	call	_evaluation_pawn_remove
	add	sp,4
	sub	_evaluation_delta,ax
$I430:
	push	WORD PTR [bp+8]
	push	WORD PTR _current_side
	mov	al,BYTE PTR [bp+12]
	sub	ah,ah
	push	ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	push	WORD PTR [bp+6]
	push	WORD PTR _current_side
	mov	cl,BYTE PTR [bp+12]
	sub	ch,ch
	push	cx
	mov	si,ax
	push	cs
	call	_evaluation_piece
	add	sp,6
	sub	ax,si
	add	ax,_evaluation_delta
	mov	WORD PTR [bp-2],ax
	jmp	SHORT $EX415
$EX415:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_evaluate_candidate	ENDP
