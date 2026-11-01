"""Closed authored animation1083 ASM component; C credit and historic attribution0."""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,subprocess,tempfile,os,re
from omf import OMFObject,OMFError,read_omf
from reference import ORIGINAL_SHA256,CARRIER_SHA256
from animation_init_6cb4_profile import SOURCE_SHA256,OBJECT_SHA256,RAW_CODE_SHA256,EXTERNALS,BINDINGS,RECORD_PINS,FIELD_PROFILE,EVIDENCE_PINS,NATIVE_MZ,SOURCE_TO_NATIVE_ROWS
BACKEND='masm510-animation-init-code-omf'
SOURCE='asm/link/init_animation_6cb4.asm'
BASE=0x6cb4
SIZE=1083
RAW_EVIDENCE='evidence/rea_animation_6cb4_instructions.json'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
class AnimationError(OMFError):pass
def need(v,s):
 if not v:raise AnimationError(s)
def validate_unit(u):
 need(set(u)=={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','reference_region','boundary_evidence'},'Exact animation metadata keys')
 need((u['id'],u['language'],u['backend'],u['object_profile'])==('init_animation_code1083','asm-code',BACKEND,'animation_init_395instructions_1083'),'Closed animation profile')
 need(u['source']==SOURCE and u['source_sha256']==SOURCE_SHA256 and u['assembler_sha256']==TOOL_PINS['toolchains/msc510/MASM.EXE'],'Exact source/assembler')
 need(u['public_symbols']==['_init_animation']and u['image_offset']==hex(BASE)and type(u['size'])is int and u['size']==SIZE and u['externals']==BINDINGS,'Whole1083/onePUBLIC/actual symbolic placements')
 need(u['rea_evidence']==RAW_EVIDENCE and u['reference_region']=='unchanged-prefix'and isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence'].strip()),'Exact native evidence/boundary')
def source_policy(content):
 need(type(content)is bytes and H(content)==SOURCE_SHA256,'Exact animation source bytes')
 try:text=content.decode('ascii')
 except UnicodeDecodeError:raise AnimationError('ASCII source required')
 live='\n'.join(s.split(';',1)[0]for s in text.splitlines());need(not re.search(r'\b(DB|DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC)\b',live,re.I),'No opcode data/padding/generation directives')
 need(len([s for s in text.splitlines()if s.startswith('    ')and'; native'in s])==395 and 'sar di,1 ; native 6ECE'in text,'395source instructions/realD1FF shift')
def validate_object(o):
 need(isinstance(o,OMFObject)and set(o.segments)=={1,2}and not o.procedures,'Exactly emptyDATA and CODE; no debug procedure')
 ds,cs=o.segments[1],o.segments[2]
 need((ds.name,ds.class_name,ds.length,ds.attributes,ds.unsupported_data,ds.chunks)==('_DATA','DATA',0,72,False,[]),'Exact empty WORD/PUBLIC DATA metadata')
 need((cs.name,cs.class_name,cs.length,cs.attributes,cs.unsupported_data)==('_TEXT','CODE',1083,72,False),'Whole WORD/PUBLIC CODE1083')
 need(o.names==['','','DGROUP','DATA','CODE','_DATA','_TEXT']and o.externals==EXTERNALS,'Exact names/25real externals')
 need(set(o.publics)=={'_init_animation'}and asdict(o.publics['_init_animation'])=={'name':'_init_animation','segment':2,'offset':0,'group':0,'type_index':0},'Exactly one nearCODE PUBLIC')
 need([(k,at,H(b))for k,at,b in o.records]==RECORD_PINS,'Every raw record payload/boundary accounted')
 raw=bytearray()
 for at,data in cs.chunks:need(at==len(raw)and bool(data)and at+len(data)<=SIZE,'CODE hole/overlap/tail');raw.extend(data)
 need(len(raw)==SIZE and H(raw)==RAW_CODE_SHA256,'Whole literal instruction/addend allocation')
 fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups];need(fields==FIELD_PROFILE and len(fields)==39,'Exact39 actual typed fields including internal jump')
 return bytes(raw),{'boundary':'whole_CODE1083_plus_empty_DATA','CODE_segment':{'index':2,'name':'_TEXT','class':'CODE','length':1083,'attributes':72},'DATA_segment':{'index':1,'name':'_DATA','length':0,'attributes':72},'publics':[asdict(o.publics['_init_animation'])],'actual_external_fields':38,'actual_internal_fields':1,'actual_fields':39,'source_instructions':395,'native_MZ':NATIVE_MZ,'C_credit':0,'authored_asm_function_credit':0,'initialized_DATA_credit':0,'WORD_neighbor_join_held':True,'historical_TU_patch_attribution_proven':False}
def extract_code(raw):
 o=read_omf(raw);code,meta=validate_object(o);need(H(raw)==OBJECT_SHA256,'Exact unchanged actual whole source object');return code,meta
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 code:bytes
 metadata:dict
 provenance:dict
def _assemble_source(source,project):
 source=Path(source);content=source.read_bytes();source_policy(content)
 tools={name:(project/name).read_bytes()for name in TOOL_PINS}
 for name,b in tools.items():need(H(b)==TOOL_PINS[name],'Pinned source-generation tool '+name)
 need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 with tempfile.TemporaryDirectory(prefix='bc-animation-init-')as scratch:
  p=Path(scratch);t=p/'tools';t.mkdir();(t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
  batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
  conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
  result=subprocess.run(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45,check=False)
  log=(p/'MASM.LOG').read_bytes().decode('cp437');need(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and '5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM assembly errors: '+log)
  raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437')
 for name,h in TOOL_PINS.items():need(H((project/name).read_bytes())==h,'Tool changed during generation')
 need(source.read_bytes()==content,'Source changed during generation')
 return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'source_instruction_count':395,'authored_asm_function_credit':0,'WORD_neighbor_join_held':True,'original_absolute_placement_proven':False}
def assemble(source,project):
 project=Path(project).resolve();source=Path(source).resolve()
 need(source==(project/SOURCE).resolve()and source.is_relative_to(project)and not(project/SOURCE).is_symlink(),'Exact regular standalone source path')
 raw,provenance=_assemble_source(source,project);code,meta=extract_code(raw)
 return Build(raw,code,meta,provenance)
def link_code(raw,load=0):
 initial,meta=extract_code(raw);o=read_omf(raw);need(type(load)is int and 0<=load<=65535,'16bit load paragraph');view=bytearray(initial);logs=[]
 for f in sorted(o.fixups,key=lambda f:f.offset):
  addend=int.from_bytes(initial[f.offset:f.offset+2],'little');disp=f.displacement or 0;name=None;native_site=BASE+f.offset
  if f.target==(0,2):
   need(f.offset==939 and f.frame==(0,2)and not f.segment_relative and disp==69 and addend==0,'Exact internal SELFREL16');value=addend+disp-f.offset-2;mode='self_relative_internal_CODE'
  else:
   name=o.externals[f.target[1]];target=BINDINGS[name]
   if not f.segment_relative:value=target+addend+disp-native_site-2;mode='self_relative_external_CODE'
   elif f.location_type==2:value=((target['segment']+load)&65535)+addend+disp;mode='segment_base16'
   else:value=(target['offset']if isinstance(target,dict)else target)+addend+disp;mode='far_offset16'if isinstance(target,dict)else'segment_relative_DGROUP'
  value&=65535;view[f.offset:f.offset+2]=value.to_bytes(2,'little');log={'segment':2,'object_offset':f.offset,'image_offset':native_site,'width':2,'mode':mode,'target_symbol':name,'frame':list(f.frame),'target':list(f.target),'raw_fixupp':f.raw.hex(),'source_addend':addend,'target_displacement':disp,'encoded_hex':value.to_bytes(2,'little').hex()}
  if f.location_type==2:log['mz_segment_relocation_image_offset']=native_site
  logs.append(log)
 return bytes(view),logs

def _evidence(project):
 out={}
 for name,h in EVIDENCE_PINS.items():
  raw=(Path(project)/name).read_bytes();need(H(raw)==h,'Animation evidence pin '+name);out[name]=json.loads(raw)if name.endswith('.json')else raw.decode()
 instructions=out[RAW_EVIDENCE];info=out['evidence/rea_animation_6cb4_info.json'];patch=out['evidence/rea_animation_6cb4_patch_tail.json']
 for e,op in[(instructions,'read_function_instructions'),(info,'procedure_info'),(patch,'read_bytes')]:need(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['operation']==op and e['provider']['id']=='ghidra','Exact original REA identity/operation')
 body=instructions['normalized_result']['procedure']['body'];need(body['ranges']==[{'start':'0x16cb4','end':'0x17088'},{'start':'0x1708d','end':'0x170ee'}]and body['span_bytes']==1083 and body['total_bytes']==1079 and len(instructions['normalized_result']['instructions'])==393,'Original live393/body1079 excludes exact dead4')
 need(info['normalized_result']['entrypoint']=='0x16cb4'and info['normalized_result']['body']==body,'Info/live-body boundary identity')
 need(patch['parameters']=={'address':'0x17077','length':35}and patch['normalized_result']['complete']and patch['normalized_result']['returned_bytes']==35,'Complete patch-tail35')
 full=out['build/animation-6cb4-required-ASM-review/review.json'];need(full['instruction_count']==395 and full['planned_external_operand_fields']==38 and full['native_MZ_sites']==NATIVE_MZ,'Full native395 instruction and operand proof')
 qualification=out['build/animation-6cb4-mnemonic-root-review/corrected-comparison-qualification.json'];need(qualification['actual_external_fields']==38 and qualification['actual_internal_fields']==1 and qualification['raw_object_unchanged']and not qualification['assembler_rerun']and qualification['actual_native_MZ_sorted']==NATIVE_MZ,'Retained list-order-only comparison qualification')
 positive=out['build/animation-6cb4-corrected-frame-root-actual/whole-object-comparison.json'];need(positive['raw_object_sha256']==OBJECT_SHA256 and positive['complete_CODE_bytes']==1083 and positive['actual_external_fields']==38 and positive['actual_internal_fields']==1,'Actual corrected whole-object positive')
 process=out['build/animation-6cb4-corrected-frame-root-actual/process-receipt.json'];tool=out['build/animation-6cb4-corrected-frame-root-actual/actual-root-tool-result.json'];need(process['status']=='COMPLETE'and process['guard_closed']and process['source_sha256']==SOURCE_SHA256 and process['raw_object_sha256']==OBJECT_SHA256 and process['assembler_calls']==1,'Source-only actual producer receipt')
 need(tool['exit_code']==0 and tool['terminal']and tool['reaped']and tool['assembler_calls']==1,'Actual producer terminal/reaped receipt')
 return out

def _sites(original_sites):
 selected=[p for p in original_sites if BASE<=p<BASE+SIZE or BASE<p+2<=BASE+SIZE];need(sorted(selected)==NATIVE_MZ and len(set(selected))==3,'Exact complete3nativeMZ, order-independent without dropping duplicates');return sorted(selected)
def validate_evidence(u,project,target_sha256,reference=None):
 validate_unit(u);need(target_sha256==ORIGINAL_SHA256 and reference is not None and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']>=BASE+SIZE,'Whole original unchanged prefix/carrier identity');_sites(reference['relocations']);out=_evidence(project)
 full=out['build/animation-6cb4-required-ASM-review/review.json'];native=reference['image'][BASE:BASE+SIZE];need(H(native)==full['native_sha256'],'Complete original native1083 hash');patch=out['evidence/rea_animation_6cb4_patch_tail.json'];need(bytes.fromhex(patch['normalized_result']['bytes_hex'])==reference['image'][0x7077:0x7077+35],'Real NOP/dead-JMP original raw tail')
 return out[RAW_EVIDENCE]['evidence_id']
def validate_comparison(u,built,image,project,original_sites):
 validate_unit(u);code,meta=extract_code(built.object_bytes);need(code==built.code and meta==built.metadata,'Actual whole generated object identity');out=_evidence(project);sites=_sites(original_sites);linked,logs=link_code(built.object_bytes);need(linked==image[BASE:BASE+SIZE]and H(linked)==out['build/animation-6cb4-required-ASM-review/review.json']['native_sha256'],'Every original1083 instruction byte matches full native identity')
 need(sorted(x['mz_segment_relocation_image_offset']for x in logs if'mz_segment_relocation_image_offset'in x)==sites,'Every actual emitted/native MZ site')
 loads=[]
 for base in[0,1,4096,65535]:
  actual,_=link_code(built.object_bytes,base);expected=bytearray(image[BASE:BASE+SIZE])
  for site in sites:
   at=site-BASE;expected[at:at+2]=((int.from_bytes(expected[at:at+2],'little')+base)&65535).to_bytes(2,'little')
  need(actual==expected,'Complete1083 four-base loader comparison');loads.append({'load_paragraph':base,'all1083_native_equal':True,'native_MZ_sites':sites})
 return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':H(linked),'whole_bytes_equal':True,'whole_original_mz_sites':sites,'emitted_mz_sites':sites,'relocations':logs,'four_load_bases':loads,'native_evidence_id':out[RAW_EVIDENCE]['evidence_id'],'source_instructions':395,'actual_external_fields':38,'actual_internal_fields':1,'classification':'authored_required_animation_CODE_component','authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'WORD_neighbor_join_held':True,'historical_patch_TU_alignment_proven':False,'original_absolute_placement_proven':False}
