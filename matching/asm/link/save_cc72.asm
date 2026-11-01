; Complete CC72..CED4/610; signed native frame coordinates and real FAR drivers retained.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _background:BYTE, _menu_state:BYTE, _dialog_text:BYTE
EXTRN _command_active:WORD, _pointer_x:WORD, _pointer_y:WORD
EXTRN _no_saved_games:BYTE, _dialog_actions_516c:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _close_dialog_d90e:NEAR
EXTRN _collect_saved_names_d2dd:NEAR
EXTRN _dialog_button_d92e:NEAR
EXTRN _dialog_hit_d840:NEAR
EXTRN _dispatch_8d73:NEAR
EXTRN _draw_saved_game_rows_d365:NEAR
EXTRN _highlight_game_d66c:NEAR
EXTRN _init_surface:NEAR
EXTRN _next_dialog_event_d766:NEAR
EXTRN _next_dialog_row_db3d:NEAR
EXTRN _prepare_dialog_d2cc:NEAR
EXTRN _previous_dialog_row_db65:NEAR
EXTRN _prompt_1296:NEAR
EXTRN _read_saved_games:NEAR
EXTRN _reset_df71:NEAR
EXTRN _reset_display_0865:NEAR
EXTRN _reset_graphics_3e4f:NEAR
EXTRN _restore_ui_92ab:NEAR
EXTRN _select_mode:NEAR
EXTRN _ticks_ea5b:NEAR
EXTRN _graphics_begin:FAR, _graphics_end:FAR, _update_pointer_11ef_0030:FAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _save_cc72
_save_cc72 PROC NEAR
    PUSH BP ; native CC72
    MOV BP, SP ; native CC73
    SUB SP, 0292h ; native CC75
    PUSH SI ; native CC79
    MOV word ptr [BP-08Ch], 00h ; native CC7A
    MOV word ptr [BP-0292h], 0FFFFh ; native CC80
    SUB AX, AX ; native CC86
    MOV word ptr [BP-08Eh], AX ; native CC88
    MOV word ptr [BP-090h], AX ; native CC8C
    MOV AL, _background ; native CC90
    MOV _dialog_text, AL ; native CC93
    MOV AL, _menu_state ; native CC96
    MOV _dialog_text+1, AL ; native CC99
    LEA AX, [BP-0290h] ; native CC9C
    PUSH AX ; native CCA0
    CALL NEAR PTR _read_saved_games ; native CCA1
    ADD SP, 02h ; native CCA4
    OR AX, AX ; native CCA7
    JNZ SHORT code_ccbf ; native CCA9
    SUB AX, AX ; native CCAB
    PUSH AX ; native CCAD
    MOV AX, 0Ch ; native CCAE
    PUSH AX ; native CCB1
    MOV AX, OFFSET DGROUP:_no_saved_games ; native CCB2
    PUSH AX ; native CCB5
    CALL NEAR PTR _prompt_1296 ; native CCB6
    ADD SP, 06h ; native CCB9
    JMP NEAR PTR code_cecf ; native CCBC
code_ccbf:
    LEA AX, [BP-0290h] ; native CCBF
    MOV word ptr [BP-02h], AX ; native CCC3
    MOV AX, 01h ; native CCC6
    PUSH AX ; native CCC9
    CALL NEAR PTR _select_mode ; native CCCA
    ADD SP, 02h ; native CCCD
    CALL FAR PTR _graphics_begin ; native CCD0
    CALL NEAR PTR _prepare_dialog_d2cc ; native CCD5
    LEA AX, [BP-082h] ; native CCD8
    PUSH AX ; native CCDC
    PUSH word ptr [BP-02h] ; native CCDD
    CALL NEAR PTR _collect_saved_names_d2dd ; native CCE0
    ADD SP, 04h ; native CCE3
    MOV AX, OFFSET DGROUP:_dialog_actions_516c ; native CCE6
    PUSH AX ; native CCE9
    LEA AX, [BP-082h] ; native CCEA
    PUSH AX ; native CCEE
    CALL NEAR PTR _draw_saved_game_rows_d365 ; native CCEF
    ADD SP, 04h ; native CCF2
    LEA AX, [BP-082h] ; native CCF5
    PUSH AX ; native CCF9
    PUSH word ptr [BP-08Ch] ; native CCFA
    CALL NEAR PTR _highlight_game_d66c ; native CCFE
    ADD SP, 04h ; native CD01
    CALL FAR PTR _graphics_end ; native CD04
code_cd09:
    CALL NEAR PTR _next_dialog_event_d766 ; native CD09
    MOV word ptr [BP-088h], AX ; native CD0C
    MOV BX, AX ; native CD10
    CMP word ptr [BX], 07h ; native CD12
    JNZ SHORT code_cd5c ; native CD15
    CMP word ptr [BX + 02h], 00h ; native CD17
    JNZ SHORT code_cd5c ; native CD1B
    MOV AX, word ptr [BX + 04h] ; native CD1D
    CMP AX, 080h ; native CD20
    JZ SHORT code_cd4e ; native CD23
    CMP AX, 081h ; native CD25
    JNZ SHORT code_cd09 ; native CD28
    PUSH word ptr [BP-08Ch] ; native CD2A
    LEA AX, [BP-082h] ; native CD2E
    PUSH AX ; native CD32
    CALL NEAR PTR _next_dialog_row_db3d ; native CD33
code_cd36:
    ADD SP, 04h ; native CD36
    MOV word ptr [BP-08Ch], AX ; native CD39
    LEA AX, [BP-082h] ; native CD3D
    PUSH AX ; native CD41
    PUSH word ptr [BP-08Ch] ; native CD42
    CALL NEAR PTR _highlight_game_d66c ; native CD46
    ADD SP, 04h ; native CD49
    JMP SHORT code_cd09 ; native CD4C
code_cd4e:
    PUSH word ptr [BP-08Ch] ; native CD4E
    LEA AX, [BP-082h] ; native CD52
    PUSH AX ; native CD56
    CALL NEAR PTR _previous_dialog_row_db65 ; native CD57
    JMP SHORT code_cd36 ; native CD5A
code_cd5c:
    MOV BX, word ptr [BP-088h] ; native CD5C
    CMP word ptr [BX], 06h ; native CD60
    JNZ SHORT code_cddc ; native CD63
    CMP word ptr [BX + 02h], 00h ; native CD65
    JNZ SHORT code_cddc ; native CD69
    MOV AX, word ptr [BX + 04h] ; native CD6B
    CMP AX, 0Dh ; native CD6E
    JZ SHORT code_cd80 ; native CD71
    CMP AX, 01Bh ; native CD73
    JNZ SHORT code_cd7b ; native CD76
    JMP NEAR PTR code_cec2 ; native CD78
code_cd7b:
    CMP AX, 020h ; native CD7B
    JNZ SHORT code_cd09 ; native CD7E
code_cd80:
    CALL FAR PTR _graphics_begin ; native CD80
    CALL NEAR PTR _close_dialog_d90e ; native CD85
    MOV SI, word ptr [BP-08Ch] ; native CD88
    MOV CL, 04h ; native CD8C
    SHL SI, CL ; native CD8E
    MOV AL, byte ptr [BP+SI-073h] ; native CD90
    SUB AH, AH ; native CD93
    MOV word ptr [BP-08Ch], AX ; native CD95
    MOV AX, 030h ; native CD99
    IMUL word ptr [BP-08Ch] ; native CD9C
    ADD AX, word ptr [BP-02h] ; native CDA0
    ADD AX, 01Fh ; native CDA3
    PUSH AX ; native CDA6
    CALL NEAR PTR _dispatch_8d73 ; native CDA7
    ADD SP, 02h ; native CDAA
    CALL NEAR PTR _reset_df71 ; native CDAD
    MOV AX, _command_active ; native CDB0
    MOV word ptr [BP-08Ah], AX ; native CDB3
    PUSH word ptr [BP-08Ch] ; native CDB7
    PUSH word ptr [BP-02h] ; native CDBB
    CALL NEAR PTR _restore_ui_92ab ; native CDBE
    ADD SP, 04h ; native CDC1
    MOV AX, _command_active ; native CDC4
    CMP word ptr [BP-08Ah], AX ; native CDC7
    JNZ SHORT code_cdd0 ; native CDCB
    JMP NEAR PTR code_ceca ; native CDCD
code_cdd0:
    CALL NEAR PTR _init_surface ; native CDD0
    CALL NEAR PTR _reset_graphics_3e4f ; native CDD3
    CALL NEAR PTR _reset_display_0865 ; native CDD6
    JMP NEAR PTR code_ceca ; native CDD9
code_cddc:
    MOV BX, word ptr [BP-088h] ; native CDDC
    MOV AX, word ptr [BX] ; native CDE0
    CMP AX, 04h ; native CDE2
    JZ SHORT code_cdf2 ; native CDE5
    CMP AX, 05h ; native CDE7
    JNZ SHORT code_cdef ; native CDEA
    JMP NEAR PTR code_ceaa ; native CDEC
code_cdef:
    JMP NEAR PTR code_cd09 ; native CDEF
code_cdf2:
    CMP word ptr [BX + 04h], 01h ; native CDF2
    JZ SHORT code_cdfb ; native CDF6
    JMP NEAR PTR code_cd09 ; native CDF8
code_cdfb:
    CALL NEAR PTR _ticks_ea5b ; native CDFB
    CWD ; native CDFE
    MOV word ptr [BP-086h], AX ; native CDFF
    MOV word ptr [BP-084h], DX ; native CE03
    SUB AX, AX ; native CE07
    PUSH AX ; native CE09
    PUSH word ptr _pointer_y ; native CE0A
    PUSH word ptr _pointer_x ; native CE0E
    CALL NEAR PTR _dialog_hit_d840 ; native CE12
    ADD SP, 06h ; native CE15
    MOV word ptr [BP-08Ah], AX ; native CE18
    CMP AX, 07h ; native CE1C
    JG SHORT code_ce42 ; native CE1F
    MOV SI, AX ; native CE21
    MOV CL, 04h ; native CE23
    SHL SI, CL ; native CE25
    CMP byte ptr [BP+SI-073h], 0FFh ; native CE27
    JZ SHORT code_ce5a ; native CE2B
    MOV word ptr [BP-08Ch], AX ; native CE2D
    LEA AX, [BP-082h] ; native CE31
    PUSH AX ; native CE35
    PUSH word ptr [BP-08Ch] ; native CE36
    CALL NEAR PTR _highlight_game_d66c ; native CE3A
    ADD SP, 04h ; native CE3D
    JMP SHORT code_ce5a ; native CE40
code_ce42:
    CMP word ptr [BP-08Ah], 08h ; native CE42
    JNZ SHORT code_ce5a ; native CE47
    SUB AX, AX ; native CE49
    PUSH AX ; native CE4B
    PUSH word ptr [BP-08Ah] ; native CE4C
    CALL NEAR PTR _dialog_button_d92e ; native CE50
    ADD SP, 04h ; native CE53
    OR AX, AX ; native CE56
    JNZ SHORT code_cec2 ; native CE58
code_ce5a:
    MOV AX, word ptr [BP-08Ch] ; native CE5A
    CMP word ptr [BP-08Ah], AX ; native CE5E
    JZ SHORT code_ce67 ; native CE62
    JMP NEAR PTR code_cd09 ; native CE64
code_ce67:
    MOV AX, word ptr [BP-086h] ; native CE67
    MOV DX, word ptr [BP-084h] ; native CE6B
    SUB AX, word ptr [BP-090h] ; native CE6F
    SBB DX, word ptr [BP-08Eh] ; native CE73
    OR DX, DX ; native CE77
    JNZ SHORT code_ce8f ; native CE79
    JC SHORT code_ce82 ; native CE7B
    CMP AX, 0Ah ; native CE7D
    JNC SHORT code_ce8f ; native CE80
code_ce82:
    MOV AX, word ptr [BP-08Ch] ; native CE82
    CMP word ptr [BP-0292h], AX ; native CE86
    JNZ SHORT code_ce8f ; native CE8A
    JMP NEAR PTR code_cd80 ; native CE8C
code_ce8f:
    MOV AX, word ptr [BP-086h] ; native CE8F
    MOV DX, word ptr [BP-084h] ; native CE93
    MOV word ptr [BP-090h], AX ; native CE97
    MOV word ptr [BP-08Eh], DX ; native CE9B
    MOV AX, word ptr [BP-08Ch] ; native CE9F
    MOV word ptr [BP-0292h], AX ; native CEA3
    JMP NEAR PTR code_cd09 ; native CEA7
code_ceaa:
    MOV BX, word ptr [BP-088h] ; native CEAA
    MOV AX, word ptr [BX + 08h] ; native CEAE
    MOV _pointer_x, AX ; native CEB1
    MOV AX, word ptr [BX + 0Ah] ; native CEB4
    MOV _pointer_y, AX ; native CEB7
    CALL FAR PTR _update_pointer_11ef_0030 ; native CEBA
    JMP NEAR PTR code_cd09 ; native CEBF
code_cec2:
    CALL FAR PTR _graphics_begin ; native CEC2
    CALL NEAR PTR _close_dialog_d90e ; native CEC7
code_ceca:
    CALL FAR PTR _graphics_end ; native CECA
code_cecf:
    POP SI ; native CECF
    MOV SP, BP ; native CED0
    POP BP ; native CED2
    RET ; native CED3
_save_cc72 ENDP
_TEXT ENDS
END
