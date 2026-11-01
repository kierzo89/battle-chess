"""Closed one-BYTE packedpen COMMON; no alias/sentinel/array allocation or credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256,validate_expanded_read
from packed_pen_profile_pins import PINS
BACKEND='msc500-near-common-packed-pen-v1'
SOURCE='src/link/packed_pen_state.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_packed_pen']
SOURCE_SHA='42fe71b2aacc0f30e592c44a580e9ea1bc4bf590b9c8b1e0265f40a88e964845'
OBJECT_SHA='20d604811d236d891589b6d497cc8d41bd13e41ebdb52ff75ce16098bac0bd1a'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR':'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a','CL.EXE':'11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504','C1.EXE':'3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791','C1.ERR':'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233','C2.EXE':'19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1','C3.EXE':'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669','C23.ERR':'75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'packedpen relative path required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'packedpen path escapes project');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'packedpen unknown allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('packed-pen-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'packedpen closed source/profile required')
 require(item['objects']==[{'symbol':'_packed_pen','size':1,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'packedpen exact one BYTE COMMON required')
 require(item['evidence']==PINS,'packedpen exact native evidence required')
def validate_object(data):
 require(isinstance(data,bytes),'packedpen raw unchanged OMF required');o=read_omf(data)
 require(not o.publics and not o.procedures,'packedpen no PUBLIC/function/alias allowed')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',19,32,False),('$$TYPES','DEBTYP',0,32,False)],'packedpen loaded/debug allocation changed')
 require([k for k,_,_ in o.records]==[0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0xb0,0x88,0xa0,0x9c,0x8a],'packedpen foreign/extra record shape')
 commons=[]
 for kind,at,p in o.records:
  if kind==0xb0:
   c=_Cursor(p)
   while c:commons.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'packedpen DGROUP changed')
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','packedpen producer filename changed')
  elif kind==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'packedpen producer directive changed')
  elif kind==0x8a:require(p==b'\0','packedpen entry point forbidden')
 require(commons==[{'symbol':'_packed_pen','type_index':0x84,'datatype':0x62,'size':1}],'packedpen exact near unsignedBYTE1 COMDEF required')
 require(o.externals=={1:'__acrtused',2:'_packed_pen'},'packedpen exact external order/names required')
 require(all(s==5 for _,s,_,_ in o.data_writes),'packedpen initialized nondebug bytes forbidden')
 require(len(o.fixups)==1,'packedpen one exact debug field required');f=o.fixups[0]
 require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'packedpen debug field changed')
 require(o.segments[5].chunks==[(0,bytes.fromhex('12050000000084000a7061636b65645f70656e'))],'packedpen exact builtintype/debug record required')
 require(sha(data)==OBJECT_SHA,'packedpen complete object/CV/source pin mismatch');return commons

def validate_evidence(project,pins,target):
 require(pins==PINS,'packedpen evidence identity changed');payload={}
 for key,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'packedpen evidence hash mismatch '+key);payload[key]=raw
 require(sha(payload['source'])==SOURCE_SHA and sha(payload['object'])==OBJECT_SHA,'packedpen source/object evidence changed');validate_object(payload['object'])
 proof=json.loads(payload['layout']);ownership=json.loads(payload['ownership'])
 require(proof['status']=='PASS'and proof['canonical_changes']is False and proof['matching_credit']==0 and proof['provider_loaded_allocation']==0,'packedpen actual source proof scope changed')
 require(proof['COMMON_provider'][0]['symbol']=='_packed_pen'and proof['COMMON_provider'][0]['size']==1 and len(proof['COMMON_provider'])==1,'packedpen one actualprovider required')
 require(ownership['native_evidence']['read_or_write_memory_at_8172_by_search_comparison']is False and ownership['source_solution']['definitions_for_old_aliases']is False and ownership['source_solution']['nearCOMMON_bytes']==1,'packedpen addresssentinel/onebyteownership scope changed')
 require(ownership['consumed_search_frame_pointer']['historical_array_capacity_proved']is False,'packedpen cannot grant searcharraycapacity')
 ref=build_reference(Path(target).read_bytes());image=ref['image']
 for key in ['search','plot','crt']:
  e=json.loads(payload[key]);require(e['subject']['digest']['sha256']==ORIGINAL_SHA256,'packedpen original native primary mismatch')
 require('0x1a80f: CMP word ptr [0x5c4], 0x8172'in json.loads(payload['search'])['normalized_result']['assembly'],'packedpen nativeaddresslimit instruction missing')
 require('0x15ad7: AND CL, byte ptr [0x8172]'in json.loads(payload['plot'])['normalized_result']['assembly'],'packedpen nativeBYTEread missing')
 require(image[0xa80f:0xa815]==bytes.fromhex('813ec4057281')and image[0x5ad7:0x5adb]==bytes.fromhex('220e7281'),'packedpen originalpointercomparison/BYTEread mismatch')
 require(image[0x5cc20+0x5c4:0x5cc20+0x5c4+2]==bytes.fromhex('d257'),'packedpen searchpointerinitializer changed')
 # Complete independently retained carrierread authenticates pen37 and actualBYTEwrite without reading targets duringgeneration.
 e=json.loads(payload['pen_code']);validate_expanded_read(e,dict(image_offset='0x5b18',size=560,reference_region='exepack-expanded'),image[0x5b18:0x5d48],ref,emitted_mz_sites=[])
 require(image[0x5b18:0x5b3d].count(bytes.fromhex('7281'))==1,'packedpen nativeBYTEstore address changed')
 crt=json.loads(payload['crt']);require(crt['parameters']=={'address':'0x1ea86','length':179}and crt['normalized_result']['complete']and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'packedpen complete CRT179clear mismatch')
 require(0x52cc<=0x8172<0x8173<=0xcbe0 and 0x5cc20+0x8172>=len(image),'packedpen not wholly uninitialized CRTcleared BYTE')
 return [{'symbol':'_packed_pen','dgroup_segment':'0x5cc2','dgroup_offset':'0x8172','end_exclusive':'0x8173','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_COMMON_order_proven':False,'search_array_capacity_proven':False}]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'packedpen source hash changed')
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'packedpen fresh compiler/source/tool provenance changed')
 defs=validate_object(c.object_bytes)
 constraints=validate_evidence(project,item['evidence'],target) # All targetcomparison reads follow source-onlygeneration.
 output=Path(output);output.mkdir(parents=True,exist_ok=True);artifact=output/'packed-pen-common.obj';artifact.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(artifact),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':1,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'one_unsignedBYTE_packed_pen_no_sentinelallocation','authored_C_function_credit':0}
