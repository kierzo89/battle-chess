"""Closed compatible piece-square logical2880 near COMMON; zero match credit."""
from pathlib import Path
import dataclasses,hashlib,json,struct
from msc import compile_c
from omf import read_omf,_Cursor
from reference import ORIGINAL_SHA256
from piece_square_profile_pins import PINS,TOOLS
BACKEND='msc500-near-common-piece-square-v1';SOURCE='src/link/piece_square_state.c';NAMES=['_piece_square'];FLAGS=['/AS','/Zl','/Zi']
SOURCE_SHA='bdefba76dabd8cc8a8ef176ae3293b1fb584d91fc4e1e7c3ff75d42c635fbfe6';OBJECT_SHA='c02f493be511252f5cf96fa79e1140ed01e294e85b08a6c498076501244b1b92';MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'piece-square relative path');p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'piece-square path escape');return p
def debug(o,klass):
 s=next(s for s in o.segments.values()if s.class_name==klass);b=bytearray(s.length);seen=set()
 for at,x in s.chunks:
  require(0<=at<=at+len(x)<=s.length,'piece-square debug bounds');b[at:at+len(x)]=x;seen.update(range(at,at+len(x)))
 require(not s.unsupported_data and len(seen)==s.length,'piece-square debug full coverage');return bytes(b)
def types(o):
 b=debug(o,'DEBTYP');at=0;idx=0x200;out={}
 while at<len(b):
  require(b[at]==1 and at+3<=len(b),'piece-square CV type header');n=int.from_bytes(b[at+1:at+3],'little');v=b[at+3:at+3+n];require(len(v)==n and n>0,'piece-square CV type bounds');out[idx]=v;at+=3+n;idx+=1
 require(at==len(b),'piece-square CV type EOF');return out
def globals(o):
 b=debug(o,'DEBSYM');at=0;out={}
 while at<len(b):
  n=b[at]+1;p=b[at:at+n];require(n>=2 and len(p)==n,'piece-square CV symbol bounds')
  if p[1]==5:
   require(len(p)>=9 and len(p)==9+p[8],'piece-square CV global');name=p[9:].decode();require(name not in out,'piece-square duplicate CV global');out[name]=int.from_bytes(p[6:8],'little')
  at+=n
 require(at==len(b),'piece-square CV symbol EOF');return out
def array_shape(o,index):
 ts=types(o);out=[]
 for _ in range(3):
  require(index in ts,'piece-square missing nested array');q=_Cursor(ts[index]);require(q.byte()==0x78,'piece-square array leaf');leaf=q.byte();require(leaf==0x85,'piece-square complete array numeric leaf');bits=q.word();require(q.byte()==0x83,'piece-square element type leaf');index=q.word();q.finish();out.append(bits)
 require(out==[23040,11520,1920]and index==0x81,'piece-square exact complete int2x6x120');return out

def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'piece-square exact registry fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('piece-square-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'piece-square exact source/compiler profile')
 require(item['objects']==[{'symbol':'_piece_square','size':2880,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'piece-square exact logical2880 declaration');require(item['evidence']==PINS,'piece-square exact pinned evidence')
def validate_object(raw):
 require(isinstance(raw,bytes),'piece-square whole raw bytes');o=read_omf(raw)
 require(not o.publics and not o.procedures,'piece-square no PUBLIC/procedure/alias')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',21,32),('$$TYPES','DEBTYP',42,32)],'piece-square empty loaded segments/exact debug')
 defs=[];records=0
 allowed={0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a}
 for k,at,p in o.records:
  require(k in allowed,'piece-square unknown OMF record')
  if k==0xb0:
   records+=1;q=_Cursor(p)
   while q:
    name,typ,dt,leaf=q.name(),q.index(),q.byte(),q.byte();require(dt==0x62 and leaf==0x81,'piece-square near COMMON16 length leaf');size=q.word();defs.append({'symbol':name,'type_index':typ,'datatype':dt,'size':size})
  elif k==0x88:require(p in [bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],'piece-square unknown COMMENT')
  elif k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'piece-square exact DGROUP members')
  elif k==0x8a:require(p==b'\0','piece-square no entry point')
 require(records==1 and defs==[{'symbol':'_piece_square','type_index':0x203,'datatype':0x62,'size':2880}],'piece-square exact COMMON2880/type203')
 require(o.externals=={1:'__acrtused',2:'_piece_square'},'piece-square exact externals')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,2,4,3,True,(5,None),(2,2),None)],'piece-square only debug FAR field')
 require(all(s in [5,6]for _,s,_,_ in o.data_writes),'piece-square no initialized loaded bytes')
 require(globals(o)=={'piece_square':0x203},'piece-square exact debug symbol');array_shape(o,0x203)
 require(sha(raw)==OBJECT_SHA,'piece-square whole reviewed object fingerprint');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'piece-square exact evidence selection');p={}
 for key,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'piece-square evidence pin '+key);p[key]=b
 proof=json.loads(p['ownership']);gen=json.loads(p['generation']);client=read_omf(p['client_object'])
 require(proof['status']=='PASS compatible complete logical storage; historical physical owner/class/order HELD'and all(c['pass']for c in proof['checks']),'piece-square closed ownership evidence')
 require(proof['native_range']['size']==2880 and proof['native_range']['begin']=='0xb0dc'and proof['native_range']['end_exclusive']=='0xbc1c'and proof['native_range']['unexplained_gap']==['0xbc1c','0xbc1e'],'piece-square bounded native range/gap')
 require(proof['current_provider_count']==23 and proof['current_provided_object_count']==103 and all(not(r['begin']<0xbc1c and r['end_exclusive']>0xb0dc)for r in proof['current_provider_ranges']),'piece-square current23 no overlaps')
 require(all(v==0 for v in proof['credit'].values())and not proof['whole3902_equal'],'piece-square zero credit/held clients preserved')
 require(sha(p['source_model'])==SOURCE_SHA and gen['source_sha256']==SOURCE_SHA and gen['object_sha256']==OBJECT_SHA,'piece-square source generation identity');validate_object(p['producer_object'])
 require(b'extern int piece_square[2][6][120];'in p['client_source'],'piece-square selected complete declaration')
 require(globals(client)['piece_square']==0x22e,'piece-square actual client type');array_shape(client,0x22e)
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'piece-square target identity');header=struct.unpack_from('<H',original,8)[0]*16;image=original[header:]
 loopraw=json.loads(p['loop_raw']);require(loopraw['normalized_result']['complete']and bytes.fromhex(loopraw['normalized_result']['bytes_hex'])==image[0xfe59:0x1094c],'piece-square complete2803 native loop carrier')
 loop=json.loads(p['loop_primary']);require(loop['evidence_id']==proof['native_evidence']['loop_dossier'],'piece-square loop evidence identity')
 require(all(x['carrier']in loop['normalized_result']['assembly']for x in proof['retained_native_loop_instructions'])and len(proof['retained_native_loop_instructions'])==12,'piece-square native loop bounds/store')
 piece=json.loads(p['piece_primary']);require(piece['subject']['digest']['sha256']==ORIGINAL_SHA256 and piece['evidence_id']==proof['native_evidence']['independent_lookup'],'piece-square original lookup identity')
 require(all(x in piece['normalized_result']['assembly']for x in ['0x20a00: MOV AX, 0xf0','0x20a08: MOV AX, 0x5a0','0x20a13: SHL BX, 0x1','0x20a15: MOV AX, word ptr [BX + SI + 0xafec]']),'piece-square actual independent lookup strides')
 fields=proof['actual_piece_square_fields'];actual=[f for f in client.fixups if f.segment==1 and f.target[0]==2 and client.externals[f.target[1]]=='_piece_square'];require(len(fields)==len(actual)==8,'piece-square all actual eight fields')
 code=bytearray(client.segments[1].length)
 for at,b in client.segments[1].chunks:code[at:at+len(b)]=b
 for row in fields:
  hits=[f for f in actual if f.segment==row['segment']and f.offset==row['object_offset']];require(len(hits)==1,'piece-square raw field ownership');f=hits[0]
  require(f.width==2 and f.location_type==1 and f.segment_relative and f.frame==(5,None)and f.raw.hex()==row['raw_fixupp'],'piece-square raw OFFSET16 field')
  value=(0xb0dc+int.from_bytes(code[f.offset:f.offset+2],'little')+(f.displacement or 0))&65535
  require(row['image_offset']==0xfdf2+f.offset and image[row['image_offset']:row['image_offset']+2]==value.to_bytes(2,'little')==bytes.fromhex(row['encoded_hex']),'piece-square actual native table operand')
 crt=json.loads(p['crt_primary']);require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in bytes.fromhex(crt['normalized_result']['bytes_hex']),'piece-square real CRT clear')
 require(0xafec+240==0xb0dc and 0xafec+6*240+1440+119*2==0xbc1a and 0xbc1a+2==0xbc1c and 0x52cc<=0xb0dc<0xbc1c<=0xcbe0 and not(119&0x88),'piece-square complete logical last WORD')
 return [{'symbol':'_piece_square','dgroup_segment':'0x5cc2','dgroup_offset':'0xb0dc','end_exclusive':'0xbc1c','size':2880,'resolved':False,'compatible_logical_type':'int[2][6][120]','historical_storageclass_TU_MAP_unique_capacity_proven':False,'following_unknown_bytes':['0xbc1c','0xbc1e']}]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'piece-square source hash')
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'piece-square fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'piece-square-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':2880,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_complete_logical_piece_square_no_historical_class_TU_MAP_claim'}
