"""Closed far COMMON model of native advertised capacities; no placement/byte credit."""
from pathlib import Path
import dataclasses,hashlib,json,re,struct
from msc import compile_c
from omf import read_omf,_Cursor
from reference import ORIGINAL_SHA256
from far_capacity_profile_pins import PINS,TOOLS
BACKEND='msc500-far-common-native-capacity-model-v1';SOURCE='src/link/far_capacity_state.c';NAMES=['_asset_buffer','_decoded_arena'];FLAGS=['/AS','/Zl','/Zi']
SOURCE_SHA='33e6aee719ce7501cb1e73b547fd0eb31e6479f17c7621d59751a4688dfcd6ab';OBJECT_SHA='aa1f2a781c21006040430270eb0b2a297ded7e6fa185ddd758a98a27e5748c01';MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'far model relative path');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'far model path escape');return p
def debug(o,klass):
 s=next(s for s in o.segments.values()if s.class_name==klass);b=bytearray(s.length);seen=set()
 for at,x in s.chunks:require(0<=at<=at+len(x)<=s.length,'far model debug bounds');b[at:at+len(x)]=x;seen.update(range(at,at+len(x)))
 require(len(seen)==s.length and not s.unsupported_data,'far model incomplete debug');return bytes(b)
def number(q):
 leaf=q.byte();require(leaf<=0x80 or leaf in [0x81,0x84,0x88],'far model communal numeric leaf');return leaf if leaf<=0x80 else int.from_bytes(q.take({0x81:2,0x84:3,0x88:4}[leaf]),'little')
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'far model exact registry schema')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('native-capacity-far-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'far model exact source/compiler profile')
 require(item['objects']==[{'symbol':'_asset_buffer','size':70000,'storage':'far-common'},{'symbol':'_decoded_arena','size':150000,'storage':'far-common'}]and all(type(x['size'])is int for x in item['objects']),'far model exact conditional capacities');require(item['evidence']==PINS,'far model exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'far model whole raw object');o=read_omf(raw);require(not o.publics and not o.procedures,'far model no PUBLIC/procedure/alias')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',43,32),('$$TYPES','DEBTYP',36,32)],'far model empty loaded segments/exact debug')
 defs=[];records=0
 for k,at,p in o.records:
  require(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a},'far model unsupported OMF record')
  if k==0xb0:
   records+=1;q=_Cursor(p)
   while q:
    n,t,dt=q.name(),q.index(),q.byte();require(dt==0x61,'far model FAR61 COMMON required');count,element=number(q),number(q);defs.append({'symbol':n,'type_index':t,'communal_kind':dt,'element_count':count,'element_bytes':element,'size':count*element,'storage':'far-common'})
  elif k==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'far model unsupported COMMENT')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'far model exact group')
  elif k==0x8a:require(p==b'\0','far model no entry point')
 require(records==1 and defs==[{'symbol':'_asset_buffer','type_index':0x203,'communal_kind':0x61,'element_count':70000,'element_bytes':1,'size':70000,'storage':'far-common'},{'symbol':'_decoded_arena','type_index':0x204,'communal_kind':0x61,'element_count':150000,'element_bytes':1,'size':150000,'storage':'far-common'}],'far model exact count times element sizes')
 require(o.externals=={1:'__acrtused',2:'_asset_buffer',3:'_decoded_arena'},'far model exact externals')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,23,4,3,True,(5,None),(2,3),None),(5,2,4,3,True,(5,None),(2,2),None)],'far model only two debug FAR fields')
 require(all(s in[5,6]for _,s,_,_ in o.data_writes),'far model no initialized loaded bytes')
 require(debug(o,'DEBSYM').hex()=='14050000000003020c61737365745f62756666657215050000000004020d6465636f6465645f6172656e61','far model exact debug names/types')
 require(debug(o,'DEBTYP').hex()=='0101008001010080010100800109007886808b08008380000109007886804f1200838000','far model complete large unsigned-byte array types')
 require(sha(raw)==OBJECT_SHA,'far model whole object fingerprint');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'far model exact evidence');p={}
 for key,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'far model evidence pin '+key);p[key]=b
 model=json.loads(p['model']);linked=json.loads(p['LINK_result']);ledger=json.loads(p['bound_ledger']);gen=json.loads(p['generation'])
 require(model['status']=='PASS conditional native-capacity reconstruction model and relative LINK geometry; absolute/full-image credit HELD'and all(x['pass']for x in model['checks']),'far model closed review')
 require(ledger['status'].startswith('HELD')and ledger['native_capacity_constants']['bank_unsigned_checked_limit']==70000 and ledger['native_capacity_constants']['bank_equality_accepted']and ledger['native_capacity_constants']['arena_main_initialized_long']==150000,'far model advertised capacities distinct from physical minima')
 require(model['old_physical_bounds_unchanged']=={'bank':[65239,70000],'arena':[57230,150000],'status':'HELD exact historical physical extents/highwater'}and all(v==0 for v in model['credit'].values()),'far model no highwater/credit claim')
 require(gen['object_sha256']==OBJECT_SHA and gen['source_sha256']==SOURCE_SHA and sha(p['source_model'])==SOURCE_SHA,'far model producer source identity');validate_object(p['producer_object'])
 require(linked['objects']==228 and linked['LINK_runs']==1 and linked['removed']==NAMES and not linked['added']and len(linked['undefined'])==154 and linked['unchanged_whole_objects']and linked['stub_definitions']==0 and not linked['partial_executable_executed']and not linked['original_input_or_mount'],'far model actual real-source LINK scope')
 require(sha(p['partial_exe'])==linked['artifacts']['PARTIAL.EXE']and sha(p['partial_map'])==linked['artifacts']['PARTIAL.MAP'],'far model actual artifacts')
 txt=p['partial_map'].decode();part=txt.split('Publics by Name')[1].split('Publics by Value')[0];pub={n:(int(s,16),int(o,16))for s,o,n in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(\S+)\s*$',part,re.M)};dg=int(re.search(r'^\s*([0-9A-F]{4}):0\s+DGROUP',txt,re.M)[1],16);at=lambda n:pub[n][0]*16+pub[n][1];a,b,c=at(NAMES[0]),at(NAMES[1]),dg*16
 require(pub[NAMES[0]][1]==pub[NAMES[1]][1]==0 and b-a==70000 and c-b==150000 and a!=0x270c0 and 0x270c0-a==0x38230-b==0x5cc20-c,'far model real relative geometry; absolute unproved')
 exe=p['partial_exe'];h=struct.unpack_from('<14H',exe);require((h[2]-1)*512+(h[1]or 512)==len(exe),'far model whole partial file length');image=exe[h[4]*16:];mz=[struct.unpack_from('<H',exe,h[12]+4*i)[0]+16*struct.unpack_from('<H',exe,h[12]+4*i+2)[0]for i in range(h[3])];require(c<=len(image)and image[a:c]==bytes(220000),'far model actual source file zero span, zero matching credit')
 native=Path(target).read_bytes();require(sha(native)==ORIGINAL_SHA256,'far model original identity');native=native[struct.unpack_from('<H',native,8)[0]*16:]
 mapping={'load_asset_bank_2525':('client_bank','_load_asset_bank',0x2525),'cache_asset_frame_3652':('client_arena','_cache_asset_frame',0x3652),'initialize_asset_storage_28ae':('client_storage','_initialize_asset_storage',0x28ae),'manage_asset_arena_3713':('client_arena','_manage_asset_arena',0x3713)}
 rows=model['actual_native_selector_fields'];require(sorted(int(r['native_site'],16)for r in rows)==[0x25e2,0x29a4,0x36b8,0x371f,0x38fa,0x3a72],'far model exact all six original sites')
 for r in rows:
  key,symbol,nb=mapping[r['unit']];obj=read_omf(p[key]);matches=[f for f in obj.fixups if f.segment==1 and f.raw.hex()==r['raw_FIXUPP']and f.target[0]==2 and obj.externals[f.target[1]]==r['symbol']];require(len(matches)==1,'far model actual raw BASE field');f=matches[0];require(f.location_type==2 and f.width==2 and f.segment_relative,'far model actual BASE16 kind')
  origin=nb-obj.publics[symbol].offset;ns=origin+f.offset;site=at(symbol)+f.offset-obj.publics[symbol].offset;require(ns==int(r['native_site'],16)and site==int(r['actual_site'],16),'far model actual function/field placements')
  require(int.from_bytes(native[ns:ns+2],'little')==int(r['native_selector'],16)and int.from_bytes(image[site:site+2],'little')==pub[r['symbol']][0]and mz.count(site)==1,'far model actual original selector and partial MZ')
  require(sha(p[key])in[r['sha256']for r in linked['input_objects']],'far model unchanged whole actual consumer')
 require(b'extern unsigned char huge asset_buffer[];'in p['bank_source']and b'extern unsigned char huge asset_buffer[];'in p['arena_source']and b'extern Byte huge decoded_arena[];'in p['arena_source']and b'extern Byte huge decoded_arena[];'in p['storage_source'],'far model actual huge-array consumer declarations')
 return [{'symbol':'_asset_buffer','size':70000,'required_image_base':'0x270c0','next_required_anchor':'0x38230','resolved':False,'conditional_native_capacity_model':True,'observed_highwater_or_unique_historical_extent_proven':False},{'symbol':'_decoded_arena','size':150000,'required_image_base':'0x38230','next_required_anchor':'0x5cc20','resolved':False,'conditional_native_capacity_model':True,'observed_highwater_or_unique_historical_extent_proven':False}]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();src=local(project,SOURCE);before=src.read_bytes();require(sha(before)==SOURCE_SHA,'far model source hash');c=(compile_c if compiler_fn is None else compiler_fn)(src,FLAGS,compiler='msc500')
 require(src.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'far model fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'native-capacity-far-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':220000,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'conditional_native_capacity_model','COMMON_kind':'far','logical_extent_model_only':True}
