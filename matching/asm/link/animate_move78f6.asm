; Whole native78F6..7A61/363. Frame20 is native machine state, not C source proof.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _cells:BYTE, _actor_map:BYTE, _kind_map:BYTE, _actors:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _detach_actor:NEAR, _queue_piece:NEAR, _undo_animation:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _animate_move
_animate_move PROC NEAR
    PUSH BP ; native 78F6
    MOV BP, SP ; native 78F7
    MOV AX, 014h ; native 78F9
    CALL NEAR PTR __chkstk ; native 78FC
    PUSH DI ; native 78FF
    PUSH SI ; native 7900
    MOV SI, word ptr [BP + 04h] ; native 7901
    MOV byte ptr [BP-02h], 00h ; native 7904
    MOV AX, word ptr [SI + 02h] ; native 7908
    SAR AX, 01h ; native 790B
    AND AL, 038h ; native 790D
    XOR AL, 038h ; native 790F
    MOV CL, byte ptr [SI + 02h] ; native 7911
    AND CL, 07h ; native 7914
    OR AL, CL ; native 7917
    MOV byte ptr [BP-0Ah], AL ; native 7919
    MOV AX, word ptr [SI] ; native 791C
    SAR AX, 01h ; native 791E
    AND AL, 038h ; native 7920
    XOR AL, 038h ; native 7922
    MOV CL, byte ptr [SI] ; native 7924
    AND CL, 07h ; native 7926
    OR AL, CL ; native 7929
    MOV byte ptr [BP-0Ch], AL ; native 792B
    MOV BL, AL ; native 792E
    SUB BH, BH ; native 7930
    MOV AL, 01Ch ; native 7932
    MUL byte ptr _actor_map[BX] ; native 7934
    ADD AX, OFFSET DGROUP:_actors ; native 7938
    PUSH AX ; native 793B
    CALL NEAR PTR _detach_actor ; native 793C
    ADD SP, 02h ; native 793F
    CMP word ptr [SI + 04h], 00h ; native 7942
    JZ SHORT code_7967 ; native 7946
    CMP byte ptr [SI + 06h], 06h ; native 7948
    JZ SHORT code_7967 ; native 794C
    CMP byte ptr [SI + 06h], 01h ; native 794E
    JZ SHORT code_7967 ; native 7952
    MOV AL, byte ptr [BP-0Ch] ; native 7954
    SUB AH, AH ; native 7957
    MOV DI, AX ; native 7959
    ADD DI, OFFSET DGROUP:_cells ; native 795B
    MOV AL, byte ptr [DI] ; native 795F
    AND AL, 078h ; native 7961
    OR AL, 04h ; native 7963
    MOV byte ptr [DI], AL ; native 7965
code_7967:
    MOV AL, byte ptr [BP-0Ch] ; native 7967
    SUB AH, AH ; native 796A
    MOV DI, AX ; native 796C
    MOV AL, byte ptr _cells[DI] ; native 796E
    AND AL, 040h ; native 7972
    MOV byte ptr [BP-06h], AL ; native 7974
    MOV AL, byte ptr [BP-0Ah] ; native 7977
    PUSH AX ; native 797A
    MOV AL, byte ptr _actor_map[DI] ; native 797B
    PUSH AX ; native 797F
    MOV AL, byte ptr [BP-06h] ; native 7980
    PUSH AX ; native 7983
    MOV AL, byte ptr _cells[DI] ; native 7984
    AND AX, 07h ; native 7988
    PUSH AX ; native 798B
    CALL NEAR PTR _queue_piece ; native 798C
    ADD SP, 08h ; native 798F
    MOV BL, byte ptr [BP-0Ch] ; native 7992
    SUB BH, BH ; native 7995
    MOV byte ptr _cells[BX], BH ; native 7997
    CMP word ptr [SI + 04h], 00h ; native 799B
    JZ SHORT code_79bb ; native 799F
    CMP byte ptr [SI + 06h], 06h ; native 79A1
    JNZ SHORT code_79bb ; native 79A5
    MOV byte ptr [BP-02h], 04h ; native 79A7
    MOV AL, byte ptr [BP-0Ch] ; native 79AB
    AND AL, 07h ; native 79AE
    MOV CL, byte ptr [BP-0Ah] ; native 79B0
    AND CL, 038h ; native 79B3
    OR AL, CL ; native 79B6
    MOV byte ptr [BP-0Ch], AL ; native 79B8
code_79bb:
    CMP byte ptr [SI + 07h], 00h ; native 79BB
    JZ SHORT code_79cd ; native 79BF
    MOV BL, byte ptr [SI + 07h] ; native 79C1
    SUB BH, BH ; native 79C4
    MOV AL, byte ptr _kind_map[BX] ; native 79C6
    MOV byte ptr [BP-02h], AL ; native 79CA
code_79cd:
    CMP byte ptr [BP-02h], 00h ; native 79CD
    JZ SHORT code_7a0c ; native 79D1
    MOV byte ptr [BP-0Ah], 00h ; native 79D3
    JMP SHORT code_79dc ; native 79D7
code_79d9:
    INC byte ptr [BP-0Ah] ; native 79D9
code_79dc:
    CMP byte ptr [BP-0Ah], 020h ; native 79DC
    JNC SHORT code_79f2 ; native 79E0
    MOV AL, 01Ch ; native 79E2
    MUL byte ptr [BP-0Ah] ; native 79E4
    MOV BX, AX ; native 79E7
    CMP word ptr _actors+20[BX], 00h ; native 79E9
    JZ SHORT code_79f2 ; native 79EE
    JMP SHORT code_79d9 ; native 79F0
code_79f2:
    MOV AL, byte ptr [BP-0Ch] ; native 79F2
    SUB AH, AH ; native 79F5
    PUSH AX ; native 79F7
    MOV AL, byte ptr [BP-0Ah] ; native 79F8
    PUSH AX ; native 79FB
    MOV AL, byte ptr [BP-06h] ; native 79FC
    XOR AL, 040h ; native 79FF
    PUSH AX ; native 7A01
    MOV AL, byte ptr [BP-02h] ; native 7A02
    PUSH AX ; native 7A05
    CALL NEAR PTR _queue_piece ; native 7A06
    ADD SP, 08h ; native 7A09
code_7a0c:
    CMP word ptr [SI + 04h], 00h ; native 7A0C
    JZ SHORT code_7a5b ; native 7A10
    CMP byte ptr [SI + 06h], 01h ; native 7A12
    JNZ SHORT code_7a5b ; native 7A16
    MOV byte ptr [BP-0Eh], 03h ; native 7A18
    MOV word ptr [BP-010h], 00h ; native 7A1C
    MOV AL, byte ptr [SI] ; native 7A21
    AND AL, 07h ; native 7A23
    CMP AL, 06h ; native 7A25
    JNZ SHORT code_7a3f ; native 7A27
    MOV AX, word ptr [SI] ; native 7A29
    AND AX, 0F0h ; native 7A2B
    OR AL, 07h ; native 7A2E
    MOV word ptr [BP-014h], AX ; native 7A30
    MOV AX, word ptr [SI] ; native 7A33
    AND AX, 0F0h ; native 7A35
    OR AL, 05h ; native 7A38
    MOV word ptr [BP-012h], AX ; native 7A3A
    JMP SHORT code_7a51 ; native 7A3D
code_7a3f:
    MOV AX, word ptr [SI] ; native 7A3F
    AND AX, 0F0h ; native 7A41
    MOV word ptr [BP-014h], AX ; native 7A44
    MOV AX, word ptr [SI] ; native 7A47
    AND AX, 0F0h ; native 7A49
    OR AL, 03h ; native 7A4C
    MOV word ptr [BP-012h], AX ; native 7A4E
code_7a51:
    LEA AX, [BP-014h] ; native 7A51
    PUSH AX ; native 7A54
    CALL NEAR PTR _undo_animation ; native 7A55
    ADD SP, 02h ; native 7A58
code_7a5b:
    POP SI ; native 7A5B
    POP DI ; native 7A5C
    MOV SP, BP ; native 7A5D
    POP BP ; native 7A5F
    RET ; native 7A60
_animate_move ENDP
_TEXT ENDS
END
