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
EXTRN	_frame_data_cursor:WORD
EXTRN	_frame_list_cursor:WORD
EXTRN	_count_0096:WORD
EXTRN	_count_0094:WORD
EXTRN	_frame_count:WORD
EXTRN	_frame_list_count:WORD
EXTRN	_arena_cursor:DWORD
EXTRN	_active_data_b0ca:WORD
EXTRN	_active_lists_b080:WORD
EXTRN	_active_95fe:WORD
EXTRN	_active_8e22:WORD
EXTRN	_active_a834:WORD
EXTRN	_active_964e:WORD
EXTRN	_active_arena_9344:DWORD
_TEXT      SEGMENT
	ASSUME	CS: _TEXT
; Line 9
	PUBLIC	_restore_active_arena
_restore_active_arena	PROC NEAR
; Line 10
	mov	ax,_active_data_b0ca
	mov	_frame_data_cursor,ax
; Line 11
	mov	ax,_active_lists_b080
	mov	_frame_list_cursor,ax
; Line 12
	mov	ax,_active_95fe
	mov	_count_0096,ax
; Line 13
	mov	ax,_active_8e22
	mov	_count_0094,ax
; Line 14
	mov	ax,_active_a834
	mov	_frame_count,ax
; Line 15
	mov	ax,_active_964e
	mov	_frame_list_count,ax
; Line 16
	mov	ax,WORD PTR _active_arena_9344
	mov	dx,WORD PTR _active_arena_9344+2
	mov	WORD PTR _arena_cursor,ax
	mov	WORD PTR _arena_cursor+2,dx
; Line 17
	ret	

_restore_active_arena	ENDP
	nop	
_TEXT	ENDS
END
