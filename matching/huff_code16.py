"""Staged closed Huffman relocatable CODE backend; no additional match credit.

Generation uses only pinned authored assembly and NASM. Original bytes and
placements enter the separate full-allocation comparison, never generation.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,shutil,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
from link16 import link_function

class HuffCodeError(OMFError):pass

def require(condition,message):
    if not condition:raise HuffCodeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
SOURCE='asm/link/huffman_core_omf.asm'
SOURCE_SHA256='d15a2234c1413f7e5a8a02dc52693ffbb82b50d64484b2c5f1b324b7fda8b33a'
NASM_SHA256='57b8fc5957237b0d9b1ff48c8f5823780fb8ce968d9b8434850c06941ad5d5f5'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BASE=0xe03a
RAW_EVIDENCE='evidence/rea-huff-core-944-raw.json'
PUBLICS={'_prepare_asset_decode':0,'_huff_tree_build_recursive':61,'_huff_read_byte':110,'_huff_get_bit':124,'_huff_build_lookup':158,'_huff_frame_decode':349,'_huff_decode_stream':584,'_huff_window_save':858,'_huff_window_init':896}
UNITS={'huff_frame_decode_entry':('_prepare_asset_decode','evidence/rea_huff_frame.json'),'huff_tree_build_recursive':('_huff_tree_build_recursive','evidence/rea_huff_tree.json'),'huff_read_byte':('_huff_read_byte','evidence/rea_huff_byte.json'),'huff_get_bit':('_huff_get_bit','evidence/rea_bit.json'),'huff_build_lookup':('_huff_build_lookup','evidence/rea-huff-table_init.json'),'huff_decode_bytes':('_huff_frame_decode','evidence/rea-huff-stream-open.json'),'huff_decode_stream':('_huff_decode_stream','evidence/rea_remaining_decode_callee_e282.json'),'huff_window_save':('_huff_window_save','evidence/rea-huff-window_save.json'),'huff_window_init':('_huff_window_init','evidence/rea-huff-window-init.json')}
# FIXUP_PROFILE and RAW_CODE_SHA256 below are from the independently emitted
# complete source object, not target bytes or original placement arithmetic.
EXTERNALS={'_huff_refill_e3ea': 58346, '_huff_depth_trap_e410': 58384, '_huff_shift_word': 12482, '_huff_bits_left': 12484, '_huff_input_cursor': 12486, '_huff_remaining': 12488, '_huff_code_table': 12492, '_huff_fast_lookup': 13516, '_huff_long_records': 14540, '_huff_long_masks': 17612, '_huff_prefix_byte': 17621, '_huff_pending_count': 17622, '_huff_saved_extent': 17624, '_huff_checksum': 17631}
FIXUP_PROFILE=[{'offset': 4, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 8, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 12, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 22, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_code_table', 'displacement': None}, {'offset': 45, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 48, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 52, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_bits_left', 'displacement': None}, {'offset': 94, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_code_table', 'displacement': None}, {'offset': 107, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_depth_trap_e410', 'displacement': None}, {'offset': 135, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 148, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 159, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_code_table', 'displacement': None}, {'offset': 162, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_long_records', 'displacement': None}, {'offset': 197, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_fast_lookup', 'displacement': None}, {'offset': 262, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_prefix_byte', 'displacement': None}, {'offset': 273, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_fast_lookup', 'displacement': None}, {'offset': 301, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_prefix_byte', 'displacement': None}, {'offset': 321, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_long_masks', 'displacement': None}, {'offset': 365, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_depth_trap_e410', 'displacement': None}, {'offset': 369, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 375, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 380, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 384, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 388, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 392, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 395, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_saved_extent', 'displacement': None}, {'offset': 398, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_pending_count', 'displacement': None}, {'offset': 405, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 414, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 418, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 426, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_bits_left', 'displacement': None}, {'offset': 434, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_saved_extent', 'displacement': None}, {'offset': 439, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_pending_count', 'displacement': None}, {'offset': 453, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_fast_lookup', 'displacement': None}, {'offset': 464, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_checksum', 'displacement': None}, {'offset': 505, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 510, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 526, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 531, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 539, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_fast_lookup', 'displacement': None}, {'offset': 560, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_checksum', 'displacement': None}, {'offset': 600, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_depth_trap_e410', 'displacement': None}, {'offset': 604, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 610, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 615, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 619, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 623, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 627, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_remaining', 'displacement': None}, {'offset': 630, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_saved_extent', 'displacement': None}, {'offset': 633, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_pending_count', 'displacement': None}, {'offset': 640, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 647, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_saved_extent', 'displacement': None}, {'offset': 656, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 660, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 668, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_bits_left', 'displacement': None}, {'offset': 683, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_saved_extent', 'displacement': None}, {'offset': 713, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_pending_count', 'displacement': None}, {'offset': 727, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_fast_lookup', 'displacement': None}, {'offset': 738, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_checksum', 'displacement': None}, {'offset': 779, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 784, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 800, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 805, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 813, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_fast_lookup', 'displacement': None}, {'offset': 834, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_checksum', 'displacement': None}, {'offset': 862, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 875, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 879, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_bits_left', 'displacement': None}, {'offset': 883, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 887, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_checksum', 'displacement': None}, {'offset': 898, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 902, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_bits_left', 'displacement': None}, {'offset': 913, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_input_cursor', 'displacement': None}, {'offset': 917, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 922, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}, {'offset': 929, 'width': 2, 'location_type': 1, 'segment_relative': True, 'frame': [5, None], 'target_symbol': '_huff_shift_word', 'displacement': None}, {'offset': 934, 'width': 2, 'location_type': 1, 'segment_relative': False, 'frame': [5, None], 'target_symbol': '_huff_refill_e3ea', 'displacement': None}]
RAW_CODE_SHA256='10b77a9a2c050398aef8bcf1f5d632c59597d561fa85cfa8cd6525735f710512'

def validate_unit(unit):
    require((unit.get('language'),unit.get('backend'),unit.get('object_profile'),unit.get('source'))==('asm','nasm-code-omf','huffman_core',SOURCE),'Requires closed Huffman OMF profile/source')
    require(unit.get('source_sha256')==SOURCE_SHA256 and unit.get('assembler_sha256')==NASM_SHA256,'Requires Huffman source/tool pins')
    row=UNITS.get(unit.get('id'));require(row is not None,'Unknown Huffman unit')
    require((unit.get('symbol'),unit.get('rea_evidence'))==row,'Huffman public/native identity')
    offset=PUBLICS[row[0]];offsets=list(PUBLICS.values());size=(offsets+[944])[offsets.index(offset)+1]-offset
    require(type(unit.get('size'))is int and unit['size']==size and unit.get('image_offset')==hex(BASE+offset),'Cannot crop/resize Huffman PUBLIC extent')
    require(unit.get('reference_region','unchanged-prefix')=='unchanged-prefix' and unit.get('externals')==EXTERNALS,'Requires exact native binding context')
    require(not any(k in unit for k in ('flags','symbols','extended_extent','owned_const','owned_data','owned_bss','data_address','code_address','end_symbol')),'No slices/ownership/foreign CODE allocation')

def extract_code(obj):
    require(isinstance(obj,OMFObject)and set(obj.segments)=={1},'Requires exactly one strict CODE SEGDEF')
    seg=obj.segments[1]
    require((seg.name,seg.class_name,seg.attributes,seg.length,seg.unsupported_data)==('_TEXT','CODE',0x48,944,False),'Requires complete WORD PUBLIC USE16 CODE944')
    require(obj.externals==dict(enumerate(EXTERNALS,1)),'Missing/foreign external symbols')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and len(obj.publics)==9 and all((p.segment,p.group,p.type_index)==(1,0,0)for p in obj.publics.values()),'Missing/foreign/aliased PUBLIC')
    for kind,_,payload in obj.records:
        require(kind in(0x80,0x88,0x96,0x98,0x8c,0x90,0xa0,0x9c,0x8a),'Foreign allocation/COMM/LIDATA/group record')
        if kind==0x88:require(payload.startswith(b'\0\0')or payload==b'\x40\xa2\x01','Unreviewed linker directive')
        if kind==0x8a:require(payload==b'\0','No Huffman entry point')
    raw=bytearray()
    for at,data in sorted(seg.chunks):
        require(data and at==len(raw)and at+len(data)<=seg.length,'CODE hole/overlap/excess/empty LEDATA')
        raw.extend(data)
    require(len(raw)==seg.length,'Uninitialized/omitted CODE tail')
    fields=[];used=set()
    for f in sorted(obj.fixups,key=lambda f:f.offset):
        require(f.segment==1 and f.width==2 and f.location_type==1 and f.target[0]==2 and f.frame==(5,None),'Foreign fixup frame/type/target/segment')
        require(0<=f.offset<f.offset+2<=len(raw)and not used.intersection(range(f.offset,f.offset+2)),'Overlapping/crossing fixup')
        used.update(range(f.offset,f.offset+2))
        fields.append({'offset':f.offset,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'frame':list(f.frame),'target_symbol':obj.externals.get(f.target[1]),'displacement':f.displacement})
    require(fields==FIXUP_PROFILE,'Complete77-field profile differs')
    require(digest(raw)==RAW_CODE_SHA256,'Complete unlinked instruction/addend bytes changed')
    publics=sorted(obj.publics.values(),key=lambda p:p.offset);extents=[]
    for i,p in enumerate(publics):
        end=publics[i+1].offset if i+1<len(publics)else seg.length
        extents.append({'symbol':p.name,'offset':p.offset,'size':end-p.offset})
    return bytes(raw),{'boundary':'complete_asm_CODE_SEGDEF','segment':{'index':1,'name':seg.name,'class_name':seg.class_name,'attributes':seg.attributes,'length':seg.length},'publics':[asdict(p)for p in publics],'public_extents':extents,'raw_code_sha256':digest(raw),'fixups':fields,'emitted_mz_sites':[],'additional_matching_credit':0,'authored_c_credit':0}

def public_extent(metadata,symbol):
    require(metadata.get('boundary')=='complete_asm_CODE_SEGDEF'and metadata.get('segment',{}).get('length')==944,'Invalid complete PUBLIC metadata')
    expected=[];names=list(PUBLICS);offsets=list(PUBLICS.values())+[944]
    for i,n in enumerate(names):expected.append({'symbol':n,'offset':offsets[i],'size':offsets[i+1]-offsets[i]})
    require(metadata.get('public_extents')==expected,'Foreign/cropped complete PUBLIC metadata')
    require(symbol in PUBLICS,'Unknown PUBLIC')
    row=next(x for x in expected if x['symbol']==symbol);return row['offset'],row['size']

@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def assemble(source,unit,nasm='nasm'):
    validate_unit(unit);source_bytes=Path(source).read_bytes();require(digest(source_bytes)==SOURCE_SHA256,'Source pin mismatch')
    executable=shutil.which(nasm);require(executable is not None,'NASM unavailable');executable=Path(executable).resolve();require(digest(executable.read_bytes())==NASM_SHA256,'NASM pin mismatch')
    with tempfile.TemporaryDirectory(prefix='huff-omf-')as tmp:
        p=Path(tmp);(p/'UNIT.ASM').write_bytes(source_bytes);command=[str(executable),'-f','obj','-Ox','UNIT.ASM','-o','UNIT.OBJ'];r=subprocess.run(command,cwd=p,capture_output=True,text=True,timeout=30)
        require(r.returncode==0 and(p/'UNIT.OBJ').exists(),'NASM generation failed: '+r.stdout+r.stderr);data=(p/'UNIT.OBJ').read_bytes()
    require(digest(executable.read_bytes())==NASM_SHA256,'NASM changed during generation')
    raw,metadata=extract_code(read_omf(data));return Build(data,raw,metadata,{'source_sha256':digest(source_bytes),'assembler_sha256':NASM_SHA256,'assembler_path':str(executable),'build_command':command,'assembler_log':r.stdout+r.stderr,'object_sha256':digest(data),'object_format':'OMF16','fresh_directory':True})

def subject(e):
    subject=e.get('subject',{});profile=e.get('analysis_profile',{});provider=e.get('provider',{})
    require(subject.get('digest',{}).get('sha256')==ORIGINAL_SHA256 and
            subject.get('format')=='dos-mz'and subject.get('architecture')=='x86'and
            provider=={'id':'ghidra','name':'Ghidra','version':'12.1.4'}and
            profile.get('provider')==provider and
            e.get('operation')in('analyze_function','read_bytes')and
            profile.get('digest')=='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'and
            all(profile.get('parameters',{}).get(k)==v for k,v in{
                'target_format':'dos-mz','loader':'MzLoader','load_segment':'0x1000',
                'language_id':'x86:LE:16:Real Mode','address_coordinates':'linear-byte-offset'}.items()),
            'Wrong native subject/kind/provider/profile parameters')
    import re
    require(isinstance(e.get('evidence_id'),str)and re.fullmatch(r'ev_[0-9a-f]{64}',e['evidence_id']),
            'Native evidence ID missing/malformed')

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj);require(raw==built.code and metadata==built.metadata,'Build metadata/bytes differ from object')
    whole=bytearray();all_logs=[]
    for symbol,offset in PUBLICS.items():
        body,logs=link_function(obj,symbol,BASE+offset,EXTERNALS);whole.extend(body);all_logs.extend(logs)
    require(len(whole)==944 and len(all_logs)==77 and bytes(whole)==image[BASE:BASE+944],'Whole CODE944 does not match native; no partial credit')
    require(not any(p<BASE+944 and p+2>BASE for p in original_sites),'Original MZ word exists or crosses CODE')
    project=Path(project);rawpath=project/RAW_EVIDENCE;e=json.loads(rawpath.read_text());subject(e);r=e['normalized_result']
    require(e['operation']=='read_bytes'and e['parameters']=={'address':'0x1e03a','length':944}and r['complete']and r['requested_bytes']==r['returned_bytes']==944 and int(r['address'],0)==BASE+0x10000 and bytes.fromhex(r['bytes_hex'])==whole,'Full original944 primary mismatch')
    native={};seen_ids={e['evidence_id']};evidence_ids={RAW_EVIDENCE:e['evidence_id']}
    for symbol,path in UNITS.values():
        e=json.loads((project/path).read_text());subject(e);require(e['evidence_id']not in seen_ids,'Duplicate native/raw evidence ID');seen_ids.add(e['evidence_id']);evidence_ids[path]=e['evidence_id'];at,size=public_extent(metadata,symbol);p=e['normalized_result']['procedure'];b=p['body'];address=BASE+at+0x10000
        require(e['operation']=='analyze_function'and e['parameters']=={'procedure':hex(address)}and int(p['address'],0)==address and not p['classification']['external']and not p['classification']['thunk']and b['available']and b['contains_entry']and not b['non_contiguous']and b['total_bytes']==b['span_bytes']==size and b['ranges']==[{'start':hex(address),'end':hex(address+size-1)}],'Native complete9-PUBLIC boundary mismatch')
        native[path]=digest((project/path).read_bytes())
    offset,size=public_extent(metadata,unit['symbol']);unit_logs=[x for x in all_logs if BASE+offset<=x['image_offset']<BASE+offset+size]
    require(not any('mz_segment_relocation_image_offset'in x for x in all_logs),'Unexpected emitted MZ')
    loads=[{'load_paragraph':base,'all944bytes_exact':True,'sha256':digest(whole),'original_mz':[],'emitted_mz':[]}for base in[0,1,0x1234,0xee10]]
    return bytes(whole[offset:offset+size]),{'whole_allocation_image_offset':BASE,'whole_allocation_size':944,'whole_allocation_sha256':digest(whole),'whole_linked_code_hex':whole.hex(),'whole_primary_path':RAW_EVIDENCE,'whole_primary_sha256':digest(rawpath.read_bytes()),'native_primaries_sha256':native,'native_evidence_ids':evidence_ids,'public_offset':offset,'public_size':size,'whole_original_mz_sites':[],'unit_original_mz_sites':[],'emitted_mz_sites':[],'whole_bytes_equal':True,'four_load_bases':loads,'relocations':unit_logs,'complete77_relocations':all_logs,'matching_credit_added':0,'actual_missing_storage_definitions_supplied':False}
