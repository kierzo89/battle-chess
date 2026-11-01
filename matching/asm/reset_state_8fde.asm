; REA ev_40aa5b5ba50bb8039db8c1eacd0a772fa6fd96763982b6bbd7ea22c8b95fd685.
; Exact image 8F88..8F95. Callees still unnamed; no subsystem claim.
bits 16
cpu 8086
org 0x8f88

    call 0x7da8
    call 0x950d
    mov word [0x8fde], 0
    ret
