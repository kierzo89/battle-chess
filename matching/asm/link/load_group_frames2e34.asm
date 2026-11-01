; Whole native load_group_frames1030. Cframe36/native40 negative remains held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _pair_offsets:WORD, _pair_directory_lengths:WORD
EXTRN _frame_metadata:BYTE, _frame_indices:BYTE, _directory_lists:WORD
EXTRN _frame_list_count:WORD, _frame_data_cursor:WORD, _frame_list_cursor:WORD
EXTRN _count_0096:WORD, _frame_count:WORD, _arena_cursor:WORD, _cached_frames:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN _seek_asset:NEAR, _read_asset:NEAR, _prepare_asset_decode:NEAR, __aNlshr:NEAR, _huff_window_save:NEAR, _huff_decode_stream:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT,DS:DGROUP,SS:DGROUP
PUBLIC _load_group_frames
_load_group_frames PROC NEAR
    PUSH BP ; native2E34 / 1 bytes
    MOV BP, SP ; native2E35 / 2 bytes
    SUB SP, 028h ; native2E37 / 3 bytes
    PUSH DI ; native2E3A / 1 bytes
    PUSH SI ; native2E3B / 1 bytes
    SUB word ptr [BP + 08h], 03h ; native2E3C / 4 bytes
    MOV BX, word ptr [BP + 08h] ; native2E40 / 3 bytes
    MOV CL, 03h ; native2E43 / 2 bytes
    SHL BX, CL ; native2E45 / 2 bytes
    ADD BX, word ptr _pair_offsets ; native2E47 / 4 bytes
    MOV ES, word ptr _pair_offsets+2 ; native2E4B / 4 bytes
    PUSH word ptr ES:[BX + 02h] ; native2E4F / 4 bytes
    PUSH word ptr ES:[BX] ; native2E53 / 3 bytes
    CALL NEAR PTR _seek_asset ; native2E56 / 3 bytes
    ADD SP, 04h ; native2E59 / 3 bytes
    MOV BX, word ptr [BP + 08h] ; native2E5C / 3 bytes
    MOV CL, 03h ; native2E5F / 2 bytes
    SHL BX, CL ; native2E61 / 2 bytes
    ADD BX, word ptr _pair_directory_lengths ; native2E63 / 4 bytes
    MOV ES, word ptr _pair_directory_lengths+2 ; native2E67 / 4 bytes
    PUSH word ptr ES:[BX + 02h] ; native2E6B / 4 bytes
    PUSH word ptr ES:[BX] ; native2E6F / 3 bytes
    MOV AX, OFFSET DGROUP:_frame_metadata ; native2E72 / 3 bytes
    PUSH DS ; native2E75 / 1 bytes
    PUSH AX ; native2E76 / 1 bytes
    CALL NEAR PTR _read_asset ; native2E77 / 3 bytes
    ADD SP, 08h ; native2E7A / 3 bytes
    SUB SI, SI ; native2E7D / 2 bytes
    JMP SHORT group_2e89 ; native2E7F / 2 bytes
group_2e81:
    MOV BX, SI ; native2E81 / 2 bytes
    INC SI ; native2E83 / 1 bytes
    MOV byte ptr _frame_indices[BX], 00h ; native2E84 / 5 bytes
group_2e89:
    CMP SI, 0100h ; native2E89 / 4 bytes
    JL SHORT group_2e81 ; native2E8D / 2 bytes
    MOV word ptr [BP - 012h], OFFSET DGROUP:_frame_metadata ; native2E8F / 5 bytes
group_2e94:
    MOV BX, word ptr [BP - 012h] ; native2E94 / 3 bytes
    CMP word ptr [BX], 00h ; native2E97 / 3 bytes
    JNZ SHORT group_2ea2 ; native2E9A / 2 bytes
    CMP word ptr [BX + 02h], 00h ; native2E9C / 4 bytes
    JZ SHORT group_2ea8 ; native2EA0 / 2 bytes
group_2ea2:
    ADD word ptr [BP - 012h], 06h ; native2EA2 / 4 bytes
    JMP SHORT group_2e94 ; native2EA6 / 2 bytes
group_2ea8:
    ADD word ptr [BP - 012h], 06h ; native2EA8 / 4 bytes
    MOV AX, word ptr [BP - 012h] ; native2EAC / 3 bytes
    MOV _directory_lists, AX ; native2EAF / 3 bytes
    MOV word ptr [BP - 06h], AX ; native2EB2 / 3 bytes
    MOV word ptr [BP - 04h], DS ; native2EB5 / 3 bytes
    LES BX, [BP - 06h] ; native2EB8 / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native2EBB / 4 bytes
    JNC SHORT group_2ec6 ; native2EBF / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native2EC1 / 5 bytes
group_2ec6:
    MOV AL, byte ptr ES:[BX] ; native2EC6 / 3 bytes
    SUB AH, AH ; native2EC9 / 2 bytes
    MOV word ptr [BP - 014h], AX ; native2ECB / 3 bytes
    SUB SI, SI ; native2ECE / 2 bytes
    JMP NEAR PTR group_2f6f ; native2ED0 / 3 bytes
group_2ed3:
    MOV AL, byte ptr [BP - 024h] ; native2ED3 / 3 bytes
    SUB AH, AH ; native2ED6 / 2 bytes
    CMP AX, SI ; native2ED8 / 2 bytes
    JNZ SHORT group_2ee9 ; native2EDA / 2 bytes
    MOV word ptr [BP - 020h], 01h ; native2EDC / 5 bytes
    MOV BX, word ptr [BP + 06h] ; native2EE1 / 3 bytes
    MOV AL, byte ptr _frame_list_count ; native2EE4 / 3 bytes
    MOV byte ptr [BX + DI], AL ; native2EE7 / 2 bytes
group_2ee9:
    ADD word ptr [BP - 0ch], 01h ; native2EE9 / 4 bytes
    SBB AX, AX ; native2EED / 2 bytes
    AND AX, 01000h ; native2EEF / 3 bytes
    ADD word ptr [BP - 0ah], AX ; native2EF2 / 3 bytes
    INC DI ; native2EF5 / 1 bytes
group_2ef6:
    LES BX, [BP - 0ch] ; native2EF6 / 3 bytes
    MOV AL, byte ptr ES:[BX] ; native2EF9 / 3 bytes
    MOV byte ptr [BP - 024h], AL ; native2EFC / 3 bytes
    CMP AL, 0ffh ; native2EFF / 2 bytes
    JNZ SHORT group_2ed3 ; native2F01 / 2 bytes
    MOV BX, word ptr [BP + 06h] ; native2F03 / 3 bytes
    MOV byte ptr [BX + DI], 0ffh ; native2F06 / 3 bytes
    LES BX, [BP - 06h] ; native2F09 / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native2F0C / 4 bytes
    JNC SHORT group_2f17 ; native2F10 / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native2F12 / 5 bytes
group_2f17:
    MOV AL, byte ptr ES:[BX] ; native2F17 / 3 bytes
    SUB AH, AH ; native2F1A / 2 bytes
    MOV word ptr [BP - 010h], AX ; native2F1C / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native2F1F / 4 bytes
    SBB AX, AX ; native2F23 / 2 bytes
    AND AX, 01000h ; native2F25 / 3 bytes
    ADD word ptr [BP - 04h], AX ; native2F28 / 3 bytes
    CMP word ptr [BP - 020h], 00h ; native2F2B / 4 bytes
    JZ SHORT group_2f59 ; native2F2F / 2 bytes
    INC word ptr _frame_list_count ; native2F31 / 4 bytes
    MOV DI, word ptr [BP - 010h] ; native2F35 / 3 bytes
    JMP SHORT group_2f3b ; native2F38 / 2 bytes
group_2f3a:
    DEC DI ; native2F3A / 1 bytes
group_2f3b:
    OR DI, DI ; native2F3B / 2 bytes
    JZ SHORT group_2f6e ; native2F3D / 2 bytes
    LES BX, [BP - 06h] ; native2F3F / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native2F42 / 4 bytes
    JNC SHORT group_2f4d ; native2F46 / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native2F48 / 5 bytes
group_2f4d:
    MOV BL, byte ptr ES:[BX] ; native2F4D / 3 bytes
    SUB BH, BH ; native2F50 / 2 bytes
    MOV byte ptr _frame_indices[BX], 01h ; native2F52 / 5 bytes
    JMP SHORT group_2f3a ; native2F57 / 2 bytes
group_2f59:
    MOV AX, word ptr [BP - 010h] ; native2F59 / 3 bytes
    CWD ; native2F5C / 1 bytes
    SUB BX, BX ; native2F5D / 2 bytes
    MOV CX, AX ; native2F5F / 2 bytes
    ADD word ptr [BP - 06h], CX ; native2F61 / 3 bytes
    ADC BX, DX ; native2F64 / 2 bytes
    MOV CX, 0ch ; native2F66 / 3 bytes
    SHL BX, CL ; native2F69 / 2 bytes
    ADD word ptr [BP - 04h], BX ; native2F6B / 3 bytes
group_2f6e:
    INC SI ; native2F6E / 1 bytes
group_2f6f:
    CMP word ptr [BP - 014h], SI ; native2F6F / 3 bytes
    JLE SHORT group_2f87 ; native2F72 / 2 bytes
    MOV word ptr [BP - 020h], 00h ; native2F74 / 5 bytes
    MOV AX, word ptr [BP + 04h] ; native2F79 / 3 bytes
    MOV word ptr [BP - 0ch], AX ; native2F7C / 3 bytes
    MOV word ptr [BP - 0ah], DS ; native2F7F / 3 bytes
    SUB DI, DI ; native2F82 / 2 bytes
    JMP NEAR PTR group_2ef6 ; native2F84 / 3 bytes
group_2f87:
    SUB SI, SI ; native2F87 / 2 bytes
    SUB DI, DI ; native2F89 / 2 bytes
    JMP SHORT group_2f93 ; native2F8B / 2 bytes
group_2f8d:
    MOV byte ptr _frame_indices[SI], 0ffh ; native2F8D / 5 bytes
group_2f92:
    INC SI ; native2F92 / 1 bytes
group_2f93:
    CMP SI, 0100h ; native2F93 / 4 bytes
    JGE SHORT group_2fa9 ; native2F97 / 2 bytes
    CMP byte ptr _frame_indices[SI], 00h ; native2F99 / 5 bytes
    JZ SHORT group_2f8d ; native2F9E / 2 bytes
    MOV AX, DI ; native2FA0 / 2 bytes
    INC DI ; native2FA2 / 1 bytes
    MOV byte ptr _frame_indices[SI], AL ; native2FA3 / 4 bytes
    JMP SHORT group_2f92 ; native2FA7 / 2 bytes
group_2fa9:
    MOV word ptr [BP - 02h], DI ; native2FA9 / 3 bytes
    MOV AX, _directory_lists ; native2FAC / 3 bytes
    MOV word ptr [BP - 06h], AX ; native2FAF / 3 bytes
    MOV word ptr [BP - 04h], DS ; native2FB2 / 3 bytes
    MOV AX, _frame_data_cursor ; native2FB5 / 3 bytes
    MOV word ptr [BP - 012h], AX ; native2FB8 / 3 bytes
    LES BX, [BP - 06h] ; native2FBB / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native2FBE / 4 bytes
    JNC SHORT group_2fc9 ; native2FC2 / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native2FC4 / 5 bytes
group_2fc9:
    MOV AL, byte ptr ES:[BX] ; native2FC9 / 3 bytes
    SUB AH, AH ; native2FCC / 2 bytes
    MOV word ptr [BP - 014h], AX ; native2FCE / 3 bytes
    SUB SI, SI ; native2FD1 / 2 bytes
    JMP NEAR PTR group_30bb ; native2FD3 / 3 bytes
group_2fd6:
    ADD word ptr [BP - 0ch], 01h ; native2FD6 / 4 bytes
    SBB AX, AX ; native2FDA / 2 bytes
    AND AX, 01000h ; native2FDC / 3 bytes
    ADD word ptr [BP - 0ah], AX ; native2FDF / 3 bytes
group_2fe2:
    LES BX, [BP - 0ch] ; native2FE2 / 3 bytes
    MOV AL, byte ptr ES:[BX] ; native2FE5 / 3 bytes
    MOV byte ptr [BP - 024h], AL ; native2FE8 / 3 bytes
    CMP AL, 0ffh ; native2FEB / 2 bytes
    JZ SHORT group_2ff5 ; native2FED / 2 bytes
    SUB AH, AH ; native2FEF / 2 bytes
    CMP AX, SI ; native2FF1 / 2 bytes
    JNZ SHORT group_2fd6 ; native2FF3 / 2 bytes
group_2ff5:
    LES BX, [BP - 06h] ; native2FF5 / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native2FF8 / 4 bytes
    JNC SHORT group_3003 ; native2FFC / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native2FFE / 5 bytes
group_3003:
    MOV AL, byte ptr ES:[BX] ; native3003 / 3 bytes
    SUB AH, AH ; native3006 / 2 bytes
    MOV word ptr [BP - 010h], AX ; native3008 / 3 bytes
    LES BX, [BP - 0ch] ; native300B / 3 bytes
    MOV AL, byte ptr ES:[BX] ; native300E / 3 bytes
    CMP AX, SI ; native3011 / 2 bytes
    JZ SHORT group_3018 ; native3013 / 2 bytes
    JMP NEAR PTR group_30a4 ; native3015 / 3 bytes
group_3018:
    MOV BX, word ptr _frame_list_cursor ; native3018 / 4 bytes
    ADD word ptr _frame_list_cursor, 02h ; native301C / 5 bytes
    MOV AX, word ptr [BP - 012h] ; native3021 / 3 bytes
    MOV word ptr [BX], AX ; native3024 / 2 bytes
    LES BX, [BP - 06h] ; native3026 / 3 bytes
    TEST byte ptr ES:[BX], 080h ; native3029 / 4 bytes
    JZ SHORT group_3047 ; native302D / 2 bytes
    ADD word ptr [BP - 06h], 01h ; native302F / 4 bytes
    JNC SHORT group_303a ; native3033 / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native3035 / 5 bytes
group_303a:
    MOV AL, byte ptr ES:[BX] ; native303A / 3 bytes
    SUB AH, AH ; native303D / 2 bytes
    AND AX, 07fh ; native303F / 3 bytes
    ADD AX, 011h ; native3042 / 3 bytes
    JMP SHORT group_305e ; native3045 / 2 bytes
group_3047:
    LES BX, [BP - 06h] ; native3047 / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native304A / 4 bytes
    JNC SHORT group_3055 ; native304E / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native3050 / 5 bytes
group_3055:
    MOV AL, byte ptr ES:[BX] ; native3055 / 3 bytes
    SUB AH, AH ; native3058 / 2 bytes
    ADD AX, word ptr _count_0096 ; native305A / 4 bytes
group_305e:
    MOV BX, word ptr [BP - 012h] ; native305E / 3 bytes
    ADD word ptr [BP - 012h], 02h ; native3061 / 4 bytes
    MOV word ptr [BX], AX ; native3065 / 2 bytes
    MOV DI, word ptr [BP - 010h] ; native3067 / 3 bytes
    JMP SHORT group_3093 ; native306A / 2 bytes
group_306c:
    LES BX, [BP - 06h] ; native306C / 3 bytes
    ADD word ptr [BP - 06h], 01h ; native306F / 4 bytes
    JNC SHORT group_307a ; native3073 / 2 bytes
    ADD word ptr [BP - 04h], 01000h ; native3075 / 5 bytes
group_307a:
    MOV BL, byte ptr ES:[BX] ; native307A / 3 bytes
    SUB BH, BH ; native307D / 2 bytes
    MOV AL, byte ptr _frame_indices[BX] ; native307F / 4 bytes
    SUB AH, AH ; native3083 / 2 bytes
    ADD AX, word ptr _frame_count ; native3085 / 4 bytes
    MOV BX, word ptr [BP - 012h] ; native3089 / 3 bytes
    ADD word ptr [BP - 012h], 02h ; native308C / 4 bytes
    MOV word ptr [BX], AX ; native3090 / 2 bytes
    DEC DI ; native3092 / 1 bytes
group_3093:
    OR DI, DI ; native3093 / 2 bytes
    JNZ SHORT group_306c ; native3095 / 2 bytes
    MOV BX, word ptr [BP - 012h] ; native3097 / 3 bytes
    ADD word ptr [BP - 012h], 02h ; native309A / 4 bytes
    MOV word ptr [BX], 0ffffh ; native309E / 4 bytes
    JMP SHORT group_30ba ; native30A2 / 2 bytes
group_30a4:
    MOV AX, word ptr [BP - 010h] ; native30A4 / 3 bytes
    INC AX ; native30A7 / 1 bytes
    CWD ; native30A8 / 1 bytes
    SUB BX, BX ; native30A9 / 2 bytes
    MOV CX, AX ; native30AB / 2 bytes
    ADD word ptr [BP - 06h], CX ; native30AD / 3 bytes
    ADC BX, DX ; native30B0 / 2 bytes
    MOV CX, 0ch ; native30B2 / 3 bytes
    SHL BX, CL ; native30B5 / 2 bytes
    ADD word ptr [BP - 04h], BX ; native30B7 / 3 bytes
group_30ba:
    INC SI ; native30BA / 1 bytes
group_30bb:
    CMP word ptr [BP - 014h], SI ; native30BB / 3 bytes
    JLE SHORT group_30cc ; native30BE / 2 bytes
    MOV AX, word ptr [BP + 04h] ; native30C0 / 3 bytes
    MOV word ptr [BP - 0ch], AX ; native30C3 / 3 bytes
    MOV word ptr [BP - 0ah], DS ; native30C6 / 3 bytes
    JMP NEAR PTR group_2fe2 ; native30C9 / 3 bytes
group_30cc:
    MOV AX, word ptr [BP - 012h] ; native30CC / 3 bytes
    MOV _frame_data_cursor, AX ; native30CF / 3 bytes
    CALL NEAR PTR _prepare_asset_decode ; native30D2 / 3 bytes
    MOV word ptr [BP - 01eh], 00h ; native30D5 / 5 bytes
    SUB AX, AX ; native30DA / 2 bytes
    MOV word ptr [BP - 01ah], AX ; native30DC / 3 bytes
    MOV word ptr [BP - 01ch], AX ; native30DF / 3 bytes
    MOV word ptr [BP - 012h], OFFSET DGROUP:_frame_metadata ; native30E2 / 5 bytes
    MOV AX, _arena_cursor ; native30E7 / 3 bytes
    MOV DX, word ptr _arena_cursor+2 ; native30EA / 4 bytes
    MOV word ptr [BP - 06h], AX ; native30EE / 3 bytes
    MOV word ptr [BP - 04h], DX ; native30F1 / 3 bytes
    MOV AX, _frame_count ; native30F4 / 3 bytes
    MOV CL, 03h ; native30F7 / 2 bytes
    SHL AX, CL ; native30F9 / 2 bytes
    ADD AX, OFFSET DGROUP:_cached_frames ; native30FB / 3 bytes
    MOV word ptr [BP - 08h], AX ; native30FE / 3 bytes
    SUB SI, SI ; native3101 / 2 bytes
    JMP SHORT group_3157 ; native3103 / 2 bytes
group_3105:
    MOV AX, word ptr [BP - 06h] ; native3105 / 3 bytes
    MOV DX, word ptr [BP - 04h] ; native3108 / 3 bytes
group_310b:
    MOV word ptr [BP - 0ch], AX ; native310B / 3 bytes
    MOV word ptr [BP - 0ah], DX ; native310E / 3 bytes
    MOV BX, word ptr [BP - 08h] ; native3111 / 3 bytes
    MOV AX, word ptr [BP - 06h] ; native3114 / 3 bytes
    MOV DX, word ptr [BP - 04h] ; native3117 / 3 bytes
    MOV word ptr [BX + 04h], AX ; native311A / 3 bytes
    MOV word ptr [BX + 06h], DX ; native311D / 3 bytes
    MOV AX, word ptr [BP - 0ch] ; native3120 / 3 bytes
    MOV DX, word ptr [BP - 0ah] ; native3123 / 3 bytes
    MOV word ptr [BP - 06h], AX ; native3126 / 3 bytes
    MOV word ptr [BP - 04h], DX ; native3129 / 3 bytes
    ADD word ptr [BP - 08h], 08h ; native312C / 4 bytes
    JMP SHORT group_3145 ; native3130 / 2 bytes
group_3132:
    MOV BX, word ptr [BP - 08h] ; native3132 / 3 bytes
    CMP byte ptr [BX], 00h ; native3135 / 3 bytes
    JZ SHORT group_3145 ; native3138 / 2 bytes
    CMP byte ptr [BX + 01h], 00h ; native313A / 4 bytes
    JZ SHORT group_3145 ; native313E / 2 bytes
    MOV word ptr [BP - 01eh], 01h ; native3140 / 5 bytes
group_3145:
    MOV BX, word ptr [BP - 012h] ; native3145 / 3 bytes
    ADD word ptr [BP - 012h], 02h ; native3148 / 4 bytes
    MOV AX, word ptr [BX] ; native314C / 2 bytes
    SUB DX, DX ; native314E / 2 bytes
    ADD word ptr [BP - 01ch], AX ; native3150 / 3 bytes
    ADC word ptr [BP - 01ah], DX ; native3153 / 3 bytes
    INC SI ; native3156 / 1 bytes
group_3157:
    MOV BX, word ptr [BP - 012h] ; native3157 / 3 bytes
    CMP word ptr [BX], 00h ; native315A / 3 bytes
    JNZ SHORT group_3168 ; native315D / 2 bytes
    CMP word ptr [BX + 02h], 00h ; native315F / 4 bytes
    JNZ SHORT group_3168 ; native3163 / 2 bytes
    JMP NEAR PTR group_321a ; native3165 / 3 bytes
group_3168:
    ADD word ptr [BP - 012h], 02h ; native3168 / 4 bytes
    MOV AX, word ptr [BX] ; native316C / 2 bytes
    MOV BX, word ptr [BP - 08h] ; native316E / 3 bytes
    MOV word ptr [BX], AX ; native3171 / 2 bytes
    MOV BX, word ptr [BP - 012h] ; native3173 / 3 bytes
    ADD word ptr [BP - 012h], 02h ; native3176 / 4 bytes
    MOV AX, word ptr [BX] ; native317A / 2 bytes
    MOV BX, word ptr [BP - 08h] ; native317C / 3 bytes
    MOV word ptr [BX + 02h], AX ; native317F / 3 bytes
    CMP byte ptr _frame_indices[SI], 0ffh ; native3182 / 5 bytes
    JZ SHORT group_3132 ; native3187 / 2 bytes
    MOV BX, word ptr [BP - 08h] ; native3189 / 3 bytes
    CMP byte ptr [BX], 00h ; native318C / 3 bytes
    JNZ SHORT group_3194 ; native318F / 2 bytes
    JMP NEAR PTR group_3105 ; native3191 / 3 bytes
group_3194:
    CMP byte ptr [BX + 01h], 00h ; native3194 / 4 bytes
    JNZ SHORT group_319d ; native3198 / 2 bytes
    JMP NEAR PTR group_3105 ; native319A / 3 bytes
group_319d:
    CMP word ptr [BP - 01eh], 00h ; native319D / 4 bytes
    JZ SHORT group_31f1 ; native31A1 / 2 bytes
    MOV AX, word ptr [BP - 01ch] ; native31A3 / 3 bytes
    MOV DX, word ptr [BP - 01ah] ; native31A6 / 3 bytes
    MOV CL, 03h ; native31A9 / 2 bytes
    CALL NEAR PTR __aNlshr ; native31AB / 3 bytes
    MOV BX, word ptr [BP + 08h] ; native31AE / 3 bytes
    MOV CL, 03h ; native31B1 / 2 bytes
    SHL BX, CL ; native31B3 / 2 bytes
    ADD BX, word ptr _pair_offsets ; native31B5 / 4 bytes
    MOV ES, word ptr _pair_offsets+2 ; native31B9 / 4 bytes
    MOV word ptr [BP - 028h], AX ; native31BD / 3 bytes
    MOV word ptr [BP - 026h], DX ; native31C0 / 3 bytes
    MOV AX, word ptr ES:[BX + 04h] ; native31C3 / 4 bytes
    MOV DX, word ptr ES:[BX + 06h] ; native31C7 / 4 bytes
    ADD AX, word ptr [BP - 028h] ; native31CB / 3 bytes
    ADC DX, word ptr [BP - 026h] ; native31CE / 3 bytes
    ADD AX, 08h ; native31D1 / 3 bytes
    ADC DX, 00h ; native31D4 / 3 bytes
    PUSH DX ; native31D7 / 1 bytes
    PUSH AX ; native31D8 / 1 bytes
    CALL NEAR PTR _seek_asset ; native31D9 / 3 bytes
    ADD SP, 04h ; native31DC / 3 bytes
    MOV AX, word ptr [BP - 01ch] ; native31DF / 3 bytes
    AND AX, 07h ; native31E2 / 3 bytes
    PUSH AX ; native31E5 / 1 bytes
    CALL NEAR PTR _huff_window_save ; native31E6 / 3 bytes
    ADD SP, 02h ; native31E9 / 3 bytes
    MOV word ptr [BP - 01eh], 00h ; native31EC / 5 bytes
group_31f1:
    MOV BX, word ptr [BP - 08h] ; native31F1 / 3 bytes
    MOV AL, byte ptr [BX] ; native31F4 / 2 bytes
    SUB AH, AH ; native31F6 / 2 bytes
    INC AX ; native31F8 / 1 bytes
    SHR AX, 01h ; native31F9 / 2 bytes
    MOV word ptr [BP - 028h], AX ; native31FB / 3 bytes
    PUSH AX ; native31FE / 1 bytes
    MOV AL, byte ptr [BX + 01h] ; native31FF / 3 bytes
    SUB AH, AH ; native3202 / 2 bytes
    MUL word ptr [BP - 028h] ; native3204 / 3 bytes
    SUB CX, CX ; native3207 / 2 bytes
    PUSH CX ; native3209 / 1 bytes
    PUSH AX ; native320A / 1 bytes
    PUSH word ptr [BP - 04h] ; native320B / 3 bytes
    PUSH word ptr [BP - 06h] ; native320E / 3 bytes
    CALL NEAR PTR _huff_decode_stream ; native3211 / 3 bytes
    ADD SP, 0ah ; native3214 / 3 bytes
    JMP NEAR PTR group_310b ; native3217 / 3 bytes
group_321a:
    MOV AX, word ptr [BP - 08h] ; native321A / 3 bytes
    SUB AX, OFFSET DGROUP:_cached_frames ; native321D / 3 bytes
    MOV CL, 03h ; native3220 / 2 bytes
    SAR AX, CL ; native3222 / 2 bytes
    MOV _frame_count, AX ; native3224 / 3 bytes
    MOV AX, word ptr [BP - 06h] ; native3227 / 3 bytes
    MOV DX, word ptr [BP - 04h] ; native322A / 3 bytes
    MOV _arena_cursor, AX ; native322D / 3 bytes
    MOV word ptr _arena_cursor+2, DX ; native3230 / 4 bytes
    POP SI ; native3234 / 1 bytes
    POP DI ; native3235 / 1 bytes
    MOV SP, BP ; native3236 / 2 bytes
    POP BP ; native3238 / 1 bytes
    RET ; native3239 / 1 bytes
_load_group_frames ENDP
_TEXT ENDS
END
