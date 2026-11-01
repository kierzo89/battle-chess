; Engineering physical initialized DATA fragment, NOT two C[20] arrays.
; Original DS103E..1066; independently owned menu data begins1066.
; Each value below is observed in the initialized decoded image and REA40.
; Historical allocation, capacity and TU boundaries remain unknown.
bits 16
cpu 8086
segment _DATA public align=2 class=DATA use16
group DGROUP _DATA
global _left_list_scratch
global _right_list_scratch
_left_list_scratch:
    dw 0x00ff,0,0,0,0 ; bytes0..9: valid-list operational minimum10
    dw 0,0,0,0,0 ; bytes10..19: opaque observed initialized bytes
_right_list_scratch:
    dw 0x00ff,0,0,0,0,0 ; bytes20..31: operational minimum12
    dw 0,0,0,0 ; bytes32..39: opaque observed initialized bytes
