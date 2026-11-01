; PREPARATION ONLY. Explicit mixed physical-carrier policy approval still required.
; Reconstructs original loaded FILE bytes, not a recovered C function/capacity/TU.
; All four real entry cells are overwritten by the selected raw graphics asset.
; The initial branch landing bytes are observed zeros, not an invented RETF stub.
.8086
GRAPHICS_DRIVER_CARRIER SEGMENT PARA 'CODE'
ASSUME CS:GRAPHICS_DRIVER_CARRIER
PUBLIC _graphics_copy, _graphics_rect_110d_0003
PUBLIC _graphics_pointer_110d_0006, _graphics_pointer_110d_0009
PUBLIC _graphics_driver_colour_110dc
_graphics_copy LABEL FAR
    jmp NEAR PTR unloaded_branch_landing
_graphics_rect_110d_0003 LABEL FAR
    jmp NEAR PTR unloaded_branch_landing
_graphics_pointer_110d_0006 LABEL FAR
    jmp NEAR PTR unloaded_branch_landing
_graphics_pointer_110d_0009 LABEL FAR
    jmp NEAR PTR unloaded_branch_landing
; Genuine consumed byte at image110DC, overwritten by asset loading and pen writes.
_graphics_driver_colour_110dc LABEL BYTE
    DB 0
; Physical zero packet slice13..E1D, not an array capacity/reserve declaration.
    DB 3600 DUP (0)
; Private coordinate justified by all four original relative JMP operands.
; LABEL NEAR deliberately supplies no function, return or callable fallback.
unloaded_branch_landing LABEL NEAR
    DB 3 DUP (0)
GRAPHICS_DRIVER_CARRIER ENDS
END
