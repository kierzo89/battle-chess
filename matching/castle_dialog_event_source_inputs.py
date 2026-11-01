"""Closed compatible castle2/event20 near COMMON; no historical placement credit."""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from castle_dialog_event_profile_pins import PINS
BACKEND='msc500-near-common-castle-dialog-event-v1';SOURCE='src/link/castle_dialog_event_state.c';NAMES=['_castle_owner','_dialog_event'];FLAGS=['/AS','/Zl','/Zi']
SOURCE_SHA='75c278c6147f9562d56ce0c3d5735ce65527bb0c5d6c0b434dcb84725de615c9';OBJECT_SHA='649fc20b444bee37ac34d93e6e62744e7e3614681ccd9aeb3be84213f2e417e3';MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
MEMBERS=['kind','status','code','reserved','x','y','word6','word7','word8','word9']
TYPENAMES=b'\x7f'+b''.join(b'\x82'+bytes([len(n)])+n.encode()+b'\x88'+bytes([2*i])for i,n in enumerate(MEMBERS))
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'castle/event relative path required');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'castle/event path escape');return p
def data(seg):
 raw=bytearray(seg.length);present=bytearray(seg.length)
 for at,b in seg.chunks:require(at+len(b)<=seg.length,'castle/event data overrun');raw[at:at+len(b)]=b;present[at:at+len(b)]=bytes([1])*len(b)
 require(all(present)and not seg.unsupported_data,'castle/event incomplete data');return bytes(raw)
def cvtypes(o):
 raw=data(next(s for s in o.segments.values()if s.class_name=='DEBTYP'));at=0;idx=0x200;out={}
 while at<len(raw):
  require(raw[at]==1,'castle/event CV type flag');n=int.from_bytes(raw[at+1:at+3],'little');p=raw[at+3:at+3+n];require(len(p)==n,'castle/event CV type truncation');out[idx]=p;at+=3+n;idx+=1
 return out
def cvglobals(o):
 raw=data(next(s for s in o.segments.values()if s.class_name=='DEBSYM'));at=0;out={}
 while at<len(raw):
  n=raw[at]+1;p=raw[at:at+n];require(n>=2 and len(p)==n,'castle/event CV symbol truncation')
  if p[1]==5:require(len(p)==9+p[8],'castle/event CV global name');out[p[9:].decode()]=int.from_bytes(p[6:8],'little')
  at+=n
 return out
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'castle/event exact item fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('castle-dialog-event-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'castle/event exact source/profile')
 require(item['objects']==[{'symbol':'_castle_owner','size':2,'storage':'near-common'},{'symbol':'_dialog_event','size':20,'storage':'near-common'}]and all(type(x['size'])is int for x in item['objects']),'castle/event exact typed extents2+20');require(item['evidence']==PINS,'castle/event exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'castle/event unchanged bytes required');o=read_omf(raw);require(not o.publics and not o.procedures,'castle/event PUBLIC/alias/procedure forbidden')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',42,32),('$$TYPES','DEBTYP',151,32)],'castle/event loaded/debug allocation')
 defs=[];records=0
 for k,at,p in o.records:
  if k==0xb0:
   records+=1;q=_Cursor(p)
   while q:defs.append({'symbol':q.name(),'type_index':q.index(),'datatype':q.byte(),'size':q.byte()})
 require(records==1 and defs==[{'symbol':'_castle_owner','type_index':0x81,'datatype':0x62,'size':2},{'symbol':'_dialog_event','type_index':0x203,'datatype':0x62,'size':20}],'castle/event exact single COMDEF2+20/types')
 require(o.externals=={1:'__acrtused',2:'_castle_owner',3:'_dialog_event'},'castle/event exact externals')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,23,4,3,True,(5,None),(2,3),None),(5,2,4,3,True,(5,None),(2,2),None)],'castle/event debug-only FAR fields')
 require(all(s in[5,6]for _,s,_,_ in o.data_writes),'castle/event initialized allocation forbidden');t=cvtypes(o);g=cvglobals(o)
 require(g=={'castle_owner':0x81,'dialog_event':0x203}and t[0x203]==bytes.fromhex('7985a0000a830402830502820069')and t[0x204]==bytes.fromhex('7f'+'838100'*10)and t[0x205]==TYPENAMES,'castle/event exact signed-int record20/member offsets CodeView')
 require(sha(raw)==OBJECT_SHA,'castle/event whole object/source fingerprint');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'castle/event exact evidence');payload={}
 for k,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'castle/event evidence pin '+k);payload[k]=raw
 r=json.loads(payload['review']);n=json.loads(payload['native_fields']);root=json.loads(payload['root_review']);gen=json.loads(payload['generation'])
 require(r['status']=='PASS_COMPATIBLE_C_DEFINITION_PROPOSAL'and root['status']=='PASS source definition proposal; zero credit'and n['status']=='SUPPORTED_COMPATIBLE_DEFINITIONS','castle/event independent reviews')
 require(r['COMMON_allocation_bytes']==22 and r['native_fields_verified']==13 and r['new_C_function_DATA_IMAGE_FILE_MZ_credit']==0 and not r['native_MAP_or_COMMON_start_proven']and r['COMMON_source_choice_only_not_original_storageclass_TU_or_visibility'],'castle/event historical placement/credit limits')
 require(n['ordinary_DF_clear_C_ABI_assumed']and n['semantic_last_four_words_unknown_but_copied_not_padding']and not n['original_storageclass_static_TU_commonstart_or_MAP_proven']and n['existing_dialog_COMMON_owners_unchanged'],'castle/event semantic/DF/ownership limits')
 require(sha(payload['source_model'])==SOURCE_SHA and gen['source_sha256']==SOURCE_SHA and gen['object_sha256']==OBJECT_SHA,'castle/event source/producer identities');validate_object(payload['object'])
 require('extern int current_side, opponent, history_index, castle_owner;'in payload['castle_source'].decode()and 'typedef struct {int kind,status,code,reserved,x,y,word6,word7,word8,word9;} DialogEvent;'in payload['event_source'].decode(),'castle/event selected declarations')
 co=read_omf(payload['castle_object']);eo=read_omf(payload['event_object']);require(cvglobals(co)['castle_owner']==0x81,'castle/event selected signed-int type');et=cvtypes(eo);st=et[cvglobals(eo)['dialog_event']]
 require(st[:6]==bytes.fromhex('7985a0000a83')and st[8]==0x83 and st[11:]==bytes.fromhex('820069')and et[int.from_bytes(st[6:8],'little')]==bytes.fromhex('7f'+'838100'*10)and et[int.from_bytes(st[9:11],'little')]==TYPENAMES,'castle/event selected client record20/member type offsets')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'castle/event original identity');image=build_reference(original)['image'];require(image[0xd789:0xd795]==bytes.fromhex('bfd6528bf01e07b90a00f2a5'),'castle/event native20 copy')
 primaries={key:json.loads(payload[key])for key in['castle_primary','piece_primary','event_primary']}
 for e in primaries.values():require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['operation']=='analyze_function','castle/event primary subject/operation')
 require(all(x in primaries['event_primary']['normalized_result']['assembly']for x in['0x1d789: MOV DI, 0x52d6','0x1d790: MOV CX, 0xa','0x1d793: MOVSW.REP ES:DI, SI']),'castle/event native20 copy primary')
 rows=n['native_runtime_fields'];require(len(rows)==13 and sum(x['symbol']=='_castle_owner'for x in rows)==2 and sum(x['symbol']=='_dialog_event'for x in rows)==11 and sum(x['address_only']for x in rows)==2,'castle/event exact13field roles')
 mapping={'castle_flags_9ad5':('castle_primary',co),'original_piece_9b46':('piece_primary',co),'next_dialog_event_d766':('event_primary',eo)}
 for row in rows:
  key,o=mapping[row['unit']];f=row['field'];hits=[x for x in o.fixups if(x.segment,x.offset)==(f['segment'],f['object_offset'])];require(len(hits)==1,'castle/event raw field identity');v=hits[0]
  require(v.width==2 and v.location_type==1 and v.segment_relative and v.frame==(5,None)and v.target[0]==2 and o.externals[v.target[1]]==row['symbol']and v.raw.hex()==row['raw_FIXUPP'],'castle/event raw field shape')
  require(row['instruction']in primaries[key]['normalized_result']['assembly']and image[f['image_offset']:f['image_offset']+2]==f['encoded_value'].to_bytes(2,'little'),'castle/event actual native operands')
 negative=read_omf(payload['wrong18']);q=_Cursor(next(p for k,at,p in negative.records if k==0xb0));q.name();q.index();q.byte();q.byte();require((q.name(),q.index(),q.byte(),q.byte())==('_dialog_event',0x203,0x62,18),'castle/event genuine18 negative');q.finish()
 require(n['copied_bytes']==20 and 18<20 and n['forward_last_WORD_DS']=='0x52e8','castle/event last copied WORD extent')
 return [{'symbol':'_castle_owner','dgroup_segment':'0x5cc2','dgroup_offset':'0x52d0','size':2,'resolved':False},{'symbol':'_dialog_event','dgroup_segment':'0x5cc2','dgroup_offset':'0x52d6','size':20,'end_exclusive':'0x52ea','resolved':False,'forward_DF_clear_ABI_assumed':True,'historical_storageclass_TU_MAP_proven':False}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'castle/event source hash')
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'castle/event fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/'castle-dialog-event-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':22,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_castle2_dialog_event20_no_historical_class_TU_claim'}
