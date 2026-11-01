"""Closed history CODE340 / anonymous literal CONST17 ownership. No generator."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from omf import OMFError,OMFObject,read_omf
from library16 import link_segment
from reference import validate_data_address,validate_expanded_read
KIND='history_input_literal17_340_v1';BACKEND='msc500-history-literal-const-omf';SOURCE='src/history_input_literal_match.c';FLAGS=['/AS','/Zi']
SOURCE_SHA256='defb66971dec96e0e745d637034b4c71d53d7ccf78c3b7e34d17bc1ad246ffd5';OBJECT_SHA256='94c9209ca131326a9f65c1f47b0353439afc1e92acf88aa4c79005270bb6fa78'
PROFILE_SHA256='53bc55f7c1f19e178ca74d65ba368440c1adc5a8d21a87b0b729908ab2550cdf'
class HistoryLiteralError(OMFError):pass
def require(ok,message):
 if not ok:raise HistoryLiteralError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):
 def view(v):
  if isinstance(v,dict):
   require(all(type(k)in(int,str)for k in v),'history snapshot key type');require(len({str(k)for k in v})==len(v),'history snapshot key collision');return {str(k):view(y)for k,y in v.items()}
  if isinstance(v,(tuple,list)):return [view(y)for y in v]
  return v
 return json.dumps(view(x),sort_keys=True,separators=(',',':'))
def snapshot(obj):
 return {'records':[{'kind':k,'offset':a,'payload_hex':b.hex()}for k,a,b in obj.records],'names':obj.names,'externals':obj.externals,'publics':{k:asdict(v)for k,v in obj.publics.items()},'procedures':obj.procedures,'data_writes':obj.data_writes,'segments':{i:{**{k:v for k,v in asdict(s).items()if k!='chunks'},'chunks':[[a,b.hex()]for a,b in s.chunks]}for i,s in obj.segments.items()},'fixups':[{**asdict(f),'raw':f.raw.hex()}for f in obj.fixups]}
def profile():
 raw=Path(__file__).with_name('history_input_literal17_profile.json').read_bytes();require(sha(raw)==PROFILE_SHA256,'history profile pin');return json.loads(raw)
def validate_unit(unit):
 p=profile();expected=p['unit_contracts'].get(unit.get('id'));require(expected is not None and canonical(unit)==canonical(expected),'history exact source/unit/ownership contract');return expected
def validate_unit_metadata(unit):
 validate_unit(unit);require(unit['id']=='accept_input_baaf'and unit['owned_const_profile']==KIND,'history literal actual referencing C owner');return dict(profile()['descriptor'])
def full(obj,segment):
 s=obj.segments[segment];require(not s.unsupported_data,'history unsupported/iterated data');b=bytearray()
 for at,x in sorted(s.chunks):require(at==len(b)and bool(x),'history complete allocation hole/overlap');b.extend(x)
 require(len(b)==s.length,'history incomplete allocation tail');return bytes(b)
def validate_object(obj):
 require(isinstance(obj,OMFObject),'history strict OMF object');p=profile();require(canonical(snapshot(obj))==canonical(p['object_snapshot']),'history complete raw/parsed/TYPE/CV/77field fingerprint')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in obj.segments.values()]==[(1,'_TEXT','CODE',340,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',17,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',355,32),(6,'$$TYPES','DEBTYP',321,32)],'history complete segment allocation')
 require(len(obj.fixups)==77 and len([f for f in obj.fixups if f.segment==1])==58 and len([f for f in obj.fixups if f.segment==5])==19,'history complete typedfield inventory')
 require(set(obj.publics)==set(p['procedures'])and set(obj.procedures)==set(p['procedures']),'history whole fourCV/PUBLIC boundary')
 for n,expected in p['procedures'].items():require(canonical({k:v for k,v in obj.function_info(n).items()if k!='fixups'})==canonical(expected),'history real independent CV boundary')
 require(len(full(obj,1))==340 and full(obj,3)==b'Jay was wrong #1\0'and not any(f.segment==3 for f in obj.fixups),'history whole native literal no fixups')
 f=next(f for f in obj.fixups if f.segment==1 and f.offset==311);require((f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.raw)==(2,1,True,(1,1),(0,3),None,bytes.fromhex('c4429c')),'history sole real ownCONST GROUP1 reference')
 require('_input_message'not in obj.externals.values()and not any(f.target==(0,0)for f in obj.fixups),'history unsupported SEG0 or fabricated external alias')
 return p

def validate_compiled(unit,compiled,project):
 validate_unit(unit);root=Path(project).resolve();path=(root/SOURCE).resolve();require(path.is_relative_to(root)and sha(path.read_bytes())==SOURCE_SHA256,'history genuine source identity')
 require(compiled.source_sha256==SOURCE_SHA256 and compiled.compiler=='msc500'and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'and compiled.toolchain_manifest_sha256==profile()['toolchain_manifest_sha256'],'history exact genuine compiler configuration')
 require(sha(compiled.object_bytes)==OBJECT_SHA256,'history whole freshly compiled OMF identity');validate_object(read_omf(compiled.object_bytes));return {'whole_CODE':340,'whole_CONST':17,'all_raw_fields':77,'real_CV_procedures':4,'real_CV_bytes':339,'literal_array_bits':136,'literal_element_builtin':0x80,'same_raw_source_cohort_required':True,'credit_delta':0}
def validate_layout(unit,obj):
 desc=validate_unit_metadata(unit);validate_object(obj);return desc,full(obj,3),[(311,0)]
def _evidence(project,p):
 root=Path(project).resolve();out={}
 for key,row in p['evidence'].items():
  relative=Path(row['path']);path=(root/relative).resolve();require(not relative.is_absolute()and path.is_relative_to(root),'history evidence escape');raw=path.read_bytes();require(sha(raw)==row['sha256'],'history evidence/source proof pin');out[key]=json.loads(raw)
 g=out['generation'];t=out['terminal'];ct=out['comparison_terminal'];c=out['comparison']
 require(g['status']=='COMPLETE'and g['guard_closed']and g['actual_C5_calls']==1 and g['source_tools_new_scratch_only']and not g['native_original_oldOBJ_comparison_inputs_inside_GEN']and len(g['blocked_probes'])==20 and g['raw_whole_object_sha256']==OBJECT_SHA256 and g['source_sha256']==SOURCE_SHA256,'history retained genuine source calibration')
 require(t['terminal']and t['reaped']and t['exit_code']==0 and t['actual_C5_calls']==1 and t['generation_receipt_SHA256']==p['evidence']['generation']['sha256'],'history retained producer terminal')
 require(ct['terminal']and ct['exit_code']==0 and ct['comparison_SHA256']==p['evidence']['comparison']['sha256']and c['raw_sha256']==OBJECT_SHA256 and c['CODE']==340 and c['CONST']==17 and c['debug_fields']==19,'history retained strict V2 semantic comparison')
 return out

def validate(unit,obj,project,reference):
 desc,blob,_=validate_layout(unit,obj);p=profile();root=Path(project).resolve();require(sha((root/SOURCE).read_bytes())==SOURCE_SHA256,'history owner source changed');e=_evidence(root,p);validate_data_address(dict(desc,reference_region='exepack-expanded'),reference);rid=validate_expanded_read(e['native'],dict(desc,reference_region='exepack-expanded'),blob,reference,emitted_mz_sites=[])
 u=p['unit_contracts']['accept_input_baaf'];near={obj.externals[f.target[1]]for f in obj.fixups if f.segment==1 and not f.segment_relative and f.target[0]==2};native=reference['image'][0xb9ba:0xb9ba+340];require(not any(a<0xb9ba+340 and a+2>0xb9ba for a in reference['relocations']),'history whole native CODE MZ set');loads=[]
 for base in[0,1,0x1000,0xffff]:
  ds=(0x5cc2+base)&65535;placements={s.index:((base,0xb9ba)if s.index==1 else(ds,0x4f0a if s.index==3 else 0))for s in obj.segments.values()};externs={n:((base if n in near else ds),v)for n,v in u['externals'].items()};code,logs=link_segment(obj,1,placements,{1:ds},externs);require(code==native and all(x['mz_relocation_image_offset']is None for x in logs),'history whole CODE340 four-base/native fields');loads.append(base)
 return desc,blob,{'classification':'complete_compiler_owned_history_literal_CONST17_context','profile':KIND,'source_data_credit':0,'authored_c_function_count':0,'size':17,'sha256':sha(blob),'complete_MZ_sites':[],'whole_CODE_size':340,'whole_CODE_fields':58,'whole_raw_fields':77,'real_CV_bytes':339,'real_CV_procedures':4,'four_forward_load_bases':loads,'rea_evidence_id':rid,'rea_evidence_sha256':p['evidence']['native']['sha256'],'raw_object_profile':OBJECT_SHA256,'literal_array_bits':136,'literal_element_builtin':0x80,'explicit_existing_DATA17_reownership':True,'original_global_MAP_proved':False,'omf_records_or_fields_modified':False}
def extract_pool(unit,obj,project,reference):
 validate_unit(unit);require(unit['backend']==BACKEND and unit['id']=='input_message_4f0a','history exact reowned existing Cdata row');p=validate_object(obj);_,blob,proof=validate(p['unit_contracts']['accept_input_baaf'],obj,project,reference)
 return blob,{'boundary':'complete_compiler_owned_anonymous_CONST_reownership','segment':{k:v for k,v in asdict(obj.segments[3]).items()if k!='chunks'},'size':17,'literal_bytes':17,'iterated_bytes':0,'reserved_bytes':0,'link_alignment_bytes':0,'emitted_mz_sites':[],'anonymous_no_data_PUBLIC_alias':True,'complete_CONST_proof':proof,'existing_credit_counted_once':True}
