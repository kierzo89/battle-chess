; Explicit authored assembly for _outline_square_543a; native 0x543a..0x578c.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_outline_square_543a PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,36
	call	__chkstk
	push	di
	push	si
	cmp	WORD PTR [bp+4],63
	jbe	g_outline_square_543a_JCC6427
	jmp	g_outline_square_543a_I523
g_outline_square_543a_JCC6427:
	mov	ax,WORD PTR [bp+4]
	mov	cl,3
	shr	ax,cl
	mov	WORD PTR [bp-18],ax
	mov	ax,WORD PTR [bp+4]
	and	ax,7
	mov	WORD PTR [bp-26],ax
	mov	ax,18
	imul	WORD PTR [bp-18]
	mov	si,ax
	add	si,_square_x
	mov	ax,WORD PTR [bp-26]
	shl	ax,1
	mov	WORD PTR [bp-34],ax
	mov	bx,ax
	mov	di,[bx][si]
	dec	di
	mov	ax,[bx+2][si]
	mov	WORD PTR [bp-22],ax
	add	si,18
	mov	ax,[bx][si]
	dec	ax
	mov	WORD PTR [bp-30],ax
	mov	ax,[bx+2][si]
	mov	WORD PTR [bp-32],ax
	mov	ax,WORD PTR [bp-18]
	shl	ax,1
	add	ax,_square_y
	mov	WORD PTR [bp-36],ax
	mov	bx,ax
	mov	ax,WORD PTR [bx]
	mov	WORD PTR [bp-20],ax
	mov	ax,WORD PTR [bx+2]
	inc	ax
	mov	WORD PTR [bp-28],ax
	mov	ax,WORD PTR [bp-30]
	cmp	ax,di
	jle	g_outline_square_543a_L20038
	mov	ax,di
g_outline_square_543a_L20038:
	sar	ax,1
	sar	ax,1
	mov	_dirty_left,ax
	mov	ax,WORD PTR [bp-22]
	cmp	ax,WORD PTR [bp-32]
	jge	g_outline_square_543a_L20039
	mov	ax,WORD PTR [bp-32]
g_outline_square_543a_L20039:
	sar	ax,1
	sar	ax,1
	mov	_dirty_right,ax
	mov	ax,WORD PTR [bp-20]
	mov	_dirty_top,ax
	mov	ax,WORD PTR [bp-28]
	mov	_dirty_bottom,ax
	cmp	WORD PTR _dirty_left,0
	jge	g_outline_square_543a_I524
	mov	WORD PTR _dirty_left,0
g_outline_square_543a_I524:
	cmp	WORD PTR _dirty_right,79
	jle	g_outline_square_543a_I525
	mov	WORD PTR _dirty_right,79
g_outline_square_543a_I525:
	cmp	WORD PTR _dirty_top,0
	jge	g_outline_square_543a_I526
	mov	WORD PTR _dirty_top,0
g_outline_square_543a_I526:
	cmp	WORD PTR _dirty_bottom,199
	jle	g_outline_square_543a_I527
	mov	WORD PTR _dirty_bottom,199
g_outline_square_543a_I527:
	sub	ax,ax
	push	ax
	call	_mark_region_41a8
	add	sp,2
	cmp	WORD PTR [bp+6],0
	jne	g_outline_square_543a_JCC6635
	jmp	g_outline_square_543a_I536
g_outline_square_543a_JCC6635:
	push	WORD PTR [bp+6]
	call	_select_pen_5b18
	add	sp,2
	sub	di,_region_left
	mov	ax,_region_left
	sub	WORD PTR [bp-22],ax
	sub	WORD PTR [bp-30],ax
	sub	WORD PTR [bp-32],ax
	sub	ax,ax
	push	ax
	push	di
	call	_move_pen_5b3d
	add	sp,4
	sub	ax,ax
	push	ax
	push	WORD PTR [bp-22]
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	push	WORD PTR [bp-32]
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	push	WORD PTR [bp-30]
	call	_line_pen_5b55
	add	sp,4
	sub	ax,ax
	push	ax
	push	di
	call	_line_pen_5b55
	add	sp,4
	mov	ax,1
	push	ax
	lea	ax,WORD PTR [di+1]
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,1
	push	ax
	mov	ax,WORD PTR [bp-22]
	dec	ax
	push	ax
	call	_line_pen_5b55
	add	sp,4
	sub	ax,ax
	push	ax
	mov	ax,WORD PTR [bp-22]
	dec	ax
	push	ax
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	mov	ax,WORD PTR [bp-32]
	dec	ax
	push	ax
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	dec	ax
	push	ax
	mov	ax,WORD PTR [bp-32]
	dec	ax
	push	ax
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	dec	ax
	push	ax
	mov	ax,WORD PTR [bp-30]
	inc	ax
	push	ax
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	mov	ax,WORD PTR [bp-30]
	inc	ax
	push	ax
	call	_line_pen_5b55
	add	sp,4
	sub	ax,ax
	push	ax
	lea	ax,WORD PTR [di+1]
	push	ax
	call	_line_pen_5b55
	add	sp,4
	cmp	WORD PTR [bp+6],0
	jne	g_outline_square_543a_JCC6863
	jmp	g_outline_square_543a_I536
g_outline_square_543a_JCC6863:
	cmp	WORD PTR [bp+6],28
	jb	g_outline_square_543a_JCC6872
	jmp	g_outline_square_543a_I536
g_outline_square_543a_JCC6872:
	cmp	WORD PTR _cursor_square_0efc,255
	jne	g_outline_square_543a_JCC6883
	jmp	g_outline_square_543a_I536
g_outline_square_543a_JCC6883:
	mov	ax,28
	push	ax
	call	_select_pen_5b18
	add	sp,2
	mov	ax,WORD PTR [bp+4]
	shl	ax,1
	and	ax,112
	mov	cx,WORD PTR [bp+4]
	and	cx,WORD PTR 7
	or	ax,cx
	mov	WORD PTR [bp+4],ax
	mov	ax,_cursor_square_0efc
	shl	ax,1
	and	ax,112
	mov	cx,_cursor_square_0efc
	and	cx,WORD PTR 7
	or	ax,cx
	mov	WORD PTR [bp-12],ax
	mov	ax,WORD PTR [bp+4]
	dec	ax
	cmp	ax,WORD PTR [bp-12]
	je	g_outline_square_543a_I531
	mov	ax,WORD PTR [bp+4]
	sub	ax,17
	cmp	ax,WORD PTR [bp-12]
	jne	g_outline_square_543a_I530
g_outline_square_543a_I531:
	sub	ax,ax
	push	ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	sub	ax,ax
	push	ax
	push	di
	call	_line_pen_5b55
	add	sp,4
	mov	ax,1
	push	ax
	sub	ax,ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,1
	push	ax
	push	di
	call	_line_pen_5b55
	add	sp,4
g_outline_square_543a_I530:
	mov	ax,WORD PTR [bp+4]
	dec	ax
	cmp	ax,WORD PTR [bp-12]
	je	g_outline_square_543a_I533
	mov	ax,WORD PTR [bp+4]
	add	ax,15
	cmp	ax,WORD PTR [bp-12]
	jne	g_outline_square_543a_I532
g_outline_square_543a_I533:
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	dec	ax
	push	ax
	sub	ax,ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	dec	ax
	push	ax
	push	WORD PTR [bp-30]
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	sub	ax,ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	push	WORD PTR [bp-30]
	call	_line_pen_5b55
	add	sp,4
g_outline_square_543a_I532:
	mov	ax,WORD PTR [bp+4]
	inc	ax
	cmp	ax,WORD PTR [bp-12]
	je	g_outline_square_543a_I535
	mov	ax,WORD PTR [bp+4]
	sub	ax,15
	cmp	ax,WORD PTR [bp-12]
	jne	g_outline_square_543a_I534
g_outline_square_543a_I535:
	sub	ax,ax
	push	ax
	mov	ax,_region_width
	dec	ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	sub	ax,ax
	push	ax
	push	WORD PTR [bp-22]
	call	_line_pen_5b55
	add	sp,4
	mov	ax,1
	push	ax
	mov	ax,_region_width
	dec	ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,1
	push	ax
	push	WORD PTR [bp-22]
	call	_line_pen_5b55
	add	sp,4
g_outline_square_543a_I534:
	mov	ax,WORD PTR [bp+4]
	inc	ax
	cmp	ax,WORD PTR [bp-12]
	je	g_outline_square_543a_I537
	mov	ax,WORD PTR [bp+4]
	add	ax,17
	cmp	ax,WORD PTR [bp-12]
	jne	g_outline_square_543a_I536
g_outline_square_543a_I537:
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	dec	ax
	push	ax
	mov	ax,_region_width
	dec	ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	dec	ax
	push	ax
	push	WORD PTR [bp-32]
	call	_line_pen_5b55
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	mov	ax,_region_width
	dec	ax
	push	ax
	call	_move_pen_5b3d
	add	sp,4
	mov	ax,WORD PTR [bp-28]
	sub	ax,WORD PTR [bp-20]
	push	ax
	push	WORD PTR [bp-32]
	call	_line_pen_5b55
	add	sp,4
g_outline_square_543a_I536:
	call	_render_42a0
g_outline_square_543a_I523:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_outline_square_543a ENDP
