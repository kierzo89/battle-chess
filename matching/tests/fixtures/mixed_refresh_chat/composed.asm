;	Static Name Aliases
;
	TITLE   C:\UNIT.C
	NAME    UNIT

	.8087
_TEXT	SEGMENT  WORD PUBLIC 'CODE'
_TEXT	ENDS
_DATA	SEGMENT  WORD PUBLIC 'DATA'
_DATA	ENDS
CONST	SEGMENT  WORD PUBLIC 'CONST'
CONST	ENDS
_BSS	SEGMENT  WORD PUBLIC 'BSS'
_BSS	ENDS
DGROUP	GROUP	CONST, _BSS, _DATA
	ASSUME  CS: _TEXT, DS: DGROUP, SS: DGROUP
EXTRN	__acrtused:ABS
EXTRN	__chkstk:NEAR
EXTRN	_write_bytes_dbb5:NEAR
EXTRN	_poll_input:NEAR
EXTRN	_obtain_input:NEAR
EXTRN	_step_872a:NEAR
EXTRN	_modes:DWORD
EXTRN	_waiting_0eee:WORD
EXTRN	_refresh_active_0548:WORD
EXTRN	_ready_9856:WORD
EXTRN	_refresh_stop_11a6:BYTE
EXTRN	_menu_state:WORD
EXTRN	_begin_input_0fb0:NEAR
EXTRN	_end_input_102d:NEAR
EXTRN	_fill_region_1780:NEAR
EXTRN	_text_input_1064:NEAR
EXTRN	_restore_region_58b0:NEAR
_TEXT      SEGMENT
	ASSUME	CS: _TEXT
; Line 10
	PUBLIC	_refresh_1446
_refresh_1446	PROC NEAR
	push	bp
	mov	bp,sp
	mov	ax,4
	call	__chkstk
;	command = -4
; Line 12
	cmp	WORD PTR _modes,2
	je	$I113
	cmp	WORD PTR _modes+2,2
	jne	$I112
$I113:
; Line 13
	mov	WORD PTR _waiting_0eee,0
; Line 14
	mov	WORD PTR [bp-4],1194	;command
; Line 15
	mov	WORD PTR [bp-2],13514
; Line 16
	mov	ax,4
	push	ax
	lea	ax,WORD PTR [bp-4]	;command
	push	ax
	call	_write_bytes_dbb5
	add	sp,4
; Line 17
	mov	WORD PTR _refresh_active_0548,1
; Line 18
	call	_poll_input
; Line 19
$FC115:
	cmp	WORD PTR _modes,2
	je	$FB117
	cmp	WORD PTR _modes+2,2
	jne	$FB116
$FB117:
	cmp	BYTE PTR _refresh_stop_11a6,0
	jne	$FB116
; Line 20
	cmp	WORD PTR _ready_9856,0
	jne	$I118
; Line 21
	call	_obtain_input
	mov	_ready_9856,ax
; Line 22
$I118:
	cmp	WORD PTR _ready_9856,0
	je	$I119
; Line 23
	call	_step_872a
; Line 24
$I119:
	jmp	SHORT $FC115
$FB116:
; Line 25
	mov	WORD PTR _refresh_active_0548,0
; Line 26
	mov	BYTE PTR _refresh_stop_11a6,0
; Line 27
; Line 28
$I112:
	mov	sp,bp
	pop	bp
	ret	

_refresh_1446	ENDP

PUBLIC _type_chat_14c1
_type_chat_14c1 PROC NEAR
    push bp ; native 14C1
    mov bp,sp ; native 14C2
    mov ax,48 ; native 14C4
    call NEAR PTR __chkstk ; native 14C7
    push di ; native 14CA
    push si ; native 14CB
    mov si,WORD PTR [bp+4] ; native 14CC
    call NEAR PTR _begin_input_0fb0 ; native 14CF
    push WORD PTR _menu_state ; native 14D2
    mov ax,112 ; native 14D6
    push ax ; native 14D9
    mov ax,319 ; native 14DA
    push ax ; native 14DD
    mov ax,88 ; native 14DE
    push ax ; native 14E1
    sub ax,ax ; native 14E2
    push ax ; native 14E4
    call NEAR PTR _fill_region_1780 ; native 14E5
    add sp,10 ; native 14E8
    push si ; native 14EB
    mov ax,37 ; native 14EC
    push ax ; native 14EF
    lea ax,[bp-40] ; native 14F0
    push ax ; native 14F3
    mov ax,96 ; native 14F4
    push ax ; native 14F7
    mov ax,8 ; native 14F8
    push ax ; native 14FB
    call NEAR PTR _text_input_1064 ; native 14FC
    add sp,10 ; native 14FF
    mov di,ax ; native 1502
    mov bx,di ; native 1504
    inc di ; native 1506
    add bx,bp ; native 1507
    mov BYTE PTR [bx-40],13 ; native 1509
    mov ax,112 ; native 150D
    push ax ; native 1510
    mov ax,88 ; native 1511
    push ax ; native 1514
    mov ax,79 ; native 1515
    push ax ; native 1518
    sub ax,ax ; native 1519
    push ax ; native 151B
    call NEAR PTR _restore_region_58b0 ; native 151C
    add sp,8 ; native 151F
    cmp di,1 ; native 1522
    jle SHORT chat_done ; native 1525
    cmp di,4 ; native 1527
    jne SHORT ordinary_message ; native 152A
    cmp BYTE PTR [bp-40],43 ; native 152C
    jne SHORT ordinary_message ; native 1530
    cmp BYTE PTR [bp-39],43 ; native 1532
    jne SHORT ordinary_message ; native 1536
    cmp BYTE PTR [bp-38],43 ; native 1538
    jne SHORT ordinary_message ; native 153C
    lea ax,[di-1] ; native 153E
    push ax ; native 1541
    lea ax,[bp-40] ; native 1542
    push ax ; native 1545
    call NEAR PTR _write_bytes_dbb5 ; native 1546
    add sp,4 ; native 1549
    jmp SHORT chat_done ; native 154C
ordinary_message:
    push di ; native 154E
    lea ax,[bp-40] ; native 154F
    push ax ; native 1552
    call NEAR PTR _write_bytes_dbb5 ; native 1553
    add sp,4 ; native 1556
chat_done:
    call NEAR PTR _end_input_102d ; native 1559
    pop si ; native 155C
    pop di ; native 155D
    mov sp,bp ; native 155E
    pop bp ; native 1560
    ret ; native 1561
_type_chat_14c1 ENDP

; Combined module finalization: one WORD alignment after both real procedures.
	EVEN
_TEXT	ENDS
END
