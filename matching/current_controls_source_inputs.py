"""Closed current_controls near-pointer union COMMON4; no matching credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from current_controls_profile_pins import PINS
BACKEND='msc500-near-common-current-controls-v1'
SOURCE='src/link/current_controls_state.c'
SOURCE_SHA='21e985248a3fdd1bd3dffc51f02d215ae7ad2024fc38a0dab915f5ce861d46a2'
OBJECT_SHA='849fee4a654d2a6642dcdf1cfa28da6998b3b2ab781269334bbc2a0b10dce0a6'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_current_controls'];OFFSETS=[0xb0ce]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(x,msg):
 if not x:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'current-controls relative input required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'current-controls input escapes project');return p

def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown current-controls allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('current-controls-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'closed current-controls source/profile required')
 require(item['objects']==[{'symbol':'_current_controls','size':4,'storage':'near-common'}],'current-controls exact single union4 definition required')
 require(item['evidence']==PINS,'current-controls evidence set/identity changed')

def validate_object(data):
 o=read_omf(data)
 require(not o.publics and not o.procedures,'current-controls PUBLIC/function forbidden')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',25,32,False),('$$TYPES','DEBTYP',119,32,False)],'current-controls loaded/debug allocation changed')
 commons=[];count=0
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'current-controls foreign record')
  if kind==0xb0:
   count+=1;c=_Cursor(p)
   while c:commons.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'current-controls DGROUP changed')
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','current-controls source filename changed')
  elif kind==0x88:require(p in [bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'current-controls directive changed')
  elif kind==0x8a:require(p==b'\0','current-controls entry point forbidden')
 require(count==1 and commons==[{'symbol':'_current_controls','type_index':0x208,'datatype':0x62,'size':4}],'current-controls exact near union COMMON shape required')
 require(o.externals=={1:'__acrtused',2:'_current_controls'},'current-controls external names/order changed')
 require(all(seg in [5,6]for _,seg,_,_ in o.data_writes),'current-controls initialized storage forbidden')
 require(len(o.fixups)==1,'current-controls one debug fixup required')
 f=o.fixups[0];require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'current-controls debug fixup changed')
 require(sha(data)==OBJECT_SHA,'current-controls whole OMF/CV/union member pin mismatch')
 return commons

def _primary(e,operation):
 p=e.get('analysis_profile',{}).get('parameters',{})
 require(e.get('subject',{}).get('digest',{}).get('sha256')==ORIGINAL_SHA256 and e.get('operation')==operation and p.get('load_segment')=='0x1000'and p.get('language_id')=='x86:LE:16:Real Mode'and p.get('target_format')=='dos-mz','current-controls native target/profile changed')

def validate_evidence(project,pins,target):
 require(pins==PINS,'current-controls evidence set/identity changed');payload={}
 for key,row in PINS.items():
  payload[key]=local(project,row['path']).read_bytes();require(sha(payload[key])==row['sha256'],'current-controls evidence pin mismatch: '+key)
 review=json.loads(payload['review']);root=json.loads(payload['root_freeze']);positive=review['trials'][0]
 require(review['canonical_changes']is False and review['matching_credit']==0 and review['initialized_bytes']==0 and review['native_MAP_placement_proven']is False and review['ordinary_source_provider_proven']is True,'current-controls proof scope changed')
 require([r['variant']for r in review['trials']]==['near','far','initialized']and positive['source_sha256']==SOURCE_SHA and positive['object_sha256']==OBJECT_SHA,'current-controls source controls changed')
 require(sha(payload['source_model'])==SOURCE_SHA and sha(payload['object'])==OBJECT_SHA,'current-controls source/object evidence changed');validate_object(payload['object'])
 union=b'typedef union {struct {Byte *left,*right;} named;Byte *by_side[2];} CurrentControls;'
 require(union in payload['source_model'],'current-controls genuine near union source required')
 for key,name in [('arena_consumer','src/asset_arena_flow_match.c'),('command_consumer','src/command_task_flow_match.c')]:
  require(sha(payload[key])==review['selected_source_pins'][name]==root['pins'][name] and union in payload[key]and b'extern CurrentControls current_controls;'in payload[key],'current-controls selected consumer type coherence changed')
 require(root['pins'][PINS['review']['path']]==PINS['review']['sha256']and root['pins'][PINS['source_model']['path']]==SOURCE_SHA and root['pins'][PINS['object']['path']]==OBJECT_SHA,'current-controls reviewed graph mismatch')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'current-controls original target pin');ref=build_reference(original);image=ref['image']
 manager=json.loads(payload['native_manager']);animation=json.loads(payload['native_animation']);crt=json.loads(payload['crt'])
 for e in [manager,animation]:_primary(e,'analyze_function')
 _primary(crt,'read_bytes')
 expected_manager=['0x1379f: MOV [0xb0ce], AX','0x137b2: MOV [0xb0d0], AX']
 require(all(s in manager['normalized_result']['assembly']for s in expected_manager),'current-controls two native word writes changed')
 require(image[0x379f:0x37a2]==bytes.fromhex('a3ceb0')and image[0x37b2:0x37b5]==bytes.fromhex('a3d0b0'),'current-controls native two-pointer word stores mismatch')
 instructions=['0x16430: MOV BL, byte ptr [BP + -0x4]','0x16433: SUB BH, BH','0x16435: SHL BX, 0x1','0x16437: MOV AX, word ptr [BX + 0xb0ce]']
 require(all(s in animation['normalized_result']['assembly']for s in instructions),'current-controls indexed near-word read changed')
 require(image[0x6430:0x643b]==bytes.fromhex('8a5efc2affd1e38b87ceb0'),'current-controls raw indexed two-byte stride mismatch')
 r=crt['normalized_result'];require(crt['parameters']=={'address':'0x1ea86','length':179}and r['complete']and r['requested_bytes']==r['returned_bytes']==179 and bytes.fromhex(r['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'current-controls CRT179 clear changed')
 require(0x52cc<=0xb0ce<0xb0d2<=0xcbe0 and 0x5cc20+0xb0ce>=len(image),'current-controls full union must be uninitialized cleared native extent')
 require(review['CRT_clear_bound']['provider_minimum_start']=='0xb0ce'and review['CRT_clear_bound']['provider_minimum_end_exclusive']=='0xb0d2'and review['CRT_clear_bound']['outside_initialized_image']is True,'current-controls storage extent changed')
 constraints=[{'symbol':'_current_controls','dgroup_segment':'0x5cc2','dgroup_offset':'0xb0ce','end_exclusive':'0xb0d2','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True}]
 return constraints,positive['compiler']

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();require(not any(x in str(project)for x in ['\r','\n','"']),'unsafe current-controls project path')
 expected=project/SOURCE;require(expected.resolve()==expected,'current-controls source alias/symlink forbidden')
 source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'current-controls source pin mismatch')
 compiler_fn=compile_c if compiler_fn is None else compiler_fn
 # Generation precedes any target/reference read. Evidence is comparison-only.
 c=compiler_fn(source,FLAGS,compiler='msc500',source_name='UNIT.C')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','current-controls fresh compiler provenance changed')
 definitions=validate_object(c.object_bytes);constraints,frozen=validate_evidence(project,item['evidence'],target)
 require(c.tool_hashes==frozen['tool_hashes']and list(c.command)==frozen['command'],'current-controls compiler tools/command changed')
 output=Path(output);output.mkdir(parents=True,exist_ok=True);objpath=output/'current-controls-common.obj';objpath.write_bytes(c.object_bytes);provenance=dataclasses.asdict(c);provenance.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(objpath),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,'allocation_profile':'nearByte-pointer union named.left/right and by_side2','historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True,'authored_C_function_credit':0}
