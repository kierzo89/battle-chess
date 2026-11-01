; Explicit authored assembly for _close_menu_4c74; native 0x4c74..0x4e5d.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_close_menu_4c74 PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,14
	call	__chkstk
	push	di
	push	si
	call	FAR PTR _graphics_begin
	mov	si,32
	cmp	WORD PTR _speed_2eb3,3000
	jle	g_close_menu_4c74_JCC4447
	jmp	g_close_menu_4c74_I402
g_close_menu_4c74_JCC4447:
g_close_menu_4c74_FC404:
	cmp	WORD PTR _menu_y,25
	jg	g_close_menu_4c74_JCC4457
	jmp	g_close_menu_4c74_FB405
g_close_menu_4c74_JCC4457:
	call	_advance_menu_5381
	sub	WORD PTR _menu_y,8
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
	jmp	SHORT g_close_menu_4c74_F406
g_close_menu_4c74_FC407:
	inc	di
g_close_menu_4c74_F406:
	cmp	_menu_columns,di
	jle	g_close_menu_4c74_FB408
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
	jmp	SHORT g_close_menu_4c74_FC407
g_close_menu_4c74_FB408:
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
	jmp	g_close_menu_4c74_FC404
g_close_menu_4c74_FB405:
	mov	ax,33
	push	ax
	mov	ax,16
	push	ax
	push	WORD PTR _menu_y
	push	WORD PTR _menu_x
	call	_configure_actor_45a2
	add	sp,8
g_close_menu_4c74_I402:
	mov	WORD PTR [bp-6],OFFSET _actors+1568
	sub	di,di
	jmp	SHORT g_close_menu_4c74_F409
g_close_menu_4c74_FC410:
	inc	di
g_close_menu_4c74_F409:
	mov	ax,_menu_columns
	add	ax,2
	cmp	ax,di
	jle	g_close_menu_4c74_FB411
	push	WORD PTR [bp-6]
	call	_clear_actor_3e81
	add	sp,2
	mov	bx,WORD PTR [bp-6]
	add	WORD PTR [bp-6],28
	mov	WORD PTR [bx+20],0
	jmp	SHORT g_close_menu_4c74_FC410
g_close_menu_4c74_FB411:
	mov	WORD PTR [bp-6],OFFSET _actors+896
	sub	di,di
	jmp	SHORT g_close_menu_4c74_F412
g_close_menu_4c74_FC413:
	inc	di
g_close_menu_4c74_F412:
	mov	ax,_menu_columns
	add	ax,2
	cmp	ax,di
	jle	g_close_menu_4c74_FB414
	push	WORD PTR [bp-6]
	call	_clear_actor_3e81
	add	sp,2
	mov	bx,WORD PTR [bp-6]
	add	WORD PTR [bp-6],28
	mov	WORD PTR [bx+20],0
	jmp	SHORT g_close_menu_4c74_FC413
g_close_menu_4c74_FB414:
	mov	ax,OFFSET _actors+1904
	push	ax
	call	_detach_actor
	add	sp,2
	mov	ax,OFFSET _actors+1932
	push	ax
	call	_detach_actor
	add	sp,2
	cmp	WORD PTR _speed_2eb3,3000
	jle	g_close_menu_4c74_I415
	push	WORD PTR _actors+1614
	push	WORD PTR _actors+1950
	mov	ax,WORD PTR _actors+1946
	sar	ax,1
	sar	ax,1
	push	ax
	mov	ax,WORD PTR _actors+1916
	sar	ax,1
	sar	ax,1
	push	ax
	call	_restore_region_58b0
	add	sp,8
	jmp	SHORT g_close_menu_4c74_I416
g_close_menu_4c74_I415:
	mov	WORD PTR _actors+944,OFFSET _frames+128
	mov	WORD PTR _actors+1616,OFFSET _frames+56
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
	mov	ax,OFFSET _actors+924
	push	ax
	call	_detach_actor
	add	sp,2
	mov	ax,OFFSET _actors+1596
	push	ax
	call	_detach_actor
	add	sp,2
g_close_menu_4c74_I416:
	mov	WORD PTR _menu_row_selected,255
	call	FAR PTR _graphics_end
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_close_menu_4c74 ENDP
