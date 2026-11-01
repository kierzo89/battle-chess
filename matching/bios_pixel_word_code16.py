"""Closed complete BIOS pixel33 ASM CODE contribution.

One observed near native procedure occupies this whole allocation. No ordinary function or initializedDATA credit.
Generation accepts only authored source and pinned tools, never target bytes.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
class BiosPixelWordError(OMFError): pass
def require(condition,message):
    if not condition: raise BiosPixelWordError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
LINK_OBJECT_SHA256='1933a53090c31564efb92a9859cfd182c2aea2e1c880ace03d913997ee71ff96'
BACKEND='masm510-bios-pixel-word-code-omf'
SOURCE='asm/link/bios_pixel_word_ea64_omf.asm'
BASE=60004
SIZE=33
SOURCE_SHA256='398fa6078a1576ad54dc79898de2d27ba531fdd2c6aa6caa4b9723e2960abe6d'
OBJECT_SHA256='1933a53090c31564efb92a9859cfd182c2aea2e1c880ace03d913997ee71ff96'
RAW_SHA256='b0b00e449cf842a13753ea4f2ebd7caddec5fd3413e606cba0dece8a2e57d060'
PUBLICS={'_bios_plot_pixel_ea64': 0}
EXTERNALS={1: '_graphics_driver_colour_110dc'}
BINDINGS={'_graphics_driver_colour_110dc': {'segment': 4365, 'offset': 12}}
RAW_EVIDENCE='build/bios-pixel-ea64/rea-bytes34.json'
PROC_EVIDENCE='build/bios-pixel-ea64/rea-current.json'
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
PROFILE_PARAMETERS={'target_kind': 'executable', 'target_format': 'dos-mz', 'architecture': 'x86', 'available_architectures': ['x86'], 'import_mode': 'ephemeral-source-immutable', 'annotation_policy': 'atomic-function-entry-metadata-v1', 'load_image_observations': 'source-mappings-entry-context-v2', 'function_body_evidence': 'complete-inclusive-ranges-v1', 'function_references': 'complete-body-and-entry-reference-manager-v2', 'location_resolution': 'explicit-address-exact-entry-symbol-first-v3', 'instruction_flow_evidence': 'decoded-return-pcode-v1', 'process_launch': 'inspected-jvm-launch-support-v1', 'load_image_evidence': 'independent-mz-mapping-relocations-v1', 'jump_table_evidence': 'typed-case-default-blocks-v1', 'decompiler_jump_loads': True, 'loader': 'MzLoader', 'language_id': 'x86:LE:16:Real Mode', 'compiler_spec_id': 'default', 'load_segment': '0x1000', 'address_coordinates': 'linear-byte-offset', 'analyzer_preset': 'ghidra-default'}
RECORD_PAYLOAD_HASHES=[(128, 0, '4fb390538337b2d69ad7c1ab5d347ae0af0bf4d3e411c89a4431eb22e98a8fd8'), (150, 13, '3d667ffa68187f19e104da5a756660cefef61cf5dfd8b1f60d3dbe0ad3d75cb4'), (152, 39, '25696e07dcd548e6e6fbb405f7806abb47a706cf563be6e72271a8e149e94a43'), (140, 49, '504a917ed09e6aef94000174026045fd5ae837066b225dfc58896e8fe96ea9a8'), (144, 84, '895d28b9addb38e2289a0e5e2dd82b099ff295add653ff86afd02f003057b818'), (136, 115, 'fd47f9fd11ee91a44ab31c40b4a2771341d5ba747d2b0f2954d92d6ea2137a48'), (160, 122, 'c216943a64ccb934802e1ab865258768a074ed82cad1e29577f70ede0b71bb67'), (156, 162, 'b1471dc59184a50660f0eab5732d80acc6490543351ed3384a0a4d1ae808aa90'), (138, 176, '6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d')]
FIELD_PROFILE=[[1, 7, 2, 2, True, [2, 1], [2, 1], None, 'c807260101', 162], [1, 15, 2, 1, True, [2, 1], [2, 1], None, 'c40f260101', 162]]
EVIDENCE_PINS={'build/bios-pixel-ea64/rea-current.json': '41accc46daac7eccceb61e572d3eef228bdefc00fb899e4f2a41d9b6779268db', 'build/bios-pixel-ea64/rea-bytes34.json': 'b7773858b71619f2319c4d666d83e17cd7d0a20e3d9f53d484fb49a6ccd40fc2', 'build/bios-pixel-ea64/proof.json': '4bce50c0f39b96afa36c28ac7fdfbfd0029b418a8d759d106136b6f7cda82ffe', 'build/bios-pixel-ea64/freeze-manifest.json': '327fd5d7095e0e02cf6577fedc19d7bfd9192aa9ee7496ac1b16bdad1fe4cdfe', 'build/bios-pixel-word33-backend-stage/actual-LINK-proof.json': '3d0d57ce08adaac9bdb489aaa32941be0fa3a6987e555564e314b09b7158bbe8', 'build/bios-pixel-word33-backend-stage/actual-LINK/PARTIAL.MAP': 'b6148852d7d7d345a00c66a6591e6a048bf69d54020e14d3d5a3c152dfa505d9', 'build/bios-pixel-word33-backend-stage/actual-LINK/LINK.LOG': '915300fdc809a3f2e7b430ae7fb86835808466633f7ec5e2cbd43d8648037ee2'}

def validate_unit(u):
    require(set(u)=={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','reference_region','boundary_evidence'},'Exact closed allocation metadata only')
    require((u.get('id'),u.get('language'),u.get('backend'),u.get('object_profile'),u.get('source'))==('bios_pixel_word_code33','asm-code',BACKEND,'bios_pixel_word33',SOURCE),'Closed BIOS33 profile/source required')
    require(u['source_sha256']==SOURCE_SHA256 and u['assembler_sha256']==MASM_SHA256,'Exact source/tool pins required')
    require(u['public_symbols']==list(PUBLICS)and u['image_offset']==hex(BASE)and type(u['size'])is int and u['size']==33,'Whole33/onePUBLIC only')
    require(u['externals']==BINDINGS and u['rea_evidence']==RAW_EVIDENCE and u['reference_region']=='unchanged-prefix','Exact native byte external view/raw primary')
    require(isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence'].strip()),'Explicit boundary explanation required')

def source_policy(content):
    try:text=content.decode('ascii')
    except UnicodeDecodeError:raise BiosPixelWordError('ASCII source required')
    live='\n'.join(line.split(';',1)[0]for line in text.splitlines())
    require(not re.search(r'\b(?:DB|DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC)\b',live,re.I),'No opcode data/padding/absolute origin/generation directives')

def extract_code(obj):
    require(isinstance(obj,OMFObject)and set(obj.segments)=={1},'Exactly one complete CODE segment; no DATA/COMMON/extraalloc')
    seg=obj.segments[1]
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.index,seg.name_index,seg.class_index,seg.overlay_index,seg.unsupported_data)==('BIOS_PIXEL_TEXT','CODE',33,72,1,3,2,1,False),'Exact WORD PUBLIC CODE33')
    require(obj.names==['','','CODE','BIOS_PIXEL_TEXT']and obj.externals==EXTERNALS,'Closed names/one actual external')
    require({k:p.offset for k,p in obj.publics.items()}==PUBLICS and all((p.segment,p.group,p.type_index)==(1,0,0)for p in obj.publics.values()),'One actual PUBLIC, no aliases')
    require(not obj.procedures,'No C/debug function credit')
    require([(k,a,digest(p))for k,a,p in obj.records]==[tuple(v)for v in RECORD_PAYLOAD_HASHES],'Whole RAW OMF record identities')
    require(len(seg.chunks)==1 and seg.chunks[0][0]==0 and len(seg.chunks[0][1])==33,'Complete33 no holes/tail')
    raw=seg.chunks[0][1];require(digest(raw)==RAW_SHA256,'Instructions/addends changed')
    fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in obj.fixups]
    require(fields==FIELD_PROFILE and raw[7:9]==raw[15:17]==bytes(2),'Exact BASE16/OFFSET16 same external frames/targets/zero addends')
    return raw,{'boundary':'complete_CODE_SEGDEF','segment':{'index':1,'name':seg.name,'class_name':seg.class_name,'length':33,'attributes':72},'publics':[asdict(p)for p in obj.publics.values()],'actual_fixup_count':2,'raw_sha256':digest(raw),'DATA_byte_credit':0,'authored_c_function_credit':0,'authored_asm_function_credit':0,'CODE_contributions':1,'driver_backing_allocation':False,'historical_module_or_original_alignment_claim':False}

@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def assemble(source,project):
    """Target-free source/tools-only generation; no placement or comparison input."""
    source,project=Path(source).resolve(),Path(project).resolve()
    require(source==(project/SOURCE).resolve() and source.is_relative_to(project),'Canonical source path required')
    require(not (project/SOURCE).is_symlink(),'Source symlink forbidden')
    content=source.read_bytes();source_policy(content);require(digest(content)==SOURCE_SHA256,'Source pin mismatch')
    tools=project/'toolchains/msc510';paths={'assembler':tools/'MASM.EXE','manifest':tools/'manifest.json','license':tools/'LICENSE','config':project/'config/msc510.json'}
    expected={'assembler':MASM_SHA256,'manifest':MANIFEST_SHA256,'license':LICENSE_SHA256,'config':CONFIG_SHA256}
    for key,p in paths.items():require(digest(p.read_bytes())==expected[key],'MASM '+key+' pin mismatch')
    for key in ['manifest','config']:
        record=next((r for r in json.loads(paths[key].read_text())['files']if r['name']=='MASM.EXE'),None)
        require(record=={'name':'MASM.EXE','sha256':MASM_SHA256,'size':110703},'MASM manifest record mismatch')
    command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
    with tempfile.TemporaryDirectory(prefix='bios-pixel-word-masm-')as tmp:
        p=Path(tmp);(p/'UNIT.ASM').write_bytes(content)
        batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n'
        (p/'RUN.BAT').write_bytes(batch.encode('ascii'))
        conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(tools)+'" -ro\nc:\nRUN.BAT\n'
        (p/'dosbox.conf').write_text(conf)
        r=subprocess.run(['dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=45)
        require(r.returncode==0 and (p/'RESULT.TXT').is_file() and (p/'RESULT.TXT').read_text().strip()=='assembled' and (p/'UNIT.OBJ').is_file(),'MASM generation failed')
        log=(p/'MASM.LOG').read_text(encoding='cp437');require('Macro Assembler Version 5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'MASM warnings/errors/version')
        data=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_text(encoding='cp437')
    require(digest(source.read_bytes())==SOURCE_SHA256,'Source changed during generation')
    for key,p in paths.items():require(digest(p.read_bytes())==expected[key],'MASM '+key+' changed during generation')
    require(digest(data)==OBJECT_SHA256,'Complete object pin mismatch')
    raw,metadata=extract_code(read_omf(data))
    return Build(data,raw,metadata,{'source_sha256':digest(content),'assembler_sha256':MASM_SHA256,'assembler_manifest_sha256':MANIFEST_SHA256,'assembler_license_sha256':LICENSE_SHA256,'assembler_configuration_sha256':CONFIG_SHA256,'compiler':'Microsoft Macro Assembler5.10','build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':digest(data),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','dosbox_configuration':conf,'batch_source':batch,'dosbox_stdout':r.stdout.decode('utf-8','replace'),'dosbox_stderr':r.stderr.decode('utf-8','replace'),'generation_target_input':False,'generation_original_placement_input':False})

def link(obj,externals,image_origin=BASE):
    """Closed symbolic BASE16 and OFFSET16 for the same external BYTE."""
    raw,_=extract_code(obj);require(set(externals)==set(EXTERNALS.values()),'Exactly actual external BYTE view required')
    require(type(image_origin)is int and 0<=image_origin<=0x1fffff-SIZE,'Complete CODE placement required')
    value=externals['_graphics_driver_colour_110dc']
    require(isinstance(value,(tuple,list))and len(value)==2 and all(type(n)is int and 0<=n<=65535 for n in value),'Actual segment/offset external placement required')
    code=bytearray(raw);logs=[]
    for f in obj.fixups:
        base=f.location_type==2;encoded=value[0 if base else 1].to_bytes(2,'little');code[f.offset:f.offset+2]=encoded
        logs.append({'segment':1,'object_offset':f.offset,'image_offset':image_origin+f.offset,'width':2,'mode':'external_BYTE_BASE16'if base else'external_BYTE_OFFSET16','frame':list(f.frame),'target':list(f.target),'target_symbol':EXTERNALS[1],'displacement':None,'encoded_hex':encoded.hex(),**({'mz_segment_relocation_image_offset':image_origin+f.offset}if base else{})})
    return bytes(code),logs

def _subject(e,operation):
    provider={'id':'ghidra','name':'Ghidra','version':'12.1.4'};p=e.get('analysis_profile',{})
    require(e.get('subject',{}).get('digest',{}).get('sha256')==CARRIER_SHA256 and e['subject'].get('format')=='dos-mz'and e['subject'].get('architecture')=='x86','Pinned native subject/format/architecture')
    require(e.get('provider')==provider and p.get('provider')==provider and p.get('digest')==PROFILE and p.get('parameters')==PROFILE_PARAMETERS,'Exact provider/loader/profile parameters')
    require(e.get('operation')==operation and re.fullmatch(r'ev_[0-9a-f]{64}',e.get('evidence_id',''))is not None,'Operation/identity required')

def _evidence(project):
    records={}
    for rel,pin in EVIDENCE_PINS.items():
        content=(Path(project)/rel).read_bytes();require(digest(content)==pin,'Primary/candidate freeze pin mismatch: '+rel);
        if rel.endswith('.json'):records[rel]=json.loads(content)
    e=records[RAW_EVIDENCE];_subject(e,'read_bytes');r=e['normalized_result']
    require(e['parameters']=={'address':'0x1ea64','length':34}and r.get('address')=='0x1ea64'and r.get('complete')is True and r['requested_bytes']==r['returned_bytes']==34,'Complete raw34 parameters')
    raw=bytes.fromhex(r['bytes_hex']);require(len(raw)==34 and raw[-1]==0,'Complete34 with excluded next zero context')
    p=records[PROC_EVIDENCE];_subject(p,'analyze_function');body=p['normalized_result']['procedure'];b=body['body']
    require(p['evidence_id']!=e['evidence_id']and p['parameters']=={'procedure':'0x1ea64'}and body['address']=='0x1ea64'and not body['classification']['external']and not body['classification']['thunk'],'Distinct exact native entry')
    require(b['available']is True and b['contains_entry']is True and b['non_contiguous']is False and b['ranges']==[{'start':'0x1ea64','end':'0x1ea84'}]and b['total_bytes']==b['span_bytes']==33,'Complete contiguous native33')
    # Raw8EC0 encodes MOV ES,AX despite provider's reversed segment-MOV display.
    require(raw[9:11]==bytes.fromhex('8ec0')and raw[11:17]==bytes.fromhex('b40c26a00c00')and raw[26:28]==bytes.fromhex('cd10'),'Native BIOS write-pixel/driver BYTE instruction identity')
    _alignment(project,records)
    return raw,e['evidence_id']

def _sites(sites):
    observed=sorted(s for s in sites if s<BASE+SIZE and s+2>BASE)
    require(observed==[0xea6b],'One whole native BASE16 MZ site only/no crossing words');return observed

def _forward(raw,load):
    out=bytearray(raw);out[7:9]=((int.from_bytes(out[7:9],'little')+load)&65535).to_bytes(2,'little');return bytes(out)

def validate_evidence(unit,project,target_sha256,reference=None):
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256 and reference['prefix_size']>=BASE+33,'Whole unchanged original prefix required')
    _sites(reference['relocations']);raw,eid=_evidence(project)
    require(_forward(reference['image'][BASE:BASE+34],0x1000)==raw,'Original prefix/carrier full34 forward-loader identity')
    return eid

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);require(digest(built.object_bytes)==OBJECT_SHA256,'Whole output object pin')
    o=read_omf(built.object_bytes);raw,metadata=extract_code(o);require(raw==built.code and metadata==built.metadata,'Complete generated allocation identity')
    primary,eid=_evidence(project);sites=_sites(original_sites)
    require(_forward(image[BASE:BASE+34],0x1000)==primary,'Native full34 context identity')
    linked,logs=link(o,{'_graphics_driver_colour_110dc':(0x110d,12)})
    require([f['mz_segment_relocation_image_offset']for f in logs if 'mz_segment_relocation_image_offset'in f]==sites,'Exact complete emitted MZ set')
    loads=[]
    for load in [0,1,0x1000,0xffff]:
        b,f=link(o,{'_graphics_driver_colour_110dc':((0x110d+load)&65535,12)},image_origin=BASE+load*16)
        require(b==_forward(linked,load),'Source fields/loader arithmetic mismatch')
        loads.append({'load_paragraph':load,'actual_external_segment':(0x110d+load)&65535,'all33_native_equal':b==_forward(image[BASE:BASE+33],load),'source_loader_arithmetic_exact':True})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':33,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':linked==image[BASE:BASE+33],'whole_original_mz_sites':sites,'emitted_mz_sites':sites,'relocations':logs,'four_load_bases':loads,'native_evidence_id':eid,'evidence_sha256':EVIDENCE_PINS,'complete_raw34_context':True,'following_zero_not_allocated':True,'segment_MOV_provider_display_erratum_preserved':True,'driver_BYTE_backing_allocation':False,'authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'historical_module_or_original_alignment_claim':False,'full_BIOS_hardware_execution_claim':False}


def _alignment(project,records):
    p=records['build/bios-pixel-word33-backend-stage/actual-LINK-proof.json']
    require(p['physical_source_objects']==200 and len(p['input_objects'])==200 and p['input_objects'][-1]['sha256']==LINK_OBJECT_SHA256,'Actual199 plus same source WORD33 object required')
    require(p['prior_undefined']==198 and p['current_undefined']==199 and p['actual_undefined_added']==['_graphics_driver_colour_110dc']and p['actual_undefined_removed']==[]and p['new_symbolic_colour_stays_undefined']is True,'No synthetic provider or removed unresolved obligation')
    require(p['original_target_read_or_mounted']is False and p['new_stub_prefix_colour_backing']is False and p['forced_offset4_or_padding_ORG']is False and p['executed']is False,'Authentic partialLINK only, no prefix/stubs/hardware claim')
    text=(Path(project)/'build/bios-pixel-word33-backend-stage/actual-LINK/PARTIAL.MAP').read_text()
    pubs=re.findall(r'\b([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+_bios_plot_pixel_ea64\b',text)
    require(bool(pubs)and len(set(pubs))==1,'Exact real PUBLIC MAP')
    cs,offset=[int(x,16)for x in pubs[0]];physical=cs*16+offset
    lines=[line for line in text.splitlines()if 'BIOS_PIXEL_TEXT'in line]
    require(len(lines)==1 and re.search(r'(?i)0F274H\s+0F294H\s+00021H\s+BIOS_PIXEL_TEXT\s+CODE',lines[0])is not None,'Whole33 source segment in actual MAP')
    require([cs,offset]==p['public_segment_offset']==[0x0f27,4]and physical==p['public_physical_image_offset']==0xf274 and physical%2==BASE%2==0 and p['source_SEGDEF_alignment_bytes']==2,'Actual WORD2 placement compatible with native evenEA64; no absoluteMAP equality claim')
    return {'alignment_bytes':2,'actual_LINK_PUBLIC':[cs,offset],'actual_LINK_physical':physical,'native_even_compatible':True,'final_native_placement_proven':False}
