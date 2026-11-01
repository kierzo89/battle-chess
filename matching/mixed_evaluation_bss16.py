"""Finite evaluation3902 BSS capability, staged; no canonical admission."""
from pathlib import Path
from functools import lru_cache
from mixed_graphics_client_frames16 import ClosedClientFrames

@lru_cache(maxsize=1)
def contract():
    return ClosedClientFrames(Path(__file__).with_name('mixed_evaluation_bss_contract.json').read_bytes(), 'bff1ee8a7ab715b6b9f4f50048af464689bc06d6d95240178abe86806dde79b1')

def validate_client_frame(row, raw, field, symbol):
    return contract().validate(row, raw, field, symbol)
