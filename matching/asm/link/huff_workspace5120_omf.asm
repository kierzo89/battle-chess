; Engineering physical DATA partition, NOT recovered historical C/ASM ownership.
; Whole shipped zero component DS30CC..44CC: 5120 initialized image bytes.
; Current native consumers justify exactly the three PUBLIC starting views.
; Initializing these zeros is an explicit new-source materialization choice;
; original object literal/reservation distinction and TU/class remain unknown.
; No opcode bytes, numeric pointers, aliases, ORG, ALIGN or reserved '?' bytes.
_DATA SEGMENT WORD PUBLIC 'DATA'
PUBLIC _huff_code_table
PUBLIC _huff_fast_lookup
PUBLIC _huff_long_records
_huff_code_table LABEL WORD
; Native STOSW512; byte-symbol-indexed256 records,4 bytes each.
DW 512 DUP (0)
_huff_fast_lookup LABEL BYTE
; Native byte-prefix-indexed256 records: length, symbol, near record pointer.
DW 512 DUP (0)
_huff_long_records LABEL BYTE
; Native consumed-record prefix bound256x4. No declaration of768 records.
DW 512 DUP (0)
; Physical zero tail2048: no PUBLIC, semantic type, logical capacity or owner.
; This is real shipped zero storage, NOT function/instruction alignment padding.
DW 1024 DUP (0)
_DATA ENDS
DGROUP GROUP _DATA
END
