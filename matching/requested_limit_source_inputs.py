"""Closed signed-long requested_limit COMMON4; zero matching-byte credit."""
from pathlib import Path
import dataclasses,hashlib,json,re,struct
from msc import compile_c
from omf import read_omf,_Cursor
from library16 import link_segment
from reference import build_reference,ORIGINAL_SHA256
from requested_limit_profile_pins import PINS
BACKEND='msc500-near-common-requested-limit-v1'
SOURCE='src/link/requested_limit_state.c'
SOURCE_SHA='da99c1abc1e0e3074a3798cddda487b4697f53644e3735628145da28b30112c3'
OBJECT_SHA='4164bd8498ff190cf5bfe280973760f94193ed6845169444c6d3500af0fb09de'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_requested_limit'];OFFSETS=[0x53f2]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(x,msg):
 if not x:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'requested-limit relative input required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'requested-limit input escapes project');return p

def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown requested-limit allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('requested-limit-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'closed requested-limit source/profile required')
 require(item['objects']==[{'symbol':'_requested_limit','size':4,'storage':'near-common'}],'requested-limit exact single signed-long4 definition required')
 require(item['evidence']==PINS,'requested-limit evidence set/identity changed')

def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'requested-limit PUBLIC/function forbidden')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',24,32,False),('$$TYPES','DEBTYP',0,32,False)],'requested-limit loaded/debug allocation changed')
 commons=[];count=0
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'requested-limit foreign record')
  if kind==0xb0:
   count+=1;c=_Cursor(p)
   while c:commons.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'requested-limit DGROUP changed')
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','requested-limit source filename changed')
  elif kind==0x88:require(p in [bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'requested-limit directive changed')
  elif kind==0x8a:require(p==b'\0','requested-limit entry point forbidden')
 require(count==1 and commons==[{'symbol':'_requested_limit','type_index':0x82,'datatype':0x62,'size':4}],'requested-limit exact signed-long COMMON shape required')
 require(o.externals=={1:'__acrtused',2:'_requested_limit'},'requested-limit external names/order changed')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'requested-limit initialized storage forbidden')
 require(len(o.fixups)==1,'requested-limit one debug fixup required')
 f=o.fixups[0];require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'requested-limit debug fixup changed')
 require(sha(data)==OBJECT_SHA,'requested-limit whole OMF/CV/type pin mismatch');return commons

def _primary(e,operation):
 p=e.get('analysis_profile',{}).get('parameters',{})
 require(e.get('subject',{}).get('digest',{}).get('sha256')==ORIGINAL_SHA256 and e.get('operation')==operation and p.get('load_segment')=='0x1000'and p.get('language_id')=='x86:LE:16:Real Mode'and p.get('target_format')=='dos-mz','requested-limit native target/profile changed')

def validate_evidence(project,pins,target):
 require(pins==PINS,'requested-limit evidence set/identity changed');payload={}
 for key,row in PINS.items():
  payload[key]=local(project,row['path']).read_bytes();require(sha(payload[key])==row['sha256'],'requested-limit evidence pin mismatch: '+key)
 proof=json.loads(payload['layout']);review=json.loads(payload['review']);freeze=json.loads(payload['source_freeze'])
 require(proof['canonical_changed']is False and proof['matching_credit']==0 and proof['source_allocation_only']is True and proof['compiler_generation_reference_reads_forbidden']is True,'requested-limit original proof scope changed')
 require(sha(payload['source_model'])==SOURCE_SHA and sha(payload['object'])==OBJECT_SHA and proof['compiles']['SCALARS']['source_sha256']==SOURCE_SHA and proof['compiles']['SCALARS']['object_sha256']==OBJECT_SHA,'requested-limit genuine source/object evidence changed');validate_object(payload['object'])
 require(freeze['pins'][PINS['source_model']['path']]==SOURCE_SHA and freeze['pins'][PINS['object']['path']]==OBJECT_SHA and freeze['pins'][PINS['layout']['path']]==PINS['layout']['sha256'],'requested-limit frozen proof graph mismatch')
 require(b'extern long requested_limit, limit;'in payload['consumer']and review['selected_consumer_sources']=={'src/hint_limit_turn_context_match.c':sha(payload['consumer'])},'requested-limit selected long declaration changed')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'requested-limit original target pin');ref=build_reference(original);image=ref['image']
 setter=json.loads(payload['native_set']);begin=json.loads(payload['native_begin']);crt=json.loads(payload['crt'])
 for e in [setter,begin]:_primary(e,'analyze_function')
 _primary(crt,'read_bytes')
 for instruction in ['0x189f9: MOV word ptr [0x53f2], 0x6','0x189ff: MOV word ptr [0x53f4], 0x0','0x18a2b: MOV [0x53f2], AX','0x18a2e: MOV word ptr [0x53f4], DX','0x18a47: CWD','0x18a48: MOV [0x53f2], AX','0x18a4b: MOV word ptr [0x53f4], DX']:
  require(instruction in setter['normalized_result']['assembly'],'requested-limit paired signed-long native stores changed')
 require(all(s in begin['normalized_result']['assembly']for s in ['0x18a70: MOV AX, [0x53f2]','0x18a73: MOV DX, word ptr [0x53f4]']),'requested-limit paired native reads changed')
 require(image[0x89f9:0x8a05]==bytes.fromhex('c706f2530600c706f4530000')and image[0x8a47:0x8a4f]==bytes.fromhex('99a3f2538916f453')and image[0x8a70:0x8a7e]==bytes.fromhex('a1f2538b16f453a38a8189168c81'),'requested-limit native raw long operands mismatch')
 r=crt['normalized_result'];require(crt['parameters']=={'address':'0x1ea86','length':179}and r['complete']and r['requested_bytes']==r['returned_bytes']==179 and bytes.fromhex(r['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'requested-limit CRT179 clear changed')
 require(0x52cc<=0x53f2<0x53f6<=0xcbe0 and 0x5cc20+0x53f2>=len(image),'requested-limit scalar must lie in cleared uninitialized storage')
 require(not proof['aliases_at_base']and proof['selected_consumers']==['begin_turn_8a64','set_limit_89df']and review['no_other_current_binding_anchor_inside_new_interval']is True,'requested-limit native storage/alias review changed')
 # Authenticate retained target-free two-order CRT harnesses, no rerun. Every
 # complete CODE/DATA byte and raw relocation is recalculated at actual MAP.
 harness=read_omf(payload['harness_object']);trials=proof['authentic_LINK'];require(len(trials)==2,'requested-limit two genuine trials required')
 for trial,order in zip(trials,[['SCALARS','MAIN'],['MAIN','SCALARS']]):
  prefix='-'.join(order);exe=payload[prefix+'_UNIT_EXE'];text=payload[prefix+'_UNIT_MAP'].decode('cp437');log=payload[prefix+'_LINK_LOG'].decode('cp437')
  require(trial['order']==order and trial['exit_zero']and trial['original_read_or_mounted']is False and payload[prefix+'_PASS_TXT'].strip()==b'passed'and'error L'not in log and sha(exe)==trial['exe_sha256']and sha(payload[prefix+'_UNIT_MAP'])==trial['map_sha256'],'requested-limit retained realLINK execution evidence changed')
  require(payload[prefix+'_LINK_RSP'].decode()=='+'.join(n+'.OBJ'for n in order)+'\r\nUNIT.EXE\r\nUNIT.MAP\r\nT:\\SLIBC.LIB;\r\n','requested-limit source-only link inputs changed')
  h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1]or 512)==len(exe),'requested-limit whole executable size')
  load=exe[h[4]*16:];sites=sorted(struct.unpack_from('<H',exe,h[12]+4*j)[0]+16*struct.unpack_from('<H',exe,h[12]+4*j+2)[0]for j in range(h[3]));require(sites==trial['MZ'],'requested-limit complete MZ changed')
  part=text.split('Publics by Name')[1].split('Publics by Value')[0];pairs=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',part,re.M);pubs={n:[int(s,16),int(o,16)]for s,o,n in pairs};require(pubs==trial['actual_publics']and len([n for s,o,n in pairs if n=='_requested_limit'])==1,'requested-limit actual MAP names')
  frame,edata=pubs['_edata'];ef,end=pubs['_end'];seg,off=pubs['_requested_limit'];require(frame==ef==seg and edata<=off<off+4<=end and 16*seg+off>=len(load),'requested-limit real COMMON uninitialized placement')
  clear=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa');require(load.count(clear)==1 and trial['actual_clear']==[edata,end],'requested-limit genuine CRT zero domain')
  places={1:pubs['_main'],2:pubs['_diagnostic_marker'],3:[frame,0],4:[frame,0]};code,fields=link_segment(harness,1,places,{1:frame},pubs);at=16*pubs['_main'][0]+pubs['_main'][1]
  require(load[at:at+len(code)]==code and code.hex()==trial['MAIN_complete_CODE']['hex']and fields==trial['MAIN_complete_CODE']['fields']and len(code)==trial['MAIN_complete_CODE']['size']==90 and harness.function_info('_main')['size']==89 and not any(at<=s<at+len(code)for s in sites),'requested-limit complete harness CODE/CV/tail/fields/MZ')
  data,dfields=link_segment(harness,2,places,{1:frame},pubs);da=16*pubs['_diagnostic_marker'][0]+pubs['_diagnostic_marker'][1];require(data==b'\x07\0'and load[da:da+len(data)]==data and data.hex()==trial['MAIN_DATA']['hex']and dfields==trial['MAIN_DATA']['fields'],'requested-limit complete genuine harness DATA')
  for base in [0,1,0x1000,0xffff]:
   shifted=bytearray(load)
   for site in sites:shifted[site:site+2]=((int.from_bytes(shifted[site:site+2],'little')+base)&0xffff).to_bytes(2,'little')
   require(shifted[at:at+len(code)]==code,'requested-limit four-base full harness CODE')
 constraints=[{'symbol':'_requested_limit','dgroup_segment':'0x5cc2','dgroup_offset':'0x53f2','end_exclusive':'0x53f6','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True}]
 return constraints,proof['compiles']['SCALARS']

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();require(not any(x in str(project)for x in ['\r','\n','"']),'unsafe requested-limit project path')
 expected=project/SOURCE;require(expected.resolve()==expected,'requested-limit source alias/symlink forbidden')
 source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'requested-limit source pin mismatch')
 compiler_fn=compile_c if compiler_fn is None else compiler_fn
 c=compiler_fn(source,FLAGS,compiler='msc500',source_name='UNIT.C')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','requested-limit fresh compiler provenance changed')
 definitions=validate_object(c.object_bytes);constraints,frozen=validate_evidence(project,item['evidence'],target)
 require(c.tool_hashes==frozen['tool_hashes']and list(c.command)==frozen['command'],'requested-limit compiler tools/command changed')
 output=Path(output);output.mkdir(parents=True,exist_ok=True);objpath=output/'requested-limit-common.obj';objpath.write_bytes(c.object_bytes);provenance=dataclasses.asdict(c);provenance.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(objpath),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,'allocation_profile':'signed-long scalar','historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True,'authored_C_function_credit':0}
