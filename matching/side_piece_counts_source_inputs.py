"""Closed CONDITIONAL compatible two-side int[2] near COMMON4; credit0.

Native reset/copy4 and independent menu_columns8DD2 support this logical
partition. Universal unmasked-side bounds and historical capacity/TU/MAP remain
HELD. Target/evidence reads are comparison-only, outside compiler generation.
"""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf
from reference import build_reference,ORIGINAL_SHA256
from side_piece_counts_profile_pins import PINS,TOOLS,FIELDS
from side_piece_counts_raw import validate_provider_module
BACKEND='msc500-near-common-conditional-side-piece-counts-v1';SOURCE='src/link/side_piece_counts_state.c';NAMES=['_side_piece_counts'];FLAGS=['/AS','/Zl','/Zi']
SOURCE_SHA='ab7501baecf5f7951570988a9a396e601c43a8706e8f17f72f536857434e79bc';OBJECT_SHA='0ae2a0275833903acd444b42dc1a5ebc93bbeea6b46fec9cf9f49ca806424fb2';MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,m):
 if not v:raise ValueError('conditional side-counts: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'relative path');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'path escape');return p
def payload(o,i):
 s=o.segments[i];b=bytearray(s.length);seen=set()
 for at,x in s.chunks:
  require(0<=at<=at+len(x)<=s.length,'payload bounds');require(s.class_name=='DEBSYM'or not seen.intersection(range(at,at+len(x))),'nondebug overlap');b[at:at+len(x)]=x;seen.update(range(at,at+len(x)))
 require(len(seen)==s.length and not s.unsupported_data,'complete payload');return bytes(b)
def types(o):
 b=payload(o,6);at=0;out={}
 while at<len(b):
  require(at+3<=len(b)and b[at]==1,'CV type header');n=int.from_bytes(b[at+1:at+3],'little');require(n>0 and at+3+n<=len(b),'complete CV type');out[512+len(out)]=b[at+3:at+3+n];at+=3+n
 return out
def globals(o):
 b=payload(o,5);at=0;out={}
 while at<len(b):
  n=b[at]+1;x=b[at:at+n];require(n>=2 and len(x)==n,'complete CV symbol');at+=n
  if x[1]==5:
   require(n>=9 and n==x[8]+9,'complete global');name='_'+x[9:].decode();require(name not in out,'duplicate global');out[name]=int.from_bytes(x[6:8],'little')
 return out
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'exact registry fields');require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('conditional-side-piece-counts-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'exact conditional source/compiler profile')
 require(item['objects']==[{'symbol':'_side_piece_counts','size':4,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'exact conditional4 extent');require(item['evidence']==PINS,'exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'whole raw bytes');r=validate_provider_module(raw);require(r['type_index_observed']==515 and r['type_graph']=='7820838100','actual observed complete int[2] type515');o=read_omf(raw);require(o.segments[5].length==26 and o.segments[6].length==20,'actual debug26/type20');require(sha(raw)==OBJECT_SHA,'whole genuine reviewed compiler object');return[{'symbol':'_side_piece_counts','type_index':515,'datatype':98,'size':4}]
def validate_evidence(project,pins,target):
 require(pins==PINS,'exact evidence selection');p={}
 for k,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'evidence pin '+k);p[k]=b
 audit=json.loads(p['actual_cohort_audit']);bounds=json.loads(p['identity_bounds']);identity=json.loads(p['identity_audit']);model=json.loads(p['model']);require(audit['status']=='PASS independent actual selected3/physical4 cohort and genuine conditional near COMMON4'and audit['physical_compiler_calls']==4 and audit['selected_roles']==3 and audit['excluded_wrong_flags_board']==1 and audit['new_matching_credit']==0,'real4physical/3selected/1excluded cohort')
 require(model['status']=='CONDITIONAL compatible two-side int[2] logical definition only'and model['base']=='0x8dce'and model['bytes']==4 and model['end_exclusive']=='0x8dd2'and model['matching_credit']==0 and len(model['conditions'])==2 and'complete historical physical capacity'in model['HELD']and'universal unmasked or corrupt-input side bounds'in model['HELD'],'explicit conditional allocation contract')
 require(identity['status']=='PASS shared incomplete int-array identity/minimum4; complete storage extent HELD'and bounds['candidate_minimum_bytes']==4 and bounds['candidate_minimum_start']==0x8dce and bounds['candidate_minimum_end_exclusive']==0x8dd2 and'unmasked'in bounds['bounds_qualification'],'conditional minimum only')
 ranges=bounds['108_provided_near_definitions'];require(len(ranges)==108 and all(not(r['native_DS_start']<0x8dd2 and r['native_DS_end_exclusive']>0x8dce)for r in ranges),'108prior logical disjointness');require({r['symbol']:(r['native_DS_start'],r['size'])for r in bounds['independent_adjacent_provided_scalars']}=={'_menu_columns':(0x8dd2,2),'_height':(0x8dd4,2),'_last_key_8dcc':(0x8dcc,2)},'independent adjacent scalar models; no gap premise')
 validate_object(p['provider_object']);require(sha(p['provider_source'])==SOURCE_SHA,'pure compatible definition')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'target identity');image=build_reference(original)['image'];clients={k:read_omf(b)for k,b in p.items()if k.startswith('client_')};seen=[];debug=[]
 for k,o in clients.items():
  gs=globals(o);ts=types(o);require('_counts'not in gs and '_counts'not in o.externals.values()and'_side_piece_counts'in gs and ts[gs['_side_piece_counts']]==bytes.fromhex('7800838100'),'actual compatible incomplete signed-int-array client graph')
  for f in o.fixups:
   if f.target[0]==2 and o.externals.get(f.target[1])=='_side_piece_counts':
    if o.segments[f.segment].class_name=='CODE':seen.append((k,f.segment,f.offset))
    else:debug.append((k,f));require(f.segment==5 and f.width==4 and f.location_type==3 and f.segment_relative and f.frame==(5,None),'debug FAR separate from memory width')
 require(len(clients)==4 and len(seen)==11 and len(debug)==4,'complete fourclients11CODE4debug inventory');expected=[]
 for row in FIELDS:
  o=clients[row['client']];hits=[f for f in o.fixups if f.segment==row['segment']and f.offset==row['offset']];require(len(hits)==1,'unique raw field');f=hits[0];code=payload(o,f.segment);addend=int.from_bytes(code[f.offset:f.offset+2],'little');require(o.externals[f.target[1]]=='_side_piece_counts'and f.width==2 and f.location_type==1 and f.segment_relative and f.frame==(5,None)and f.raw.hex()==row['raw_FIXUPP']and addend==row['raw_addend']and addend in[0,2],'actual OFFSET16 field/addend')
  require(image[row['native_image_field']:row['native_image_field']+2]==bytes.fromhex(row['native_encoded'])==(0x8dce+addend).to_bytes(2,'little'),'actual native operand');expected.append((row['client'],f.segment,f.offset))
 require(set(expected)==set(seen)and len(set(expected))==11,'exact complete native field inventory');require(image[0x94ea:0x94f9]==bytes.fromhex('c706ce8dffffc706d08dffffb80400'),'actual twoWORD reset/copy4')
 return[{'symbol':'_side_piece_counts','dgroup_segment':'0x5cc2','dgroup_offset':'0x8dce','end_exclusive':'0x8dd2','size':4,'resolved':False,'conditional_two_side_model':True,'universal_unmasked_side_bound_proven':False,'historical_capacity_storageclass_TU_MAP_proven':False}]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'source hash');constraints=validate_evidence(project,item['evidence'],target)
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'fresh compiler provenance')
 definitions=validate_object(c.object_bytes);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'conditional-side-piece-counts-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');return{'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'CONDITIONAL_two_side_logical_int2_no_universal_bounds_or_historical_capacity_claim'}
