"""Closed menu-active int paused COMMON2; no initialized/function credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from menu_paused_profile_pins import PINS
BACKEND='msc500-near-common-menu-paused-v1'
SOURCE='src/link/menu_paused_state.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_paused'];OFFSETS=[0x988e]
SOURCE_SHA='91112eebaebf2b98d9b267c3dd5d788bc6b2e51133a8bac80075663492850293'
OBJECT_SHA='c8637cefb7d44da02b25cf7570e740743b54c8ca53fef64f24f3629479ad8902'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}

def require(ok,message):
 if not ok:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'menu-paused relative path required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'menu-paused path escapes project');return p

def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'menu-paused unknown allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('menu-paused-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'menu-paused closed source/profile required')
 require(item['objects']==[{'symbol':'_paused','size':2,'storage':'near-common'}],'menu-paused exact one signed-int COMMON2 required')
 require(item['evidence']==PINS,'menu-paused exact native evidence required')

def validate_object(data):
 require(isinstance(data,bytes),'menu-paused raw unchanged OMF required');o=read_omf(data)
 require(not o.publics and not o.procedures,'menu-paused no PUBLIC/function/alias definitions allowed')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',15,32,False),('$$TYPES','DEBTYP',0,32,False)],'menu-paused loaded/debug allocation changed')
 require([k for k,_,_ in o.records]==[0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0xb0,0x88,0xa0,0x9c,0x8a],'menu-paused foreign/extra record shape')
 commons=[]
 for kind,at,p in o.records:
  if kind==0xb0:
   c=_Cursor(p)
   while c:commons.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'menu-paused DGROUP changed')
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','menu-paused producer filename changed')
  elif kind==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'menu-paused producer directive changed')
  elif kind==0x8a:require(p==b'\0','menu-paused entry point forbidden')
 require(commons==[{'symbol':'_paused','type_index':0x81,'datatype':0x62,'size':2}],'menu-paused exact near signed-int2 COMDEF required')
 require(o.externals=={1:'__acrtused',2:'_paused'},'menu-paused exact external order/names required')
 require(all(s==5 for _,s,_,_ in o.data_writes),'menu-paused initialized nondebug bytes forbidden')
 require(len(o.fixups)==1,'menu-paused one exact debug field required');f=o.fixups[0]
 require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'menu-paused debug field changed')
 require(sha(data)==OBJECT_SHA,'menu-paused complete object/CV/source pin mismatch');return commons

def validate_evidence(project,pins,target):
 require(pins==PINS,'menu-paused evidence identity changed');payload={}
 for key,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'menu-paused evidence hash mismatch '+key);payload[key]=raw
 proof=json.loads(payload['layout']);require(proof['source_allocation_only']is True and proof['matching_credit']==0 and proof['canonical_changed']is False and proof['compiler_generation_reference_reads_forbidden']is True,'menu-paused original proof scope changed')
 require(sha(payload['source'])==SOURCE_SHA and sha(payload['object'])==OBJECT_SHA,'menu-paused source/object evidence changed');validate_object(payload['object'])
 require(all(d['type']=='int'and d['storage']=='extern'and d['initialized']is None for ds in proof['actual_selected_global_declarations'].values()for d in ds),'menu-paused actual selected signed-int views changed')
 require(proof['source_defined_names']==['_paused']and proof['alias_not_independently_allocated']=='_pending_input_988e'and not proof['other_existing_COMMON_anchors_unresolved_here'],'menu-paused duplicate/unknown provider review changed')
 reference=build_reference(Path(target).read_bytes());image=reference['image']
 for key in ['native_input','native_keyboard','native_search']:
  e=json.loads(payload[key]);require(e['subject']['digest']['sha256']==ORIGINAL_SHA256,'menu-paused original native primary mismatch')
 main=json.loads(payload['native_main']);require(main['subject']['digest']['sha256']==reference['carrier_sha256'],'menu-paused main carrier primary mismatch')
 native_input=json.loads(payload['native_input']);native_keyboard=json.loads(payload['native_keyboard']);native_search=json.loads(payload['native_search'])
 for instruction in ['0x1060c: MOV word ptr [0x988e], 0x1','0x10632: MOV word ptr [0x988e], 0x0']:
  require(instruction in native_input['normalized_result']['assembly'],'menu-paused open/close WORD lifecycle missing')
 require('0x1022a: MOV word ptr [0x988e], 0x0'in main['normalized_result']['assembly']and'0x11930: CMP word ptr [0x988e], 0x0'in native_keyboard['normalized_result']['assembly']and'0x1ad00: CMP word ptr [0x988e], 0x0'in native_search['normalized_result']['assembly'],'menu-paused matching WORD clients missing')
 for at,raw in [(0x22a,'c7068e980000'),(0x60c,'c7068e980100'),(0x632,'c7068e980000'),(0x1930,'833e8e9800')]:require(image[at:at+len(bytes.fromhex(raw))]==bytes.fromhex(raw),'menu-paused full original WORD opcode/operand mismatch')
 crt=json.loads(payload['crt']);require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['parameters']=={'address':'0x1ea86','length':179}and crt['normalized_result']['complete']and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'menu-paused complete native CRT179 clear mismatch')
 require(0x52cc<=0x988e<0x9890<=0xcbe0 and 0x5cc20+0x988e>=len(image),'menu-paused not wholly uninitialized CRT-cleared scalar')
 return [{'symbol':'_paused','dgroup_segment':'0x5cc2','dgroup_offset':'0x988e','end_exclusive':'0x9890','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_COMMON_order_proven':False}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'menu-paused source hash changed')
 fn=compile_c if compiler_fn is None else compiler_fn
 c=fn(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'menu-paused fresh compiler/source/tool provenance changed')
 defs=validate_object(c.object_bytes)
 # All native comparison/evidence reads intentionally follow generation.
 constraints=validate_evidence(project,item['evidence'],target)
 output=Path(output);output.mkdir(parents=True,exist_ok=True);artifact=output/'menu-paused-common.obj';artifact.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(artifact),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':2,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'one_int_menu_active_flag','authored_C_function_credit':0}
