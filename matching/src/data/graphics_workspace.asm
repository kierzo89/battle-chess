; Opaque physical decoded-image DATA representation, not an original C object.
; The two initialized pieces are an engineering OMF16 split, not historical SEGDEFs.
; No C capacity, initialized-source storage class, TU or semantic subregion claim.
GRAPHICS_WORKSPACE_0 SEGMENT PARA 'FAR_DATA'
PUBLIC _graphics_workspace, _metadata_workspace
_graphics_workspace LABEL BYTE
    DB 0CC6Ch DUP (0)
_metadata_workspace LABEL BYTE
    DB 03384h DUP (0)
GRAPHICS_WORKSPACE_0 ENDS

GRAPHICS_WORKSPACE_1 SEGMENT PARA 'FAR_DATA'
    DB 05000h DUP (0)
GRAPHICS_WORKSPACE_1 ENDS
END
