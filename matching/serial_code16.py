"""Closed MASM5.10 serial182 contribution; target-free generation, separate comparison.

Two far PUBLICs are actual C-link definitions. The internal IRQ71 and savedDS
word2 remain part of one complete CODE allocation, never invented functions.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
from library16 import link_segment

class SerialCodeError(OMFError): pass
def require(condition,message):
    if not condition: raise SerialCodeError(message)
def digest(data): return hashlib.sha256(data).hexdigest()
BACKEND='masm510-code-contribution-omf'
SOURCE='asm/link/serial_irq_omf.asm'
SOURCE_SHA256='e3571172ef936c9adc81e8cb347ed84e0e656695bcbb5d21155d55adc61bbdb2'
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BASE=0x10d30
PUBLICS={'_enable_serial_irq_10d3_0023':35,'_set_serial_format_10d3_0000':0}
BINDINGS={'_serial_irq':{'segment':0x5cc2,'offset':0x2ebc},'_serial_base':{'segment':0x5cc2,'offset':0x2ebe},'_byte_write_cursor':{'segment':0x5cc2,'offset':0x9342},'_byte_read_cursor':{'segment':0x5cc2,'offset':0x8ae6},'_byte_ring_buffer':{'segment':0x5cc2,'offset':0x8b2e},'_serial_ring_end_2eba':{'segment':0x5cc2,'offset':0x2eba},'_serial_irq_flags_b0d4':{'segment':0x5cc2,'offset':0xb0d4}}
EXTERNALS={1:'_byte_read_cursor',2:'_serial_base',3:'_byte_write_cursor',4:'_serial_ring_end_2eba',5:'_serial_irq_flags_b0d4',6:'_serial_irq',7:'_byte_ring_buffer'}
RAW_SHA256='700087a7b62158238ce174186b1da2eae54bd82a8fbc874ce3af133a24210152'
RAW_EVIDENCE='build/serial-enclosing-context/rea-original184.json'
# Filled below with reviewed independent object/evidence identities, not target generator input.
EVIDENCE_PINS={'build/serial-enclosing-context/rea-original184.json': '4d9800f682469cc5fbe4cd772e7be733654478877a382bdd41f82fc0548dc930', 'build/serial-enclosing-context/rea-carrier184.json': '9ff761c5a758cb379f2a29845fb18f3e203f8cdf26f8dd8497c19b9b800b14ff', 'evidence/rea_byte_setup_actual_0d30.json': 'cdde425d37611c588b9206c75998f423248c126b11d3491a3231a8a4ebf7c9c5', 'build/enable-serial-irq-10d53/rea-carrier-native.json': '1d4e1b074d07f5a78014f9ff08cc74f7da0c774433d915cb4f88b20e97177445', 'build/serial-enclosing-context/proof.json': '931961ea8f6c3be0504653bc70b459f845acebe4e951d9cf741714a289b30827'}
FIXUPS=[(9, 2, 1, True, (1, 1), (2, 2), None), (26, 2, 1, True, (1, 1), (2, 2), None), (41, 2, 1, True, (0, 2), (0, 2), 180), (45, 2, 1, True, (1, 1), (2, 6), None), (56, 2, 1, True, (1, 1), (2, 2), None), (64, 2, 1, True, (0, 2), (0, 2), 109), (90, 2, 1, True, (1, 1), (2, 6), None), (116, 2, 1, True, (0, 2), (0, 2), 180), (122, 2, 1, True, (1, 1), (2, 3), None), (126, 2, 1, True, (1, 1), (2, 2), None), (135, 2, 1, True, (1, 1), (2, 5), None), (145, 2, 1, True, (1, 1), (2, 4), None), (150, 2, 1, True, (0, 1), (2, 7), None), (154, 2, 1, True, (1, 1), (2, 1), None), (160, 2, 1, True, (1, 1), (2, 5), None), (165, 2, 1, True, (1, 1), (2, 3), None), (169, 2, 1, True, (1, 1), (2, 3), None)]

def validate_unit(unit):
    if unit.get('object_profile') == 'serial_irq248_dgroup_v1':
        from serial248_dgroup_code16 import validate_unit as successor
        return successor(unit)

    if unit.get('object_profile') == 'serial_irq248':
        from serial248_code16 import validate_unit as successor
        return successor(unit)

    require((unit.get('id'),unit.get('language'),unit.get('backend'),unit.get('object_profile'),unit.get('source'))==('serial_irq_code182','asm-code',BACKEND,'serial_irq182',SOURCE),'Closed serial182 profile/source required')
    require(unit.get('source_sha256')==SOURCE_SHA256 and unit.get('assembler_sha256')==MASM_SHA256,'Pinned serial source/MASM required')
    require(unit.get('public_symbols')==list(PUBLICS) and unit.get('image_offset')==hex(BASE) and type(unit.get('size'))is int and unit['size']==182,'Complete182/twoPUBLICs required; no slices')
    require(unit.get('externals')==BINDINGS and unit.get('rea_evidence')==RAW_EVIDENCE and unit.get('reference_region','unchanged-prefix')=='unchanged-prefix','Closed native comparison bindings/evidence required')
    require(not any(k in unit for k in ('symbol','flags','end_symbol','extended_extent','owned_const','owned_const_profile','owned_data','owned_bss','data_address','code_address','runtime_kind','compiler_source_name')),'No function/ownership/foreign frame metadata')

def extract_code(obj):
    if isinstance(obj, OMFObject) and 2 in obj.segments and obj.segments[2].length == 248 and any(f.offset == 150 and f.frame == (1, 1) and f.target == (2, 7) for f in obj.fixups):
        from serial248_dgroup_code16 import extract_code as successor
        return successor(obj)

    if isinstance(obj, OMFObject) and 2 in obj.segments and obj.segments[2].length == 248:
        from serial248_code16 import extract_code as successor
        return successor(obj)

    require(isinstance(obj,OMFObject) and set(obj.segments)=={1,2},'Exactly emptyDATA and wholeCODE required')
    data,seg=obj.segments[1],obj.segments[2]
    require((data.name,data.class_name,data.length,data.attributes,data.unsupported_data,data.chunks)==('_DATA','DATA',0,72,False,[]),'Empty DATA0 only; no initialized DATA or BSS')
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.unsupported_data)==('SERIAL_TEXT','CODE',182,72,False),'Whole WORD CODE182 required')
    require(obj.names==['','','DGROUP','DATA','CODE','_DATA','SERIAL_TEXT'],'Closed segment/group names required')
    require((data.index,data.name_index,data.class_index,data.overlay_index)==(1,5,3,1) and (seg.index,seg.name_index,seg.class_index,seg.overlay_index)==(2,6,4,1),'Closed SEGDEF indices/overlay required')
    require(obj.externals==EXTERNALS,'Exact seven external names/indices required')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and len(obj.publics)==2 and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'Two genuine PUBLIC entries only, no aliases')
    require(not obj.procedures,'No fabricated C procedure metadata')
    kinds=[k for k,_,_ in obj.records]
    require(kinds==[0x80,0x96,0x98,0x98,0x9a,0x8c,0x90,0x88,0xa0,0x9c,0x8a],'Closed record sequence; no COMMON/LIDATA/debug/extraallocation')
    require([p for k,_,p in obj.records if k==0x80]==[b'\x08UNIT.ASM'],'Deterministic UNIT.ASM THEADR required')
    require([p for k,_,p in obj.records if k==0x9a]==[b'\x02\xff\x01'],'Exact DGROUP containing emptyDATA required')
    require([p for k,_,p in obj.records if k==0x88]==[b'\x00\xa2\x01'],'Unreviewed MASM linker directive')
    require([p for k,_,p in obj.records if k==0x8a]==[b'\x00'],'No executable entry metadata')
    raw=bytearray()
    for at,content in sorted(seg.chunks):
        require(content and at==len(raw) and at+len(content)<=seg.length,'CODE hole/overlap/excess')
        raw.extend(content)
    require(len(raw)==seg.length,'Omitted CODE tail')
    fields=[(f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in obj.fixups]
    require(all(f.segment==2 for f in obj.fixups) and fields==FIXUPS,'Exact17 fields/frames/targets/displacements required')
    require(digest(raw)==RAW_SHA256,'Unlinked instructions/addends changed')
    require(raw[180:182]==b'\0\0','Actual savedDS scalar only')
    return bytes(raw),{'boundary':'complete_multi_entry_CODE_SEGDEF','segment':{'index':2,'name':seg.name,'class_name':seg.class_name,'attributes':72,'length':seg.length},'empty_data_segment':{'index':1,'name':'_DATA','length':0},'group':{'index':1,'name':'DGROUP','segments':[1]},'publics':[asdict(p)for p in obj.publics.values()],'internal_components':[{'kind':'raw_CFG_interrupt_body','offset':109,'size':71,'ordinary_REA_function_claim':False},{'kind':'saved_DS_word','offset':180,'size':2,'DATA_credit':0}],'actual_fixup_count':17,'raw_sha256':digest(raw),'authored_c_function_credit':0,'authored_asm_function_credit':0,'CODE_contributions':1}

@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def assemble(source,project):
    """Accept source+tool identity only; no comparison bytes, size or placements."""
    candidate,root=Path(source).resolve(),Path(project).resolve()
    if candidate==(root/'asm/link/serial_context248_dgroup.asm').resolve() and candidate.is_relative_to(root):
        from serial248_dgroup_code16 import assemble as successor
        return successor(source,project)
    if candidate==(root/'asm/link/serial_context248_omf.asm').resolve() and candidate.is_relative_to(root):
        from serial248_code16 import assemble as successor
        return successor(source,project)
    source,project=Path(source).resolve(),Path(project).resolve()
    require(source==(project/SOURCE).resolve() and source.is_relative_to(project),'Canonical source path required')
    content=source.read_bytes();require(digest(content)==SOURCE_SHA256,'Source pin mismatch')
    tools=project/'toolchains/msc510';paths={'assembler':tools/'MASM.EXE','manifest':tools/'manifest.json','license':tools/'LICENSE','config':project/'config/msc510.json'}
    expected={'assembler':MASM_SHA256,'manifest':MANIFEST_SHA256,'license':LICENSE_SHA256,'config':CONFIG_SHA256}
    for key,p in paths.items():require(digest(p.read_bytes())==expected[key],'MASM '+key+' pin mismatch')
    for key in ['manifest','config']:
        record=next((r for r in json.loads(paths[key].read_text())['files']if r['name']=='MASM.EXE'),None)
        require(record=={'name':'MASM.EXE','sha256':MASM_SHA256,'size':110703},'MASM manifest record mismatch')
    command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
    with tempfile.TemporaryDirectory(prefix='serial-masm-')as tmp:
        p=Path(tmp);(p/'UNIT.ASM').write_bytes(content)
        batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n'
        (p/'RUN.BAT').write_bytes(batch.encode('ascii'))
        conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(tools)+'" -ro\nc:\nRUN.BAT\n'
        (p/'dosbox.conf').write_text(conf)
        r=subprocess.run(['dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=45)
        require(r.returncode==0 and (p/'RESULT.TXT').is_file() and (p/'RESULT.TXT').read_text().strip()=='assembled' and (p/'UNIT.OBJ').is_file(),'MASM generation failed')
        log=(p/'MASM.LOG').read_text(encoding='cp437');require('Macro Assembler Version 5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'MASM warnings/errors/version')
        data=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_text(encoding='cp437')
    for key,p in paths.items():require(digest(p.read_bytes())==expected[key],'MASM '+key+' changed during generation')
    raw,metadata=extract_code(read_omf(data))
    return Build(data,raw,metadata,{'source_sha256':digest(content),'assembler_sha256':MASM_SHA256,'assembler_manifest_sha256':MANIFEST_SHA256,'assembler_license_sha256':LICENSE_SHA256,'assembler_configuration_sha256':CONFIG_SHA256,'compiler':'Microsoft Macro Assembler5.10','build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':digest(data),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','dosbox_configuration':conf,'batch_source':batch,'dosbox_stdout':r.stdout.decode('utf-8','replace'),'dosbox_stderr':r.stderr.decode('utf-8','replace'),'generation_target_input':False,'generation_original_placement_input':False})

def _subject(e,sha,operation):
    p=e.get('analysis_profile',{});provider={'id':'ghidra','name':'Ghidra','version':'12.1.4'}
    require(e.get('subject',{}).get('digest',{}).get('sha256')==sha and e['subject'].get('format')=='dos-mz' and e['subject'].get('architecture')=='x86' and e.get('operation')==operation and e.get('provider')==provider and p.get('provider')==provider and p.get('digest')==PROFILE,'Native subject/provider/profile mismatch')
    require(all(p.get('parameters',{}).get(k)==v for k,v in {'target_format':'dos-mz','loader':'MzLoader','load_segment':'0x1000','language_id':'x86:LE:16:Real Mode','address_coordinates':'linear-byte-offset'}.items()),'Native loader parameters mismatch')
    require(re.fullmatch(r'ev_[0-9a-f]{64}',e.get('evidence_id',''))is not None,'Missing evidence identity')

def _evidence(project):
    records={}
    for rel,pin in EVIDENCE_PINS.items():
        p=Path(project)/rel;content=p.read_bytes();require(digest(content)==pin,'Primary/CFG evidence pin mismatch: '+rel);records[rel]=json.loads(content)
    raw=[]
    for rel,sha in [(RAW_EVIDENCE,ORIGINAL_SHA256),('build/serial-enclosing-context/rea-carrier184.json',CARRIER_SHA256)]:
        e=records[rel];_subject(e,sha,'read_bytes');r=e['normalized_result']
        require(e['parameters']=={'address':'0x20d30','length':184} and r.get('address')=='0x20d30' and r.get('complete')is True and r['requested_bytes']==r['returned_bytes']==184,'Complete184 primary read required')
        b=bytes.fromhex(r['bytes_hex']);require(len(b)==184,'Primary byte length');raw.append(b)
    require(raw[0]==raw[1],'Original/carrier raw mismatch')
    for rel,sha,start,size in [('evidence/rea_byte_setup_actual_0d30.json',ORIGINAL_SHA256,0x20d30,35),('build/enable-serial-irq-10d53/rea-carrier-native.json',CARRIER_SHA256,0x20d53,74)]:
        e=records[rel];_subject(e,sha,'analyze_function');p=e['normalized_result']['procedure'];b=p['body']
        require(e['parameters']=={'procedure':hex(start)} and int(p['address'],0)==start and not p['classification']['external'] and not p['classification']['thunk'] and b['available']and b['contains_entry']and not b['non_contiguous']and b['total_bytes']==b['span_bytes']==size and b['ranges']==[{'start':hex(start),'end':hex(start+size-1)}],'Two exact ordinary native entries required')
    proof=records['build/serial-enclosing-context/proof.json'];instructions=proof['handler_instructions'];end=109
    for ins in instructions:
        content=bytes.fromhex(ins['bytes']);require(ins['offset']==end and content and raw[0][end:end+len(content)]==content,'Complete raw IRQ instruction partition mismatch');end+=len(content)
    require(end==180 and instructions[0]['text']=='sti' and instructions[-1]['text']=='iret' and proof['ordinary_REA_handler_extent_claim']is False,'IRQ extent must remain rawCFG-only')
    require(proof['handler_CFG']=={'entry':109,'conditional_edges':[[147,152],[156,167]],'both_fallthrough_edges':True,'sole_exit':'IRET at179','all71_instruction_bytes_consumed':True},'Closed IRQ CFG mismatch')
    require(raw[0][180:182]==b'\0\0' and raw[0][41:43]==b'\xb4\0' and raw[0][116:118]==b'\xb4\0' and raw[0][64:66]==b'\x6d\0','SavedDS word/install/read semantics mismatch')
    return raw[0],records[RAW_EVIDENCE]['evidence_id']

def validate_evidence(unit,project,target_sha256,reference=None):
    if unit.get('object_profile') == 'serial_irq248_dgroup_v1':
        from serial248_dgroup_code16 import validate_evidence as successor
        return successor(unit,project,target_sha256,reference)

    if unit.get('object_profile') == 'serial_irq248':
        from serial248_code16 import validate_evidence as successor
        return successor(unit,project,target_sha256,reference)

    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    raw,evidence_id=_evidence(project)
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Pinned expanded context required')
    require(reference['image'][BASE:BASE+184]==raw,'Primary/reference whole context mismatch')
    require(not any(s<BASE+182 and s+2>BASE for s in reference['relocations']),'Serial context MZ/crossing word forbidden')
    return evidence_id

def validate_comparison(unit,built,image,project,original_sites):
    if unit.get('object_profile') == 'serial_irq248_dgroup_v1':
        from serial248_dgroup_code16 import validate_comparison as successor
        return successor(unit,built,image,project,original_sites)

    if unit.get('object_profile') == 'serial_irq248':
        from serial248_code16 import validate_comparison as successor
        return successor(unit,built,image,project,original_sites)

    validate_unit(unit);obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj)
    require(raw==built.code and metadata==built.metadata,'Build differs from complete object')
    externs={k:(v['segment'],v['offset'])for k,v in BINDINGS.items()}
    linked,logs=link_segment(obj,2,{1:(0x5cc2,0),2:(0x10d3,0)},{1:0x5cc2},externs)
    primary,evidence_id=_evidence(project)
    require(len(linked)==182 and linked==primary[:182]==image[BASE:BASE+182],'Complete182 native/source bytes differ; no partial credit')
    require(not any(s<BASE+182 and s+2>BASE for s in original_sites),'Serial MZ set must be empty, no crossing words')
    loads=[]
    for base in [0,1,0x1000,0xffff]:
        ex={k:((v[0]+base)&65535,v[1])for k,v in externs.items()}
        b,l=link_segment(obj,2,{1:((0x5cc2+base)&65535,0),2:((0x10d3+base)&65535,0)},{1:(0x5cc2+base)&65535},ex)
        require(b==primary[:182] and all(f['mz_relocation_image_offset']is None for f in l),'Forward loader arithmetic mismatch')
        loads.append({'load_paragraph':base,'all182bytes_exact':True,'original_mz':[],'emitted_mz':[]})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':182,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':logs,'four_load_bases':loads,'native_evidence_id':evidence_id,'evidence_sha256':EVIDENCE_PINS,'function_partition_claim':False,'DATA_byte_credit':0,'authored_c_function_credit':0,'authored_asm_function_credit':0,'historical_module_or_MAP_claim':False,'missing_source_storage':['near_pointer_word_DS2EBA','byte_flags_DSB0D4']}
