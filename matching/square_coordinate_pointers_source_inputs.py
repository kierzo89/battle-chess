"""Closed two nearpointer COMMON4, no pointee allocation or matching credit."""
from pathlib import Path
import json,hashlib,dataclasses,os,shutil
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from screen_coordinate_pointers_source_inputs import payload,globals as cv_globals
from asset_fixed_arrays_source_inputs import types
from ui_animation_scalars_generation_scope import scope as source_only_scope
from square_coordinate_pointers_profile_pins import PINS,TOOLS,PROFILE_SHA,SOURCE_SHA,OBJECT_SHA,MANIFEST_SHA
BACKEND='msc500-near-common-square-coordinate-pointers-v1';SOURCE='src/link/square_coordinate_pointers.c';FLAGS=['/AS','/Zl','/Zi'];NAMES=['_square_x','_square_y'];OFFSETS=[0x8d06,0x8d0c]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,m):
 if not v:raise ValueError('squarepointer: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'relativeownedpath');r=Path(project).resolve();p=(r/name).resolve();require(p.is_relative_to(r),'pathescape');return p
def profile():
 p=Path(__file__).with_name('square_coordinate_pointers_profile.json');b=p.read_bytes();require(sha(b)==PROFILE_SHA,'closedprofilehash');return json.loads(b)
def graph(ts,t):
 if t==0xa1:return['near_pointer',['signed_int16']]
 require(t in ts,'completepointertype');b=ts[t];require(len(b)==7 and b[:3]==bytes.fromhex('7a7483')and b[5:]==bytes.fromhex('8200'),'exactanonymousnear pointerleaf74');child=int.from_bytes(b[3:5],'little');require(ts.get(child)==bytes.fromhex('78859000838100'),'exact144bit signedintrow9');return['near_pointer',['array',9,['signed_int16']]]
EXPECTED={'_square_x':['near_pointer',['array',9,['signed_int16']]],'_square_y':['near_pointer',['signed_int16']]}
def validate_provider_structure(o):
 require(not o.publics and not o.procedures and set(o.segments)==set(range(1,7)),'noPUBLIC/proc/foreignsegment')
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',34,32),('$$TYPES','DEBTYP',32,32)],'exactzero loadedallocation/debug34/type32')
 require(all(o.segments[s].class_name in['DEBSYM','DEBTYP']for _,s,_,_ in o.data_writes),'debugonlywrites');ts=types(o);gs=cv_globals(o);require(set(gs)==set(NAMES)and{n:graph(ts,gs[n])for n in NAMES}==EXPECTED,'completeproviderpointergraphs')
 defs=[];count=0
 for k,at,p in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'closedrecordkinds')
  if k==0xb0:
   count+=1;c=_Cursor(p)
   while c:defs.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  if k==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'exactDGROUP')
  if k==0x8a:require(p==b'\0','noentrypoint')
 require(count==1 and defs==[{'symbol':'_square_x','type_index':515,'datatype':98,'size':2},{'symbol':'_square_y','type_index':161,'datatype':98,'size':2}],'exacttwo nearCOMDEF2/one record');require(o.externals=={1:'__acrtused',2:'_square_x',3:'_square_y'},'exactexternnames')
 actual=[{**dataclasses.asdict(f),'frame':list(f.frame),'target':list(f.target),'raw':f.raw.hex()}for f in o.fixups];require(actual==profile()['fields']and len(actual)==2,'exacttwo genuine globalCVFARfields')
 return defs
def validate_object(raw):
 require(type(raw)is bytes,'wholebytes');o=read_omf(raw);defs=validate_provider_structure(o);require(len(raw)==352 and sha(raw)==OBJECT_SHA,'wholeactualC5fingerprint');require([{'kind':k,'offset':at,'payload_sha256':sha(p)}for k,at,p in o.records]==profile()['records'],'allrawrecords/chronology');return defs
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'exactregistrykeys');require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('square-coordinate-pointers-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'exactsource/compilerprofile');require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES]and all(type(x['size'])is int for x in item['objects']),'exacttwo cells4logicalbytes');require(item['evidence']==PINS,'exactownedevidence')
def validate_evidence(project,pins,target):
 require(pins==PINS,'exactevidence');data={}
 for n,r in PINS.items():
  b=local(project,r['path']).read_bytes();require(sha(b)==r['sha256'],'ownedpin '+n);data[n]=b
 p=json.loads(data['ownership_DATA8']);g=json.loads(data['generation']);t=json.loads(data['terminal']);sem=json.loads(data['producer_semantics'])
 require(p['status']=='SUPPORTED_INDEPENDENT_COMPATIBLE_TWO_NEAR_POINTER_CELLS_NO_ADMISSION'and p['parent_scope']==[466,35,246]and p['all246_raw_source_objects_scanned']==246 and p['pureCOMMON35_raw_owned_records_independently_validated']and not p['source_PUBLIC_or_COMMON_candidate_collisions']and not p['other_selected_nativeDS_identifier_aliases']and not p['all_native_unit_extent_overlaps'],'actualDATA8parent collisionclosure')
 require(g['status']=='COMPLETE'and g['guard_closed']and g['actual_C5_calls']==1 and len(g['calls'])==1 and g['calls'][0]['terminal']and g['calls'][0]['reaped']and g['calls'][0]['returncode']==0 and g['source_sha256']==SOURCE_SHA and g['raw_whole_object_sha256']==OBJECT_SHA and len(g['blocked_probes'])==20 and not g['native_original_oldOBJ_comparison_inputs_inside_GEN'],'genuineoneC5sourceonlycontrol');require(t['session_id']==26647 and t['terminal_chunk']=='d5703f'and t['exit_code']==0 and t['terminal']and t['reaped']and t['whole_object_sha256']==OBJECT_SHA and t['future_strict_profile_fingerprint_eligible']and sem['raw_sha256']==OBJECT_SHA,'rootclosedactualproducereligible');require(sha(data['producer_source'])==SOURCE_SHA,'actualsourcecopy');validate_object(data['producer_object'])
 ref=build_reference(Path(target).read_bytes());require(ref['original_sha256']==ORIGINAL_SHA256,'originalidentity');image=ref['image'];near=p['all35_provider125near_rawdefinitions'];require(len(near)==125 and sum(r['size']for r in near)==4947 and len(p['far2_definitions_separate'])==2,'actual125rawnear/farseparate')
 for a in OFFSETS:require(0x52cc<=a<a+2<=0xcbe0 and 0x5cc20+a>=len(image)and all(not(a<r['end']and a+2>r['begin'])for r in near),'outsideFILE/insideCRTclear/disjoint125')
 crt=json.loads(data['crt_clear']);require(bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in bytes.fromhex(crt['normalized_result']['bytes_hex']),'nativeCRTclear')
 actual=[]
 for i,client in enumerate(p['complete3_client_TUs']):
  raw=data['client_'+str(i)];source=data['source_'+str(i)];require(sha(raw)==client['object_sha256']and sha(source)==client['source_sha256'],'actualDATA8client/sourceidentity');o=read_omf(raw);gs=cv_globals(o);ts=types(o);require({n:graph(ts,gs[n])for n in NAMES}==EXPECTED,'all6completeclientgraphs')
  for f in o.fixups:
   if f.target[0]==2 and o.externals.get(f.target[1])in NAMES:actual.append((client['slot'],{**dataclasses.asdict(f),'frame':list(f.frame),'target':list(f.target),'raw':f.raw.hex()}))
 expected=[(q['slot'],q['raw_field'])for q in p['all6_selected_native_CODE_fields']+p['all2_held_outline_operands']+p['all6_DEBUG_address_fields']];require(len(actual)==len(expected)==14 and sorted((slot,json.dumps(v,sort_keys=True))for slot,v in actual)==sorted((slot,json.dumps(v,sort_keys=True))for slot,v in expected),'all6selected+2held+6DEBUG fieldscomplete')
 for q in p['all6_selected_native_CODE_fields']+p['all2_held_outline_operands']:
  n=q['symbol'];at=q['native_image_field'];require(image[at:at+2]==OFFSETS[NAMES.index(n)].to_bytes(2,'little')and not any(s<at+2 and s+2>at for s in ref['relocations']),'nativeoperandword/noMZ');require(image[at-2:at+4].hex()==q['native_context_hex'],'retainednativecontext')
 require(all(q['whole_function_match']is False and q['Ccredit']==0 for q in p['all2_held_outline_operands']),'heldoutlinewholebodynevercredited')
 return[{'symbol':n,'dgroup_segment':'0x5cc2','dgroup_offset':hex(a),'end_exclusive':hex(a+2),'size':2,'resolved':False,'pointee_allocation_or_capacity_claim':False,'historical_unique_type_TU_storageclass_or_alias_proven':False}for n,a in zip(NAMES,OFFSETS)]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'fixedsourcehash');constraints=validate_evidence(project,item['evidence'],target)
 default=shutil.which('dosbox');path_before=os.environ.get('PATH');require(default is not None and Path(default).resolve()==Path('/usr/bin/dosbox')and sha(Path(default).read_bytes())=='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477','pinneddefaultDOSBox')
 with source_only_scope(source,project)as events:
  probes=[]
  for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',local(project,PINS['producer_object']['path']),local(project,PINS['ownership_DATA8']['path']),project/'config/units.json']:
   for api,fn in[('Path',lambda p:p.read_bytes()),('io',lambda p:__import__('io').open(p,'rb')),('builtin',lambda p:open(p,'rb')),('os',lambda p:os.open(p,os.O_RDONLY))]:
    try:fn(forbidden)
    except ValueError:probes.append({'API':api,'path':str(forbidden),'denied':True})
    else:raise ValueError('sourceguardinactive')
  require(len(events['blocked'])==20,'20activeGENdenials');c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
 require(os.environ.get('PATH')==path_before and shutil.which('dosbox')==default and sha(Path(default).read_bytes())=='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477','unchangeddefaultDOSBox/nooverride')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'wholefreshcompilerprovenance');defs=validate_object(c.object_bytes);out=Path(output);out.mkdir(parents=True,exist_ok=True);p=out/'square-coordinate-pointers-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(source_tool_scratch_guard=events,active_open_API_probes=probes,generation_comparison_input=False)
 return{'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible two nearpointercells, xrow9signedint/yint, no pointee allocation/capacity/historicalTU claim'}
