"""Closed two unsigned-long near COMMON definitions; zero loaded/matched credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from input_timer_profile_pins import PINS
BACKEND='msc500-near-common-input-timer-pair-v1'
SOURCE='src/link/input_timer_state.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_current_ticks_9884','_last_event_ticks_b07a']
OFFSETS={'_current_ticks_9884':0x9884,'_last_event_ticks_b07a':0xb07a}
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
SOURCE_SHA='bd8c018fe9a01d9eeb88a9e83a3027b17919d0d66fe72cecb7c20bd3c97d31a9'
OBJECT_SHA='c2ba57795b5671f3654e6f38fcfa544f3c0bcc8330a396a113410b4dc718ba32'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
CLIENT_OBJECTS={'src/dialog_saved_game_context_match.c': 'build/coherent454-packed-canonical-validation/fresh-output/objects/msc500-1c9f6a20814ad2f4-a24fc804.obj', 'src/next_event_184d_match.c': 'build/coherent454-packed-canonical-validation/fresh-output/objects/msc500-b0d3f2bd36c36aeb-e6eaca7e.obj', 'src/input_wait_command_context_match.c': 'build/coherent454-packed-canonical-validation/fresh-output/objects/msc500-2c88e7578a2e50e2-e6eaca7e.obj'}
DEBUG_BYTES='1a050000000086001263757272656e745f7469636b735f393838341d05000000008600156c6173745f6576656e745f7469636b735f62303761'

def require(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'inputtimer relative path required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'inputtimer path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'inputtimer exact fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('input-timer-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'inputtimer closed source/profile')
 expected=[{'symbol':n,'size':4,'storage':'near-common'}for n in NAMES]
 require(item['objects']==expected and all(type(x['size'])is int for x in item['objects']),'inputtimer exact two LONG4 selections')
 require(item['evidence']==PINS,'inputtimer evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'inputtimer unchanged raw bytes required');o=read_omf(raw)
 require(not o.publics and not o.procedures,'inputtimer PUBLIC/alias/function forbidden')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',57,32,False),('$$TYPES','DEBTYP',0,32,False)],'inputtimer exact loaded/debug allocations')
 require([k for k,_,_ in o.records]==[0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0xb0,0x88,0xa0,0x9c,0x8a],'inputtimer exact record shape')
 defs=[];record_count=0
 for k,at,p in o.records:
  if k==0xb0:
   record_count+=1;q=_Cursor(p)
   while q:defs.append({'symbol':q.name(),'type_index':q.index(),'datatype':q.byte(),'size':q.byte()})
  elif k==0x80:require(p==b'\x09C:\\UNIT.C','inputtimer producer filename')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'inputtimer DGROUP')
  elif k==0x88:require(p in[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'inputtimer producer directive')
  elif k==0x8a:require(p==b'\0','inputtimer entrypoint forbidden')
 require(record_count==1 and defs==[{'symbol':n,'type_index':0x86,'datatype':0x62,'size':4}for n in NAMES],'inputtimer one COMDEF record/two unsignedlong4 definitions')
 require(o.externals=={1:'__acrtused',2:NAMES[0],3:NAMES[1]},'inputtimer external names/order')
 require(all(s==5 for _,s,_,_ in o.data_writes),'inputtimer initialized nondebug data forbidden')
 require(len(o.fixups)==2 and [(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,29,4,3,True,(5,None),(2,3),None),(5,2,4,3,True,(5,None),(2,2),None)],'inputtimer two exact debug-only fields')
 require(o.segments[5].chunks==[(0,bytes.fromhex(DEBUG_BYTES))],'inputtimer complete builtin unsignedlong debug records')
 require(sha(raw)==OBJECT_SHA,'inputtimer complete object/source/type fingerprint');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'inputtimer exact evidence identity');payload={}
 for key,row in PINS.items():
  payload[key]=local(project,row['path']).read_bytes();require(sha(payload[key])==row['sha256'],'inputtimer evidence pin '+key)
 review=json.loads(payload['review']);controls=json.loads(payload['compiler_controls'])
 require(review['status']=='PASS'and review['runtime_WORD_field_count']==26 and review['DEBSYM_field_count']==6 and review['provided_name_overlap']==[]and review['initialized_DATA_overlap']==[]and review['native_anchored_COMMON_overlap']==[],'inputtimer26 runtime/6 debug/nonoverlap scope')
 require(review['historical_adjacency_or_TU_or_MAP_proven']is False and review['both_ranges_outside_initialized_reference_image']and review['other_actual_names_inside_ranges']==OFFSETS,'inputtimer no invented ownership/aliases')
 require(controls['status']=='PASS'and controls['controls'][0]['source_sha256']==SOURCE_SHA and controls['controls'][0]['object_sha256']==OBJECT_SHA and sha(payload['source_model'])==SOURCE_SHA,'inputtimer source/compiler proof');validate_object(payload['object'])
 wrong=controls['controls'][1];require(wrong['complete_COMDEFs']==[{'symbol':n,'type':0x85,'datatype':0x62,'size':2}for n in NAMES]and wrong['native_paired_WORD_width_requirement_pass']is False,'inputtimer genuine wrongWORD width control')
 correction=json.loads(payload['record_correction']);require(correction['actual_record_counts']=={'positive_COMDEF_records':1,'positive_definitions':2,'negative_COMDEF_records':1,'negative_definitions':2},'inputtimer one-record/two-definition shape')
 sourcehashes={sha(v)for k,v in payload.items()if k.startswith('client_source_')};require(sourcehashes=={x['sha256']for x in review['actual_typed_sources'].values()},'inputtimer all3 typed snapshots')
 for info in review['actual_typed_sources'].values():require({x['name']for x in info['declarations']}==set(NAMES)and all(x['type']=='unsigned long'and x['storage']=='extern'and x['init']is None for x in info['declarations']),'inputtimer unsignedlong client ABI')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'inputtimer original target');ref=build_reference(original);image=ref['image'];objects={PINS[k]['path']:read_omf(v)for k,v in payload.items()if k.startswith('client_object_')};primaries={}
 for key,entry,size in [('primary_0',0x184d,202),('primary_1',0x2301,548),('primary_2',0xd766,218)]:
  e=json.loads(payload[key]);p=e['analysis_profile'];b=e['normalized_result']['procedure']['body'];require(e['subject']['digest']['sha256']==ref['carrier_sha256']and e['subject']['format']=='dos-mz'and e['subject']['architecture']=='x86'and e['provider']['id']=='ghidra'and p['digest']=='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'and p['parameters']['loader']=='MzLoader'and p['parameters']['language_id']=='x86:LE:16:Real Mode'and p['parameters']['load_segment']=='0x1000'and p['parameters']['address_coordinates']=='linear-byte-offset'and e['operation']=='read_function_instructions'and e['parameters']=={'procedure':hex(entry+0x10000)}and b['available']and b['total_bytes']==b['span_bytes']==size and not b['non_contiguous'],'inputtimer complete primary/profile/bounds')
  ins=e['normalized_result']['instructions'];require(any('SUB AX, word ptr [0xb07a]'in x for x in ins)and any('SBB DX, word ptr [0xb07c]'in x for x in ins),'inputtimer paired SUB/SBB');primaries[e['evidence_id']]=e
 require(len(primaries)==3 and any('0x1d804: CWD'in e['normalized_result']['instructions']for e in primaries.values()),'inputtimer dialog truncation/CWD limit')
 refs=review['actual_runtime_WORD_FIXUPPs'];require(len(refs)==26,'inputtimer exact26 runtime fields');counts={};debug=[];coords=set()
 for record in refs:
  f=record['runtime_field'];o=objects[CLIENT_OBJECTS[record['source']]];fields=[x for x in o.fixups if x.segment==f['segment']and x.offset==f['object_offset']];require(len(fields)==1,'inputtimer unique raw field');v=fields[0];name=record['symbol'];base=OFFSETS[name];addr=f['arithmetic_result'];require(addr in[base,base+2]and f['original_addend']==addr-base and f['target_offset']==base and record['word_DS']==hex(addr)and record['memory_operand_width']==2 and f['mode']=='segment_relative_dgroup'and v.raw.hex()==record['raw_FIXUPP']and o.segments[v.segment].class_name=='CODE'and v.width==2 and v.location_type==1 and v.segment_relative and v.frame==(5,None)and v.target==(2,f['target_index'])and o.externals[v.target[1]]==name and image[f['image_offset']:f['image_offset']+2]==addr.to_bytes(2,'little'),'inputtimer actual low/high WORD memory field')
  e=primaries[record['native_primary_id']];require(record['instruction']in e['normalized_result']['instructions']and '['+hex(addr)+']'in record['instruction']and ' LEA 'not in record['instruction'],'inputtimer native memory operand not address-only');counts[record['unit']]=counts.get(record['unit'],0)+1;require(f['image_offset']not in coords,'inputtimer duplicate runtime coordinate');coords.add(f['image_offset'])
 require(counts=={'next_event_184d':10,'pump_input_2301':8,'next_dialog_event_d766':8},'inputtimer per-function10/8/8 counts')
 for path,o in objects.items():
  for v in o.fixups:
   if v.target[0]==2 and o.externals.get(v.target[1])in NAMES and o.segments[v.segment].class_name!='CODE':debug.append((o.segments[v.segment].class_name,v.width))
 require(len(debug)==6 and all(x==('DEBSYM',4)for x in debug),'inputtimer debug-only client fields separate')
 crt=json.loads(payload['crt']);require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['parameters']=={'address':'0x1ea86','length':179}and crt['normalized_result']['complete']and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'inputtimer native CRT clear')
 for base in OFFSETS.values():require(0x52cc<=base<base+4<=0xcbe0 and 0x5cc20+base>=len(image),'inputtimer nonfilebacked cleared4byte ranges')
 return [{'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(base),'end_exclusive':hex(base+4),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'historical_COMMON_order_proven':False,'original_TU_or_adjacency_unknown':True}for name,base in OFFSETS.items()]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'inputtimer source hash')
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'inputtimer fresh tool/source provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/'input-timer-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':8,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'two_unsignedlong_input_timers','authored_C_function_credit':0}
