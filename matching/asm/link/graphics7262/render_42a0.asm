; Explicit authored assembly for _render_42a0; native 0x42a0..0x4575.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_render_42a0 PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,46
	call	__chkstk
	push	di
	push	si
	mov	ax,_region_left
	sar	ax,1
	sar	ax,1
	mov	WORD PTR [bp-8],ax
	mov	si,_actors_head
	jmp	SHORT g_render_42a0_F279
g_render_42a0_FC280:
	mov	si,WORD PTR [si+26]
g_render_42a0_F279:
	or	si,si
	jne	g_render_42a0_JCC1938
	jmp	g_render_42a0_FB281
g_render_42a0_JCC1938:
	mov	ax,_region_right
	cmp	WORD PTR [si+12],ax
	jle	g_render_42a0_JCC1949
	jmp	g_render_42a0_I282
g_render_42a0_JCC1949:
	mov	ax,_region_left
	cmp	WORD PTR [si+14],ax
	jge	g_render_42a0_JCC1960
	jmp	g_render_42a0_I282
g_render_42a0_JCC1960:
	mov	ax,_dirty_bottom
	cmp	WORD PTR [si+16],ax
	jle	g_render_42a0_JCC1971
	jmp	g_render_42a0_I282
g_render_42a0_JCC1971:
	mov	ax,_dirty_top
	cmp	WORD PTR [si+18],ax
	jge	g_render_42a0_JCC1982
	jmp	g_render_42a0_I282
g_render_42a0_JCC1982:
	cmp	WORD PTR _active_actor,0
	je	g_render_42a0_I283
	cmp	_active_actor,si
	je	g_render_42a0_JCC1998
	jmp	g_render_42a0_I282
g_render_42a0_JCC1998:
g_render_42a0_I283:
	cmp	BYTE PTR [si+10],0
	je	g_render_42a0_I284
	push	WORD PTR [si+20]
	call	_prepare_color_4575
	add	sp,2
g_render_42a0_I284:
	mov	ax,WORD PTR [si+12]
	sub	ax,_region_left
	mov	WORD PTR [bp-24],ax
	or	ax,ax
	jge	g_render_42a0_I285
	neg	ax
	mov	di,ax
	mov	WORD PTR [bp-24],0
	mov	bx,di
	and	bx,WORD PTR 3
	shl	bx,1
	mov	ax,WORD PTR _left_masks[bx]
	mov	WORD PTR [bp-30],ax
	jmp	SHORT g_render_42a0_I286
g_render_42a0_I285:
	sub	di,di
	mov	WORD PTR [bp-30],-1
g_render_42a0_I286:
	mov	ax,_region_right
	sub	ax,WORD PTR [si+14]
	mov	WORD PTR [bp-38],ax
	or	ax,ax
	jge	g_render_42a0_I287
	neg	ax
	mov	WORD PTR [bp-36],ax
	mov	WORD PTR [bp-38],0
	mov	bx,ax
	and	bx,WORD PTR 3
	shl	bx,1
	mov	ax,WORD PTR _right_masks[bx]
	mov	WORD PTR [bp-40],ax
	jmp	SHORT g_render_42a0_I288
g_render_42a0_I287:
	mov	WORD PTR [bp-36],0
	test	BYTE PTR [bp-38],3
	je	g_render_42a0_L20012
	sub	ax,ax
	jmp	SHORT g_render_42a0_L20013
g_render_42a0_L20012:
	mov	ax,-1
g_render_42a0_L20013:
	mov	WORD PTR [bp-40],ax
g_render_42a0_I288:
	mov	bx,WORD PTR [si+20]
	mov	al,BYTE PTR [bx]
	sub	ah,ah
	add	ax,3
	and	ax,252
	sub	ax,WORD PTR [bp-36]
	sub	ax,di
	mov	WORD PTR [bp-6],ax
	add	ax,3
	sar	ax,1
	and	al,254
	mov	WORD PTR [bp-4],ax
	test	BYTE PTR [si+12],3
	je	g_render_42a0_I292
	cmp	WORD PTR [bp-36],0
	jne	g_render_42a0_I290
	add	WORD PTR [bp-4],2
	jmp	SHORT g_render_42a0_I292
g_render_42a0_I290:
	or	di,di
	je	g_render_42a0_I292
	add	WORD PTR [bp-4],2
g_render_42a0_I292:
	mov	ax,WORD PTR [si+16]
	sub	ax,_dirty_top
	mov	WORD PTR [bp-2],ax
	or	ax,ax
	jge	g_render_42a0_I293
	neg	ax
	mov	WORD PTR [bp-44],ax
	mov	WORD PTR [bp-2],0
	mov	ax,_dirty_bottom
	cmp	WORD PTR [si+18],ax
	jle	g_render_42a0_L20014
	sub	ax,_dirty_top
	inc	ax
	jmp	SHORT g_render_42a0_L20015
g_render_42a0_L20014:
	mov	ax,WORD PTR [si+18]
	sub	ax,_dirty_top
	inc	ax
g_render_42a0_L20015:
	mov	WORD PTR [bp-34],ax
	jmp	SHORT g_render_42a0_I294
g_render_42a0_I293:
	mov	WORD PTR [bp-44],0
	mov	ax,_dirty_bottom
	cmp	WORD PTR [si+18],ax
	jle	g_render_42a0_L20016
	sub	ax,WORD PTR [si+16]
	inc	ax
	jmp	SHORT g_render_42a0_L20017
g_render_42a0_L20016:
	mov	ax,WORD PTR [si+18]
	sub	ax,WORD PTR [si+16]
	inc	ax
g_render_42a0_L20017:
	mov	WORD PTR [bp-34],ax
g_render_42a0_I294:
	mov	bx,WORD PTR [si+20]
	mov	al,BYTE PTR [bx]
	sub	ah,ah
	add	ax,3
	shr	ax,1
	and	ax,254
	mov	WORD PTR [bp-46],ax
	mov	ax,WORD PTR [bp-34]
	dec	ax
	add	ax,WORD PTR [bp-44]
	mul	WORD PTR [bp-46]
	mov	cx,di
	sar	cx,1
	and	cl,254
	add	ax,cx
	mov	WORD PTR [bp-28],ax
	mov	ax,WORD PTR [bp-34]
	add	ax,WORD PTR [bp-2]
	dec	ax
	imul	WORD PTR _stride
	mov	cx,WORD PTR [bp-24]
	sar	cx,1
	and	cl,254
	add	ax,cx
	mov	WORD PTR [bp-32],ax
	test	di,3
	je	g_render_42a0_I295
	sub	WORD PTR [bp-32],2
g_render_42a0_I295:
	mov	bx,WORD PTR [si+20]
	mov	al,BYTE PTR [bx+1]
	sub	ah,ah
	mov	cx,ax
	mov	al,BYTE PTR [bx]
	add	ax,3
	shr	ax,1
	and	ax,254
	mul	cx
	mov	WORD PTR [bp-10],ax
	mov	ax,_stride
	imul	WORD PTR _height
	mov	WORD PTR [bp-14],ax
	mov	ax,WORD PTR [bp-30]
	mov	WORD PTR _blit+12,ax
	mov	ax,WORD PTR [bp-40]
	mov	WORD PTR _blit+14,ax
	mov	bx,WORD PTR [si+20]
	mov	al,BYTE PTR [bx]
	sub	ah,ah
	add	ax,3
	shr	ax,1
	and	ax,254
	add	ax,WORD PTR [bp-4]
	neg	ax
	mov	WORD PTR _blit+8,ax
	mov	ax,WORD PTR [bp-4]
	add	ax,_stride
	neg	ax
	mov	WORD PTR _blit+10,ax
	cmp	BYTE PTR [si+10],0
	je	g_render_42a0_I296
	mov	bx,WORD PTR [bp-28]
	ASSUME DS:NOTHING
	lea	ax,WORD PTR _color_buffer[bx]
	ASSUME DS:DGROUP
	mov	dx,SEG _color_buffer
	mov	WORD PTR _blit+20,ax
	mov	WORD PTR _blit+22,dx
	jmp	SHORT g_render_42a0_I297
g_render_42a0_I296:
	mov	ax,WORD PTR [bp-28]
	cwd
	mov	bx,WORD PTR [si+20]
	add	ax,WORD PTR [bx+4]
	adc	dx,0
	mov	cx,OFFSET __AHSHIFT
	shl	dx,cl
	add	dx,WORD PTR [bx+6]
	mov	WORD PTR _blit+20,ax
	mov	WORD PTR _blit+22,dx
g_render_42a0_I297:
	mov	ax,WORD PTR [bp-32]
	cwd
	add	ax,OFFSET _region_buffer
	adc	dx,0
	mov	cx,OFFSET __AHSHIFT
	shl	dx,cl
	add	dx,SEG _region_buffer
	mov	WORD PTR _blit+16,ax
	mov	WORD PTR _blit+18,dx
	mov	ax,WORD PTR [bp-34]
	mov	WORD PTR _blit+6,ax
	mov	ax,WORD PTR [bp-4]
	sar	ax,1
	mov	WORD PTR _blit+4,ax
	mov	ax,WORD PTR [si+12]
	and	ax,3
	mov	WORD PTR _blit,ax
	mov	WORD PTR _blit+2,1
	call	_blit_e57a
g_render_42a0_I282:
	jmp	g_render_42a0_FC280
g_render_42a0_FB281:
	mov	WORD PTR _active_actor,0
	cmp	BYTE PTR _page_mode,0
	jne	g_render_42a0_I298
	call	FAR PTR _graphics_begin
	mov	ax,OFFSET _region_buffer
	mov	dx,SEG _region_buffer
	push	dx
	push	ax
	push	WORD PTR _height
	push	WORD PTR _stride
	push	WORD PTR _dirty_top
	mov	ax,WORD PTR [bp-8]
	shl	ax,1
	push	ax
	call	FAR PTR _graphics_copy
	add	sp,12
	call	FAR PTR _graphics_end
	jmp	SHORT g_render_42a0_I299
g_render_42a0_I298:
	mov	ax,OFFSET _region_buffer
	mov	dx,SEG _region_buffer
	push	dx
	push	ax
	push	WORD PTR _height
	push	WORD PTR _stride
	push	WORD PTR _dirty_top
	mov	ax,WORD PTR [bp-8]
	shl	ax,1
	push	ax
	call	_copy_5cb5
	add	sp,12
g_render_42a0_I299:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_render_42a0 ENDP
