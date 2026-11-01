"""Strict genuine C455+C328 and authored ASM187 source-composed whole970."""
from pathlib import Path
from dataclasses import dataclass
import json,hashlib,dataclasses,collections
from omf import read_omf,OMFError
from library16 import link_segment
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256
import mixed_motion_special_generation16 as generation
from mixed_motion_special_source16 import C_SOURCE_SHA256,DECODER_SOURCE_SHA256,TRANSFORM
BACKEND=generation.BACKEND;KIND=generation.KIND
PROFILE_SHA256='39c47543da8fc0bee666f3d3d3a581ffe437038bf4c366709b6187007fb2da04';PINS_SHA256='dbefcf3adc691a5218fbe54c3a3aaff147921ff9cbb28edcd4269882a32261ed';H=lambda b:hashlib.sha256(b).hexdigest()
class MixedError(OMFError):pass
def need(v,m):
 if not v:raise MixedError(m)
def safe(x):
 if dataclasses.is_dataclass(x):return safe(dataclasses.asdict(x))
 if isinstance(x,bytes):return x.hex()
 if isinstance(x,dict):return{str(k):safe(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return[safe(v)for v in x]
 return x
def snapshot(o):return{'names':o.names,'segments':[safe(s)for s in o.segments.values()],'publics':safe(o.publics),'externals':[[k,v]for k,v in o.externals.items()],'procedures':safe(o.procedures),'fixups':[safe(f)for f in o.fixups],'records':[[k,a,p.hex()]for k,a,p in o.records]}
def profile():
 raw=Path(__file__).with_name('mixed_motion_special_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'closed whole comparison profile');return json.loads(raw)
def validate_unit(u):
 p=profile();need(u.get('id')in p['units']and u==p['units'][u['id']],'one exact three-owner contract')
def _structural(b):
 p=profile()
 for key,raw in [('mixed',b.object_bytes),('c5',b.c5_sidecar_bytes),('fa',b.fresh_fa_bytes),('composed',b.mixed_source_bytes)]:need(type(raw)is bytes and H(raw)==p['comparison_only_expected_SHA256'][key],'whole actual output '+key)
 r=b.provenance;need(r['status']=='COMPLETE'and r['guard_closed']and r['source_tools_freshscratch_only']and r['native_original_oldOBJ_profile_inside_GEN']is False,'closed actual source-only generation')
 need(r['source_SHA256']==C_SOURCE_SHA256 and r['authored_ASM_SHA256']==DECODER_SOURCE_SHA256 and r['flags']==['/AS','/Zi']and r['listing_flag']=='/FaC:\\UNIT.ASM'and r['MASM_flags']==['/Mx'],'real source/flags/basenames')
 need([x['phase']for x in r['processes']]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 and type(x['pid'])is int and x['pid']>0 for x in r['processes'])and len({x['pid']for x in r['processes']})==2,'exact two actual reaped processes')
 need(len(r['guard']['blocked'])==20 and len({x['path']for x in r['guard']['blocked']})==5 and r['guard']['FIFO'],'real GEN denials/FIFO')
 for key,value in [('raw_mixed_SHA256',b.object_bytes),('C5_sidecar_SHA256',b.c5_sidecar_bytes),('fresh_FA_SHA256',b.fresh_fa_bytes),('mixed_ASM_SHA256',b.mixed_source_bytes)]:need(r[key]==H(value),'same current output receipt')
 from mixed_motion_special_source16 import compose_fresh
 composed,transform=compose_fresh(b.fresh_fa_bytes,(Path(__file__).parent/generation.ASM_SOURCE).read_bytes(),c_source_sha256=C_SOURCE_SHA256)
 need(composed==b.mixed_source_bytes and transform==r['transform']==p['source_transform'],'full source inverse and exact current-call composition')
 o=read_omf(b.object_bytes);c=read_omf(b.c5_sidecar_bytes);need(snapshot(o)==p['whole_mixed_snapshot']and snapshot(c)==p['whole_C5_snapshot'],'complete OMF/raw records/CV/TYPE views; no parsed mutation')
 info={}
 for key,v in p['C_extent_contracts'].items():
  i=c.function_info(v['symbol']);need(i['boundary']=='codeview3_procedure'and(i['offset'],i['size'],i['end'])==(v['offset'],v['size'],v['offset']+v['size']),'genuine complete C5 CV455/328');info[key]=i
 need(c.segments[1].length==784,'whole genuine C5 CODE784 sidecar/terminal90 retained')
 need([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',970,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72)]and not o.procedures,'whole mixed970 and exactly empty DATA/CONST/BSS')
 need(all(not s.chunks and not s.unsupported_data for s in o.segments.values()if s.index!=1),'no hidden storage')
 need(set(o.publics)==set(p['PUBLICs'])and all((o.publics[n].segment,o.publics[n].group,o.publics[n].offset,o.publics[n].type_index)==(1,0,at,0)for n,at in p['PUBLICs'].items()),'exact three near publics')
 code=bytearray()
 for at,raw in o.segments[1].chunks:need(at==len(code)and raw,'full contiguous code');code.extend(raw)
 need(len(code)==970 and len(o.fixups)==52,'whole970/all52fields')
 expected={x['offset']:x for x in p['actual_fields']};need(len(expected)==52 and len({q.offset for q in o.fixups})==52,'unique actual field join')
 counts=collections.Counter();last=-1
 for q in sorted(o.fixups,key=lambda f:f.offset):
  e=expected[q.offset];need(safe(q)=={k:v for k,v in e.items()if k in safe(q)},'exact raw typed field including record order/frame/index/displacement')
  need(q.segment==1 and q.width==2 and q.location_type==1 and q.offset>=last,'complete nonoverlapping fields');last=q.offset+2;effective=int.from_bytes(code[q.offset:q.offset+2],'little')+(q.displacement or 0);need(effective==e['effective_addend'],'combined source/displacement addend')
  if e['category']=='17_F0_external_nearCALL':need(q.target[0]==2 and q.frame==(0,1)and not q.segment_relative and o.externals[q.target[1]]==e['symbol']and code[q.offset-1]==0xe8,'exact seventeen genuine ASSUME-CS external CALLs')
  elif e['category']=='6_F0_internal_PC_relative':need(q.target==(0,1)and q.frame==(0,1)and not q.segment_relative and code[q.offset-1]in(0xe8,0xe9),'six genuine internal near branches')
  elif e['category']=='4_F1_group_DATA_WORD':need(q.frame==(1,1)and q.target[0]==2 and q.segment_relative and o.externals[q.target[1]]==e['symbol']=='_frame_lists','four real GROUP1 fields')
  else:need(e['category']=='25_F2_external_DATA_WORD'and q.target[0]==2 and q.frame==(2,q.target[1])and q.segment_relative and o.externals[q.target[1]]==e['symbol']in p['explicit_actual_F2_DATA_symbols'],'exact twenty-five real external DATA fields')
  counts[e['category']]+=1
 need(dict(counts)==p['field_categories'],'exact complete field category census')
 return o,c,info,bytes(code)
def assemble(source,project):
 b=generation.assemble(source,project);_structural(b);return b
def linked_whole(b,reference):
 o,c,info,raw=_structural(b);p=profile();origin=p['native_origin'];end=origin+970
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']>=end,'whole native unchanged prefix')
 need(not[x for x in reference['relocations']if x<end and x+2>origin],'complete empty native MZ span');native=reference['image'][origin:end];loads=[];logs=None;linked=None;near=set(p['own_CODE_external_calls'])
 for load in[0,1,4096,65535]:
  ds=(0x5cc2+load)&65535;segs={s.index:((load,origin)if s.index==1 else(ds,0))for s in o.segments.values()};ext={n:((load if n in near else ds),v)for n,v in p['bindings'].items()};value,log=link_segment(o,1,segs,{1:ds},ext);need(value==native and all(x['mz_relocation_image_offset']is None for x in log),'whole970 native/all52/fourbases/noMZ');loads.append({'load_paragraph':load,'whole_native_equal':True,'native_MZ':[]})
  # Independently link unchanged complete C5 sidecar, preserving all CVs and its uncredited EOF byte.
  csegs={s.index:((load,origin)if s.index==1 else(ds,0))for s in c.segments.values()};cvalue,_=link_segment(c,1,csegs,{1:ds},ext);need(cvalue[:783]==native[:783]and len(cvalue)==784,'genuine whole C5 C783 comparison and terminal byte retained')
  if load==0:linked=value;logs=log
 crel={}
 for key,v in p['C_extent_contracts'].items():
  at=origin+v['offset'];body,rel=link_function(c,v['symbol'],at,p['original_units'][key]['externals'],image_origin=at);need(body==linked[v['offset']:v['offset']+v['size']],'individual genuine C5 sidecar/CV/typed fields equal final real mixed span');crel[key]=rel
 return linked,{'whole_image_offset':origin,'whole_CODE_bytes':970,'whole_SHA256':H(linked),'whole_native_equal':True,'all52fields':logs,'four_bases':loads,'native_MZ':[],'C783_compiler_produced':True,'ASM187_authored':True,'C5_sidecar_not_SOURCE':True,'historical_TU_proven':False,'field_categories':p['field_categories']},info,crel
def validate_evidence(u,project,target_sha256,reference):
 validate_unit(u);need(target_sha256==ORIGINAL_SHA256,'native original identity')
 if u['language']=='asm-code':
  import special_task_code16
  return special_task_code16.validate_evidence(profile()['original_units'][u['id']],project,target_sha256,reference)
 raise MixedError('C owners retain generic exact native REA preflight and genuine typed sidecar comparison')
def validate_certificate(project):
 b=Path(__file__).with_name('mixed_motion_special_evidence_pins.json').read_bytes();need(H(b)==PINS_SHA256,'owned calibration closure');p=json.loads(b);r={}
 for n,h in p['files'].items():v=(Path(project)/p['root']/n).read_bytes();need(H(v)==h,'owned actual calibration '+n);r[n]=json.loads(v)
 g,t,c,ct=[r[n]for n in['generation.json','generation-terminal.json','comparison.json','comparison-terminal.json']]
 need(g['status']=='COMPLETE'and g['source_SHA256']==C_SOURCE_SHA256 and g['authored_ASM_SHA256']==DECODER_SOURCE_SHA256 and g['flags']==['/AS','/Zi'],'real calibrated source identities')
 need(t['terminal']and t['reaped']and t['exit_code']==0 and t['actual_C5_calls']==t['actual_MASM_calls']==1 and t['generation_receipt_SHA256']==p['files']['generation.json'],'actual outer GEN closure')
 need(ct['terminal']and ct['exit_code']==0 and ct['comparison_SHA256']==p['files']['comparison.json']and c['status']=='PASS_FRESH_MOTION783_SPECIAL187_MIXED970_PURE_CALIBRATION'and c['whole_CODE']==970 and c['raw_sha256']==profile()['comparison_only_expected_SHA256']['mixed']and len(c['fields'])==52 and not c['native_MZ'],'whole calibrated native970/all52 proof')
 return{'calibration_only_not_fresh_witness':True,'genuine_C5_CV':[455,328],'whole970_fourbases':True,'TYPEs_unchanged':True}
_CACHE_CAP=object()
@dataclass(frozen=True)
class _FreshEntry:
 cap:object
 cache_id:int
 built:object
def _cache_key(project):
 project=Path(project);tools=json.loads((project/'config/msc500.json').read_text())['files'];paths=[project/generation.C_SOURCE,project/generation.ASM_SOURCE,Path(generation.__file__),Path(__file__).with_name('mixed_motion_special_source16.py'),Path(__file__),Path(__file__).with_name('mixed_motion_special_profile.json'),project/'config/msc500.json',project/'config/msc510.json',project/'toolchains/msc500/manifest.json',project/'toolchains/msc510/MASM.EXE',project/'toolchains/msc510/manifest.json',project/'toolchains/msc510/LICENSE',Path('/usr/bin/dosbox').resolve()]+[project/'toolchains/msc500'/r['name']for r in tools];return(KIND,TRANSFORM,tuple((str(p.resolve()),H(p.read_bytes()))for p in paths),('/AS','/Zi','/FaC:\\UNIT.ASM'),('/Mx',),'UNIT.C','UNIT.ASM')
def build_unit(u,image,project,cache,output,reference):
 validate_unit(u);certificate=validate_certificate(project);need(type(cache)is dict,'current checker cache factory');key=_cache_key(project)
 if key not in cache:cache[key]=_FreshEntry(_CACHE_CAP,id(cache),assemble((Path(project)/generation.C_SOURCE).resolve(),project))
 entry=cache[key];need(type(entry)is _FreshEntry and entry.cap is _CACHE_CAP and entry.cache_id==id(cache),'same current-run factory/cache; never fixtures');b=entry.built;code,proof,info,cr=linked_whole(b,reference);p=profile();isc=u['language']=='c';start=int(u['image_offset'],0);off=start-p['native_origin'];actual=code[off:off+u['size']];need(actual==image[start:start+u['size']]and len(actual)==u['size'],'complete native owner span')
 ar=[dict(x,field_image_offset=x['image_offset'],unit_offset=x['object_offset']-783)for x in proof['all52fields']if x['object_offset']>=783];rel=cr[u['id']]if isc else ar;r=dict(u);r.update(status='c_matched'if isc else'asm_code_matched',expected_size=len(actual),actual_size=len(actual),expected_sha256=H(actual),actual_sha256=H(actual),first_difference=None,expected_byte=None,actual_byte=None,source_sha256=C_SOURCE_SHA256 if isc else DECODER_SOURCE_SHA256,object_sha256=H(b.object_bytes),relocations=rel,mixed_object_proof=proof,mixed_profile='motion_special970_v1',mixed_source_calibration=certificate,classification='compiler_produced_C_in_mixed_module'if isc else'authored_ASM_in_mixed_module',comparison_object_role='genuine_C5_typed_sidecar'if isc else'final_mixed_span783_970',compiler='Microsoft C 5.00'if isc else None,compiler_flags=['/AS','/Zi']if isc else[],build_command=[x['command']for x in b.provenance['processes']],mixed_generation_provenance=b.provenance,authored_c_function_credit=1 if isc else 0,authored_asm_function_credit=0)
 if isc:
  i=info[u['id']];r.update(emitted_procedure={k:v for k,v in i.items()if k!='fixups'},emitted_procedure_object_role='genuine_C5_sidecar_not_game_SOURCE',comparison_object_sha256=H(b.c5_sidecar_bytes),compiler_tool_hashes=b.provenance['tool_hashes'],toolchain_manifest_sha256=b.provenance['compiler_manifest_SHA256'])
  if u.get('extended_extent'):
   from extent import validate_extended_extent
   # Exact historical backend label is comparison metadata for the SAME unchanged real C source/sidecar, not the newly selected game object.
   r['extended_extent_proof']=validate_extended_extent(p['original_units'][u['id']],project,ORIGINAL_SHA256,i,actual,source_object=read_omf(b.c5_sidecar_bytes))
 else:r.update(complete_code_allocation={'whole_object_CODE_bytes':970,'owner_offset':783,'owner_bytes':187},complete_allocation_proof={'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':ar})
 if output is not None:
  directory=Path(output)/'mixed-source';directory.mkdir(parents=True,exist_ok=True);artifact=directory/'motion-special.obj';side=Path(output)/'typed-sidecars/motion-special';side.mkdir(parents=True,exist_ok=True)
  for path,content in[(artifact,b.object_bytes),(side/'C5.obj',b.c5_sidecar_bytes),(side/'compiler-FA.asm',b.fresh_fa_bytes),(side/'composed.asm',b.mixed_source_bytes),(side/'generation-receipt.json',(json.dumps(b.provenance,indent=2)+'\n').encode())]:
   if path.exists():need(path.read_bytes()==content,'same actual current-run artifact reused unchanged')
   else:path.write_bytes(content)
  for name,content in b.artifacts.items():
   if Path(name).suffix.lower()in('.obj','.asm','.c'):continue
   path=side/'generation-logs'/name;path.parent.mkdir(parents=True,exist_ok=True)
   if path.exists():need(path.read_bytes()==content,'same source log')
   else:path.write_bytes(content)
  r['object_artifact']=str(artifact.resolve())
  if isc:r['comparison_object_artifact']=str((side/'C5.obj').resolve())
 return r
