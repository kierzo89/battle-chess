; Explicit authored assembly for _finish_menu_5035; native 0x5035..0x50af.
; Symbolic FA naming blueprint; native reservation/BP homes; historical C declarations unknown.
; Whole PROC only, composed inside the genuine fresh C5 module; no opcode/data directives.
_finish_menu_5035 PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,14
	call	__chkstk
	push	di
	push	si
	call	FAR PTR _graphics_begin
	mov	WORD PTR [bp-12],0
	cmp	WORD PTR _selected_menu,255
	je	g_finish_menu_5035_I442
	cmp	WORD PTR _menu_row_selected,255
	je	g_finish_menu_5035_I444
	mov	di,_selected_menu
	shl	di,1
	shl	di,1
	mov	bx,_menus
	mov	si,[bx+2][di]
	mov	ax,_menu_row_selected
	mov	cx,ax
	shl	ax,1
	add	ax,cx
	shl	ax,1
	add	si,ax
	cmp	BYTE PTR [si+4],0
	je	g_finish_menu_5035_I444
	mov	ax,WORD PTR [si+2]
	mov	WORD PTR [bp-12],ax
g_finish_menu_5035_I444:
	call	_close_menu_4c74
g_finish_menu_5035_I442:
	mov	WORD PTR _selected_menu,255
	mov	ax,23
	push	ax
	sub	ax,ax
	push	ax
	mov	ax,79
	push	ax
	sub	ax,ax
	push	ax
	call	_restore_region_58b0
	add	sp,8
	call	FAR PTR _graphics_end
	mov	ax,WORD PTR [bp-12]
	jmp	SHORT g_finish_menu_5035_EX439
g_finish_menu_5035_EX439:
	pop	si
	pop	di
	mov	sp,bp
	pop	bp
	ret
_finish_menu_5035 ENDP
