; Diagnostic C ABI adapter: the actual helper returns SI and clobbers flags.
bits 16
cpu 8086
segment _TEXT public align=2 class=CODE use16
global _invoke_huff_refill
extern _huff_refill_e3ea
_invoke_huff_refill:
    push si
    call _huff_refill_e3ea
    mov ax,si
    pop si
    ret
