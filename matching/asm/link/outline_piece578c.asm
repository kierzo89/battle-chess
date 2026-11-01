; Authored symbolic ASM reconstruction, not historical source attribution.
; C reconstruction remains HELD. Native frame twelve is reproduced as ABI state.
.8086
_DATA SEGMENT WORD PUBLIC 'DATA'
EXTRN _dirty_left:WORD, _dirty_right:WORD, _dirty_top:WORD
EXTRN _dirty_bottom:WORD, _region_left:WORD
_DATA ENDS
DGROUP GROUP _DATA
EXTRN __chkstk:NEAR
EXTRN _mark_region_41a8:NEAR, _render_42a0:NEAR
EXTRN _select_pen_5b18:NEAR, _move_pen_5b3d:NEAR, _line_pen_5b55:NEAR
_TEXT SEGMENT WORD PUBLIC 'CODE'
ASSUME CS:_TEXT, DS:DGROUP, SS:DGROUP
PUBLIC _outline_piece_578c
_outline_piece_578c PROC NEAR
    push bp ; native 578C
    mov bp,sp ; native 578D
    mov ax,0ch ; native 578F
    call NEAR PTR __chkstk ; native 5792
    push di ; native 5795
    push si ; native 5796
    mov si,WORD PTR [bp+4] ; native 5797
    add si,WORD PTR [bp+8] ; native 579A
    dec si ; native 579D
    mov di,WORD PTR [bp+6] ; native 579E
    add di,WORD PTR [bp+0ah] ; native 57A1
    dec di ; native 57A4
    mov ax,WORD PTR [bp+4] ; native 57A5
    sar ax,1 ; native 57A8
    sar ax,1 ; native 57AA
    mov _dirty_left,ax ; native 57AC
    mov ax,si ; native 57AF
    sar ax,1 ; native 57B1
    sar ax,1 ; native 57B3
    mov _dirty_right,ax ; native 57B5
    mov ax,WORD PTR [bp+6] ; native 57B8
    mov _dirty_top,ax ; native 57BB
    mov _dirty_bottom,di ; native 57BE
    cmp WORD PTR _dirty_left,0 ; native 57C2
    jge SHORT left_clipped ; native 57C7
    mov WORD PTR _dirty_left,0 ; native 57C9
left_clipped:
    cmp WORD PTR _dirty_right,79 ; native 57CF
    jle SHORT right_clipped ; native 57D4
    mov WORD PTR _dirty_right,79 ; native 57D6
right_clipped:
    cmp WORD PTR _dirty_top,0 ; native 57DC
    jge SHORT top_clipped ; native 57E1
    mov WORD PTR _dirty_top,0 ; native 57E3
top_clipped:
    cmp WORD PTR _dirty_bottom,199 ; native 57E9
    jle SHORT bottom_clipped ; native 57EF
    mov WORD PTR _dirty_bottom,199 ; native 57F1
bottom_clipped:
    sub ax,ax ; native 57F7
    push ax ; native 57F9
    call NEAR PTR _mark_region_41a8 ; native 57FA
    add sp,2 ; native 57FD
    cmp WORD PTR [bp+0ch],0 ; native 5800
    jne SHORT draw_outline ; native 5804
    jmp NEAR PTR render_outline ; native 5806
draw_outline:
    push WORD PTR [bp+0ch] ; native 5809
    call NEAR PTR _select_pen_5b18 ; native 580C
    add sp,2 ; native 580F
    mov ax,_region_left ; native 5812
    sub WORD PTR [bp+4],ax ; native 5815
    sub si,ax ; native 5818
    sub ax,ax ; native 581A
    push ax ; native 581C
    push WORD PTR [bp+4] ; native 581D
    call NEAR PTR _move_pen_5b3d ; native 5820
    add sp,4 ; native 5823
    sub ax,ax ; native 5826
    push ax ; native 5828
    push si ; native 5829
    call NEAR PTR _line_pen_5b55 ; native 582A
    add sp,4 ; native 582D
    mov ax,di ; native 5830
    sub ax,WORD PTR [bp+6] ; native 5832
    push ax ; native 5835
    push si ; native 5836
    call NEAR PTR _line_pen_5b55 ; native 5837
    add sp,4 ; native 583A
    mov ax,di ; native 583D
    sub ax,WORD PTR [bp+6] ; native 583F
    push ax ; native 5842
    push WORD PTR [bp+4] ; native 5843
    call NEAR PTR _line_pen_5b55 ; native 5846
    add sp,4 ; native 5849
    sub ax,ax ; native 584C
    push ax ; native 584E
    push WORD PTR [bp+4] ; native 584F
    call NEAR PTR _line_pen_5b55 ; native 5852
    add sp,4 ; native 5855
    mov ax,1 ; native 5858
    push ax ; native 585B
    mov ax,WORD PTR [bp+4] ; native 585C
    inc ax ; native 585F
    push ax ; native 5860
    call NEAR PTR _move_pen_5b3d ; native 5861
    add sp,4 ; native 5864
    mov ax,1 ; native 5867
    push ax ; native 586A
    lea ax,[si-1] ; native 586B
    push ax ; native 586E
    call NEAR PTR _line_pen_5b55 ; native 586F
    add sp,4 ; native 5872
    mov ax,di ; native 5875
    sub ax,WORD PTR [bp+6] ; native 5877
    dec ax ; native 587A
    push ax ; native 587B
    lea ax,[si-1] ; native 587C
    push ax ; native 587F
    call NEAR PTR _line_pen_5b55 ; native 5880
    add sp,4 ; native 5883
    mov ax,di ; native 5886
    sub ax,WORD PTR [bp+6] ; native 5888
    dec ax ; native 588B
    push ax ; native 588C
    mov ax,WORD PTR [bp+4] ; native 588D
    inc ax ; native 5890
    push ax ; native 5891
    call NEAR PTR _line_pen_5b55 ; native 5892
    add sp,4 ; native 5895
    mov ax,1 ; native 5898
    push ax ; native 589B
    mov ax,WORD PTR [bp+4] ; native 589C
    inc ax ; native 589F
    push ax ; native 58A0
    call NEAR PTR _line_pen_5b55 ; native 58A1
    add sp,4 ; native 58A4
render_outline:
    call NEAR PTR _render_42a0 ; native 58A7
    pop si ; native 58AA
    pop di ; native 58AB
    mov sp,bp ; native 58AC
    pop bp ; native 58AE
    ret ; native 58AF
_outline_piece_578c ENDP
_TEXT ENDS
END
