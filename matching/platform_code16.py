"""Closed complete platform hardware659 ASM CODE contribution.

Nine native procedure observations, two raw interrupt bodies and one live CS
byte share this whole allocation. No ordinary function or initializedDATA credit.
Generation accepts only authored source and pinned tools, never target bytes.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,os,re,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError
class PlatformCodeError(OMFError): pass
def require(condition,message):
    if not condition: raise PlatformCodeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
BACKEND='masm510-platform-code-contribution-omf'
SOURCE='asm/link/platform_hardware_omf.asm'
BASE=0x10e30
SIZE=659
FRAME=0x10e3
MASM_SHA256='1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f'
MANIFEST_SHA256='f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4'
CONFIG_SHA256='058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'
LICENSE_SHA256='b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
RAW_EVIDENCE='build/platform-code-10e30/rea-whole660.json'
PUBLICS={'_play_audio_10e3':0,'_initialize_renderer':130,'_play_audio_alt_10e3':241,'_initialize_video':482,'_restore_input_11066':566,'_select_asset_drive':596}
BINDINGS={n:{'segment':0x5cc2,'offset':a}for n,a in {'_speed_2eb3':0x2eb3,'_audio_calibration_ticks_2eae':0x2eae,'_saved_timer_vector_2eaf':0x2eaf,'_saved_critical_vector_2eb5':0x2eb5,'_saved_pic_mask_2eb9':0x2eb9,'_mode_11aa':0x11aa,'_palette_mode':0x11ab}.items()}
SOURCE_SHA256='f9715345307762a7ce357e3cec631433363d209831bf1a4e078df7b057d2d022'
OBJECT_SHA256='73892dbe3853dbf91824fd06678fc55adc0c292313e5bbb2608a6709c39ab230'
RAW_SHA256='b2ba9f9e50262c89c0756050412a869511a490fea133ed357cfd60f5c5f911b7'
FIELD_PROFILE=[[2, 13, 2, 1, True, [1, 1], [2, 6], None, 'c40d160106', 1049], [2, 66, 2, 1, True, [1, 1], [2, 3], None, 'c442160103', 1049], [2, 122, 2, 1, True, [1, 1], [2, 3], None, 'c47a160103', 1049], [2, 137, 2, 1, True, [1, 1], [2, 7], None, 'c489160107', 1049], [2, 147, 2, 1, True, [1, 1], [2, 1], None, 'c493160101', 1049], [2, 151, 2, 1, True, [1, 1], [2, 1], 2, 'c4971201010200', 1049], [2, 159, 2, 1, True, [0, 2], [0, 2], 348, 'c49f0002025c01', 1049], [2, 173, 2, 1, True, [1, 1], [2, 7], None, 'c4ad160107', 1049], [2, 211, 2, 1, True, [1, 1], [2, 7], None, 'c4d3160107', 1049], [2, 218, 2, 1, True, [1, 1], [2, 6], None, 'c4da160106', 1049], [2, 223, 2, 1, True, [1, 1], [2, 1], 2, 'c4df1201010200', 1049], [2, 227, 2, 1, True, [1, 1], [2, 1], None, 'c4e3160101', 1049], [2, 254, 2, 1, True, [1, 1], [2, 6], None, 'c4fe160106', 1049], [2, 306, 2, 1, True, [1, 1], [2, 3], None, 'c532160103', 1049], [2, 340, 2, 1, True, [1, 1], [2, 3], None, 'c554160103', 1049], [2, 353, 2, 1, True, [1, 1], [2, 7], None, 'c561160107', 1049], [2, 388, 2, 1, True, [1, 1], [2, 5], None, 'c584160105', 1049], [2, 393, 2, 1, True, [1, 1], [2, 2], None, 'c589160102', 1049], [2, 400, 2, 1, True, [1, 1], [2, 5], None, 'c590160105', 1049], [2, 404, 2, 1, False, [0, 2], [0, 2], 426, '8594000202aa01', 1049], [2, 412, 2, 1, True, [1, 1], [2, 2], None, 'c59c160102', 1049], [2, 418, 2, 1, False, [0, 2], [0, 2], 457, '85a2000202c901', 1049], [2, 421, 2, 1, True, [1, 1], [2, 2], None, 'c5a5160102', 1049], [2, 494, 4, 3, True, [0, 2], [0, 2], 359, 'cdee0002026701', 1049], [2, 503, 2, 1, True, [1, 1], [2, 2], None, 'c5f7160102', 1049], [2, 513, 2, 1, True, [1, 1], [2, 2], None, 'c601160102', 1049], [2, 523, 2, 1, True, [1, 1], [2, 2], None, 'c60b160102', 1049], [2, 540, 2, 1, True, [1, 1], [2, 4], None, 'c61c160104', 1049], [2, 544, 2, 1, True, [1, 1], [2, 4], 2, 'c6201201040200', 1049], [2, 551, 2, 1, True, [0, 2], [0, 2], 479, 'c627000202df01', 1049], [2, 579, 2, 1, True, [1, 1], [2, 4], None, 'c643160104', 1049], [2, 583, 2, 1, True, [1, 1], [2, 4], 2, 'c6471201040200', 1049], [2, 606, 2, 1, True, [0, 2], [0, 2], 595, 'c65e0002025302', 1049], [2, 612, 2, 1, True, [0, 2], [0, 2], 595, 'c6640002025302', 1049], [2, 620, 2, 1, True, [0, 2], [0, 2], 595, 'c66c0002025302', 1049]]
RECORD_PAYLOAD_HASHES=[[128, 0, '4fb390538337b2d69ad7c1ab5d347ae0af0bf4d3e411c89a4431eb22e98a8fd8'], [150, 13, '643d4a10e6f982119f2ec9c513e7f0b5e71e64dd04bdecf235d6bc21ae99f8bd'], [152, 55, 'c3ac26c0bd61c0094f0bee15e3788e631d8e55fb5f45d6abfa34341507d44b4b'], [152, 65, '90c35e8e018247ea6745747cb46d771fc47d0f4dff110d268a6ea86ae63e1f05'], [154, 75, '7270bf5afdbd1cef0dc73aa616704df89a65b3917892b04b6f0bb18fc2156f41'], [140, 82, 'f2edf36513bc4d3b09afb45f5ef7839656b0f9415439d5c27e8256a810078491'], [144, 234, '8187b720a1fb4f12ab6823ae25371b524d77515f50b475a6c06fe38167c69f3d'], [136, 376, 'fd47f9fd11ee91a44ab31c40b4a2771341d5ba747d2b0f2954d92d6ea2137a48'], [160, 383, 'bd2838ac9e557004fabf69bd9b64af280b5b41a439cf9035a6d5d2e2f576e18e'], [156, 1049, 'ae14326fa07486a0984da0202383699aabeac9e1b189abc5b9dd5d6d4216b8da'], [138, 1252, '6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d']]
PARTS=[['rea-sound-entry.json', 0, 130], ['rea-renderer-entry.json', 130, 111], ['rea-alt-sound-entry.json', 241, 107], ['rea-timer-handler11.json', 348, 11], ['rea-video-detect.json', 359, 67], ['rea-vga-detect.json', 426, 31], ['rea-ega-detect.json', 457, 22], ['rea-critical-handler3.json', 479, 3], ['rea-video-init.json', 482, 84], ['rea-video-restore.json', 566, 29], ['rea-drive-attempt-byte1.json', 595, 1], ['rea-drive-probe.json', 596, 63]]
EVIDENCE_PINS={'build/platform-code-10e30/rea-sound-entry.json': 'aba1075fdaabba5d4dec0bccd93360d70a8e2b4237a297e0ad9c7388c91731da', 'build/platform-code-10e30/rea-renderer-entry.json': 'd946ef6bf5511bcfc1b9ccad5363f7a0a46c46b56e585eb76940012b81b82187', 'build/platform-code-10e30/rea-alt-sound-entry.json': '09f2b27e7293ea18541a930c4c83ddd02163b800c561849bf8527cdb3fdd9797', 'build/platform-code-10e30/rea-timer-handler11.json': '4fe8ecfee3671fabe16e9881f026875996c10e2b82ef81e8ba9eac72c19f3af1', 'build/platform-code-10e30/rea-video-detect.json': 'b036a706d8da1292dba30437d32aec7aa7ad18e158e00309308a2f0f37fb0abb', 'build/platform-code-10e30/rea-vga-detect.json': 'bafb8a3f80c3ae23f205ae37f153a2c939653c497688bc9b43152b48e1d39d60', 'build/platform-code-10e30/rea-ega-detect.json': '8450589e63969ac7cbda7d87dae94a8741c13312658e36e3249110098679fb5c', 'build/platform-code-10e30/rea-critical-handler3.json': 'e649c61d6a80666632832cce874c93cc4f3bd8eec4dd13d566c1eeda02094eb5', 'build/platform-code-10e30/rea-video-init.json': '657bcce9412206e429bfea5877105cdc9d4bda85f1738e14a25b7118d3b245b4', 'build/platform-code-10e30/rea-video-restore.json': 'c1bbabb7e7af3d5644e1edf4adbea0ca1701a27035699ef4d66ecb04ae028de5', 'build/platform-code-10e30/rea-drive-attempt-byte1.json': '628541a580e557310df241ae2cdf3172ef8013daf46387ca368eb726e9fa5e9c', 'build/platform-code-10e30/rea-drive-probe.json': '12db2b77c02f9089a6fcca80a0acf9896dbce0eb872c150acab3dc89b453e27e', 'build/platform-code-10e30/rea-whole660.json': '974891c6313f6eeeddfdf2173230b902b31ad99dc2806f5516fab88ca46fb290', 'build/platform-code-10e30/rea-timer-handler.json': '3e40a7b010b158bcac6ac1b57d2e44ff914f86e42bfd38e6644fe191dc744f46', 'build/platform-code-10e30/rea-critical-handler.json': '8eec4eaa6ed6c4e4c45072c5613846e505871933a7fadd676cb36349686ed1f4', 'build/platform-code-10e30/root-review.json': '01e908f85ffd34377d6700abc2799482fda19962a044328b15906475de159dae', 'build/platform-code-10e30/guarded-proof.json': 'a0ccee04ca77c09f453bb15578a6facfc4c1cb4884e3094cea931887cc4d5de7', 'build/platform-code-10e30/freeze-reviewed.json': '75df14cee7021dd89911c80194769345d9c031baac1faa3d8feac3770411f110', 'build/future-platform-input-data-LINK-252/actual-LINK.json': '3027d901c0a8f40c630841dc7a8d9effd86a682839e0c3746e8c2ff14b9033a1', 'build/future-platform-input-data-LINK-252/LINK/PARTIAL.EXE': '725d5313a2c9bb23f6b8ec2b27753aeced217e0bb1e0e7705a6586ce80bffbf8', 'build/future-platform-input-data-LINK-252/LINK/PARTIAL.MAP': '8731d598e3b088b46a5d5cdf2eeaa7e7c1b19dba1c6a4352b4e2e66f4e96fc0a'}
PROFILE_PARAMETERS={'target_kind': 'executable', 'target_format': 'dos-mz', 'architecture': 'x86', 'available_architectures': ['x86'], 'import_mode': 'ephemeral-source-immutable', 'annotation_policy': 'atomic-function-entry-metadata-v1', 'load_image_observations': 'source-mappings-entry-context-v2', 'function_body_evidence': 'complete-inclusive-ranges-v1', 'function_references': 'complete-body-and-entry-reference-manager-v2', 'location_resolution': 'explicit-address-exact-entry-symbol-first-v3', 'instruction_flow_evidence': 'decoded-return-pcode-v1', 'process_launch': 'inspected-jvm-launch-support-v1', 'load_image_evidence': 'independent-mz-mapping-relocations-v1', 'jump_table_evidence': 'typed-case-default-blocks-v1', 'decompiler_jump_loads': True, 'loader': 'MzLoader', 'language_id': 'x86:LE:16:Real Mode', 'compiler_spec_id': 'default', 'load_segment': '0x1000', 'address_coordinates': 'linear-byte-offset', 'analyzer_preset': 'ghidra-default'}
EXTERNALS={1: '_saved_timer_vector_2eaf', 2: '_palette_mode', 3: '_saved_pic_mask_2eb9', 4: '_saved_critical_vector_2eb5', 5: '_mode_11aa', 6: '_speed_2eb3', 7: '_audio_calibration_ticks_2eae'}

def validate_unit(u):
    require(set(u)=={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','reference_region','boundary_evidence'},'Exact closed allocation metadata only')
    require(isinstance(u.get('boundary_evidence'),str)and bool(u['boundary_evidence'].strip()),'Explicit complete allocation boundary explanation required')
    require((u.get('id'),u.get('language'),u.get('backend'),u.get('object_profile'),u.get('source'))==('platform_code659','asm-code',BACKEND,'platform_hardware659',SOURCE),'Closed platform659 identity required')
    require(u.get('source_sha256')==SOURCE_SHA256 and u.get('assembler_sha256')==MASM_SHA256,'Pinned source and assembler required')
    require(u.get('public_symbols')==list(PUBLICS) and u.get('image_offset')==hex(BASE) and type(u.get('size'))is int and u['size']==SIZE,'Whole659/sixPUBLICs only')
    require(u.get('externals')==BINDINGS and u.get('rea_evidence')==RAW_EVIDENCE and u.get('reference_region','unchanged-prefix')=='unchanged-prefix','Closed bindings/raw native evidence required')
    require(not any(k in u for k in ('symbol','flags','end_symbol','extended_extent','owned_const','owned_const_profile','owned_data','owned_bss','data_address','code_address','runtime_kind','compiler_source_name')),'No function/ownership/foreign metadata')

def source_policy(content):
    try: text=content.decode('ascii')
    except UnicodeDecodeError: raise PlatformCodeError('ASCII authored source required')
    live=[line.split(';',1)[0].strip().upper() for line in text.splitlines()]
    require(not any(re.search(r'\b(?:DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC)\b',s)for s in live),'No opcodeblob/alignment/generation directives')
    require([s for s in live if re.search(r'\bDB\b',s)]==['DRIVE_ATTEMPTS DB 0'],'Only actually consumed CS retry byte may use DB')

def extract_code(obj):
    require(isinstance(obj,OMFObject) and set(obj.segments)=={1,2},'Only empty DATA and complete CODE')
    data,seg=obj.segments[1],obj.segments[2]
    require((data.name,data.class_name,data.length,data.attributes,data.unsupported_data,data.chunks)==('_DATA','DATA',0,72,False,[]),'Empty DATA0 only')
    require((seg.name,seg.class_name,seg.length,seg.attributes,seg.unsupported_data)==('PLATFORM_TEXT','CODE',SIZE,104,False),'Complete PARA PUBLIC CODE659 required')
    require(obj.names==['','','DGROUP','PLATFORM_TEXT','DATA','CODE','_DATA'],'Exact group/segment names')
    require((data.index,data.name_index,data.class_index,data.overlay_index)==(1,6,4,1)and(seg.index,seg.name_index,seg.class_index,seg.overlay_index)==(2,3,5,1),'Exact SEGDEF identity')
    require(obj.externals==EXTERNALS,'Seven exact EXTDEF names/indices')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'Six actual PUBLICs only')
    require(not obj.procedures,'No fabricated C/debug procedure metadata')
    require([(k,a,digest(p))for k,a,p in obj.records]==[tuple(r)for r in RECORD_PAYLOAD_HASHES],'Whole closed record layout; no debug/COMMON/extra allocations')
    raw=bytearray()
    for at,b in seg.chunks:
        require(bool(b)and at==len(raw)and at+len(b)<=SIZE,'CODE hole/overlap/excess')
        raw.extend(b)
    require(len(raw)==SIZE and digest(raw)==RAW_SHA256 and raw[595]==0,'Complete raw instructions/addends/live scalar')
    fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in obj.fixups]
    require(fields==FIELD_PROFILE,'All35 exact fixup identities/raw records required')
    occupied=set()
    for f in obj.fixups:
        field=set(range(f.offset,f.offset+f.width));require(not occupied.intersection(field)and min(field)>=0 and max(field)<SIZE,'Overlapping/foreign fields');occupied.update(field)
        require(raw[f.offset:f.offset+f.width]==bytes(f.width),'Native source fields must have zero addends')
    return bytes(raw),{'boundary':'complete_multi_entry_CODE_SEGDEF','segment':{'index':2,'name':seg.name,'class_name':seg.class_name,'attributes':104,'length':SIZE},'empty_data_segment':{'index':1,'name':'_DATA','length':0},'group':{'index':1,'name':'DGROUP','segments':[1]},'publics':[asdict(p)for p in obj.publics.values()],'actual_fixup_count':35,'raw_sha256':digest(raw),'ordinary_native_procedure_observations':9,'raw_interrupt_components':[{'offset':348,'size':11},{'offset':479,'size':3}],'live_CS_retry_byte':{'offset':595,'size':1},'authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'CODE_contributions':1,'historical_module_or_PARAGRAPH_attribute_unique':False}

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
    with tempfile.TemporaryDirectory(prefix='platform-masm-')as tmp:
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

def link(obj,segments,groups,externals):
    """Only this closed object's standard DGROUP/own-CODE OMF relocations."""
    raw,_=extract_code(obj)
    require(set(segments)=={1,2}and set(groups)=={1}and set(externals)==set(EXTERNALS.values()),'Exact placement domains required')
    def placement(v):
        require(isinstance(v,(list,tuple))and len(v)==2 and all(type(x)is int and 0<=x<=65535 for x in v),'16bit placement required');return tuple(v)
    ds,empty=placement(segments[1]);cs,offset=placement(segments[2])
    require(type(groups[1])is int and empty==0 and groups[1]==ds and offset+SIZE<=65536,'Whole DATA group/CODE must fit 16bits')
    ex={k:placement(v)for k,v in externals.items()};require(all(v[0]==ds for v in ex.values()),'All near externals must use actual DGROUP frame')
    code=bytearray(raw);logs=[]
    for f in obj.fixups:
        disp=f.displacement or 0;symbol=None;mz=None
        if f.target[0]==2:
            symbol=EXTERNALS[f.target[1]];value=ex[symbol][1]+disp;mode='DGROUP_OFFSET16'
            require(value<=65535,'External near field exceeds group')
            encoded=value.to_bytes(2,'little')
        elif f.width==4:
            require(offset+disp<=65535,'Own far target exceeds segment')
            encoded=(offset+disp).to_bytes(2,'little')+cs.to_bytes(2,'little');mode='own_CODE_FAR16';mz=cs*16+offset+f.offset+2
        elif f.segment_relative:
            require(offset+disp<=65535,'Own near target exceeds segment')
            encoded=(offset+disp).to_bytes(2,'little');mode='own_CODE_OFFSET16'
        else:
            encoded=((disp-(f.offset+f.width))&65535).to_bytes(2,'little');mode='own_CODE_PCREL16'
        code[f.offset:f.offset+f.width]=encoded
        logs.append({'segment':2,'object_offset':f.offset,'image_offset':cs*16+offset+f.offset,'width':f.width,'mode':mode,'frame':list(f.frame),'target':list(f.target),'target_symbol':symbol,'displacement':f.displacement,'encoded_hex':encoded.hex(),**({'mz_segment_relocation_image_offset':mz}if mz is not None else {})})
    return bytes(code),logs

def _subject(e,operation):
    provider={'id':'ghidra','name':'Ghidra','version':'12.1.4'}
    require(e.get('subject',{}).get('digest',{}).get('sha256')==CARRIER_SHA256 and e['subject'].get('format')=='dos-mz' and e['subject'].get('architecture')=='x86','Native subject/format/architecture')
    p=e.get('analysis_profile',{})
    require(e.get('provider')==provider and p.get('provider')==provider and p.get('digest')==PROFILE and p.get('parameters')==PROFILE_PARAMETERS,'Exact Ghidra/loader/profile parameters')
    require(e.get('operation')==operation and re.fullmatch(r'ev_[0-9a-f]{64}',e.get('evidence_id',''))is not None,'Native operation/evidence identity')

def _read(e,address,size):
    _subject(e,'read_bytes');r=e['normalized_result']
    require(e['parameters']=={'address':hex(address),'length':size}and r.get('address')==hex(address)and r.get('complete')is True and r['requested_bytes']==r['returned_bytes']==size,'Exact complete read parameters')
    b=bytes.fromhex(r['bytes_hex']);require(len(b)==size,'Exact read length');return b

def _evidence(project):
    records={}
    for rel,pin in EVIDENCE_PINS.items():
        b=(Path(project)/rel).read_bytes();require(digest(b)==pin,'Pinned primary/corroboration changed: '+rel)
        if rel.endswith('.json'):records[rel]=json.loads(b)
    whole=records[RAW_EVIDENCE];native=_read(whole,0x10000+BASE,660);identities=[whole['evidence_id']]
    end=0
    for filename,offset,size in PARTS:
        require(offset==end,'Closed native partition');end+=size
        e=records['build/platform-code-10e30/'+filename];address=0x10000+BASE+offset
        if offset in (348,479,595):
            b=_read(e,address,size);require(b==native[offset:offset+size],'Raw interrupt/live scalar bytes')
        else:
            _subject(e,'analyze_function');p=e['normalized_result']['procedure'];b=p['body']
            require(e['parameters']=={'procedure':hex(address)}and int(p['address'],0)==address and not p['classification']['external']and not p['classification']['thunk'],'Actual native procedure entry')
            require(b['available']is True and b['contains_entry']is True and b['non_contiguous']is False and b['total_bytes']==b['span_bytes']==size and b['ranges']==[{'start':hex(address),'end':hex(address+size-1)}],'Exact complete native procedure bounds')
        identities.append(e['evidence_id'])
    require(end==SIZE and len(set(identities))==13,'Complete659/13 distinct native IDs')
    require(native[348:359]==bytes.fromhex('50b020fe06ae2ee62058cf')and native[479:482]==bytes.fromhex('b001cf')and native[595]==0,'Raw interrupt and live CS byte semantics')
    for f in ('rea-timer-handler.json','rea-critical-handler.json'):
        e=records['build/platform-code-10e30/'+f]
        require('error'in e and 'normalized_result'not in e,'Provider lack of ordinary interrupt extent retained')
    return native,whole['evidence_id']

def _sites(sites):
    observed=sorted(s for s in sites if s<BASE+SIZE and s+2>BASE)
    require(observed==[0x11020],'One complete native MZ word only; no omitted/crossing relocations');return observed

def _forward(b,sites,load):
    out=bytearray(b)
    for s in sites:
        at=s-BASE;require(0<=at and at+2<=len(out),'Crossing relocation')
        out[at:at+2]=((int.from_bytes(out[at:at+2],'little')+load)&65535).to_bytes(2,'little')
    return bytes(out)

def validate_evidence(unit,project,target_sha256,reference=None):
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong original target')
    require(reference is not None and reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Pinned original/carrier reference required')
    require(BASE+SIZE<=reference['prefix_size'],'Whole659 must be unchanged original prefix')
    native,eid=_evidence(project);sites=_sites(reference['relocations'])
    require(_forward(reference['image'][BASE:BASE+660],sites,0x1000)==native,'Original prefix/forward loader/carrier full660 mismatch')
    return eid

def validate_comparison(unit,built,image,project,original_sites):
    validate_unit(unit);require(digest(built.object_bytes)==OBJECT_SHA256,'Complete output object pin')
    obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj)
    require(raw==built.code and metadata==built.metadata,'Build whole allocation identity')
    native,eid=_evidence(project);sites=_sites(original_sites)
    require(_forward(image[BASE:BASE+660],sites,0x1000)==native,'Native full660 context/raw identity')
    ex={k:(v['segment'],v['offset'])for k,v in BINDINGS.items()}
    linked,logs=link(obj,{1:(0x5cc2,0),2:(FRAME,0)},{1:0x5cc2},ex)
    require([r['mz_segment_relocation_image_offset']for r in logs if 'mz_segment_relocation_image_offset'in r]==sites,'Exact emitted MZ set')
    loads=[]
    for load in (0,1,0x1000,0xffff):
        emitted,fields=link(obj,{1:((0x5cc2+load)&65535,0),2:((FRAME+load)&65535,0)},{1:(0x5cc2+load)&65535},{k:((v[0]+load)&65535,v[1])for k,v in ex.items()})
        require(emitted==_forward(linked,sites,load),'Source relocation/loader arithmetic at four bases')
        loads.append({'load_paragraph':load,'source_loader_arithmetic_exact':True,'all659_native_bytes_equal':emitted==_forward(image[BASE:BASE+SIZE],sites,load)})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':linked==image[BASE:BASE+SIZE],'whole_original_mz_sites':sites,'emitted_mz_sites':sites,'relocations':logs,'four_load_bases':loads,'native_evidence_id':eid,'evidence_sha256':EVIDENCE_PINS,'native_complete_partition':PARTS,'following_zero_byte_not_allocated':True,'provider_interrupt_function_failures_retained':True,'authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'historical_module_or_MAP_claim':False,'full_hardware_execution_proven':False,'actual_LINK_corroboration':'Pinned 197-object partial LINK verifies own8 fields, not whole executable or hardware behavior'}
