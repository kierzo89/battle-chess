"""Closed symbolic blit873 ASM contribution; no ordinary function/DATA credit.
Target-free pinned source/tool generation is separate from complete comparison.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
from library16 import link_segment
class BlitCodeError(OMFError): pass
def require(condition,message):
    if not condition: raise BlitCodeError(message)
def digest(data): return hashlib.sha256(data).hexdigest()
BACKEND='masm510-blit-code-contribution-omf'
SOURCE='asm/link/blit_e57a_omf.asm'
SOURCE_SHA256='5b43ba68ada64d0147127b2e8eb2749f31eef56bfbe00f79201802cf415cd675'
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
RAW_SHA256='fc28839039edea383811ae2bdd3b655967a28082a181147b7117079b287f4308'
BASE=0xe462
SIZE=873
PUBLICS={'_blit_e57a':280}
BINDINGS={'_blit':{'segment':0x5cc2,'offset':0x4924}}
EXTERNALS={1:'_blit'}
RAW_EVIDENCE='build/blit-e57a-native-review/rea-context900.json'
NATIVE_EVIDENCE='build/blit-e57a-native-review/rea-native.json'
CFG_EVIDENCE='build/blit-e57a-native-review/focused-review.json'
REPLAY_EVIDENCE='build/blit-e57a-sixpath-execution/execution-proof.json'
REPLAY_REVIEW='build/blit-e57a-sixpath-execution/dependency-and-model-review.json'
CALL_EVIDENCE='build/blit-e57a-native-review/rea-xrefs-entry.json'
EVIDENCE_PINS={'build/blit-e57a-native-review/rea-context900.json': '8d9fe21c6895560ee746ab340321836d7cb24d43810829dba1b968f410cc49f1', 'build/blit-e57a-native-review/rea-native.json': 'd6b94d6ab264b2048224f1fad446712f96a825d523f24d0a02d801a180a19277', 'build/blit-e57a-native-review/focused-review.json': 'b66fb2a20af51f87607cb192a0f53107ec5e7087294b8c35a9dfb7a4abd09797', 'build/blit-e57a-sixpath-execution/execution-proof.json': '72d5943101955344e009d30b4596ecfd3ffa0d832fc128ef7c453b50cb1c904e', 'build/blit-e57a-sixpath-execution/dependency-and-model-review.json': '1820012e1702d4bcc3f1d513d0cab35bc974b8230f12d7a08de85d1d71e06485', 'build/blit-e57a-native-review/rea-xrefs-entry.json': '7ff1ddd374fdfe0107d08a06bde66bd715bdd328fdefd93a0dd6d9e1f1b07ec2', 'build/blit-e57a-symbolic873/caller-API-review.json': 'e7e63d93f81944dcae29cbb523fd6ca4168ef99e44c10985520f4219afeae11e'}
PROFILE_PARAMETERS={'target_kind': 'executable', 'target_format': 'dos-mz', 'architecture': 'x86', 'available_architectures': ['x86'], 'import_mode': 'ephemeral-source-immutable', 'annotation_policy': 'atomic-function-entry-metadata-v1', 'load_image_observations': 'source-mappings-entry-context-v2', 'function_body_evidence': 'complete-inclusive-ranges-v1', 'function_references': 'complete-body-and-entry-reference-manager-v2', 'location_resolution': 'explicit-address-exact-entry-symbol-first-v3', 'instruction_flow_evidence': 'decoded-return-pcode-v1', 'process_launch': 'inspected-jvm-launch-support-v1', 'load_image_evidence': 'independent-mz-mapping-relocations-v1', 'jump_table_evidence': 'typed-case-default-blocks-v1', 'decompiler_jump_loads': True, 'loader': 'MzLoader', 'language_id': 'x86:LE:16:Real Mode', 'compiler_spec_id': 'default', 'load_segment': '0x1000', 'address_coordinates': 'linear-byte-offset', 'analyzer_preset': 'ghidra-default'}
FIXUPS=[(268, 2, 1, True, (0, 2), (0, 2), 409), (270, 2, 1, True, (0, 2), (0, 2), 453), (272, 2, 1, True, (0, 2), (0, 2), 537), (274, 2, 1, True, (0, 2), (0, 2), 614), (276, 2, 1, True, (0, 2), (0, 2), 731), (278, 2, 1, True, (0, 2), (0, 2), 781), (286, 2, 1, True, (1, 1), (2, 1), None), (290, 2, 1, True, (1, 1), (2, 1), 2), (293, 2, 1, True, (1, 1), (2, 1), 4), (300, 2, 1, False, (0, 2), (0, 2), 868), (304, 2, 1, True, (0, 2), (0, 2), None), (307, 2, 1, True, (1, 1), (2, 1), 6), (314, 2, 1, False, (0, 2), (0, 2), 868), (318, 2, 1, True, (0, 2), (0, 2), 2), (321, 2, 1, True, (1, 1), (2, 1), 8), (325, 2, 1, True, (0, 2), (0, 2), 4), (328, 2, 1, True, (1, 1), (2, 1), 10), (332, 2, 1, True, (0, 2), (0, 2), 6), (336, 2, 1, True, (1, 1), (2, 1), 16), (339, 2, 1, True, (1, 1), (2, 1), 12), (343, 2, 1, True, (1, 1), (2, 1), 14), (354, 2, 1, True, (0, 2), (0, 2), 8), (359, 2, 1, True, (0, 2), (0, 2), 10), (363, 2, 1, True, (1, 1), (2, 1), 20), (407, 2, 1, True, (0, 2), (0, 2), 268), (412, 2, 1, True, (0, 2), (0, 2), None), (418, 2, 1, True, (0, 2), (0, 2), 8), (430, 2, 1, True, (0, 2), (0, 2), 10), (436, 2, 1, True, (0, 2), (0, 2), 4), (441, 2, 1, True, (0, 2), (0, 2), 6), (446, 2, 1, True, (0, 2), (0, 2), 2), (451, 2, 1, False, (0, 2), (0, 2), 868), (456, 2, 1, True, (0, 2), (0, 2), None), (464, 2, 1, True, (0, 2), (0, 2), 8), (495, 2, 1, True, (0, 2), (0, 2), 10), (520, 2, 1, True, (0, 2), (0, 2), 4), (525, 2, 1, True, (0, 2), (0, 2), 6), (530, 2, 1, True, (0, 2), (0, 2), 2), (535, 2, 1, False, (0, 2), (0, 2), 868), (538, 2, 1, True, (0, 2), (0, 2), 12), (543, 2, 1, True, (0, 2), (0, 2), None), (549, 2, 1, True, (0, 2), (0, 2), 8), (576, 2, 1, True, (0, 2), (0, 2), 10), (597, 2, 1, True, (0, 2), (0, 2), 4), (602, 2, 1, True, (0, 2), (0, 2), 6), (607, 2, 1, True, (0, 2), (0, 2), 2), (612, 2, 1, False, (0, 2), (0, 2), 868), (615, 2, 1, True, (0, 2), (0, 2), 12), (620, 2, 1, True, (0, 2), (0, 2), None), (628, 2, 1, True, (0, 2), (0, 2), 8), (674, 2, 1, True, (0, 2), (0, 2), 10), (714, 2, 1, True, (0, 2), (0, 2), 4), (719, 2, 1, True, (0, 2), (0, 2), 6), (724, 2, 1, True, (0, 2), (0, 2), 2), (729, 2, 1, False, (0, 2), (0, 2), 868), (734, 2, 1, True, (0, 2), (0, 2), None), (740, 2, 1, True, (0, 2), (0, 2), 8), (755, 2, 1, True, (0, 2), (0, 2), 10), (764, 2, 1, True, (0, 2), (0, 2), 4), (769, 2, 1, True, (0, 2), (0, 2), 6), (774, 2, 1, True, (0, 2), (0, 2), 2), (784, 2, 1, True, (0, 2), (0, 2), None), (792, 2, 1, True, (0, 2), (0, 2), 8), (826, 2, 1, True, (0, 2), (0, 2), 10), (854, 2, 1, True, (0, 2), (0, 2), 4), (859, 2, 1, True, (0, 2), (0, 2), 6), (864, 2, 1, True, (0, 2), (0, 2), 2)]

def validate_unit(unit):
    allowed={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','boundary_evidence','reference_region'}
    require(set(unit)<=allowed,'Foreign function/ownership/slice metadata')
    require((unit.get('id'),unit.get('language'),unit.get('backend'),unit.get('object_profile'),unit.get('source'))==('blit_e57a_code873','asm-code',BACKEND,'blit_dependency873',SOURCE),'Closed blit873 profile/source required')
    require(unit.get('source_sha256')==SOURCE_SHA256 and unit.get('assembler_sha256')==MASM_SHA256,'Pinned blit source/MASM required')
    require(unit.get('public_symbols')==list(PUBLICS) and unit.get('image_offset')==hex(BASE) and type(unit.get('size'))is int and unit['size']==873,'Complete873/onePUBLIC required; no slices')
    require(unit.get('externals')==BINDINGS and unit.get('rea_evidence')==RAW_EVIDENCE and unit.get('reference_region','unchanged-prefix')=='unchanged-prefix','Closed native comparison bindings/evidence required')

def extract_code(obj):
    require(isinstance(obj,OMFObject) and set(obj.segments)=={1,2},'Exactly emptyDATA and wholeCODE required')
    data,seg=obj.segments[1],obj.segments[2]
    require((data.name,data.class_name,data.length,data.attributes,data.unsupported_data,data.chunks)==('_DATA','DATA',0,72,False,[]),'Empty DATA0 only; no initialized DATA or BSS')
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.unsupported_data)==('_TEXT','CODE',873,72,False),'Whole WORD CODE873 required')
    require(obj.names==['','','DGROUP','DATA','CODE','_DATA','_TEXT'],'Closed segment/group names required')
    require((data.index,data.name_index,data.class_index,data.overlay_index)==(1,5,3,1) and (seg.index,seg.name_index,seg.class_index,seg.overlay_index)==(2,6,4,1),'Closed SEGDEF indices/overlay required')
    require(obj.externals==EXTERNALS,'Exact one external name/index required')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and len(obj.publics)==1 and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'One genuine PUBLIC entry only, no aliases')
    require(not obj.procedures,'No fabricated C procedure metadata')
    require([k for k,_,_ in obj.records]==[0x80,0x96,0x98,0x98,0x9a,0x8c,0x90,0x88,0xa0,0x9c,0x8a],'Closed record sequence; no COMMON/LIDATA/debug/extraallocation')
    for kind,expected,message in [(0x80,[b'\x08UNIT.ASM'],'Deterministic UNIT.ASM THEADR'),(0x9a,[b'\x02\xff\x01'],'Exact DGROUP containing emptyDATA'),(0x88,[b'\x00\xa2\x01'],'Reviewed MASM linker directive'),(0x8a,[b'\x00'],'No executable entry metadata')]:
        require([p for k,_,p in obj.records if k==kind]==expected,message)
    raw=bytearray()
    for at,content in sorted(seg.chunks):
        require(content and at==len(raw) and at+len(content)<=seg.length,'CODE hole/overlap/excess');raw.extend(content)
    require(len(raw)==873,'Omitted CODE tail')
    require(all(f.segment==2 for f in obj.fixups) and [(f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in obj.fixups]==FIXUPS,'Exact67 fields/frames/targets/displacements required')
    require(digest(raw)==RAW_SHA256,'Unlinked instructions/addends changed')
    require(raw[:12]==bytes(12) and raw[778:781]==bytes.fromhex('eb5890'),'Actual consumed CS words/natural forwardJMP relaxation required')
    return bytes(raw),{'boundary':'complete_dependency_closed_CODE_SEGDEF','segment':{'index':2,'name':seg.name,'class_name':seg.class_name,'attributes':72,'length':873},'empty_data_segment':{'index':1,'name':'_DATA','length':0},'group':{'index':1,'name':'DGROUP','segments':[1]},'publics':[asdict(p)for p in obj.publics.values()],'internal_components':[{'kind':'consumed_CS_scratch','offset':0,'size':12},{'kind':'functional_transparency_table','offset':12,'size':256},{'kind':'six_symbolic_dispatch_targets','offset':268,'size':12},{'kind':'raw_instruction_span','offset':280,'size':593,'ordinary_REA_live':134,'conditional_CFG_live':592,'native_unreachable_NOP':1}],'actual_fixup_count':67,'field_classes':{'ownCODE_OFFSET16':51,'DS_OFFSET16':10,'ownCODE_self_relative16':6},'raw_sha256':digest(raw),'authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'CODE_contributions':1}

@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def assemble(source,project):
    """Accept source+tool identity only; no comparison bytes, size or placements."""
    source,project=Path(source).resolve(),Path(project).resolve()
    require(not any(c in str(project) for c in '\r\n\"'),'Unsafe assembler project path')
    require(source==(project/SOURCE).resolve() and source.is_relative_to(project),'Canonical source path required')
    content=source.read_bytes();require(digest(content)==SOURCE_SHA256,'Source pin mismatch')
    tools=project/'toolchains/msc510';paths={'assembler':tools/'MASM.EXE','manifest':tools/'manifest.json','license':tools/'LICENSE','config':project/'config/msc510.json'}
    expected={'assembler':MASM_SHA256,'manifest':MANIFEST_SHA256,'license':LICENSE_SHA256,'config':CONFIG_SHA256}
    for key,p in paths.items():require(digest(p.read_bytes())==expected[key],'MASM '+key+' pin mismatch')
    for key in ['manifest','config']:
        record=next((r for r in json.loads(paths[key].read_text())['files']if r['name']=='MASM.EXE'),None)
        require(record=={'name':'MASM.EXE','sha256':MASM_SHA256,'size':110703},'MASM manifest record mismatch')
    command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
    with tempfile.TemporaryDirectory(prefix='blit-masm-')as tmp:
        p=Path(tmp);require(not any(c in str(p) for c in '\r\n\"'),'Unsafe assembler scratch path');(p/'UNIT.ASM').write_bytes(content)
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
    provider={'id':'ghidra','name':'Ghidra','version':'12.1.4'};p=e.get('analysis_profile',{});subject=e.get('subject',{})
    require(subject.get('digest',{}).get('sha256')==sha and subject.get('format')=='dos-mz' and subject.get('architecture')=='x86' and e.get('operation')==operation,'Native subject/operation mismatch')
    require(e.get('provider')==provider and p.get('provider')==provider and p.get('digest')==PROFILE and p.get('parameters')==PROFILE_PARAMETERS,'Native provider/profile/loader parameters mismatch')
    require(re.fullmatch(r'ev_[0-9a-f]{64}',e.get('evidence_id',''))is not None,'Missing evidence identity')

def _evidence(project):
    records={};project=Path(project).resolve()
    for rel,pin in EVIDENCE_PINS.items():
        path=(project/rel).resolve();require(path.is_relative_to(project),'Evidence outside project')
        b=path.read_bytes();require(digest(b)==pin,'Primary/derived evidence pin mismatch: '+rel);records[rel]=json.loads(b)
    e=records[RAW_EVIDENCE];_subject(e,ORIGINAL_SHA256,'read_bytes');r=e['normalized_result']
    require(e['parameters']=={'address':'0x1e462','length':900} and r.get('address')=='0x1e462' and r.get('complete')is True and r['requested_bytes']==r['returned_bytes']==900,'Complete900 original primary required')
    raw=bytes.fromhex(r['bytes_hex']);require(len(raw)==900,'Primary byte length')
    n=records[NATIVE_EVIDENCE];_subject(n,ORIGINAL_SHA256,'analyze_function');p=n['normalized_result']['procedure'];b=p['body']
    require(n['parameters']=={'procedure':'0x1e57a'} and p['address']=='0x1e57a' and not p['classification']['external'] and not p['classification']['thunk'],'Actual near entry primary required')
    require(b.get('available')is True and b['contains_entry'] and b['non_contiguous']is True and b['total_bytes']==134 and b['span_bytes']==593 and b['ranges']==[{'start':'0x1e57a','end':'0x1e5fa'},{'start':'0x1e7c6','end':'0x1e7ca'}],'Preserve partial ordinary134/span593 native boundary')
    x=records[CALL_EVIDENCE];_subject(x,ORIGINAL_SHA256,'xrefs')
    require(x['parameters']=={'address':'0x1e57a'} and x['normalized_result']==['0x13d52','0x13e46','0x1427d','0x1450e'],'Exact four native near caller references')
    require(len({v['evidence_id']for v in(e,n,x)})==3,'Distinct native primary identities required')
    mask=bytes((0xf0 if v&0xf0==0 else 0)|(15 if v&15==0 else 0)for v in range(256))
    require(raw[:12]==bytes(12) and raw[12:268]==mask,'Consumed CS scratch/mask table mismatch')
    targets=[int.from_bytes(raw[i:i+2],'little')for i in range(268,280,2)]
    require(targets==[0xe5fb,0xe627,0xe67b,0xe6c8,0xe73d,0xe76f],'Exact six native dispatch words required')
    cfg=records[CFG_EVIDENCE]['secondary_CFG'];graph=cfg['graph'];entries=set();owned=set()
    for q in graph:
        a=int(q['address'],0);content=bytes.fromhex(q['bytes']);at=a-BASE
        require(a not in entries and content and 280<=at<873 and at+len(content)<=873 and raw[at:at+len(content)]==content,'Private raw instruction partition mismatch');entries.add(a)
        here=set(range(at,at+len(content)));require(not(owned&here),'Private raw instruction overlap');owned|=here
        require(all(0xe57a<=int(s,0)<0xe7cb for s in q['successors']),'Private CFG escapes known scope')
    require(len(entries)==231 and owned==set(range(280,873))-{780} and raw[780]==0x90,'Exact conditional592live/rawNOP1 scope required')
    require(cfg['conditionally_reachable_bytes']==592 and cfg['span_bytes']==593 and cfg['not_REA_complete_CFG_or_historical_source_proof']is True,'Do not forge ordinary CFG completeness')
    dispatch=next(q for q in graph if q['address']=='0xe5f6');require([int(v,0)for v in dispatch['successors']]==targets,'Private dispatch target closure mismatch')
    replay=records[REPLAY_EVIDENCE];cases=replay['cases'];seen=set()
    require(replay['native_raw_primary']==e['evidence_id'] and replay['case_count']==75 and len(cases)==75 and replay['actual_native_instruction_execution']is True and replay['instruction_or_decoder_hooks_substituted']is False,'Bounded native75 execution provenance required')
    flags=['all_destination_bytes_match_independent_nibble_model','all_memory_unchanged_outside_exact_native_write_footprint','source_not_written','code_tables_unchanged','DS_global_record_unchanged','DS_SI_DI_BP_SS_restored_SP_nearRET_plus2']
    for c in cases:
        require(c['mode']in(0,1,2) and c['shift']in(0,1,2,3) and all(c.get(k)is True for k in flags),'Bounded replay mode/ABI/footprint mismatch')
        require(set(c['instruction_offsets'])<=entries,'Replay executed outside authenticated CFG');seen.update(c['instruction_offsets'])
        expected=hex(targets[2*c['mode']+(c['shift']&1)])if c['width_words']and c['height_rows']else None
        require(c['selected_handler']==expected,'Replay actual dispatch mismatch')
    require(seen==entries,'Replay misses authenticated conditional instruction entries')
    review=records[REPLAY_REVIEW]
    require(review['native_cases']==75 and review['actual_six_handler_paths']is True and review['all12_mode_shift_pairs']is True and review['all_conditionally_live592bytes_executed']is True and review['unreachable_native90_E76E_not_executed']is True,'Derived replay coverage limit changed')
    require(raw[778:781]==bytes.fromhex('eb5890'),'Actual natural forwardJMP relaxation missing')
    api=records['build/blit-e57a-symbolic873/caller-API-review.json']
    require(api['provider_public']=='_blit_e57a' and api['all_current_function_declarations_agree']is True and api['caller_source_changes']==0 and api['no_new_backing_capacity']is True and len(api['actual_source_calls'])==4,'Pinned near API/storage limits mismatch')
    return raw,e['evidence_id']

def validate_evidence(unit,project,target_sha256,reference=None):
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    raw,evidence_id=_evidence(project)
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Pinned expanded context required')
    require(reference['image'][BASE:BASE+900]==raw,'Primary/reference whole context mismatch')
    require(not any(s<BASE+873 and s+2>BASE for s in reference['relocations']),'Blit context MZ/crossing word forbidden')
    return evidence_id

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj)
    require(raw==built.code and metadata==built.metadata,'Build differs from complete object')
    externs={k:(v['segment'],v['offset'])for k,v in BINDINGS.items()}
    linked,logs=link_segment(obj,2,{1:(0x5cc2,0),2:(0,BASE)},{1:0x5cc2},externs)
    primary,evidence_id=_evidence(project)
    require(len(linked)==873 and linked==primary[:873]==image[BASE:BASE+873],'Complete873 native/source bytes differ; no partial credit')
    require(not any(s<BASE+873 and s+2>BASE for s in original_sites),'Blit MZ set must be empty, no crossing words')
    loads=[]
    for base in(0,1,0x1000,0xffff):
        b,l=link_segment(obj,2,{1:((0x5cc2+base)&65535,0),2:(base,BASE)},{1:(0x5cc2+base)&65535},{k:((v[0]+base)&65535,v[1])for k,v in externs.items()})
        require(b==primary[:873] and len(l)==67 and all(f['mz_relocation_image_offset']is None for f in l),'Forward loader arithmetic mismatch')
        loads.append({'load_paragraph':base,'all873bytes_exact':True,'original_mz':[],'emitted_mz':[]})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':873,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':logs,'four_load_bases':loads,'native_evidence_id':evidence_id,'evidence_sha256':EVIDENCE_PINS,'native_boundary_limit':'ordinary134/span593; private conditionalCFG592+rawNOP1 and75syntheticnativecases','function_partition_claim':False,'DATA_byte_credit':0,'authored_c_function_credit':0,'authored_asm_function_credit':0,'historical_module_or_MAP_claim':False,'following_odd_table_alignment_resolved':False,'missing_source_storage':['_blit DS5CC2:4924']}
