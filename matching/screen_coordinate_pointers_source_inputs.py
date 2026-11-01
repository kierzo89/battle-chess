"""Closed compatible two-near-int-pointer COMMON4 profile. Zero matching credit.

Evidence comparison precedes compilation and must not be inside the compiler's
source/tool/scratch read scope. Historical TU/storage class and pointee capacities
remain unproved. The whole fresh compiler object is retained without rewriting.
"""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from screen_coordinate_pointers_profile_pins import PINS,TOOLS,FIELDS
BACKEND='msc500-near-common-screen-coordinate-pointers-v1'
SOURCE='src/link/screen_coordinate_pointer_state.c'
SOURCE_SHA='df76428b7c4738f86e3aa61b14b701e7d6be83eabf636892664d58fe7b89c587'
OBJECT_SHA='0faf72323f8e52a6627374496672c7e0746743e2ab8f3e4cad560354f87eea00'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_screen_x','_screen_y'];OFFSETS=[0xb0c6,0xb0c8]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'screen-pointer relative path');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'screen-pointer path escape');return p
def payload(o,klass):
 s=next(s for s in o.segments.values()if s.class_name==klass);b=bytearray(s.length);seen=set()
 for at,x in s.chunks:
  require(0<=at<=at+len(x)<=s.length,'screen-pointer payload bounds')
  # Genuine C500 DEBSYM headers patch earlier records. Other classes may not.
  require(klass in ['DEBSYM','DEBTYP']or not seen.intersection(range(at,at+len(x))),'screen-pointer overlapping loaded bytes');b[at:at+len(x)]=x;seen.update(range(at,at+len(x)))
 require(not s.unsupported_data and len(seen)==s.length,'screen-pointer complete payload');return bytes(b)
def globals(o):
 b=payload(o,'DEBSYM');at=0;out={}
 while at<len(b):
  n=b[at];v=b[at+1:at+1+n];require(n>=1 and len(v)==n,'screen-pointer symbol bounds');at+=n+1
  if v[0]==5:
   require(len(v)>=8 and len(v)==8+v[7],'screen-pointer full global record');name='_'+v[8:].decode('ascii');require(name not in out,'screen-pointer duplicate global');out[name]=int.from_bytes(v[5:7],'little')
 require(at==len(b),'screen-pointer symbol EOF');return out
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'screen-pointer exact registry fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('screen-coordinate-pointers-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'screen-pointer exact source/compiler profile')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES]and all(type(o['size'])is int for o in item['objects']),'screen-pointer exact two logical extents');require(item['evidence']==PINS,'screen-pointer exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'screen-pointer whole raw bytes');o=read_omf(raw)
 require(not o.publics and not o.procedures,'screen-pointer no PUBLIC/procedure/alias')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',34,32),('$$TYPES','DEBTYP',0,32)],'screen-pointer empty loaded segments/exact debug')
 require(not any(s.unsupported_data for s in o.segments.values()),'screen-pointer no LIDATA')
 defs=[];records=0
 for k,at,p in o.records:
  require(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a},'screen-pointer unsupported OMF record')
  if k==0xb0:
   records+=1;q=_Cursor(p)
   while q:
    n,t,dt,s=q.name(),q.index(),q.byte(),q.byte();require(dt==98 and s==2,'screen-pointer near COMMON2');defs.append({'symbol':n,'type_index':t,'datatype':dt,'size':s})
  elif k==0x88:require(p in [bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'screen-pointer unknown COMMENT')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'screen-pointer exact DGROUP')
  elif k==0x8a:require(p==b'\0','screen-pointer no entry point')
 require(records==1 and defs==[{'symbol':n,'type_index':161,'datatype':98,'size':2}for n in NAMES],'screen-pointer exact builtin A1 definitions/order')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'screen-pointer exact externals')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,a,4,3,True,(5,None),(2,t),None)for a,t in [(19,3),(2,2)]],'screen-pointer only two debug FAR fields')
 require(all(s==5 for _,s,_,_ in o.data_writes),'screen-pointer no initialized loaded or type bytes')
 require(globals(o)==dict.fromkeys(NAMES,161)and payload(o,'DEBTYP')==b'','screen-pointer exact builtin near-int-pointer globals/no custom types')
 require(sha(raw)==OBJECT_SHA,'screen-pointer complete reviewed object fingerprint');return defs
def validate_evidence(project,pins,target):
 require(pins==PINS,'screen-pointer exact evidence selection');p={}
 for k,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'screen-pointer evidence pin '+k);p[k]=b
 proof=json.loads(p['identity']);actual=json.loads(p['actual_audit']);generation=json.loads(p['generation_guard']);terminal=json.loads(p['terminal'])
 require(proof['status']=='PASS independent compatible two near signed-int-pointer cells and alias identity; production/provider admission HELD'and proof['uniform_actual_builtin_type']==161 and len(proof['actual_CODE_fields'])==24 and len(proof['complete_global_CV_records'])==10 and not proof['held_unselected_CODE_fields'],'screen-pointer independent full identity')
 require(proof['all108_range_extents_from_exact_raw_OMF_not_report_metadata_only']and proof['all108_prior_ranges_disjoint']and proof['new_slots_disjoint_against108']and len(proof['all108_prior_near_ranges'])==108,'screen-pointer complete prior108 constraints')
 spans=[(a,a+2)for a in OFFSETS]
 require(all(not(a<r['end_exclusive']and b>r['begin'])for a,b in spans for r in proof['all108_prior_near_ranges'])and spans[0][1]==spans[1][0]and spans[1][1]==proof['following_distinct_active_data']['begin']==0xb0ca,'screen-pointer disjoint cells/following anchor')
 require(actual['actual_compiler_scopes']==2 and actual['actual_terminal_handle_reaped']==21990 and actual['actual_terminal_exit']==0 and actual['whole_producer_object_sha256']==OBJECT_SHA and actual['context_CODE2322_DEBTYP1022_byte_exact']and actual['logical_fields258_CODE199_complete_equal']and len(actual['complete_native_MZ26'])==26 and actual['new_C_DATA_IMAGE_FILE_MZ_credit']==0,'screen-pointer closed actual independent audit')
 require(terminal['exit_code']==0 and terminal['unified_session_reaped']==21990 and not terminal.get('session_id')and generation['source_tool_scratch_only']and not generation['old_positive_injection']and len(generation['calls'])==2 and all(len(c['blocked_original_carrier_oldOBJ'])==4 and c['compiler_called_once']for c in generation['calls']),'screen-pointer closed source-only generation')
 require(sha(p['producer_source'])==SOURCE_SHA,'screen-pointer compatible fixed definition');validate_object(p['producer_object'])
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'screen-pointer target identity');image=build_reference(original)['image'];clients={k:read_omf(b)for k,b in p.items()if k.startswith('client_')};seen=[];debug=[];typed=0
 for k,o in clients.items():
  gs=globals(o);require({n:gs[n]for n in NAMES if n in gs}==dict.fromkeys(NAMES,161),'screen-pointer actual two builtin A1 client globals');typed+=2
  for f in o.fixups:
   if f.target[0]!=2 or o.externals.get(f.target[1])not in NAMES:continue
   if o.segments[f.segment].class_name=='CODE':seen.append((k,f.offset))
   else:debug.append(f);require(f.segment==5 and f.width==4 and f.location_type==3 and f.segment_relative and f.frame==(5,None),'screen-pointer debug address separate from storage width')
 require(len(clients)==5 and typed==len(debug)==10 and len(seen)==24 and len(set(seen))==24,'screen-pointer complete five clients/24CODE/10debug')
 expected=[]
 for row in FIELDS:
  o=clients[row['client']];hits=[f for f in o.fixups if f.segment==1 and f.offset==row['offset']];require(len(hits)==1,'screen-pointer field uniqueness');f=hits[0]
  require(o.externals[f.target[1]]==row['symbol']and f.width==2 and f.location_type==1 and f.segment_relative and f.frame==(5,None)and f.raw.hex()==row['raw_FIXUPP'],'screen-pointer actual raw OFFSET16')
  code=payload(o,'CODE');addend=int.from_bytes(code[f.offset:f.offset+2],'little');address=dict(zip(NAMES,OFFSETS))[row['symbol']];require(addend==0 and row['native_DS_offset']==address and image[row['native_image_field']:row['native_image_field']+2]==address.to_bytes(2,'little')and row['runtime_slot_access_width']==2,'screen-pointer actual native slot operand');expected.append((row['client'],f.offset))
 require(set(expected)==set(seen)and len(FIELDS)==24 and sum(r['access']=='write'for r in FIELDS)==4 and sum(r['access']=='read'for r in FIELDS)==20,'screen-pointer all runtime accesses accounted')
 for row in proof['native_initializer_near_assignments']:
  at=row['native_image_instruction'];b=bytes.fromhex(row['native_bytes']);require(image[at:at+len(b)]==b and len(b)==6 and b[:2]==bytes.fromhex('c706')and int.from_bytes(b[2:4],'little')==int(row['slot'],16)and int.from_bytes(b[4:6],'little')==int(row['near_value'],16),'screen-pointer native near assignment')
 for row in proof['native_refresh_DS_word_indexing']:
  for a,k in [('slot_load_image','slot_load_bytes'),('DS_indexed_word_read_image','DS_indexed_word_read_bytes')]:
   at=row[a];b=bytes.fromhex(row[k]);require(image[at:at+len(b)]==b,'screen-pointer DS WORD indexing')
 return [{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(a),'end_exclusive':hex(a+2),'size':2,'resolved':False,'historical_placement_TU_storageclass_or_pointee_capacity_proven':False}for n,a in zip(NAMES,OFFSETS)]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'screen-pointer source hash')
 constraints=validate_evidence(project,item['evidence'],target)
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'screen-pointer fresh compiler provenance')
 defs=validate_object(c.object_bytes);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'screen-coordinate-pointers-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_two_near_int_pointer_cells_no_historical_owner_TU_storageclass_or_pointee_capacity_claim'}
