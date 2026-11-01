"""Two exact mixed460 external-frame BSS clients; no generic frame relaxation.

The caller still proves the sole physical PUBLIC provider, DGROUP membership,
actual LINK word, complete file range and absence of MZ overlap.
"""
import hashlib
RAW_SHA256='8ffb303e79a7c818b2efa5ee616c5c6d8a3708c4c9868da610519dfa1c640ea6'
ALLOWED={343:('_stride',3,None,'c557260303'),421:('_packed_pen',11,None,'c5a5260b0b')}
def validate_client_frame(row,raw,f,symbol):
 from mixed_remove460_pipeline16 import OWNERS,C_SOURCE_SHA256
 assert hashlib.sha256(raw).hexdigest()==RAW_SHA256,'exact whole mixed460 object'
 assert row['kind']=='mixed-c-fa-authored-asm-whole-omf' and row['source']=='src/remove_neighbors_match.c' and row['source_sha256']==C_SOURCE_SHA256 and row['selected_owners']==OWNERS,'exact mixed460 source/owner contract'
 assert f.offset in ALLOWED and (symbol,f.target[1],f.displacement,f.raw.hex())==ALLOWED[f.offset],'exact two mixed460 fields'
 assert f.frame==(2,f.target[1]) and f.target[0]==2 and f.segment==1 and f.width==2 and f.location_type==1 and f.segment_relative is True,'actual F2 external frame, never normalized'
 return 'proven_MIXED460_external_PUBLIC_group1'
