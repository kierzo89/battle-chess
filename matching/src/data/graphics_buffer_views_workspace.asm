; Same admitted physical86000 initialized bytes; two real interior BYTE views.
; Labels express native far coordinates, not C object capacities or historical TU.
GRAPHICS_WORKSPACE_0 SEGMENT PARA 'FAR_DATA'
PUBLIC _graphics_workspace, _color_buffer, _region_buffer, _metadata_workspace
_graphics_workspace LABEL BYTE
    DB 032E0h DUP (0)
_color_buffer LABEL BYTE
    DB 00CB0h DUP (0)
_region_buffer LABEL BYTE
    DB 08CDCh DUP (0)
_metadata_workspace LABEL BYTE
    DB 00354h DUP (0)
GRAPHICS_WORKSPACE_0 ENDS

GRAPHICS_WORKSPACE_1 SEGMENT PARA 'FAR_DATA'
PUBLIC _splash_buffer
_splash_buffer LABEL BYTE
    DB 08030h DUP (0)
GRAPHICS_WORKSPACE_1 ENDS
END
