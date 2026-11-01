"""Closed seventeen-scalar/pointer COMMON input; no initialized matching credit."""
import dataclasses,hashlib,json,re,struct
from pathlib import Path
from msc import compile_c
from omf import read_omf,_Cursor
from library16 import link_segment
from link16 import link_function
from reference import build_reference,ORIGINAL_SHA256
from arena_snapshot_profile_pins import PINS
BACKEND='msc500-near-common-arena-snapshot-v1'
SOURCE='src/link/arena_snapshot_state.c'
SOURCE_SHA='9b53ac6250ca39b3909f4946a1a765e7bd9eecff4e5786fcbebd4d12a0ceb759'
OBJECT_SHA='cafe5091d5ed442a2a661594d3d0e048ffef71609dfc3e4a96afb907a86e313f'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_frame_data_cursor', '_frame_list_cursor', '_arena_cursor', '_checkpoint_data_933e', '_checkpoint_lists_a84e', '_checkpoint_8180', '_checkpoint_8186', '_checkpoint_936e', '_checkpoint_987e', '_checkpoint_arena_9368', '_active_data_b0ca', '_active_lists_b080', '_active_95fe', '_active_8e22', '_active_a834', '_active_964e', '_active_arena_9344']
SIZES=[2, 2, 4, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 4]
TYPES=[161, 516, 228, 161, 516, 133, 133, 133, 133, 228, 161, 516, 133, 133, 133, 133, 228]
OFFSETS=[37740, 45182, 37432, 37694, 43086, 33152, 33158, 37742, 39038, 37736, 45258, 45184, 38398, 36386, 43060, 38478, 37700]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def local(project,name):
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'arena input path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'arena unknown allocation fields')
 require(item['id']=='arena-snapshot-common'and item['backend']==BACKEND and item['compiler']=='msc500'and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'arena unreviewed source/profile')
 require(item['objects']==[{'symbol':n,'size':s,'storage':'near-common'}for n,s in zip(NAMES,SIZES)],'arena incomplete COMMON selection')
 require(item['evidence']==PINS,'arena evidence selection changed')
def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'arena COMMON PUBLIC/function forbidden')
 expected=[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',415,32),('$$TYPES','DEBTYP',26,32)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'arena loaded/debug allocation changed')
 require(not any(s.unsupported_data for s in o.segments.values()),'arena reserved/LIDATA data forbidden')
 commons=[]
 for kind,at,payload in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'arena foreign OMF record')
  if kind==0xb0:
   c=_Cursor(payload)
   while c:
    n,t,d,s=c.name(),c.index(),c.byte(),c.byte();i=len(commons)
    require(i<len(NAMES)and(n,t,d,s)==(NAMES[i],TYPES[i],0x62,SIZES[i]),'arena exact name/type/nearCOMMON/size/order required')
    commons.append({'symbol':n,'size':s,'datatype':d,'type_index':t})
  elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'arena DGROUP changed')
  elif kind==0x8a:require(payload==b'\0','arena entry point forbidden')
  elif kind==0x88:require(payload in[bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],'arena linker directive changed')
 require([r['symbol']for r in commons]==NAMES,'arena missing COMMON')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'arena external/marker changed')
 require(all(seg in(5,6)for _,seg,_,_ in o.data_writes),'arena initialized nondebug bytes')
 require(len(o.fixups)==17,'arena debug fixup count changed')
 offsets=[391,371,351,331,311,285,260,230,206,182,158,134,104,75,54,28,2]
 for f,(at,target)in zip(o.fixups,zip(offsets,range(18,1,-1))):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,at,4,3,True,(5,None),(2,target),None),'arena exact CodeView field changed')
 require(sha(data)==OBJECT_SHA,'arena whole genuine OMF changed');return commons

def validate_evidence(project,pins,target):
 require(pins==PINS,'arena evidence set/identity changed');payloads={k:local(project,r['path']).read_bytes()for k,r in pins.items()}
 for k,b in payloads.items():require(sha(b)==pins[k]['sha256'],'arena evidence pin mismatch: '+k)
 proof=json.loads(payloads['layout']);audit=json.loads(payloads['audit']);state=proof['compiles']['STATE']
 require(proof['matching_credit']==0 and proof['canonical_changed']is False and proof['game_executed']is False and proof['generation_no_target_reads_or_mounts']and proof['whole_snapshot_TU_native_layout_claim']is False,'arena diagnostic scope changed')
 require(state['source_sha256']==SOURCE_SHA and state['object_sha256']==OBJECT_SHA and sha(payloads['source_model'])==SOURCE_SHA and sha(payloads['object'])==OBJECT_SHA,'arena source/object identity')
 commons=validate_object(payloads['object']);declared=proof['COMMON_definitions']
 require(len(declared)==17 and[{k:r[k]for k in('symbol','size','datatype','type_index')}for r in declared]==commons and all(r['record_offset']==216 for r in declared),'arena raw COMMON proof changed')
 # Complete native independent bodies and scalar/pair copy fields, no byte masks.
 live=[0x936c,0xb07e,0x96,0x94,0x98,0x92];checkpoint=[0x933e,0xa84e,0x8180,0x8186,0x936e,0x987e];active=[0xb0ca,0xb080,0x95fe,0x8e22,0xa834,0x964e]
 profiles=[(0x2c46,live,checkpoint,0x9238,0x9368),(0x2c79,checkpoint,live,0x9368,0x9238),(0x2cac,live,active,0x9238,0x9344),(0x2ce0,active,live,0x9344,0x9238)]
 for i,(at,src,dst,hs,hd)in enumerate(profiles):
  e=json.loads(payloads['native'+str(i)]);p=e['analysis_profile']['parameters'];body=e['normalized_result']['procedure']['body']
  require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode'and p['target_format']=='dos-mz'and e['parameters']=={'procedure':hex(at+0x10000)}and body['contains_entry']and not body['non_contiguous']and body['total_bytes']==body['span_bytes']==51 and body['ranges']==[{'start':hex(at+0x10000),'end':hex(at+0x10000+50)}],'arena native consumer identity/extent')
 raw=Path(target).read_bytes();require(sha(raw)==ORIGINAL_SHA256,'arena original target pin');ref=build_reference(raw);image=ref['image']
 for at,src,dst,hs,hd in profiles:
  expected=b''.join(b'\xa1'+struct.pack('<H',a)+b'\xa3'+struct.pack('<H',b)for a,b in zip(src,dst))+b'\xa1'+struct.pack('<H',hs)+b'\x8b\x16'+struct.pack('<H',hs+2)+b'\xa3'+struct.pack('<H',hd)+b'\x89\x16'+struct.pack('<H',hd+2)+b'\xc3'
  require(image[at:at+51]==expected and not any(at<=x<at+51 for x in ref['relocations']),'arena exact native word/pointer copy bytes/MZ')
 crt=json.loads(payloads['crt']);p=crt['analysis_profile']['parameters'];r=crt['normalized_result']
 require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode'and crt['parameters']=={'address':'0x1ea86','length':179}and r['complete']and r['requested_bytes']==r['returned_bytes']==179 and bytes.fromhex(r['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'arena native CRT179/zero range')
 require(audit['mutual_candidate_ranges_disjoint']and audit['all_current_initialized_DATA_disjoint']and audit['private_BSS4_disjoint']and len(audit['all30_current_COMMON_constraints_disjoint'])==30,'arena reviewed provider overlap audit changed')
 constraints=[]
 for n,off,size,row in zip(NAMES,OFFSETS,SIZES,audit['providers']):
  require(row['symbol']==n and row['DS_offset']==off and row['size']==size and row['current_aliases_within_range']==[n]and 0x52cc<=off and off+size<=0xcbe0 and 0x5cc20+off>=len(image),'arena native scalar/pointer CRT constraint changed')
  constraints.append({'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+size),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False})
 modules={'STATE':read_omf(payloads['object']),'COUNTERS':read_omf(payloads['counter_object']),'SNAP':read_omf(payloads['functions_object']),'MAIN':read_omf(payloads['harness_object'])}
 for key,src,obj in [('COUNTERS','counter_source','counter_object'),('SNAP','functions_source','functions_object'),('MAIN','harness_source','harness_object')]:
  require(proof['compiles'][key]['source_sha256']==sha(payloads[src])and proof['compiles'][key]['object_sha256']==sha(payloads[obj]),'arena collateral source/object provenance')
 require(len(proof['authentic_LINK_trials'])==2,'arena requires two real object orders')
 for trial,order in zip(proof['authentic_LINK_trials'],[['STATE','COUNTERS','SNAP','MAIN'],['MAIN','SNAP','COUNTERS','STATE']]):
  prefix='-'.join(order);exe=payloads[prefix+'_exe'];text=payloads[prefix+'_map'].decode('cp437').replace('\r\n','\n')
  require(trial['order']==order and trial['command']=='T:\\LINK /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP @LINK.RSP'and trial['original_or_reference_read_or_mounted']is False and trial['execution_exit_zero']and payloads[prefix+'_pass'].strip()==b'passed'and'error L'not in payloads[prefix+'_linklog'].decode('cp437')and sha(exe)==trial['exe_sha256']and text==trial['MAP'],'arena genuine executed LINK proof')
  h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1] or 512)==len(exe),'arena complete MZ executable size');load=exe[h[4]*16:];sites=sorted(struct.unpack_from('<H',exe,h[12]+4*j+2)[0]*16+struct.unpack_from('<H',exe,h[12]+4*j)[0]for j in range(h[3]));require(sites==trial['MZ_sites']and list(h)==trial['MZ_header'],'arena full MZ header/sites')
  part=text.split('Publics by Name')[1].split('Publics by Value')[0];pairs=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',part,re.M);pubs={n:[int(s,16),int(o,16)]for s,o,n in pairs};require(len(pubs)==len(pairs),'arena duplicate MAP public')
  frame,edata=pubs['_edata'];ef,end=pubs['_end'];require(ef==frame and trial['CRTzero_range']==[edata,end],'arena actual CRTclear extent');clear=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa');at=trial['CRTzero_instruction_image'];require(load[at:at+len(clear)]==clear,'arena actual CRTclear instruction')
  allocs=[]
  for n,size in zip(NAMES,SIZES):
   seg,off=pubs[n];where=16*seg+off;require(seg==frame and edata<=off and off+size<=end and where>=len(load)and not any(where<=x<where+size for x in sites),'arena COMMON must be wholly uninitialized CRT storage');allocs.append({'symbol':n,'size':size,'actual_MAP':[seg,off]})
  require(allocs==trial['actual_COMMON_allocations'],'arena actual allocation metadata');positions=sorted((x['actual_MAP'][1],x['size'])for x in allocs);require(all(a+n<=b for(a,n),(b,_)in zip(positions,positions[1:])),'arena actual COMMON overlap')
  emitted=[]
  for key,obj in modules.items():
   placements={i:[frame,0]for i,s in obj.segments.items()if s.class_name in ['CODE','DATA','CONST','BSS']}
   for i,s in obj.segments.items():
    if s.class_name not in ['CODE','DATA','CONST','BSS']or not s.length:continue
    pubs_here=[p for p in obj.publics.values()if p.segment==i];require(bool(pubs_here),'arena unexplained loaded allocation');pub=min(pubs_here,key=lambda x:x.offset);seg,offset=pubs[pub.name];placements[i]=[seg,offset-pub.offset]
   for i,s in obj.segments.items():
    if s.class_name not in ['CODE','DATA','CONST','BSS']or not s.length:continue
    data,fields=link_segment(obj,i,placements,{1:frame},pubs);seg,off=placements[i];at=16*seg+off;expected=sorted(f['mz_relocation_image_offset']for f in fields if f['mz_relocation_image_offset']is not None);actual=sorted(x for x in sites if at<=x<at+len(data));require(load[at:at+len(data)]==data and actual==expected,'arena complete independently linked source contribution/MZ')
    emitted.append((key,i,len(data),data.hex(),fields,actual))
  retained=[(x['object'],x['segment'],x['size'],x['hex'],x['fields'],x['MZ_sites'])for x in trial['complete_source_contributions']];require(emitted==retained,'arena collateral full CODE/DATA metadata changed')
 bindings=dict(zip(NAMES,OFFSETS))|{'_count_0096':0x96,'_count_0094':0x94,'_frame_count':0x98,'_frame_list_count':0x92}
 for n,at in [('_save_arena_state',0x2c46),('_restore_arena_state',0x2c79),('_save_active_arena',0x2cac),('_restore_active_arena',0x2ce0)]:
  data,fields=link_function(modules['SNAP'],n,at,bindings);require(len(data)==51 and data==image[at:at+51]and not any(f.get('mz_segment_relocation_image_offset')is not None for f in fields),'arena complete independent native snapshot function mismatch')
 return constraints,proof

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'arena source pin mismatch');compiler_fn=compile_c if compiler_fn is None else compiler_fn
 c=compiler_fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','arena fresh compiler provenance')
 definitions=validate_object(c.object_bytes);constraints,proof=validate_evidence(project,item['evidence'],target);require(c.tool_hashes==proof['compiles']['STATE']['tool_hashes']and list(c.command)==proof['compiles']['STATE']['command'],'arena compiler tool/command changed');output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/'arena-snapshot-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return{'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':40,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'seventeen_arena_snapshot_scalar_pointer_fields','authored_C_function_credit':0}
