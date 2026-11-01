"""Opt-in compatible unsignedchar animation COMMON1; no historical signedness/storage claim."""
from pathlib import Path
import dataclasses,hashlib,json,tempfile,re,builtins,io,os,shutil
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from link16 import link_function
from animation_counter_profile_pins import PINS,TOOLS,MANIFEST_SHA,SOURCE_SHA,OBJECT_SHA,RECORD_PINS,FIELD_PROFILE
from animation_counter_generation_scope import scope
BACKEND='msc500-near-common-animation-counter9602-v1';SOURCE='src/link/animation_counter.c';DOSBOX_SHA='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477';NAMES=['_animation_counter'];FLAGS=['/AS','/Zl','/Zi']
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'animation-counter relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'animation-counter path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'animation-counter exact registry keys')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('animation-counter-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'animation-counter exact source/compiler profile')
 require(item['objects']==[{'symbol':'_animation_counter','size':1,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'animation-counter exact compatible unsigned BYTE storage');require(item['evidence']==PINS,'animation-counter exact owned evidence selection')
def debug(o):
 s=o.segments[5];v=bytearray(s.length);seen=set()
 for at,b in s.chunks:require(0<=at<=at+len(b)<=s.length,'animation-counter debug bounds');v[at:at+len(b)]=b;seen.update(range(at,at+len(b)))
 require(len(seen)==s.length,'animation-counter whole debug coverage');return bytes(v)
def validate_object(raw):
 require(type(raw)is bytes,'animation-counter whole raw object');o=read_omf(raw)
 require(not o.publics and not o.procedures,'animation-counter no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',26,32),(6,'$$TYPES','DEBTYP',0,32)],'animation-counter empty loaded segments/exact scalar debug')
 require(all(s==5 for _,s,_,_ in o.data_writes),'animation-counter no loaded bytes/type arrays')
 defs=[]
 for k,at,p in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'animation-counter unknown/foreign OMF record')
  if k==0xb0:
   c=_Cursor(p)
   while c:
    name,typ,kind,size=c.name(),c.index(),c.byte(),c.byte();require((name,typ,kind,size)==('_animation_counter',0x84,0x62,1),'animation-counter compatible unsigned84 nearCOMDEF62 size1 only');defs.append({'symbol':name,'type_index':typ,'datatype':kind,'size':size})
 require(defs==[{'symbol':'_animation_counter','type_index':0x84,'datatype':0x62,'size':1}],'animation-counter exact single scalar definition')
 require(o.externals=={1:'__acrtused',2:'_animation_counter'},'animation-counter genuine scalar/debug external binding')
 require(debug(o)==bytes.fromhex('190500000000840011616e696d6174696f6e5f636f756e746572'),'animation-counter scalar compatible unsigned84 global CV')
 fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups];require(fields==FIELD_PROFILE and len(fields)==1,'animation-counter only exact debug FAR binding')
 require([(k,at,sha(p))for k,at,p in o.records]==RECORD_PINS,'animation-counter every raw record accounted');require(sha(raw)==OBJECT_SHA,'animation-counter exact genuine whole object');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'animation exact evidence');p={}
 for name,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'animation owned evidence '+name);p[name]=raw
 proof=json.loads(p['ownership']);g=json.loads(p['actual_generation']);positive=json.loads(p['actual_comparison']);tool=json.loads(p['actual_tool'])
 require(proof['status'].startswith('SUPPORTED compatible unsigned-char scalar1')and proof['compatible_declaration']=='unsigned char animation_counter;'and proof['native_DS_interval']==[0x9602,0x9603],'animation compatible byte model, not historical signedness')
 require(proof['actual_selected245_objects_scanned']==245 and len(proof['actual_clients'])==2 and len(proof['all_actual_fields'])==4 and proof['current_PUBLIC_COMDEF_collisions']==[],'animation bounded actual clients/provider inventory')
 require(g['status']=='COMPLETE'and g['actual_C5_calls']==1 and g['source_tool_freshscratch_only']and g['source_sha256']==SOURCE_SHA and g['raw_object_sha256']==OBJECT_SHA and len(g['active_open_API_probes'])==20 and len(g['guard']['blocked'])==20 and g['terminal']and g['child_reaped'],'animation genuine closed oneC5 control')
 require(tool['exit_code']==0 and tool['terminal']and tool['reaped']and tool['actual_C5_calls']==1 and tool['comparison_exit_code']==0 and tool['raw_sha256']==OBJECT_SHA and positive['raw_object_sha256']==OBJECT_SHA,'animation root terminal/comparison receipt');validate_object(p['producer_object'])
 ref=build_reference(Path(target).read_bytes());require(ref['original_sha256']==ORIGINAL_SHA256 and len(ref['image'])==0x61eeb and 0x5cc20+0x9602==0x66222>len(ref['image'])and 0x52cc<=0x9602<0x9603<=0xcbe0,'animation uninitialized RAM outsideFILE/insideCRTclear')
 crt=json.loads(p['crt_native']);rawcrt=bytes.fromhex(crt['normalized_result']['bytes_hex']);require(rawcrt==ref['image'][0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in rawcrt,'animation actual CRT clear')
 ranges=proof['accepted32_near119_ranges_disjoint'];require(len(ranges)==119 and all(not(r['start']<0x9603 and r['start']+r['size']>0x9602)for r in ranges)and proof['accepted_far_definitions_kept_separate']==2 and proof['current_staged33_extra_provider_disjoint']['native_interval']==[0x57d0,0x57d2],'animation accepted32/current33 nonoverlap; no future profile assertion')
 counts={'CODE':0,'DEBUG':0}
 for client in proof['actual_clients']:
  slot=str(client['slot']);o=read_omf(p['client_'+slot]);src=p['source_'+slot];require(sha(p['client_'+slot])==client['raw_object_sha256']and sha(src)==client['source_sha256'],'animation complete matching reconstructed client copies')
  text=src.decode();require(re.search(r'\btypedef\s+unsigned\s+char\s+Byte\s*;',text)and re.search(r'\bextern\s+Byte\s+[^;]*\banimation_counter\s*;',text),'animation reconstructedC unsignedByte scalar model')
  data=debug(o);at=0;hits=[]
  while at<len(data):
   n=data[at];v=data[at+1:at+1+n];require(n>0 and len(v)==n,'animation whole reconstructed clientCV')
   if v[0]==5 and v[8:]==b'animation_counter':hits.append(int.from_bytes(v[5:7],'little'))
   at+=n+1
  require(at==len(data)and hits==[0x84],'animation CV84 from reconstructed matching clients, not shipped debug types')
  actual=[f for f in o.fixups if f.target[0]==2 and o.externals.get(f.target[1])=='_animation_counter'];expected=[r for r in proof['all_actual_fields']if r['slot']==client['slot']];require(len(actual)==len(expected),'animation all actual fields')
  for f,r in zip(actual,expected):
   model=dataclasses.asdict(f);model.update(raw=f.raw.hex(),frame=list(f.frame),target=list(f.target));require(model==r['raw_field'],'animation exact field identity/boundary');counts[r['kind']]+=1
   if r['kind']=='CODE':
    require(f.width==2 and f.location_type==1 and f.segment_relative and f.frame==(5,None)and not f.displacement,'animation16bit address operand');v=bytearray(o.segments[f.segment].length)
    for at,b in o.segments[f.segment].chunks:v[at:at+len(b)]=b
    site=r['native_field'];require(v[f.offset-2:f.offset+2]==bytes.fromhex('00060000')and ref['image'][site-2:site+2]==bytes.fromhex('00060296')and site not in ref['relocations']and r['memory_access_bits']==8,'animation real native BYTE ADD/noMZ; no WORD-valued scalar inference')
   else:require(o.segments[f.segment].class_name=='DEBSYM'and f.width==4,'animation debug address only')
 require(counts=={'CODE':2,'DEBUG':2},'animation complete2BYTE/2DEBUG inventory')
 for key in['command_native','capture_native']:
  e=json.loads(p[key]);a=e['normalized_result']['assembly'];a='\n'.join(a)if isinstance(a,list)else a;require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and'ADD byte ptr [0x9602], AL'in a,'animation original BYTE operation primary')
 return [{'symbol':'_animation_counter','dgroup_segment':'0x5cc2','dgroup_offset':'0x9602','end_exclusive':'0x9603','size':1,'resolved':False,'compatible_model':'unsigned char8 accumulation scalar from matching reconstructed clients','initialized_byte_credit':0,'original_historical_declaration_signedness_COMM_TU_MAP_proven':False,'neighbor_capacity_claim':False}]

# Standard existing-COMMON compiler_fn signature: no dosbox keyword override.
# The first scalar control used /usr/bin/dosbox explicitly. Here the pinned
# msc default argv0='dosbox' is resolved before/after to that same binary, with
# unchanged PATH and exact compiler result/tool/object acceptance. No alternate
# configuration or third aggregate wrapper keyword is introduced.
def invoke_standard(source,project,compiler_fn):
 tempfile.gettempdir();path_before=os.environ.get('PATH');default=shutil.which('dosbox');require(default is not None and Path(default).resolve()==Path('/usr/bin/dosbox').resolve(),'animation exact default DOSBox resolution')
 probes=[]
 with scope(source,project)as events:
  require(sha(Path(default).resolve().read_bytes())==DOSBOX_SHA,'animation default host executable pin')
  for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/PINS['producer_object']['path'],project/PINS['ownership']['path'],project/'config/units.json']:
   for api,fn in[('Path.read_bytes',lambda p:p.read_bytes()),('builtins.open',lambda p:builtins.open(p,'rb')),('io.open',lambda p:io.open(p,'rb')),('os.open',lambda p:os.open(p,os.O_RDONLY))]:
    try:fn(forbidden)
    except ValueError:probes.append({'path':str(forbidden),'API':api,'denied':True})
    else:raise ValueError('animation source-only probe allowed')
  require(len(events['blocked'])==20,'animation20 active open denials')
  c=compiler_fn(source,FLAGS,compiler='msc500')
  require(os.environ.get('PATH')==path_before and shutil.which('dosbox')==default and sha(Path(default).resolve().read_bytes())==DOSBOX_SHA,'animation unchanged same default DOSBox after call')
 return c,{'source_tool_scratch_guard':events,'active_open_API_probes':probes,'host_default_dosbox':{'argv0':'dosbox','resolved':str(Path(default).resolve()),'sha256':DOSBOX_SHA,'PATH_unchanged':True,'explicit_dosbox_override':False},'generation_comparison_input':False}
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'animation exact standalone source')
 c,guard=invoke_standard(source,project,compile_c if compiler_fn is None else compiler_fn)
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'animation exact fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'animation-counter-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(guard)
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':1,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_unsignedchar_byte_model_no_original_signedness_storage_class_TU_MAP_claim'}
