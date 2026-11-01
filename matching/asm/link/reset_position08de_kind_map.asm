; Physical08DE..0D6E/1168; Ghidra1166 live bytes plus explicit derived dead JMP0D39.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _actor_map:BYTE
EXTRN _actors:BYTE
EXTRN _alternate_menus_115e:BYTE
EXTRN _arena_cursor:BYTE
EXTRN _board:BYTE
EXTRN _board_input_0ef2:BYTE
EXTRN _cells:BYTE
EXTRN _clear_board_question_4c12:BYTE
EXTRN _command_active:BYTE
EXTRN _current_side:BYTE
EXTRN _cursor_actor_57d0:BYTE
EXTRN _cursor_colour_9850:BYTE
EXTRN _cursor_frames_820e:BYTE
EXTRN _cursor_kind_0ef4:BYTE
EXTRN _editor_piece_map_004c:BYTE
EXTRN _main_menus_114a:BYTE
EXTRN _menu_open_0044:BYTE
EXTRN _menus:BYTE
EXTRN _no_actor_message_4c00:BYTE
EXTRN _page_mode:BYTE
EXTRN _kind_map:BYTE
EXTRN _pointer_x:BYTE
EXTRN _pointer_y:BYTE
EXTRN _row_mask_9230:BYTE
EXTRN _screen_x:BYTE
EXTRN _screen_y:BYTE
EXTRN _selected_square_0efa:BYTE
EXTRN _waiting_0eee:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR
EXTRN _attach_actor:NEAR
EXTRN _detach_actor:NEAR
EXTRN _detach_all:NEAR
EXTRN _init_surface:NEAR
EXTRN _obtain_input:NEAR
EXTRN _prompt_1296:NEAR
EXTRN _refresh_panel_1d51:NEAR
EXTRN _reset_df71:NEAR
EXTRN _reset_display_0865:NEAR
EXTRN _reset_graphics_3e4f:NEAR
EXTRN _show_error_0d6e:NEAR
EXTRN _validate_editor_8e36:NEAR
EXTRN _draw_fce8:FAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _reset_position_08de
_reset_position_08de PROC NEAR
    PUSH BP ; native 08DE
    MOV BP, SP ; native 08DF
    MOV AX, 018h ; native 08E1
    CALL NEAR PTR __chkstk ; native 08E4
    PUSH DI ; native 08E7
    PUSH SI ; native 08E8
    MOV WORD PTR _board_input_0ef2, 01h ; native 08E9
    MOV WORD PTR _menus, OFFSET DGROUP:_alternate_menus_115e ; native 08EF
    MOV AX, WORD PTR _command_active ; native 08F5
    MOV WORD PTR [BP-0Ch], AX ; native 08F8
    MOV AX, WORD PTR _waiting_0eee ; native 08FB
    MOV WORD PTR [BP-0Eh], AX ; native 08FE
    CMP WORD PTR _command_active, 00h ; native 0901
    JNZ SHORT code_0911 ; native 0906
    MOV WORD PTR _command_active, 01h ; native 0908
    CALL NEAR PTR _init_surface ; native 090E
code_0911:
    CALL NEAR PTR _refresh_panel_1d51 ; native 0911
    MOV BYTE PTR _page_mode, 01h ; native 0914
    MOV BYTE PTR _actors+907, 00h ; native 0919
    MOV WORD PTR [BP-010h], 00h ; native 091E
    JMP SHORT code_0928 ; native 0923
code_0925:
    INC WORD PTR [BP-010h] ; native 0925
code_0928:
    CMP WORD PTR [BP-010h], 06h ; native 0928
    JGE SHORT code_0993 ; native 092C
    MOV WORD PTR _actors+916, 00h ; native 092E
    MOV AX, OFFSET DGROUP:_actors+896 ; native 0934
    PUSH AX ; native 0937
    MOV BX, WORD PTR [BP-010h] ; native 0938
    MOV AL, BYTE PTR _kind_map+1[BX] ; native 093B
    SUB AH, AH ; native 093F
    MOV CL, 03h ; native 0941
    SHL AX, CL ; native 0943
    ADD AX, OFFSET DGROUP:_cursor_frames_820e ; native 0945
    PUSH AX ; native 0948
    SUB AX, AX ; native 0949
    PUSH AX ; native 094B
    MOV AX, 018h ; native 094C
    IMUL BX ; native 094F
    ADD AX, 010h ; native 0951
    PUSH AX ; native 0954
    MOV AX, 010h ; native 0955
    PUSH AX ; native 0958
    CALL NEAR PTR _attach_actor ; native 0959
    ADD SP, 0Ah ; native 095C
    MOV WORD PTR _actors+916, 00h ; native 095F
    MOV AX, OFFSET DGROUP:_actors+896 ; native 0965
    PUSH AX ; native 0968
    MOV BX, WORD PTR [BP-010h] ; native 0969
    MOV AL, BYTE PTR _kind_map+1[BX] ; native 096C
    SUB AH, AH ; native 0970
    MOV CL, 03h ; native 0972
    SHL AX, CL ; native 0974
    ADD AX, OFFSET DGROUP:_cursor_frames_820e ; native 0976
    PUSH AX ; native 0979
    MOV AX, 01h ; native 097A
    PUSH AX ; native 097D
    MOV AX, 018h ; native 097E
    IMUL BX ; native 0981
    ADD AX, 010h ; native 0983
    PUSH AX ; native 0986
    MOV AX, 0130h ; native 0987
    PUSH AX ; native 098A
    CALL NEAR PTR _attach_actor ; native 098B
    ADD SP, 0Ah ; native 098E
    JMP SHORT code_0925 ; native 0991
code_0993:
    MOV BYTE PTR _page_mode, 00h ; native 0993
    MOV AX, OFFSET DGROUP:_actors+896 ; native 0998
    PUSH AX ; native 099B
    CALL NEAR PTR _detach_actor ; native 099C
    ADD SP, 02h ; native 099F
    CALL NEAR PTR _reset_graphics_3e4f ; native 09A2
    CALL NEAR PTR _reset_display_0865 ; native 09A5
    MOV WORD PTR [BP-010h], 00h ; native 09A8
    JMP SHORT code_09ba ; native 09AD
code_09af:
    MOV BX, WORD PTR [BP-010h] ; native 09AF
    INC WORD PTR [BP-010h] ; native 09B2
    MOV BYTE PTR _row_mask_9230[BX], 0FFh ; native 09B5
code_09ba:
    CMP WORD PTR [BP-010h], 08h ; native 09BA
    JGE SHORT code_09c2 ; native 09BE
    JMP SHORT code_09af ; native 09C0
code_09c2:
    MOV AX, WORD PTR _arena_cursor ; native 09C2
    MOV DX, WORD PTR _arena_cursor+2 ; native 09C5
    MOV WORD PTR [BP-04h], AX ; native 09C9
    MOV WORD PTR [BP-02h], DX ; native 09CC
    MOV AX, OFFSET DGROUP:_board ; native 09CF
    MOV WORD PTR [BP-0Ah], AX ; native 09D2
    MOV WORD PTR [BP-08h], DS ; native 09D5
    MOV WORD PTR [BP-010h], 00h ; native 09D8
    JMP SHORT code_09e2 ; native 09DD
code_09df:
    INC WORD PTR [BP-010h] ; native 09DF
code_09e2:
    CMP WORD PTR [BP-010h], 01E0h ; native 09E2
    JGE SHORT code_0a0d ; native 09E7
    LES BX, DWORD PTR [BP-0Ah] ; native 09E9
    ADD WORD PTR [BP-0Ah], 01h ; native 09EC
    JNC SHORT code_09f7 ; native 09F0
    ADD WORD PTR [BP-08h], 01000h ; native 09F2
code_09f7:
    MOV AL, BYTE PTR ES:[BX] ; native 09F7
    LES BX, DWORD PTR [BP-04h] ; native 09FA
    ADD WORD PTR [BP-04h], 01h ; native 09FD
    JNC SHORT code_0a08 ; native 0A01
    ADD WORD PTR [BP-02h], 01000h ; native 0A03
code_0a08:
    MOV BYTE PTR ES:[BX], AL ; native 0A08
    JMP SHORT code_09df ; native 0A0B
code_0a0d:
    MOV BYTE PTR _menu_open_0044, 01h ; native 0A0D
    CALL NEAR PTR _obtain_input ; native 0A12
    MOV WORD PTR [BP-06h], AX ; native 0A15
    OR AX, AX ; native 0A18
    JZ SHORT code_0a0d ; native 0A1A
    JMP NEAR PTR code_0d3b ; native 0A1C
code_0a1f:
    MOV AX, WORD PTR _selected_square_0efa ; native 0A1F
    SHL AX, 01h ; native 0A22
    AND AX, 070h ; native 0A24
    XOR AL, 070h ; native 0A27
    MOV CX, WORD PTR _selected_square_0efa ; native 0A29
    AND CX, FULLWORD_IMMEDIATE_ZERO + 07h ; native 0A2D
    OR AX, CX ; native 0A31
    MOV WORD PTR [BP-012h], AX ; native 0A33
    CMP WORD PTR _cursor_kind_0ef4, 00h ; native 0A36
    JNZ SHORT code_0a40 ; native 0A3B
    JMP NEAR PTR code_0af5 ; native 0A3D
code_0a40:
    MOV BX, WORD PTR _selected_square_0efa ; native 0A40
    CMP BYTE PTR _cells[BX], 00h ; native 0A44
    JZ SHORT code_0a5b ; native 0A49
    MOV AL, 01Ch ; native 0A4B
    MUL BYTE PTR _actor_map[BX] ; native 0A4D
    ADD AX, OFFSET DGROUP:_actors ; native 0A51
    PUSH AX ; native 0A54
    CALL NEAR PTR _detach_actor ; native 0A55
    ADD SP, 02h ; native 0A58
code_0a5b:
    MOV AX, 01Ch ; native 0A5B
    IMUL WORD PTR _cursor_actor_57d0 ; native 0A5E
    MOV SI, AX ; native 0A62
    CMP WORD PTR [SI + 05F4h], 00h ; native 0A64
    JZ SHORT code_0a75 ; native 0A69
    ADD AX, OFFSET DGROUP:_actors ; native 0A6B
    PUSH AX ; native 0A6E
    CALL NEAR PTR _detach_actor ; native 0A6F
    ADD SP, 02h ; native 0A72
code_0a75:
    MOV AX, 01Ch ; native 0A75
    IMUL WORD PTR _cursor_actor_57d0 ; native 0A78
    ADD AX, OFFSET DGROUP:_actors ; native 0A7C
    PUSH AX ; native 0A7F
    MOV AX, WORD PTR _cursor_kind_0ef4 ; native 0A80
    MOV CL, 03h ; native 0A83
    SHL AX, CL ; native 0A85
    ADD AX, OFFSET DGROUP:_cursor_frames_820e ; native 0A87
    PUSH AX ; native 0A8A
    PUSH WORD PTR _cursor_colour_9850 ; native 0A8B
    MOV BX, WORD PTR _selected_square_0efa ; native 0A8F
    SAR BX, CL ; native 0A93
    SHL BX, 01h ; native 0A95
    MOV DI, WORD PTR _screen_y ; native 0A97
    PUSH WORD PTR [BX + DI] ; native 0A9B
    MOV BX, WORD PTR _selected_square_0efa ; native 0A9D
    SHL BX, 01h ; native 0AA1
    MOV DI, WORD PTR _screen_x ; native 0AA3
    PUSH WORD PTR [BX + DI] ; native 0AA7
    CALL NEAR PTR _attach_actor ; native 0AA9
    ADD SP, 0Ah ; native 0AAC
    MOV BX, WORD PTR _selected_square_0efa ; native 0AAF
    MOV AL, BYTE PTR _cursor_colour_9850 ; native 0AB3
    MOV CL, 06h ; native 0AB6
    SHL AL, CL ; native 0AB8
    OR AL, BYTE PTR _cursor_kind_0ef4 ; native 0ABA
    MOV BYTE PTR _cells[BX], AL ; native 0ABE
    MOV BX, WORD PTR _selected_square_0efa ; native 0AC2
    MOV AL, BYTE PTR _cursor_actor_57d0 ; native 0AC6
    MOV BYTE PTR _actor_map[BX], AL ; native 0AC9
    MOV SI, WORD PTR [BP-012h] ; native 0ACD
    MOV CL, 02h ; native 0AD0
    SHL SI, CL ; native 0AD2
    CMP WORD PTR _cursor_colour_9850, 01h ; native 0AD4
    SBB AX, AX ; native 0AD9
    NEG AX ; native 0ADB
    MOV BYTE PTR [SI + 0A8BBh], AL ; native 0ADD
    MOV BX, WORD PTR _cursor_kind_0ef4 ; native 0AE1
    MOV AL, BYTE PTR _editor_piece_map_004c[BX] ; native 0AE5
    MOV BYTE PTR [SI + 0A8BAh], AL ; native 0AE9
    MOV WORD PTR _cursor_kind_0ef4, 00h ; native 0AED
    JMP SHORT code_0b2f ; native 0AF3
code_0af5:
    MOV BX, WORD PTR _selected_square_0efa ; native 0AF5
    CMP BYTE PTR _cells[BX], 00h ; native 0AF9
    JZ SHORT code_0b2f ; native 0AFE
    MOV AL, BYTE PTR _cells[BX] ; native 0B00
    SUB AH, AH ; native 0B04
    MOV SI, AX ; native 0B06
    AND AX, 07h ; native 0B08
    MOV WORD PTR _cursor_kind_0ef4, AX ; native 0B0B
    MOV AX, SI ; native 0B0E
    MOV CL, 06h ; native 0B10
    SHR AX, CL ; native 0B12
    MOV WORD PTR _cursor_colour_9850, AX ; native 0B14
    MOV AL, BYTE PTR _actor_map[BX] ; native 0B17
    SUB AH, AH ; native 0B1B
    MOV WORD PTR _cursor_actor_57d0, AX ; native 0B1D
    MOV BYTE PTR _cells[BX], AH ; native 0B20
    MOV BX, WORD PTR [BP-012h] ; native 0B24
    SHL BX, 01h ; native 0B27
    SHL BX, 01h ; native 0B29
    MOV BYTE PTR _board[BX], AH ; native 0B2B
code_0b2f:
    JMP NEAR PTR code_0d65 ; native 0B2F
code_0b32:
    CMP WORD PTR _cursor_kind_0ef4, 00h ; native 0B32
    JZ SHORT code_0b59 ; native 0B37
    MOV AX, 01Ch ; native 0B39
    IMUL WORD PTR _cursor_actor_57d0 ; native 0B3C
    MOV SI, AX ; native 0B40
    CMP WORD PTR [SI + 05F4h], 00h ; native 0B42
    JZ SHORT code_0b59 ; native 0B47
    ADD AX, OFFSET DGROUP:_actors ; native 0B49
    PUSH AX ; native 0B4C
    CALL NEAR PTR _detach_actor ; native 0B4D
    ADD SP, 02h ; native 0B50
    MOV WORD PTR _cursor_kind_0ef4, 00h ; native 0B53
code_0b59:
    MOV AX, WORD PTR _pointer_y ; native 0B59
    SUB AX, 04h ; native 0B5C
    CWD ; native 0B5F
    MOV CX, 018h ; native 0B60
    IDIV CX ; native 0B63
    MOV WORD PTR [BP-012h], AX ; native 0B65
    OR AX, AX ; native 0B68
    JL SHORT code_0bb4 ; native 0B6A
    CMP AX, 05h ; native 0B6C
    JG SHORT code_0bb4 ; native 0B6F
    CMP WORD PTR _pointer_x, 019h ; native 0B71
    JGE SHORT code_0b92 ; native 0B76
    CMP WORD PTR _pointer_x, 07h ; native 0B78
    JLE SHORT code_0b92 ; native 0B7D
    MOV BX, AX ; native 0B7F
    MOV AL, BYTE PTR _kind_map+1[BX] ; native 0B81
    SUB AH, AH ; native 0B85
    MOV WORD PTR _cursor_kind_0ef4, AX ; native 0B87
    MOV WORD PTR _cursor_colour_9850, 00h ; native 0B8A
    JMP SHORT code_0bb4 ; native 0B90
code_0b92:
    CMP WORD PTR _pointer_x, 0127h ; native 0B92
    JLE SHORT code_0bb4 ; native 0B98
    CMP WORD PTR _pointer_x, 0139h ; native 0B9A
    JGE SHORT code_0bb4 ; native 0BA0
    MOV BX, WORD PTR [BP-012h] ; native 0BA2
    MOV AL, BYTE PTR _kind_map+1[BX] ; native 0BA5
    SUB AH, AH ; native 0BA9
    MOV WORD PTR _cursor_kind_0ef4, AX ; native 0BAB
    MOV WORD PTR _cursor_colour_9850, 01h ; native 0BAE
code_0bb4:
    CMP WORD PTR _cursor_kind_0ef4, 00h ; native 0BB4
    JZ SHORT code_0c25 ; native 0BB9
    MOV WORD PTR [BP-012h], 00h ; native 0BBB
    JMP SHORT code_0bc5 ; native 0BC0
code_0bc2:
    INC WORD PTR [BP-012h] ; native 0BC2
code_0bc5:
    CMP WORD PTR [BP-012h], 020h ; native 0BC5
    JGE SHORT code_0bdc ; native 0BC9
    MOV AX, 01Ch ; native 0BCB
    IMUL WORD PTR [BP-012h] ; native 0BCE
    MOV BX, AX ; native 0BD1
    CMP WORD PTR _actors+20[BX], 00h ; native 0BD3
    JZ SHORT code_0bdc ; native 0BD8
    JMP SHORT code_0bc2 ; native 0BDA
code_0bdc:
    CMP WORD PTR [BP-012h], 020h ; native 0BDC
    JNZ SHORT code_0bf4 ; native 0BE0
    MOV WORD PTR _cursor_kind_0ef4, 00h ; native 0BE2
    MOV AX, OFFSET DGROUP:_no_actor_message_4c00 ; native 0BE8
    PUSH AX ; native 0BEB
    CALL NEAR PTR _show_error_0d6e ; native 0BEC
    ADD SP, 02h ; native 0BEF
    JMP SHORT code_0c25 ; native 0BF2
code_0bf4:
    MOV AX, WORD PTR [BP-012h] ; native 0BF4
    MOV WORD PTR _cursor_actor_57d0, AX ; native 0BF7
    MOV AX, 01Ch ; native 0BFA
    IMUL WORD PTR _cursor_actor_57d0 ; native 0BFD
    ADD AX, OFFSET DGROUP:_actors ; native 0C01
    PUSH AX ; native 0C04
    MOV AX, WORD PTR _cursor_kind_0ef4 ; native 0C05
    MOV CL, 03h ; native 0C08
    SHL AX, CL ; native 0C0A
    ADD AX, OFFSET DGROUP:_cursor_frames_820e ; native 0C0C
    PUSH AX ; native 0C0F
    PUSH WORD PTR _cursor_colour_9850 ; native 0C10
    MOV AX, WORD PTR _pointer_y ; native 0C14
    ADD AX, 0C8h ; native 0C17
    PUSH AX ; native 0C1A
    PUSH WORD PTR _pointer_x ; native 0C1B
    CALL NEAR PTR _attach_actor ; native 0C1F
    ADD SP, 0Ah ; native 0C22
code_0c25:
    JMP NEAR PTR code_0d65 ; native 0C25
code_0c28:
    MOV AX, 01h ; native 0C28
    PUSH AX ; native 0C2B
    MOV AX, 0Ch ; native 0C2C
    PUSH AX ; native 0C2F
    MOV AX, OFFSET DGROUP:_clear_board_question_4c12 ; native 0C30
    PUSH AX ; native 0C33
    CALL NEAR PTR _prompt_1296 ; native 0C34
    ADD SP, 06h ; native 0C37
    CMP AX, 01003h ; native 0C3A
    JNZ SHORT code_0c7d ; native 0C3D
    CALL NEAR PTR _detach_all ; native 0C3F
    MOV WORD PTR [BP-010h], 00h ; native 0C42
    JMP SHORT code_0c4c ; native 0C47
code_0c49:
    INC WORD PTR [BP-010h] ; native 0C49
code_0c4c:
    CMP WORD PTR [BP-010h], 040h ; native 0C4C
    JGE SHORT code_0c7d ; native 0C50
    MOV BX, WORD PTR [BP-010h] ; native 0C52
    MOV BYTE PTR _cells[BX], 00h ; native 0C55
    MOV AX, WORD PTR [BP-010h] ; native 0C5A
    SHL AX, 01h ; native 0C5D
    AND AX, 070h ; native 0C5F
    XOR AL, 070h ; native 0C62
    MOV CX, WORD PTR [BP-010h] ; native 0C64
    AND CX, FULLWORD_IMMEDIATE_ZERO + 07h ; native 0C67
    OR AX, CX ; native 0C6B
    MOV WORD PTR [BP-014h], AX ; native 0C6D
    MOV BX, AX ; native 0C70
    SHL BX, 01h ; native 0C72
    SHL BX, 01h ; native 0C74
    MOV BYTE PTR _board[BX], 00h ; native 0C76
    JMP SHORT code_0c49 ; native 0C7B
code_0c7d:
    JMP NEAR PTR code_0d65 ; native 0C7D
code_0c80:
    MOV AX, WORD PTR _arena_cursor ; native 0C80
    MOV DX, WORD PTR _arena_cursor+2 ; native 0C83
    MOV WORD PTR [BP-04h], AX ; native 0C87
    MOV WORD PTR [BP-02h], DX ; native 0C8A
    MOV AX, OFFSET DGROUP:_board ; native 0C8D
    MOV WORD PTR [BP-0Ah], AX ; native 0C90
    MOV WORD PTR [BP-08h], DS ; native 0C93
    MOV WORD PTR [BP-010h], 00h ; native 0C96
    JMP SHORT code_0ca0 ; native 0C9B
code_0c9d:
    INC WORD PTR [BP-010h] ; native 0C9D
code_0ca0:
    CMP WORD PTR [BP-010h], 01E0h ; native 0CA0
    JGE SHORT code_0ccb ; native 0CA5
    LES BX, DWORD PTR [BP-04h] ; native 0CA7
    ADD WORD PTR [BP-04h], 01h ; native 0CAA
    JNC SHORT code_0cb5 ; native 0CAE
    ADD WORD PTR [BP-02h], 01000h ; native 0CB0
code_0cb5:
    MOV AL, BYTE PTR ES:[BX] ; native 0CB5
    LES BX, DWORD PTR [BP-0Ah] ; native 0CB8
    ADD WORD PTR [BP-0Ah], 01h ; native 0CBB
    JNC SHORT code_0cc6 ; native 0CBF
    ADD WORD PTR [BP-08h], 01000h ; native 0CC1
code_0cc6:
    MOV BYTE PTR ES:[BX], AL ; native 0CC6
    JMP SHORT code_0c9d ; native 0CC9
code_0ccb:
    CALL NEAR PTR _detach_all ; native 0CCB
    MOV WORD PTR _cursor_kind_0ef4, 00h ; native 0CCE
    CALL NEAR PTR _reset_display_0865 ; native 0CD4
    JMP NEAR PTR code_0d65 ; native 0CD7
code_0cda:
    CALL NEAR PTR _validate_editor_8e36 ; native 0CDA
    MOV WORD PTR [BP-018h], AX ; native 0CDD
    OR AX, AX ; native 0CE0
    JZ SHORT code_0cf3 ; native 0CE2
    MOV WORD PTR _cursor_kind_0ef4, 00h ; native 0CE4
    PUSH AX ; native 0CEA
    CALL NEAR PTR _show_error_0d6e ; native 0CEB
    ADD SP, 02h ; native 0CEE
    JMP SHORT code_0d37 ; native 0CF1
code_0cf3:
    MOV WORD PTR _menus, OFFSET DGROUP:_main_menus_114a ; native 0CF3
    MOV WORD PTR _cursor_kind_0ef4, 00h ; native 0CF9
    MOV WORD PTR _board_input_0ef2, 00h ; native 0CFF
    MOV AX, WORD PTR [BP-0Ch] ; native 0D05
    MOV WORD PTR _command_active, AX ; native 0D08
    MOV AX, WORD PTR [BP-0Eh] ; native 0D0B
    MOV WORD PTR _waiting_0eee, AX ; native 0D0E
    CALL NEAR PTR _init_surface ; native 0D11
    CALL NEAR PTR _reset_graphics_3e4f ; native 0D14
    CALL NEAR PTR _reset_display_0865 ; native 0D17
    CALL NEAR PTR _reset_df71 ; native 0D1A
    CMP WORD PTR _waiting_0eee, 00h ; native 0D1D
    JZ SHORT code_0d30 ; native 0D22
    PUSH WORD PTR _current_side ; native 0D24
    CALL FAR PTR _draw_fce8 ; native 0D28
    ADD SP, 02h ; native 0D2D
code_0d30:
    MOV BYTE PTR _menu_open_0044, 00h ; native 0D30
    JMP SHORT code_0d68 ; native 0D35
code_0d37:
    JMP SHORT code_0d65 ; native 0D37
    JMP SHORT code_0d65 ; native 0D39
code_0d3b:
    CMP AX, 01002h ; native 0D3B
    JNZ SHORT code_0d43 ; native 0D3E
    JMP NEAR PTR code_0a1f ; native 0D40
code_0d43:
    CMP AX, 01003h ; native 0D43
    JNZ SHORT code_0d4b ; native 0D46
    JMP NEAR PTR code_0b32 ; native 0D48
code_0d4b:
    CMP AX, 03000h ; native 0D4B
    JNZ SHORT code_0d53 ; native 0D4E
    JMP NEAR PTR code_0c28 ; native 0D50
code_0d53:
    CMP AX, 03002h ; native 0D53
    JNZ SHORT code_0d5b ; native 0D56
    JMP NEAR PTR code_0c80 ; native 0D58
code_0d5b:
    CMP AX, 03003h ; native 0D5B
    JNZ SHORT code_0d63 ; native 0D5E
    JMP NEAR PTR code_0cda ; native 0D60
code_0d63:
    JMP SHORT code_0d65 ; native 0D63
code_0d65:
    JMP NEAR PTR code_0a0d ; native 0D65
code_0d68:
    POP SI ; native 0D68
    POP DI ; native 0D69
    MOV SP, BP ; native 0D6A
    POP BP ; native 0D6C
    RET ; native 0D6D
_reset_position_08de ENDP
; Microsoft KB Q69987 pre-6.0 immediate-width recipe; no allocation/PUBLIC.
FULLWORD_IMMEDIATE_ZERO EQU 0
_TEXT ENDS
END
