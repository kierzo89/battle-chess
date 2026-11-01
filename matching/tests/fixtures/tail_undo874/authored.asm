; Complete native77AF..78F6/327. Genuine machine frame18, not a C-source proof.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _cells:BYTE, _actor_map:BYTE, _kind_map:BYTE, _actors:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _detach_actor:NEAR, _queue_piece:NEAR
_TEXT SEGMENT BYTE PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _undo_animation
_undo_animation PROC NEAR
    PUSH BP ; native 77AF
    MOV BP, SP ; native 77B0
    MOV AX, 012h ; native 77B2
    CALL NEAR PTR __chkstk ; native 77B5
    PUSH DI ; native 77B8
    PUSH SI ; native 77B9
    MOV SI, word ptr [BP + 04h] ; native 77BA
    CMP word ptr [SI + 04h], 00h ; native 77BD
    JZ SHORT code_7831 ; native 77C1
    CMP byte ptr [SI + 06h], 01h ; native 77C3
    JNZ SHORT code_7831 ; native 77C7
    MOV AX, word ptr [SI] ; native 77C9
    MOV word ptr [BP-012h], AX ; native 77CB
    MOV AX, word ptr [SI + 02h] ; native 77CE
    MOV word ptr [BP-010h], AX ; native 77D1
    MOV word ptr [BP-0Eh], 00h ; native 77D4
    MOV AL, byte ptr [SI + 06h] ; native 77D9
    MOV byte ptr [BP-0Ch], AL ; native 77DC
    MOV byte ptr [BP-0Bh], 00h ; native 77DF
    LEA AX, [BP-012h] ; native 77E3
    PUSH AX ; native 77E6
    CALL NEAR PTR _undo_animation ; native 77E7
    ADD SP, 02h ; native 77EA
    MOV AL, byte ptr [SI] ; native 77ED
    AND AL, 07h ; native 77EF
    CMP AL, 06h ; native 77F1
    JNZ SHORT code_780c ; native 77F3
    MOV AX, word ptr [SI] ; native 77F5
    AND AX, 0F0h ; native 77F7
    OR AL, 05h ; native 77FA
    MOV word ptr [BP-012h], AX ; native 77FC
    MOV AX, word ptr [SI + 02h] ; native 77FF
    AND AX, 0F0h ; native 7802
    OR AL, 07h ; native 7805
    MOV word ptr [BP-010h], AX ; native 7807
    JMP SHORT code_781f ; native 780A
code_780c:
    MOV AX, word ptr [SI] ; native 780C
    AND AX, 0F0h ; native 780E
    OR AL, 03h ; native 7811
    MOV word ptr [BP-012h], AX ; native 7813
    MOV AX, word ptr [SI + 02h] ; native 7816
    AND AX, 0F0h ; native 7819
    MOV word ptr [BP-010h], AX ; native 781C
code_781f:
    MOV byte ptr [BP-0Ch], 03h ; native 781F
    MOV byte ptr [BP-0Bh], 00h ; native 7823
    MOV word ptr [BP-0Eh], 00h ; native 7827
    LEA AX, [BP-012h] ; native 782C
    MOV SI, AX ; native 782F
code_7831:
    MOV AX, word ptr [SI + 02h] ; native 7831
    SAR AX, 01h ; native 7834
    AND AL, 038h ; native 7836
    XOR AL, 038h ; native 7838
    MOV CL, byte ptr [SI + 02h] ; native 783A
    AND CL, 07h ; native 783D
    OR AL, CL ; native 7840
    MOV byte ptr [BP-0Ah], AL ; native 7842
    MOV AX, word ptr [SI] ; native 7845
    SAR AX, 01h ; native 7847
    AND AL, 038h ; native 7849
    XOR AL, 038h ; native 784B
    MOV CL, byte ptr [SI] ; native 784D
    AND CL, 07h ; native 784F
    OR AL, CL ; native 7852
    MOV byte ptr [BP-08h], AL ; native 7854
    SUB AH, AH ; native 7857
    MOV DI, AX ; native 7859
    CMP byte ptr _cells[DI], AH ; native 785B
    JZ SHORT code_7871 ; native 785F
    MOV AL, 01Ch ; native 7861
    MUL byte ptr _actor_map[DI] ; native 7863
    ADD AX, OFFSET DGROUP:_actors ; native 7867
    PUSH AX ; native 786A
    CALL NEAR PTR _detach_actor ; native 786B
    ADD SP, 02h ; native 786E
code_7871:
    MOV BL, byte ptr [BP-0Ah] ; native 7871
    SUB BH, BH ; native 7874
    MOV AL, 01Ch ; native 7876
    MUL byte ptr _actor_map[BX] ; native 7878
    ADD AX, OFFSET DGROUP:_actors ; native 787C
    PUSH AX ; native 787F
    CALL NEAR PTR _detach_actor ; native 7880
    ADD SP, 02h ; native 7883
    MOV AL, byte ptr [BP-0Ah] ; native 7886
    SUB AH, AH ; native 7889
    MOV DI, AX ; native 788B
    MOV AL, byte ptr [BP-08h] ; native 788D
    PUSH AX ; native 7890
    MOV AL, byte ptr _actor_map[DI] ; native 7891
    PUSH AX ; native 7895
    MOV AL, byte ptr _cells[DI] ; native 7896
    AND AX, 040h ; native 789A
    PUSH AX ; native 789D
    MOV BL, byte ptr [SI + 06h] ; native 789E
    SUB BH, BH ; native 78A1
    MOV AL, byte ptr _kind_map[BX] ; native 78A3
    SUB AH, AH ; native 78A7
    PUSH AX ; native 78A9
    CALL NEAR PTR _queue_piece ; native 78AA
    ADD SP, 08h ; native 78AD
    MOV BL, byte ptr [BP-0Ah] ; native 78B0
    SUB BH, BH ; native 78B3
    MOV byte ptr _cells[BX], BH ; native 78B5
    CMP word ptr [SI + 04h], 00h ; native 78B9
    JZ SHORT code_78f0 ; native 78BD
    CMP byte ptr [SI + 06h], 06h ; native 78BF
    JNZ SHORT code_78f0 ; native 78C3
    MOV AL, byte ptr [BP-0Ah] ; native 78C5
    AND AL, 038h ; native 78C8
    MOV CL, byte ptr [BP-08h] ; native 78CA
    AND CL, 07h ; native 78CD
    OR AL, CL ; native 78D0
    MOV byte ptr [BP-0Ah], AL ; native 78D2
    MOV BL, AL ; native 78D5
    MOV AL, 01Ch ; native 78D7
    MUL byte ptr _actor_map[BX] ; native 78D9
    ADD AX, OFFSET DGROUP:_actors ; native 78DD
    PUSH AX ; native 78E0
    CALL NEAR PTR _detach_actor ; native 78E1
    ADD SP, 02h ; native 78E4
    MOV BL, byte ptr [BP-0Ah] ; native 78E7
    SUB BH, BH ; native 78EA
    MOV byte ptr _cells[BX], BH ; native 78EC
code_78f0:
    POP SI ; native 78F0
    POP DI ; native 78F1
    MOV SP, BP ; native 78F2
    POP BP ; native 78F4
    RET ; native 78F5
_undo_animation ENDP
_TEXT ENDS
END
