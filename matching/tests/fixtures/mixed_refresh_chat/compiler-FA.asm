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
$$SYMBOLS	SEGMENT  BYTE PUBLIC 'DEBSYM'
$$SYMBOLS	ENDS
$$TYPES	SEGMENT  BYTE PUBLIC 'DEBTYP'
$$TYPES	ENDS
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
	nop	
_TEXT	ENDS
END
