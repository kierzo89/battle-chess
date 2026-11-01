"""Closed consumed-compatible serial COMMON4/133 input, zero matching credit.

This admits no initialized DATA, array filler or native MAP assertion. The128
ring domain is proved consumed; historical spare capacity/ownership is unknown.
"""
from pathlib import Path
import dataclasses,hashlib,json,re,struct
from msc import compile_c
from omf import read_omf,_Cursor
from library16 import link_segment
from cdata_pointer import link_pointer_data
from reference import build_reference,ORIGINAL_SHA256,CARRIER_SHA256,validate_expanded_read
from serial_ring_profile_pins import PINS
BACKEND='msc500-near-common-serial-ring-v1'
SOURCE='src/link/serial_state.c'
SOURCE_SHA='93c1e1692a5e2e006d23c996b714f07f7507f61de4ca2e5ef68a4540d5ac0435'
OBJECT_SHA='c5ca09a1d525979b70a1805ee1ed2f9a34cbd093eba5d1378f3a5f0ac0321f58'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi']
SOURCE_NAME='SCALARS.C'
NAMES=['_byte_ring_buffer','_byte_read_cursor','_byte_write_cursor','_serial_irq_flags_b0d4']
SIZES=[128,2,2,1]
TYPES=[0x204,0xa4,0xa4,0x84]
OFFSETS=[0x8b2e,0x8ae6,0x9342,0xb0d4]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}

def require(value,message):
 if not value:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def local(project,name):
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'serial input path escapes project');return p

def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown serial allocation fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('serial-ring-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'closed serial source/profile required')
 require(item['objects']==[{'symbol':n,'size':size,'storage':'near-common'}for n,size in zip(NAMES,SIZES)],'complete serial four COMMON selection required')
 require(item['evidence']==PINS,'serial evidence set/identity changed')

def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'serial COMMON forbids PUBLIC/function')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',106,32,False),('$$TYPES','DEBTYP',26,32,False)],'serial loaded/debug allocation changed')
 commons=[];count=0
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a},'serial foreign OMF record/COMM form')
  if kind==0xb0:
   count+=1;c=_Cursor(p)
   while c:
    n,typ,storage=c.name(),c.index(),c.byte();require(storage==0x62,'serial near COMMON datatype62 required')
    leaf=c.byte()
    if n=='_byte_ring_buffer':require(leaf==0x81,'serial array size uses exact numeric leaf81');size=c.word()
    else:require(leaf<=0x80,'serial scalar size must be direct');size=leaf
    commons.append({'symbol':n,'size':size,'datatype':storage,'type_index':typ})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'serial DGROUP changed')
  elif kind==0x88:require(p in [bytes.fromhex(s)for s in ['009d30734f','00a1014356','00a201']],'serial unreviewed linker directive')
  elif kind==0x8a:require(p==b'\0','serial entry point forbidden')
  elif kind==0x80:require(p==b'\x0cC:\\SCALARS.C','serial deterministic source name changed')
 require(count==1 and [r['symbol']for r in commons]==NAMES,'serial four names/order/duplicates changed')
 require([r['size']for r in commons]==SIZES and [r['type_index']for r in commons]==TYPES,'serial exact sizes/types:array128/nearByte*2/Byte1')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'serial foreign EXTDEF/startup marker')
 require(all(seg in [5,6]for _,seg,_,_ in o.data_writes),'serial initialized nondebug bytes')
 require(len(o.fixups)==4,'serial four debug fixups required')
 for f,(at,target)in zip(o.fixups,[(78,5),(52,4),(27,3),(2,2)]):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,at,4,3,True,(5,None),(2,target),None),'serial exact CV address fixup changed')
 require(sha(data)==OBJECT_SHA,'serial complete genuine OMF/debug changed')
 return commons

def _primary(e,sha256,operation):
 p=e.get('analysis_profile',{}).get('parameters',{})
 require(e.get('subject',{}).get('digest',{}).get('sha256')==sha256 and e.get('operation')==operation and p.get('load_segment')=='0x1000'and p.get('language_id')=='x86:LE:16:Real Mode'and p.get('target_format')=='dos-mz','serial native subject/profile changed')

def validate_evidence(project,pins,target):
 require(pins==PINS,'serial evidence set/identity changed');payload={}
 for key,row in PINS.items():
  payload[key]=local(project,row['path']).read_bytes();require(sha(payload[key])==row['sha256'],'serial evidence pin mismatch: '+key)
 proof=json.loads(payload['layout']);root=json.loads(payload['root_review']);require(root['freeze_sha256']==PINS['source_freeze']['sha256'],'serial reviewed source graph changed')
 source=payload['source_model'];require(sha(source)==SOURCE_SHA and sha(payload['object'])==OBJECT_SHA,'serial frozen source/object identity')
 definitions=validate_object(payload['object']);require([{k:r[k]for k in ['symbol','size','type_index']}for r in definitions]==[{k:r[k]for k in ['symbol','size','type_index']}for r in proof['common']['definitions']],'serial frozen common metadata changed')
 require(proof['generation_target_input']is False and proof['canonical_changes']is False and proof['common']['matching_byte_credit']==0 and proof['common']['placements_unresolved']and not proof['common']['historical_capacity_unique'],'serial source/credit/model scope changed')
 guard=json.loads(payload['guard']);require(not guard['target_or_reference_reads_succeeded']and len(guard['blocked_original_and_reference_reads'])==2 and guard['object_reproduction']['common']==OBJECT_SHA and guard['source_operands_changed']is False,'serial source-only generation proof changed')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'serial original target pin');ref=build_reference(original);image=ref['image']
 crt=json.loads(payload['crt']);_primary(crt,ORIGINAL_SHA256,'read_bytes');r=crt['normalized_result'];require(crt['parameters']=={'address':'0x1ea86','length':179}and r['complete']and r['requested_bytes']==r['returned_bytes']==179 and bytes.fromhex(r['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'serial nativeCRT179/clear extent')
 # Exact original I/O prefix proves initialization and +128 wrap, never an inferred array capacity.
 io=json.loads(payload['native_io']);_primary(io,ORIGINAL_SHA256,'read_bytes');r=io['normalized_result'];require(io['parameters']=={'address':'0x1db8a','length':585}and r['complete']and r['requested_bytes']==r['returned_bytes']==585 and bytes.fromhex(r['bytes_hex'])==image[0xdb8a:0xddd3],'serial exact native I/O context')
 require(image[0xdb92:0xdb9b]==bytes.fromhex('b82e8ba34293a3e68a')and image[0xdc5d:0xdc6b]==bytes.fromhex('813ee68aae8b7506c706e68a2e8b'),'serial cursor initialization/consumed128 wrap changed')
 handler=json.loads(payload['native_handler']);_primary(handler,ORIGINAL_SHA256,'read_bytes');r=handler['normalized_result'];native=bytes.fromhex(r['bytes_hex']);require(handler['parameters']=={'address':'0x20d30','length':184}and r['complete']and r['requested_bytes']==r['returned_bytes']==184 and native==image[0x10d30:0x10de8],'serial full182/native next boundary')
 require(native[0x78:0x80]==bytes.fromhex('8b1e42938b16be2e')and native[0x85:0x89]==bytes.fromhex('0806d4b0')and native[0x8f:0xa7]==bytes.fromhex('3b1eba2e7203bb2e8b3b1ee68a7509800ed4b0408b1e4293')and native[0xa7:0xab]==bytes.fromhex('891e4293'),'serial byte flag/word cursors/end pointer width/semantics changed')
 ptr=read_omf(payload['pointer_object']);data,meta=link_pointer_data(ptr,'_serial_ring_end_2eba',0x5fada,0x5cc2,{'_byte_ring_buffer':0x8b2e});e=json.loads(payload['pointer_primary']);_primary(e,CARRIER_SHA256,'read_bytes');validate_expanded_read(e,{'image_offset':'0x5fada','size':2,'reference_region':'exepack-expanded'},data,ref)
 require(data==bytes.fromhex('ae8b')and len(meta['relocations'])==1 and meta['relocations'][0]['original_addend']==128,'serial original near endpoint must be buffer+128')
 audit=json.loads(payload['audit']);require(not audit['definitions_or_aliases_or_known_provider_overlap']and not audit['unlocated_existing_COMMON']and audit['actual_common_definitions_checked']==47,'serial existing provider overlap review changed')
 require(audit['original_MAP_or_COMMON_order_claim']is False,'serial originalMAP not recovered')
 candidates={r['symbol']:r for r in audit['candidate_constraints']};constraints=[]
 for n,off,size in zip(NAMES,OFFSETS,SIZES):
  r=candidates[n];require(r['DSoffset']==off and r['size_model']==size and not r['existing_definitions']and not r['provided_overlaps']and not r['same_interval_other_aliases']and 0x52cc<=off<off+size<=0xcbe0 and 0x5cc20+off>=len(image),'serial native consumed COMMON constraint changed')
  constraints.append({'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+size),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_capacity_unique':False,'larger_aggregate_ownership_unknown':True})
 # Replay complete independent source allocation arithmetic against both real diagnostic maps.
 linked=json.loads(payload['link']);require(len(linked['runs'])==2 and linked['hardware_execution']is False and linked['selected_byte_io_C_functions_executed']is False and linked['current_matching_credit_added']==0,'serial realLINK diagnostic scope')
 modules={'STATE':read_omf(payload['object']),'POINTER':ptr,'MAIN':read_omf(payload['harness_object'])}
 for trial,order in zip(linked['runs'],[['STATE','POINTER','MAIN'],['MAIN','POINTER','STATE']]):
  prefix='-'.join(order);exe=payload[prefix+'_exe'];text=payload[prefix+'_map'].decode('cp437');require(trial['object_order']==order and trial['harness_exit_zero']and trial['original_or_carrier_read_or_mounted']is False and payload[prefix+'_pass'].strip()==b'passed'and'error L'not in payload[prefix+'_log'].decode('cp437')and sha(exe)==trial['exe_sha256']and text==trial['link_map'],'serial authentic LINK/zero/wrap evidence changed')
  header=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(header[2]-1)*512+(header[1] or 512)==len(exe)and list(header)==trial['mz_header'],'serial wholeMZ size/header')
  load=exe[header[4]*16:];ordered_sites=[struct.unpack_from('<HH',exe,header[12]+4*j)[1]*16+struct.unpack_from('<HH',exe,header[12]+4*j)[0]for j in range(header[3])];require(ordered_sites==trial['mz_sites'],'serial fullMZ sites changed');sites=sorted(ordered_sites)
  part=text.split('Publics by Name')[1].split('Publics by Value')[0];pairs=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(\S+)\s*$',part,re.M);pubs={n:[int(s,16),int(o,16)]for s,o,n in pairs};require(len(pubs)==len(pairs)and pubs==trial['publics'],'serial actual MAP symbols/aliases')
  ds=trial['dgroup'];require(all(pubs[n][0]==ds for n in NAMES),'serial actual common near frame')
  spans=sorted((pubs[n][1],size)for n,size in zip(NAMES,SIZES));require(all(a+n<=b for(a,n),(b,_)in zip(spans,spans[1:])),'serial actual common overlap')
  require(pubs['_edata'][0]==pubs['_end'][0]==ds,'serial actual CRT data frame')
  edata,end=pubs['_edata'][1],pubs['_end'][1]
  clear=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa');require(clear in load,'serial actualCRTclear instruction')
  require(all(edata<=off and off+size<=end and ds*16+off>=len(load)for off,size in spans),'serial commons must be uninitialized actual CRT region')
  actual_checks=[]
  for role,obj in modules.items():
   placements={i:[ds,0]for i,s in obj.segments.items()if s.class_name in ['CODE','DATA','CONST','BSS']}
   for i,s in obj.segments.items():
    if s.class_name not in ['CODE','DATA']or not s.length:continue
    symbols=[p for p in obj.publics.values()if p.segment==i];require(symbols,'serial unnamed loaded allocation');p=min(symbols,key=lambda p:p.offset);frame,off=pubs[p.name];placements[i]=[frame,off-p.offset]
   for i,s in obj.segments.items():
    if s.class_name not in ['CODE','DATA']or not s.length:continue
    b,fields=link_segment(obj,i,placements,{1:ds},pubs);frame,off=placements[i];at=frame*16+off;emitted=sorted(f['mz_relocation_image_offset']for f in fields if f['mz_relocation_image_offset']is not None);actual=sorted(x for x in sites if at<=x<at+len(b));require(load[at:at+len(b)]==b and emitted==actual,'serial complete actual CODE/DATA/MZ')
    actual_checks.append((role,i,len(b),b.hex(),fields,actual))
  retained=[(c['object'],c['segment'],c['complete_size'],c['complete_emitted_hex'],c['fixups'],c['actual_mz_sites'])for c in trial['complete_contributions']];require(actual_checks==retained,'serial full-contribution proof mismatch')
 return constraints,json.loads(payload['compiler'])['common']

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();expected=project/SOURCE
 require(expected.resolve()==expected,'serial source alias/symlink forbidden')
 source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'serial source pin mismatch')
 compiler_fn=compile_c if compiler_fn is None else compiler_fn
 c=compiler_fn(source,FLAGS,compiler='msc500',source_name=SOURCE_NAME)
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name==SOURCE_NAME,'serial fresh compiler provenance')
 definitions=validate_object(c.object_bytes);constraints,frozen=validate_evidence(project,item['evidence'],target)
 require(c.tool_hashes==frozen['tool_hashes']and list(c.command)==frozen['command'],'serial compiler tool/command changed')
 output=Path(output);output.mkdir(parents=True,exist_ok=True);objpath=output/'serial-ring-common.obj';objpath.write_bytes(c.object_bytes);provenance=dataclasses.asdict(c);provenance.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(objpath),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':133,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,'allocation_profile':'consumed_ring128_two_nearByte_pointers_Byteflags','historical_capacity_unique':False,'larger_aggregate_ownership_unknown':True,'authored_C_function_credit':0}
