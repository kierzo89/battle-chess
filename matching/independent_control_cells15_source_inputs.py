"""Versioned consumed-compatible COMMON15 cells; zero initialized/function credit."""
from pathlib import Path
import dataclasses,hashlib,json,tempfile,re,builtins,io,os,shutil,codecs,locale
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256,CARRIER_SHA256
from independent_control_cells15_profile_pins import PINS,TOOLS,MANIFEST_SHA,SOURCE_SHA,OBJECT_SHA,DEFS,RECORD_PINS,FIELD_PROFILE,DEBUG_HEX,EXTERNALS
from independent_control_cells15_generation_scope import scope
BACKEND='msc500-near-common-independent-control-cells15-v1';SOURCE='src/link/independent_control_cells.c';FLAGS=['/AS','/Zl','/Zi'];NAMES=[q[0]for q in DEFS];DOSBOX_SHA='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,message):
 if not v:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'control15 relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'control15 path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'control15 exact registry keys')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('independent-control-cells15-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'control15 exact source/profile')
 require(item['objects']==[{'symbol':n,'size':s,'storage':'near-common'}for n,t,s,ds in DEFS]and all(type(x['size'])is int for x in item['objects']),'control15 fifteen complete near definitions');require(item['evidence']==PINS,'control15 owned evidence selection')
def segment_bytes(o,klass):
 ss=[s for s in o.segments.values()if s.class_name==klass]
 if not ss:return b''
 require(len(ss)==1,'control15 one segment class');s=ss[0];out=bytearray(s.length);seen=set()
 for at,v in s.chunks:
  require(0<=at<=at+len(v)<=s.length,'control15 data bounds');out[at:at+len(v)]=v;seen.update(range(at,at+len(v)))
 require(len(seen)==s.length,'control15 complete ordered segment');return bytes(out)
def validate_object(raw):
 require(type(raw)is bytes,'control15 whole raw bytes');o=read_omf(raw)
 require(not o.publics and not o.procedures,'control15 no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',327,32),(6,'$$TYPES','DEBTYP',0,32)],'control15 zero loaded allocations and exact DEBUG327')
 require(all(s==5 for _,s,_,_ in o.data_writes),'control15 debug-only writes');defs=[];count=0
 for k,at,p in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'control15 unknown/foreign record')
  if k==0xb0:
   count+=1;c=_Cursor(p)
   while c:
    n,t,kind,size=c.name(),c.index(),c.byte(),c.byte();require(kind==0x62 and(n,t,size)in[(n,t,s)for n,t,s,ds in DEFS],'control15 exact primitive nearCOMMON62');defs.append({'symbol':n,'type_index':t,'datatype':kind,'size':size})
 expected=[{'symbol':n,'type_index':t,'datatype':0x62,'size':s}for n,t,s,ds in DEFS];require(count==1 and defs==expected and len(defs)==15,'control15 one record/fifteen exact definitions')
 require(o.externals==EXTERNALS and segment_bytes(o,'DEBSYM').hex()==DEBUG_HEX,'control15 exact DEBUG/externals')
 fp=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups];require(fp==FIELD_PROFILE and len(fp)==15 and all(f.segment==5 and f.width==4 and f.location_type==3 for f in o.fixups),'control15 only exact fifteen DEBUG FAR fields')
 require([(k,at,sha(p))for k,at,p in o.records]==RECORD_PINS,'control15 every raw record and THREAD payload');require(len(raw)==912 and sha(raw)==OBJECT_SHA,'control15 exact genuine whole912B object')
 return [dict(q,communal_kind=0x62,storage='near-common')for q in defs]
def _width(image,site):
 op,m=image[site-2:site];byte={0x88,0x8a,0x38,0x3a,0x00,0x02,0x28,0x2a,0x80,0xc6,0xfe,0xf6,0x20,0x22,0x08,0x0a,0x30,0x32,0x84};word={0x89,0x8b,0x39,0x3b,0x01,0x03,0x29,0x2b,0x81,0x83,0xc7,0xf7,0x21,0x23,0x09,0x0b,0x31,0x33,0x85}
 if m&0xc7==6 and op in byte|word:return 1 if op in byte else 2,2
 if m&0xc7==6 and op==0xff and(m>>3)&7 in(0,1,6):return 2,2
 if m in(0xa0,0xa2):return 1,1
 if m in(0xa1,0xa3):return 2,1
 raise ValueError('control15 unknown memory encoding')
def _has_instruction(doc,at,text):
 if isinstance(doc,str):
  m=re.match(r'^0x([0-9a-fA-F]+):\s+(.*)$',doc);return bool(m and int(m[1],16)==at and m[2]==text)
 if isinstance(doc,list):return any(_has_instruction(v,at,text)for v in doc)
 if isinstance(doc,dict):return any(_has_instruction(v,at,text)for v in doc.values())
 return False
def validate_evidence(project,pins,target):
 require(pins==PINS,'control15 exact owned evidence');p={}
 for name,row in PINS.items():
  b=local(project,row['path']).read_bytes();require(sha(b)==row['sha256'],'control15 owned pin '+name);p[name]=b
 proof=json.loads(p['ownership']);g=json.loads(p['actual_generation']);positive=json.loads(p['actual_comparison']);tool=json.loads(p['actual_tool']);current=json.loads(p['current_scope']);prior=json.loads(p['prior_allocations']);profile=json.loads(p['format_profile'])
 require(proof['status']=='EVIDENCE_COMPLETE_COMPATIBLE15_CELL_COMMON_SOURCE_PROPOSAL_NOT_GENERATED'and proof['near_definition_count']==15 and proof['logical_BSS_bytes']==27 and proof['native_CODE_fields']==105 and proof['DEBUG_address_fields']==37,'control15 eligibility scope')
 require([(q['symbol'],q['type_index'],q['size'],q['native_DS'])for q in proof['definitions']]==DEFS,'control15 native definition identities')
 require(current['current_objects']==254 and current['current_missing']==90 and current['prior251_whole_object_prefix_exact']and current['proposed15_unchanged_no_newclients']and [r['name']for r in current['added_ARRAY_view_fields']]==['_frames','_frames','_piece_controls'],'control15 current254 scope and held640 views')
 require(g['status']=='COMPLETE'and g['guard_closed']and g['actual_C5_calls']==1 and len(g['calls'])==1 and g['calls'][0]['terminal']and g['calls'][0]['reaped']and g['calls'][0]['returncode']==0 and g['source_tools_new_scratch_only']and not g['native_original_oldOBJ_comparison_inputs_inside_GEN']and len(g['blocked_probes'])==20 and g['source_sha256']==SOURCE_SHA and g['raw_whole_object_sha256']==OBJECT_SHA and g['compiler']=='msc500'and g['flags']==FLAGS and g['source_name']=='UNIT.C','control15 genuine source-only control')
 require(tool['exit_code']==0 and tool['terminal']and tool['reaped']and tool['raw_object_sha256']==OBJECT_SHA and tool['raw_object_bytes']==912 and tool['generation_receipt_sha256']==sha(p['actual_generation']),'control15 root terminal')
 require(positive['status']=='PASS_GENUINE_C5_15_NEAR_COMMON27_LOGICAL_BYTES'and positive['raw_object_sha256']==OBJECT_SHA and positive['near_definition_count']==15 and positive['COMDEF_records']==1 and positive['logical_BSS_bytes']==27 and positive['loaded_CODE_DATA_CONST_BSS_bytes']==0 and positive['PUBLIC_count']==0 and positive['DEBUG_bytes']==327,'control15 genuine whole raw comparison');validate_object(p['producer_object'])
 require(profile['schema']=='independent-control-cells15-common-profile-v1'and profile['source_sha256']==SOURCE_SHA and profile['object_sha256']==OBJECT_SHA and profile['raw_object_bytes']==912 and profile['definitions']==[list(q)for q in DEFS],'control15 versioned format profile')
 ref=build_reference(Path(target).read_bytes());require(ref['original_sha256']==ORIGINAL_SHA256 and len(ref['image'])==0x61eeb,'control15 original reference');image=ref['image'];crt=json.loads(p['crt_native']);b=bytes.fromhex(crt['raw_result']['bytes_hex']);require(b==image[0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in b,'control15 exact native clear bounds')
 near=prior['near127'];require(len(near)==127 and sum(q['size']for q in near)==4951 and len(prior['far2_one_provider_retained'])==2,'control15 prior near/far inventory')
 for n,t,s,ds in DEFS:
  require(0x52d0<=ds<ds+s<=0xcbe0 and 0x5cc20+ds>=len(image)and not(0x8172<ds+s and ds<0x8250)and all(not(q['native_DS']<ds+s and ds<q['native_DS']+q['size'])for q in near),'control15 native RAM/disjoint/limit exclusion')
 for i,a in enumerate(DEFS):
  for b in DEFS[i+1:]:require(not(a[3]<b[3]+b[2]and b[3]<a[3]+a[2]),'control15 mutual overlap')
 named=proof['all_named_fields'];require(len(named)==142,'control15 complete field inventory');counts={'CODE':0,'DEBSYM':0};typed={n:t for n,t,s,ds in DEFS};native_defs={n:(s,ds)for n,t,s,ds in DEFS};clients=proof['owned_client_sources'];require(len(clients)==28,'control15 all28 clientTUs')
 for client in clients:
  slot=str(client['slot']);raw=p['client_'+slot];src=p['source_'+slot];require(sha(raw)==client['raw_object_sha256']and sha(src)==client['source_sha256'],'control15 owned whole client/source');o=read_omf(raw);text=src.decode();group=[q for q in named if q['slot']==client['slot']];require(len(group)==client['field_count'],'control15 perclient count')
  for n,decls in client['declarations'].items():require(decls and all(d in text for d in decls),'control15 retained C/ASM declarations')
  if client['source'].endswith('.c'):
   deb=segment_bytes(o,'DEBSYM');at=0;globs=[]
   while at<len(deb):
    num=deb[at];r=deb[at+1:at+1+num];require(num>0 and len(r)==num,'control15 bounded CV globals')
    if r[0]==5:
     name='_'+r[8:].decode('ascii')
     if name in typed:globs.append((name,int.from_bytes(r[5:7],'little')))
    at+=num+1
   require(sorted(globs)==sorted((n,typed[n])for n in client['declarations']),'control15 all client reconstructed primitive/pointer types')
  actual=[f for f in o.fixups if f.target[0]==2 and o.externals.get(f.target[1])in NAMES];require(len(actual)==len(group),'control15 every current client field')
  for f,q in zip(actual,group):
   model=dataclasses.asdict(f);model.update(raw=f.raw.hex(),frame=list(f.frame),target=list(f.target));require(model==q['field']and o.externals[f.target[1]]==q['name'],'control15 raw field boundary/target identity');counts[q['class']]+=1
   if q['class']=='DEBSYM':require(o.segments[f.segment].class_name=='DEBSYM'and f.width==4,'control15 debugaddress notvaluedcell');continue
   require(q['class']=='CODE'and o.segments[f.segment].class_name=='CODE'and f.width==2 and f.location_type==1 and f.segment_relative,'control15 actual native OFFSET16 field');code=segment_bytes(o,'CODE');add=int.from_bytes(code[f.offset:f.offset+2],'little')+(f.displacement or 0);site=q['native_image_field'];s,ds=native_defs[q['name']];width,prefix=_width(image,site)
   require(add==q['source_addend']and int.from_bytes(image[site:site+2],'little')==ds+add and 0<=add and add+width<=s and code[f.offset-prefix:f.offset]==image[site-prefix:site]and site not in ref['relocations'],'control15 actual memorywidth/address/subfield bounds')
   obs=q['retained_instruction'];require(obs['operand_effect']=='memory'and obs['memory_width']==width and q['fits_complete_cell']is True,'control15 no address/calleeextent escape');primary=obs['primary']
   if primary=='ORIGINAL_UNCHANGED_PREFIX':require(site+2<=ref['prefix_size'],'control15 original unchanged CODE prefix')
   else:
    key=proof['owned_native_primary_keys'][primary];doc=json.loads(p[key]);require(doc['subject']['digest']['sha256']in(ORIGINAL_SHA256,CARRIER_SHA256),'control15 native primary target');r=doc.get('raw_result')
    if isinstance(r,dict)and 'bytes_hex'in r:
     start=int(r['address'],0)-0x10000;body=bytes.fromhex(r['bytes_hex']);require(r['complete']and r['requested_bytes']==r['returned_bytes']==len(body)and start<=site-prefix and site+2<=start+len(body)and body[site-prefix-start:site+2-start]==image[site-prefix:site+2],'control15 fullraw primary bounds')
    else:require(_has_instruction(doc,obs['native_instruction_image']+0x10000,obs['instruction']),'control15 retained provider instruction')
 require(counts=={'CODE':105,'DEBSYM':37},'control15 every105CODE37CV')
 return [{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(ds),'end_exclusive':hex(ds+s),'size':s,'resolved':False,'compatible_model':'consumed_primitive_or_near_BYTE_pointer','initialized_byte_credit':0,'historical_unique_TU_grouping_or_absolute_MAP_proven':False,'neighbor_capacity_claim':False}for n,t,s,ds in DEFS]

def invoke_standard(source,project,compiler_fn):
 tempfile.gettempdir();locale.getpreferredencoding(False);codecs.lookup('utf8');codecs.lookup('cp437');path_before=os.environ.get('PATH');default=shutil.which('dosbox');require(default is not None and Path(default).resolve()==Path('/usr/bin/dosbox').resolve(),'control15 pinned default DOSBox resolution');probes=[]
 with scope(source,project)as events:
  require(sha(Path(default).resolve().read_bytes())==DOSBOX_SHA,'control15 pinned host executable')
  for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/PINS['producer_object']['path'],project/PINS['ownership']['path'],project/'config/units.json']:
   for api,fn in[('Path.read_bytes',lambda p:p.read_bytes()),('builtins.open',lambda p:builtins.open(p,'rb')),('io.open',lambda p:io.open(p,'rb')),('os.open',lambda p:os.open(p,os.O_RDONLY))]:
    try:fn(forbidden)
    except ValueError:probes.append({'path':str(forbidden),'API':api,'denied':True})
    else:raise ValueError('control15 source-only probe allowed')
  require(len(events['blocked'])==20,'control15 all20 active denials');c=compiler_fn(source,FLAGS,compiler='msc500');require(os.environ.get('PATH')==path_before and shutil.which('dosbox')==default and sha(Path(default).resolve().read_bytes())==DOSBOX_SHA,'control15 unchanged pinned default host')
 return c,{'source_tool_scratch_guard':events,'active_open_API_probes':probes,'host_default_dosbox':{'argv0':'dosbox','resolved':str(Path(default).resolve()),'sha256':DOSBOX_SHA,'PATH_unchanged':True,'explicit_dosbox_override':False},'generation_comparison_input':False}
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'control15 source pin');c,guard=invoke_standard(source,project,compile_c if compiler_fn is None else compiler_fn);require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'control15 fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'independent-control-cells15-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(guard)
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':27,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'COMMON_kind':'near','compiler':meta,'allocation_profile':'fifteen_consumed_complete_cells_no_historical_TU_or_MAP_claim'}
