"""Closed two-int input/display COMMON allocation. Zero matching credit."""
import dataclasses,hashlib,json
from pathlib import Path
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
BACKEND='msc500-near-common-input-display-v1'
SOURCE='src/link/input_display_state.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_cursor_colour_9850','_ready_9856'];OFFSETS=[0x9850,0x9856]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
SOURCE_SHA='3e9c36c6317a4524025bf814716dd84c4c9f47a4708923bf953cc36a18792667'
OBJECT_SHA='b8d5d335631d300880e96bcb5be17d2a37428785db6453d0df66189e523a3d44'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
PINS={'layout': {'path': 'build/native-state-scalars-053a/proof.json', 'sha256': '28acfee985297133255f250ff7a140ef4748711fb558b0a50f55ef33985e66c4'}, 'bounds': {'path': 'build/native-state-scalars-053a/bounds-and-ownership.json', 'sha256': 'f26ec7f3ceb1032ae0f58920eb78d8851bada2989b87112bec89b6f12d359712'}, 'frozen': {'path': 'build/native-state-scalars-053a/freeze-manifest.json', 'sha256': '4cc1566cc3eeca004c5e112d4b019acc64c3746f314c7f5e25bd94a8870106d9'}, 'cursor_read': {'path': 'build/native-state-scalars-053a/rea-cursor-word2.json', 'sha256': '92d1db3fafc39890e4eac6cc3b76d40562f79567e541f7d05f7877bc9e68d377'}, 'ready_read': {'path': 'build/native-state-scalars-053a/rea-ready-word2.json', 'sha256': '8ee3acbdca5baba6bf22a8570b35b4e96ec4395b6a6841b849c9d61860901e98'}, 'native_cursor': {'path': 'evidence/rea_obtain_input_0254_original.json', 'sha256': 'c03e3645fafa8275ce00aea6f4e8e6c20fd6a7849c5a21a0eb8add9aee77ca86'}, 'native_refresh': {'path': 'evidence/rea_chat_refresh_primary.json', 'sha256': '611059e9694f9bfab9bda2ce9cc774e474bb97d985189b242c244df9816368e3'}, 'crt': {'path': 'evidence/rea_crt_startup_500.json', 'sha256': 'f1ef14871734df318dcf05a9ea366706a46bf2484a5623678271df7cf612d1ad'}}
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
def require(v,m):
 if not v:raise ValueError(m)
def sha(v):return hashlib.sha256(v).hexdigest()
def local(project,name):
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'input-display path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'input-display fields')
 require(item['id']=='input-display-common'and item['backend']==BACKEND and item['compiler']=='msc500'and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'input-display source/profile')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES],'input-display WORD selection')
 require(item['evidence']==PINS,'input-display evidence selection')
def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'input-display PUBLIC/function forbidden')
 expected=[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',46,32),('$$TYPES','DEBTYP',0,32)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'input-display loaded/debug allocation')
 require(not any(s.unsupported_data for s in o.segments.values()),'input-display LIDATA/reservation')
 defs=[]
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'input-display foreign OMF record')
  if kind==0xb0:
   c=_Cursor(p)
   while c:
    n,t,d,s=c.name(),c.index(),c.byte(),c.byte();require((t,d,s)==(0x81,0x62,2),'input-display near signed-int COMDEF2');defs.append({'symbol':n,'size':s,'datatype':d,'type_index':t})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'input-display DGROUP')
  elif kind==0x8a:require(p==b'\0','input-display entry point')
  elif kind==0x88:require(p in[bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],'input-display directive')
 require([x['symbol']for x in defs]==NAMES,'input-display COMMON names/count/order')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'input-display external/marker')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'input-display initialized nondebug bytes')
 require(len(o.fixups)==2,'input-display debug fixup count')
 for f,(offset,target)in zip(o.fixups,[(29,3),(2,2)]):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,offset,4,3,True,(5,None),(2,target),None),'input-display exact CV field')
 require(sha(data)==OBJECT_SHA,'input-display whole genuine OMF identity');return defs

def validate_evidence(project,pins,target):
 require(OFFSETS==[0x9850,0x9856],'input-display fixed native scalar addresses');require(pins==PINS,'input-display evidence identity');payload={k:local(project,v['path']).read_bytes()for k,v in pins.items()}
 for k,v in payload.items():require(sha(v)==pins[k]['sha256'],'input-display evidence pin '+k)
 proof=json.loads(payload['layout']);trial=proof['COMMON_trials'][0]
 require(trial['name']=='pending_scalars'and trial['object_sha256']==OBJECT_SHA and trial['compiler']['source_sha256']==SOURCE_SHA and trial['initialized_bytes']==0 and trial['matching_credit']==0 and not trial['native_placement_proven']and not trial['nondebug_allocation'],'input-display proof scope')
 for key,addr in [('cursor_read','0x76470'),('ready_read','0x76476')]:
  e=json.loads(payload[key]);require(e['subject']['digest']['sha256']=='faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'and e['analysis_profile']['parameters']['load_segment']=='0x1000'and e['parameters']=={'address':addr,'length':2}and e['normalized_result']=={'address':addr,'requested_bytes':2,'returned_bytes':0,'bytes_hex':'','complete':False},'input-display incomplete native read')
 raw=Path(target).read_bytes();require(sha(raw)==ORIGINAL_SHA256,'input-display original target');ref=build_reference(raw);image=ref['image']
 for at,h in [(0x529,'ff365098'),(0x1499,'833e569800'),(0x14a3,'a35698'),(0x14a6,'833e569800')]:
  b=bytes.fromhex(h);require(image[at:at+len(b)]==b,'input-display actual native WORD operand')
 crt=json.loads(payload['crt']);b=bytes.fromhex(crt['normalized_result']['bytes_hex']);clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
 require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['parameters']=={'address':'0x1ea86','length':179}and crt['normalized_result']['complete']and b==image[0xea86:0xeb39]and image[0xeaed:0xeaed+len(clear)]==clear,'input-display actual CRT clear')
 bounds=json.loads(payload['bounds']);require(bounds['startup_clear']['DS_start']=='0x52cc'and bounds['startup_clear']['DS_end_exclusive']=='0xcbe0'and not bounds['startup_clear']['exact_historical_COMMON_order_or_native_MAP_proven'],'input-display native bounds')
 constraints=[]
 for n,off in zip(NAMES,OFFSETS):
  require(0x52cc<=off and off+2<=0xcbe0 and 0x5cc20+off>=len(image),'input-display native WORD outside initialized image')
  constraints.append({'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+2),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False})
 return constraints

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'input-display source pin')
 fn=compile_c if compiler_fn is None else compiler_fn
 # Generation must finish before any native target/evidence comparison.
 c=fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.tool_hashes==TOOLS,'input-display fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target)
 output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/'input-display-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'two_int_input_display_scalars','authored_C_function_credit':0}
