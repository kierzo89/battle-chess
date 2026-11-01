; Authored mnemonic reconstruction; C frame/local allocation cause remains held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _dissolve_masks_0486:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _rand:NEAR, _attach_actor:NEAR, _detach_actor:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT,DS:DGROUP,SS:DGROUP
PUBLIC _remove_actor_5934
_remove_actor_5934 PROC NEAR
    PUSH BP ; native5934
    MOV BP, SP ; native5935
    MOV AX, 012h ; native5937
    call NEAR PTR __chkstk ; native593A
    PUSH DI ; native593D
    PUSH SI ; native593E
    MOV SI, word ptr [BP + 04h] ; native593F
    SUB DI, DI ; native5942
    JMP SHORT remove_5947 ; native5944
remove_5946:
    INC DI ; native5946
remove_5947:
    CMP DI, 0fh ; native5947
    JNC SHORT remove_598c ; native594A
    call NEAR PTR _rand ; native594C
    SUB DX, DX ; native594F
    MOV CX, 0fh ; native5951
    SUB CX, DI ; native5954
    DIV CX ; native5956
    ADD DX, DI ; native5958
    INC DX ; native595A
    MOV word ptr [BP - 0ch], DX ; native595B
    MOV AX, DI ; native595E
    SHL AX, 01h ; native5960
    add ax,OFFSET DGROUP:_dissolve_masks_0486 ; native5962
    MOV word ptr [BP - 010h], AX ; native5965
    MOV BX, AX ; native5968
    MOV AX, word ptr [BX] ; native596A
    MOV word ptr [BP - 08h], AX ; native596C
    MOV AX, DX ; native596F
    SHL AX, 01h ; native5971
    add ax,OFFSET DGROUP:_dissolve_masks_0486 ; native5973
    MOV word ptr [BP - 012h], AX ; native5976
    MOV BX, AX ; native5979
    MOV AX, word ptr [BX] ; native597B
    MOV BX, word ptr [BP - 010h] ; native597D
    MOV word ptr [BX], AX ; native5980
    MOV BX, word ptr [BP - 012h] ; native5982
    MOV AX, word ptr [BP - 08h] ; native5985
    MOV word ptr [BX], AX ; native5988
    JMP SHORT remove_5946 ; native598A
remove_598c:
    MOV AX, word ptr [SI + 08h] ; native598C
    MOV word ptr [BP - 08h], AX ; native598F
    MOV word ptr [SI + 08h], 00h ; native5992
    MOV BX, word ptr [SI + 014h] ; native5997
    MOV AL, byte ptr [BX + 01h] ; native599A
    SUB AH, AH ; native599D
    MOV CX, AX ; native599F
    MOV AL, byte ptr [BX] ; native59A1
    ADD AX, 03h ; native59A3
    SHR AX, 01h ; native59A6
    SHR AX, 01h ; native59A8
    MUL CX ; native59AA
    MOV word ptr [BP - 02h], AX ; native59AC
    SUB DI, DI ; native59AF
    JMP SHORT remove_59b4 ; native59B1
remove_59b3:
    INC DI ; native59B3
remove_59b4:
    CMP DI, 010h ; native59B4
    JNC SHORT remove_5a14 ; native59B7
    MOV BX, word ptr [SI + 014h] ; native59B9
    MOV AX, word ptr [BX + 04h] ; native59BC
    MOV DX, word ptr [BX + 06h] ; native59BF
    MOV word ptr [BP - 06h], AX ; native59C2
    MOV word ptr [BP - 04h], DX ; native59C5
    MOV word ptr [BP - 0ch], 00h ; native59C8
    JMP SHORT remove_59de ; native59CD
remove_59cf:
    INC word ptr [BP - 0ch] ; native59CF
    ADD word ptr [BP - 06h], 02h ; native59D2
    SBB AX, AX ; native59D6
    AND AX, 01000h ; native59D8
    ADD word ptr [BP - 04h], AX ; native59DB
remove_59de:
    MOV AX, word ptr [BP - 02h] ; native59DE
    CMP word ptr [BP - 0ch], AX ; native59E1
    JNC SHORT remove_59fd ; native59E4
    MOV BX, word ptr [BP - 0ch] ; native59E6
    ADD BX, DI ; native59E9
    AND BX, FULLWORD_IMMEDIATE_ZERO + 0fh ; native59EB
    SHL BX, 01h ; native59EF
    MOV AX, word ptr [BX+_dissolve_masks_0486] ; native59F1
    LES BX, [BP - 06h] ; native59F5
    AND word ptr ES:[BX], AX ; native59F8
    JMP SHORT remove_59cf ; native59FB
remove_59fd:
    PUSH SI ; native59FD
    PUSH word ptr [SI + 014h] ; native59FE
    MOV AL, byte ptr [SI + 0ah] ; native5A01
    SUB AH, AH ; native5A04
    PUSH AX ; native5A06
    PUSH word ptr [SI + 02h] ; native5A07
    PUSH word ptr [SI] ; native5A0A
    call NEAR PTR _attach_actor ; native5A0C
    ADD SP, 0ah ; native5A0F
    JMP SHORT remove_59b3 ; native5A12
remove_5a14:
    MOV byte ptr [SI + 0bh], 00h ; native5A14
    MOV AX, word ptr [BP - 08h] ; native5A18
    MOV word ptr [SI + 08h], AX ; native5A1B
    PUSH SI ; native5A1E
    call NEAR PTR _detach_actor ; native5A1F
    ADD SP, 02h ; native5A22
    POP SI ; native5A25
    POP DI ; native5A26
    MOV SP, BP ; native5A27
    POP BP ; native5A29
    RET ; native5A2A
_remove_actor_5934 ENDP
_TEXT ENDS
; Microsoft KB Q69987 pre-6.0 immediate-width recipe: forward zero EQU.
FULLWORD_IMMEDIATE_ZERO EQU 0
END
