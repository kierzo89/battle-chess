; Explicit authored assembly for _build_menu_466b; native 0x466b..0x4c74.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_build_menu_466b PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,24
	call	__chkstk
	push	di
	push	si
	mov	si,WORD PTR [bp+4]
	call	FAR PTR _graphics_begin
	mov	BYTE PTR _menu_text+1,9
	mov	WORD PTR _menu_y,25
	mov	bx,si
	shl	bx,1
	shl	bx,1
	add	bx,_menus
	mov	ax,WORD PTR [bx+2]
	mov	WORD PTR [bp-10],ax
	mov	WORD PTR [bp-14],ax
	mov	bx,si
	shl	bx,1
	mov	ax,WORD PTR _menu_positions[bx]
	sub	ax,32
	mov	_menu_x,ax
	mov	WORD PTR _menu_columns,0
g_build_menu_466b_FC352:
	mov	bx,WORD PTR [bp-14]
	add	WORD PTR [bp-14],6
	mov	ax,WORD PTR [bx]
	mov	WORD PTR [bp-4],ax
	or	ax,ax
	je	g_build_menu_466b_FB353
	mov	WORD PTR [bp-22],0
g_build_menu_466b_FC355:
	mov	bx,WORD PTR [bp-4]
	inc	WORD PTR [bp-4]
	cmp	BYTE PTR [bx],0
	je	g_build_menu_466b_FB356
	inc	WORD PTR [bp-22]
	jmp	SHORT g_build_menu_466b_FC355
g_build_menu_466b_FB356:
	mov	ax,_menu_columns
	cmp	WORD PTR [bp-22],ax
	jle	g_build_menu_466b_I357
	mov	ax,WORD PTR [bp-22]
	mov	_menu_columns,ax
g_build_menu_466b_I357:
	jmp	SHORT g_build_menu_466b_FC352
g_build_menu_466b_FB353:
	mov	ax,_menu_columns
	sar	ax,1
	dec	ax
	mov	_menu_columns,ax
	mov	cl,4
	shl	ax,cl
	mov	WORD PTR [bp-24],ax
	add	ax,_menu_x
	cmp	ax,224
	jle	g_build_menu_466b_I358
	mov	ax,224
	sub	ax,WORD PTR [bp-24]
	mov	_menu_x,ax
g_build_menu_466b_I358:
	mov	ax,32
	push	ax
	mov	ax,15
	push	ax
	push	WORD PTR _menu_y
	push	WORD PTR _menu_x
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,33
	push	ax
	mov	ax,16
	push	ax
	push	WORD PTR _menu_y
	push	WORD PTR _menu_x
	call	_configure_actor_45a2
	add	sp,8
	sub	di,di
	jmp	SHORT g_build_menu_466b_F359
g_build_menu_466b_FC360:
	inc	di
g_build_menu_466b_F359:
	cmp	_menu_columns,di
	jle	g_build_menu_466b_FB361
	lea	ax,WORD PTR [di+34]
	push	ax
	mov	ax,4
	push	ax
	push	WORD PTR _menu_y
	mov	ax,di
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	jmp	SHORT g_build_menu_466b_FC360
g_build_menu_466b_FB361:
	cmp	WORD PTR _speed_2eb3,3000
	jle	g_build_menu_466b_JCC3128
	jmp	g_build_menu_466b_FB368
g_build_menu_466b_JCC3128:
	mov	ax,44
	push	ax
	mov	ax,8
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,32
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,45
	push	ax
	mov	ax,10
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,57
	push	ax
	mov	ax,7
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	sub	di,di
	jmp	SHORT g_build_menu_466b_F363
g_build_menu_466b_FC364:
	inc	di
g_build_menu_466b_F363:
	cmp	_menu_columns,di
	jle	g_build_menu_466b_FB365
	lea	ax,WORD PTR [di+46]
	push	ax
	mov	ax,9
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,di
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	jmp	SHORT g_build_menu_466b_FC364
g_build_menu_466b_FB365:
	mov	ax,56
	push	ax
	mov	ax,5
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	sub	di,di
	jmp	SHORT g_build_menu_466b_F366
g_build_menu_466b_FC367:
	inc	di
g_build_menu_466b_F366:
	cmp	_menu_columns,di
	jle	g_build_menu_466b_FB368
	lea	ax,WORD PTR [di+58]
	push	ax
	mov	ax,6
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,di
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	jmp	SHORT g_build_menu_466b_FC367
g_build_menu_466b_FB368:
	mov	ax,68
	push	ax
	sub	ax,ax
	push	ax
	push	WORD PTR _menu_y
	push	WORD PTR _menu_x
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,69
	push	ax
	mov	ax,2
	push	ax
	push	WORD PTR _menu_y
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,32
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,OFFSET _actors+1904
	push	ax
	mov	ax,OFFSET _frames
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,200
	push	ax
	push	WORD PTR _menu_x
	call	_attach_actor
	add	sp,10
	mov	ax,OFFSET _actors+1932
	push	ax
	mov	ax,OFFSET _frames+16
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,200
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,32
	push	ax
	call	_attach_actor
	add	sp,10
	mov	ax,OFFSET _actors+924
	push	ax
	mov	ax,OFFSET _frames+128
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,200
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,32
	push	ax
	call	_attach_actor
	add	sp,10
	cmp	WORD PTR _speed_2eb3,3000
	jg	g_build_menu_466b_I369
	mov	ax,OFFSET _actors+1596
	push	ax
	mov	ax,OFFSET _frames+56
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,223
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_attach_actor
	add	sp,10
	mov	ax,57
	push	ax
	mov	ax,7
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
g_build_menu_466b_I369:
	mov	ax,WORD PTR [bp-10]
	mov	WORD PTR [bp-14],ax
	mov	WORD PTR _menu_rows,0
	mov	WORD PTR [bp-22],0
g_build_menu_466b_FC371:
	mov	bx,WORD PTR [bp-14]
	mov	ax,WORD PTR [bx]
	mov	WORD PTR [bp-4],ax
	or	ax,ax
	jne	g_build_menu_466b_JCC3611
	jmp	g_build_menu_466b_FB372
g_build_menu_466b_JCC3611:
	call	_advance_menu_5381
	add	WORD PTR _menu_y,8
	inc	WORD PTR _menu_rows
	cmp	WORD PTR _speed_2eb3,3000
	jg	g_build_menu_466b_JCC3634
	jmp	g_build_menu_466b_I373
g_build_menu_466b_JCC3634:
	mov	ax,45
	push	ax
	mov	ax,10
	push	ax
	mov	ax,_menu_y
	add	ax,15
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,44
	push	ax
	mov	ax,8
	push	ax
	mov	ax,_menu_y
	add	ax,15
	push	ax
	mov	ax,_menu_x
	add	ax,32
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,OFFSET _actors+1232
	push	ax
	mov	ax,OFFSET _frames+64
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,215
	push	ax
	mov	ax,_menu_x
	add	ax,32
	push	ax
	call	_attach_actor
	add	sp,10
	mov	ax,OFFSET _actors+1260
	push	ax
	mov	ax,OFFSET _frames+80
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,215
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_attach_actor
	add	sp,10
	sub	ax,ax
	push	ax
	push	WORD PTR [bp-22]
	inc	WORD PTR [bp-22]
	call	_draw_menu_row_527e
	add	sp,4
	jmp	g_build_menu_466b_I374
g_build_menu_466b_I373:
	mov	ax,56
	push	ax
	mov	ax,5
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	sub	di,di
	jmp	SHORT g_build_menu_466b_F375
g_build_menu_466b_FC376:
	inc	di
g_build_menu_466b_F375:
	cmp	_menu_columns,di
	jle	g_build_menu_466b_FB377
	mov	WORD PTR [bp-6],OFFSET _frames+48
	mov	ax,28
	imul	di
	add	ax,OFFSET _actors+1624
	mov	WORD PTR [bp-12],ax
	mov	bx,ax
	mov	ax,_menu_y
	add	ax,23
	mov	WORD PTR [bx+2],ax
	mov	bx,WORD PTR [bp-6]
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	cx,_menu_y
	sub	cx,ax
	add	cx,23
	mov	bx,WORD PTR [bp-12]
	mov	WORD PTR [bx+16],cx
	mov	bx,WORD PTR [bp-6]
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	cx,_menu_y
	sub	cx,ax
	mov	al,BYTE PTR [bx+1]
	sub	ah,ah
	add	cx,ax
	add	cx,22
	mov	bx,WORD PTR [bp-12]
	mov	WORD PTR [bx+18],cx
	jmp	SHORT g_build_menu_466b_FC376
g_build_menu_466b_FB377:
	mov	ax,OFFSET _actors+1596
	push	ax
	mov	ax,OFFSET _frames+56
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,223
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_attach_actor
	add	sp,10
	mov	ax,WORD PTR [bp-4]
	mov	WORD PTR _menu_text+2,ax
	cmp	WORD PTR _menu_state,0
	je	g_build_menu_466b_I378
	mov	bx,WORD PTR [bp-14]
	cmp	BYTE PTR [bx+4],0
	je	g_build_menu_466b_L20018
	mov	al,14
	jmp	SHORT g_build_menu_466b_L20019
g_build_menu_466b_L20018:
	mov	al,8
g_build_menu_466b_L20019:
	mov	BYTE PTR _menu_text,al
	jmp	SHORT g_build_menu_466b_I379
g_build_menu_466b_I378:
	mov	bx,WORD PTR [bp-14]
	cmp	BYTE PTR [bx+4],0
	je	g_build_menu_466b_L20020
	mov	al,15
	jmp	SHORT g_build_menu_466b_L20021
g_build_menu_466b_L20020:
	sub	al,al
g_build_menu_466b_L20021:
	mov	BYTE PTR _menu_text,al
g_build_menu_466b_I379:
	mov	ax,_menu_y
	add	ax,15
	push	ax
	mov	ax,_menu_x
	add	ax,36
	push	ax
	mov	ax,OFFSET _menu_text
	push	ax
	call	_draw_text_e915
	add	sp,6
	sub	di,di
	jmp	SHORT g_build_menu_466b_F380
g_build_menu_466b_FC381:
	inc	di
g_build_menu_466b_F380:
	cmp	_menu_columns,di
	jle	g_build_menu_466b_FB382
	mov	WORD PTR [bp-6],OFFSET _frames+72
	mov	ax,28
	imul	di
	add	ax,OFFSET _actors+1288
	mov	WORD PTR [bp-12],ax
	mov	bx,ax
	mov	ax,_menu_y
	add	ax,23
	mov	WORD PTR [bx+2],ax
	mov	bx,WORD PTR [bp-6]
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	cx,_menu_y
	sub	cx,ax
	add	cx,23
	mov	bx,WORD PTR [bp-12]
	mov	WORD PTR [bx+16],cx
	mov	bx,WORD PTR [bp-6]
	mov	al,BYTE PTR [bx+3]
	cbw
	mov	cx,_menu_y
	sub	cx,ax
	mov	al,BYTE PTR [bx+1]
	sub	ah,ah
	add	cx,ax
	add	cx,22
	mov	bx,WORD PTR [bp-12]
	mov	WORD PTR [bx+18],cx
	jmp	SHORT g_build_menu_466b_FC381
g_build_menu_466b_FB382:
	mov	ax,45
	push	ax
	mov	ax,10
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,44
	push	ax
	mov	ax,8
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,32
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,57
	push	ax
	mov	ax,7
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
g_build_menu_466b_I374:
	add	WORD PTR [bp-14],6
	jmp	g_build_menu_466b_FC371
g_build_menu_466b_FB372:
	cmp	WORD PTR _speed_2eb3,3000
	jg	g_build_menu_466b_JCC4220
	jmp	g_build_menu_466b_I383
g_build_menu_466b_JCC4220:
	mov	ax,56
	push	ax
	mov	ax,5
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	mov	ax,57
	push	ax
	mov	ax,7
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,_menu_x
	add	ax,16
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	sub	di,di
	jmp	SHORT g_build_menu_466b_F384
g_build_menu_466b_FC385:
	inc	di
g_build_menu_466b_F384:
	cmp	_menu_columns,di
	jle	g_build_menu_466b_FB386
	lea	ax,WORD PTR [di+58]
	push	ax
	mov	ax,6
	push	ax
	mov	ax,_menu_y
	add	ax,23
	push	ax
	mov	ax,di
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_configure_actor_45a2
	add	sp,8
	jmp	SHORT g_build_menu_466b_FC385
g_build_menu_466b_FB386:
	mov	ax,OFFSET _actors+1596
	push	ax
	mov	ax,OFFSET _frames+56
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,_menu_y
	add	ax,223
	push	ax
	mov	ax,_menu_columns
	mov	cl,4
	shl	ax,cl
	add	ax,_menu_x
	add	ax,48
	push	ax
	call	_attach_actor
	add	sp,10
g_build_menu_466b_I383:
	mov	WORD PTR [bp-12],OFFSET _actors+1232
	sub	di,di
	jmp	SHORT g_build_menu_466b_F387
g_build_menu_466b_FC388:
	inc	di
g_build_menu_466b_F387:
	mov	ax,_menu_columns
	add	ax,2
	cmp	ax,di
	jle	g_build_menu_466b_FB389
	push	WORD PTR [bp-12]
	call	_clear_actor_3e81
	add	sp,2
	mov	bx,WORD PTR [bp-12]
	add	WORD PTR [bp-12],28
	mov	WORD PTR [bx+20],0
	jmp	SHORT g_build_menu_466b_FC388
g_build_menu_466b_FB389:
	call	FAR PTR _graphics_end
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_build_menu_466b ENDP
