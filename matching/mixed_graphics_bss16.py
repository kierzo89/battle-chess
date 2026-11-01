"""Finite graphics7262 BSS capability, staged; no canonical admission."""
from pathlib import Path
from functools import lru_cache
from mixed_graphics_client_frames16 import ClosedClientFrames

@lru_cache(maxsize=1)
def contract():
    return ClosedClientFrames(Path(__file__).with_name('mixed_graphics_bss_contract.json').read_bytes(), 'e60153d9e88bf33d398df521ebfeccc8f5b08e6514c3da9765f663ec9b355e83')

def validate_client_frame(row, raw, field, symbol):
    return contract().validate(row, raw, field, symbol)
