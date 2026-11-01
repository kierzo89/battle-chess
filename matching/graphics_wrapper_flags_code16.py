"""Closed genuine graphics wrapper CODE78. No C/function/DATA credit.
First native entry has an explicitly diagnostic COM-decoded CFG, not ordinary
original function metadata. No dynamic driver or zero-gap capacity is allocated.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
from library16 import _word,_placement
class WrapperCodeError(OMFError):pass
def require(value,message):
    if not value:raise WrapperCodeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
BACKEND='masm510-graphics-wrapper-flags-code-omf'
SOURCE='build/input-flags4952-coherent/graphics_wrapper_flags.asm'
BASE=0x11ef0
SIZE=78
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
RAW_EVIDENCE='build/graphics-overlay-ownership/rea-expanded-input-wrappers96.json'
MZ_SITES=[0x11f0b,0x11f1d,0x11f2a,0x11f3b]
PUBLICS={'_graphics_end':0,'_graphics_begin':30,'_update_pointer_11ef_0030':48}
BINDINGS={'_input_flags_4952':{'segment':0x5cc2,'offset':0x4952},'_input_mode_0046':{'segment':0x5cc2,'offset':0x46},'_input_x_005c':{'segment':0x5cc2,'offset':0x5c},'_input_y_005e':{'segment':0x5cc2,'offset':0x5e},'_graphics_pointer_110d_0006':{'segment':0x110d,'offset':6},'_graphics_pointer_110d_0009':{'segment':0x110d,'offset':9}}
SOURCE_SHA256='427ab6e7d0b844700327b7599b1e9f9363c5ba9d93af92e2ae964d9c5bf9de18'
OBJECT_SHA256='99c55ba1bb2133492959a065507fa13067c726421eb373377ecd18bfc6818b05'
RAW_SHA256='b7061eb7ab99a4b88d9102bb5db3848c975d614852572c5717f9db79131b8781'
EXTERNALS={1: '_input_x_005c', 2: '_input_y_005e', 3: '_graphics_pointer_110d_0006', 4: '_graphics_pointer_110d_0009', 5: '_input_mode_0046', 6: '_input_flags_4952'}
FIELD_PROFILE=[(2, 1, 2, 1, True, (1, 1), (2, 6), None, 'c401160106', 380), (2, 6, 2, 1, True, (1, 1), (2, 6), None, 'c406160106', 380), (2, 14, 2, 1, True, (1, 1), (2, 5), None, 'c40e160105', 380), (2, 18, 2, 1, True, (1, 1), (2, 1), None, 'c412160101', 380), (2, 22, 2, 1, True, (1, 1), (2, 2), None, 'c416160102', 380), (2, 25, 4, 3, True, (2, 3), (2, 3), None, 'cc19260303', 380), (2, 31, 2, 1, True, (1, 1), (2, 6), None, 'c41f160106', 380), (2, 36, 2, 1, True, (1, 1), (2, 6), None, 'c424160106', 380), (2, 43, 4, 3, True, (2, 4), (2, 4), None, 'cc2b260404', 380), (2, 50, 2, 1, True, (1, 1), (2, 6), None, 'c432160106', 380), (2, 56, 4, 3, True, (2, 4), (2, 4), None, 'cc38260404', 380), (2, 62, 2, 1, True, (1, 1), (2, 5), None, 'c43e160105', 380), (2, 66, 2, 1, True, (1, 1), (2, 1), None, 'c442160101', 380), (2, 70, 2, 1, True, (1, 1), (2, 2), None, 'c446160102', 380), (2, 73, 4, 3, True, (2, 3), (2, 3), None, 'cc49260303', 380)]
EVIDENCE_PINS={'build/graphics-wrapper78-followup/freeze-manifest.json': 'a8cd4192a671d84f9297227dc970830a965cb1b88ec0d3e1619571516d5afc7c', 'build/graphics-overlay-ownership/rea-expanded-input-wrappers96.json': 'cd8c7bd7090efad1d0583bb4124ca75574669e096c181a2c2b1dfd6264ffddd7', 'build/graphics-overlay-ownership/rea-expanded-pointer-wrapper30.json': 'f5fe3e380086be096500907d5a8e3d91de4e8a1dfee4bd24531e7e5d4ce641ca', 'build/graphics-wrapper78-followup/rea-middle18.json': '0558bfa914a45ebe2bce17145c68ea081fc6a3dce832298aa2c79490b9abfaea', 'build/graphics-wrapper78-followup/rea-first-entry-unrecognized.json': '3a8f46b020c00902c380e179f51cfc7c1d551db00337089b6ce03e11d098ae4b', 'build/graphics-wrapper78-followup/rea-derived-entry30.json': '80bed40f7b8911cd666e1cf0b11e03219d768ec63452c0876e87f8eaa2c29ae1', 'build/graphics-wrapper78-followup/analysis-entry78.COM': '6c57bd9bdb0280e5147db093c30bbec8fe2126c8d6ee8830a10c59df036d27e5', 'build/graphics-wrapper78-followup/instruction-0x21ef0.json': 'e5af7d3ca5604d65b4eac9e47aabf2d133c7492446c50cc7d5cdb46e9f125b88', 'build/graphics-wrapper78-followup/instruction-0x21ef3.json': '58854697d895d77bffa7080d14ef9cdd91ff184931314df1ac7da6c072946b89', 'build/graphics-wrapper78-followup/instruction-0x21ef5.json': '16fbffd8c022900eb42e2490bf6579f9310f22febe16577f5c49529d26090080', 'build/graphics-wrapper78-followup/instruction-0x21ef8.json': '13734462a79e3cc1744d330d1d754533b15f4deebf0e0b51559ed73be1f2fce5', 'build/graphics-wrapper78-followup/instruction-0x21efa.json': '3e23d047ed819fdb712162a5a940dd29552f26e6c858c4250f5ba2e17cfb8eab', 'build/graphics-wrapper78-followup/instruction-0x21efc.json': '7497ffcf86f3eafbd60bc93223e7063942b0b30ee2404524b3046f8d5ec45eab', 'build/graphics-wrapper78-followup/instruction-0x21f00.json': 'e867cb6ddff5a45db50b4361b274676905ba9505c59fcd0d711cde16accf75b0', 'build/graphics-wrapper78-followup/instruction-0x21f04.json': 'bce7a18b1c913de2a41b1f370956961be4a03cddfa93b9c370e86aaad41d0b64', 'build/graphics-wrapper78-followup/instruction-0x21f08.json': 'e68025195f06859af3a573c2cd045451e2ef5c65f42eda56585ae97366f8aeee', 'build/graphics-wrapper78-followup/instruction-0x21f0d.json': '10e8325bd467832c40a404865c21ad99c6da7ff5fcc2c0f2b9dd394ed48b6990', 'build/input-flags4952-coherent/freeze-manifest.json': '97a66a3713ceb8a2570191ca2c2aeb2504de8ebb7882aaa43cbf8f0888849e54', 'build/input-flags4952-coherent/backend-migration-bindings.json': 'afca13f3e4681a9cba6ab4c0920846ab96b0d08dd9eb3925da12d735c0c10fb1', 'build/input-flags4952-coherent/rea-native-flags2.json': '06d7417e69d189a7c5b6afad58aecd4b2c8a657ea600e78520d05f602cc44d84', 'build/input-flags4952-coherent/rea-latch-compare.json': '635796712bdb658fadbbb36481035b2763129855ffcbae2ccf1d6551bed3907d', 'build/input-flags4952-coherent/rea-latch-store.json': 'dfab94485621d2397c6054f1b4cc9a0545340072fcf7f4aaf9fd7677eca577d7'}
RECORD_PAYLOAD_HASHES=[(128, 0, '4fb390538337b2d69ad7c1ab5d347ae0af0bf4d3e411c89a4431eb22e98a8fd8'), (150, 13, '9a7383100ded185ae9ad03129fcbf38b66d88327abe68b54fbe50771bee0899c'), (152, 61, 'c3ac26c0bd61c0094f0bee15e3788e631d8e55fb5f45d6abfa34341507d44b4b'), (152, 71, 'e0d7073c7b7bbe3ebdec7648912bf6d391879abcde16a458a73a2b6b6c8c2761'), (154, 81, '7270bf5afdbd1cef0dc73aa616704df89a65b3917892b04b6f0bb18fc2156f41'), (140, 88, '6bcda55d2be6bf715d658bca8284327502781aace767f1509bcfe0d753e1ceee'), (144, 217, 'a8c1d73d20a244d6f77066a7f8a35e817e1728580a4631aaf74505169827d50b'), (136, 288, 'fd47f9fd11ee91a44ab31c40b4a2771341d5ba747d2b0f2954d92d6ea2137a48'), (160, 295, '4f3f7dd90b5262bf72928722cb4357ebd58fd69afa0e325ae305023b50805ed1'), (156, 380, '5ceec46af4f64c27176589f85007f890a9b73f24f7cf737f2ad2448e1697df86'), (138, 459, '6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d')]
DERIVED_PROFILE='92c4408b0419731bc035df849c2cf5ebf47bbeafb0fb55f68fd7b171d7f49ade'

def validate_unit(unit):
    required={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','boundary_evidence','reference_region'}
    require(type(unit)is dict and set(unit)==required,'Closed wrapper78 metadata keys; no ownership/slice/capacity/alias metadata')
    require((unit['id'],unit['language'],unit['backend'],unit['object_profile'],unit['source'])==('graphics_input_code78','asm-code',BACKEND,'graphics_input78_flags_v1',SOURCE),'Closed wrapper78 profile/source required')
    require(unit['source_sha256']==SOURCE_SHA256 and unit['assembler_sha256']==MASM_SHA256,'Pinned source/MASM required')
    require(unit['public_symbols']==list(PUBLICS)and unit['image_offset']==hex(BASE)and type(unit['size'])is int and unit['size']==SIZE,'Whole78/threePUBLICs required; no slices')
    require(unit['externals']==BINDINGS and unit['rea_evidence']==RAW_EVIDENCE and unit['reference_region']=='exepack-expanded','Closed comparison bindings/evidence required')
    require(type(unit['boundary_evidence'])is str and bool(unit['boundary_evidence'].strip()),'Boundary explanation required')

def extract_code(obj):
    require(isinstance(obj,OMFObject)and set(obj.segments)=={1,2},'Exactly emptyDATA and wholeCODE required')
    data,seg=obj.segments[1],obj.segments[2]
    require((data.name,data.class_name,data.length,data.attributes,data.unsupported_data,data.chunks)==('_DATA','DATA',0,72,False,[]),'Empty DATA0 only; no backing storage')
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.unsupported_data)==('GRAPHICS_INPUT_TEXT','CODE',SIZE,72,False),'Whole WORD CODE78 required')
    require(obj.names==['','','DGROUP','GRAPHICS_INPUT_TEXT','DATA','CODE','_DATA'],'Closed segment/group names')
    require((data.index,data.name_index,data.class_index,data.overlay_index)==(1,6,4,1)and(seg.index,seg.name_index,seg.class_index,seg.overlay_index)==(2,3,5,1),'Closed SEGDEF identities')
    require(obj.externals==EXTERNALS,'Exact six symbolic external names/indices')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'Three real PUBLICs only; no aliases')
    require(not obj.procedures,'No fabricated C procedure metadata')
    require([k for k,_,_ in obj.records]==[0x80,0x96,0x98,0x98,0x9a,0x8c,0x90,0x88,0xa0,0x9c,0x8a],'Closed records; no COMMON/LIDATA/debug/extraallocation')
    for kind,expected in [(0x80,[b'\x08UNIT.ASM']),(0x9a,[b'\x02\xff\x01']),(0x88,[b'\x00\xa2\x01']),(0x8a,[b'\x00'])]:require([p for k,_,p in obj.records if k==kind]==expected,'Closed header/group/directive/entry records')
    raw=bytearray()
    for off,b in sorted(seg.chunks):require(b and off==len(raw)and off+len(b)<=SIZE,'CODE hole/overlap/excess');raw.extend(b)
    require(len(raw)==SIZE,'Omitted CODE tail')
    shape=[(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.raw.hex(),f.record_offset)for f in obj.fixups]
    require(shape==FIELD_PROFILE,'Exact15 authentic field/frame/target/raw records required')
    require(digest(raw)==RAW_SHA256,'Unlinked instructions/addends changed')
    require([(k,a,digest(b))for k,a,b in obj.records]==RECORD_PAYLOAD_HASHES,'Complete authentic record payload hashes required')
    return bytes(raw),{'boundary':'complete_multi_entry_CODE_SEGDEF','segment':{'index':2,'name':seg.name,'class_name':'CODE','attributes':72,'length':SIZE},'empty_data_segment':{'index':1,'name':'_DATA','length':0},'group':{'index':1,'name':'DGROUP','segments':[1]},'publics':[asdict(p)for p in sorted(obj.publics.values(),key=lambda p:p.offset)],'actual_fixup_count':15,'field_classes':{'DGROUP_OFFSET16':11,'external_FAR16':4},'raw_sha256':digest(raw),'first_entry_ordinary_REA_function_claim':False,'first_entry_CFG_source':'explicit unchanged COM diagnostic decode','authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'CODE_contributions':1}
@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def assemble(source,project):
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
    with tempfile.TemporaryDirectory(prefix='wrapper-masm-')as tmp:
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
    require(digest(data)==OBJECT_SHA256,'Complete deterministic graphics wrapper78 OMF changed')
    raw,metadata=extract_code(read_omf(data))
    return Build(data,raw,metadata,{'source_sha256':digest(content),'assembler_sha256':MASM_SHA256,'assembler_manifest_sha256':MANIFEST_SHA256,'assembler_license_sha256':LICENSE_SHA256,'assembler_configuration_sha256':CONFIG_SHA256,'compiler':'Microsoft Macro Assembler5.10','build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':digest(data),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','dosbox_configuration':conf,'batch_source':batch,'dosbox_stdout':r.stdout.decode('utf-8','replace'),'dosbox_stderr':r.stderr.decode('utf-8','replace'),'generation_target_input':False,'generation_original_placement_input':False})


def link(obj,segments,groups,externals):
    """Closed source-object arithmetic only; no reference/target input or reads."""
    raw,meta=extract_code(obj)
    require(set(segments)=={1,2}and set(groups)=={1}and set(externals)==set(EXTERNALS.values()),'Exact complete segment/group/external placements')
    segments={k:_placement(v)for k,v in segments.items()};groups={k:_word(v)for k,v in groups.items()};externals={k:_placement(v)for k,v in externals.items()}
    require(segments[1]==(groups[1],0),'Empty DATA explicit DGROUP frame')
    require(segments[2][1]+SIZE<=65536,'CODE crosses explicit frame')
    require(all(externals[n][0]==groups[1]for n in EXTERNALS.values()if not n.startswith('_graphics_pointer_')),'Near scalar must share explicit DGROUP frame')
    result=bytearray(raw);logs=[]
    for f in obj.fixups:
        target=externals[obj.externals[f.target[1]]];place=segments[2][0]*16+segments[2][1]+f.offset
        addend=int.from_bytes(raw[f.offset:f.offset+f.width],'little');require(addend==0,'Closed zero source addend')
        if f.width==2:
            require(f.location_type==1 and f.segment_relative and f.frame==(1,1)and f.target[0]==2 and f.displacement is None,'DGROUP OFFSET16 exact shape')
            value=target[0]*16+target[1]-groups[1]*16;mode='DGROUP_OFFSET16';mz=None
        else:
            # Same strict external-frame/target FAR16 form corroborated by the
            # separately frozen unrelated two-order authentic LINK controls.
            require(f.width==4 and f.location_type==3 and f.segment_relative and f.frame==f.target and f.target[0]==2 and f.displacement is None,'External FAR16 exact shape')
            value=(target[0]<<16)|target[1];mode='external_FAR16';mz=place+2
        require(0<=value<1<<(8*f.width),'Relocation outside field width')
        encoded=value.to_bytes(f.width,'little');result[f.offset:f.offset+f.width]=encoded
        log={'segment':2,'object_offset':f.offset,'image_offset':place,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'frame':list(f.frame),'target':list(f.target),'target_symbol':obj.externals[f.target[1]],'target_paragraph':target[0],'target_offset':target[1],'frame_paragraph':groups[1]if f.width==2 else target[0],'original_addend':addend,'displacement':0,'mode':mode,'encoded_hex':encoded.hex(),'raw_fixupp':f.raw.hex(),'record_offset':f.record_offset,'mz_relocation_image_offset':mz}
        if mz is not None:log['mz_segment_relocation_image_offset']=mz
        logs.append(log)
    return bytes(result),logs

def _subject(e,sha,operation,profile=PROFILE):
    require(e.get('subject',{}).get('digest',{}).get('sha256')==sha and e.get('operation')==operation,'Native subject/operation mismatch')
    require(e.get('analysis_profile',{}).get('digest')==profile,'Native load/profile mismatch')

def _evidence(project):
    records={};project=Path(project).resolve()
    for rel,pin in EVIDENCE_PINS.items():
        p=(project/rel).resolve();require(p.is_relative_to(project),'Evidence path outside project');b=p.read_bytes();require(digest(b)==pin,'Native evidence pin mismatch: '+rel)
        records[rel]=json.loads(b)if rel.endswith('.json')else b
    e=records[RAW_EVIDENCE];_subject(e,CARRIER_SHA256,'read_bytes');r=e['normalized_result']
    require(e['parameters']=={'address':'0x21ef0','length':96}and r.get('address')=='0x21ef0'and r.get('complete')is True and r['requested_bytes']==r['returned_bytes']==96,'Complete loaded primary96 required')
    loaded=bytes.fromhex(r['bytes_hex']);require(len(loaded)==96,'Loaded primary byte count')
    base='build/graphics-wrapper78-followup/'
    first=records[base+'rea-first-entry-unrecognized.json'];require(first['error']['code']=='invalid_request'and '0x21ef0'in first['error']['details']['issues'][0]['message'],'First native ordinary boundary must remain unrecognized')
    middle=records[base+'rea-middle18.json'];_subject(middle,CARRIER_SHA256,'analyze_function');p=middle['normalized_result']['procedure'];b=p['body']
    require(middle['parameters']=={'procedure':'0x21f0e'}and p['address']=='0x21f0e'and not p['classification']['external']and not p['classification']['thunk']and b=={'available':True,'provenance':'ghidra-function-body-address-set','ranges':[{'start':'0x21f0e','end':'0x21f1f'}],'total_bytes':18,'span_bytes':18,'non_contiguous':False,'contains_entry':True},'Middle native complete18 boundary')
    last=records['build/graphics-overlay-ownership/rea-expanded-pointer-wrapper30.json'];_subject(last,CARRIER_SHA256,'read_function_instructions');p=last['normalized_result']['procedure'];b=p['body']
    require(last['parameters']=={'procedure':'0x21f20'}and p['address']=='0x21f20'and not p['classification']['external']and not p['classification']['thunk']and b=={'available':True,'provenance':'ghidra-function-body-address-set','ranges':[{'start':'0x21f20','end':'0x21f3d'}],'total_bytes':30,'span_bytes':30,'non_contiguous':False,'contains_entry':True},'Last native complete30 boundary')
    derived_bytes=records[base+'analysis-entry78.COM'];require(derived_bytes==loaded[:78],'Diagnostic COM must be unchanged provenance-bound loaded78')
    derived=records[base+'rea-derived-entry30.json'];_subject(derived,digest(derived_bytes),'analyze_function',DERIVED_PROFILE)
    require(derived['parameters']=={'procedure':'0x10100'}and derived['subject']['format']=='dos-com','Explicit COM diagnostic entry required')
    b=derived['normalized_result']['procedure']['body']
    require(b=={'available':True,'provenance':'ghidra-function-body-address-set','ranges':[{'start':'0x10100','end':'0x1011d'}],'total_bytes':30,'span_bytes':30,'non_contiguous':False,'contains_entry':True},'Derived entry exact30 diagnostic boundary')
    require(derived['normalized_result']['assembly']==['0x10100: MOV AL, [0x4952]','0x10103: INC AL','0x10105: MOV [0x4952], AL','0x10108: CMP AL, 0x1','0x1010a: JNZ 0x1000:011d','0x1010c: MOV BX, word ptr [0x46]','0x10110: MOV CX, word ptr [0x5c]','0x10114: MOV DX, word ptr [0x5e]','0x10118: JMPF 0x2000:10d6','0x1011d: RETF'],'Derived diagnostic exact instruction flow')
    require(derived['normalized_result']['basic_blocks']==[{'start':'0x10100','end':'0x1010c','successors':['0x1010c','0x1011d']},{'start':'0x1010c','end':'0x1011d','successors':[]},{'start':'0x1011d','end':'0x1011e','successors':[]}],'Derived diagnostic closed CFG')
    for offset in [0,3,5,8,10,12,16,20,24,29]:
        key=base+'instruction-'+hex(0x21ef0+offset)+'.json';ins=records[key];_subject(ins,CARRIER_SHA256,'inspect_native_instruction');r=ins['normalized_result']
        require(ins['parameters']=={'address':hex(0x21ef0+offset)}and r['address']==hex(0x21ef0+offset),'Exact native instruction query')
        if offset==0:require(r['status']=='not-instruction-boundary'and r['bytes']is None,'Do not erase first-entry native listing defect')
        else:require(r['status']=='decoded'and bytes.fromhex(r['bytes'])==loaded[offset:offset+r['length']],'Original native instruction/raw identity')
    return loaded,[e['evidence_id'],middle['evidence_id'],last['evidence_id'],derived['evidence_id']]

def _sites(sites):
    require(all(type(s)is int for s in sites),'MZ sites require integer coordinates')
    local=sorted(s for s in sites if s<BASE+96 and s+2>BASE)
    require(local==MZ_SITES and all(BASE<=s and s+2<=BASE+SIZE for s in local),'Exact four MZ words; missing/extra/crossing forbidden')
    return local

def _forward(data,sites,load):
    b=bytearray(data)
    for s in sites:
        i=s-BASE;require(0<=i and i+2<=len(b),'MZ crossing read boundary');b[i:i+2]=((int.from_bytes(b[i:i+2],'little')+load)&65535).to_bytes(2,'little')
    return bytes(b)

def validate_evidence(unit,project,target_sha256,reference=None):
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Pinned expanded original context required')
    loaded,ids=_evidence(project);sites=_sites(reference['relocations'])
    require(_forward(reference['image'][BASE:BASE+96],sites,0x1000)==loaded,'Full primary96 forward original-loader comparison')
    return ids[0]

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);obj=read_omf(built.object_bytes);raw,meta=extract_code(obj)
    require(digest(built.object_bytes)==OBJECT_SHA256 and raw==built.code and meta==built.metadata,'Build differs from complete deterministic source object')
    ex={n:(v['segment'],v['offset'])for n,v in BINDINGS.items()};linked,logs=link(obj,{1:(0x5cc2,0),2:(0x11ef,0)},{1:0x5cc2},ex)
    loaded,ids=_evidence(project);sites=_sites(original_sites)
    require(linked==image[BASE:BASE+SIZE]and _forward(image[BASE:BASE+96],sites,0x1000)==loaded,'Whole78/native96 mismatch; no partial credit')
    emitted=sorted(f['mz_segment_relocation_image_offset']for f in logs if 'mz_segment_relocation_image_offset'in f)
    require(len(logs)==15 and emitted==sites,'All15 fields/exact MZ4 required')
    loads=[]
    for load in [0,1,0x1000,0xffff]:
        b,l=link(obj,{1:((0x5cc2+load)&65535,0),2:((0x11ef+load)&65535,0)},{1:(0x5cc2+load)&65535},{n:((v[0]+load)&65535,v[1])for n,v in ex.items()})
        require(b==_forward(linked,sites,load),'Whole78 forward-loader arithmetic')
        require([f['object_offset']+2 for f in l if 'mz_segment_relocation_image_offset'in f]==[s-BASE for s in sites],'Exact relative MZ set at every load')
        loads.append({'load_paragraph':load,'all78bytes_exact':True,'MZ_word_count':4,'linked_sha256':digest(b)})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':True,'whole_original_mz_sites':sites,'emitted_mz_sites':emitted,'relocations':logs,'four_load_bases':loads,'native_evidence_ids':ids,'evidence_sha256':EVIDENCE_PINS,'first_entry_ordinary_REA_function_claim':False,'first_entry_diagnostic_COM_CFG':{'bytes':30,'unchanged_raw_derived_from_primary96':True,'generation_input':False},'native_boundary_limit':'first native listing consumes initial MOV from false21EED; explicit unchanged COM entry decode proves30 CFG; native middle18/last30 retain full boundaries','function_partition_claim':False,'DATA_byte_credit':0,'authored_c_function_credit':0,'authored_asm_function_credit':0,'historical_module_or_MAP_claim':False,'preceding_zero_gap_allocated':False,'dynamic_driver_capacity_proven':False,'remaining_dependencies':list(BINDINGS),'driver_BP_SS_or_full_register_ABI_proven':False,'hardware_execution':False}
