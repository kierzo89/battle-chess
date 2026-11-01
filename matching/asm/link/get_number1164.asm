; Authored mnemonic reconstruction of complete native306. C buffer-home cause remains held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _menu_state:WORD, _foreground:BYTE, _menu_text:BYTE, _number_label_4c28:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _begin_input_0fb0:NEAR, _end_input_102d:NEAR, _fill_region_1780:NEAR, _draw_text_e915:NEAR, _text_input_1064:NEAR, _restore_region_58b0:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT,DS:DGROUP,SS:DGROUP
PUBLIC _get_number
_get_number PROC NEAR
    PUSH BP ; native1164 / 1 bytes
    MOV BP, SP ; native1165 / 2 bytes
    MOV AX, 01eh ; native1167 / 3 bytes
    CALL NEAR PTR __chkstk ; native116A / 3 bytes
    PUSH DI ; native116D / 1 bytes
    PUSH SI ; native116E / 1 bytes
    MOV word ptr [BP - 06h], 00h ; native116F / 5 bytes
    CALL NEAR PTR _begin_input_0fb0 ; native1174 / 3 bytes
number_1177:
    PUSH WORD PTR [_menu_state] ; native1177 / 4 bytes
    MOV AX, 06fh ; native117B / 3 bytes
    PUSH AX ; native117E / 1 bytes
    MOV AX, 013fh ; native117F / 3 bytes
    PUSH AX ; native1182 / 1 bytes
    MOV AX, 058h ; native1183 / 3 bytes
    PUSH AX ; native1186 / 1 bytes
    SUB AX, AX ; native1187 / 2 bytes
    PUSH AX ; native1189 / 1 bytes
    CALL NEAR PTR _fill_region_1780 ; native118A / 3 bytes
    ADD SP, 0ah ; native118D / 3 bytes
    MOV WORD PTR [_menu_text+2],OFFSET DGROUP:_number_label_4c28 ; native1190 / 6 bytes
    MOV AL,[_foreground] ; native1196 / 3 bytes
    MOV [_menu_text],AL ; native1199 / 3 bytes
    MOV AL,BYTE PTR [_menu_state] ; native119C / 3 bytes
    MOV [_menu_text+1],AL ; native119F / 3 bytes
    MOV AX, 060h ; native11A2 / 3 bytes
    PUSH AX ; native11A5 / 1 bytes
    MOV AX, 08h ; native11A6 / 3 bytes
    PUSH AX ; native11A9 / 1 bytes
    MOV AX,OFFSET DGROUP:_menu_text ; native11AA / 3 bytes
    PUSH AX ; native11AD / 1 bytes
    CALL NEAR PTR _draw_text_e915 ; native11AE / 3 bytes
    ADD SP, 06h ; native11B1 / 3 bytes
    SUB AX, AX ; native11B4 / 2 bytes
    PUSH AX ; native11B6 / 1 bytes
    MOV AX, 05h ; native11B7 / 3 bytes
    PUSH AX ; native11BA / 1 bytes
    LEA AX, [BP - 018h] ; native11BB / 3 bytes
    PUSH AX ; native11BE / 1 bytes
    MOV AX, 060h ; native11BF / 3 bytes
    PUSH AX ; native11C2 / 1 bytes
    MOV AX, 0e8h ; native11C3 / 3 bytes
    PUSH AX ; native11C6 / 1 bytes
    CALL NEAR PTR _text_input_1064 ; native11C7 / 3 bytes
    ADD SP, 0ah ; native11CA / 3 bytes
    MOV DI, AX ; native11CD / 2 bytes
    SUB AX, AX ; native11CF / 2 bytes
    MOV word ptr [BP - 02h], AX ; native11D1 / 3 bytes
    MOV word ptr [BP - 04h], AX ; native11D4 / 3 bytes
    OR DI, DI ; native11D7 / 2 bytes
    JZ SHORT number_1238 ; native11D9 / 2 bytes
    SUB SI, SI ; native11DB / 2 bytes
    JMP SHORT number_11e0 ; native11DD / 2 bytes
number_11df:
    INC SI ; native11DF / 1 bytes
number_11e0:
    CMP SI, DI ; native11E0 / 2 bytes
    JGE SHORT number_1236 ; native11E2 / 2 bytes
    MOV AL, byte ptr [BP + SI - 018h] ; native11E4 / 3 bytes
    SUB AH, AH ; native11E7 / 2 bytes
    SUB AX,030h ; native11E9 / 3 bytes
    SUB DX, DX ; native11EC / 2 bytes
    MOV CX, word ptr [BP - 04h] ; native11EE / 3 bytes
    MOV BX, word ptr [BP - 02h] ; native11F1 / 3 bytes
    MOV word ptr [BP - 01eh], AX ; native11F4 / 3 bytes
    MOV word ptr [BP - 01ch], DX ; native11F7 / 3 bytes
    MOV AX, CX ; native11FA / 2 bytes
    MOV DX, BX ; native11FC / 2 bytes
    SHL CX, 01h ; native11FE / 2 bytes
    RCL BX, 01h ; native1200 / 2 bytes
    SHL CX, 01h ; native1202 / 2 bytes
    RCL BX, 01h ; native1204 / 2 bytes
    ADD CX, AX ; native1206 / 2 bytes
    ADC BX, DX ; native1208 / 2 bytes
    SHL CX, 01h ; native120A / 2 bytes
    RCL BX, 01h ; native120C / 2 bytes
    MOV AX, word ptr [BP - 01eh] ; native120E / 3 bytes
    MOV DX, word ptr [BP - 01ch] ; native1211 / 3 bytes
    ADD AX, CX ; native1214 / 2 bytes
    ADC DX, BX ; native1216 / 2 bytes
    MOV word ptr [BP - 04h], AX ; native1218 / 3 bytes
    MOV word ptr [BP - 02h], DX ; native121B / 3 bytes
    CMP byte ptr [BP + SI - 018h], 030h ; native121E / 4 bytes
    JC SHORT number_122a ; native1222 / 2 bytes
    CMP byte ptr [BP + SI - 018h], 039h ; native1224 / 4 bytes
    JBE SHORT number_1234 ; native1228 / 2 bytes
number_122a:
    SUB AX, AX ; native122A / 2 bytes
    MOV word ptr [BP - 02h], AX ; native122C / 3 bytes
    MOV word ptr [BP - 04h], AX ; native122F / 3 bytes
    MOV SI, DI ; native1232 / 2 bytes
number_1234:
    JMP SHORT number_11df ; native1234 / 2 bytes
number_1236:
    JMP SHORT number_1242 ; native1236 / 2 bytes
number_1238:
    MOV word ptr [BP - 04h], 0ffffh ; native1238 / 5 bytes
    MOV word ptr [BP - 02h], 0ffffh ; native123D / 5 bytes
number_1242:
    MOV AX, word ptr [BP - 04h] ; native1242 / 3 bytes
    OR AX, word ptr [BP - 02h] ; native1245 / 3 bytes
    JNZ SHORT number_124d ; native1248 / 2 bytes
    JMP NEAR PTR number_1177 ; native124A / 3 bytes
number_124d:
    CMP word ptr [BP - 02h], 00h ; native124D / 4 bytes
    JLE SHORT number_1256 ; native1251 / 2 bytes
    JMP NEAR PTR number_1177 ; native1253 / 3 bytes
number_1256:
    JL SHORT number_1262 ; native1256 / 2 bytes
    CMP word ptr [BP - 04h], 02710h ; native1258 / 5 bytes
    JBE SHORT number_1262 ; native125D / 2 bytes
    JMP NEAR PTR number_1177 ; native125F / 3 bytes
number_1262:
    MOV AX, 06fh ; native1262 / 3 bytes
    PUSH AX ; native1265 / 1 bytes
    MOV AX, 058h ; native1266 / 3 bytes
    PUSH AX ; native1269 / 1 bytes
    MOV AX, 04fh ; native126A / 3 bytes
    PUSH AX ; native126D / 1 bytes
    SUB AX, AX ; native126E / 2 bytes
    PUSH AX ; native1270 / 1 bytes
    CALL NEAR PTR _restore_region_58b0 ; native1271 / 3 bytes
    ADD SP, 08h ; native1274 / 3 bytes
    CALL NEAR PTR _end_input_102d ; native1277 / 3 bytes
    CMP word ptr [BP - 02h], 00h ; native127A / 4 bytes
    JGE SHORT number_1288 ; native127E / 2 bytes
    SUB AX, AX ; native1280 / 2 bytes
    MOV word ptr [BP - 02h], AX ; native1282 / 3 bytes
    MOV word ptr [BP - 04h], AX ; native1285 / 3 bytes
number_1288:
    MOV AX, word ptr [BP - 04h] ; native1288 / 3 bytes
    MOV DX, word ptr [BP - 02h] ; native128B / 3 bytes
    JMP SHORT number_1290 ; native128E / 2 bytes
number_1290:
    POP SI ; native1290 / 1 bytes
    POP DI ; native1291 / 1 bytes
    MOV SP, BP ; native1292 / 2 bytes
    POP BP ; native1294 / 1 bytes
    RET ; native1295 / 1 bytes
_get_number ENDP
_TEXT ENDS
END
