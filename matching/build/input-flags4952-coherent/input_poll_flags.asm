; Original register-based mouse/joystick acquisition and PIT timing.
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _input_poll_handler_4950:WORD
EXTRN _input_flags_4952:BYTE
EXTRN _joystick_centre_x_4954:WORD, _joystick_centre_y_4956:WORD
EXTRN _flag_005b:BYTE, _input_x_005c:WORD, _input_y_005e:WORD
EXTRN _buttons_8d04:WORD
_DATA ENDS
DGROUP GROUP _DATA
GRAPHICS_INPUT_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:GRAPHICS_INPUT_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _input_probe_11ef_004e, _input_poll_11ef_00b9, _special_command_1fc2
_input_probe_11ef_004e PROC FAR
    mov bx, 0cch
    mov ax, 0
    mov es, ax
    mov ax, es:[bx+2]
    or ax, ax
    jz probe_joystick
    sub ax, ax
    int 33h
    or ax, ax
    jz probe_joystick
    mov _input_poll_handler_4950, OFFSET mouse_poll
    mov ax, 7
    mov cx, 0
    mov dx, 319
    int 33h
    mov ax, 8
    mov cx, 0
    mov dx, 199
    int 33h
    mov ax, 1
    retf
probe_joystick:
    mov dx, 201h
    sub cx, cx
    out dx, al
    in al, dx
    and al, 3
    mov bl, al
probe_discharge:
    in al, dx
    and al, 3
    cmp al, bl
    jne joystick_present
    loop probe_discharge
    sub ax, ax
    retf
joystick_present:
    mov _input_poll_handler_4950, OFFSET joystick_poll
    call far ptr _special_command_1fc2
    call far ptr _special_command_1fc2
    call far ptr _special_command_1fc2
    mov ax, 1
    mov _flag_005b, al
    retf
_input_probe_11ef_004e ENDP
_input_poll_11ef_00b9 PROC FAR
    mov ax, _input_poll_handler_4950
    jmp ax
_input_poll_11ef_00b9 ENDP
mouse_poll PROC FAR
    push bp
    mov ax, 3
    int 33h
    mov _buttons_8d04, bx
    mov _input_x_005c, cx
    mov _input_y_005e, dx
    pop bp
    retf
mouse_poll ENDP
_special_command_1fc2 PROC FAR
    push si
    push di
    cmp _input_poll_handler_4950, OFFSET joystick_poll
    jne centre_done
    call far ptr read_joystick
    sub cx, 30
    sub dx, 10
    mov _joystick_centre_x_4954, cx
    mov _joystick_centre_y_4956, dx
centre_done:
    pop di
    pop si
    retf
_special_command_1fc2 ENDP
joystick_poll PROC FAR
    push si
    push di
    call far ptr read_joystick
    sub cx, _joystick_centre_x_4954
    sub dx, _joystick_centre_y_4956
    mov al, ch
    cbw
    sar ax, 1
    mov cx, ax
    mov al, dh
    cbw
    sar ax, 1
    mov dx, ax
    mov ax, _input_x_005c
    add ax, cx
    jns x_nonnegative
    sub ax, ax
x_nonnegative:
    cmp ax, 320
    jl x_ready
    mov ax, 319
x_ready:
    mov _input_x_005c, ax
    mov ax, _input_y_005e
    add ax, dx
    jns y_nonnegative
    sub ax, ax
y_nonnegative:
    cmp ax, 200
    jl y_ready
    mov ax, 199
y_ready:
    mov _input_y_005e, ax
    sub bx, bx
    mov dx, 201h
    in al, dx
    and al, 30h
    cmp al, 30h
    je buttons_ready
    mov bl, al
    xor bl, 30h
buttons_ready:
    cmp al, _input_flags_4952+1
    je debounce_done
    mov _input_flags_4952+1, al
    call far ptr read_pit
    mov cx, ax
    ; The real hardware debounce branch switches unsigned/signed ordering
    ; when the timer sum crosses16 bits. The writable byte is code, not DATA.
    mov byte ptr cs:debounce_branch, 77h
    add cx, 1785
    jnc debounce_wait
    mov byte ptr cs:debounce_branch, 7fh
debounce_wait:
    call far ptr read_pit
    mov dx, ax
    cmp cx, dx
debounce_branch:
    ja debounce_wait
debounce_done:
    sub ah, ah
    mov al, bl
    mov cl, 4
    shr ax, cl
    mov _buttons_8d04, ax
    pop di
    pop si
    retf
joystick_poll ENDP
read_joystick PROC FAR
    mov dx, 201h
    sub al, al
    cli
    out dx, al
    call far ptr read_pit
    mov si, ax
    mov ah, 3
wait_first_axis:
    in al, dx
    and al, ah
    cmp al, ah
    je wait_first_axis
    mov bl, al
    call far ptr read_pit
    mov di, ax
    mov ah, bl
    and ah, 3
wait_second_axis:
    in al, dx
    test al, ah
    jne wait_second_axis
    mov bl, ah
    call far ptr read_pit
    sti
    mov cx, si
    sub cx, di
    mov dx, si
    sub dx, ax
    cmp bl, 2
    je axes_ready
    xchg cx, dx
axes_ready:
    retf
read_joystick ENDP
read_pit PROC FAR
    sub al, al
    out 43h, al
    in al, 40h
    mov ah, al
    in al, 40h
    xchg al, ah
    retf
read_pit ENDP
GRAPHICS_INPUT_TEXT ENDS
END
