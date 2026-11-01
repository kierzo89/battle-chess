"""Closed relocatable 50-byte BIOS CODE contribution; no C or extra ASM credit.

Generation accepts source/tool pins only. Original bytes enter comparison only
following complete fresh SEGDEF extraction. No target bounds select output.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
from omf import OMFError, OMFObject, read_omf

class ASMCodeError(OMFError):
    pass

SOURCE_SHA256 = 'c020eb418999014cd0a671e6f4009e3d178b7b79eb139e0df90c235a56c766c1'
NASM_SHA256 = '57b8fc5957237b0d9b1ff48c8f5823780fb8ce968d9b8434850c06941ad5d5f5'
ORIGINAL_SHA256 = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BASE = 0xea32
PUBLICS = {'_poll_event': 0, '_ticks_ea5b': 41}
UNITS = {'poll_event_ea32': ('_poll_event', 'evidence/rea_newinput_poll_ea32.json'),
         'bios_ticks_ea5b': ('_ticks_ea5b', 'evidence/rea_newinput_delay_ea5b.json')}
RAW_EVIDENCE = 'evidence/rea_newinput_bios_full_context.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def validate_unit(unit):
    if (unit.get('language'), unit.get('backend'), unit.get('source'), unit.get('object_profile')) != (
            'asm', 'nasm-code-omf', 'asm/link/bios_input_omf.asm', 'bios_input'):
        raise ASMCodeError('Requires closed BIOS relocatable CODE profile')
    if unit.get('source_sha256') != SOURCE_SHA256 or unit.get('assembler_sha256') != NASM_SHA256:
        raise ASMCodeError('Requires pinned BIOS source and NASM')
    row = UNITS.get(unit.get('id'))
    if row is None or (unit.get('symbol'), unit.get('rea_evidence')) != row:
        raise ASMCodeError('Requires actual BIOS public/native evidence identity')
    symbol = row[0]; offset = PUBLICS[symbol]
    size = (list(PUBLICS.values())[1:] + [50])[list(PUBLICS).index(symbol)] - offset
    if (type(unit.get('size')) is not int or unit['size'] != size
            or unit.get('image_offset') != hex(BASE + offset)
            or unit.get('reference_region', 'unchanged-prefix') != 'unchanged-prefix'):
        raise ASMCodeError('Unit differs from complete public-derived extent')
    for key in ('externals','flags','symbols','extended_extent','owned_const','owned_data',
                'owned_bss','data_address','code_address','end_symbol'):
        if key in unit:
            raise ASMCodeError('Closed BIOS CODE forbids foreign bindings, slices and ownership')

def extract_code(obj):
    """Return every initialized byte of the independent SEGDEF, no unit input."""
    if not isinstance(obj, OMFObject) or set(obj.segments) != {1}:
        raise ASMCodeError('Requires one strict OMF segment')
    if obj.externals or obj.fixups:
        raise ASMCodeError('BIOS CODE forbids externals/fixups')
    for kind, _, payload in obj.records:
        if kind not in (0x80,0x88,0x96,0x98,0x90,0xa0,0x8a):
            raise ASMCodeError('BIOS CODE forbids group/COMM/LIDATA/auxiliary records')
        if kind == 0x88 and not (payload.startswith(b'\0\0') or payload == b'\x40\xa2\x01'):
            raise ASMCodeError('BIOS CODE forbids linker directives')
        if kind == 0x8a and payload != b'\0':
            raise ASMCodeError('BIOS CODE forbids entry points')
    seg = obj.segments[1]
    if (seg.index,seg.name,seg.class_name,seg.attributes,seg.length,seg.unsupported_data) != (
            1,'_TEXT','CODE',0x48,50,False):
        raise ASMCodeError('Requires complete WORD PUBLIC USE16 BIOS CODE50')
    publics = sorted(obj.publics.values(),key=lambda p:p.offset)
    if ({p.name:p.offset for p in publics} != PUBLICS or len(publics) != 2
            or any((p.segment,p.group,p.type_index) != (1,0,0) for p in publics)):
        raise ASMCodeError('Requires exactly two unaliased actual BIOS publics')
    data = bytearray()
    for offset,content in sorted(seg.chunks):
        if not content or offset != len(data) or offset + len(content) > seg.length:
            raise ASMCodeError('CODE hole/overlap/empty or excess LEDATA')
        data.extend(content)
    if len(data) != seg.length:
        raise ASMCodeError('Uninitialized or omitted CODE tail')
    extents = []
    for i,p in enumerate(publics):
        end = publics[i+1].offset if i+1 < len(publics) else seg.length
        extents.append({'symbol':p.name,'offset':p.offset,'size':end-p.offset})
    return bytes(data), {'boundary':'complete_asm_CODE_SEGDEF',
        'segment':{'index':1,'name':seg.name,'class_name':seg.class_name,
                   'attributes':seg.attributes,'length':seg.length},
        'publics':[asdict(p) for p in publics], 'public_extents':extents,
        'sha256':digest(data),'emitted_mz_sites':[],'authored_c_credit':0}

def public_extent(metadata,symbol):
    # Metadata is required to be the result of extraction, not user ranges.
    if (metadata.get('boundary') != 'complete_asm_CODE_SEGDEF'
            or metadata.get('segment',{}).get('length') != 50
            or metadata.get('public_extents') != [
                {'symbol':'_poll_event','offset':0,'size':41},
                {'symbol':'_ticks_ea5b','offset':41,'size':9}]):
        raise ASMCodeError('Invalid independent complete PUBLIC extent metadata')
    for row in metadata['public_extents']:
        if row['symbol'] == symbol:return row['offset'],row['size']
    raise ASMCodeError('Unknown BIOS public')

@dataclass(frozen=True)
class Build:
    object_bytes: bytes
    code: bytes
    metadata: dict
    provenance: dict

def assemble(source,unit,nasm='nasm'):
    validate_unit(unit)
    source = Path(source);source_bytes = source.read_bytes()
    if digest(source_bytes) != SOURCE_SHA256:
        raise ASMCodeError('BIOS source hash mismatch; no includes/ORG/blob changes admitted')
    executable = shutil.which(nasm)
    if executable is None:raise ASMCodeError('NASM unavailable')
    executable = Path(executable).resolve()
    if digest(executable.read_bytes()) != NASM_SHA256:raise ASMCodeError('NASM pin mismatch')
    with tempfile.TemporaryDirectory(prefix='bc-asm-code-') as tmp:
        tmp = Path(tmp);(tmp/'UNIT.ASM').write_bytes(source_bytes)
        command = [str(executable),'-f','obj','-Ox','UNIT.ASM','-o','UNIT.OBJ']
        result = subprocess.run(command,cwd=tmp,capture_output=True,text=True,timeout=30)
        if result.returncode or not (tmp/'UNIT.OBJ').is_file():
            raise ASMCodeError('Assembly failed: '+result.stdout+result.stderr)
        raw = (tmp/'UNIT.OBJ').read_bytes()
    if digest(executable.read_bytes()) != NASM_SHA256:raise ASMCodeError('NASM changed')
    code,metadata = extract_code(read_omf(raw))
    return Build(raw,code,metadata,{'source_sha256':digest(source_bytes),
        'assembler_sha256':NASM_SHA256,'assembler_path':str(executable),
        'build_command':command,'assembler_log':result.stdout+result.stderr,
        'object_sha256':digest(raw),'object_format':'OMF16','fresh_directory':True})

def _subject(e):
    if (e.get('analysis_profile',{}).get('digest') != '894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
            or e.get('subject',{}).get('format') != 'dos-mz'
            or e.get('subject',{}).get('digest',{}).get('sha256') != ORIGINAL_SHA256
            or e.get('provider',{}).get('id') != 'ghidra'
            or any(e.get('analysis_profile',{}).get('parameters',{}).get(k) != v for k,v in {
                'load_segment':'0x1000','loader':'MzLoader','target_format':'dos-mz',
                'language_id':'x86:LE:16:Real Mode','address_coordinates':'linear-byte-offset'}.items())):
        raise ASMCodeError('Wrong original subject or loader profile')

def validate_comparison(unit,built,image,project,original_sites):
    """Post-generation whole/raw/native/public MZ equality; no masked bytes."""
    validate_unit(unit)
    code,metadata = extract_code(read_omf(built.object_bytes))
    if code != built.code or metadata != built.metadata:
        raise ASMCodeError('Build bytes/metadata differ from complete independent object')
    offset,size = public_extent(metadata,unit['symbol'])
    if size != unit['size']:raise ASMCodeError('Selected extent is not complete public')
    if len(image) < BASE + len(code) or image[BASE:BASE+len(code)] != code:
        raise ASMCodeError('Whole CODE differs from original; cannot credit only a slice')
    for start,end in ((BASE,BASE+len(code)),(BASE+offset,BASE+offset+size)):
        if any(p < end and p+2 > start for p in original_sites):
            raise ASMCodeError('Original MZ word exists/crosses BIOS allocation or unit')
    rawpath = Path(project)/RAW_EVIDENCE;raw = json.loads(rawpath.read_text());_subject(raw)
    r = raw['raw_result']
    if (raw.get('operation') != 'read_bytes' or raw.get('parameters') != {'address':'0x1ea32','length':83}
            or r.get('complete') is not True or r.get('returned_bytes') != 83
            or int(r['address'],0) != BASE+0x10000):
        raise ASMCodeError('Requires complete exact original raw83 context')
    observed = bytes.fromhex(r['bytes_hex'])
    if len(observed) != 83 or observed[:len(code)] != code:
        raise ASMCodeError('Complete independent CODE differs from raw primary')
    native_proofs = {}
    for symbol,path in UNITS.values():
        nativepath = Path(project)/path;native = json.loads(nativepath.read_text());_subject(native)
        at,n = public_extent(metadata,symbol)
        proc = native['normalized_result']['procedure'];body = proc['body'];address = BASE+at+0x10000
        if (native.get('operation') != 'analyze_function' or native.get('parameters') != {'procedure':hex(address)}
                or int(proc['address'],0) != address or proc['classification']['external']
                or proc['classification']['thunk'] or body.get('available') is not True
                or body.get('contains_entry') is not True or body.get('non_contiguous') is not False
                or body.get('total_bytes') != n or body.get('span_bytes') != n
                or body.get('ranges') != [{'start':hex(address),'end':hex(address+n-1)}]):
            raise ASMCodeError('Native primary does not prove both complete PUBLIC extents')
        native_proofs[path] = digest(nativepath.read_bytes())
    return code[offset:offset+size], {'whole_allocation_image_offset':BASE,
        'whole_allocation_size':len(code),'whole_allocation_sha256':digest(code),
        'whole_primary_path':RAW_EVIDENCE,'whole_primary_sha256':digest(rawpath.read_bytes()),
        'native_primaries_sha256':native_proofs,'public_offset':offset,
        'public_size':size,'whole_original_mz_sites':[],'unit_original_mz_sites':[],
        'emitted_mz_sites':[],'whole_bytes_equal':True,'matching_credit_added':0}
