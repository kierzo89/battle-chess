"""Closed compatible logical Ray239 near COMMON, zero loaded/matching credit."""
from pathlib import Path
import dataclasses,hashlib,json,struct
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from rays239_profile_pins import PINS
BACKEND='msc500-near-common-rays239-v1'
SOURCE='src/link/ray_table_state.c'
SOURCE_SHA='74e9fe1712f73813ff35b12cb9bbe7c9b7be56cfb3f97194f462cb6ea8e73234'
OBJECT_SHA='59aec888b16df45cabfb8ce15e8ec566aaed16a343ce67c5537b1581d4184f69'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_rays']
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
TYPES='010100800101008001010080010c007920028304028305028200690107007f8385008381000111007f82046d61736b88008204737465708802010100800107007885e01d830302'
DEBUG='0c050000000007020472617973'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}

def require(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'rays239 relative path required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'rays239 path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'rays239 exact item fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('rays239-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'rays239 exact source/profile')
 require(item['objects']==[{'symbol':'_rays','size':956,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'rays239 exact logical956 COMMON')
 require(item['evidence']==PINS,'rays239 exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'rays239 unchanged bytes required');o=read_omf(raw)
 require(not o.publics and not o.procedures,'rays239 PUBLIC/alias/procedure forbidden')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',13,32,False),('$$TYPES','DEBTYP',71,32,False)],'rays239 loaded/debug allocation')
 require([k for k,_,_ in o.records]==[0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0xb0,0x88,0xa0,0x9c,0xa0,0x8a],'rays239 exact record shape')
 defs=[];comm=0
 for k,at,p in o.records:
  if k==0xb0:
   comm+=1;q=_Cursor(p)
   while q:
    n,t,mode,leaf=q.name(),q.index(),q.byte(),q.byte();require(leaf==0x81,'rays239 exact COMMON956 numeric leaf');size=q.word();defs.append({'symbol':n,'type_index':t,'datatype':mode,'size':size})
  elif k==0x80:require(p==b'\x09C:\\UNIT.C','rays239 producer filename')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'rays239 DGROUP')
  elif k==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'rays239 compiler directive')
  elif k==0x8a:require(p==b'\0','rays239 entrypoint forbidden')
 require(comm==1 and defs==[{'symbol':'_rays','type_index':0x207,'datatype':0x62,'size':956}],'rays239 exact single nearCOMMON956/type207')
 require(o.externals=={1:'__acrtused',2:'_rays'},'rays239 exact external identities/order')
 require(all(s in[5,6]for _,s,_,_ in o.data_writes),'rays239 loaded initialization forbidden')
 require(o.segments[5].chunks==[(0,bytes.fromhex(DEBUG))]and o.segments[6].chunks==[(0,bytes.fromhex(TYPES))],'rays239 unsignedmask/intstep/offsets/array956 CodeView')
 require(len(o.fixups)==1 and [(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,2,4,3,True,(5,None),(2,2),None)],'rays239 sole debug field')
 require(sha(raw)==OBJECT_SHA,'rays239 whole object/source fingerprint');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'rays239 exact evidence');payload={}
 for k,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'rays239 evidence pin '+k);payload[k]=raw
 r=json.loads(payload['review']);root=json.loads(payload['root_review']);oracle=json.loads(payload['native_oracle'])
 require(r['status']=='SUPPORTED_COMPATIBLE_LOGICAL_EXTENT'and root['status']=='SUPPORTED_COMPATIBLE_LOGICAL_ARRAY_UNDER_DISTINCT_SCALAR_MODEL'and not root['blockers_to_this_bounded_model'],'rays239 conditional independent extent review')
 require(r['candidate_logical_array_records']==239 and r['candidate_bytes']==956 and r['range_DS']==['0x5404','0x57c0']and r['lower_bound_independent_of_fill_bytes']==956,'rays239 lower/upper logical extent')
 require(r['historical_unique_capacity_container_owner_TU_MAP_proven']is False and r['held_initializer_C_match_claimed']is False and not r['existing_initialized_overlap']and not r['existing_native_anchored_COMMON_overlap'],'rays239 no historical ownership/heldC/overlap claim')
 require(not root['global_caller_safety_proven']and not root['native_MAP_proven']and root['malformed_inputs_held']and r['valid_0x88_domain']=={'squares':64,'pairs':4096,'minimum_index':0,'maximum_index':238,'actual_input_validation_proved':False},'rays239 finite normal-domain limits')
 require(oracle['not_C_match_or_complete_game_execution']and len(oracle['explicit_substitutions'])==2 and oracle['fill_hook_bytes']==956 and oracle['minimum_index']==0 and oracle['maximum_index']==238,'rays239 native oracle contract limits')
 require(sha(payload['source_model'])==SOURCE_SHA,'rays239 actual source model');validate_object(payload['object'])
 controls=json.loads(payload['compiler_controls']);require(controls['status']=='PASS'and controls['controls'][0]['object_sha256']==OBJECT_SHA and controls['controls'][1]['complete_COMDEF'][0]['size']==952,'rays239 genuine wrong238 boundary control')
 require('typedef struct { unsigned mask; int step; } Ray;'in payload['piece_source'].decode()and 'extern Ray rays[];'in payload['piece_source'].decode(),'rays239 exact selected consumer type')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'rays239 original identity');ref=build_reference(original);image=ref['image']
 require(sha(image[0x9840:0x98f9])==oracle['native_sha256'],'rays239 native185 bytes')
 init=json.loads(payload['init_primary']);piece=json.loads(payload['piece_primary']);pawn=json.loads(payload['pawn_primary'])
 for e,entry,size in [(init,0x9840,185),(piece,0x98f9,197)]:
  b=e['normalized_result']['procedure']['body'];require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['operation']=='analyze_function'and e['parameters']=={'procedure':hex(entry+0x10000)}and b['total_bytes']==b['span_bytes']==size and not b['non_contiguous'],'rays239 original primary/bounds')
 ia=init['normalized_result']['assembly']
 for line in ['0x19879: CMP word ptr [BP + -0x6], 0x7','0x19884: MOV AX, word ptr [BX + 0x4ea]','0x19888: IMUL word ptr [BP + -0x6]','0x1988f: ADD AX, 0x55e0','0x198c0: MOV word ptr [BX + 0x2], AX']:require(line in ia,'rays239 actual native endpoint operations')
 steps=struct.unpack('<8h',image[0x5cc20+0x4ea:0x5cc20+0x4ea+16]);require(steps==(1,-1,16,-16,17,-17,15,-15),'rays239 supplied actual directions')
 indices=[s*d+119 for s in steps for d in range(1,8)];require(min(indices)==0 and max(indices)==238 and 0x5404+max(indices)*4+4==0x57c0,'rays239 native full last record')
 upper=r['upper_bound_independent_distinct_supplied_scalar'];require(upper['name']=='_pawn_material'and upper['native_start_DS']=='0x57c0'and upper['size']==2 and upper['type']=='int','rays239 distinct pawn upper bound')
 po=read_omf(payload['pawn_object']);defs=[]
 for k,off,p in po.records:
  if k==0xb0:
   q=_Cursor(p)
   while q:defs.append((q.name(),q.index(),q.byte(),q.byte()))
 require(('_pawn_material',0x81,0x62,2)in defs,'rays239 actual separate int pawn provider')
 require(pawn['subject']['digest']['sha256']==ORIGINAL_SHA256 and '0x1fe6e: MOV word ptr [0x57c0], 0x0'in pawn['normalized_result']['assembly']and '0x1fec2: ADD word ptr [0x57c0], AX'in pawn['normalized_result']['assembly']and image[0xfe6e:0xfe74]==bytes.fromhex('c706c0570000')and image[0xfec2:0xfec6]==bytes.fromhex('0106c057'),'rays239 native independent pawn lifecycle')
 rayrefs=r['actual_ray_runtime_FIXUPPs'];require(len(rayrefs)==1,'rays239 one actual immediate base field');f=rayrefs[0]['runtime_field'];co=read_omf(payload['piece_object']);v=[v for v in co.fixups if v.segment==f['segment']and v.offset==f['object_offset']];require(len(v)==1 and v[0].raw.hex()==rayrefs[0]['raw_FIXUPP']and co.externals[v[0].target[1]]=='_rays'and image[f['image_offset']:f['image_offset']+2]==bytes.fromhex('0454'),'rays239 real immediate base, not invented memory width')
 crt=json.loads(payload['crt']);require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['parameters']=={'address':'0x1ea86','length':179}and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'rays239 actual CRTclear')
 require(0x52cc<=0x5404<0x57c0<=0xcbe0 and 0x5cc20+0x5404>=len(image),'rays239 cleared nonfilebacked allocation')
 return [{'symbol':'_rays','dgroup_segment':'0x5cc2','dgroup_offset':'0x5404','end_exclusive':'0x57c0','logical_records':239,'record_bytes':4,'resolved':False,'historical_COMMON_order_proven':False,'unique_historical_capacity_container_TU_type':False,'global_invalid_input_safety_proven':False,'conditional_on_distinct_pawn_scalar_nonoverlap':True}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();src=local(project,SOURCE);before=src.read_bytes();require(sha(before)==SOURCE_SHA,'rays239 source hash')
 c=(compile_c if compiler_fn is None else compiler_fn)(src,FLAGS,compiler='msc500');require(src.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'rays239 fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/'rays239-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':956,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_logical_Ray239_distinct_pawn_scalar'}
