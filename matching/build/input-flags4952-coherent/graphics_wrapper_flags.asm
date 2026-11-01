; Three contiguous register-convention wrappers around the loaded graphics driver.
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _input_flags_4952:BYTE
EXTRN _input_mode_0046:WORD, _input_x_005c:WORD, _input_y_005e:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _graphics_pointer_110d_0006:FAR, _graphics_pointer_110d_0009:FAR
GRAPHICS_INPUT_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:GRAPHICS_INPUT_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _graphics_end, _graphics_begin, _update_pointer_11ef_0030
_graphics_end PROC FAR
    mov al, _input_flags_4952+0
    inc al
    mov _input_flags_4952+0, al
    cmp al, 1
    jne graphics_end_done
    mov bx, _input_mode_0046
    mov cx, _input_x_005c
    mov dx, _input_y_005e
    jmp _graphics_pointer_110d_0006
graphics_end_done:
    retf
_graphics_end ENDP
_graphics_begin PROC FAR
    mov al, _input_flags_4952+0
    dec al
    mov _input_flags_4952+0, al
    or al, al
    jne graphics_begin_done
    jmp _graphics_pointer_110d_0009
graphics_begin_done:
    retf
_graphics_begin ENDP
_update_pointer_11ef_0030 PROC FAR
    cmp _input_flags_4952+0, 0
    jle graphics_pointer_done
    call _graphics_pointer_110d_0009
    mov bx, _input_mode_0046
    mov cx, _input_x_005c
    mov dx, _input_y_005e
    call _graphics_pointer_110d_0006
graphics_pointer_done:
    retf
_update_pointer_11ef_0030 ENDP
GRAPHICS_INPUT_TEXT ENDS
END
