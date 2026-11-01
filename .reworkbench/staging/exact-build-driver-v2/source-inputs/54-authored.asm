; Whole procedure reconstructed from REA ev_31c96210365a5b375c7f1abf5cb0cbe0ef2fdd88ad69cac974edd3427dc90ecb.
; Stack reservations reflect native assembly, not invented C locals.
_apply_9749 PROC NEAR
 push bp
 mov bp,sp
 mov ax,8
 call __chkstk
 cmp WORD PTR [bp+12],0
 je apply_forward
 push WORD PTR [bp+4]
 push WORD PTR [bp+6]
 call _swap_cells
 add sp,4
 cmp BYTE PTR [bp+11],0
 je apply_undo_done
 push WORD PTR [bp+4]
 push WORD PTR _opponent
 mov al,BYTE PTR [bp+11]
 sub ah,ah
 push ax
 call _add_piece
 add sp,6
apply_undo_done:
 jmp SHORT apply_special
apply_forward:
 cmp BYTE PTR [bp+11],0
 je apply_forward_swap
 push WORD PTR [bp+4]
 call _remove_piece
 add sp,2
apply_forward_swap:
 push WORD PTR [bp+6]
 push WORD PTR [bp+4]
 call _swap_cells
 add sp,4
apply_special:
 cmp WORD PTR [bp+8],0
 jne apply_kind
 jmp apply_end
apply_kind:
 cmp BYTE PTR [bp+10],1
 jne apply_pawn
 lea ax,WORD PTR [bp-6]
 push ax
 lea ax,WORD PTR [bp-8]
 push ax
 push WORD PTR [bp+4]
 push cs
 call NEAR PTR _castle_95df
 add sp,6
 cmp WORD PTR [bp+12],0
 je apply_castle_forward
 push WORD PTR [bp-8]
 push WORD PTR [bp-6]
 call _swap_cells
 add sp,4
 jmp SHORT apply_castle_done
apply_castle_forward:
 push WORD PTR [bp-6]
 push WORD PTR [bp-8]
 call _swap_cells
 add sp,4
apply_castle_done:
 jmp SHORT apply_end
apply_pawn:
 cmp BYTE PTR [bp+10],6
 jne apply_promote
 mov ax,WORD PTR [bp+4]
 and ax,WORD PTR 7
 mov cx,WORD PTR [bp+6]
 and cx,WORD PTR 112
 add ax,cx
 mov WORD PTR [bp-2],ax
 cmp WORD PTR [bp+12],0
 je apply_pawn_forward
 push ax
 push WORD PTR _opponent
 mov ax,6
 push ax
 call _add_piece
 add sp,6
 jmp SHORT apply_pawn_done
apply_pawn_forward:
 push WORD PTR [bp-2]
 call _remove_piece
 add sp,2
apply_pawn_done:
 jmp SHORT apply_end
apply_promote:
 cmp WORD PTR [bp+12],0
 je apply_promote_forward
 push WORD PTR [bp+6]
 mov ax,6
 push ax
 call _change_piece
 add sp,4
 jmp SHORT apply_end
apply_promote_forward:
 push WORD PTR [bp+4]
 mov al,BYTE PTR [bp+10]
 sub ah,ah
 push ax
 call _change_piece
 add sp,4
apply_end:
 mov sp,bp
 pop bp
 ret
_apply_9749 ENDP
