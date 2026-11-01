_pawn_bit_count	PROC FAR
	push	bp
	mov	bp,sp
	sub	sp,4
	mov	WORD PTR [bp-4],0
$FC387:
	cmp	WORD PTR [bp+6],0
	je	$FB388
	push	WORD PTR [bp+6]
	push	cs
	call	_evaluation_parity
	add	sp,2
	or	ax,ax
	je	$I389
	inc	WORD PTR [bp-4]
$I389:
	sar	WORD PTR [bp+6],1
	jmp	SHORT $FC387
$FB388:
	mov	ax,WORD PTR [bp-4]
	jmp	SHORT $EX384
$EX384:
	mov	sp,bp
	pop	bp
	ret
_pawn_bit_count	ENDP
