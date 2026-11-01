"""Closed compatible logical6x6 near-pointer grids; COMMON144, zero match credit."""
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import dataclasses,hashlib,json,tempfile
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from left_right_lists_profile_pins import PINS,TOOLS,EXPECTED_GRAPH
BACKEND='msc500-near-common-left-right-lists-v1'
SOURCE='src/link/left_right_lists.c'
SOURCE_SHA='d6523544e227efcd9eb94b12ff5cbd36eb4821ecb47d65fbd73b02720b6c7a82'
OBJECT_SHA='ba59e18bdf095f13d7c1f18c3fbbaa6c75d025a6ed4baa97c5654ed295769ba0'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_left_lists','_right_lists'];OFFSETS=[0x8f46,0x8f8e]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'grids relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'grids path escape');return p
def segment(o,kind):
 s=next(s for s in o.segments.values()if s.class_name==kind);b=bytearray(s.length);seen=bytearray(s.length)
 for at,v in s.chunks:
  require(0<=at<=at+len(v)<=s.length,'grids complete segment bounds');b[at:at+len(v)]=v;seen[at:at+len(v)]=b'\1'*len(v)
 require(not s.unsupported_data and all(seen),'grids unsupported or incomplete segment');return bytes(b)
def types(o):
 b=segment(o,'DEBTYP');at=0;t=512;out={}
 while at<len(b):
  require(at+3<=len(b)and b[at]==1,'grids CV type header');n=int.from_bytes(b[at+1:at+3],'little');require(n>0 and at+3+n<=len(b),'grids CV type bound');out[t]=b[at+3:at+3+n];t+=1;at+=3+n
 require(at==len(b),'grids complete type EOF');return out
def globals(o):
 b=segment(o,'DEBSYM');at=0;out={}
 while at<len(b):
  n=b[at];require(n>0 and at+n+1<=len(b),'grids CV symbol bounds');v=b[at+1:at+n+1]
  if v[0]==5:
   require(len(v)>=8 and len(v)==8+v[7],'grids complete CV global');name='_'+v[8:].decode('ascii');require(name not in out,'grids duplicate CV global');out[name]={'type':int.from_bytes(v[5:7],'little'),'offset':at,'raw':v.hex()}
  at+=n+1
 require(at==len(b),'grids complete symbol EOF');return out
def graph(ts,t,trail=()):
 if t<512:return ['builtin',t]
 require(t in ts and t not in trail and len(trail)<8,'grids missing/cyclic/deep array type');q=_Cursor(ts[t]);require(q.byte()==0x78,'grids array type leaf');n=q.byte();require(n<128 or n==0x85,'grids bounded array numeric leaf');bits=q.word()if n==0x85 else n;require(q.byte()==0x83,'grids array element leaf');elem=q.word();q.finish();return ['array',bits,graph(ts,elem,trail+(t,))]
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'grids exact registry fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('left-right-lists-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'grids exact source/compiler profile')
 require(item['objects']==[{'symbol':n,'size':72,'storage':'near-common'}for n in NAMES]and all(type(d['size'])is int for d in item['objects']),'grids exact two logical extents');require(item['evidence']==PINS,'grids exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'grids whole raw object bytes');o=read_omf(raw)
 require(not o.publics and not o.procedures,'grids no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',39,32),(6,'$$TYPES','DEBTYP',34,32)],'grids exact empty loaded segments and complete debug shape')
 defs=[];common_records=0
 for k,at,b in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'grids unsupported raw OMF record')
  if k==0xb0:
   common_records+=1;q=_Cursor(b)
   while q:
    name,t,kind,n=q.name(),q.index(),q.byte(),q.byte();require(kind==0x62 and n==72,'grids exact near COMMON72');defs.append({'symbol':name,'type_index':t,'communal_kind':kind,'size':n,'storage':'near-common'})
  elif k==0x88:require(b in[bytes.fromhex(x)for x in['009d30734f','00a1014356','00a201']],'grids unknown COMMENT')
  elif k==0x9a:require(b==bytes.fromhex('02ff03ff04ff02'),'grids exact DGROUP')
  elif k==0x8a:require(b==b'\0','grids no entrypoint')
 require(common_records==1 and defs==[{'symbol':n,'type_index':516,'communal_kind':98,'size':72,'storage':'near-common'}for n in NAMES],'grids complete two definitions/type/order')
 require(o.externals=={1:'__acrtused',2:NAMES[0],3:NAMES[1]},'grids exact external inventory')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,21,4,3,True,(5,None),(2,3),None),(5,2,4,3,True,(5,None),(2,2),None)],'grids only two DEBUG FAR fixups')
 require(all(sn in[5,6]for pos,sn,off,n in o.data_writes),'grids no initialized loaded bytes')
 require(not any(pos>f.record_offset and sn==f.segment and off<f.offset+f.width and f.offset<off+n for f in o.fixups for pos,sn,off,n in o.data_writes),'grids DEBUG field overwritten later')
 ts=types(o);gs=globals(o);require(set(gs)==set(NAMES)and all(v['type']==516 and graph(ts,v['type'])==EXPECTED_GRAPH for v in gs.values()),'grids complete array dimensions/pointer graph')
 require({hex(t):v.hex()for t,v in ts.items()}=={'0x200':'80','0x201':'80','0x202':'80','0x203':'80','0x204':'78854002830502','0x205':'786083a000'},'grids exact complete raw type stream')
 require(segment(o,'DEBSYM').hex()=='12050000000004020a6c6566745f6c6973747313050000000004020b72696768745f6c69737473','grids exact complete DEBUG globals')
 require(sha(raw)==OBJECT_SHA,'grids exact genuine whole object fingerprint');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'grids exact evidence selection');project=Path(project).resolve();p={}
 for key,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'grids evidence pin '+key);p[key]=b
 ownership=json.loads(p['ownership']);boundary=json.loads(p['boundaries']);producer=json.loads(p['producer']);generation=json.loads(p['generation']);context=json.loads(p['context']);native=json.loads(p['native_REA']);freeze=json.loads(p['ownership_freeze'])
 require(sha(p['ownership_freeze'])=='5f9dac49cc6f4f88412f141c5cc92c4056d826409567ff94c5aa1e561f89c1c8','grids closed actual evidence freeze')
 require(ownership['status'].startswith('SUPPORTED')and len(ownership['prior_all29_strict_decoders'])==29 and len(ownership['prior_near112_disjoint_ranges'])==112 and len(ownership['far2_separate'])==2 and not ownership['held_unselected_fields'],'grids complete prior typed/native scope')
 require(producer['status'].startswith('GENUINE_PROVIDER_COMPATIBLE_PASS')and producer['normalized_graphs']==dict.fromkeys(NAMES,EXPECTED_GRAPH)and producer['whole_object_sha256']==OBJECT_SHA,'grids compatible actual producer')
 require(generation['actual_compiler_calls']==1 and generation['source_sha256']==SOURCE_SHA and generation['object_sha256']==OBJECT_SHA and generation['tool_hashes']==TOOLS and generation['flags']==FLAGS and generation['source_tool_fresh_scratch_only']and len(generation['blocked_probes'])==5,'grids actual guarded source provenance');require(sha(p['source_model'])==SOURCE_SHA,'grids genuine source model');validate_object(p['producer_object'])
 require([(r['symbol'],r['base'],r['end_exclusive'],r['bytes'])for r in ownership['arrays']]==[(NAMES[0],0x8f46,0x8f8e,72),(NAMES[1],0x8f8e,0x8fd6,72)],'grids exact logical spans')
 for base in OFFSETS:
  require(all(base+72<=r['base']or r['end']<=base for r in ownership['prior_near112_disjoint_ranges']),'grids prior range overlap')
 require(native['subject']['digest']['sha256']==ORIGINAL_SHA256 and native['evidence_id']==ownership['retained_native_REA_evidence'],'grids retained native identity')
 require(all(x in native['normalized_result']['instructions']for x in ownership['native_initialization_loop']['required_instructions'])and ownership['native_initialization_loop']['writes']==72 and ownership['native_initialization_loop']['stride']==2,'grids exact72 native WORD writes')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'grids original target identity');ref=build_reference(original);image=ref['image'];byhash={};actual=[];debug=[];typed=[]
 for client in context['clients']:
  raw=p[client['object_key']];u=client['row'];require(sha(raw)==u['object_sha256']and sha(p[client['source_key']])==u['source_sha256'],'grids immutable client source/object');o=read_omf(raw);byhash[sha(raw)]=o
  at=int(u['image_offset'],0);require(sha(image[at:at+u['size']])==u['expected_sha256']==u['actual_sha256'],'grids retained complete original client body identity')
  if u['id']=='manage_asset_arena_3713':
   require(u['status']=='c_matched'and u['size']==902,'grids existing complete manager902');gs=globals(o);ts=types(o)
   for n in NAMES:require(n in gs and graph(ts,gs[n]['type'])==EXPECTED_GRAPH,'grids actual complete client type graph');typed.append(n)
  else:require(u['id']=='init_animation_code1083'and u['size']==1083 and o.publics['_init_animation'].offset==0,'grids actual native animation1083')
  for f in o.fixups:
   n=o.externals.get(f.target[1])if f.target[0]==2 else None
   if n not in NAMES:continue
   if o.segments[f.segment].class_name=='DEBSYM':
    require((f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(4,3,True,(5,None),None),'grids separate client DEBUG FAR');require(not any(pos>f.record_offset and sn==f.segment and off<f.offset+4 and f.offset<off+nbytes for pos,sn,off,nbytes in o.data_writes),'grids client DEBUG overwritten');debug.append((n,f.offset));continue
   expected=[x for x in context['native_fields']if x['object_sha256']==sha(raw)and x['actual_FIXUPP']['segment']==f.segment and x['actual_FIXUPP']['offset']==f.offset];require(len(expected)==1,'grids no held/unselected actual CODE field');old=expected[0];q=old['actual_FIXUPP'];require(f.raw.hex()==q['raw']and(f.width,f.location_type,f.segment_relative,f.displacement)==(2,1,True,None),'grids exact actual CODE field shape')
   if u['id']=='init_animation_code1083':require(f.frame==(1,1)and[(k,b.hex())for k,pos,b in o.records if k==0x9a]==[(0x9a,'02ff01')],'grids exact animation DGROUP frame')
   else:require(f.frame==(5,None),'grids exact C field frame')
   code=segment(o,'CODE');add=int.from_bytes(code[f.offset:f.offset+2],'little');site=old['actual_native_field']['image_offset'];value=(OFFSETS[NAMES.index(n)]+add)&65535;require(add==old['source_addend']and image[site:site+2]==value.to_bytes(2,'little')==bytes.fromhex(old['actual_native_field']['encoded_hex']),'grids actual original native operand');actual.append((sha(raw),f.segment,f.offset))
 require(len(actual)==len(set(actual))==3 and len(debug)==len(typed)==2,'grids complete3CODE/2DEBUG/2typed inventory')
 require(boundary['status'].startswith('PASS')and boundary['following_timer_actual_initializer_WORD_addends']==[0,2,4,6]and not boundary['8F45_claimed'],'grids distinct native boundary proof')
 for anchor in boundary['anchors']:
  for field in anchor['actual_selected_fields']:
   h=field['object_sha256'];key=context['anchor_object_keys_by_hash'][h];raw=p[key];require(sha(raw)==h,'grids actual anchor object');o=read_omf(raw);q=field['actual_raw_FIXUPP'];f=next((f for f in o.fixups if f.segment==q['segment']and f.offset==q['offset']),None);require(f is not None and f.raw.hex()==q['raw']and o.externals[f.target[1]]==anchor['symbol']and(f.width,f.location_type,f.segment_relative,f.frame)==(2,1,True,(5,None)),'grids distinct actual boundary raw field');old=field['retained_native_field'];site=old['image_offset'];require(image[site:site+2]==bytes.fromhex(old['encoded_hex']),'grids actual native boundary operand')
 require(all(0x52cc<=a<a+72<=0xcbe0 for a in OFFSETS),'grids native CRT clear bounds')
 return[{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(a),'end_exclusive':hex(a+72),'size':72,'resolved':False,'compatible_complete_graph':EXPECTED_GRAPH,'historical_capacity_storageclass_TU_physical_partition_order_MAP_proven':False}for n,a in zip(NAMES,OFFSETS)]

@contextmanager
def source_generation_scope(project,source,target):
 project=Path(project).resolve();source=Path(source).resolve();allowed={source,project/'config/msc500.json',project/'toolchains/msc500/manifest.json',*((project/'toolchains/msc500'/n).resolve()for n in TOOLS)};rb=Path.read_bytes;rt=Path.read_text;oldtemp=tempfile.TemporaryDirectory;roots=[];reads=[];denied=[]
 def temporary(*args,**kw):
  t=oldtemp(*args,**kw);require(Path(t.name).name.startswith('battlechess-msc-'),'grids genuine fresh compiler scratch');roots.append(Path(t.name).resolve());return t
 def permit(p):
  q=Path(p).resolve()
  if q not in allowed and not any(q==r/n for r in roots for n in['UNIT.OBJ','COMPILE.LOG']):denied.append(str(q));raise ValueError('grids forbidden generation read '+str(q))
  reads.append(str(q))
 def bread(p,*a,**k):permit(p);return rb(p,*a,**k)
 def tread(p,*a,**k):permit(p);return rt(p,*a,**k)
 with patch.object(Path,'read_bytes',bread),patch.object(Path,'read_text',tread),patch.object(tempfile,'TemporaryDirectory',temporary):
  for p in[Path(target),project/'build/exepack/TRIM5_UNPACK.EXE',local(project,PINS['producer_object']['path']),local(project,PINS['ownership']['path']),local(project,PINS['consumer_object']['path'])]:
   try:p.read_bytes()
   except ValueError:pass
   else:raise ValueError('grids source guard inactive')
  yield reads,denied,roots
 require(len(denied)==5 and len(roots)==1,'grids exact denied comparisons/one fresh scratch')
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);require((project/SOURCE).is_file()and not(project/SOURCE).is_symlink(),'grids regular source');before=source.read_bytes();require(sha(before)==SOURCE_SHA,'grids source hash');constraints=validate_evidence(project,item['evidence'],target)
 with source_generation_scope(project,source,target)as(reads,denied,roots):c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'grids fresh exact compiler provenance');defs=validate_object(c.object_bytes);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'left-right-lists-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(source_tool_fresh_scratch_only=True,generation_reads=reads,blocked_comparison_probes=denied,fresh_scratch_roots=[str(r)for r in roots],comparison_reads_separate=True)
 return{'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':144,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_complete_6x6_pointer_grids_no_historical_capacity_storageclass_TU_MAP_claim'}
