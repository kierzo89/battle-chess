; Complete authored procedure from native REA evidence
; ev_b45b9415b9a0ce8658180e00b0e5cbdef7cb9127f9935fdbdae3f7e3402da0a5
; The unused frame word is native assembly layout, not claimed as a C local.
_search_window PROC NEAR
 push bp
 mov bp,sp
 mov ax,4
 call __chkstk
 cmp BYTE PTR _working_move+6,1
 sbb ax,ax
 inc ax
 mov WORD PTR _search_options,ax
 mov WORD PTR _input_state,0
 mov ax,OFFSET _working_move
 push ax
 push WORD PTR _search_options+4
 push WORD PTR _search_options+2
 push WORD PTR _search_options
 push WORD PTR _iteration
 push WORD PTR [bp+6]
 push WORD PTR [bp+4]
 call _search_node
 add sp,14
 mov WORD PTR [bp-4],ax
 cmp WORD PTR _input_state,0
 jne window_no_best
 mov _best,ax
window_no_best:
 mov ax,WORD PTR [bp-4]
 jmp SHORT window_return
window_return:
 mov sp,bp
 pop bp
 ret
_search_window ENDP
