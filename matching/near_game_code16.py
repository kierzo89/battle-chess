"""Closed authored mnemonic near-game components; no generic fallback or C credit."""
from pathlib import Path
from dataclasses import dataclass,asdict
from contextlib import contextmanager
from unittest.mock import patch
import json,hashlib,re,tempfile,subprocess,os,builtins,io
from omf import OMFObject,OMFError,read_omf
from reference import ORIGINAL_SHA256,CARRIER_SHA256
from near_game_code_pins import PROFILE_SHA256,GEN_SOURCES,EVIDENCE_PINS
BACKEND='masm510-near-game-authored-code-omf-v1'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
class NearGameError(OMFError):pass
def need(v,s):
 if not v:raise NearGameError(s)
def canon(v):
 def norm(x):
  if isinstance(x,dict):
   need(all(type(k)in(int,str)for k in x),'Snapshot key type');need(len({str(k)for k in x})==len(x),'Duplicate normalized snapshot key');return {str(k):norm(y)for k,y in x.items()}
  if isinstance(x,(list,tuple)):return [norm(y)for y in x]
  return x
 return json.dumps(norm(v),sort_keys=True,separators=(',',':'))
def snapshot(o):
 return {'records':[[k,at,p.hex()]for k,at,p in o.records],'names':o.names,'externals':o.externals,'publics':{n:asdict(p)for n,p in o.publics.items()},'procedures':o.procedures,'data_writes':o.data_writes,'segments':{i:{**{k:v for k,v in asdict(s).items()if k!='chunks'},'chunks':[[at,b.hex()]for at,b in s.chunks]}for i,s in o.segments.items()},'fixups':[{**asdict(f),'raw':f.raw.hex()}for f in o.fixups]}
def profiles():
 b=Path(__file__).with_name('near_game_code_profiles.json').read_bytes();need(H(b)==PROFILE_SHA256,'Closed near-game profile SHA');return json.loads(b)
def spec(key):
 p=profiles();need(key in p['ASM'],'Unknown near-game object profile; no fallback');return p['ASM'][key]
def validate_unit(u):
 need(set(u)=={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','reference_region','boundary_evidence'},'Exact near-game unit keys')
 s=spec(u['object_profile']);c=s['unit'];need(all(u[k]==c[k]for k in c if k!='boundary_evidence'),'Closed per-source/per-unit near-game contract');need(type(u['size'])is int and isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence'].strip()),'Whole extent and meaningful boundary')

def source_policy(content,source_name):
 need(source_name in GEN_SOURCES and type(content)is bytes and H(content)==GEN_SOURCES[source_name]['sha256'],'Exact selected mnemonic source')
 try:text=content.decode('ascii')
 except UnicodeDecodeError:raise NearGameError('ASCII mnemonic source')
 live='\n'.join(x.split(';',1)[0]for x in text.splitlines());need(not re.search(r'\b(DB|DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC)\b',live,re.I),'No source bytes/includes/padding directives')
 need(len(re.findall(r'; native[ ]*[0-9A-Fa-f]{4}',text))==GEN_SOURCES[source_name]['instructions'],'Exact mnemonic instruction count')
 if source_name in('asm/link/reset_position08de.asm','asm/link/reset_position08de_kind_map.asm'):
  need(re.findall(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s+EQU\s+([^\n]+)',live,re.M)==[('FULLWORD_IMMEDIATE_ZERO','0')]and text.count('AND CX, FULLWORD_IMMEDIATE_ZERO + 07h')==2 and live.index('FULLWORD_IMMEDIATE_ZERO EQU 0')>live.index('_reset_position_08de ENDP'),'Exact closed reset fullword-immediate local constant')


def validate_object(o,key):
 need(isinstance(o,OMFObject),'Actual OMF object required');s=spec(key);need(canon(snapshot(o))==canon(s['snapshot']),'Complete raw/parsed near-game OMF changed')
 cs=o.segments[2];code=bytearray()
 for at,b in cs.chunks:need(at==len(code)and b and at+len(b)<=s['size'],'Whole CODE hole/overlap');code.extend(b)
 need(len(code)==s['size']and H(code)==s['raw_CODE_sha256'],'Whole raw CODE identity')
 return bytes(code),{'object_profile':key,'whole_CODE_bytes':s['size'],'CODE_segment':{'index':2,'name':cs.name,'class':cs.class_name,'length':cs.length,'attributes':cs.attributes},'DATA_segment':{'index':1,'name':'_DATA','length':0,'attributes':72},'publics':[asdict(x)for x in o.publics.values()],'native_instructions':s['instructions'],'external_fields':len(s['external_fields']),'internal_fields':len(s['internal_fields']),'native_MZ':s['native_MZ'],'C_credit':0,'DATA_byte_credit':0,'historical_language_TU_or_C_unrepresentability_proven':False}
def extract_code(raw,key):
 s=spec(key);need(type(raw)is bytes and H(raw)==s['object_sha256'],'Exact fresh whole source object');return validate_object(read_omf(raw),key)
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 code:bytes
 metadata:dict
 provenance:dict
@contextmanager
def generation_guard(source,project,scratch):
 source=Path(source).resolve();project=Path(project).resolve();scratch=Path(scratch).resolve();reads={source,Path('/usr/bin/dosbox').resolve()}|{(project/n).resolve()for n in TOOL_PINS};saved=(builtins.open,io.open,os.open);events={'reads':[],'writes':[],'blocked':[]}
 def allow(name,write):
  need(not isinstance(name,int),'No inherited descriptor in near-game generation');p=Path(name).resolve()
  if not(p.is_relative_to(scratch)or(not write and p in reads)):events['blocked'].append(str(p));raise NearGameError('Source-only generation denied '+str(p))
  events['writes'if write else'reads'].append(str(p))
 def bo(name,mode='r',*a,**kw):allow(name,any(c in str(mode)for c in 'wax+'));return saved[0](name,mode,*a,**kw)
 def io_(name,mode='r',*a,**kw):allow(name,any(c in str(mode)for c in 'wax+'));return saved[1](name,mode,*a,**kw)
 def oo(name,flags,*a,**kw):need(not kw.get('dir_fd'),'No relative descriptor access');allow(name,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)));return saved[2](name,flags,*a,**kw)
 with patch.object(builtins,'open',bo),patch.object(io,'open',io_),patch.object(os,'open',oo):yield events

def _assemble_source(source,project,source_name):
 # Only generation constants/source/tools/fresh scratch. No profile, native or
 # archived object reads. Comparison happens after this entire scope closes.
 with tempfile.TemporaryDirectory(prefix='bc-near-game-')as directory:
  p=Path(directory);t=p/'tools';t.mkdir()
  with generation_guard(source,project,p)as events:
   content=source.read_bytes();source_policy(content,source_name);tools={n:(project/n).read_bytes()for n in TOOL_PINS}
   for n,b in tools.items():need(H(b)==TOOL_PINS[n],'Pinned near-game generation tool')
   need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
   for forbidden in [project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'evidence/near_game_asm/decode_directory289/comparison.json',project/'near_game_code_profiles.json',project/'tests/fixtures/near_game/decode_directory289.obj']:
    try:forbidden.read_bytes()
    except NearGameError:pass
    else:raise NearGameError('Generation probe was allowed')
   (t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
   command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;';batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
   conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
   with(p/'HOST.LOG').open('wb')as host:
    child=subprocess.Popen(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=host,stderr=subprocess.STDOUT)
    try:status=child.wait(timeout=45)
    except subprocess.TimeoutExpired:child.kill();child.wait();raise
   log=(p/'MASM.LOG').read_bytes().decode('cp437');need(status==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and'5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM error '+log)
   raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437');host_output=(p/'HOST.LOG').read_bytes().decode('utf8','replace')
   for n,h in TOOL_PINS.items():need(H((project/n).read_bytes())==h,'Generation tool changed')
   need(source.read_bytes()==content,'Generation source changed')
  provenance={'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_manifest_sha256':TOOL_PINS['toolchains/msc510/manifest.json'],'assembler_license_sha256':TOOL_PINS['toolchains/msc510/LICENSE'],'assembler_configuration_sha256':TOOL_PINS['config/msc510.json'],'build_command':command,'assembler_log':log,'assembler_listing':listing,'dosbox_stdout':host_output,'subprocess_pid':child.pid,'subprocess_returncode':status,'subprocess_terminal_reaped':True,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_guard':events,'generation_target_input':False,'generation_original_placement_input':False,'authored_c_function_credit':0,'authored_asm_function_credit':0}
 return raw,provenance

def assemble(source,project):
 project=Path(project).resolve();source=Path(source);need(source.is_absolute()and source==source.resolve()and not source.is_symlink(),'No source alias or relative path');name=str(source.relative_to(project));need(name in GEN_SOURCES and source==project/name and not(project/name).is_symlink(),'One of the closed exact source paths required')
 raw,provenance=_assemble_source(source,project,name);key=GEN_SOURCES[name]['profile'];code,meta=extract_code(raw,key);return Build(raw,code,meta,provenance)

def link_code(raw,key,load=0):
 initial,meta=extract_code(raw,key);s=spec(key);o=read_omf(raw);need(type(load)is int and 0<=load<=65535,'16bit load paragraph');out=bytearray(initial);logs=[];emitted=[]
 for f in o.fixups:
  add=int.from_bytes(initial[f.offset:f.offset+2],'little');disp=f.displacement or 0;site=s['base']+f.offset;name=None;mz=None
  if f.target[0]==2:
   e=next((x for x in s['external_fields']if x['offset']==f.offset),None);need(e is not None,'Unclaimed external field');name=o.externals[f.target[1]];need(name==e['symbol']and add+disp==e['source_addend'],'Exact symbolic field/addend')
   if e['kind']=='near-CALL':
    need((f.width,f.location_type,f.segment_relative,f.frame)==(2,1,False,(2,f.target[1])),'Actual near CALL frame');v=e['native_target']+add+disp-site-2;mode='self_relative_external_CODE'
   elif e['kind']=='DGROUP':
    need((f.width,f.location_type,f.segment_relative,f.frame)==(2,1,True,(1,1)),'Actual DGROUP frame');v=e['native_target']+add+disp;mode='segment_relative_DGROUP'
   elif e['kind']=='FAR-CALL':
    need((f.width,f.location_type,f.segment_relative,f.frame)==(4,3,True,(2,f.target[1]))and initial[f.offset+2:f.offset+4]==b'\0\0'and e['source_addend']==0 and type(e['native_frame'])is int and 0<=e['native_frame']<=65535,'Exact closed FAR CALL field/frame')
    v=e['native_target']+add+disp;need(0<=v<=65535,'Exact FAR offset');out[f.offset+2:f.offset+4]=((e['native_frame']+load)&65535).to_bytes(2,'little');mz=site+2;emitted.append(mz);mode='external_FAR16'
   else:raise NearGameError('Unknown field kind; closed near-CODE/DGROUP only')
  else:
   e=next((x for x in s['internal_fields']if x['offset']==f.offset),None);need(e is not None and(f.width,f.location_type,f.segment_relative,f.frame,f.target)==(2,1,False,(0,2),(0,2))and add+disp==e['target_offset'],'Exact own-CODE near-branch field');v=e['target_offset']-f.offset-2;mode='self_relative_internal_CODE'
  out[f.offset:f.offset+2]=(v&65535).to_bytes(2,'little');row={'segment':2,'object_offset':f.offset,'image_offset':site,'width':f.width,'mode':mode,'target_symbol':name,'frame':list(f.frame),'target':list(f.target),'raw_fixupp':f.raw.hex(),'source_addend':add,'target_displacement':disp,'encoded_hex':out[f.offset:f.offset+f.width].hex()}
  if mz is not None:row['mz_segment_relocation_image_offset']=mz
  logs.append(row)
 need(sorted(emitted)==s['native_MZ'],'Exact emitted MZ set');return bytes(out),logs

def _reset_physical_evidence(s,primary,body,p,out,r):
 need((s['base'],s['size'],s['instructions'],s['native_MZ'])==(0x8de,1168,392,[0xd2b]),'Exact closed reset physical profile')
 need(primary['subject']['digest']['sha256']==CARRIER_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode'and primary['normalized_result']['procedure']['address']=='0x108de','Reset carrier live primary identity')
 need(body.get('available')and body['ranges']==[{'start':'0x108de','end':'0x10d38'},{'start':'0x10d3b','end':'0x10d6d'}]and body['total_bytes']==1166 and body['span_bytes']==1168 and body['non_contiguous']and body['contains_entry'],'Exact reset1166 noncontiguous live body, not1168')
 read=out[r+'/physical-read.json'];n=read['normalized_result'];need(read['subject']['digest']['sha256']==CARRIER_SHA256 and read['analysis_profile']['parameters']['load_segment']=='0x1000'and n['complete']and int(n['address'],0)==0x108de and n['requested_bytes']==n['returned_bytes']==1199,'Complete retained1199 read, only physical1168 prefix owned')
 loaded=bytes.fromhex(n['bytes_hex']);need(len(loaded)==1199,'Complete actual carrier read bytes');native=bytearray(loaded[:1168]);at=0xd2b-0x8de;need(int.from_bytes(native[at:at+2],'little')==0x1fbf,'Exact one loaded FAR segment');native[at:at+2]=(0xfbf).to_bytes(2,'little');need(H(native)==s['native_sha256'],'Whole physical1168 after only genuine D2B relocation normalization')
 gap=out[r+'/gap-instruction.json'];xrefs=out[r+'/gap-xrefs.json'];gn=gap['normalized_result'];need(gap['subject']['digest']['sha256']==CARRIER_SHA256 and gn['address']=='0x10d39'and gn['status']=='undecodable'and gn['procedure']is None and gn['bytes']is None and xrefs['subject']['digest']['sha256']==CARRIER_SHA256 and xrefs['parameters']['address']=='0x10d39'and xrefs['normalized_result']==[],'Preserve actual unowned/undecodable gap query and no analyzed incoming xrefs')
 ledger=out[r+'/instruction-ledger.json'];need(len(ledger)==392,'Exact physical instruction inventory');dead=[q for q in ledger if q['image']==0xd39];need(len(dead)==1 and dead[0]['size']==2 and dead[0]['native_hex']=='eb2a'and dead[0]['source']=='JMP SHORT code_0d65'and native[0xd39-0x8de:0xd3b-0x8de]==bytes.fromhex('eb2a'),'Real derived dead JMP D65, never padding')
 live=[q for q in ledger if q['image']!=0xd39];observed=[(int(q.split(': ',1)[0],16)-0x10000,q.split(': ',1)[1])for q in primary['normalized_result']['assembly']];need(len(observed)==391 and[(q['image'],q['instruction'])for q in live]==observed,'All391 actual live instructions retained without forged contiguous primary')
 need(out[r+'/V1-negative-binder.json']['V1_one_actual_MASM']=='FAILED_STRICT_WARNINGS_NO_BODY_COMPARISON'and out[r+'/V2-negative-binder.json']['actual_CODE']==1166 and out[r+'/V2-negative-binder.json']['prior_actual_MASM_calls']==2,'Three genuine MASM controls and earlier negatives remain qualified')

def _evidence(project,key):
 s=spec(key);out={}
 for name,h in EVIDENCE_PINS[key].items():
  path=(Path(project)/name).resolve();need(path.is_relative_to(Path(project).resolve()),'Owned comparison path');raw=path.read_bytes();need(H(raw)==h,'Owned closed near-game evidence '+name);out[name]=json.loads(raw)
 r=s['evidence_root'];primary=out[r+'/primary.json'];body=primary['normalized_result']['procedure']['body'];p=primary['analysis_profile']['parameters']
 if key in('reset_position08de_1168','reset_position08de_kind_map_1168'):_reset_physical_evidence(s,primary,body,p,out,r)
 else:
  need(primary['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode'and body['ranges']==[{'start':hex(0x10000+s['base']),'end':hex(0x10000+s['base']+s['size']-1)}]and body['total_bytes']==s['size']and not body['non_contiguous'],'Complete native whole procedure')
 g=out[r+'/generation.json'];outer=out[r+'/outer.json'];c=out[r+'/comparison.json'];t=out[r+'/comparison-terminal.json']
 need(g['status']=='COMPLETE'and g['error']is None and g['guard_closed']and g['actual_MASM_calls']==1 and g['source_sha256']==s['source_sha256']and g['raw_whole_object_sha256']==s['object_sha256']and len(g['calls'])==1 and g['calls'][0]['pid']>0 and g['calls'][0]['terminal']and g['calls'][0]['reaped']and g['calls'][0]['returncode']==0 and len(g['blocked_probes'])==20 and g['source_tools_new_scratch_only'],'Closed genuine source-only generation')
 need(outer['terminal']and outer['reaped']and outer['exit_code']==0 and outer['raw_whole_object_sha256']==s['object_sha256']and outer['generation_receipt_sha256']==H((Path(project)/r/'generation.json').read_bytes()),'Actual outer source terminal')
 need(c['status']==s['comparison_status']and c[s['comparison_object_key']]==s['object_sha256']and c[s.get('comparison_size_key','whole_CODE')]==s['size']and c['instructions']==s['instructions']and c['native_MZ']==s['native_MZ']and t['terminal']and t['reaped']and t['exit_code']==0 and (t['comparison_SHA256']if key=='reset_position08de_kind_map_1168'else t['comparison_sha256'])==H((Path(project)/r/'comparison.json').read_bytes()),'Exact closed whole native comparison')
 ledger=out[r+'/instruction-ledger.json'];need(len(ledger)==s['instructions']and sum(q['size']for q in ledger)==s['size']and H(b''.join(bytes.fromhex(q['native_hex'])for q in ledger))==s['native_sha256'],'Complete native instruction boundaries/bytes')
 return out

def _sites(s,original_sites):
 actual=sorted(p for p in original_sites if max(s['base'],p)<min(s['base']+s['size'],p+2));need(actual==s['native_MZ'],'Complete native MZ including boundary-crossing words');return actual

def validate_evidence(u,project,target_sha256,reference=None):
 validate_unit(u);s=spec(u['object_profile']);need(target_sha256==ORIGINAL_SHA256 and reference is not None and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']>=s['base']+s['size'],'Native source/carrier provenance');out=_evidence(project,u['object_profile']);_sites(s,reference['relocations']);need(H(reference['image'][s['base']:s['base']+s['size']])==s['native_sha256'],'Whole original native allocation')
 return out[s['evidence_root']+'/primary.json']['evidence_id']

def validate_comparison(u,built,image,project,original_sites):
 validate_unit(u);key=u['object_profile'];s=spec(key);code,meta=extract_code(built.object_bytes,key);need(code==built.code and meta==built.metadata and built.provenance['source_sha256']==s['source_sha256']and built.provenance['assembler_sha256']==TOOL_PINS['toolchains/msc510/MASM.EXE']and type(built.provenance.get('subprocess_pid'))is int and built.provenance['subprocess_pid']>0 and built.provenance['subprocess_terminal_reaped']and built.provenance['subprocess_returncode']==0,'Fresh unmodified whole-object/source/process provenance');out=_evidence(project,key);sites=_sites(s,original_sites);linked,logs=link_code(built.object_bytes,key);need(linked==image[s['base']:s['base']+s['size']]and H(linked)==s['native_sha256'],'Every complete native byte');loads=[]
 for base in[0,1,4096,65535]:
  actual,_=link_code(built.object_bytes,key,base);expected=bytearray(image[s['base']:s['base']+s['size']])
  for at in sites:
   p=at-s['base'];expected[p:p+2]=((int.from_bytes(expected[p:p+2],'little')+base)&65535).to_bytes(2,'little')
  need(actual==expected,'Full allocation/four load bases');loads.append({'load_paragraph':base,'whole_equal':True,'native_MZ_sites':sites})
 return linked,{'whole_allocation_image_offset':s['base'],'whole_allocation_size':s['size'],'whole_allocation_sha256':H(linked),'whole_bytes_equal':True,'whole_original_mz_sites':sites,'emitted_mz_sites':sites,'relocations':logs,'four_load_bases':loads,'native_evidence_id':out[s['evidence_root']+'/primary.json']['evidence_id'],'source_instructions':s['instructions'],'actual_external_fields':len(s['external_fields']),'actual_internal_fields':len(s['internal_fields']),'classification':'authored_near_game_CODE_component','authored_c_function_credit':0,'authored_asm_function_credit':0,'DATA_byte_credit':0,'historical_language_TU_or_C_unrepresentability_proven':False,'original_absolute_placement_proven':False}
