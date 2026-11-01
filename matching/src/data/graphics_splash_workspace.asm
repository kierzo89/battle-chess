; Same opaque physical86000 initialized bytes; engineering partition, not C capacity.
; This boundary supplies the native segment-relative splash view; no new allocation.
GRAPHICS_WORKSPACE_0 SEGMENT PARA 'FAR_DATA'
PUBLIC _graphics_workspace, _metadata_workspace
_graphics_workspace LABEL BYTE
    DB 0CC6Ch DUP (0)
_metadata_workspace LABEL BYTE
    DB 00354h DUP (0)
GRAPHICS_WORKSPACE_0 ENDS

GRAPHICS_WORKSPACE_1 SEGMENT PARA 'FAR_DATA'
PUBLIC _splash_buffer
_splash_buffer LABEL BYTE
    DB 08030h DUP (0)
GRAPHICS_WORKSPACE_1 ENDS
END
