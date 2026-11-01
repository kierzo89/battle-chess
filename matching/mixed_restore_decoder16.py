"""Closed genuine C51/authored ASM289 whole-module mixed route, comparison separate."""
from pathlib import Path
import json,hashlib,dataclasses
from dataclasses import dataclass
from omf import read_omf,OMFError
from library16 import link_segment
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256
import mixed_restore_decoder_generation16 as generation
from mixed_restore_decoder_source16 import C_SOURCE_SHA256,DECODER_SOURCE_SHA256,TRANSFORM
BACKEND=generation.BACKEND;KIND=generation.KIND
PROFILE_SHA256='df9dd50461b136d7da89630111b2bdb703f6d31366f71e4bd9936199d977526f';PINS_SHA256='25a0ffbf96c310ab7f915c6797035ba66dbde36080a10ade5b2be76832424d25';H=lambda b:hashlib.sha256(b).hexdigest()
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
 b=Path(__file__).with_name('mixed_restore_decoder_profile.json').read_bytes();need(H(b)==PROFILE_SHA256,'exact closed comparison profile');return json.loads(b)
def validate_unit(u):
 p=profile();need(u['id']in p['units']and u==p['units'][u['id']],'one exact mixed340 owner contract')
def _structural(b):
 p=profile()
 for key,raw in [('mixed',b.object_bytes),('c5',b.c5_sidecar_bytes),('fa',b.fresh_fa_bytes),('composed',b.mixed_source_bytes)]:need(type(raw)is bytes and H(raw)==p['comparison_only_expected_SHA256'][key],'whole real output '+key)
 r=b.provenance;need(r['status']=='COMPLETE'and r['guard_closed']and r['source_tools_freshscratch_only']and r['native_original_oldOBJ_profile_inside_GEN']is False,'actual source-only generation receipt')
 need(r['source_SHA256']==C_SOURCE_SHA256 and r['authored_ASM_SHA256']==DECODER_SOURCE_SHA256 and r['flags']==['/AS','/Gs','/Os','/Zi']and r['listing_flag']=='/FaC:\\UNIT.ASM'and r['MASM_flags']==['/Mx'],'exact source identities/flags')
 need([x['phase']for x in r['processes']]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 and type(x['pid'])is int and x['pid']>0 for x in r['processes']),'exact two actual reaped source processes')
 need(len(r['guard']['blocked'])==20 and len({x['path']for x in r['guard']['blocked']})==5 and r['guard']['FIFO'],'20 real source-capability denials/FIFO')
 need(r['raw_mixed_SHA256']==H(b.object_bytes)and r['C5_sidecar_SHA256']==H(b.c5_sidecar_bytes)and r['fresh_FA_SHA256']==H(b.fresh_fa_bytes)and r['mixed_ASM_SHA256']==H(b.mixed_source_bytes),'same actual outputs in receipt')
 o=read_omf(b.object_bytes);side=read_omf(b.c5_sidecar_bytes);need(snapshot(o)==p['whole_mixed_snapshot']and snapshot(side)==p['whole_C5_snapshot'],'complete raw/decoded OMF/CV/TYPE/record order identity; no mutable cache view')
 info=side.function_info('_restore_active_arena');need(info['boundary']=='codeview3_procedure'and info['offset']==0 and info['size']==51 and side.segments[info['segment']].length==52,'genuine C5 CV51 and whole CODE52 sidecar/tail retained')
 need([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',340,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72)]and not o.procedures,'whole mixed CODE340/no inventedCV/no extra allocation')
 need(set(o.publics)==set(p['PUBLICs'])and all((o.publics[n].segment,o.publics[n].group,o.publics[n].offset,o.publics[n].type_index)==(1,0,off,0)for n,off in p['PUBLICs'].items()),'two genuine publics0/51 only')
 code=bytearray()
 for at,v in o.segments[1].chunks:need(at==len(code)and v,'whole contiguous mixed CODE');code.extend(v)
 need(len(code)==340 and len(o.fixups)==31,'whole CODE340/31 actual fixups')
 by={f.offset:f for f in o.fixups};expected={e['module_offset']:e for e in p['expected_fields']};need(len(by)==len(expected)==31 and set(by)==set(expected),'unique exact field offset join, preserve raw record order')
 prior=-1
 for off in sorted(by):
  q,e=by[off],expected[off];need(q.segment==1 and(q.offset,q.width,q.location_type,q.segment_relative)==(e['module_offset'],e['width'],e['location_type'],e['segment_relative'])and off>=prior,'all exact field widths/positions/nonoverlap');prior=off+q.width;add=int.from_bytes(code[off:off+q.width],'little')+(q.displacement or 0);need(add==e['effective_addend'],'exact combined raw/displacement addend')
  if e['kind']=='external':
   need(q.target[0]==2 and o.externals[q.target[1]]==e['symbol'],'exact real symbolic target')
   if off==241:
    need(e['symbol']=='_huff_decode_stream'and q.frame==(0,1)and q.target==(2,6)and not q.segment_relative and q.displacement is None and q.raw==bytes.fromhex('84f1060106')and code[off-1]==0xe8,'sole genuine ASSUME-CS nearCALL frame0; no frame fallback')
   else:need(q.frame==((1,1)if e['expected_frame']=='GROUP1'else(2,q.target[1])),'exact other30 frames')
  else:need(q.target==(0,1)and q.frame==(0,1)and not q.segment_relative,'true own CODE relative field')
 return o,side,info,bytes(code)
def assemble(source,project):
 b=generation.assemble(source,project);_structural(b);return b

def linked_whole(b,reference):
 o,side,info,raw=_structural(b);p=profile();need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']>=0x2e34,'native source context/unchanged prefix')
 need(not[x for x in reference['relocations']if x<0x2e34 and x+2>0x2ce0],'complete empty MZ span')
 native=reference['image'][0x2ce0:0x2e34];need(native[240:243]==bytes.fromhex('e8afb4')and(0x2ce0+243+int.from_bytes(native[241:243],'little',signed=True))&65535==p['bindings']['_huff_decode_stream']==0xe282,'sole F0 call real target/native instruction')
 loads=[];logs=None;code=None
 for load in[0,1,4096,65535]:
  ds=(0x5cc2+load)&65535;segs={s.index:((load,0x2ce0)if s.index==1 else(ds,0))for s in o.segments.values()};ext={n:((load if n=='_huff_decode_stream'else ds),v)for n,v in p['bindings'].items()};value,log=link_segment(o,1,segs,{1:ds},ext);need(value==native and all(x['mz_relocation_image_offset']is None for x in log),'all340 exact/native/all31/fourbases/noMZ');loads.append({'load_paragraph':load,'whole_native_equal':True,'native_MZ':[]})
  if load==0:code=value;logs=log
 c,cr=link_function(side,'_restore_active_arena',0x2ce0,p['original_units']['restore_active_arena_2ce0']['externals'],image_origin=0x2ce0);need(c==code[:51]and len(c)==51,'C51 genuine typed sidecar and final mixed span agree')
 proof={'whole_image_offset':0x2ce0,'whole_CODE_bytes':340,'whole_SHA256':H(code),'whole_native_equal':True,'all31fields':logs,'four_bases':loads,'native_MZ':[],'C51_compiler_produced':True,'ASM289_authored':True,'C5_sidecar_not_SOURCE':True,'historical_TU_proven':False,'one_exact_PC_relative_CODE_frame_transition':p['CODEframe0_exact']};return code,proof,info,cr

def validate_evidence(u,project,target_sha256,reference):
 validate_unit(u);need(target_sha256==ORIGINAL_SHA256,'native target identity')
 if u['language']=='asm-code':
  import near_game_code16
  return near_game_code16.validate_evidence(profile()['original_units'][u['id']],project,target_sha256,reference)
 raise MixedError('C owner retains the unchanged generic C REA extent gate')
def validate_certificate(project):
 data=Path(__file__).with_name('mixed_restore_decoder_evidence_pins.json').read_bytes();need(H(data)==PINS_SHA256,'owned comparison proof closure');p=json.loads(data);rows={}
 for n,h in p['files'].items():b=(Path(project)/p['root']/n).read_bytes();need(H(b)==h,'exact owned calibration '+n);rows[n]=json.loads(b)
 g,t,c,ct=[rows[n]for n in['generation.json','generation-terminal.json','comparison.json','comparison-terminal.json']];need(g['status']=='COMPLETE'and g['source_SHA256']==C_SOURCE_SHA256 and g['authored_ASM_SHA256']==DECODER_SOURCE_SHA256 and g['flags']==['/AS','/Gs','/Os','/Zi']and[x['phase']for x in g['processes']]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 for x in g['processes']),'real bounded calibration source processes')
 need(t['terminal']and t['reaped']and t['exit_code']==0 and t['C5_calls']==t['MASM_calls']==1 and t['generation_receipt_SHA256']==p['files']['generation.json'],'real calibration GEN terminal')
 need(ct['terminal']and ct['exit_code']==0 and ct['comparison_SHA256']==p['files']['comparison.json']and c['status']=='PASS_FRESH_RESTORE51_DECODER289_MIXED340_CALIBRATION_ONLY'and c['whole_CODE_bytes']==340 and c['raw_object_sha256']==profile()['comparison_only_expected_SHA256']['mixed']and len(c['all31_actual_fields'])==31 and len(c['four_load_bases'])==4 and not c['native_MZ'],'complete native calibrated comparison')
 return{'calibration_only_not_fresh_witness':True,'C5_CV51':True,'all340_native_fourbases':True,'TYPEs_unchanged':True}
_CACHE_CAP=object()
@dataclass(frozen=True)
class _FreshEntry:
 cap:object
 cache_id:int
 built:object
def _cache_key(project):
 project=Path(project);tools=json.loads((project/'config/msc500.json').read_text())['files'];paths=[project/generation.C_SOURCE,project/generation.ASM_SOURCE,Path(generation.__file__),Path(__file__).with_name('mixed_restore_decoder_source16.py'),Path(__file__),Path(__file__).with_name('mixed_restore_decoder_profile.json'),project/'config/msc500.json',project/'config/msc510.json',project/'toolchains/msc500/manifest.json',project/'toolchains/msc510/MASM.EXE',project/'toolchains/msc510/manifest.json',project/'toolchains/msc510/LICENSE',Path('/usr/bin/dosbox').resolve()]+[project/'toolchains/msc500'/r['name']for r in tools];return(KIND,TRANSFORM,tuple((str(x.resolve()),H(x.read_bytes()))for x in paths),('/AS','/Gs','/Os','/Zi','/FaC:\\UNIT.ASM'),('/Mx',),'UNIT.C','UNIT.ASM')
def build_unit(u,image,project,cache,output,reference):
 validate_unit(u);certificate=validate_certificate(project);need(type(cache)is dict,'current checker cache factory');key=_cache_key(project)
 if key not in cache:cache[key]=_FreshEntry(_CACHE_CAP,id(cache),assemble((Path(project)/generation.C_SOURCE).resolve(),project))
 entry=cache[key];need(type(entry)is _FreshEntry and entry.cap is _CACHE_CAP and entry.cache_id==id(cache),'same current-run factory/cache, never fixture output');b=entry.built;code,proof,info,cr=linked_whole(b,reference);isc=u['language']=='c';actual=code[:51]if isc else code[51:];start=int(u['image_offset'],0);need(actual==image[start:start+u['size']]and len(actual)==u['size'],'complete owner native match')
 ar=[dict(x,field_image_offset=x['image_offset'],unit_offset=x['object_offset']-51)for x in proof['all31fields']if x['object_offset']>=51];r=dict(u);r.update(status='c_matched'if isc else'asm_code_matched',expected_size=len(actual),actual_size=len(actual),expected_sha256=H(actual),actual_sha256=H(actual),first_difference=None,expected_byte=None,actual_byte=None,source_sha256=C_SOURCE_SHA256 if isc else DECODER_SOURCE_SHA256,object_sha256=H(b.object_bytes),relocations=cr if isc else ar,mixed_object_proof=proof,mixed_profile='restore_decoder340_v1',mixed_source_calibration=certificate,classification='compiler_produced_C_in_mixed_module'if isc else'authored_ASM_in_mixed_module',comparison_object_role='genuine_C5_typed_sidecar'if isc else'final_mixed_span51_340',compiler='Microsoft C 5.00'if isc else None,compiler_flags=['/AS','/Gs','/Os','/Zi']if isc else[],build_command=[x['command']for x in b.provenance['processes']],mixed_generation_provenance=b.provenance,authored_c_function_credit=1 if isc else 0,authored_asm_function_credit=0)
 if isc:r.update(emitted_procedure={k:v for k,v in info.items()if k!='fixups'},emitted_procedure_object_role='genuine_C5_sidecar_not_game_SOURCE',comparison_object_sha256=H(b.c5_sidecar_bytes),compiler_tool_hashes=b.provenance['tool_hashes'],toolchain_manifest_sha256=b.provenance['compiler_manifest_SHA256'])
 else:r.update(complete_code_allocation={'whole_object_CODE_bytes':340,'owner_offset':51,'owner_bytes':289},complete_allocation_proof={'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':ar})
 if output is not None:
  directory=Path(output)/'mixed-source';directory.mkdir(parents=True,exist_ok=True);artifact=directory/'restore-decoder.obj';side=Path(output)/'typed-sidecars/restore-decoder';side.mkdir(parents=True,exist_ok=True)
  for path,content in[(artifact,b.object_bytes),(side/'C5.obj',b.c5_sidecar_bytes),(side/'compiler-FA.asm',b.fresh_fa_bytes),(side/'composed.asm',b.mixed_source_bytes),(side/'generation-receipt.json',(json.dumps(b.provenance,indent=2)+'\n').encode())]:
   if path.exists():need(path.read_bytes()==content,'same current-run artifact reused unchanged')
   else:path.write_bytes(content)
  for name,content in b.artifacts.items():
   if Path(name).suffix.lower()in('.obj','.asm','.c'):continue
   path=side/'generation-logs'/name;path.parent.mkdir(parents=True,exist_ok=True)
   if path.exists():need(path.read_bytes()==content,'same actual source log')
   else:path.write_bytes(content)
  r['object_artifact']=str(artifact.resolve())
  if isc:r['comparison_object_artifact']=str((side/'C5.obj').resolve())
 return r
