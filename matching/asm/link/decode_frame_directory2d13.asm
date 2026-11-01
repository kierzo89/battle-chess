; Complete native289 frame-directory decoder; old ordinary C differences stay held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _arena_cursor:WORD, _count_0096:WORD, _frames:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _huff_decode_stream:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT,DS:DGROUP,SS:DGROUP
PUBLIC _decode_frame_directory
_decode_frame_directory PROC NEAR
    PUSH BP ; native2D13 / 1 bytes
    MOV BP, SP ; native2D14 / 2 bytes
    SUB SP, 01ch ; native2D16 / 3 bytes
    PUSH DI ; native2D19 / 1 bytes
    PUSH SI ; native2D1A / 1 bytes
    MOV AX, _arena_cursor ; native2D1B / 3 bytes
    MOV DX, word ptr _arena_cursor+2 ; native2D1E / 4 bytes
    MOV word ptr [BP - 08h], AX ; native2D22 / 3 bytes
    MOV word ptr [BP - 06h], DX ; native2D25 / 3 bytes
    MOV AX, _count_0096 ; native2D28 / 3 bytes
    MOV CL, 03h ; native2D2B / 2 bytes
    SHL AX, CL ; native2D2D / 2 bytes
    ADD AX, OFFSET DGROUP:_frames ; native2D2F / 3 bytes
    MOV word ptr [BP - 014h], AX ; native2D32 / 3 bytes
    MOV SI, word ptr _count_0096 ; native2D35 / 4 bytes
    JMP SHORT decode_2d71 ; native2D39 / 2 bytes
decode_2d3b:
    LES BX, [BP - 08h] ; native2D3B / 3 bytes
    MOV AL, byte ptr ES:[BX] ; native2D3E / 3 bytes
    LES BX, [BP - 0ch] ; native2D41 / 3 bytes
    XOR byte ptr ES:[BX], AL ; native2D44 / 3 bytes
    ADD word ptr [BP - 0ch], 01h ; native2D47 / 4 bytes
    SBB AX, AX ; native2D4B / 2 bytes
    AND AX, 01000h ; native2D4D / 3 bytes
    ADD word ptr [BP - 0ah], AX ; native2D50 / 3 bytes
    ADD word ptr [BP - 08h], 01h ; native2D53 / 4 bytes
    SBB AX, AX ; native2D57 / 2 bytes
    AND AX, 01000h ; native2D59 / 3 bytes
    ADD word ptr [BP - 06h], AX ; native2D5C / 3 bytes
    DEC DI ; native2D5F / 1 bytes
decode_2d60:
    OR DI, DI ; native2D60 / 2 bytes
    JNZ SHORT decode_2d3b ; native2D62 / 2 bytes
    MOV AX, word ptr [BP - 0ch] ; native2D64 / 3 bytes
    MOV DX, word ptr [BP - 0ah] ; native2D67 / 3 bytes
    MOV word ptr [BP - 08h], AX ; native2D6A / 3 bytes
    MOV word ptr [BP - 06h], DX ; native2D6D / 3 bytes
    INC SI ; native2D70 / 1 bytes
decode_2d71:
    MOV BX, word ptr [BP + 04h] ; native2D71 / 3 bytes
    MOV AX, word ptr [BX] ; native2D74 / 2 bytes
    OR AX, word ptr [BX + 02h] ; native2D76 / 3 bytes
    JNZ SHORT decode_2d7e ; native2D79 / 2 bytes
    JMP NEAR PTR decode_2e1d ; native2D7B / 3 bytes
decode_2d7e:
    ADD word ptr [BP + 04h], 04h ; native2D7E / 4 bytes
    MOV AX, word ptr [BX] ; native2D82 / 2 bytes
    MOV DX, word ptr [BX + 02h] ; native2D84 / 3 bytes
    MOV BX, word ptr [BP - 014h] ; native2D87 / 3 bytes
    ADD word ptr [BP - 014h], 04h ; native2D8A / 4 bytes
    MOV word ptr [BX], AX ; native2D8E / 2 bytes
    MOV word ptr [BX + 02h], DX ; native2D90 / 3 bytes
    MOV BX, word ptr [BP - 014h] ; native2D93 / 3 bytes
    ADD word ptr [BP - 014h], 04h ; native2D96 / 4 bytes
    MOV AX, word ptr [BP - 08h] ; native2D9A / 3 bytes
    MOV DX, word ptr [BP - 06h] ; native2D9D / 3 bytes
    MOV word ptr [BX], AX ; native2DA0 / 2 bytes
    MOV word ptr [BX + 02h], DX ; native2DA2 / 3 bytes
    MOV AX, SI ; native2DA5 / 2 bytes
    MOV CL, 03h ; native2DA7 / 2 bytes
    SHL AX, CL ; native2DA9 / 2 bytes
    MOV word ptr [BP - 016h], AX ; native2DAB / 3 bytes
    MOV BX, AX ; native2DAE / 2 bytes
    MOV AL, byte ptr _frames[BX] ; native2DB0 / 4 bytes
    SUB AH, AH ; native2DB4 / 2 bytes
    INC AX ; native2DB6 / 1 bytes
    SHR AX, 01h ; native2DB7 / 2 bytes
    MOV word ptr [BP - 018h], AX ; native2DB9 / 3 bytes
    PUSH AX ; native2DBC / 1 bytes
    MOV AL, byte ptr _frames[BX]+1 ; native2DBD / 4 bytes
    SUB AH, AH ; native2DC1 / 2 bytes
    MUL word ptr [BP - 018h] ; native2DC3 / 3 bytes
    SUB CX, CX ; native2DC6 / 2 bytes
    PUSH CX ; native2DC8 / 1 bytes
    PUSH AX ; native2DC9 / 1 bytes
    PUSH word ptr [BP - 06h] ; native2DCA / 3 bytes
    PUSH word ptr [BP - 08h] ; native2DCD / 3 bytes
    CALL NEAR PTR _huff_decode_stream ; native2DD0 / 3 bytes
    ADD SP, 0ah ; native2DD3 / 3 bytes
    MOV AX, SI ; native2DD6 / 2 bytes
    MOV CL, 03h ; native2DD8 / 2 bytes
    SHL AX, CL ; native2DDA / 2 bytes
    MOV word ptr [BP - 01ah], AX ; native2DDC / 3 bytes
    MOV BX, AX ; native2DDF / 2 bytes
    MOV AL, byte ptr _frames[BX] ; native2DE1 / 4 bytes
    SUB AH, AH ; native2DE5 / 2 bytes
    ADD AX, 03h ; native2DE7 / 3 bytes
    SHR AX, 01h ; native2DEA / 2 bytes
    AND AX, 0feh ; native2DEC / 3 bytes
    MOV word ptr [BP - 01ch], AX ; native2DEF / 3 bytes
    MOV AL, byte ptr _frames[BX]+1 ; native2DF2 / 4 bytes
    SUB AH, AH ; native2DF6 / 2 bytes
    DEC AX ; native2DF8 / 1 bytes
    MUL word ptr [BP - 01ch] ; native2DF9 / 3 bytes
    MOV word ptr [BP - 04h], AX ; native2DFC / 3 bytes
    MOV AX, word ptr [BP - 01ch] ; native2DFF / 3 bytes
    SUB DX, DX ; native2E02 / 2 bytes
    ADD AX, word ptr [BP - 08h] ; native2E04 / 3 bytes
    ADC DX, DX ; native2E07 / 2 bytes
    MOV CX, 0ch ; native2E09 / 3 bytes
    SHL DX, CL ; native2E0C / 2 bytes
    ADD DX, word ptr [BP - 06h] ; native2E0E / 3 bytes
    MOV word ptr [BP - 0ch], AX ; native2E11 / 3 bytes
    MOV word ptr [BP - 0ah], DX ; native2E14 / 3 bytes
    MOV DI, word ptr [BP - 04h] ; native2E17 / 3 bytes
    JMP NEAR PTR decode_2d60 ; native2E1A / 3 bytes
decode_2e1d:
    MOV AX, word ptr [BP - 08h] ; native2E1D / 3 bytes
    MOV DX, word ptr [BP - 06h] ; native2E20 / 3 bytes
    MOV _arena_cursor, AX ; native2E23 / 3 bytes
    MOV word ptr _arena_cursor+2, DX ; native2E26 / 4 bytes
    MOV word ptr _count_0096, SI ; native2E2A / 4 bytes
    POP SI ; native2E2E / 1 bytes
    POP DI ; native2E2F / 1 bytes
    MOV SP, BP ; native2E30 / 2 bytes
    POP BP ; native2E32 / 1 bytes
    RET ; native2E33 / 1 bytes
_decode_frame_directory ENDP
_TEXT ENDS
END
