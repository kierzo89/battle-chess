"""Closed compatible four-array logical COMMON64; no matching credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from link16 import link_function
from asset_fixed_arrays_profile_pins import PINS,TOOLS,GRAPHS
BACKEND='msc500-near-common-asset-fixed-arrays-v1'
SOURCE='src/link/asset_fixed_arrays_state.c'
SOURCE_SHA='f732c2373bc459bd2a876650330d0be6859c0c76116d099dc68e96c1ff1f8428'
OBJECT_SHA='8801be97f9712d06874fef0e29a2989031d66d25ffcfae85b2850a369beb96c7'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_metadata_records','_frame_descriptors','_values','_task_pool'];SIZES=[16,32,8,8];TYPES=[522,523,524,525];OFFSETS=[0x934e,0x985a,0x8d1a,0xb0be]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'asset-four relative path');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'asset-four path escape');return p
def debug(o,klass):
 s=next(s for s in o.segments.values()if s.class_name==klass);b=bytearray(s.length);seen=set()
 for at,x in s.chunks:
  require(0<=at<=at+len(x)<=s.length,'asset-four debug bounds');b[at:at+len(x)]=x;seen.update(range(at,at+len(x)))
 require(not s.unsupported_data and len(seen)==s.length,'asset-four debug complete coverage');return bytes(b)
def types(o):
 b=debug(o,'DEBTYP');at=0;idx=512;out={}
 while at<len(b):
  require(at+3<=len(b)and b[at]==1,'asset-four CV header');n=int.from_bytes(b[at+1:at+3],'little');v=b[at+3:at+3+n];require(n>0 and len(v)==n,'asset-four CV bounds');out[idx]=v;at+=3+n;idx+=1
 require(at==len(b),'asset-four CV EOF');return out
def globals(o):
 b=debug(o,'DEBSYM');at=0;out={}
 while at<len(b):
  n=b[at];v=b[at+1:at+n+1];require(n>=1 and len(v)==n,'asset-four CV symbol bounds');at+=n+1
  if v[0]==5:
   require(len(v)>=8 and len(v)==8+v[7],'asset-four complete CV global');name='_'+v[8:].decode();require(name not in out,'asset-four duplicate CV global');out[name]=int.from_bytes(v[5:7],'little')
 require(at==len(b),'asset-four CV symbol EOF');return out
def graph(ts,t,trail=()):
 if t<512:return ['builtin',t]
 require(t in ts and t not in trail and len(trail)<16,'asset-four CV missing/cyclic/deep type');trail=trail+(t,);b=ts[t];q=_Cursor(b);leaf=q.byte()
 if leaf==0x78:
  n=q.byte();require(n<0x80 or n==0x85,'asset-four array numeric leaf');bits=q.word()if n==0x85 else n;require(q.byte()==0x83,'asset-four array element leaf');elem=q.word();q.finish();return ['array',bits,graph(ts,elem,trail)]
 if leaf==0x79:
  require(q.byte()==64 and q.byte()==5 and q.byte()==0x83,'asset-four exact Frame shape');members=q.word();require(q.byte()==0x83,'asset-four Frame field names');names=q.word()
  require(b==bytes.fromhex('79400583')+members.to_bytes(2,'little')+b'\x83'+names.to_bytes(2,'little')+bytes.fromhex('820069'),'asset-four exact complete Frame record');return ['Frame',64,5,graph(ts,members,trail),graph(ts,names,trail)]
 if leaf==0x7f and len(b)>1 and b[1]==0x83:
  entries=[]
  while q:require(q.byte()==0x83,'asset-four Frame member type leaf');entries.append(graph(ts,q.word(),trail))
  return ['member-types',entries]
 if leaf==0x7f:return ['member-names-offsets',b.hex()]
 if leaf==0x7a:
  require(q.byte()==0x74 and q.byte()==0x83,'asset-four actual named pointer');target=q.word();require(b[5:]==bytes.fromhex('820d416e696d6174696f6e5461736b'),'asset-four AnimationTask pointer identity');return ['named-pointer',0x74,graph(ts,target,trail),'AnimationTask']
 require(b==b'\x80','asset-four unknown CV leaf');return ['placeholder',128]
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'asset-four exact registry fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('asset-fixed-arrays-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'asset-four exact source/compiler profile')
 require(item['objects']==[{'symbol':n,'size':s,'storage':'near-common'}for n,s in zip(NAMES,SIZES)]and all(type(o['size'])is int for o in item['objects']),'asset-four exact four logical extents');require(item['evidence']==PINS,'asset-four exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'asset-four whole raw bytes');o=read_omf(raw)
 require(not o.publics and not o.procedures,'asset-four no PUBLIC/procedure/alias')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',84,32),('$$TYPES','DEBTYP',164,32)],'asset-four empty loaded segments/exact debug')
 require(not any(s.unsupported_data for s in o.segments.values()),'asset-four no LIDATA')
 defs=[];records=0
 for k,at,p in o.records:
  require(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a},'asset-four unknown OMF record')
  if k==0xb0:
   records+=1;q=_Cursor(p)
   while q:
    name,t,dt,size=q.name(),q.index(),q.byte(),q.byte();require(dt==0x62 and size<0x80,'asset-four near COMMON byte length');defs.append({'symbol':name,'type_index':t,'datatype':dt,'size':size})
  elif k==0x88:require(p in [bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'asset-four unknown COMMENT')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'asset-four exact DGROUP')
  elif k==0x8a:require(p==b'\0','asset-four no entry point')
 require(records==1 and defs==[{'symbol':n,'type_index':t,'datatype':98,'size':s}for n,t,s in zip(NAMES,TYPES,SIZES)],'asset-four exact four near COMMON64/name/type/order')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'asset-four exact externals')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,a,4,3,True,(5,None),(2,t),None)for a,t in [(68,5),(53,4),(27,3),(2,2)]],'asset-four only four debug FAR fields')
 require(all(s in [5,6]for _,s,_,_ in o.data_writes),'asset-four no initialized loaded bytes')
 gs=globals(o);ts=types(o);require(gs==dict(zip(NAMES,TYPES))and len(ts)==15,'asset-four exact global/type inventory')
 require({n:graph(ts,t)for n,t in gs.items()}==GRAPHS,'asset-four complete array/pointer/Frame member type graph')
 require(sha(raw)==OBJECT_SHA,'asset-four whole reviewed object fingerprint');return defs
def validate_evidence(project,pins,target):
 require(pins==PINS,'asset-four exact evidence selection');p={}
 for key,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'asset-four evidence pin '+key);p[key]=b
 proof=json.loads(p['ownership']);producer=json.loads(p['producer_proof']);gen=json.loads(p['generation']);context=json.loads(p['native_context'])
 require(proof['status']=='PASS compatible complete logical arrays supported by native initializer and actual client CV'and proof['native_complete_initializer_bytes_equal']and proof['old23_strict_decoder_definitions']==103,'asset-four closed native ownership proof')
 require(len(proof['prior_checked_ranges'])==103 and len({r[2]for r in proof['prior_checked_ranges']})==103,'asset-four all103 prior ranges')
 spans=[(a,a+n)for a,n in zip(OFFSETS,SIZES)]
 require(all(not(a<d and b>c)for a,b in spans for c,d,name in proof['prior_checked_ranges'])and all(not(a<d and b>c)for i,(a,b)in enumerate(spans)for c,d in spans[i+1:]),'asset-four all103 and mutual nonoverlap')
 require([(r['symbol'],int(r['base'],16),int(r['end_exclusive'],16),r['bytes'],r['entries'])for r in proof['arrays']]==[(n,a,a+s,s,4)for n,a,s in zip(NAMES,OFFSETS,SIZES)],'asset-four exact native logical ranges')
 require(all(v==0 for v in proof['credit'].values())and not proof['held_unselected_fields']and producer['matching_credit']==producer['loaded_bytes']==producer['PUBLICs']==producer['procedures']==0,'asset-four zero credit and no held referring fields')
 require(producer['normalized_graphs']==GRAPHS and producer['whole_object_sha256']==OBJECT_SHA and gen['source_sha256']==SOURCE_SHA and gen['object_sha256']==OBJECT_SHA and sha(p['source_model'])==SOURCE_SHA,'asset-four genuine source/object/type identity');validate_object(p['producer_object'])
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'asset-four target identity');image=build_reference(original)['image']
 native=json.loads(p['native_primary']);body=native['normalized_result']['procedure']['body']
 require(native['subject']['digest']['sha256']==ORIGINAL_SHA256 and native['evidence_id']==proof['native_evidence']and body['ranges']==[{'start':'0x128ae','end':'0x129b8'}]and body['total_bytes']==body['span_bytes']==267 and not body['non_contiguous'],'asset-four complete native initializer identity')
 require(all(s in native['normalized_result']['assembly']for s in proof['native_required_instructions']),'asset-four native loop bounds/strides/stores')
 clients={row['path']:read_omf(p[k])for k,row in PINS.items()if k.startswith('client_object_')};byname={Path(k).name:o for k,o in clients.items()};allfields=[];debugfields=[];typed=0
 for key,o in clients.items():
  gs=globals(o);ts=types(o)
  for n in NAMES:
   if n in gs:require(graph(ts,gs[n])==GRAPHS[n],'asset-four actual complete client type');typed+=1
  for f in o.fixups:
   if f.target[0]==2 and o.externals.get(f.target[1])in NAMES:
    (allfields if o.segments[f.segment].class_name=='CODE'else debugfields).append((Path(key).name,o,f))
 require(len(allfields)==len(proof['selected_CODE_fields'])==11 and len(debugfields)==len(proof['debug_fields_not_runtime'])==typed==6,'asset-four all actual eleven CODE and six debug fields')
 expected=[]
 for row in proof['selected_CODE_fields']:
  frow=row['field'];u=context['units'][row['unit']];o=byname[Path(u['object']).name];hits=[f for f in o.fixups if f.segment==1 and f.offset==frow['object_offset']];require(len(hits)==1,'asset-four raw CODE field ownership');f=hits[0]
  require(o.externals[f.target[1]]==row['symbol']and f.width==2 and f.location_type==1 and f.segment_relative and f.frame==(5,None)and f.raw.hex()==frow['raw_FIXUPP'],'asset-four raw OFFSET16')
  code=bytearray(o.segments[1].length)
  for at,b in o.segments[1].chunks:code[at:at+len(b)]=b
  addend=int.from_bytes(code[f.offset:f.offset+2],'little');address=dict(zip(NAMES,OFFSETS))[row['symbol']];value=(address+addend+(f.displacement or 0))&65535;info=o.function_info(u['symbol']);at=u['image_offset']-info['offset']+f.offset
  require(addend==frow['raw_addend']and at==frow['native_image_offset']and image[at:at+2]==value.to_bytes(2,'little')==bytes.fromhex(frow['encoded_hex']),'asset-four actual native CODE operand');expected.append((Path(u['object']).name,f.segment,f.offset))
 require(set(expected)=={(name,f.segment,f.offset)for name,o,f in allfields}and len(set(expected))==11,'asset-four complete runtime inventory equality')
 require(all(f.width==4 and f.location_type==3 and f.segment_relative and f.frame==(5,None)for name,o,f in debugfields),'asset-four debug FAR separate')
 init=context['units']['initialize_asset_storage_28ae'];o=byname[Path(init['object']).name];ext=dict(init['externals']);ext.update({n:pub.offset+0x28ae for n,pub in o.publics.items()if pub.segment==1});linked,_=link_function(o,init['symbol'],0x28ae,ext,image_origin=0x28ae)
 require(len(linked)==267 and linked==image[0x28ae:0x29b9],'asset-four full267 native client')
 require(all(0x52cc<=a<b<=0xcbe0 for a,b in spans)and [(r['symbol'],r['address'])for r in proof['following_distinct_anchors']]==[('_setup_lengths','0x987a'),('_screen_x','0xb0c6')],'asset-four CRT bounds and separate following anchors')
 for anchor in proof['following_distinct_anchors']:
  require(bool(anchor['actual_selected_fields']),'asset-four following native anchor inventory')
  for row in anchor['actual_selected_fields']:
   f=row['field'];key=next((key for key,pin in PINS.items()if key.startswith('anchor_object_')and Path(pin['path']).name==Path(row['object']).name),None);require(key is not None,'asset-four pinned anchor object');a=read_omf(p[key]);hits=[q for q in a.fixups if q.segment==f['segment']and q.offset==f['object_offset']];require(len(hits)==1,'asset-four actual anchor raw ownership');q=hits[0]
   require(a.externals[q.target[1]]==anchor['symbol']and q.raw.hex()==row['raw_FIXUPP']and q.width==2 and q.location_type==1 and q.segment_relative and q.frame==(5,None),'asset-four actual distinct anchor raw field')
   require(image[f['image_offset']:f['image_offset']+2]==bytes.fromhex(f['encoded_hex'])==int(anchor['address'],16).to_bytes(2,'little'),'asset-four distinct following native anchor')
 return [{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(a),'end_exclusive':hex(a+s),'size':s,'resolved':False,'historical_physical_owner_class_TU_order_MAP_unique_capacity_proven':False}for n,a,s in zip(NAMES,OFFSETS,SIZES)]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'asset-four source hash')
 constraints=validate_evidence(project,item['evidence'],target)
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'asset-four fresh compiler provenance')
 defs=validate_object(c.object_bytes);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'asset-fixed-arrays-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':64,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_four_entry_logical_arrays_no_physical_owner_class_TU_order_MAP_claim'}
