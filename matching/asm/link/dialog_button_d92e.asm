; Complete native152 mnemonic source; genuine Cframe2/native4 remains held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _pointer_x:WORD, _pointer_y:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _paint_dialog_button_d9c6:NEAR, _next_dialog_event_d766:NEAR, _dialog_hit_d840:NEAR
EXTRN _update_pointer_11ef_0030:FAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT,DS:DGROUP,SS:DGROUP
PUBLIC _dialog_button_d92e
_dialog_button_d92e PROC NEAR
    PUSH BP ; nativeD92E / 1 bytes
    MOV BP, SP ; nativeD92F / 2 bytes
    SUB SP, 04h ; nativeD931 / 3 bytes
button_d934:
    MOV AX, 01h ; nativeD934 / 3 bytes
button_d937:
    PUSH AX ; nativeD937 / 1 bytes
    PUSH word ptr [BP + 04h] ; nativeD938 / 3 bytes
    CALL NEAR PTR _paint_dialog_button_d9c6 ; nativeD93B / 3 bytes
    ADD SP, 04h ; nativeD93E / 3 bytes
button_d941:
    CALL NEAR PTR _next_dialog_event_d766 ; nativeD941 / 3 bytes
    MOV word ptr [BP - 02h], AX ; nativeD944 / 3 bytes
    MOV BX, AX ; nativeD947 / 2 bytes
    CMP word ptr [BX], 04h ; nativeD949 / 3 bytes
    JNZ SHORT button_d985 ; nativeD94C / 2 bytes
    CMP word ptr [BX + 02h], 00h ; nativeD94E / 4 bytes
    JNZ SHORT button_d985 ; nativeD952 / 2 bytes
    CMP word ptr [BX + 04h], 00h ; nativeD954 / 4 bytes
    JNZ SHORT button_d985 ; nativeD958 / 2 bytes
    SUB AX, AX ; nativeD95A / 2 bytes
    PUSH AX ; nativeD95C / 1 bytes
    PUSH word ptr [BP + 04h] ; nativeD95D / 3 bytes
    CALL NEAR PTR _paint_dialog_button_d9c6 ; nativeD960 / 3 bytes
    ADD SP, 04h ; nativeD963 / 3 bytes
    PUSH word ptr [BP + 06h] ; nativeD966 / 3 bytes
    PUSH WORD PTR [_pointer_y] ; nativeD969 / 4 bytes
    PUSH WORD PTR [_pointer_x] ; nativeD96D / 4 bytes
    CALL NEAR PTR _dialog_hit_d840 ; nativeD971 / 3 bytes
    ADD SP, 06h ; nativeD974 / 3 bytes
    CMP AX, word ptr [BP + 04h] ; nativeD977 / 3 bytes
    JNZ SHORT button_d981 ; nativeD97A / 2 bytes
    MOV AX, 01h ; nativeD97C / 3 bytes
    JMP SHORT button_d9c2 ; nativeD97F / 2 bytes
button_d981:
    SUB AX, AX ; nativeD981 / 2 bytes
    JMP SHORT button_d9c2 ; nativeD983 / 2 bytes
button_d985:
    MOV BX, word ptr [BP - 02h] ; nativeD985 / 3 bytes
    CMP word ptr [BX], 05h ; nativeD988 / 3 bytes
    JNZ SHORT button_d941 ; nativeD98B / 2 bytes
    CMP word ptr [BX + 02h], 00h ; nativeD98D / 4 bytes
    JNZ SHORT button_d941 ; nativeD991 / 2 bytes
    MOV AX, word ptr [BX + 08h] ; nativeD993 / 3 bytes
    MOV [_pointer_x],AX ; nativeD996 / 3 bytes
    MOV AX, word ptr [BX + 0ah] ; nativeD999 / 3 bytes
    MOV [_pointer_y],AX ; nativeD99C / 3 bytes
    CALL FAR PTR _update_pointer_11ef_0030 ; nativeD99F / 5 bytes
    PUSH word ptr [BP + 06h] ; nativeD9A4 / 3 bytes
    PUSH WORD PTR [_pointer_y] ; nativeD9A7 / 4 bytes
    PUSH WORD PTR [_pointer_x] ; nativeD9AB / 4 bytes
    CALL NEAR PTR _dialog_hit_d840 ; nativeD9AF / 3 bytes
    ADD SP, 06h ; nativeD9B2 / 3 bytes
    CMP AX, word ptr [BP + 04h] ; nativeD9B5 / 3 bytes
    JNZ SHORT button_d9bd ; nativeD9B8 / 2 bytes
    JMP NEAR PTR button_d934 ; nativeD9BA / 3 bytes
button_d9bd:
    SUB AX, AX ; nativeD9BD / 2 bytes
    JMP NEAR PTR button_d937 ; nativeD9BF / 3 bytes
button_d9c2:
    MOV SP, BP ; nativeD9C2 / 2 bytes
    POP BP ; nativeD9C4 / 1 bytes
    RET ; nativeD9C5 / 1 bytes
_dialog_button_d92e ENDP
_TEXT ENDS
END
