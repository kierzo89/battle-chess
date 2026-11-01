; Explicit authored assembly for _mark_region_41a8; native 0x41a8..0x42a0.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_mark_region_41a8 PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,6
	call	__chkstk
	push	si
	mov	si,WORD PTR [bp+4]
	mov	ax,_dirty_left
	shl	ax,1
	shl	ax,1
	mov	_region_left,ax
	mov	ax,_dirty_right
	shl	ax,1
	shl	ax,1
	add	ax,3
	mov	_region_right,ax
	sub	ax,_region_left
	inc	ax
	mov	_region_width,ax
	mov	ax,_dirty_right
	sub	ax,_dirty_left
	shl	ax,1
	add	ax,2
	mov	_stride,ax
	mov	ax,_dirty_bottom
	sub	ax,_dirty_top
	inc	ax
	mov	_height,ax
	mov	ax,_stride
	imul	WORD PTR _height
	cmp	ax,3248
	jle	g_mark_region_41a8_I251
	mov	ax,OFFSET _overflow_message
	push	ax
	call	_error_message
	add	sp,2
	jmp	g_mark_region_41a8_I253
g_mark_region_41a8_I251:
	mov	ax,160
	imul	WORD PTR _dirty_top
	mov	cx,_dirty_left
	shl	cx,1
	add	ax,cx
	cwd
	add	ax,WORD PTR _screen
	adc	dx,0
	mov	cx,OFFSET __AHSHIFT
	shl	dx,cl
	add	dx,WORD PTR _screen+2
	mov	WORD PTR [bp-4],ax
	mov	WORD PTR [bp-2],dx
	mov	WORD PTR _blit+12,-1
	mov	WORD PTR _blit+14,-1
	mov	ax,160
	sub	ax,_stride
	mov	WORD PTR _blit+8,ax
	mov	WORD PTR _blit+10,0
	mov	ax,WORD PTR [bp-4]
	mov	WORD PTR _blit+20,ax
	mov	WORD PTR _blit+22,dx
	mov	WORD PTR _blit+16,OFFSET _region_buffer
	mov	WORD PTR _blit+18,SEG _region_buffer
	mov	ax,_height
	mov	WORD PTR _blit+6,ax
	mov	ax,_stride
	sar	ax,1
	mov	WORD PTR _blit+4,ax
	mov	WORD PTR _blit,0
	mov	WORD PTR _blit+2,0
	or	si,si
	jne	g_mark_region_41a8_I252
	call	_blit_e57a
	jmp	SHORT g_mark_region_41a8_I253
g_mark_region_41a8_I252:
	sub	ax,ax
	push	ax
	mov	ax,_height
	imul	WORD PTR _stride
	push	ax
	mov	ax,OFFSET _region_buffer
	mov	dx,SEG _region_buffer
	push	dx
	push	ax
	call	_fill_5a4f
	add	sp,8
g_mark_region_41a8_I253:
	pop	si
	mov	sp,bp
	pop	bp
	ret
_mark_region_41a8 ENDP
