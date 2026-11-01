"""Closed compatible logical Move8 owner; zero matching credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from link16 import link_function
from move8d12_profile_pins import PINS,TOOLS,EXPECTED_GRAPH
BACKEND='msc500-near-common-move8-state-v1';SOURCE='src/link/move_state_8d12.c';NAMES=['_state_8d12'];FLAGS=['/AS','/Zl','/Zi']
SOURCE_SHA='926b01ba7e41a506e741ba0f70cd123fbd9a10826ad3b8880508ac782a3c1507';OBJECT_SHA='02f193a1ca631b647f42ab5e0bd592ddac9e31ad0adbd2b5f950790ef1cb4ecb';MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'Move8 relative path');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'Move8 path escape');return p
def debug(o,klass):
 ss=[s for s in o.segments.values()if s.class_name==klass];require(len(ss)==1,'Move8 unique debug class');s=ss[0];b=bytearray(s.length);seen=set()
 for at,v in s.chunks:require(0<=at<=at+len(v)<=s.length,'Move8 debug bounds');b[at:at+len(v)]=v;seen.update(range(at,at+len(v)))
 require(len(seen)==s.length and not s.unsupported_data,'Move8 complete ordered debug');return bytes(b)
def types(o):
 b=debug(o,'DEBTYP');at=0;ts={}
 while at<len(b):
  require(at+3<=len(b)and b[at]==1,'Move8 CV type header');n=int.from_bytes(b[at+1:at+3],'little');require(n>0 and at+3+n<=len(b),'Move8 CV type bounds');ts[512+len(ts)]=b[at+3:at+3+n];at+=3+n
 require(at==len(b),'Move8 CV type EOF');return ts
def globals(o):
 b=debug(o,'DEBSYM');at=0;out={}
 while at<len(b):
  n=b[at]+1;v=b[at:at+n];require(n>=2 and len(v)==n,'Move8 CV symbol bounds')
  if v[1]==5:
   require(n>=9 and n==9+v[8],'Move8 complete CV global');name='_'+v[9:].decode();require(name not in out,'Move8 duplicate CV global');out[name]={'type':int.from_bytes(v[6:8],'little'),'offset':at,'raw':v.hex()}
  at+=n
 require(at==len(b),'Move8 CV symbol EOF');return out
def graph(ts,t,seen=None,trail=()):
 if t<512:return {'builtin':t}
 require(t in ts and t not in trail and len(trail)<12,'Move8 missing/cyclic/deep CV type');v=ts[t];q=_Cursor(v);leaf=q.byte();trail=trail+(t,)
 if seen is not None:seen.add(t)
 if leaf==0x79:
  bits=q.byte();require(bits<0x80,'Move8 exact finite composite size');count=q.byte();require(q.byte()==0x83,'Move8 composite member leaf');members=q.word();require(q.byte()==0x83,'Move8 composite names leaf');names=q.word();require(q.take(3)==bytes.fromhex('820069'),'Move8 complete anonymous composite');q.finish();return {'composite_leaf':121,'bits':bits,'member_count':count,'members':graph(ts,members,seen,trail),'names_offsets':graph(ts,names,seen,trail)}
 require(leaf==0x7f,'Move8 unknown CV leaf')
 if len(v)>1 and v[1]==0x83:
  out=[]
  while q:require(q.byte()==0x83,'Move8 member type leaf');out.append(graph(ts,q.word(),seen,trail))
  return {'member_types':out}
 out=[]
 while q:
  require(q.byte()==0x82,'Move8 member name leaf');n=q.byte();name=q.take(n).decode();require(q.byte()==0x88,'Move8 member offset leaf');out.append({'name':name,'offset':q.byte()})
 return {'member_names_offsets':out}
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'Move8 exact registry fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('move8-state-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'Move8 exact source/compiler profile')
 require(item['objects']==[{'symbol':'_state_8d12','size':8,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'Move8 exact logical8 declaration');require(item['evidence']==PINS,'Move8 exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'Move8 whole raw bytes');o=read_omf(raw);require(not o.publics and not o.procedures,'Move8 no PUBLIC/procedure/alias')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',19,32),('$$TYPES','DEBTYP',177,32)],'Move8 empty loaded/exact debug segments')
 defs=[];records=0
 for k,at,p in o.records:
  require(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a},'Move8 unknown OMF record')
  if k==0xb0:
   records+=1;q=_Cursor(p)
   while q:defs.append({'symbol':q.name(),'type_index':q.index(),'datatype':q.byte(),'size':q.byte()})
  elif k==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'Move8 unknown COMMENT')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'Move8 exact DGROUP')
  elif k==0x8a:require(p==b'\0','Move8 no entry point')
 require(records==1 and defs==[{'symbol':'_state_8d12','type_index':522,'datatype':98,'size':8}],'Move8 exact single near COMMON8/type20A')
 require(o.externals=={1:'__acrtused',2:'_state_8d12'},'Move8 exact externals')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,2,4,3,True,(5,None),(2,2),None)],'Move8 only debug FAR field')
 require(all(sn in[5,6]for pos,sn,off,n in o.data_writes)and not any(s.unsupported_data for s in o.segments.values()),'Move8 no loaded data/LIDATA')
 require(globals(o)=={'_state_8d12':{'type':522,'offset':0,'raw':'1205000000000a020a73746174655f38643132'}},'Move8 exact CV global')
 seen=set();require(graph(types(o),522,seen)==EXPECTED_GRAPH and len(seen)==9,'Move8 complete64bit graph and exact member signedness/union/offsets')
 f=o.fixups[0];require(not any(pos>f.record_offset and sn==5 and off<6 and 2<off+n for pos,sn,off,n in o.data_writes),'Move8 debug field overwritten after FIXUPP');require(sha(raw)==OBJECT_SHA,'Move8 whole reviewed object fingerprint');return defs
def validate_evidence(project,pins,target):
 require(pins==PINS,'Move8 exact evidence selection');p={}
 for key,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'Move8 evidence pin '+key);p[key]=b
 identity=json.loads(p['identity']);inventory=json.loads(p['inventory']);controls=json.loads(p['controls_summary']);cases=json.loads(p['control_cases']);provider=json.loads(p['provider_proof']);generation=json.loads(p['provider_generation']);context=json.loads(p['native_context']);ranges=json.loads(p['range_preflight'])
 require(identity['same_normalized_complete_graph']and identity['actual_CODE_fields']==79 and identity['actual_candidate_fields']==73 and identity['actual_state_fields']==6 and identity['no_unselected_actual_CODE_fields'],'Move8 closed native identity')
 require(all(x['normalized_complete_Move']==EXPECTED_GRAPH for x in identity['complete_types_five_TUs'])and provider['normalized_complete_Move']==EXPECTED_GRAPH and provider['matches_all_five_existing_complete_client_graphs'],'Move8 complete five-client/provider graph identity')
 require(controls['status']=='PASS all four genuine lexical rename controls'and controls['actual_C5_compiles']==4 and controls['all42_selected_native_units']==42 and controls['editor_source_object_profile_unchanged']and controls['book800_CONST2_all8CV_sevenCONSTrefs_BASE619C6_skip22_gate_PASS'],'Move8 closed genuine rename controls')
 require(len(cases)==4 and all(c['status']=='PASS'for c in cases)and generation['actual_compiler_calls']==1 and generation['source_sha256']==SOURCE_SHA and generation['object_sha256']==OBJECT_SHA and sha(p['source_model'])==SOURCE_SHA,'Move8 actual source generation identity');validate_object(p['producer_object'])
 require(len(ranges['current25_near_ranges'])==104 and len(ranges['future26_near_ranges'])==108 and all(not(a<0x8d1a and b>0x8d12)for a,b,n in ranges['future26_near_ranges'])and ranges['following_values']==[0x8d1a,0x8d22],'Move8 all108 logical ranges and distinct values boundary')
 require(0x52cc<=0x8d12<0x8d1a<=0xcbe0,'Move8 CRT clear bounds')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'Move8 original target');ref=build_reference(original);expected={f['native_image_field']:f for f in inventory['actual_CODE_fields']};require(len(expected)==79,'Move8 native79 unique fields')
 actual=[];debugfields=[];matched_graphs=[];bodies=0;bookgates=0
 for client in context['clients']:
  raw=p[client['object_key']];require(sha(raw)==client['object_sha256']and sha(p[client['source_key']])==client['source_sha256'],'Move8 whole actual client/source identity');o=read_omf(raw);gs=globals(o);seen=set();require('_candidate_move'not in o.externals.values()and graph(types(o),gs['_state_8d12']['type'],seen)==EXPECTED_GRAPH and len(seen)==9,'Move8 complete actual renamed/client graph');matched_graphs.append(client['source'])
  rows=client['units'];code=bytearray(o.segments[1].length)
  for at,b in o.segments[1].chunks:code[at:at+len(b)]=b
  for f in o.fixups:
   if f.target[0]!=2 or o.externals.get(f.target[1])!='_state_8d12':continue
   if o.segments[f.segment].class_name=='DEBSYM':
    require((f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(4,3,True,(5,None),None)and f.offset==gs['_state_8d12']['offset']+2,'Move8 separate actual debug FAR')
    require(not any(pos>f.record_offset and sn==f.segment and off<f.offset+4 and f.offset<off+n for pos,sn,off,n in o.data_writes),'Move8 selected client debug field late overwrite');debugfields.append((client['source'],f.offset));continue
   require(f.segment==1 and(f.width,f.location_type,f.segment_relative,f.frame)==(2,1,True,(5,None)),'Move8 actual CODE OFFSET16')
   owners=[u for u in rows if o.function_info(u['symbol'])['offset']<=f.offset<o.function_info(u['symbol'])['end']];require(len(owners)==1,'Move8 no held/unselected referring CODE field');u=owners[0];info=o.function_info(u['symbol']);site=int(u['image_offset'],0)-info['offset']+f.offset;old=expected[site];addend=int.from_bytes(code[f.offset:f.offset+2],'little');value=(0x8d12+addend+(f.displacement or 0))&65535
   require(old['source']==client['source']and old['unit']==u['id']and old['object_offset']==f.offset and old['raw_addend']==addend and ref['image'][site:site+2]==value.to_bytes(2,'little')and u['externals']['_state_8d12']==0x8d12,'Move8 actual original native operand');actual.append(site)
  for u in rows:
   kw={k:u[k]for k in ['owned_const','owned_data','owned_bss','owned_selector_const']if u.get(k)is not None};body,fields=link_function(o,u['symbol'],int(u['image_offset'],0),u['externals'],**kw);at=int(u['image_offset'],0);require(len(body)==u['size']and body==ref['image'][at:at+u['size']],'Move8 complete selected client body');bodies+=1
   if u.get('owned_selector_const'):
    from owned_selector_const16 import validate
    descriptor,pool,proof=validate(u,o,project,ref);require(len(pool)==2 and proof['complete_CODE_bytes']==800 and proof['complete_MZ_sites']==[0x619c6],'Move8 unchanged current book selector gate');bookgates+=1
   if u.get('extended_extent',{}).get('kind')=='book_skip_8577_v1':
    from book_skip_extent import validate_book_skip_extent
    skip=validate_book_skip_extent(u,project,ref['original_sha256'],o.function_info(u['symbol']),body,source_object=o);require(skip['native_union_bytes']==22,'Move8 unchanged book skip22')
 require(len(actual)==len(set(actual))==79 and set(actual)==set(expected)and len(debugfields)==len(matched_graphs)==5 and bodies==56 and bookgates==5,'Move8 complete79/5debug/56body/book5 inventory')
 require(all(v==0 for v in [provider['new_C_DATA_IMAGE_FILE_nativeMZ_credit'],controls['new_matching_credit']]),'Move8 zero matching credit')
 return [{'symbol':'_state_8d12','dgroup_segment':'0x5cc2','dgroup_offset':'0x8d12','end_exclusive':'0x8d1a','size':8,'resolved':False,'compatible_complete_Move_graph':EXPECTED_GRAPH,'historical_physical_owner_class_TU_order_MAP_unique_capacity_proven':False,'DF_global_invariant_or_reentrancy_proven':False}]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'Move8 source hash');constraints=validate_evidence(project,item['evidence'],target)
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'Move8 fresh compiler provenance');defs=validate_object(c.object_bytes)
 out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'move8-state-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':8,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_shared_Move8_no_historical_physical_owner_class_TU_order_MAP_claim'}
