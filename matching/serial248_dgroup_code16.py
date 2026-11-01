"""Closed MASM5.10 serial248 contribution; target-free generation, separate comparison.

Four far PUBLICs are actual C-link definitions. The internal IRQ71 and savedDS
word2 remain part of one complete CODE allocation, never invented functions.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
from library16 import link_segment
import serial_code16 as old182
_subject=old182._subject

class SerialCodeError(OMFError): pass
def require(condition,message):
    if not condition: raise SerialCodeError(message)
def digest(data): return hashlib.sha256(data).hexdigest()
BACKEND='masm510-code-contribution-omf'
SOURCE='asm/link/serial_context248_dgroup.asm'
SOURCE_SHA256='7e14ccb1bc4efe3a6fa26c61bb35a6d9d6602b1e412bdbc607dcd9c3de9a4836'
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BASE=0x10d30
PUBLICS={'_enable_serial_irq_10d3_0023': 35, '_set_serial_format_10d3_0000': 0, '_write_byte_far': 182, '_restore_mode_10e0d': 221}
BINDINGS={'_serial_irq':{'segment':0x5cc2,'offset':0x2ebc},'_serial_base':{'segment':0x5cc2,'offset':0x2ebe},'_byte_write_cursor':{'segment':0x5cc2,'offset':0x9342},'_byte_read_cursor':{'segment':0x5cc2,'offset':0x8ae6},'_byte_ring_buffer':{'segment':0x5cc2,'offset':0x8b2e},'_serial_ring_end_2eba':{'segment':0x5cc2,'offset':0x2eba},'_serial_irq_flags_b0d4':{'segment':0x5cc2,'offset':0xb0d4}}
EXTERNALS={1:'_byte_read_cursor',2:'_serial_base',3:'_byte_write_cursor',4:'_serial_ring_end_2eba',5:'_serial_irq_flags_b0d4',6:'_serial_irq',7:'_byte_ring_buffer'}
RAW_SHA256='bdf15445ea3573a9e6d1561dff1b8d5a75e4b2016bcd6965b88bc115b568654e'
RAW_EVIDENCE='build/serial-enclosing-context/rea-original184.json'
# Filled below with reviewed independent object/evidence identities, not target generator input.
EVIDENCE_PINS={'build/serial-enclosing-context/rea-original184.json': '4d9800f682469cc5fbe4cd772e7be733654478877a382bdd41f82fc0548dc930', 'build/serial-enclosing-context/rea-carrier184.json': '9ff761c5a758cb379f2a29845fb18f3e203f8cdf26f8dd8497c19b9b800b14ff', 'evidence/rea_byte_setup_actual_0d30.json': 'cdde425d37611c588b9206c75998f423248c126b11d3491a3231a8a4ebf7c9c5', 'build/enable-serial-irq-10d53/rea-carrier-native.json': '1d4e1b074d07f5a78014f9ff08cc74f7da0c774433d915cb4f88b20e97177445', 'build/serial-enclosing-context/proof.json': '931961ea8f6c3be0504653bc70b459f845acebe4e951d9cf741714a289b30827'}
FIXUPS=[(9, 2, 1, True, (1, 1), (2, 2), None), (26, 2, 1, True, (1, 1), (2, 2), None), (41, 2, 1, True, (0, 2), (0, 2), 180), (45, 2, 1, True, (1, 1), (2, 6), None), (56, 2, 1, True, (1, 1), (2, 2), None), (64, 2, 1, True, (0, 2), (0, 2), 109), (90, 2, 1, True, (1, 1), (2, 6), None), (116, 2, 1, True, (0, 2), (0, 2), 180), (122, 2, 1, True, (1, 1), (2, 3), None), (126, 2, 1, True, (1, 1), (2, 2), None), (135, 2, 1, True, (1, 1), (2, 5), None), (145, 2, 1, True, (1, 1), (2, 4), None), (150, 2, 1, True, (1, 1), (2, 7), None), (154, 2, 1, True, (1, 1), (2, 1), None), (160, 2, 1, True, (1, 1), (2, 5), None), (165, 2, 1, True, (1, 1), (2, 3), None), (169, 2, 1, True, (1, 1), (2, 3), None), (187, 2, 1, True, (1, 1), (2, 2), None), (207, 2, 1, True, (1, 1), (2, 5), None), (225, 2, 1, True, (1, 1), (2, 6), None), (237, 2, 1, True, (1, 1), (2, 2), None)]

def validate_unit(unit):
    required={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','boundary_evidence'}
    require(type(unit)is dict and required<=set(unit)<=required|{'reference_region'},'Closed serial248 unit metadata keys required; no function/ownership metadata')
    require(type(unit['boundary_evidence'])is str and bool(unit['boundary_evidence'].strip()),'Boundary evidence description required')
    require((unit.get('id'),unit.get('language'),unit.get('backend'),unit.get('object_profile'),unit.get('source'))==('serial_irq_code248','asm-code',BACKEND,'serial_irq248_dgroup_v1',SOURCE),'Closed serial248 profile/source required')
    require(unit.get('source_sha256')==SOURCE_SHA256 and unit.get('assembler_sha256')==MASM_SHA256,'Pinned serial source/MASM required')
    require(unit.get('public_symbols')==list(PUBLICS) and unit.get('image_offset')==hex(BASE) and type(unit.get('size'))is int and unit['size']==248,'Complete248/fourPUBLICs required; no slices')
    require(unit.get('externals')==BINDINGS and unit.get('rea_evidence')==RAW_EVIDENCE and unit.get('reference_region','unchanged-prefix')=='unchanged-prefix','Closed native comparison bindings/evidence required')
    require(not any(k in unit for k in ('symbol','flags','end_symbol','extended_extent','owned_const','owned_const_profile','owned_data','owned_bss','data_address','code_address','runtime_kind','compiler_source_name')),'No function/ownership/foreign frame metadata')

def extract_code(obj):
    require(isinstance(obj,OMFObject) and set(obj.segments)=={1,2},'Exactly emptyDATA and wholeCODE required')
    data,seg=obj.segments[1],obj.segments[2]
    require((data.name,data.class_name,data.length,data.attributes,data.unsupported_data,data.chunks)==('_DATA','DATA',0,72,False,[]),'Empty DATA0 only; no initialized DATA or BSS')
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.unsupported_data)==('SERIAL_TEXT','CODE',248,72,False),'Whole WORD CODE248 required')
    require(obj.names==['','','DGROUP','DATA','CODE','_DATA','SERIAL_TEXT'],'Closed segment/group names required')
    require((data.index,data.name_index,data.class_index,data.overlay_index)==(1,5,3,1) and (seg.index,seg.name_index,seg.class_index,seg.overlay_index)==(2,6,4,1),'Closed SEGDEF indices/overlay required')
    require(obj.externals==EXTERNALS,'Exact seven external names/indices required')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and len(obj.publics)==4 and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'Four genuine PUBLIC entries only, no aliases')
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
    require(all(f.segment==2 for f in obj.fixups) and fields==FIXUPS,'Exact21 fields/frames/targets/displacements required')
    require(digest(raw)==RAW_SHA256,'Unlinked instructions/addends changed')
    require(raw[180:182]==b'\0\0' and digest(raw[:182])==old182.RAW_SHA256,'Actual savedDS scalar/unchanged182 required')
    return bytes(raw),{'boundary':'complete_multi_entry_CODE_SEGDEF','segment':{'index':2,'name':seg.name,'class_name':seg.class_name,'attributes':72,'length':seg.length},'empty_data_segment':{'index':1,'name':'_DATA','length':0},'group':{'index':1,'name':'DGROUP','segments':[1]},'publics':[asdict(p)for p in obj.publics.values()],'internal_components':[{'kind':'raw_CFG_interrupt_body','offset':109,'size':71,'ordinary_REA_function_claim':False},{'kind':'saved_DS_word','offset':180,'size':2,'DATA_credit':0}],'actual_fixup_count':21,'raw_sha256':digest(raw),'authored_c_function_credit':0,'authored_asm_function_credit':0,'CODE_contributions':1}

@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def _assemble(source,project):
    """Accept source+tool identity only; no comparison bytes, size or placements."""
    require(not Path(source).is_symlink(),'Source symlink forbidden')
    source,project=Path(source).resolve(),Path(project).resolve()
    require(not any(c in str(project) for c in (chr(13),chr(10),chr(34))),'Unsafe assembler project path')
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
        p=Path(tmp);require(not any(c in str(p) for c in (chr(13),chr(10),chr(34))),'Unsafe assembler scratch path');(p/'UNIT.ASM').write_bytes(content)
        batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n'
        (p/'RUN.BAT').write_bytes(batch.encode('ascii'))
        conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(tools)+'" -ro\nc:\nRUN.BAT\n'
        (p/'dosbox.conf').write_text(conf)
        r=subprocess.run(['dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=45)
        require(r.returncode==0 and (p/'RESULT.TXT').is_file() and (p/'RESULT.TXT').read_text().strip()=='assembled' and (p/'UNIT.OBJ').is_file(),'MASM generation failed')
        log=(p/'MASM.LOG').read_text(encoding='cp437');require('Macro Assembler Version 5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'MASM warnings/errors/version')
        data=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_text(encoding='cp437')
    for key,p in paths.items():require(digest(p.read_bytes())==expected[key],'MASM '+key+' changed during generation')
    require(digest(data)=='5988f0f3344eadda3961609db62be85d4ab0ade0301335f248bf4de5a2e87726','Complete deterministic serial248 OMF changed')
    raw,metadata=extract_code(read_omf(data))
    return Build(data,raw,metadata,{'source_sha256':digest(content),'assembler_sha256':MASM_SHA256,'assembler_manifest_sha256':MANIFEST_SHA256,'assembler_license_sha256':LICENSE_SHA256,'assembler_configuration_sha256':CONFIG_SHA256,'compiler':'Microsoft Macro Assembler5.10','build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':digest(data),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','dosbox_configuration':conf,'batch_source':batch,'dosbox_stdout':r.stdout.decode('utf-8','replace'),'dosbox_stderr':r.stderr.decode('utf-8','replace'),'generation_target_input':False,'generation_original_placement_input':False})


TAIL_EVIDENCE_PINS={'build/serial-tail-native-followup/freeze-manifest.json': '27f96173053afa2f13c3f566e0320203181dd5ff9d4317cc3697c5f382c8d0ea', 'build/serial-tail-native-followup/rea-raw.json': 'bdc729ea3e8dda47638e0d2fbeba9092fe6bc094853836fb7728fe48b475be72', 'build/serial-tail-native-followup/rea-carrier-raw.json': '9d05ed5f8aca9e07f1ac00293ccec3e9c1429c8adfa4a351eca957a544e7be21', 'build/serial-tail-native-followup/rea-carrier-write.json': '5e7200166f1659ec7bea025f9fa4e056a608a0d658a54695e1c4af247650dcd0', 'build/serial-tail-native-followup/rea-carrier-restore.json': 'cfae402d79e04d5f70cfd593bd49559991859eebb2dc68834a21b558d30ad0a8', 'build/serial-tail-native-followup/rea-carrier-next.json': 'f5c3c1c9a76d3770329139010f1dbfcfdd49e22c71052dc276dd0eb8d8cc7dcf', 'build/serial-tail-native-followup/native-review.json': '454481f5a9f951c3b66c8e7155e2772f5a9a88d68eec284638e873b24a88cb94', 'build/serial-tail-native-followup/caller-report-snapshot.json': '80dc43204cea73f32421dc805329664d68286702b20829f6a44f007fdaaea157'}

def _evidence(project):
    # Existing182 native/handler/state admission remains exactly unchanged.
    prefix,first_id=old182._evidence(project)
    rows={}
    for rel,pin in TAIL_EVIDENCE_PINS.items():
        content=(Path(project)/rel).read_bytes();require(digest(content)==pin,'Serial tail evidence pin mismatch: '+rel);rows[rel]=json.loads(content)
    base='build/serial-tail-native-followup/'
    tails=[];ids=[first_id]
    for name,sha in [('rea-raw.json',ORIGINAL_SHA256),('rea-carrier-raw.json',CARRIER_SHA256)]:
        e=rows[base+name];old182._subject(e,sha,'read_bytes');r=e['normalized_result']
        require(e['parameters']=={'address':'0x20de6','length':82}and r['address']=='0x20de6'and r['complete']is True and r['requested_bytes']==r['returned_bytes']==82,'Complete tail82 primary required')
        b=bytes.fromhex(r['bytes_hex']);require(len(b)==82,'Tail primary length');tails.append(b);ids.append(e['evidence_id'])
    require(tails[0]==tails[1]and prefix[182:184]==tails[0][:2],'Original/carrier tail or old182 overlap mismatch')
    raw=prefix[:182]+tails[0][:66];require(len(raw)==248,'Complete native248 union required')
    e=rows[base+'rea-carrier-write.json'];old182._subject(e,CARRIER_SHA256,'analyze_function');p=e['normalized_result']['procedure'];b=p['body']
    require(e['parameters']=={'procedure':'0x20de6'}and p['address']=='0x20de6'and not p['classification']['external']and not p['classification']['thunk'],'Write-byte native entry required')
    require(b=={'available':True,'provenance':'ghidra-function-body-address-set','ranges':[{'start':'0x20de6','end':'0x20e03'},{'start':'0x20e05','end':'0x20e0c'}],'total_bytes':38,'span_bytes':39,'non_contiguous':True,'contains_entry':True},'Write-byte must remain reachable38/span39 with native gap')
    require(raw[201:207]==bytes.fromhex('750ae2f9800e')and raw[210:213]==bytes.fromhex('eb0790')and raw[213:221]==bytes.fromhex('8a4606b2f8ee5dcb'),'Write nativeCFG/low-byte fararg/real90 mismatch')
    e=rows[base+'rea-carrier-restore.json'];old182._subject(e,CARRIER_SHA256,'analyze_function');p=e['normalized_result']['procedure'];b=p['body']
    require(e['parameters']=={'procedure':'0x20e0d'}and p['address']=='0x20e0d'and not p['classification']['external']and not p['classification']['thunk']and b['available']and b['contains_entry']and not b['non_contiguous']and b['total_bytes']==b['span_bytes']==27 and b['ranges']==[{'start':'0x20e0d','end':'0x20e27'}],'Cleanup must be exact27 contiguous far entry')
    require(raw[221:]==bytes.fromhex('e4218b0ebc2eb401d2e40ac4e6218b16be2eb2f8ecb2f92ac0eecb'),'Cleanup PIC/UART/raw27 mismatch')
    e=rows[base+'rea-carrier-next.json'];old182._subject(e,CARRIER_SHA256,'analyze_function');p=e['normalized_result']['procedure']
    require(e['parameters']=={'procedure':'0x20e30'}and p['address']=='0x20e30'and p['body']['ranges']==[{'start':'0x20e30','end':'0x20eb1'}]and p['body']['total_bytes']==130,'Following audio boundary required')
    require(tails[0][66:74]==bytes(8)and tails[0][74:]==bytes.fromhex('558bec56578b4606'),'Unowned8bytes/followingentry mismatch')
    review=rows[base+'native-review.json'];require(review['current_unsigned_word_API_machine_compatible']is True and review['hardware_execution']is False and review['C_compiles_attempted']==0 and len(review['actual_selected_far_calls'])==4,'Retained native ABI limits mismatch')
    require(review['following_gap']=={'image':'0x10e28','size':8,'raw_zero':True,'source_allocated':False,'original_SEGDEF_or_ALIGNMENT_proof':False},'Eight following bytes must remain unowned')
    snapshot=rows[base+'caller-report-snapshot.json'];observed=[]
    for caller in snapshot['rows']:
        for f in caller.get('relocations',[]):
            if f.get('target_symbol')not in ('_write_byte_far','_restore_mode_10e0d'):continue
            target=182 if f['target_symbol']=='_write_byte_far' else 221
            require(f['mode']=='far16_pointer'and f['width']==4 and f['target_segment']==0x10d3 and f['target_offset']==target,'Current farcaller ABI operands mismatch');observed.append((caller['id'],f['image_offset'],target))
    require(len(observed)==4,'Four actual retained C farcall sites required')
    return raw,{'old182_evidence_id':first_id,'tail_primary_ids':ids[1:],'tail_reachable_vs_span':[38,39],'cleanup27':True,'unowned_following8':True,'call_sites':observed}

def validate_evidence(unit,project,target_sha256,reference=None):
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    raw,proof=_evidence(project)
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Pinned expanded context required')
    require(reference['image'][BASE:BASE+248]==raw,'Whole native248 reference mismatch')
    require(not any(s<BASE+248 and s+2>BASE for s in reference['relocations']),'Serial248 MZ/crossing word forbidden')
    for name,at,target in proof['call_sites']:
        require(reference['image'][at-1]==0x9a and reference['image'][at:at+4]==target.to_bytes(2,'little')+bytes.fromhex('d310')and at+2 in reference['relocations'],'Primary C farcaller operand/MZ mismatch')
    return proof['old182_evidence_id']

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj)
    require(raw==built.code and metadata==built.metadata,'Build differs from complete serial248 object')
    require(digest(built.object_bytes)=='5988f0f3344eadda3961609db62be85d4ab0ade0301335f248bf4de5a2e87726','Whole serial248 source object changed')
    ex={k:(v['segment'],v['offset'])for k,v in BINDINGS.items()}
    linked,logs=link_segment(obj,2,{1:(0x5cc2,0),2:(0x10d3,0)},{1:0x5cc2},ex)
    primary,native=_evidence(project)
    require(len(linked)==248 and linked==primary==image[BASE:BASE+248],'Complete248 native/source bytes differ; no partial credit')
    require(not any(s<BASE+248 and s+2>BASE for s in original_sites),'Serial248 MZ/crossing words forbidden')
    loads=[]
    for base in [0,1,0x1000,0xffff]:
        externs={k:((v[0]+base)&65535,v[1])for k,v in ex.items()}
        b,l=link_segment(obj,2,{1:((0x5cc2+base)&65535,0),2:((0x10d3+base)&65535,0)},{1:(0x5cc2+base)&65535},externs)
        require(b==primary and all(f['mz_relocation_image_offset']is None for f in l),'Serial248 forward loader mismatch')
        loads.append({'load_paragraph':base,'all248bytes_exact':True,'original_mz':[],'emitted_mz':[]})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':248,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':logs,'four_load_bases':loads,'native_evidence_id':native['old182_evidence_id'],'old182_evidence_pins':EVIDENCE_PINS,'tail_evidence_pins':TAIL_EVIDENCE_PINS,'tail_native_proof':native,'function_partition_claim':False,'DATA_byte_credit':0,'authored_c_function_credit':0,'authored_asm_function_credit':0,'historical_module_or_MAP_claim':False,'following8bytes_allocated':False,'previous182_preserved':True,'replacement_only':'whole248 replaces182, never overlap'}


def assemble(source,project):
    from serial248_dgroup_generation_scope import scope
    p=Path(project);probes=[p.parent/'CHESS.EXE',p/'build/exepack/TRIM5_UNPACK.EXE',p/'build/serial248-DGROUP-offset-one-MASM-root-actual/scratch/UNIT.OBJ',p/'build/serial248-DGROUP-offset-one-MASM-root-actual/comparison.v2.json',p/'config/units.json']
    with scope(source,p,probes)as evidence:result=_assemble(source,p)
    return Build(result.object_bytes,result.code,result.metadata,dict(result.provenance,generation_guard=evidence))
