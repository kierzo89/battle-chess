"""Versioned five-DGROUP-frame graphics1488 ASM allocation; zero added credit.
Source-only generation and authenticated source-link arithmetic precede comparison.
Replaces the prior873 allocation; no historical unique module/MAP claim.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
import graphics1488_dgroup_link16 as adapter
import blit_code16 as prefix
class GraphicsCodeError(OMFError):pass
def require(value,message):
    if not value:raise GraphicsCodeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
BACKEND='masm510-graphics-dgroup-code-contribution-omf'
SOURCE='asm/link/graphics_blit_text_dgroup_omf.asm'
SOURCE_SHA256='af98cd1b7372cbe27fd9c1cb88623f5f23eed3f9db0bb726d4924a94b5a2e21e'
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'

BASE=0xe462
SIZE=1488
RAW_SHA256='d30daecd2b2fc10d25fbda776cd208c60f136c34a92044ca1fafcbff5bcbacf5'
PUBLICS=adapter.PUBLICS
EXTERNALS=adapter.EXTERNALS
BINDINGS={'_font_glyphs':{'segment':0x5cc2,'offset':0x4524},'_text_cursor':{'segment':0x5cc2,'offset':0x4520},'_graphics_end':{'segment':0x11ef,'offset':0},'_color_buffer':{'segment':0x120d,'offset':0x32e0},'_text_glyph_pixels':{'segment':0x5cc2,'offset':0x4500},'_text_colour_words':{'segment':0x5cc2,'offset':0x44e0},'_graphics_copy':{'segment':0x110d,'offset':0},'_graphics_begin':{'segment':0x11ef,'offset':0x1e},'_blit':{'segment':0x5cc2,'offset':0x4924}}
MZ_SITES=[0xe8d1,0xe918,0xe9af,0xea25]
RAW_EVIDENCE='build/graphics-following-e8cb-e915/rea-cluster615-next41.json'
PREPARE_EVIDENCE='build/blit-e57a-sixpath-execution/rea-following-e8cb.json'
DRAW_EVIDENCE='build/graphics-following-e8cb-e915/rea-draw-text-e915.json'
NEXT_EVIDENCE='evidence/rea_newinput_poll_ea32.json'
API_EVIDENCE='build/graphics-following-e8cb-e915/API-and-ownership-review.json'
EVIDENCE_PINS={'blit_code16.py': '2828451bdc2b786ceb4f9931f63aca1aa8662616181f1ab95ef4f67727bbc125', 'build/graphics-following-e8cb-e915/rea-cluster615-next41.json': '39dea84169266ce27636872cebf8ea305388d7574ce734a2d290d6d4043139bc', 'build/blit-e57a-sixpath-execution/rea-following-e8cb.json': '7895fd41421d026addd348bf1403dca8794ed80da98e80e3a560aa6b91673f91', 'build/graphics-following-e8cb-e915/rea-draw-text-e915.json': '430534f46cc003bc180611dc1f15454c442509938e3c229c0c6f2f4e67a03f48', 'evidence/rea_newinput_poll_ea32.json': '33d8851d632b5f8f9df7351a1e789323c1b690668b17d5446993e43836d05b63', 'build/graphics-following-e8cb-e915/API-and-ownership-review.json': '1d23c530f2e6bf7fc1bfa76b7b8bf45ca7aa5cecbdbecb0ead59c7d4e383e646', 'graphics1488_dgroup_link16.py': 'aae6276b466ba45c228f17a7acbc45e9f02dda006ac09c1655c3a9f28d93c495'}
NEXT_RAW_SHA256='35b4dc1675b05e35f419a8ff6a4eeb43686fae64e4c7b340acaf3ac2ecb795a2'
PREPARE_BLOCKS=[{'start': '0x1e8cb', 'end': '0x1e903', 'successors': ['0x1e903']}, {'start': '0x1e903', 'end': '0x1e90d', 'successors': ['0x1e903', '0x1e90d']}, {'start': '0x1e90d', 'end': '0x1e915', 'successors': []}]
DRAW_BLOCKS=[{'start': '0x1e915', 'end': '0x1e9a4', 'successors': ['0x1e9a4']}, {'start': '0x1e9a4', 'end': '0x1e9a9', 'successors': ['0x1e9a9', '0x1e9b2']}, {'start': '0x1e9a9', 'end': '0x1e9b2', 'successors': []}, {'start': '0x1e9b2', 'end': '0x1e9cb', 'successors': ['0x1e9cb']}, {'start': '0x1e9cb', 'end': '0x1ea07', 'successors': ['0x1e9cb', '0x1ea07']}, {'start': '0x1ea07', 'end': '0x1ea32', 'successors': ['0x1e9a4']}]

def validate_unit(unit):
    allowed={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','boundary_evidence','reference_region'}
    require(set(unit)<=allowed,'Foreign function/ownership/slice metadata')
    require((unit.get('id'),unit.get('language'),unit.get('backend'),unit.get('object_profile'),unit.get('source'))==('graphics_blit_text_code1488','asm-code',BACKEND,'graphics_blit_text1488_dgroup',SOURCE),'Closed graphics1488 profile/source required')
    require(unit.get('source_sha256')==SOURCE_SHA256 and unit.get('assembler_sha256')==MASM_SHA256,'Pinned graphics source/MASM required')
    require(unit.get('public_symbols')==list(PUBLICS) and unit.get('image_offset')==hex(BASE) and type(unit.get('size'))is int and unit['size']==SIZE,'Complete1488/threePUBLIC required; no slices')
    require(unit.get('externals')==BINDINGS and unit.get('rea_evidence')==RAW_EVIDENCE and unit.get('reference_region','unchanged-prefix')=='unchanged-prefix','Closed native bindings/evidence required')

def extract_code(obj):
    require(isinstance(obj,OMFObject)and set(obj.segments)=={1,2},'Exactly emptyDATA and wholeCODE required')
    data,seg=obj.segments[1],obj.segments[2]
    require((data.name,data.class_name,data.length,data.attributes,data.unsupported_data,data.chunks)==('_DATA','DATA',0,72,False,[]),'Empty DATA0 only; no fake backing allocation')
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.unsupported_data)==('_TEXT','CODE',SIZE,72,False),'Whole WORD CODE1488 required')
    require(obj.names==['','','DGROUP','DATA','CODE','_DATA','_TEXT'],'Closed segment/group names')
    require((data.index,data.name_index,data.class_index,data.overlay_index)==(1,5,3,1)and(seg.index,seg.name_index,seg.class_index,seg.overlay_index)==(2,6,4,1),'Closed SEGDEF indices/overlay')
    require(obj.externals==EXTERNALS,'Exact nine external names/indices')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and len(obj.publics)==3 and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'Three genuine PUBLICs only; no aliases')
    require(not obj.procedures,'No fabricated procedure metadata')
    require([k for k,_,_ in obj.records]==[0x80,0x96,0x98,0x98,0x9a,0x8c,0x90,0x88,0xa0,0x9c,0xa0,0x9c,0x8a],'Closed records; no COMMON/LIDATA/debug/extraallocation')
    for kind,expected in [(0x80,[b'\x08UNIT.ASM']),(0x9a,[b'\x02\xff\x01']),(0x88,[b'\x00\xa2\x01']),(0x8a,[b'\x00'])]:require([p for k,_,p in obj.records if k==kind]==expected,'Closed THEADR/DGROUP/directive/entry records')
    raw=bytearray()
    for off,chunk in sorted(seg.chunks):
        require(chunk and off==len(raw) and off+len(chunk)<=SIZE,'CODE hole/overlap/excess');raw.extend(chunk)
    require(len(raw)==SIZE,'Omitted CODE tail')
    shape=[(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.raw.hex(),f.record_offset)for f in obj.fixups]
    require(shape==adapter.FIELD_PROFILE,'Exact84 authentic fields/frames/targets/rawrecords')
    require(digest(raw)==RAW_SHA256,'Unlinked instructions/addends changed')
    require(raw[:12]==bytes(12)and raw[778:781]==bytes.fromhex('eb5890'),'Consumed scratch/natural relaxation lost')
    return bytes(raw),{'boundary':'complete_dependency_closed_CODE_SEGDEF','segment':{'index':2,'name':'_TEXT','class_name':'CODE','attributes':72,'length':SIZE},'empty_data_segment':{'index':1,'name':'_DATA','length':0},'group':{'index':1,'name':'DGROUP','segments':[1]},'publics':[asdict(p)for p in sorted(obj.publics.values(),key=lambda p:p.offset)],'internal_components':[{'kind':'preceding_blitter_allocation','offset':0,'size':873,'ordinary_REA_live':134,'ordinary_REA_span':593,'conditional_CFG_live':592,'raw_NOP':1},{'kind':'functional_nibble_translation_table','offset':873,'size':256},{'kind':'ordinary_complete_prepare_native','offset':1129,'size':74},{'kind':'ordinary_complete_drawtext_native','offset':1203,'size':285}],'actual_fixup_count':84,'field_classes':{'ownCODE_OFFSET16':52,'ownCODE_self_relative16':7,'external_OFFSET16':21,'external_BASE16':1,'external_FAR16':3},'raw_sha256':digest(raw),'authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'CODE_contributions':1}

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
    with tempfile.TemporaryDirectory(prefix='graphics-masm-')as tmp:
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
    adapter.validate_object(data)
    raw,metadata=extract_code(read_omf(data))
    return Build(data,raw,metadata,{'source_sha256':digest(content),'assembler_sha256':MASM_SHA256,'assembler_manifest_sha256':MANIFEST_SHA256,'assembler_license_sha256':LICENSE_SHA256,'assembler_configuration_sha256':CONFIG_SHA256,'compiler':'Microsoft Macro Assembler5.10','build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':digest(data),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','dosbox_configuration':conf,'batch_source':batch,'dosbox_stdout':r.stdout.decode('utf-8','replace'),'dosbox_stderr':r.stderr.decode('utf-8','replace'),'generation_target_input':False,'generation_original_placement_input':False})


def _subject(e,sha,operation):
    prefix._subject(e,sha,operation)

def _complete(e,address,size,blocks=None):
    _subject(e,ORIGINAL_SHA256,'analyze_function')
    r=e['normalized_result'];p=r['procedure'];b=p['body'];start=hex(address)
    require(e['parameters']=={'procedure':start}and p['address']==start and not p['classification']['external']and not p['classification']['thunk'],'Exact native procedure entry/parameters')
    require(b.get('available')is True and b.get('contains_entry')is True and b.get('non_contiguous')is False and b['ranges']==[{'start':start,'end':hex(address+size-1)}]and b['total_bytes']==b['span_bytes']==size,'Exact complete native boundary required')
    if blocks is not None:
        require(r['basic_blocks']==blocks,'Exact complete native CFG required')
        owned=set();starts={q['start']for q in blocks}
        for q in blocks:
            a,z=int(q['start'],0),int(q['end'],0);s=set(range(a,z))
            require(a<z and address<=a<z<=address+size and not(owned&s)and set(q['successors'])<=starts,'Native CFG partition/closure');owned|=s
        require(owned==set(range(address,address+size)),'Native CFG must own every procedure byte')

def _evidence(project):
    project=Path(project).resolve()
    require(Path(adapter.__file__).resolve()==(project/'graphics1488_dgroup_link16.py').resolve()and Path(prefix.__file__).resolve()==(project/'blit_code16.py').resolve(),'Actual local dependency module paths required')
    records={}
    for rel,pin in EVIDENCE_PINS.items():
        p=(project/rel).resolve();require(p.is_relative_to(project),'Evidence outside project');content=p.read_bytes();require(digest(content)==pin,'Native/dependency evidence pin mismatch: '+rel)
        if rel.endswith('.json'):records[rel]=json.loads(content)
    api=records[API_EVIDENCE];decls=[d for a in api['source_AST_declarations']for d in a['declarations']if d['name']in('prepare_pixels_e8cb','draw_text_e915')]
    require({d['name']for d in decls}=={'prepare_pixels_e8cb','draw_text_e915'},'New near API declarations missing')
    for d in decls:
        expected='void (char *, int, int)'if d['name']=='prepare_pixels_e8cb'else'void (Text *, int, int)'
        require(d['expanded_type']==expected and d['function_far']is False and (d['name']!='prepare_pixels_e8cb'or d['original_qualifiers']==['huge']),'New near API type/huge-pointer declaration mismatch')
    expected=dict(BINDINGS,_prepare_pixels_e8cb=0xe8cb,_draw_text_e915=0xe915)
    def same_binding(n,v):
        target=expected[n]
        # Existing C near-DGROUP maps use offsets; ASM explicit frame maps include DS.
        if type(v)is int and isinstance(target,dict)and target['segment']==0x5cc2:return v==target['offset']
        return v==target
    require(all(same_binding(n,v)for row in api['actual_current_external_bindings']for n,v in row['bindings'].items()),'New native caller binding identity mismatch')
    views=api['new_external_views'];require(set(views)=={'_text_colour_words','_text_glyph_pixels','_text_cursor','_font_glyphs'},'Exact symbolic storage views required')
    for name,off,size in[('_text_colour_words','44E0',32),('_text_glyph_pixels','4500',32),('_text_cursor','4520',4),('_font_glyphs','4524',None)]:
        view=views[name];keys={'DS_offset','source_allocated','interpretation'}|({'native_consumed_bytes'}if size is not None else set())
        require(set(view)==keys and view['DS_offset']==off and view['source_allocated']is False and (size is None or view['native_consumed_bytes']==size),'No invented storage allocation/font capacity; exact consumed views only')
    old,old_id=prefix._evidence(project)
    e=records[RAW_EVIDENCE];_subject(e,ORIGINAL_SHA256,'read_bytes');r=e['normalized_result']
    require(e['parameters']=={'address':'0x1e7cb','length':656}and r.get('address')=='0x1e7cb'and r.get('complete')is True and r['requested_bytes']==r['returned_bytes']==656,'Complete656 original context required')
    following=bytes.fromhex(r['bytes_hex']);require(len(following)==656 and old[873:900]==following[:27],'Overlapping primary bytes mismatch')
    require(digest(following[615:])==NEXT_RAW_SHA256,'Exact original next41 bytes required')
    prep,draw,nxt=(records[p]for p in[PREPARE_EVIDENCE,DRAW_EVIDENCE,NEXT_EVIDENCE])
    _complete(prep,0x1e8cb,74,PREPARE_BLOCKS);_complete(draw,0x1e915,285,DRAW_BLOCKS);_complete(nxt,0x1ea32,41)
    ids=[e['evidence_id'],prep['evidence_id'],draw['evidence_id'],nxt['evidence_id'],old_id]
    for rel in[prefix.NATIVE_EVIDENCE,prefix.CALL_EVIDENCE]:ids.append(json.loads((project/rel).read_text())['evidence_id'])
    require(len(set(ids))==7,'Distinct native evidence identities required')
    remap=lambda n:4 if n==1 else 12 if n==9 else n
    table=bytes((remap(v>>4)<<4)|remap(v&15)for v in range(256))
    require(following[:256]==table,'Functional byte-domain colour table mismatch')
    native=old[:873]+following[:615];require(len(native)==SIZE,'Whole native1488 span')
    require(native[1134:1137]==bytes.fromhex('b80d12')and native[1203:1208]==bytes.fromhex('9a1e00ef11')and native[1354:1359]==bytes.fromhex('9a0000ef11')and native[1472:1477]==bytes.fromhex('9a00000d11'),'Raw external SEG/FAR identity required; do not use provider far-resolution aliases')
    return native,ids

def _sites(sites):
    overlapping=sorted(s for s in sites if s<BASE+SIZE and s+2>BASE)
    require(overlapping==MZ_SITES and all(BASE<=s and s+2<=BASE+SIZE for s in overlapping),'Exact four MZ sites; crossing/missing/extra word forbidden')
    return overlapping

def validate_evidence(unit,project,target_sha256,reference=None):
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    raw,ids=_evidence(project)
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Pinned expanded context required')
    require(reference['image'][BASE:BASE+SIZE]==raw,'Complete primary/reference1488 mismatch')
    require(digest(reference['image'][BASE+SIZE:BASE+SIZE+41])==NEXT_RAW_SHA256,'Complete next41 reference mismatch');_sites(reference['relocations'])
    return ids[0]

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj)
    require(raw==built.code and metadata==built.metadata,'Build differs from complete object')
    ex={k:(v['segment'],v['offset'])for k,v in BINDINGS.items()}
    linked,logs=adapter.link(built.object_bytes,{1:(0x5cc2,0),2:(0,BASE)},{1:0x5cc2},ex)
    primary,ids=_evidence(project);sites=_sites(original_sites)
    require(len(linked)==SIZE and linked==primary==image[BASE:BASE+SIZE],'Complete1488 native/source mismatch; no partial credit')
    emitted=sorted(f['mz_relocation_image_offset']for f in logs if f['mz_relocation_image_offset']is not None)
    require(len(logs)==84 and emitted==sites,'All84 fields/fourMZ required')
    loads=[]
    for load in(0,1,0x1000,0xffff):
        b,l=adapter.link(built.object_bytes,{1:((0x5cc2+load)&65535,0),2:(load,BASE)},{1:(0x5cc2+load)&65535},{k:((v[0]+load)&65535,v[1])for k,v in ex.items()})
        expected=bytearray(primary)
        for s in sites:
            at=s-BASE;expected[at:at+2]=((int.from_bytes(expected[at:at+2],'little')+load)&65535).to_bytes(2,'little')
        actual=sorted(f['mz_relocation_image_offset']-load*16 for f in l if f['mz_relocation_image_offset']is not None)
        require(b==bytes(expected)and len(l)==84 and actual==sites,'Full forward loader/all84 field arithmetic mismatch')
        loads.append({'load_paragraph':load,'all1488bytes_exact':True,'original_mz':sites,'emitted_mz':actual,'linked_sha256':digest(b)})
    # Canonical reporter treats presence of mz_segment... as an actual site.
    # Keep every authentic field and preserve the raw adapter logs separately.
    report_logs=[{k:v for k,v in f.items()if k!='mz_segment_relocation_image_offset'or v is not None}for f in logs]
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':True,'whole_original_mz_sites':sites,'emitted_mz_sites':emitted,'relocations':report_logs,'raw_adapter_field_logs':logs,'four_load_bases':loads,'native_evidence_ids':ids,'evidence_sha256':EVIDENCE_PINS,'native_boundary_limit':'blitterordinary134/span593/privateconditional592+naturalNOP1/75nativecases retained; prepare74 and draw285 complete native bodies; table256 wholly consumed CS:XLAT domain','function_partition_claim':False,'DATA_byte_credit':0,'authored_c_function_credit':0,'authored_asm_function_credit':0,'historical_module_or_MAP_claim':False,'actual_source_allocation_replaces':'blit_e57a_code873; never admit both','following_odd_table_alignment_resolved_by_actual_whole1488':True,'remaining_storage':['font capacity/owner unknown','colourwords/glyphpixels/cursor owner unknown','far colorbuffer/dynamicgraphics real providers unresolved'],'font_or_scratch_backing_supplied':False}
