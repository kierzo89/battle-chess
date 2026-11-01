"""Closed C5 initialized sixteen-WORD colour-table profile; staged, zero canonical credit.

This reads the unchanged checksum-validated OMF. It neither clears unsupported
flags nor manufactures LEDATA for uninitialized holes. Ordinary cdata and omf
remain unchanged. Generation accepts no target/reference/placement argument.
"""
from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path

from msc import compile_c, validate_toolchain
from omf import read_omf, OMFError

BACKEND = 'msc500-text-colour-data-omf'
SYMBOL = '_text_colour_words'
FLAGS = ['/AS', '/Zl', '/Zi']
SOURCE_SHA256 = '8537267304fb24a9d26a29fbba5240de7c0fc70e7a23402ded1a988ec00375f9'
NEGATIVE_SOURCE_SHA256 = '1b4b382c732910e75d6f5d894017ed5d5ead06383775efc28c799f3105c1a737'
REVIEWED_SOURCE_HASHES = {SOURCE_SHA256, NEGATIVE_SOURCE_SHA256}
MANIFEST_SHA256 = 'd2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOL_HASHES = {
 'CL.ERR':'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a',
 'CL.EXE':'11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504',
 'C1.EXE':'3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791',
 'C1.ERR':'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233',
 'C2.EXE':'19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1',
 'C3.EXE':'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669',
 'C23.ERR':'75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
CV = bytes.fromhex('01010080010100800101008001070078850001838100')
KINDS = [0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0x90,0x88,0xa0,0xa2,0xa0,0x8a]

class TextColourDataError(OMFError):
    pass


def require(condition, message):
    if not condition:
        raise TextColourDataError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate_unit(unit):
    require(unit.get('language') == 'c-data' and unit.get('backend') == BACKEND,
            'text colour DATA backend/language mismatch')
    require(unit.get('symbol') == SYMBOL and unit.get('flags') == FLAGS,
            'text colour DATA symbol/flags mismatch')
    require(unit.get('size') == 32 and unit.get('reference_region') == 'exepack-expanded',
            'text colour DATA comparison extent/profile mismatch')
    require(unit.get('externals') == {} and not any(unit.get(k) is not None
            for k in ('owned_data','owned_const','owned_bss','extended_extent','code_address','data_address')),
            'text colour DATA admits no external placement or function ownership')


def extract_data(object_bytes, symbol=SYMBOL):
    """Decode only the complete independently declared DATA32 profile.

    Input is raw OMF, never a fabricated OMFObject. read_omf validates the entire
    record stream/checksums/EOF first. The sole supported LIDATA is one leaf,
    with repeat15, literal0000, at offset2 following one real LEDATA WORD at offset0.
    Array extent is cross-checked against SEGDEF, CV and actual decoded length.
    No expected unit size or target bytes participate.
    """
    require(isinstance(object_bytes, bytes), 'text colour DATA requires unchanged raw object bytes')
    require(symbol == SYMBOL, 'text colour DATA unexpected public selection')
    obj = read_omf(object_bytes)
    require([k for k,_,_ in obj.records] == KINDS, 'text colour DATA unreviewed record sequence/allocation')
    require(obj.names == ['', '', 'DGROUP', '_TEXT', 'CODE', '_DATA', 'DATA', 'CONST',
                          '_BSS', 'BSS', '$$TYPES', 'DEBTYP', '$$SYMBOLS', 'DEBSYM'],
            'text colour DATA LNAMES/group identity changed')
    expected = [('_TEXT','CODE',0,0x48),('_DATA','DATA',32,0x48),
                ('CONST','CONST',0,0x48),('_BSS','BSS',0,0x48),
                ('$$SYMBOLS','DEBSYM',0,0x20),('$$TYPES','DEBTYP',22,0x20)]
    require([(s.name,s.class_name,s.length,s.attributes) for s in obj.segments.values()] == expected,
            'text colour DATA segment allocations/attributes changed')
    require([b.hex() for k,_,b in obj.records if k==0x98] ==
            ['480000030401','482000050601','480000070701','480000080901',
             '2000000c0d01','2016000a0b01'],
            'text colour DATA SEGDEF identity/overlay indices changed')
    require(not obj.fixups and not obj.procedures, 'text colour DATA forbids actual fixup fields/procedures')
    require(obj.externals == {1:'__acrtused'}, 'text colour DATA startup marker/externals changed')
    require(len(obj.publics) == 1 and SYMBOL in obj.publics, 'text colour DATA public identity/count changed')
    p = obj.publics[SYMBOL]
    require((p.segment,p.offset,p.group,p.type_index)==(2,0,1,515), 'text colour DATA public/group/CV type changed')
    # Thread-only FIXUPP is real compiler metadata, not a relocation field.
    fixed = {0x80:[b'\x09C:\\UNIT.C'], 0x88:[bytes.fromhex(x) for x in
             ('009d30734f','00a1014356','00a201')],
             0x9a:[bytes.fromhex('02ff03ff04ff02')],
             0x9c:[bytes.fromhex('000301020201030440014501')],0x8a:[b'\0']}
    for kind, payloads in fixed.items():
        require([b for k,_,b in obj.records if k==kind] == payloads,
                'text colour DATA group/startup/header directive changed')
    require(len(obj.segments[2].chunks)==1 and obj.segments[2].chunks[0][0]==0 and len(obj.segments[2].chunks[0][1])==2 and obj.segments[2].unsupported_data,
            'text colour DATA requires one complete explicit first-WORD LEDATA')
    require(all(not s.chunks and not s.unsupported_data for i,s in obj.segments.items() if i not in (2,6)),
            'text colour DATA extra initialized allocation')
    require(obj.segments[6].chunks == [(0,CV)] and not obj.segments[6].unsupported_data,
            'text colour DATA complete CV unsigned-int array profile changed')
    # Retain all CV records, including their independent index sequence. The
    # source pin establishes unsigned-int semantics; raw 0x81 element encoding
    # is recorded rather than generalized to other CV dialects.
    types=[];at=0
    while at<len(CV):
        size=int.from_bytes(CV[at+1:at+3],'little')
        raw=CV[at:at+3+size]
        types.append({'type_index':0x200+len(types),'offset':at,'raw_hex':raw.hex(),'leaf':raw[3]})
        at += len(raw)
    array=bytes.fromhex(types[-1]['raw_hex'])
    bit_size=int.from_bytes(array[5:7],'little')
    require(types[-1]['type_index']==p.type_index and array[7:]==bytes.fromhex('838100') and bit_size==256 and bit_size%16==0 and bit_size//16==16 and bit_size//8==obj.segments[2].length,
            'text colour DATA CV/SEGDEF capacity disagreement')
    record=next((at,b)for k,at,b in obj.records if k==0xa2)
    payload=record[1]
    require(len(payload)==10, 'text colour DATA malformed/trailing LIDATA leaf')
    segment=payload[0];offset=int.from_bytes(payload[1:3],'little')
    count=int.from_bytes(payload[3:5],'little');children=int.from_bytes(payload[5:7],'little')
    literal_length=payload[7];literal=payload[8:]
    require(segment==2 and offset==2, 'text colour DATA foreign/overlapping/holey LIDATA extent')
    require(children==0 and literal_length==2 and len(literal)==literal_length,
            'text colour DATA nested/malformed LIDATA is unsupported')
    require(count==15 and literal==b'\0\0', 'text colour DATA unreviewed repeat count/literal')
    repeated=literal*count
    data=obj.segments[2].chunks[0][1]+repeated
    require(len(data)==obj.segments[2].length==bit_size//8, 'text colour DATA incomplete initialized ownership')
    return data, {'boundary':'complete_omf_data_segment','symbol':SYMBOL,
        'segment':{'index':2,'name':'_DATA','class_name':'DATA','length':len(data),'attributes':0x48},
        'public':asdict(p),'publics':{SYMBOL:asdict(p)},
        'group':{'index':1,'name':'DGROUP','segments':[3,4,2]},
        'data_writes':[{'kind':'LEDATA','offset':0,'length':2,'literal_hex':obj.segments[2].chunks[0][1].hex()},
          {'kind':'LIDATA','record_offset':record[0],'raw_payload':payload.hex(),'offset':offset,
           'repeat_count':count,'child_blocks':children,'literal_hex':literal.hex(),'length':len(repeated)}],
        'cv':{'records':types,'array_bit_size':bit_size,'array_elements':16,'element_bits':16,
              'element_type_raw':'838100','source_declared_type':'unsigned int[16]','raw_hex':CV.hex()},
        'all_segments':[{'index':s.index,'name':s.name,'class_name':s.class_name,'length':s.length,
            'attributes':s.attributes,'unsupported_data_retained':s.unsupported_data}for s in obj.segments.values()],
        'object_sha256':sha(object_bytes),'sha256':sha(data),'startup_marker_unused':True,
        'thread_only_FIXUPP_retained':True,'emitted_mz_sites':[], 'authored_c_function_count':0,
        'historical_array_capacity_proven':False,'native_consumed_minimum':32,'native_write_count_WORDs':16,'native_lookup_mask':30,'reviewed_semantic_negative_first_WORD_permitted_for_comparison':True}


def validate_compiled(compiled, source_bytes):
    require(sha(source_bytes)in REVIEWED_SOURCE_HASHES and compiled.source_sha256==sha(source_bytes),
            'text colour DATA reviewed source fingerprint changed')
    require(compiled.compiler=='msc500' and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C',
            'text colour DATA compiler/profile changed')
    require(compiled.toolchain_manifest_sha256==MANIFEST_SHA256 and compiled.tool_hashes==TOOL_HASHES,
            'text colour DATA pinned compiler tools/manifest changed')
    require(tuple(compiled.command)==('T:\\CL.EXE','/c',*FLAGS,'/FoC:\\UNIT.OBJ','C:\\UNIT.C'),
            'text colour DATA compiler command changed')
    return extract_data(compiled.object_bytes)


@dataclass(frozen=True)
class Built:
    object_bytes: bytes
    data: bytes
    metadata: dict
    provenance: dict


def build(source):
    """Fresh source-only generation. No target is read or mounted."""
    source=Path(source);before=source.read_bytes()
    require(sha(before)in REVIEWED_SOURCE_HASHES, 'text colour DATA reviewed source fingerprint changed')
    manifest,tools=validate_toolchain(compiler='msc500')
    require(manifest==MANIFEST_SHA256 and tools==TOOL_HASHES, 'text colour DATA tool pins changed')
    compiled=compile_c(source,FLAGS,compiler='msc500')
    require(source.read_bytes()==before, 'text colour DATA source changed during generation')
    data,metadata=validate_compiled(compiled,before)
    provenance=asdict(compiled);provenance.pop('object_bytes')
    return Built(compiled.object_bytes,data,metadata,provenance)
