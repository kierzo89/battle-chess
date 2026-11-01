; Sound port playback, timer calibration, BIOS video and drive probing.
; This is hardware/register assembly. The only DB is the used retry counter.
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _speed_2eb3:WORD
EXTRN _audio_calibration_ticks_2eae:BYTE
EXTRN _saved_timer_vector_2eaf:DWORD
EXTRN _saved_critical_vector_2eb5:DWORD
EXTRN _saved_pic_mask_2eb9:BYTE
EXTRN _mode_11aa:BYTE, _palette_mode:BYTE
_DATA ENDS
DGROUP GROUP _DATA
PLATFORM_TEXT SEGMENT PARA PUBLIC 'CODE'
ASSUME CS:PLATFORM_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _play_audio_10e3, _initialize_renderer, _play_audio_alt_10e3
PUBLIC _initialize_video, _restore_input_11066, _select_asset_drive

_play_audio_10e3 PROC FAR
    push bp
    mov bp, sp
    push si
    push di
    mov ax, [bp+6]
    mov dx, [bp+8]
    mov cx, _speed_2eb3
    div cx
    sub ax, 10
    jg sound_delay_ready
    xor ax, ax
    inc ax
sound_delay_ready:
    mov di, [bp+10]
    shl di, 1
    les si, DWORD PTR [bp+12]
    mov bp, ax
    mov ax, si
    mov cx, es
    shr ax, 1
    shr ax, 1
    shr ax, 1
    shr ax, 1
    add ax, cx
    sub ax, 800h
    mov es, ax
    and si, WORD PTR 0fh
    add si, 8000h
    in al, 21h
    mov ss:_saved_pic_mask_2eb9, al
    mov al, 0e7h
    out 21h, al
    sti
    mov al, 81h
    out 0c0h, al
    mov al, 0
    out 0c0h, al
    mov ah, 90h
    xor bx, bx
sound_sample:
    mov al, es:[si]
    ror al, 1
    ror al, 1
    ror al, 1
    ror al, 1
    mov es:[si], al
    xor al, 0ffh
    and al, 0fh
    or al, ah
    out 0c0h, al
    add si, bx
    xor bx, WORD PTR 1
    mov cx, bp
sound_delay:
    loop sound_delay
    dec di
    jnz sound_sample
    mov al, ss:_saved_pic_mask_2eb9
    out 21h, al
    pop di
    pop si
    pop bp
    retf
_play_audio_10e3 ENDP

_initialize_renderer PROC FAR
    push bp
    mov bp, sp
    push si
    push di
    mov _audio_calibration_ticks_2eae, 0ffh
    mov ax, 3508h
    int 21h
    mov WORD PTR _saved_timer_vector_2eaf, bx
    mov WORD PTR _saved_timer_vector_2eaf+2, es
    push ds
    mov ax, cs
    mov ds, ax
    mov dx, OFFSET calibration_interrupt
    mov ax, 2508h
    int 21h
    pop ds
    xor cx, cx
    mov al, 0ffh
calibration_wait:
    test _audio_calibration_ticks_2eae, al
    jnz calibration_wait
calibration_loop:
    loop calibration_loop
    xor al, al
    out 43h, al
    cli
    in al, 40h
    mov bl, al
    in al, 40h
    mov bh, al
    xor ax, ax
    sub ax, bx
    mov cx, 838
    mul cx
    test ax, ax
    jns calibration_round_ready
    inc dx
calibration_round_ready:
    mov bx, dx
    xor ax, ax
    mov al, _audio_calibration_ticks_2eae
    mul cx
    add ax, bx
    mov _speed_2eb3, ax
    sti
    push ds
    mov ax, WORD PTR _saved_timer_vector_2eaf+2
    mov dx, WORD PTR _saved_timer_vector_2eaf
    mov ds, ax
    mov ax, 2508h
    int 21h
    pop ds
    pop di
    pop si
    pop bp
    retf
_initialize_renderer ENDP

_play_audio_alt_10e3 PROC FAR
    push bp
    mov bp, sp
    push si
    push di
    mov ax, [bp+6]
    mov dx, [bp+8]
    mov cx, _speed_2eb3
    div cx
    sub ax, 2
    jg speaker_delay_ready
    xor ax, ax
    inc ax
speaker_delay_ready:
    mov di, [bp+10]
    les si, DWORD PTR [bp+12]
    mov bp, ax
    mov ax, si
    mov cx, es
    shr ax, 1
    shr ax, 1
    shr ax, 1
    shr ax, 1
    add ax, cx
    sub ax, 800h
    mov es, ax
    and si, WORD PTR 0fh
    add si, 8000h
    sti
    in al, 21h
    mov ss:_saved_pic_mask_2eb9, al
    mov al, 0e7h
    out 21h, al
    in al, 61h
    and al, 0fdh
    mov bh, al
speaker_sample:
    xor bh, 2
    mov al, bh
    out 61h, al
    lods BYTE PTR es:[si]
speaker_repeat:
    mov cx, bp
speaker_delay:
    loop speaker_delay
    dec al
    jnz speaker_repeat
    dec di
    jnz speaker_sample
    mov al, ss:_saved_pic_mask_2eb9
    out 21h, al
    pop di
    pop si
    pop bp
    retf
_play_audio_alt_10e3 ENDP

calibration_interrupt LABEL NEAR
    push ax
    mov al, 20h
    inc _audio_calibration_ticks_2eae
    out 20h, al
    pop ax
    iret

detect_video PROC FAR
    push si
    push di
    mov ax, 0f000h
    mov es, ax
    mov al, es:[0fffeh]
    cmp al, 0ffh
    je check_rom_signature
    cmp al, 0fdh
    je builtin_video
check_rom_signature:
    mov al, es:[0c000h]
    cmp al, 21h
    jne detect_bios_video
builtin_video:
    mov _mode_11aa, 0
    mov _palette_mode, 2
    jmp SHORT detection_done
detect_bios_video:
    mov _mode_11aa, 1
    call detect_vga
    or ax, ax
    jz try_ega
    mov _palette_mode, 4
    jmp SHORT detection_done
try_ega:
    call detect_ega
    mov _palette_mode, al
detection_done:
    pop di
    pop si
    retf
detect_video ENDP

detect_vga PROC NEAR
    mov ax, 1a00h
    int 10h
    cmp al, 1ah
    jne no_vga
    cmp bl, 0ch
    je have_vga
    cmp bl, 0ah
    je have_vga
    cmp bl, 8
    jne have_vga
have_vga:
    mov ax, 1
    ret
no_vga:
    sub ax, ax
    ret
detect_vga ENDP

detect_ega PROC NEAR
    mov bl, 10h
    mov ah, 12h
    int 10h
    cmp bl, 10h
    je no_ega
    or bh, bh
    jnz no_ega
    mov ax, 1
    ret
no_ega:
    sub ax, ax
    ret
detect_ega ENDP

critical_error_interrupt LABEL NEAR
    mov al, 1
    iret

_initialize_video PROC FAR
    push bp
    mov bp, sp
    push si
    push di
    cmp WORD PTR [bp+6], 0
    jne mode_cga
    call detect_video
    mov ax, 9
    cmp _palette_mode, 2
    je set_video_mode
    mov ax, 0dh
    cmp _palette_mode, 1
    je set_video_mode
    mov ax, 13h
    cmp _palette_mode, 4
    je set_video_mode
mode_cga:
    mov ax, 4
set_video_mode:
    int 10h
    mov ax, 3524h
    int 21h
    mov WORD PTR _saved_critical_vector_2eb5, bx
    mov WORD PTR _saved_critical_vector_2eb5+2, es
    mov ax, cs
    mov ds, ax
    mov dx, OFFSET critical_error_interrupt
    mov ax, 2524h
    int 21h
    mov ax, ss
    mov ds, ax
    pop di
    pop si
    pop bp
    retf
_initialize_video ENDP

_restore_input_11066 PROC FAR
    push bp
    push si
    push di
    mov ax, 3
    int 10h
    mov ax, 2524h
    mov dx, WORD PTR _saved_critical_vector_2eb5
    mov ds, WORD PTR _saved_critical_vector_2eb5+2
    int 21h
    mov ax, ss
    mov ds, ax
    pop di
    pop si
    pop bp
    retf
_restore_input_11066 ENDP

drive_attempts DB 0
_select_asset_drive PROC FAR
    push bp
    push si
    push di
    sub ax, ax
    int 13h
    mov cs:drive_attempts, 0
drive_retry:
    cmp cs:drive_attempts, 3
    je drive_failed
    inc cs:drive_attempts
    mov ax, 0401h
    sub bx, bx
    mov es, bx
    mov cx, 1
    mov dh, 0
    mov bp, sp
    mov dl, [bp+10]
    sub dl, 41h
    int 13h
    jnc drive_succeeded
    jmp SHORT drive_retry
drive_succeeded:
    mov ax, 1
    jmp SHORT drive_probe_done
drive_failed:
    sub ax, ax
drive_probe_done:
    pop di
    pop si
    pop bp
    retf
_select_asset_drive ENDP
PLATFORM_TEXT ENDS
END
