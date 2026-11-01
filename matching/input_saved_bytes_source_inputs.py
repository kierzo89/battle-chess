"""Compatible saved input BYTE COMMON4; zero function/initialized/native credit."""
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import dataclasses,hashlib,json,tempfile
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from input_saved_bytes_profile_pins import PINS,TOOLS
BACKEND='msc500-near-common-input-saved-bytes-v1'
SOURCE='src/link/input_saved_bytes.c'
SOURCE_SHA='346aa5e6169eb208c30f66b048898d321b3d347434bda3d20f795e14f348bbbb'
OBJECT_SHA='17b5b5292a78adddc191f19965b70aa6cb540b3421cc6b716aa3eb2680e13e4a'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_saved_cursor_8d0a','_actor_flag_9374','_input_mode_984e','_input_flag_8fe0'];OFFSETS=[0x8d0a,0x9374,0x984e,0x8fe0]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'savedBYTE relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'savedBYTE path escape');return p
def debug_bytes(o):
 s=o.segments[5];b=bytearray(s.length);seen=bytearray(s.length)
 for at,v in s.chunks:require(0<=at<=at+len(v)<=s.length,'savedBYTE debug bounds');b[at:at+len(v)]=v;seen[at:at+len(v)]=b'\1'*len(v)
 require(not s.unsupported_data and all(seen),'savedBYTE complete debug coverage');return bytes(b)
def globals(o):
 b=debug_bytes(o);at=0;out=[]
 while at<len(b):
  n=b[at];require(n>0 and at+n+1<=len(b),'savedBYTE global bound');v=b[at+1:at+n+1];require(v[0]==5 and len(v)>=8 and len(v)==8+v[7],'savedBYTE complete global');out.append({'symbol':'_'+v[8:].decode('ascii'),'type_index':int.from_bytes(v[5:7],'little'),'offset':at,'raw':v.hex()});at+=n+1
 require(at==len(b),'savedBYTE debug EOF');return out
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'savedBYTE exact registry fields')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('input-saved-bytes-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'savedBYTE exact source/compiler profile')
 require(item['objects']==[{'symbol':n,'size':1,'storage':'near-common'}for n in NAMES]and all(type(x['size'])is int for x in item['objects']),'savedBYTE exact four logical extents');require(item['evidence']==PINS,'savedBYTE exact evidence selection')
def validate_object(raw):
 require(isinstance(raw,bytes),'savedBYTE whole raw object bytes');o=read_omf(raw);require(not o.publics and not o.procedures,'savedBYTE no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',98,32),(6,'$$TYPES','DEBTYP',0,32)],'savedBYTE exact empty loaded segments/builtin-only types')
 require(all(not(s.chunks or s.unsupported_data)for s in o.segments.values()if s.index!=5),'savedBYTE no hidden loaded/type data');defs=[];count=0
 for k,at,v in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'savedBYTE unsupported raw record')
  if k==0xb0:
   count+=1;q=_Cursor(v)
   while q:
    n,t,kind,size=q.name(),q.index(),q.byte(),q.byte();require(kind==0x62 and size==1 and t==132,'savedBYTE exact nearCOMMON1 unsigned132');defs.append({'symbol':n,'type_index':t,'communal_kind':kind,'size':size,'storage':'near-common'})
  elif k==0x88:require(v in[bytes.fromhex(x)for x in['009d30734f','00a1014356','00a201']],'savedBYTE unknown COMMENT')
  elif k==0x9a:require(v==bytes.fromhex('02ff03ff04ff02'),'savedBYTE exact DGROUP')
  elif k==0x8a:require(v==b'\0','savedBYTE no entrypoint')
 require(count==1 and defs==[{'symbol':n,'type_index':132,'communal_kind':98,'size':1,'storage':'near-common'}for n in NAMES],'savedBYTE complete four definitions/name/type/order')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'savedBYTE exact external inventory')
 require([(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups]==[(5,off,4,3,True,(5,None),(2,t),None)for off,t in[(76,5),(52,4),(28,3),(2,2)]],'savedBYTE only four DEBUG FAR fields')
 require(all(sn==5 for pos,sn,off,n in o.data_writes),'savedBYTE initialized nondebug bytes forbidden');require(not any(pos>f.record_offset and sn==f.segment and off<f.offset+4 and f.offset<off+n for f in o.fixups for pos,sn,off,n in o.data_writes),'savedBYTE DEBUG field overwritten')
 require([(x['symbol'],x['type_index'])for x in globals(o)]==[(n,132)for n in NAMES],'savedBYTE complete unsigned globals')
 require(debug_bytes(o).hex()=='19050000000084001173617665645f637572736f725f3864306117050000000084000f6163746f725f666c61675f3933373417050000000084000f696e7075745f6d6f64655f3938346517050000000084000f696e7075745f666c61675f38666530','savedBYTE exact complete DEBUG stream');require(sha(raw)==OBJECT_SHA,'savedBYTE exact genuine whole-object hash');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'savedBYTE exact evidence selection');project=Path(project).resolve();p={}
 for key,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'savedBYTE evidence pin '+key);p[key]=b
 ownership=json.loads(p['ownership']);producer=json.loads(p['producer']);generation=json.loads(p['generation']);context=json.loads(p['context']);assembly=json.loads(p['ASM_comparison']);asmgen=json.loads(p['ASM_generation']);crt=json.loads(p['CRT_REA'])
 require(sha(p['ownership_freeze'])=='1590352dd51173a471488b8848d0a2a476d700e614fc12c831149f94812d3a08','savedBYTE closed actual evidence freeze')
 require(ownership['status'].startswith('SUPPORTED')and not ownership['actual_root_MASM_corroboration_pending']and len(ownership['current_all30_strict_decoders'])==30 and len(ownership['current_all114_near_disjoint_ranges'])==114 and len(ownership['current_far2_separate'])==2 and not ownership['registered_initialized_DATA_overlap'],'savedBYTE complete old scope/disjoint initialized extent proof')
 require(producer['status'].startswith('GENUINE_FOUR_BYTE_PROVIDER_COMPATIBLE_PASS')and producer['whole_object_sha256']==OBJECT_SHA and producer['actual_CV_unsigned_BYTE_builtin']==132 and producer['logical_COMMON_bytes']==4 and producer['initialized_bytes']==0,'savedBYTE actual producer scope');validate_object(p['producer_object'])
 require(generation['actual_compiler_calls']==1 and generation['source_sha256']==SOURCE_SHA and generation['object_sha256']==OBJECT_SHA and generation['flags']==FLAGS and generation['tool_hashes']==TOOLS and generation['source_tool_fresh_scratch_only']and len(generation['blocked_probes'])==5 and sha(p['source_model'])==SOURCE_SHA,'savedBYTE genuine original source/tools guard')
 spans=[(x['symbol'],x['base'],x['end_exclusive'])for x in ownership['facts']];require(spans==[(n,a,a+1)for n,a in zip(NAMES,OFFSETS)],'savedBYTE exact four1-byte views')
 for a in OFFSETS:require(all(a+1<=r['base']or r['end_exclusive']<=a for r in ownership['current_all114_near_disjoint_ranges']),'savedBYTE old114 near overlap')
 require(ownership['all_four_native_linear_bytes_beyond_maximum_decoded_FILE_image']and ownership['maximum_decoded_FILE_paragraph_bytes']==401136 and all(0x5cc20+a>401136 for a in OFFSETS),'savedBYTE memory not initializedFILE')
 require(asmgen['actual_MASM_calls']==1 and asmgen['source_tool_scratch_only']and all(c['returncode']==0 and c['terminal']and c['child_reaped_by_subprocess_run']for c in asmgen['calls']),'savedBYTE closed actual MASM producer')
 require(assembly['status']=='FULL_NATIVE180_MATCH_COMPONENT_ONLY'and assembly['whole_native_CODE_equal']and not assembly['all_differences']and assembly['native_MZ']==[]and sha(p['ASM_object'])==assembly['raw_object_sha256']==context['actual_ASM_whole_object_sha256']and sha(p['ASM_source'])==context['source_ASM_sha256'],'savedBYTE complete actual mnemonic180 identity')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'savedBYTE original target identity');ref=build_reference(original);image=ref['image'];native=image[0xfb0:0x1064];require(native==p['native180']and sha(native)==context['native_CODE_sha256'],'savedBYTE original complete native180')
 o=read_omf(p['ASM_object']);require([(s.index,s.class_name,s.length)for s in o.segments.values()]==[(1,'DATA',0),(2,'CODE',180)]and not o.procedures and set(o.publics)=={'_begin_input_0fb0','_end_input_102d'},'savedBYTE actual ASM whole shape')
 require([(o.publics[n].group,o.publics[n].segment,o.publics[n].offset)for n in['_begin_input_0fb0','_end_input_102d']]==[(0,2,0),(0,2,125)],'savedBYTE complete125/55 same-segment bounds');require([v for k,pos,v in o.records if k==0x9a]==[bytes.fromhex('02ff01')],'savedBYTE actual DGROUP')
 code=bytearray();seen=set()
 for at,b in o.segments[2].chunks:require(at==len(code)and b,'savedBYTE ASM CODE coverage');code.extend(b)
 require(len(code)==180 and not o.segments[2].unsupported_data,'savedBYTE all180 actualCODE');view=bytearray(code);expected={f['shared_CODE_field_offset']:f for f in context['expected_all34_symbolic_fields']};require(len(expected)==len(o.fixups)==34 and{f.offset for f in o.fixups}==set(expected),'savedBYTE actual34 exact symbolic fields');actual_saved=[]
 for f in o.fixups:
  q=expected[f.offset];require((f.segment,f.width,f.location_type)==(2,2,1)and f.target[0]==2 and o.externals[f.target[1]]==q['symbol'],'savedBYTE actual operand identity');call=q['kind']=='near_selfrelative_CODE';require(f.segment_relative==(not call),'savedBYTE actual operand kind')
  require(f.frame in[(5,None),(2,f.target[1])]if call else f.frame==(1,1),'savedBYTE actual CODE-target/DGROUP frame');add=int.from_bytes(code[f.offset:f.offset+2],'little');disp=f.displacement or 0;require(add+disp==q['source_addend'],'savedBYTE exact source addend');value=(context['bindings'][q['symbol']]+add+disp-(q['native_field_offset']+2 if call else 0))&65535;view[f.offset:f.offset+2]=value.to_bytes(2,'little');require(image[q['native_field_offset']:q['native_field_offset']+2]==value.to_bytes(2,'little'),'savedBYTE original actual operand')
  if q['symbol']in NAMES:
   facts=[x for x in ownership['actual_eight_symbolic_BYTE_address_fields']if x['symbol']==q['symbol']and x['actual_FIXUPP']['offset']==f.offset];require(len(facts)==1 and f.raw.hex()==facts[0]['actual_FIXUPP']['raw']and f.frame==(1,1)and add==disp==0,'savedBYTE all eight actual fields');fact=facts[0];op=fact['actual_BYTE_instruction'];at=op['native_instruction_offset'];raw=image[at:at+3];require(raw.hex()==op['whole_native_instruction_bytes']and raw[0]in[0xa0,0xa2]and int.from_bytes(raw[1:],'little')==OFFSETS[NAMES.index(q['symbol'])],'savedBYTE BYTE opcode not WORD storage');actual_saved.append((q['symbol'],f.offset))
 require(bytes(view)==native and len(actual_saved)==8 and len(set(actual_saved))==8,'savedBYTE whole native180/eight BYTE fields');require(not[s for s in ref['relocations']if 0xfb0<=s<0x1064],'savedBYTE no CODE nativeMZ')
 require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['evidence_id']=='ev_587bfb28c9071a17199d532d2342ac7b6aa29f64a05a4e424d5af57686e6d032','savedBYTE authentic CRT identity');crtbytes=bytes.fromhex(crt['normalized_result']['bytes_hex']);require(crt['normalized_result']['complete']and len(crtbytes)==179 and crtbytes==image[0xea86:0xea86+179]and sha(crtbytes)=='d4cdd4a13398dc3abb17a9b9edfd09ccf9ad7f0570561ccb75a90a9522bb76fd','savedBYTE full original CRT179')
 require(crtbytes[100:115]==bytes.fromhex('1607fcbfcc52b9e0cb2bcf33c0f3aa')and crtbytes[10:13]==bytes.fromhex('bfc25c')and bytes.fromhex('fa8ed7')in crtbytes[:35],'savedBYTE actual ES5CC2 startup clear');require(all(0x52cc<=a<a+1<=0xcbe0 for a in OFFSETS),'savedBYTE CRT clear bounds')
 return[{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(a),'end_exclusive':hex(a+1),'size':1,'resolved':False,'compatible_BYTE_view':True,'historical_type_storageclass_capacity_TU_order_MAP_proven':False}for n,a in zip(NAMES,OFFSETS)]

@contextmanager
def source_generation_scope(project,source,target):
 project=Path(project).resolve();source=Path(source).resolve();allowed={source,project/'config/msc500.json',project/'toolchains/msc500/manifest.json',*((project/'toolchains/msc500'/n).resolve()for n in TOOLS)};rb=Path.read_bytes;rt=Path.read_text;oldtemp=tempfile.TemporaryDirectory;roots=[];reads=[];denied=[]
 def temporary(*args,**kw):
  t=oldtemp(*args,**kw);require(Path(t.name).name.startswith('battlechess-msc-'),'savedBYTE genuine fresh compiler scratch');roots.append(Path(t.name).resolve());return t
 def permit(p):
  q=Path(p).resolve()
  if q not in allowed and not any(q==r/n for r in roots for n in['UNIT.OBJ','COMPILE.LOG']):denied.append(str(q));raise ValueError('savedBYTE forbidden generation read '+str(q))
  reads.append(str(q))
 def bread(p,*a,**k):permit(p);return rb(p,*a,**k)
 def tread(p,*a,**k):permit(p);return rt(p,*a,**k)
 with patch.object(Path,'read_bytes',bread),patch.object(Path,'read_text',tread),patch.object(tempfile,'TemporaryDirectory',temporary):
  for p in[Path(target),project/'build/exepack/TRIM5_UNPACK.EXE',local(project,PINS['producer_object']['path']),local(project,PINS['ownership']['path']),local(project,PINS['ASM_object']['path'])]:
   try:p.read_bytes()
   except ValueError:pass
   else:raise ValueError('savedBYTE source guard inactive')
  yield reads,denied,roots
 require(len(denied)==5 and len(roots)==1,'savedBYTE exact denied comparisons/one fresh scratch')
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);require((project/SOURCE).is_file()and not(project/SOURCE).is_symlink(),'savedBYTE regular source');before=source.read_bytes();require(sha(before)==SOURCE_SHA,'savedBYTE source hash');constraints=validate_evidence(project,item['evidence'],target)
 with source_generation_scope(project,source,target)as(reads,denied,roots):c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'savedBYTE exact fresh compiler provenance');defs=validate_object(c.object_bytes);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'input-saved-bytes-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(source_tool_fresh_scratch_only=True,generation_reads=reads,blocked_comparison_probes=denied,fresh_scratch_roots=[str(r)for r in roots],comparison_reads_separate=True)
 return{'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_four_BYTE_views_no_historical_type_storageclass_TU_capacity_MAP_claim'}
