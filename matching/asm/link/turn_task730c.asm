; Authored mnemonic reconstruction; original language/TU and C frame cause held.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _asset_groups:BYTE, _frames:BYTE, _piece_controls:BYTE
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR, _task_ready_772d:NEAR, _pop_value:NEAR
EXTRN _compose_frame_3b3a:NEAR, _attach_actor:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _turn_task_730c
_turn_task_730c PROC NEAR
    push bp ; native 730C
    mov bp, sp ; native 730D
    mov ax, 10h ; native 730F
    call NEAR PTR __chkstk ; native 7312
    push di ; native 7315
    push si ; native 7316
    mov si, word ptr [bp+4h] ; native 7317
    cmp word ptr [si+0ch], 0h ; native 731A
    jz SHORT turn_7330 ; native 731E
    push si ; native 7320
    call NEAR PTR _task_ready_772d ; native 7321
    add sp, 2h ; native 7324
    or ax, ax ; native 7327
    jnz SHORT turn_7330 ; native 7329
    sub ax, ax ; native 732B
    jmp NEAR PTR turn_7586 ; native 732D
turn_7330:
    mov ax, word ptr [si] ; native 7330
    mov word ptr [bp-0ch], ax ; native 7332
    mov di, word ptr [si+6h] ; native 7335
    mov al, byte ptr [si+0eh] ; native 7338
    sub ah, ah ; native 733B
    mov word ptr [bp-0eh], ax ; native 733D
    mov al, byte ptr [si+10h] ; native 7340
    mov byte ptr [bp-8h], al ; native 7343
    cmp word ptr [bp-0ch], 0h ; native 7346
    jz SHORT turn_734f ; native 734A
    jmp NEAR PTR turn_752d ; native 734C
turn_734f:
    cmp word ptr [si+0ch], 0h ; native 734F
    jnz SHORT turn_7358 ; native 7353
    jmp NEAR PTR turn_7451 ; native 7355
turn_7358:
    mov al, byte ptr [si+0ch] ; native 7358
    add al, byte ptr [bp-0eh] ; native 735B
    and al, 7h ; native 735E
    cmp al, byte ptr [si+0fh] ; native 7360
    jnz SHORT turn_736b ; native 7363
    mov ax, 1h ; native 7365
    jmp NEAR PTR turn_7586 ; native 7368
turn_736b:
    mov ax, word ptr [si+0ch] ; native 736B
    add ax, word ptr [bp-0eh] ; native 736E
    and ax, 7h ; native 7371
    mov word ptr [bp-0eh], ax ; native 7374
    cmp word ptr [si+0ch], 0h ; native 7377
    jle SHORT turn_7382 ; native 737B
    add ax, 8h ; native 737D
    jmp SHORT turn_7388 ; native 7380
turn_7382:
    mov ax, word ptr [bp-0eh] ; native 7382
    add ax, 10h ; native 7385
turn_7388:
    mov word ptr [bp-6h], ax ; native 7388
    cmp byte ptr [bp-8h], 3h ; native 738B
    jz SHORT turn_739d ; native 738F
    cmp byte ptr [bp-8h], 6h ; native 7391
    jz SHORT turn_739d ; native 7395
    cmp byte ptr [bp-8h], 1h ; native 7397
    jnz SHORT turn_73a0 ; native 739B
turn_739d:
    shr word ptr [bp-6h], 1h ; native 739D
turn_73a0:
    cmp byte ptr [bp-8h], 2h ; native 73A0
    jz SHORT turn_73b2 ; native 73A4
    cmp byte ptr [bp-8h], 5h ; native 73A6
    jz SHORT turn_73b2 ; native 73AA
    cmp byte ptr [bp-8h], 1h ; native 73AC
    jnz SHORT turn_740d ; native 73B0
turn_73b2:
    mov al, 14h ; native 73B2
    mul byte ptr [bp-8h] ; native 73B4
    mov bx, ax ; native 73B7
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 73B9
    mov ax, word ptr [bp-6h] ; native 73BD
    shl ax, 1h ; native 73C0
    add bx, ax ; native 73C2
    mov ax, word ptr [bx] ; native 73C4
    mov word ptr [bp-0ch], ax ; native 73C6
    add word ptr [bp-0ch], 4h ; native 73C9
    mov ax, word ptr [di+14h] ; native 73CD
    mov word ptr [bp-4h], ax ; native 73D0
    call NEAR PTR _pop_value ; native 73D3
    mov word ptr [bp-2h], ax ; native 73D6
    push ax ; native 73D9
    mov bx, word ptr [bp-0ch] ; native 73DA
    add word ptr [bp-0ch], 2h ; native 73DD
    push word ptr [bx] ; native 73E1
    push word ptr [bp-4h] ; native 73E3
    call NEAR PTR _compose_frame_3b3a ; native 73E6
    add sp, 6h ; native 73E9
    mov ax, word ptr [bp-2h] ; native 73EC
    mov word ptr [bp-4h], ax ; native 73EF
    push di ; native 73F2
    push ax ; native 73F3
    mov al, byte ptr [di+0ah] ; native 73F4
    sub ah, ah ; native 73F7
    push ax ; native 73F9
    push word ptr [di+6h] ; native 73FA
    push word ptr [di+4h] ; native 73FD
    call NEAR PTR _attach_actor ; native 7400
    add sp, 0ah ; native 7403
    mov word ptr [di+8h], 1h ; native 7406
    jmp SHORT turn_744e ; native 740B
turn_740d:
    mov al, 14h ; native 740D
    mul byte ptr [bp-8h] ; native 740F
    mov bx, ax ; native 7412
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 7414
    mov ax, word ptr [bp-6h] ; native 7418
    shl ax, 1h ; native 741B
    add bx, ax ; native 741D
    mov ax, word ptr [bx] ; native 741F
    mov word ptr [bp-0ch], ax ; native 7421
    mov bx, ax ; native 7424
    add word ptr [bp-0ch], 2h ; native 7426
    mov ax, word ptr [bx] ; native 742A
    mov cl, 3h ; native 742C
    shl ax, cl ; native 742E
    add ax,OFFSET DGROUP:_frames ; native 7430
    mov word ptr [bp-4h], ax ; native 7433
    push di ; native 7436
    push ax ; native 7437
    mov al, byte ptr [di+0ah] ; native 7438
    sub ah, ah ; native 743B
    push ax ; native 743D
    push word ptr [di+2h] ; native 743E
    push word ptr [di] ; native 7441
    call NEAR PTR _attach_actor ; native 7443
    add sp, 0ah ; native 7446
    mov word ptr [di+8h], 0h ; native 7449
turn_744e:
    jmp NEAR PTR turn_74fc ; native 744E
turn_7451:
    mov al, byte ptr [si+0fh] ; native 7451
    sub ah, ah ; native 7454
    cmp ax, word ptr [bp-0eh] ; native 7456
    jnz SHORT turn_7461 ; native 7459
    mov ax, 1h ; native 745B
    jmp NEAR PTR turn_7586 ; native 745E
turn_7461:
    mov al, byte ptr [si+0fh] ; native 7461
    sub al, byte ptr [bp-0eh] ; native 7464
    test al, 4h ; native 7467
    jz SHORT turn_7470 ; native 7469
    mov ax, 0ffffh ; native 746B
    jmp SHORT turn_7473 ; native 746E
turn_7470:
    mov ax, 1h ; native 7470
turn_7473:
    mov word ptr [si+0ch], ax ; native 7473
    or ax, ax ; native 7476
    jle SHORT turn_7482 ; native 7478
    mov ax, word ptr [bp-0eh] ; native 747A
    add ax, 8h ; native 747D
    jmp SHORT turn_7488 ; native 7480
turn_7482:
    mov ax, word ptr [bp-0eh] ; native 7482
    add ax, 10h ; native 7485
turn_7488:
    mov word ptr [bp-6h], ax ; native 7488
    cmp byte ptr [bp-8h], 3h ; native 748B
    jz SHORT turn_749d ; native 748F
    cmp byte ptr [bp-8h], 6h ; native 7491
    jz SHORT turn_749d ; native 7495
    cmp byte ptr [bp-8h], 1h ; native 7497
    jnz SHORT turn_74b9 ; native 749B
turn_749d:
    shl word ptr [si+0ch], 1h ; native 749D
    mov al, 14h ; native 74A0
    mul byte ptr [bp-8h] ; native 74A2
    mov bx, ax ; native 74A5
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 74A7
    mov ax, word ptr [bp-6h] ; native 74AB
    and al, 0feh ; native 74AE
    add bx, ax ; native 74B0
    mov ax, word ptr [bx] ; native 74B2
    mov word ptr [bp-0ch], ax ; native 74B4
    jmp SHORT turn_74d0 ; native 74B7
turn_74b9:
    mov al, 14h ; native 74B9
    mul byte ptr [bp-8h] ; native 74BB
    mov bx, ax ; native 74BE
    mov bx, word ptr [bx+_asset_groups-0ch] ; native 74C0
    mov ax, word ptr [bp-6h] ; native 74C4
    shl ax, 1h ; native 74C7
    add bx, ax ; native 74C9
    mov ax, word ptr [bx] ; native 74CB
    mov word ptr [bp-0ch], ax ; native 74CD
turn_74d0:
    mov bx, word ptr [bp-0ch] ; native 74D0
    add word ptr [bp-0ch], 2h ; native 74D3
    mov ax, word ptr [bx] ; native 74D7
    mov cl, 3h ; native 74D9
    shl ax, cl ; native 74DB
    add ax,OFFSET DGROUP:_frames ; native 74DD
    mov word ptr [bp-4h], ax ; native 74E0
    push di ; native 74E3
    push ax ; native 74E4
    mov al, byte ptr [di+0ah] ; native 74E5
    sub ah, ah ; native 74E8
    push ax ; native 74EA
    push word ptr [di+6h] ; native 74EB
    push word ptr [di+4h] ; native 74EE
    call NEAR PTR _attach_actor ; native 74F1
    add sp, 0ah ; native 74F4
    mov word ptr [di+8h], 0h ; native 74F7
turn_74fc:
    cmp word ptr [si+0ch], 0h ; native 74FC
    jge SHORT turn_7506 ; native 7500
    sub bx, bx ; native 7502
    jmp SHORT turn_7509 ; native 7504
turn_7506:
    mov bx, 1h ; native 7506
turn_7509:
    mov ax, word ptr [bp-0eh] ; native 7509
    shl ax, 1h ; native 750C
    add bx, ax ; native 750E
    shl bx, 1h ; native 7510
    mov al, 30h ; native 7512
    mul byte ptr [bp-8h] ; native 7514
    add bx, ax ; native 7517
    mov ax, word ptr [bx+_piece_controls+10h] ; native 7519
    mov word ptr [si+4h], ax ; native 751D
    mov byte ptr [si+2h], 0h ; native 7520
    push si ; native 7524
    call NEAR PTR _task_ready_772d ; native 7525
    add sp, 2h ; native 7528
    jmp SHORT turn_756a ; native 752B
turn_752d:
    mov ax, word ptr [di+14h] ; native 752D
    mov word ptr [bp-4h], ax ; native 7530
    call NEAR PTR _pop_value ; native 7533
    mov word ptr [bp-2h], ax ; native 7536
    push ax ; native 7539
    mov bx, word ptr [bp-0ch] ; native 753A
    add word ptr [bp-0ch], 2h ; native 753D
    push word ptr [bx] ; native 7541
    push word ptr [bp-4h] ; native 7543
    call NEAR PTR _compose_frame_3b3a ; native 7546
    add sp, 6h ; native 7549
    mov ax, word ptr [bp-2h] ; native 754C
    mov word ptr [bp-4h], ax ; native 754F
    push di ; native 7552
    push ax ; native 7553
    mov al, byte ptr [di+0ah] ; native 7554
    sub ah, ah ; native 7557
    push ax ; native 7559
    push word ptr [di+2h] ; native 755A
    push word ptr [di] ; native 755D
    call NEAR PTR _attach_actor ; native 755F
    add sp, 0ah ; native 7562
    mov word ptr [di+8h], 1h ; native 7565
turn_756a:
    mov bx, word ptr [bp-0ch] ; native 756A
    cmp word ptr [bx], -1h ; native 756D
    jnz SHORT turn_7577 ; native 7570
    mov word ptr [bp-0ch], 0h ; native 7572
turn_7577:
    mov ax, word ptr [bp-0ch] ; native 7577
    mov word ptr [si], ax ; native 757A
    mov al, byte ptr [bp-0eh] ; native 757C
    mov byte ptr [si+0eh], al ; native 757F
    sub ax, ax ; native 7582
    jmp SHORT turn_7586 ; native 7584
turn_7586:
    pop si ; native 7586
    pop di ; native 7587
    mov sp, bp ; native 7588
    pop bp ; native 758A
    ret ; native 758B
_turn_task_730c ENDP
_TEXT ENDS
END
