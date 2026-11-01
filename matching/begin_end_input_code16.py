"""Closed authored begin/end input180 ASM component; C credit and historic attribution0."""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,subprocess,tempfile,os,re
from omf import OMFObject,OMFError,read_omf
from reference import ORIGINAL_SHA256,CARRIER_SHA256
from begin_end_input_180_profile import SOURCE_SHA256,OBJECT_SHA256,RAW_CODE_SHA256,EXTERNALS,BINDINGS,RECORD_PINS,FIELD_PROFILE,EVIDENCE_PINS,NATIVE_MZ,SOURCE_TO_NATIVE_ROWS,NATIVE_SHA256,PUBLIC_OFFSETS,UNPROVIDED_SAVED_BYTES
BACKEND='masm510-begin-end-input-code-omf'
SOURCE='asm/link/begin_end_input180.asm'
BASE=0xfb0
SIZE=180
RAW_EVIDENCE='evidence/rea_newinput_begin_0fb0.json'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
class BeginEndInputError(OMFError):pass
def need(v,s):
 if not v:raise BeginEndInputError(s)
def validate_unit(u):
 need(set(u)=={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','reference_region','boundary_evidence'},'Exact input180 metadata keys')
 need((u['id'],u['language'],u['backend'],u['object_profile'])==('begin_end_input_code180','asm-code',BACKEND,'begin_end_input_66instructions_180'),'Closed input180 identity')
 need(u['source']==SOURCE and u['source_sha256']==SOURCE_SHA256 and u['assembler_sha256']==TOOL_PINS['toolchains/msc510/MASM.EXE'],'Exact source/assembler')
 need(u['public_symbols']==list(PUBLIC_OFFSETS)and u['image_offset']==hex(BASE)and type(u['size'])is int and u['size']==SIZE and u['externals']==BINDINGS,'Whole180/two native PUBLICs/exact logical bindings')
 need(u['rea_evidence']==RAW_EVIDENCE and u['reference_region']=='unchanged-prefix'and isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence'].strip()),'Exact native evidence')
def source_policy(content):
 need(type(content)is bytes and H(content)==SOURCE_SHA256,'Exact reviewed mnemonic source')
 try:text=content.decode('ascii')
 except UnicodeDecodeError:raise BeginEndInputError('ASCII source required')
 live='\n'.join(line.split(';',1)[0]for line in text.splitlines())
 need(not re.search(r'\b(DB|DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC)\b',live,re.I),'No data/opcode inclusion/padding directives')
 need(len([line for line in text.splitlines()if line.startswith('    ')and'; native'in line])==66 and 'OFFSET DGROUP:_actors'in live,'Exact66mnemonics/explicit native DGROUP actor field')
def validate_object(o):
 need(isinstance(o,OMFObject)and set(o.segments)=={1,2}and not o.procedures,'Exactly empty DATA/CODE/no invented CV procedures')
 ds,cs=o.segments[1],o.segments[2]
 need((ds.name,ds.class_name,ds.length,ds.attributes,ds.unsupported_data,ds.chunks)==('_DATA','DATA',0,72,False,[]),'No DATA allocation')
 need((cs.name,cs.class_name,cs.length,cs.attributes,cs.unsupported_data)==('_TEXT','CODE',180,72,False),'Whole WORD/PUBLIC CODE180')
 need(o.names==['','','DGROUP','DATA','CODE','_DATA','_TEXT']and o.externals==EXTERNALS,'Exact names/14 real externals')
 need(set(o.publics)==set(PUBLIC_OFFSETS),'Exactly two entry PUBLICs')
 for name,off in PUBLIC_OFFSETS.items():need(asdict(o.publics[name])=={'name':name,'segment':2,'offset':off,'group':0,'type_index':0},'Exact PUBLIC segment/offset/type')
 need([(k,at,H(b))for k,at,b in o.records]==RECORD_PINS,'Every raw record payload/boundary')
 raw=bytearray()
 for at,data in cs.chunks:need(at==len(raw)and bool(data)and at+len(data)<=SIZE,'CODE hole/overlap/tail');raw.extend(data)
 need(len(raw)==SIZE and H(raw)==RAW_CODE_SHA256,'Whole unchanged raw CODE180')
 need(all(sn==2 for pos,sn,off,n in o.data_writes),'Every actual write belongs to CODE')
 fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups]
 need(fields==FIELD_PROFILE and len(fields)==34,'Exact34 typed fields/no omitted fixups')
 need(sum(f.segment_relative for f in o.fixups)==28 and all(f.segment==2 and f.width==2 and f.location_type==1 for f in o.fixups),'28 DGROUP fields/6near CALL/no MZ')
 return bytes(raw),{'boundary':'whole_CODE180_plus_empty_DATA','CODE_segment':{'index':2,'name':'_TEXT','class':'CODE','length':180,'attributes':72},'DATA_segment':{'index':1,'name':'_DATA','length':0,'attributes':72},'publics':[asdict(o.publics[n])for n in PUBLIC_OFFSETS],'actual_external_fields':34,'actual_DGROUP_fields':28,'actual_near_CALL_fields':6,'actual_internal_fields':0,'source_instructions':66,'native_MZ':[],'C_credit':0,'authored_asm_function_credit':0,'initialized_DATA_credit':0,'C_status':'UNRESOLVED nativeframe4/naturalCframe0','unprovided_saved_BYTE':UNPROVIDED_SAVED_BYTES,'historical_ASM_TU_or_C_unrepresentability_proven':False}
def extract_code(raw):
 o=read_omf(raw);code,meta=validate_object(o);need(H(raw)==OBJECT_SHA256,'Exact unchanged whole source object');return code,meta
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 code:bytes
 metadata:dict
 provenance:dict
from contextlib import contextmanager
from unittest.mock import patch
import builtins,io
@contextmanager
def generation_guard(source,project,scratch):
 # Open guards cover Python producer reads/writes; DOSBox sees only fresh scratch/tools mounts.
 source=Path(source).resolve();project=Path(project).resolve();scratch=Path(scratch).resolve()
 reads={source,Path('/usr/bin/dosbox').resolve()}|{(project/n).resolve()for n in TOOL_PINS}
 saved=(builtins.open,io.open,os.open);events={'reads':[],'writes':[],'blocked':[]}
 def authorize(name,write):
  need(not isinstance(name,int),'No inherited file descriptors in source generator')
  p=Path(name).resolve();ok=p.is_relative_to(scratch)or(not write and p in reads)
  if not ok:events['blocked'].append(str(p));raise BeginEndInputError('Source-only generation denied '+str(p))
  events['writes'if write else'reads'].append(str(p))
 def guarded_open(name,mode='r',*a,**kw):authorize(name,any(c in str(mode)for c in 'wax+'));return saved[0](name,mode,*a,**kw)
 def guarded_io(name,mode='r',*a,**kw):authorize(name,any(c in str(mode)for c in 'wax+'));return saved[1](name,mode,*a,**kw)
 def guarded_os(name,flags,*a,**kw):need(not kw.get('dir_fd'),'No relative descriptor access');authorize(name,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)));return saved[2](name,flags,*a,**kw)
 with patch.object(builtins,'open',guarded_open),patch.object(io,'open',guarded_io),patch.object(os,'open',guarded_os):yield events

def _assemble_source(source,project):
 # No reference/carrier/OBJ/profile/evidence argument or lookup in this generation phase.
 source=Path(source).resolve();project=Path(project).resolve()
 with tempfile.TemporaryDirectory(prefix='bc-begin-end-input-')as directory:
  p=Path(directory);t=p/'tools';t.mkdir()
  with generation_guard(source,project,p)as events:
   content=source.read_bytes();source_policy(content)
   tools={n:(project/n).read_bytes()for n in TOOL_PINS}
   for n,b in tools.items():need(H(b)==TOOL_PINS[n],'Pinned source-generation tool '+n)
   need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
   # Inert denial probes are retained in actual generation provenance, outside comparison.
   for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'build/begin-end-input180-root-actual/scratch/UNIT.OBJ',project/'build/begin-end-input180-mnemonic-preparation/native180-comparison-only.bin',project/'build/begin-end-input180-mnemonic-preparation/preparation-review.json']:
    try:forbidden.read_bytes()
    except BeginEndInputError:pass
    else:raise BeginEndInputError('Generation guard probe unexpectedly permitted')
   (t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
   command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
   batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
   conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
   with (p/'HOST.LOG').open('wb')as host:
    result=subprocess.run(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=host,stderr=subprocess.STDOUT,timeout=45,check=False)
   host_output=(p/'HOST.LOG').read_bytes().decode('utf-8','replace')
   log=(p/'MASM.LOG').read_bytes().decode('cp437');need(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and'5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM errors: '+log)
   raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437')
   for n,h in TOOL_PINS.items():need(H((project/n).read_bytes())==h,'Tool changed')
   need(source.read_bytes()==content,'Source changed')
  return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'subprocess_returncode':result.returncode,'subprocess_terminal_reaped':True,'host_output':host_output,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_guard':events,'generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'source_instruction_count':66,'authored_asm_function_credit':0,'original_absolute_placement_proven':False}
def assemble(source,project):
 project=Path(project).resolve();source=Path(source).resolve()
 need(source==(project/SOURCE).resolve()and source.is_relative_to(project)and not(project/SOURCE).is_symlink(),'Exact standalone source path')
 raw,provenance=_assemble_source(source,project);code,meta=extract_code(raw)
 return Build(raw,code,meta,provenance)
def link_code(raw,load=0):
 initial,meta=extract_code(raw);o=read_omf(raw);need(type(load)is int and 0<=load<=65535,'16bit load paragraph');view=bytearray(initial);logs=[]
 for f in sorted(o.fixups,key=lambda f:f.offset):
  add=int.from_bytes(initial[f.offset:f.offset+2],'little');disp=f.displacement or 0;name=o.externals[f.target[1]];site=BASE+f.offset
  if f.segment_relative:need(f.frame==(1,1),'DGROUP frame');value=BINDINGS[name]+add+disp;mode='segment_relative_DGROUP'
  else:need(f.frame in[(5,None),(2,f.target[1])]and add+disp==0,'Near external CALL frame/addend');value=BINDINGS[name]-site-2;mode='self_relative_external_CODE'
  value&=65535;view[f.offset:f.offset+2]=value.to_bytes(2,'little');logs.append({'segment':2,'object_offset':f.offset,'image_offset':site,'width':2,'mode':mode,'target_symbol':name,'frame':list(f.frame),'target':list(f.target),'raw_fixupp':f.raw.hex(),'source_addend':add,'target_displacement':disp,'encoded_hex':value.to_bytes(2,'little').hex()})
 return bytes(view),logs

def _evidence(project):
 out={}
 for name,h in EVIDENCE_PINS.items():
  raw=(Path(project)/name).read_bytes();need(H(raw)==h,'Input180 evidence pin '+name);out[name]=json.loads(raw)
 p=out['build/begin-end-input180-mnemonic-preparation/preparation-review.json'];q=p['original_REA_false_hole_qualification']
 need(p['instruction_count']==66 and p['native_complete_bytes']==180 and p['native_sha256']==NATIVE_SHA256 and p['bindings']==BINDINGS,'Exact66/native180/bindings')
 need(q['original_body']['total_bytes']==124 and q['original_body']['span_bytes']==125 and q['complete_expanded_body']['total_bytes']==125 and q['excluded_original_byte']==0x1012 and q['same44_decoded_instructions'],'Retain original false operand hole; independent expanded125')
 positive=out['build/begin-end-input180-root-actual/comparison/whole-object-comparison.json'];need(positive['raw_object_sha256']==OBJECT_SHA256 and positive['whole_native_CODE_equal']and positive['whole_CODE_bytes']==180 and len(positive['all_actual_symbolic_fields'])==34 and not positive['all_differences'],'Whole accepted raw34-field positive')
 receipt=out['build/begin-end-input180-root-actual/generation-receipt.json'];tool=out['build/begin-end-input180-root-actual/actual-root-tool-result.json'];need(receipt['status']=='COMPLETE'and receipt['actual_MASM_calls']==1 and receipt['source_tool_scratch_only']and len(receipt['blocked_probes'])==6 and tool['terminal']and tool['exit_code']==0 and tool['child_reaped']and tool['raw_object_sha256']==OBJECT_SHA256,'Closed actual genuine producer provenance')
 for name in[RAW_EVIDENCE,'evidence/rea_newinput_reset_102d.json','evidence/rea_board_coordinates_102d_raw.json']:
  e=out[name];need(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['provider']['id']=='ghidra','Original native REA identity')
 expanded=out['evidence/rea_board_pointer_next_0fb0_expanded.json'];need(expanded['subject']['digest']['sha256']==CARRIER_SHA256,'Pinned expanded identity')
 return out

def _sites(original_sites):
 selected=[p for p in original_sites if BASE<=p<BASE+SIZE or BASE<p+2<=BASE+SIZE];need(not selected,'Exact native180 MZempty including boundary-crossing fields');return []
def validate_evidence(u,project,target_sha256,reference=None):
 validate_unit(u);need(target_sha256==ORIGINAL_SHA256 and reference is not None and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']>=BASE+SIZE,'Original/carrier unchanged prefix');_sites(reference['relocations']);out=_evidence(project)
 need(H(reference['image'][BASE:BASE+SIZE])==NATIVE_SHA256,'Complete native180 identity')
 raw=out['evidence/rea_board_coordinates_102d_raw.json'];need(raw['parameters']=={'address':'0x1102d','length':56}and raw['normalized_result']['complete']and bytes.fromhex(raw['normalized_result']['bytes_hex'])==reference['image'][0x102d:0x102d+56],'Original full55 end body plus independent next-byte join; nextbyte unclaimed')
 return out[RAW_EVIDENCE]['evidence_id']
def validate_comparison(u,built,image,project,original_sites):
 validate_unit(u);code,meta=extract_code(built.object_bytes);need(code==built.code and meta==built.metadata,'Fresh unchanged whole generated object');out=_evidence(project);sites=_sites(original_sites);linked,logs=link_code(built.object_bytes)
 need(linked==image[BASE:BASE+SIZE]and H(linked)==NATIVE_SHA256,'Every whole180 native byte');loads=[]
 for base in[0,1,4096,65535]:
  actual,_=link_code(built.object_bytes,base);need(actual==image[BASE:BASE+SIZE],'Whole180 no-MZ fourbase comparison');loads.append({'load_paragraph':base,'all180_native_equal':True,'native_MZ_sites':[]})
 return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':H(linked),'whole_bytes_equal':True,'whole_original_mz_sites':sites,'emitted_mz_sites':[],'relocations':logs,'four_load_bases':loads,'native_evidence_id':out[RAW_EVIDENCE]['evidence_id'],'source_instructions':66,'actual_external_fields':34,'actual_internal_fields':0,'classification':'authored_begin_end_input_CODE_component','authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'C_status':'UNRESOLVED nativeframe4/naturalCframe0','unprovided_saved_BYTE':UNPROVIDED_SAVED_BYTES,'historical_ASM_TU_or_C_unrepresentability_proven':False,'original_absolute_placement_proven':False}
