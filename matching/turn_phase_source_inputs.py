"""Closed signed-int WORD turn phase COMMON2. No aliases or byte credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256,validate_expanded_read
from turn_phase_profile_pins import PINS
BACKEND='msc500-near-common-turn-phase-v1'
SOURCE='src/link/turn_phase_state.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_state_57cc']
SOURCE_SHA='fdf751c8cd877355886fb5ab369247058def8dd84dfcd84b598e7536df7b5978'
OBJECT_SHA='684c243a7d82a394dfaa9b46ab79d73cecdf362edb8dbda80dcf7912392b68aa'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR':'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a','CL.EXE':'11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504','C1.EXE':'3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791','C1.ERR':'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233','C2.EXE':'19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1','C3.EXE':'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669','C23.ERR':'75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'turnphase relative path required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'turnphase path escapes project');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'turnphase unknown allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('turn-phase-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'turnphase closed source/profile required')
 require(item['objects']==[{'symbol':'_state_57cc','size':2,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'turnphase exact one WORD COMMON required')
 require(item['evidence']==PINS,'turnphase exact native evidence required')
def validate_object(data):
 require(isinstance(data,bytes),'turnphase raw unchanged OMF required');o=read_omf(data)
 require(not o.publics and not o.procedures,'turnphase no PUBLIC/function/alias allowed')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',19,32,False),('$$TYPES','DEBTYP',0,32,False)],'turnphase loaded/debug allocation changed')
 require([k for k,_,_ in o.records]==[0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0xb0,0x88,0xa0,0x9c,0x8a],'turnphase foreign/extra record shape')
 commons=[]
 for kind,at,p in o.records:
  if kind==0xb0:
   c=_Cursor(p)
   while c:commons.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'turnphase DGROUP changed')
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','turnphase producer filename changed')
  elif kind==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'turnphase producer directive changed')
  elif kind==0x8a:require(p==b'\0','turnphase entry point forbidden')
 require(commons==[{'symbol':'_state_57cc','type_index':0x81,'datatype':0x62,'size':2}],'turnphase exact near signed-int WORD2 COMDEF required')
 require(o.externals=={1:'__acrtused',2:'_state_57cc'},'turnphase exact external order/names required')
 require(all(s==5 for _,s,_,_ in o.data_writes),'turnphase initialized nondebug bytes forbidden')
 require(len(o.fixups)==1,'turnphase one exact debug field required');f=o.fixups[0]
 require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'turnphase debug field changed')
 require(o.segments[5].chunks==[(0,bytes.fromhex('12050000000081000a73746174655f35376363'))],'turnphase exact builtintype/debug record required')
 require(sha(data)==OBJECT_SHA,'turnphase complete object/CV/source pin mismatch');return commons

def validate_evidence(project,pins,target):
 require(pins==PINS,'turnphase exact evidence identity');payload={}
 for key,row in PINS.items():
  payload[key]=local(project,row['path']).read_bytes();require(sha(payload[key])==row['sha256'],'turnphase evidence hash '+key)
 review=json.loads(payload['review']);controls=json.loads(payload['compiler_controls'])
 require(review['status']=='PASS'and review['actual_reference_counts']=={'_display_mode':1,'_state':1,'_state_57cc':8}and review['selected_provided_owner_overlap']==[]and review['existing_COMMON_name_overlap']==[],'turnphase exact10/runtime/nonoverlap scope')
 require(review['minimal_compatible_provider']['declaration']=='int state_57cc;'and review['minimal_compatible_provider']['bytes']==2 and review['minimal_compatible_provider']['matching_credit']==0 and not review['minimal_compatible_provider']['new_alias_PUBLICs'],'turnphase compatible scalar/noalias scope')
 require(controls['status']=='PASS'and controls['controls'][0]['object_sha256']==OBJECT_SHA and controls['controls'][0]['source_sha256']==SOURCE_SHA and sha(payload['source_model'])==SOURCE_SHA,'turnphase source proof')
 validate_object(payload['object']);require(controls['controls'][1]['whole_common']==[{'symbol':'_state_57cc','type':132,'datatype':98,'size':1}]and not controls['controls'][1]['native_WORD_type_constraint_pass'],'turnphase genuine wrongwidth control')
 raw=Path(target).read_bytes();require(sha(raw)==ORIGINAL_SHA256,'turnphase original target');image=build_reference(raw)['image'];objects={};primaries={};sourcehashes=set()
 for key,row in pins.items():
  if key.startswith('client_object_'):objects[row['path']]=read_omf(payload[key])
  if key.startswith('primary_'):primaries[row['path']]=json.loads(payload[key])
  if key.startswith('client_source_'):sourcehashes.add(sha(payload[key]))
 require(sourcehashes=={v['source_sha256']for v in review['actual_sources_AST'].values()},'turnphase actual all5 typed source snapshots')
 for info in review['actual_sources_AST'].values():require(info['declarations']and all(x['type']=='int'and x['storage']=='extern'and x['init']is None for x in info['declarations']),'turnphase client int ABI')
 expected={0x7e63,0x91cd,0x7ba5,0x7e75,0x7f4a,0x7fba,0x8e25,0x8e2d,0x8048,0x805c}
 refs=review['actual_runtime_WORD_fields'];require(len(refs)==10 and {int(x['native_field_image'],0)for x in refs}==expected,'turnphase exact10 field coordinates')
 ids=set()
 for ref in refs:
  f=ref['relocation'];matches=[]
  for o in objects.values():
   for v in o.fixups:
    if v.segment==f['segment']and v.offset==f['object_offset']and v.raw.hex()==ref['raw_FIXUPP']and v.target[0]==2 and o.externals.get(v.target[1])==ref['symbol']:matches.append((o,v))
  require(len(matches)==1,'turnphase unique exact raw client field');o,v=matches[0]
  require(o.segments[v.segment].class_name=='CODE'and v.width==2 and v.location_type==1 and v.segment_relative and v.frame==(5,None)and v.target==(2,f['target_index'])and v.displacement in[None,0]and f['target_offset']==0x57cc and f['mode']=='segment_relative_dgroup'and ref['memory_access_bytes']==2 and not ref['address_only']and image[f['image_offset']:f['image_offset']+2]==b'\xcc\x57','turnphase real WORD memory field')
  e=primaries[ref['native_primary']];p=e['analysis_profile'];entry={'turn_7ddb':'0x17ddb','no_move_900a':'0x1900a','select_display_7ba4':'0x17ba4','alternate_view_7e6b':'0x17e6b','dispatch_8d73':'0x18d73','computer_cycle_801a':'0x1801a'}[ref['unit']];require(e['parameters']=={'procedure':entry}and e['evidence_id']==ref['native_primary_id']and e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['subject']['format']=='dos-mz'and e['subject']['architecture']=='x86'and e['provider']['id']=='ghidra'and p['digest']=='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'and p['parameters']['loader']=='MzLoader'and p['parameters']['load_segment']=='0x1000'and p['parameters']['address_coordinates']=='linear-byte-offset'and p['parameters']['language_id']=='x86:LE:16:Real Mode'and e['operation']=='analyze_function'and ref['instruction']in e['normalized_result']['assembly']and '[0x57cc]'in ref['instruction'],'turnphase native profile/direct memory semantics');ids.add(e['evidence_id'])
 require(len(ids)==6,'turnphase six distinct callable native bodies')
 selector=next(e for e in primaries.values()if e['parameters']=={'procedure':'0x17ba4'})['normalized_result']['assembly'];require(all(x in selector for x in['0x17bb6: CALL 0x1000:7ddb','0x17bba: CALL 0x1000:7e6b','0x17bbe: CALL 0x1000:801a']),'turnphase dispatcher lifecycle')
 crt=json.loads(payload['crt']);require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['parameters']=={'address':'0x1ea86','length':179}and crt['normalized_result']['complete']and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'turnphase complete CRT clear')
 require(0x52cc<=0x57cc<0x57ce<=0xcbe0 and 0x5cc20+0x57cc>=len(image),'turnphase uninitialized cleared WORD')
 return [{'symbol':'_state_57cc','dgroup_segment':'0x5cc2','dgroup_offset':'0x57cc','end_exclusive':'0x57ce','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_COMMON_order_proven':False,'original_TU_or_larger_owner_unknown':True}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'turnphase source hash changed')
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'turnphase fresh compiler/source/tool provenance changed')
 defs=validate_object(c.object_bytes)
 constraints=validate_evidence(project,item['evidence'],target) # All targetcomparison reads follow source-onlygeneration.
 output=Path(output);output.mkdir(parents=True,exist_ok=True);artifact=output/'turn-phase-common.obj';artifact.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(artifact),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':2,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'single_signed_int_turn_phase_no_alias','authored_C_function_credit':0}
