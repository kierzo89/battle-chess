"""Closed two near-pointer COMMON cells. Pointees are never allocated."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from event_pointer_profile_pins import PINS
BACKEND='msc500-near-common-event-pointers-v1'
SOURCE='src/link/event_pointer_state.c'
SOURCE_SHA='e124aca20623476372166b8cd28ad27d865020e6dcfc59af72478c80a310e72b'
OBJECT_SHA='e8863fc7ee72b22c034f1aa7cb22162fb4a3b828c977567f4e0b0e2a0a9e8d61'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_event_context','_current_event'];OFFSETS=[0x53f0,0x9882]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(x,msg):
 if not x:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'event-pointer relative input required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'event-pointer input escapes project');return p

def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown event-pointer allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('event-pointer-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'closed event-pointer source/profile required')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES]and all(type(r['size'])is int for r in item['objects']),'event-pointer exact two near-pointer2 definitions required')
 require(item['evidence']==PINS,'event-pointer evidence set/identity changed')

def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'event-pointer PUBLIC/function forbidden')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',44,32,False),('$$TYPES','DEBTYP',205,32,False)],'event-pointer loaded/debug allocation changed')
 commons=[];count=0
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'event-pointer foreign record')
  if kind==0xb0:
   count+=1;c=_Cursor(p)
   while c:commons.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'event-pointer DGROUP changed')
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','event-pointer source filename changed')
  elif kind==0x88:require(p in [bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'event-pointer directive changed')
  elif kind==0x8a:require(p==b'\0','event-pointer entry point forbidden')
 require(count==1 and commons==[{'symbol':n,'type_index':t,'datatype':0x62,'size':2}for n,t in zip(NAMES,[0x20d,0x20e])],'event-pointer exact near typed COMMON shape required')
 require(o.externals=={1:'__acrtused',2:'_event_context',3:'_current_event'},'event-pointer external names/order changed')
 require(all(seg in [5,6]for _,seg,_,_ in o.data_writes),'event-pointer initialized storage forbidden')
 require(len(o.fixups)==2,'event-pointer two debug fixups required')
 for f,(at,target)in zip(o.fixups,[(24,3),(2,2)]):require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,at,4,3,True,(5,None),(2,target),None),'event-pointer debug fixup changed')
 require(sha(data)==OBJECT_SHA,'event-pointer whole OMF/CV/pointee-view pin mismatch');return commons

def _primary(e,operation):
 p=e.get('analysis_profile',{}).get('parameters',{})
 require(e.get('subject',{}).get('digest',{}).get('sha256')==ORIGINAL_SHA256 and e.get('operation')==operation and p.get('load_segment')=='0x1000'and p.get('language_id')=='x86:LE:16:Real Mode'and p.get('target_format')=='dos-mz','event-pointer native target/profile changed')

def validate_evidence(project,pins,target):
 require(pins==PINS,'event-pointer evidence set/identity changed');payload={}
 for key,row in PINS.items():
  payload[key]=local(project,row['path']).read_bytes();require(sha(payload[key])==row['sha256'],'event-pointer evidence pin mismatch: '+key)
 proof=json.loads(payload['layout']);controls=json.loads(payload['controls']);positive=controls[0]
 require(proof['canonical_changed']is False and proof['native_matching_credit']==0 and not proof['aliases_or_existing_providers']and proof['original_sha256']==ORIGINAL_SHA256,'event-pointer native proof scope changed')
 require([x['variant']for x in controls]==['near','far','initialized','integer','wrong_pointee']and sha(payload['source_model'])==SOURCE_SHA==positive['source_sha256']and sha(payload['object'])==OBJECT_SHA==positive['object_sha256'],'event-pointer source controls/object changed');validate_object(payload['object'])
 event=b'typedef struct {int kind,code,status,reserved,x,y,data[4];} Event;';context=b'typedef struct {int words[5];int queue;} EventContext;'
 require(event in payload['source_model']and context in payload['source_model'],'event-pointer exact selected pointee views required')
 for key,name in [('event_consumer','src/event_text_match.c'),('main_consumer','src/main_input_exit_match.c')]:require(sha(payload[key])==proof['selected_source_pins'][name]and event in payload[key]and b'extern Event *current_event;'in payload[key],'event-pointer selected consumer declaration coherence changed')
 require(context in payload['event_consumer']and b'extern EventContext *event_context;'in payload['event_consumer'],'event-pointer context view changed')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'event-pointer original target pin');image=build_reference(original)['image']
 wait=json.loads(payload['native_wait']);pointer=json.loads(payload['native_pointer']);main=json.loads(payload['native_main']);crt=json.loads(payload['crt'])
 for e in [wait,pointer,main]:_primary(e,'analyze_function')
 _primary(crt,'read_bytes')
 rows=[(wait,['0x15d53: MOV BX, word ptr [0x53f0]','0x15d57: PUSH word ptr [BX + 0xa]','0x15d60: MOV [0x9882], AX']),(pointer,['0x15d85: MOV BX, word ptr [0x53f0]','0x15d89: PUSH word ptr [BX + 0xa]','0x15d92: MOV [0x9882], AX','0x15da0: MOV BX, word ptr [0x9882]']),(main,['0x10426: MOV [0x9882], AX','0x10430: MOV BX, word ptr [0x9882]'])]
 for e,ins in rows:require(all(i in e['normalized_result']['assembly']for i in ins),'event-pointer native near storage/dereference operands changed')
 exact=[(0x5d53,'8b1ef053ff770a'),(0x5d60,'a382988bd8837f0401'),(0x5d85,'8b1ef053ff770a'),(0x5d92,'a382988bd8837f0401'),(0x5da0,'8b1e8298833f05'),(0x426,'a382988bd88b07'),(0x430,'8b1e82988b4708')]
 require(proof['exact_native_opcode_checks']==[{'image_offset':a,'hex':h}for a,h in exact],'event-pointer raw native proof table changed')
 for a,h in exact:require(image[a:a+len(bytes.fromhex(h))]==bytes.fromhex(h),'event-pointer raw near pointer opcode mismatch')
 r=crt['normalized_result'];require(crt['parameters']=={'address':'0x1ea86','length':179}and r['complete']and r['requested_bytes']==r['returned_bytes']==179 and bytes.fromhex(r['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'event-pointer CRT179 clear changed')
 constraints=[]
 for row,n,off in zip(proof['constraints'],NAMES,OFFSETS):
  require(row=={'symbol':n,'size':2,'native_DS':hex(off),'native_end_exclusive':hex(off+2),'uninitialized_beyond_image':True,'original_MAP_resolved':False}and 0x52cc<=off<off+2<=0xcbe0 and 0x5cc20+off>=len(image),'event-pointer cleared uninitialized scalar bounds changed')
  constraints.append({'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+2),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'pointee_allocation_included':False,'historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True})
 require(len(constraints)==2,'event-pointer complete constraint pair required');return constraints,positive['compiler']

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();require(not any(x in str(project)for x in ['\r','\n','"']),'unsafe event-pointer project path')
 expected=project/SOURCE;require(expected.resolve()==expected,'event-pointer source alias/symlink forbidden')
 source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'event-pointer source pin mismatch')
 compiler_fn=compile_c if compiler_fn is None else compiler_fn
 c=compiler_fn(source,FLAGS,compiler='msc500',source_name='UNIT.C')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','event-pointer fresh compiler provenance changed')
 definitions=validate_object(c.object_bytes);constraints,frozen=validate_evidence(project,item['evidence'],target)
 require(c.tool_hashes==frozen['tool_hashes']and list(c.command)==frozen['command'],'event-pointer compiler tools/command changed')
 output=Path(output);output.mkdir(parents=True,exist_ok=True);objpath=output/'event-pointer-common.obj';objpath.write_bytes(c.object_bytes);provenance=dataclasses.asdict(c);provenance.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(objpath),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,'allocation_profile':'two near typed pointers; no pointee allocation','historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True,'authored_C_function_credit':0}
