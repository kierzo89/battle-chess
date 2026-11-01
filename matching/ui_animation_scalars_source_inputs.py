"""Opt-in compatible coordinate/flag nearCOMMON cells; no historical source/storage claim."""
from pathlib import Path
import dataclasses,hashlib,json,tempfile,re,builtins,io,os,shutil
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from ui_animation_scalars_profile_pins import PINS,TOOLS,MANIFEST_SHA,SOURCE_SHA,OBJECT_SHA,RECORD_PINS,FIELD_PROFILE,DEBUG_HEX,EXTERNALS
from ui_animation_scalars_generation_scope import scope
BACKEND='msc500-near-common-ui-animation-scalars-v1';SOURCE='src/link/ui_animation_scalars.c';DOSBOX_SHA='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477';FLAGS=['/AS','/Zl','/Zi']
DEFS=[('_pointer_x',0x81,2,0x933a),('_pointer_y',0x81,2,0x935e),('_menu_blink',0x84,1,0x933c),('_animation_busy',0x84,1,0x9852)];NAMES=[x[0]for x in DEFS]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'UI scalar relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'UI scalar path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'UI scalar exact registry keys')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('ui-animation-scalars-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'UI scalar exact source/compiler profile')
 require(item['objects']==[{'symbol':n,'size':size,'storage':'near-common'}for n,typ,size,ds in DEFS]and all(type(x['size'])is int for x in item['objects']),'UI scalar four exact near definitions');require(item['evidence']==PINS,'UI scalar owned evidence selection')
def debug(o):
 s=o.segments[5];v=bytearray(s.length);seen=set()
 for at,b in s.chunks:require(0<=at<=at+len(b)<=s.length,'UI scalar debug bounds');v[at:at+len(b)]=b;seen.update(range(at,at+len(b)))
 require(len(seen)==s.length,'UI scalar whole debug coverage');return bytes(v)
def validate_object(raw):
 require(type(raw)is bytes,'UI scalar whole raw object');o=read_omf(raw)
 require(not o.publics and not o.procedures,'UI scalar no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',78,32),(6,'$$TYPES','DEBTYP',0,32)],'UI scalar empty loaded segments/exact debug78')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'UI scalar no loaded/type storage')
 defs=[];count=0
 for k,at,p in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'UI scalar unknown/foreign OMF record')
  if k==0xb0:
   count+=1;c=_Cursor(p)
   while c:
    name,typ,kind,size=c.name(),c.index(),c.byte(),c.byte();require(kind==0x62 and(name,typ,size)in[(n,t,s)for n,t,s,ds in DEFS],'UI scalar exact primitive nearCOMMON62 only');defs.append({'symbol':name,'type_index':typ,'datatype':kind,'size':size})
 expected=[{'symbol':n,'type_index':t,'datatype':0x62,'size':s}for n,t,s,ds in DEFS];require(count==1 and defs==expected,'UI scalar one rawCOMDEF record/four definitions only')
 require(o.externals==EXTERNALS and debug(o).hex()==DEBUG_HEX,'UI scalar genuine debug globals/external bindings')
 fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups];require(fields==FIELD_PROFILE and len(fields)==4 and all(f.segment==5 and f.width==4 and f.location_type==3 for f in o.fixups),'UI scalar four exact debugFAR fields only')
 require([(k,at,sha(p))for k,at,p in o.records]==RECORD_PINS,'UI scalar every raw record accounted');require(len(raw)==403 and sha(raw)==OBJECT_SHA,'UI scalar exact genuine whole403B object');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'UI scalar exact evidence');p={}
 for name,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'UI scalar owned evidence '+name);p[name]=raw
 proof=json.loads(p['ownership']);g=json.loads(p['actual_generation']);positive=json.loads(p['actual_comparison']);tool=json.loads(p['actual_tool'])
 require(proof['status'].startswith('SUPPORTED compatible four nearBSS scalars6logicalbytes')and proof['source_model']=='int pointer_x; int pointer_y; unsigned char menu_blink; unsigned char animation_busy;','UI scalar compatible model, no historical declaration')
 require(len(proof['all_actual_source_clients'])==9 and proof['total_client_CODE_fields']==33 and proof['total_client_DEBUG_FAR_fields']==15 and len(proof['all48_fields'])==48 and proof['existing_named_PUBLIC_or_COMMON_providers']==[]and proof['other_actual_used_native_DS_identifier_candidates']==[],'UI scalar complete current244 client/name inventory')
 current=json.loads(p['current_scope']);require(current['status']=='PASS_CLOSED_CURRENT466_SOURCE245_EQUIVALENT_NINE_CLIENTS'and current['actual_source_objects']==245 and current['COMMON_providers']==34 and current['all9_whole_raw_sources_and48_fields_identical_to_retained244']is True and len(current['all_actual_clients'])==9 and{(q['source'],q['raw_object_sha256'],q['source_sha256'])for q in current['all_actual_clients']}=={(q['source'],q['whole_object_sha256'],q['source_sha256'])for q in proof['all_actual_source_clients']},'UI scalar current466/245 context closure without oldscope waiver')
 require(g['status']=='COMPLETE'and g['guard_closed']and g['actual_C5_calls']==1 and len(g['calls'])==1 and g['calls'][0]['terminal']and g['calls'][0]['reaped']and g['calls'][0]['returncode']==0 and g['source_tools_new_scratch_only']and not g['native_original_oldOBJ_comparison_inputs_inside_GEN']and g['source_sha256']==SOURCE_SHA and g['raw_whole_object_sha256']==OBJECT_SHA and len(g['blocked_probes'])==20 and g['compiler']=='msc500'and g['flags']==FLAGS and g['source_name']=='UNIT.C','UI scalar genuine closed oneC5 source-only control')
 require(tool['exit_code']==0 and tool['terminal']and tool['reaped']and tool['actual_C5_calls']==1 and positive['status']=='PASS_FOUR_GENUINE_NEAR_COMMON_SCALARS'and positive['whole_object_sha256']==OBJECT_SHA and positive['COMDEF_records']==1 and positive['logical_BSS_bytes']==6,'UI scalar root terminal/independent raw comparison');validate_object(p['producer_object'])
 ref=build_reference(Path(target).read_bytes());require(ref['original_sha256']==ORIGINAL_SHA256 and len(ref['image'])==0x61eeb,'UI scalar original decodedFILE identity')
 crt=json.loads(p['crt_native']);rawcrt=bytes.fromhex(crt['normalized_result']['bytes_hex']);require(rawcrt==ref['image'][0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in rawcrt,'UI scalar exact native CRTclear52CC..CBE0')
 ranges=proof['current34_sourceallocations']['native_compatible_ranges'];require(len(ranges)==121 and len(proof['current34_sourceallocations']['far_definitions_kept_separate'])==2,'UI scalar prior34 near/far distinction')
 for n,t,size,ds in DEFS:require(0x52cc<=ds<ds+size<=0xcbe0 and 0x5cc20+ds>=len(ref['image'])and all(not(r['start']<ds+size and r['start']+r['size']>ds)for r in ranges),'UI scalar RAM outsideFILE/insideclear/disjoint current34')
 counts={'CODE_memory_access':0,'DEBUG_FAR_global_address':0};typed={n:t for n,t,s,ds in DEFS}
 for client in proof['all_actual_source_clients']:
  slot=str(client['slot']);raw=p['client_'+slot];src=p['source_'+slot];o=read_omf(raw);require(sha(raw)==client['whole_object_sha256']and sha(src)==client['source_sha256'],'UI scalar whole matching client/source copies')
  text=src.decode()
  for name,decl in client['declarations'].items():
   require(decl in text,'UI scalar actual declaration');require(re.match(r'extern\s+int\b',decl)if typed[name]==0x81 else re.search(r'\btypedef\s+unsigned\s+char\s+Byte\s*;',text)and re.match(r'extern\s+Byte\b',decl),'UI scalar reconstructed C primitive model')
  data=debug(o);at=0;globals=[]
  while at<len(data):
   num=data[at];v=data[at+1:at+1+num];require(num>0 and len(v)==num,'UI scalar whole reconstructed CV stream')
   if v[0]==5:
    name='_'+v[8:].decode('ascii')
    if name in typed:globals.append((name,int.from_bytes(v[5:7],'little')))
   at+=num+1
  require(sorted(globals)==sorted((q['symbol'],q['type_index'])for q in client['reconstructed_CV_globals'])and all(t==typed[n]for n,t in globals),'UI scalar reconstructed signed81/unsigned84 globals, not shipped debug')
  actual=[f for f in o.fixups if f.target[0]==2 and o.externals.get(f.target[1])in NAMES];require(len(actual)==len(client['actual_fields']),'UI scalar all source client fields')
  for f,r in zip(actual,client['actual_fields']):
   model=dataclasses.asdict(f);model.update(raw=f.raw.hex(),frame=list(f.frame),target=list(f.target));require(model==r['raw_field'],'UI scalar exact typed field identity/boundary');counts[r['kind']]+=1
   if r['kind']=='CODE_memory_access':
    name=r['symbol'];n,t,size,ds=next(q for q in DEFS if q[0]==name);require(f.width==2 and f.location_type==1 and f.segment_relative and f.frame==(5,None)and not f.displacement,'UI scalar addressOFFSET16')
    code=bytearray(o.segments[f.segment].length)
    for at,body in o.segments[f.segment].chunks:code[at:at+len(body)]=body
    info=o.function_info(r['owner']);require(info['offset']<=f.offset<f.offset+2<=info['end']and info['size']==r['full_matching_CV_size'],'UI scalar complete matched CV owns field')
    native_at=r['native_instruction_image_start'];site=r['native_image_field'];delta=site-native_at;source=bytes.fromhex(r['source_instruction_hex']);native=bytes.fromhex(r['native_instruction_hex']);start=f.offset-delta
    require(bytes(code[start:start+len(source)])==source and ref['image'][native_at:native_at+len(native)]==native and int.from_bytes(native[delta:delta+2],'little')==ds and source[delta:delta+2]==b'\0\0'and r['value_access_bits']==size*8 and site not in ref['relocations'],'UI scalar all native WORD/BYTE operations and unlinkedaddress fields')
   else:require(o.segments[f.segment].class_name=='DEBSYM'and f.width==4 and not r['pointer_valued_scalar_claim'],'UI scalar debugFAR address only, no loadedMZ')
 require(counts=={'CODE_memory_access':33,'DEBUG_FAR_global_address':15},'UI scalar all nineclients33CODE/15CV')
 return [{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(ds),'end_exclusive':hex(ds+size),'size':size,'resolved':False,'compatible_model':'signedint16'if t==0x81 else'unsignedchar8','initialized_byte_credit':0,'historical_unique_declaration_signedness_COMM_TU_MAP_proven':False,'neighbor_capacity_claim':False}for n,t,size,ds in DEFS]

# Standard existing-COMMON callback; no extra DOSBox override keyword.
def invoke_standard(source,project,compiler_fn):
 tempfile.gettempdir();path_before=os.environ.get('PATH');default=shutil.which('dosbox');require(default is not None and Path(default).resolve()==Path('/usr/bin/dosbox').resolve(),'UI scalar exact default DOSBox resolution');probes=[]
 with scope(source,project)as events:
  require(sha(Path(default).resolve().read_bytes())==DOSBOX_SHA,'UI scalar default host executable pin')
  for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/PINS['producer_object']['path'],project/PINS['ownership']['path'],project/'config/units.json']:
   for api,fn in[('Path.read_bytes',lambda p:p.read_bytes()),('builtins.open',lambda p:builtins.open(p,'rb')),('io.open',lambda p:io.open(p,'rb')),('os.open',lambda p:os.open(p,os.O_RDONLY))]:
    try:fn(forbidden)
    except ValueError:probes.append({'path':str(forbidden),'API':api,'denied':True})
    else:raise ValueError('UI scalar source-only probe allowed')
  require(len(events['blocked'])==20,'UI scalar20 active open denials');c=compiler_fn(source,FLAGS,compiler='msc500')
  require(os.environ.get('PATH')==path_before and shutil.which('dosbox')==default and sha(Path(default).resolve().read_bytes())==DOSBOX_SHA,'UI scalar unchanged pinned default host')
 return c,{'source_tool_scratch_guard':events,'active_open_API_probes':probes,'host_default_dosbox':{'argv0':'dosbox','resolved':str(Path(default).resolve()),'sha256':DOSBOX_SHA,'PATH_unchanged':True,'explicit_dosbox_override':False},'generation_comparison_input':False}
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'UI scalar exact standalone source');c,guard=invoke_standard(source,project,compile_c if compiler_fn is None else compiler_fn)
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'UI scalar exact fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'ui-animation-scalars-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(guard)
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':6,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_four_scalar_cells_no_historical_storage_TU_MAP_capacity_claim'}
