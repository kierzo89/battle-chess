; Transparent native180 fallback. C reconstruction/frame explanation remains held.
; No historical ASM attribution, new initialized storage, or C-function credit.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _cursor_square_0efc:WORD, _selected_square_0efa:WORD
EXTRN _waiting_0eee:WORD, _menu_enabled_0ef0:WORD, _cursor_kind_0ef4:WORD
EXTRN _cursor_actor_57d0:WORD, _actors:BYTE
; Real saved BYTE views, currently lacking logical providers. No storage defined.
EXTRN _saved_cursor_8d0a:BYTE, _actor_flag_9374:BYTE
EXTRN _input_mode_984e:BYTE, _input_flag_8fe0:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR
EXTRN _outline_square_543a:NEAR
EXTRN _detach_actor:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _begin_input_0fb0, _end_input_102d
_begin_input_0fb0 PROC NEAR
    push bp                              ; native0FB0
    mov bp,sp                            ; native0FB1
    mov ax,04h                           ; native0FB3
    call NEAR PTR __chkstk                ; native0FB6
    push si                              ; native0FB9
    sub ax,ax                            ; native0FBA
    push ax                              ; native0FBC
    push WORD PTR _cursor_square_0efc     ; native0FBD
    call NEAR PTR _outline_square_543a    ; native0FC1
    add sp,04h                           ; native0FC4
    sub ax,ax                            ; native0FC7
    push ax                              ; native0FC9
    push WORD PTR _selected_square_0efa   ; native0FCA
    call NEAR PTR _outline_square_543a    ; native0FCE
    add sp,04h                           ; native0FD1
    mov al,BYTE PTR _cursor_square_0efc   ; native0FD4
    mov _saved_cursor_8d0a,al             ; native0FD7
    mov ax,0ffh                          ; native0FDA
    mov _selected_square_0efa,ax          ; native0FDD
    mov _cursor_square_0efc,ax            ; native0FE0
    cmp WORD PTR _cursor_kind_0ef4,00h    ; native0FE3
    jz short L_1004                      ; native0FE8
    mov ax,01ch                          ; native0FEA
    imul WORD PTR _cursor_actor_57d0      ; native0FED
    mov si,ax                            ; native0FF1
    cmp WORD PTR _actors[si+014h],00h     ; native0FF3
    jz short L_1004                      ; native0FF8
    add ax,OFFSET DGROUP:_actors                ; native0FFA
    push ax                              ; native0FFD
    call NEAR PTR _detach_actor          ; native0FFE
    add sp,02h                           ; native1001
L_1004:
    mov al,BYTE PTR _cursor_kind_0ef4     ; native1004
    mov _actor_flag_9374,al               ; native1007
    mov al,BYTE PTR _waiting_0eee         ; native100A
    mov _input_mode_984e,al               ; native100D
    mov al,BYTE PTR _menu_enabled_0ef0    ; native1010
    mov _input_flag_8fe0,al               ; native1013
    mov WORD PTR _waiting_0eee,00h        ; native1016
    mov WORD PTR _menu_enabled_0ef0,00h   ; native101C
    mov WORD PTR _cursor_kind_0ef4,00h    ; native1022
    pop si                               ; native1028
    mov sp,bp                            ; native1029
    pop bp                               ; native102B
    ret                                  ; native102C
_begin_input_0fb0 ENDP
_end_input_102d PROC NEAR
    push bp                              ; native102D
    mov bp,sp                            ; native102E
    mov ax,04h                           ; native1030
    call NEAR PTR __chkstk                ; native1033
    mov al,_saved_cursor_8d0a             ; native1036
    sub ah,ah                            ; native1039
    mov _cursor_square_0efc,ax            ; native103B
    mov ax,01ch                          ; native103E
    push ax                              ; native1041
    push WORD PTR _cursor_square_0efc     ; native1042
    call NEAR PTR _outline_square_543a    ; native1046
    add sp,04h                           ; native1049
    mov al,_input_mode_984e               ; native104C
    sub ah,ah                            ; native104F
    mov _waiting_0eee,ax                  ; native1051
    mov al,_input_flag_8fe0               ; native1054
    mov _menu_enabled_0ef0,ax              ; native1057
    mov al,_actor_flag_9374               ; native105A
    mov _cursor_kind_0ef4,ax              ; native105D
    mov sp,bp                            ; native1060
    pop bp                               ; native1062
    ret                                  ; native1063
_end_input_102d ENDP
_TEXT ENDS
END
