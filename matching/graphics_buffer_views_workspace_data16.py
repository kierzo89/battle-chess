"""Exact five-PUBLIC initialized workspace; same86000 bytes, no C/capacity credit."""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,subprocess,tempfile,os,re
from graphics_buffer_views_zero_omf16 import validate_obj,DataError
from omf import read_omf
from reference import ORIGINAL_SHA256,CARRIER_SHA256,validate_expanded_read
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
BACKEND='masm510-graphics-buffer-views-workspace-data-omf'
SOURCE='src/data/graphics_buffer_views_workspace.asm'
SOURCE_SHA256='29cf1316bab6c0db5261e54dfcb0f38577595c6d412004c194caa904948a4c31'
OBJECT_SHA256='0ebca9e135fccd18d46d3fdc12a12ecd0f68183c722abf290b92dc6627379ad4'
PROFILE_SHA256='655792622908846629be079e96ca677b462b5a5bb98ff0d0bf05fc9a249f4c78'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise DataError(s)
def _profile():
 raw=(M/'graphics_buffer_views_workspace_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'Exact closed5PUBLIC profile');return json.loads(raw)
def validate_unit(u):
 p=_profile();need(p['schema']=='graphics-buffer-views-workspace-v1'and p['backend']==BACKEND and u==p['unit'],'Exact closed physical5view unit metadata')
 need(p['whole_object_sha256']==OBJECT_SHA256 and p['source_sha256']==SOURCE_SHA256 and p['complete_initialized_bytes']==86000,'Whole unchanged extent/source/object')
def source_policy(content):
 need(type(content)is bytes and H(content)==SOURCE_SHA256,'Exact standalone five-view mnemonic DATA source')
 try:text=content.decode('ascii')
 except UnicodeDecodeError:raise DataError('ASCII source required')
 live='\n'.join(line.split(';',1)[0]for line in text.splitlines());need(not re.search(r'\b(ORG|ALIGN|EVEN|INCLUDE|INCBIN|EXTRN|PROC|MACRO|REPT|IRP|IRPC)\b',live,re.I),'No external/opcode/padding/import directives')
def extract_data(raw):
 pieces,meta=validate_obj(raw);need(H(raw)==OBJECT_SHA256,'Exact genuine whole5PUBLIC object')
 meta.update(boundary='two_complete_initialized_PRIVATE_PARA_53184_32816_five_distinct_BYTE_PUBLICs',classification='opaque_physical_initialized_DATA_with_native_views',source_partition_is_engineering=True,historical_TU_proven=False,historical_C_capacity_proven=False,original_global_MAP_proven=False,authored_c_credit=0,new_byte_credit=0,new_native_MZ_credit=0,authored_asm_function_credit=0)
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
   for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'tests/fixtures/graphics_buffer_views/actual.obj',project/'evidence/graphics_buffer_views/comparison.json',project/'graphics_buffer_views_workspace_profile.json']:
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
 validate_unit(unit);source=Path(source);need(source.resolve()==(M/SOURCE).resolve()and not source.is_symlink(),'Exact regular five-view source path')
 raw,provenance=_assemble_source(source,M);data,meta=extract_data(raw);need(provenance['source_sha256']==unit['source_sha256'],'Exact generated source')
 return Build(raw,data,meta,provenance)
def _owned_evidence(project):
 p=_profile();out={}
 for name,h in p['evidence_pins'].items():
  path=(Path(project)/name).resolve();need(path.is_relative_to(Path(project).resolve()),'Owned evidence path');raw=path.read_bytes();need(H(raw)==h,'Owned comparison dependency '+name);out[name]=json.loads(raw)if name.endswith('.json')else raw
 return p,out

def _whole_debug(o,klass):
 s=next((s for s in o.segments.values()if s.class_name==klass),None)
 if s is None:return None
 view=bytearray(s.length);seen=set()
 for at,b in s.chunks:need(0<=at<=at+len(b)<=s.length,'CV bounded ordered write');view[at:at+len(b)]=b;seen.update(range(at,at+len(b)))
 need(len(seen)==s.length,'Whole debug graph ownership');return bytes(view)
def _cv_graph(o):
 b=_whole_debug(o,'DEBTYP');types={};at=0;idx=0x200
 if b:
  while at<len(b):
   need(b[at]==1 and at+3<=len(b),'CV type linkage/header');n=int.from_bytes(b[at+1:at+3],'little');v=b[at+3:at+3+n];need(len(v)==n,'Whole CV type');types[str(idx)]=v.hex();idx+=1;at+=n+3
  need(at==len(b),'CV type boundary')
 b=_whole_debug(o,'DEBSYM');symbols=[];at=0
 if b:
  while at<len(b):
   n=b[at];v=b[at+1:at+1+n];need(len(v)==n and n>0,'Whole CV symbol')
   if any(name in v for name in[b'color_buffer',b'region_buffer']):symbols.append({'symbol_record_offset':at,'raw':v.hex(),'kind':v[0],'type_index':int.from_bytes(v[5:7],'little')if v[0]==5 else None})
   at+=n+1
  need(at==len(b),'CV symbol boundary')
 return symbols,types

def validate_evidence(u,project,target_sha256,reference=None):
 validate_unit(u);need(Path(project).resolve()==M.resolve(),'Adopted project evidence root');need(target_sha256==ORIGINAL_SHA256 and reference is not None and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'Original/carrier identity')
 p,out=_owned_evidence(project);root='evidence/graphics_buffer_views/';audit=out[root+'typed-field-review.json'];positive=out[root+'comparison.json'];receipt=out[root+'generation-receipt.json'];tool=out[root+'tool-result.json']
 need(audit['objects_scanned']==240 and audit['definitions_collision_count']==0 and audit['fields']==21 and audit['native_fields']==18 and audit['whole86000_owned_unchanged'],'Complete original consumer inventory')
 need(positive['status'].startswith('PASS whole86000')and positive['whole_object_sha256']==OBJECT_SHA256 and positive['source_sha256']==SOURCE_SHA256 and positive['native_CODE_fields']==18 and positive['debug_fields']==3 and positive['all240_input_objects_unchanged'],'Whole actual source positive')
 need(receipt['status']=='COMPLETE'and receipt['actual_MASM_calls']==1 and receipt['source_tool_scratch_only']and receipt['source_sha256']==SOURCE_SHA256 and receipt['raw_object_sha256']==OBJECT_SHA256 and len(receipt['guard']['blocked'])==5 and receipt['terminal']and receipt['child_reaped'],'Exact closed source-only positive producer')
 need(tool['exit_code']==0 and tool['terminal']and tool['reaped']and tool['actual_MASM_calls']==1 and tool['raw_object_sha256']==OBJECT_SHA256,'Actual terminal producer receipt')
 fields=audit['all_fields'];objects={};actual=[]
 for old,name in p['comparison_client_copies'].items():
  o=read_omf(out[name]);objects[old]=o
  for f in o.fixups:
   if f.target[0]==2 and o.externals.get(f.target[1])in['_color_buffer','_region_buffer']:
    s=asdict(f);s.update(raw=f.raw.hex(),frame=list(f.frame),target=list(f.target));actual.append((old,o.externals[f.target[1]],s))
 key=lambda row:(row[0],row[2]['record_offset'],row[2]['segment'],row[2]['offset']);need(len(actual)==21 and sorted(actual,key=key)==sorted([(f['object'],f['symbol'],f['raw_field'])for f in fields],key=key),'All21 actual raw client fields, no omitted debug/BASE/OFFSET fields')
 for graph in audit['complete_client_CV_graphs']:
  syms,types=_cv_graph(objects[graph['object']]);need(syms==graph['symbols']and types==graph['whole_type_graph'],'Whole genuine client CV graph')
  need(all(s['kind']==5 and types[str(s['type_index'])]=='7800838000'for s in syms),'Incomplete zero-extent char-array views, no capacity')
 view_segments={1:0x120d,2:0x1f09};native=reference['image'];mz=[];code_fields=0
 for f in fields:
  seg,off=p['publics'][f['symbol']];address={'segment':view_segments[seg],'offset':off};need(address==f['native_binding'],'Exact real distinct view coordinates')
  if f['native_field']is None:need(f['source_segment_class']=='DEBSYM'and f['raw_field']['width']==4,'Debug-only FAR field');continue
  q=f['raw_field'];need(f['source_segment_class']=='CODE'and q['width']==2 and q['location_type']in[1,2]and q['segment_relative']and q['frame']in[[5,None],[2,q['target'][1]]],'Exact BASE/OFFSET frame contract');o=objects[f['object']];s=o.segments[q['segment']];raw=bytearray(s.length)
  for at,b in s.chunks:raw[at:at+len(b)]=b
  add=int.from_bytes(raw[q['offset']:q['offset']+2],'little');need(add==f['original_addend']and(q['displacement']or 0)==f['displacement'],'Actual source field/addend');site=f['native_field'];need(site==audit['source_native_origins'][f['object']]+q['offset'],'Exact whole CODE origin')
  expected_site=[]if q['location_type']==1 else[site];need(expected_site==f['native_MZ'],'Actual native MZ ownership');mz+=expected_site;code_fields+=1
  for load in[0,1,4096,65535]:
   value=((off if q['location_type']==1 else address['segment']+load)+add+f['displacement'])&65535;expected=int.from_bytes(native[site:site+2],'little');expected=(expected+(load if expected_site else 0))&65535;need(value==expected,'All18 native fields at four actual load bases')
 need(code_fields==18 and len(mz)==9 and sorted(set(mz))==audit['native_MZ_sites']and all(s in reference['relocations']for s in mz),'Nine existing native consumer MZ sites, no credit addition')
 observed=out[root+'rea_graphics_workspace_86000.json'];need(not [s for s in reference['relocations']if 0x120d0<=s<0x270c0 or 0x120d0<s+2<=0x270c0],'No MZ inside initialized workspace')
 return validate_expanded_read(observed,u,bytes(86000),reference,emitted_mz_sites=[])
