; Explicit authored assembly for _draw_actor; native 0x3f9e..0x41a8.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_draw_actor PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,6
	call	__chkstk
	push	di
	push	si
	mov	si,WORD PTR [bp+4]
	mov	di,WORD PTR [bp+6]
g_draw_actor_FC224:
	cmp	di,200
	jl	g_draw_actor_FB225
	sub	di,200
	jmp	SHORT g_draw_actor_FC224
g_draw_actor_FB225:
	mov	bx,WORD PTR [bp+10]
	mov	al,BYTE PTR [bx+2]
	cbw
	sub	ax,si
	neg	ax
	sar	ax,1
	sar	ax,1
	mov	_dirty_left,ax
	mov	al,BYTE PTR [bx+2]
	cbw
	mov	cl,BYTE PTR [bx]
	sub	ch,ch
	add	cx,3
	and	cx,252
	sub	cx,ax
	add	cx,si
	dec	cx
	shr	cx,1
	shr	cx,1
	mov	_dirty_right,cx
	mov	al,BYTE PTR [bx+3]
	cbw
	sub	ax,di
	neg	ax
	mov	_dirty_top,ax
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	cl,BYTE PTR [bx+1]
	sub	ch,ch
	sub	ax,cx
	neg	ax
	add	ax,di
	dec	ax
	mov	_dirty_bottom,ax
	mov	al,BYTE PTR [bx+2]
	cbw
	sub	ax,si
	neg	ax
	mov	bx,WORD PTR [bp+12]
	mov	WORD PTR [bx+12],ax
	mov	bx,WORD PTR [bp+10]
	mov	al,BYTE PTR [bx]
	sub	ah,ah
	add	ax,3
	and	ax,252
	mov	bx,WORD PTR [bp+12]
	add	ax,WORD PTR [bx+12]
	dec	ax
	mov	WORD PTR [bx+14],ax
	mov	bx,WORD PTR [bp+12]
	mov	ax,_dirty_top
	mov	WORD PTR [bx+16],ax
	mov	bx,WORD PTR [bp+12]
	mov	ax,_dirty_bottom
	mov	WORD PTR [bx+18],ax
	mov	bx,WORD PTR [bp+12]
	mov	ax,WORD PTR [bx+20]
	mov	WORD PTR [bp-4],ax
	or	ax,ax
	jne	g_draw_actor_JCC1307
	jmp	g_draw_actor_I226
g_draw_actor_JCC1307:
	cmp	WORD PTR [bx+8],0
	je	g_draw_actor_I227
	push	WORD PTR [bx+20]
	call	_push_value
	add	sp,2
g_draw_actor_I227:
	mov	bx,WORD PTR [bp-4]
	mov	al,BYTE PTR [bx+2]
	cbw
	mov	bx,WORD PTR [bp+12]
	mov	cx,WORD PTR [bx]
	sub	cx,ax
	sar	cx,1
	sar	cx,1
	mov	WORD PTR [bp-6],cx
	mov	ax,_dirty_left
	cmp	cx,ax
	jge	g_draw_actor_I228
	mov	ax,cx
	mov	_dirty_left,ax
g_draw_actor_I228:
	mov	bx,WORD PTR [bp-4]
	mov	al,BYTE PTR [bx+2]
	cbw
	mov	cl,BYTE PTR [bx]
	sub	ch,ch
	add	cx,3
	and	cx,252
	sub	cx,ax
	mov	bx,WORD PTR [bp+12]
	add	cx,WORD PTR [bx]
	dec	cx
	shr	cx,1
	shr	cx,1
	mov	WORD PTR [bp-6],cx
	mov	ax,_dirty_right
	cmp	cx,ax
	jle	g_draw_actor_I229
	mov	ax,cx
	mov	_dirty_right,ax
g_draw_actor_I229:
	mov	bx,WORD PTR [bp-4]
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	bx,WORD PTR [bp+12]
	mov	cx,WORD PTR [bx+2]
	sub	cx,ax
	mov	WORD PTR [bp-6],cx
	mov	ax,_dirty_top
	cmp	cx,ax
	jge	g_draw_actor_I230
	mov	ax,cx
	mov	_dirty_top,ax
g_draw_actor_I230:
	mov	bx,WORD PTR [bp-4]
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	bx,WORD PTR [bp+12]
	mov	cx,WORD PTR [bx+2]
	sub	cx,ax
	mov	bx,WORD PTR [bp-4]
	mov	al,BYTE PTR [bx+1]
	sub	ah,ah
	add	cx,ax
	dec	cx
	mov	WORD PTR [bp-6],cx
	mov	ax,_dirty_bottom
	cmp	cx,ax
	jle	g_draw_actor_I231
	mov	ax,cx
	mov	_dirty_bottom,ax
g_draw_actor_I231:
	jmp	SHORT g_draw_actor_I232
g_draw_actor_I226:
	mov	bx,WORD PTR [bp+12]
	mov	WORD PTR [bx+8],0
g_draw_actor_I232:
	cmp	WORD PTR _dirty_left,0
	jge	g_draw_actor_I233
	mov	WORD PTR _dirty_left,0
g_draw_actor_I233:
	cmp	WORD PTR _dirty_right,79
	jle	g_draw_actor_I234
	mov	WORD PTR _dirty_right,79
g_draw_actor_I234:
	cmp	WORD PTR _dirty_top,0
	jge	g_draw_actor_I235
	mov	WORD PTR _dirty_top,0
g_draw_actor_I235:
	cmp	WORD PTR _dirty_bottom,199
	jle	g_draw_actor_I236
	mov	WORD PTR _dirty_bottom,199
g_draw_actor_I236:
	mov	bx,WORD PTR [bp+12]
	mov	WORD PTR [bx],si
	mov	bx,WORD PTR [bp+12]
	mov	WORD PTR [bx+2],di
	mov	bx,WORD PTR [bp+12]
	mov	WORD PTR [bx+4],si
	mov	bx,WORD PTR [bp+12]
	mov	WORD PTR [bx+6],di
	mov	bx,WORD PTR [bp+12]
	cmp	WORD PTR [bp+8],1
	sbb	ax,ax
	inc	ax
	mov	BYTE PTR [bx+10],al
	mov	bx,WORD PTR [bp+12]
	mov	ax,WORD PTR [bp+10]
	mov	WORD PTR [bx+20],ax
	cmp	WORD PTR _dirty_right,0
	jl	g_draw_actor_I237
	cmp	WORD PTR _dirty_left,79
	jg	g_draw_actor_I237
	cmp	WORD PTR _dirty_top,199
	jg	g_draw_actor_I237
	cmp	WORD PTR _dirty_bottom,0
	jl	g_draw_actor_I237
	mov	bx,WORD PTR [bp+12]
	cmp	BYTE PTR [bx+11],254
	jne	g_draw_actor_I238
	mov	ax,1
	push	ax
	call	_mark_region_41a8
	add	sp,2
	mov	ax,WORD PTR [bp+12]
	mov	_active_actor,ax
	jmp	SHORT g_draw_actor_I239
g_draw_actor_I238:
	sub	ax,ax
	push	ax
	call	_mark_region_41a8
	add	sp,2
g_draw_actor_I239:
	call	_render_42a0
g_draw_actor_I237:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_draw_actor ENDP
