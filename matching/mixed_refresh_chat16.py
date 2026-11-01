"""Exact mixed C123/authored-ASM161 route. Neither legacy whole-object gate changes."""
from pathlib import Path
import json,hashlib,dataclasses
from dataclasses import dataclass
from omf import read_omf,OMFError
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256
import mixed_refresh_chat_generation16 as generation
from mixed_refresh_chat_source16 import C_SOURCE_SHA256,CHAT_SOURCE_SHA256,TRANSFORM
BACKEND=generation.BACKEND;KIND=generation.KIND
PROFILE_SHA256='8e00f7b3620d1c2cd7846df3f5028d41a988b02a26542dddfa543373c770fc10'
EVIDENCE_PINS_SHA256='7cf23dd2ce098e8ccda19ebe47be99fd9a2d87daa13171af74624e93ef0a3018'
H=lambda b:hashlib.sha256(b).hexdigest()
class MixedError(OMFError):pass
def need(v,m):
 if not v:raise MixedError(m)
def profile():
 b=Path(__file__).with_name('mixed_refresh_chat_profile.json').read_bytes();need(H(b)==PROFILE_SHA256,'Exact comparison-only mixed profile');return json.loads(b)
def validate_unit(u):
 p=profile();need(u['id']in p['units']and u==p['units'][u['id']],'Exact one of two mixed-owner unit contracts')
def _structural(b):
 p=profile()
 for key,raw in [('mixed',b.object_bytes),('c5',b.c5_sidecar_bytes),('fa',b.fresh_fa_bytes),('composed',b.mixed_source_bytes)]:need(H(raw)==p['comparison_only_expected_SHA256'][key],'Whole fresh '+key+' identity')
 r=b.provenance;need(r['status']=='COMPLETE'and r['guard_closed']and r['source_tools_freshscratch_only']and r['native_original_oldOBJ_profile_inside_GEN']is False,'Fresh dual-phase GEN provenance')
 need([x['phase']for x in r['processes']]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 and type(x['pid'])is int and x['pid']>0 for x in r['processes']),'Two actual successful reaped processes')
 need(len(r['guard']['blocked'])==20 and len({x['path']for x in r['guard']['blocked']})==5 and r['guard']['FIFO'],'Active source-only capabilities and PIPE checks')
 need(r['raw_mixed_SHA256']==H(b.object_bytes)and r['C5_sidecar_SHA256']==H(b.c5_sidecar_bytes)and r['fresh_FA_SHA256']==H(b.fresh_fa_bytes)and r['mixed_ASM_SHA256']==H(b.mixed_source_bytes),'Exact fresh output roles')
 o=read_omf(b.object_bytes);side=read_omf(b.c5_sidecar_bytes);info=side.function_info('_refresh_1446');need(info['boundary']=='codeview3_procedure'and info['size']==123,'Authentic C5 CV123 sidecar')
 need([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',284,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72)],'Whole mixed CODE and empty real DATA classes')
 need(set(o.publics)=={'_refresh_1446','_type_chat_14c1'}and o.publics['_refresh_1446'].offset==0 and o.publics['_type_chat_14c1'].offset==123 and not o.procedures,'Two real PUBLICs; no invented MASM CV')
 code=bytearray()
 for at,v in o.segments[1].chunks:need(at==len(code)and v,'No CODE gap/overlap');code.extend(v)
 need(len(code)==284 and len(o.fixups)==len(p['expected_fields'])==26,'Whole284/all26 fields')
 for q,e in zip(o.fixups,p['expected_fields']):
  near=not q.segment_relative;need(q.segment==1 and q.width==2 and q.location_type==1 and q.target[0]==2 and q.frame==((0,1)if near else(2,q.target[1])),'Exact actual mixed field/frame grammar')
  need((q.offset,o.externals[q.target[1]],int.from_bytes(code[q.offset:q.offset+2],'little')+(q.displacement or 0))==(e['module_offset'],e['symbol'],e['addend']),'Exact field identity/addend/position')
 return o,side,info,bytes(code)
def assemble(source,project):
 # Generator receives real source paths/tools only. Comparison profile is read
 # strictly after both child phases and the generation capability scope close.
 b=generation.assemble(source,project);_structural(b);return b

def linked_whole(b,reference):
 o,side,info,raw=_structural(b);p=profile();need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']>=0x1562,'Exact native context')
 need(not[x for x in reference['relocations']if 0x1445<=x<0x1562],'Complete empty native MZ interval')
 loads=[];logs=[]
 for base in [0,1,4096,65535]:
  out=bytearray(raw);entries=[]
  for q,e in zip(o.fixups,p['expected_fields']):
   value=(p['bindings'][e['symbol']]+e['addend']-(0x1446+q.offset+2 if not q.segment_relative else 0))&65535;out[q.offset:q.offset+2]=value.to_bytes(2,'little');entries.append({'field':q.offset,'symbol':e['symbol'],'frame':list(q.frame),'target':list(q.target),'displacement':q.displacement,'addend':e['addend'],'encoded':value})
  need(bytes(out)==reference['image'][0x1446:0x1562],'Every complete mixed native byte at four bases');loads.append({'load_paragraph':base,'whole_equal':True,'native_MZ':[]})
  if base==0:code=bytes(out);logs=entries
 c,rel=link_function(side,'_refresh_1446',0x1446,p['original_units']['refresh_1446']['externals'],image_origin=0x1446)
 need(c==code[:123]and len(c)==123,'Genuine C5 sidecar comparison agrees with final mixed C body')
 proof={'whole_image_offset':0x1446,'whole_CODE_bytes':284,'whole_SHA256':H(code),'whole_native_equal':True,'all26fields':logs,'four_bases':loads,'native_MZ':[],'C123_compiler_produced':True,'ASM161_authored':True,'C5_sidecar_not_SOURCE':True,'historical_TU_proven':False}
 return code,proof,info,rel

def validate_evidence(u,project,target_sha256,reference):
 validate_unit(u);need(target_sha256==ORIGINAL_SHA256,'Original target identity')
 if u['language']=='asm-code':
  import input_dialog_code16
  # Reuse the unchanged original complete native/ABI gate on its exact original
  # descriptor; this changes metadata routing, never bytes or PUBLIC identities.
  return input_dialog_code16.validate_evidence(profile()['original_units'][u['id']],project,target_sha256,reference)
 raise MixedError('C owner continues through unchanged generic C REA extent gate')
_CACHE_CAP=object()
@dataclass(frozen=True)
class _FreshEntry:
 cap:object
 cache_id:int
 built:object
def validate_certificate(project):
 data=Path(__file__).with_name('mixed_refresh_chat_evidence_pins.json').read_bytes();need(H(data)==EVIDENCE_PINS_SHA256,'Owned source-calibration pins');pins=json.loads(data);root=Path(project)/pins['root'];out={}
 for name,h in pins['files'].items():
  b=(root/name).read_bytes();need(H(b)==h,'Owned mixed certificate '+name);out[name]=json.loads(b)
 g=out['generation.json'];t=out['generation-terminal.json'];c=out['comparison.json'];ct=out['comparison-terminal.json']
 need(g['status']=='COMPLETE'and g['source_SHA256']==C_SOURCE_SHA256 and g['authored_ASM_SHA256']==CHAT_SOURCE_SHA256 and [x['phase']for x in g['processes']]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 for x in g['processes']),'Actual dual-source generation calibration')
 need(t['terminal']and t['reaped']and t['exit_code']==0 and t['C5_calls']==t['MASM_calls']==1 and t['generation_receipt_SHA256']==pins['files']['generation.json'],'Actual outer GEN calibration closure')
 need(ct['terminal']and ct['reaped']and ct['exit_code']==0 and ct['comparison_SHA256']==pins['files']['comparison.json']and c['status']=='PASS_FRESH_MIXED_PROTOTYPE_NOT_ADMISSION'and c['CODE284']and c['PUBLIC0_123']and c['C5_CV_size123']and c['all4bases']and len(c['all26_actual_fields'])==26 and c['native_MZ']==[],'Complete native/type/calibration comparison')
 need(c['mixed_SHA256']==profile()['comparison_only_expected_SHA256']['mixed']and c['C5_sidecar_SHA256']==profile()['comparison_only_expected_SHA256']['c5'],'Actual calibrated raw roles')
 return {'calibration_only_not_fresh_witness':True,'all4bases':True,'C5_CV123':True,'mixed_CODE284':True}
def _cache_key(project):
 project=Path(project);p=profile();tools=json.loads((project/'config/msc500.json').read_text())['files'];paths=[project/generation.C_SOURCE,project/generation.ASM_SOURCE,Path(generation.__file__),Path(__file__).with_name('mixed_refresh_chat_source16.py'),project/'config/msc500.json',project/'config/msc510.json',project/'toolchains/msc500/manifest.json',project/'toolchains/msc510/MASM.EXE',project/'toolchains/msc510/manifest.json',project/'toolchains/msc510/LICENSE',Path('/usr/bin/dosbox').resolve(),Path(__file__).with_name('mixed_refresh_chat_profile.json')]+[project/'toolchains/msc500'/r['name']for r in tools]
 return(KIND,TRANSFORM,tuple((str(x.resolve()),H(x.read_bytes()))for x in paths),('/AS','/Zi','/FaC:\\UNIT.ASM'),('/Mx',),'UNIT.C','UNIT.ASM')
def build_unit(u,image,project,cache,output,reference):
 validate_unit(u);certificate=validate_certificate(project);need(type(cache)is dict,'Current-run checker cache required');key=_cache_key(project)
 if key not in cache:cache[key]=_FreshEntry(_CACHE_CAP,id(cache),assemble((Path(project)/generation.C_SOURCE).resolve(),project))
 entry=cache[key];need(type(entry)is _FreshEntry and entry.cap is _CACHE_CAP and entry.cache_id==id(cache),'Same current-run mixed cache factory; no fixture Build injection');b=entry.built;code,proof,info,c_relocations=linked_whole(b,reference);isc=u['language']=='c';actual=code[:123]if isc else code[123:];start=int(u['image_offset'],0);expected=image[start:start+u['size']];need(actual==expected and len(actual)==u['size'],'Complete owner-native match')
 asm_relocations=[dict(x,field_image_offset=0x1446+x['field'],unit_offset=x['field']-123)for x in proof['all26fields']if x['field']>=123]
 r=dict(u);r['mixed_source_calibration']=certificate;r.update(status='c_matched'if isc else'asm_code_matched',expected_size=len(expected),actual_size=len(actual),expected_sha256=H(expected),actual_sha256=H(actual),first_difference=None,expected_byte=None,actual_byte=None,source_sha256=C_SOURCE_SHA256 if isc else CHAT_SOURCE_SHA256,object_sha256=H(b.object_bytes),relocations=c_relocations if isc else asm_relocations,mixed_object_proof=proof,mixed_profile='refresh_chat284_v1',classification='compiler_produced_C_in_mixed_module'if isc else'authored_ASM_in_mixed_module',comparison_object_role='genuine_C5_typed_sidecar'if isc else'final_mixed_span123_284',compiler='Microsoft C 5.00'if isc else None,compiler_flags=['/AS','/Zi']if isc else[],build_command=[x['command']for x in b.provenance['processes']],mixed_generation_provenance=b.provenance,authored_c_function_credit=0 if not isc else 1,authored_asm_function_credit=0)
 if isc:r.update(emitted_procedure={k:v for k,v in info.items()if k!='fixups'},emitted_procedure_object_role='genuine_C5_sidecar_not_game_SOURCE',comparison_object_sha256=H(b.c5_sidecar_bytes),compiler_tool_hashes=b.provenance['tool_hashes'],toolchain_manifest_sha256=b.provenance['compiler_manifest_SHA256'])
 else:r.update(complete_code_allocation={'whole_object_CODE_bytes':284,'owner_offset':123,'owner_bytes':161},complete_allocation_proof={'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':asm_relocations})
 if output is not None:
  directory=Path(output)/'mixed-source';directory.mkdir(parents=True,exist_ok=True);artifact=directory/'refresh-chat.obj';side=Path(output)/'typed-sidecars'/'refresh-chat';side.mkdir(parents=True,exist_ok=True)
  for path,content in [(artifact,b.object_bytes),(side/'C5.obj',b.c5_sidecar_bytes),(side/'compiler-FA.asm',b.fresh_fa_bytes),(side/'composed.asm',b.mixed_source_bytes)]:
   if path.exists():need(path.read_bytes()==content,'Same current-run output role reused unchanged')
   else:path.write_bytes(content)
  receipt=side/'generation-receipt.json';encoded=(json.dumps(b.provenance,indent=2)+'\n').encode()
  if receipt.exists():need(receipt.read_bytes()==encoded,'Same generation receipt')
  else:receipt.write_bytes(encoded)
  for name,content in b.artifacts.items():
   if Path(name).suffix.lower()in('.obj','.asm','.c'):continue
   path=side/'generation-logs'/name;path.parent.mkdir(parents=True,exist_ok=True)
   if path.exists():need(path.read_bytes()==content,'Same retained genuine log')
   else:path.write_bytes(content)
  r['object_artifact']=str(artifact.resolve())
  if isc:r['comparison_object_artifact']=str((side/'C5.obj').resolve())
 return r
