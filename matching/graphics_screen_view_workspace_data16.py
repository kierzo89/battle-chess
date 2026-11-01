"""Exact six-PUBLIC initialized workspace; same86000 bytes, no C/capacity credit."""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,subprocess,tempfile,os,re
from graphics_screen_view_zero_omf16 import validate_obj,DataError
from omf import read_omf
from reference import ORIGINAL_SHA256,CARRIER_SHA256,validate_expanded_read
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
BACKEND='masm510-graphics-screen-view-workspace-data-omf'
SOURCE='src/data/graphics_screen_view_workspace.asm'
SOURCE_SHA256='15afff3a47714d772582b2c91a8a675411d324dbdeeccf24a2ade564392e6b22'
OBJECT_SHA256='0a44eb20bc364a52fba29d5420546ead27ec61910548f1f4f813cbaec8e1eeb7'
PROFILE_SHA256='443d6372b38d92cb5a676088524e3b253917f0c829d8723a5b30f24c4c50cf5d'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise DataError(s)
def _profile():
 raw=(M/'graphics_screen_view_workspace_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'Exact closed6PUBLIC profile');return json.loads(raw)
def validate_unit(u):
 p=_profile();need(p['schema']=='graphics-screen-view-workspace-v1'and p['backend']==BACKEND and u==p['unit'],'Exact closed physical5view unit metadata')
 need(p['whole_object_sha256']==OBJECT_SHA256 and p['source_sha256']==SOURCE_SHA256 and p['complete_initialized_bytes']==86000,'Whole unchanged extent/source/object')
def source_policy(content):
 need(type(content)is bytes and H(content)==SOURCE_SHA256,'Exact standalone six-view mnemonic DATA source')
 try:text=content.decode('ascii')
 except UnicodeDecodeError:raise DataError('ASCII source required')
 live='\n'.join(line.split(';',1)[0]for line in text.splitlines());need(not re.search(r'\b(ORG|ALIGN|EVEN|INCLUDE|INCBIN|EXTRN|PROC|MACRO|REPT|IRP|IRPC)\b',live,re.I),'No external/opcode/padding/import directives')
def extract_data(raw):
 pieces,meta=validate_obj(raw);need(H(raw)==OBJECT_SHA256,'Exact genuine whole6PUBLIC object')
 meta.update(boundary='two_complete_initialized_PRIVATE_PARA_53184_32816_six_distinct_BYTE_PUBLICs',classification='opaque_physical_initialized_DATA_with_native_views',source_partition_is_engineering=True,historical_TU_proven=False,historical_C_capacity_proven=False,original_global_MAP_proven=False,authored_c_credit=0,new_byte_credit=0,new_native_MZ_credit=0,authored_asm_function_credit=0)
 return b''.join(pieces),meta
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 data:bytes
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
  if not ok:events['blocked'].append(str(p));raise DataError('Source-only generation denied '+str(p))
  events['writes'if write else'reads'].append(str(p))
 def guarded_open(name,mode='r',*a,**kw):authorize(name,any(c in str(mode)for c in 'wax+'));return saved[0](name,mode,*a,**kw)
 def guarded_io(name,mode='r',*a,**kw):authorize(name,any(c in str(mode)for c in 'wax+'));return saved[1](name,mode,*a,**kw)
 def guarded_os(name,flags,*a,**kw):need(not kw.get('dir_fd'),'No relative descriptor access');authorize(name,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)));return saved[2](name,flags,*a,**kw)
 with patch.object(builtins,'open',guarded_open),patch.object(io,'open',guarded_io),patch.object(os,'open',guarded_os):yield events

def _assemble_source(source,project):
 # No reference/carrier/OBJ/profile/evidence argument or lookup in this generation phase.
 source=Path(source).resolve();project=Path(project).resolve()
 with tempfile.TemporaryDirectory(prefix='bc-buffer-views-')as directory:
  p=Path(directory);t=p/'tools';t.mkdir()
  with generation_guard(source,project,p)as events:
   content=source.read_bytes();source_policy(content)
   tools={n:(project/n).read_bytes()for n in TOOL_PINS}
   for n,b in tools.items():need(H(b)==TOOL_PINS[n],'Pinned source-generation tool '+n)
   need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
   # Inert denial probes are retained in actual generation provenance, outside comparison.
   for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'tests/fixtures/graphics_screen_view/actual.obj',project/'evidence/graphics_screen_view/component.json',project/'graphics_screen_view_workspace_profile.json']:
    try:forbidden.read_bytes()
    except DataError:pass
    else:raise DataError('Generation guard probe unexpectedly permitted')
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
  return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'subprocess_returncode':result.returncode,'subprocess_terminal_reaped':True,'host_output':host_output,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_guard':events,'generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'whole_initialized_bytes':86000,'new_byte_credit':0,'new_native_MZ_credit':0,'authored_asm_function_credit':0,'original_absolute_placement_proven':False}
def assemble(source,unit,nasm=None):
 validate_unit(unit);source=Path(source);need(source.resolve()==(M/SOURCE).resolve()and not source.is_symlink(),'Exact regular six-view source path')
 raw,provenance=_assemble_source(source,M);data,meta=extract_data(raw);need(provenance['source_sha256']==unit['source_sha256'],'Exact generated source')
 return Build(raw,data,meta,provenance)
def _owned_evidence(project):
 p=_profile();out={}
 for name,h in p['evidence_pins'].items():
  path=(Path(project)/name).resolve();need(path.is_relative_to(Path(project).resolve()),'Owned evidence path');raw=path.read_bytes();need(H(raw)==h,'Owned comparison dependency '+name);out[name]=json.loads(raw)if name.endswith('.json')else raw
 return p,out

def validate_evidence(u,project,target_sha256,reference=None):
 validate_unit(u)
 import graphics_buffer_views_workspace_data16 as old
 import screen_far_pointer_data16 as pointer
 # The established five-view gate remains exact and independently authenticates all21 native fields.
 need(H((Path(project)/'graphics_buffer_views_workspace_profile.json').read_bytes())==_profile()['old_five_profile_sha256'],'Unchanged old five-view profile')
 proof=old.validate_evidence(old._profile()['unit'],project,target_sha256,reference)
 p,out=_owned_evidence(project);r='evidence/graphics_screen_view/'
 c=out[r+'component.json'];g=out[r+'generation.json'];ct=out[r+'component-terminal.json'];lt=out[r+'LINK-comparison-terminal.json'];link=out[r+'LINK-calibration.json'];terminal=out[r+'LINK-terminal.json'];gt=out[r+'generation-terminal.json']
 need(c['status']=='PASS_GENUINE6PUBLIC_SAME86000_NONCANONICAL_SCREEN_VIEW_COMPONENT_ONLY' and c['source_sha256']==SOURCE_SHA256 and c['raw_object_sha256']==OBJECT_SHA256 and c['old5PUBLIC_oldbytes_unchanged'],'Closed whole six-view source/component')
 need(g['status']=='COMPLETE' and g['guard_closed'] and g['actual_MASM_calls']==1 and g['source_sha256']==SOURCE_SHA256 and g['raw_whole_object_sha256']==OBJECT_SHA256,'Closed genuine source-only MASM')
 need(ct['terminal'] and ct['reaped'] and ct['exit_code']==0 and lt['terminal'] and lt['reaped'] and lt['exit_code']==0 and lt['comparison_sha256']==H(json.dumps(link,indent=2).encode()+b'\n'),'Closed component and LINK comparison terminals')
 need(gt['terminal'] and gt['reaped'] and gt['exit_code']==0 and gt['actual_MASM_calls']==1 and gt['raw_whole_object_sha256']==OBJECT_SHA256 and gt['generation_receipt_sha256']==H(json.dumps(g,indent=2).encode()+b'\n'),'Actual source producer terminal')
 need(terminal['terminal'] and terminal['reaped'] and terminal['exit_code']==0 and terminal['LINK_calls']==1,'One actual calibration LINK terminal')
 need(ct['comparison_sha256']==H(json.dumps(c,indent=2).encode()+b'\n'),'Whole component comparison receipt')
 need(link['status']=='PASS_ONE_AUTHENTIC_RETAINED267_LINK_SIX_VIEW_CALIBRATION_NO_FRESH_SOURCE_CLAIM' and link['objects']==267 and link['only_replaced_slot']==73 and link['replacement_raw_sha256']==OBJECT_SHA256 and link['unchanged_other_raw_objects']==266 and link['actual_missing']==64 and link['only_removed']=='_screen_pixels' and link['old_allPUBs_and_SEGDEF_layout_unchanged'] and link['whole86000unchanged'] and link['actual_pointer_hex'].startswith('404c') and link['native_Cfunction_DATA_FILE_MZ_orallocation_credit_added']==0,'Actual retained full-LIB calibration; no fresh claim or credit')
 raw=out[r+'screen-pointer.obj'];need(H(raw)=='fa688769a8e29de119fb2a55a1d157678a776595799deb710d83ed3eed85ee1a','Whole genuine pointer client')
 data,q=pointer.link_data(raw,'_screen',0x5d1ee,0x5cc2,{'_screen_pixels':{'segment':0x120d,'offset':0x4c40}})
 need(data==reference['image'][0x5d1ee:0x5d1f2] and q['emitted_mz_sites']==[0x5d1f0] and 0x5d1f0 in reference['relocations'],'Native noncanonical FAR4 and existing selector MZ')
 need(len(q['all_raw_fixups'])==2 and q['debug']['validated_debug_fixups']==1 and q['debug']['type_records'][-1]['raw_hex']=='0105007800838000','Both actual DATA/debug FAR fields and incomplete char[] view')
 for load in [0,1,4096,65535]:
  b=bytes.fromhex('404c')+((0x120d+load)&65535).to_bytes(2,'little');need(b[:2]==data[:2] and int.from_bytes(b[2:],'little')==((int.from_bytes(data[2:],'little')+load)&65535),'Four loader bases preserve offset4C40')
 return proof
