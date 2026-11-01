"""Opt-in signed16 move-list length COMMON2; zero initialized/function credit."""
from pathlib import Path
import dataclasses,hashlib,json,tempfile
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from link16 import link_function
from move_count_profile_pins import PINS,TOOLS,MANIFEST_SHA,SOURCE_SHA,OBJECT_SHA,RECORD_PINS,FIELD_PROFILE
from move_count_generation_scope import scope
BACKEND='msc500-near-common-move-count845e-v1';SOURCE='src/link/move_count.c';DOSBOX_SHA='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477';NAMES=['_move_count'];FLAGS=['/AS','/Zl','/Zi']
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'move-count relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'move-count path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'move-count exact registry keys')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('move-count-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'move-count exact source/compiler profile')
 require(item['objects']==[{'symbol':'_move_count','size':2,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'move-count exact signed WORD storage');require(item['evidence']==PINS,'move-count exact owned evidence selection')
def debug(o):
 s=o.segments[5];v=bytearray(s.length);seen=set()
 for at,b in s.chunks:require(0<=at<=at+len(b)<=s.length,'move-count debug bounds');v[at:at+len(b)]=b;seen.update(range(at,at+len(b)))
 require(len(seen)==s.length,'move-count whole debug coverage');return bytes(v)
def validate_object(raw):
 require(type(raw)is bytes,'move-count whole raw object');o=read_omf(raw)
 require(not o.publics and not o.procedures,'move-count no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',19,32),(6,'$$TYPES','DEBTYP',0,32)],'move-count empty loaded segments/exact scalar debug')
 require(all(s==5 for _,s,_,_ in o.data_writes),'move-count no loaded bytes/type arrays')
 defs=[]
 for k,at,p in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'move-count unknown/foreign OMF record')
  if k==0xb0:
   c=_Cursor(p)
   while c:
    name,typ,kind,size=c.name(),c.index(),c.byte(),c.byte();require((name,typ,kind,size)==('_move_count',0x81,0x62,2),'move-count signed81 nearCOMDEF62 size2 only');defs.append({'symbol':name,'type_index':typ,'datatype':kind,'size':size})
 require(defs==[{'symbol':'_move_count','type_index':0x81,'datatype':0x62,'size':2}],'move-count exact single scalar definition')
 require(o.externals=={1:'__acrtused',2:'_move_count'},'move-count genuine scalar/debug external binding')
 require(debug(o)==bytes.fromhex('12050000000081000a6d6f76655f636f756e74'),'move-count scalar signed81 global CV')
 fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups];require(fields==FIELD_PROFILE and len(fields)==1,'move-count only exact debug FAR binding')
 require([(k,at,sha(p))for k,at,p in o.records]==RECORD_PINS,'move-count every raw record accounted');require(sha(raw)==OBJECT_SHA,'move-count exact genuine whole object');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'move-count exact evidence');p={}
 for name,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'move-count owned pin '+name);p[name]=raw
 review=json.loads(p['native_review']);ren=json.loads(p['rename_comparison']);provider=json.loads(p['provider_comparison']);address=json.loads(p['address_semantics'])
 require(review['status'].startswith('PASS compatible shared signed-int16')and review['native_DS_word']==[0x845e,0x8460],'move-count compatible logical counter proof')
 require(review['objects']['search']['selected_units']==19 and review['objects']['move']['selected_units']==12 and len(review['all_actual_counter_CODE_fields'])==5,'move-count both whole native clients')
 require(all(v['type']==0x81 and v['logical_type']=='signed int16'for v in review['CV_views'])and len(review['CV_views'])==2,'move-count two genuine signed81 views')
 require(ren['status']=='PASS strict whole-source alpha rename only'and ren['whole_CODE_bytes_unchanged']==5350 and ren['actual_fields']==604 and ren['selected_bodies_preserved']==19 and ren['held_search_window_differences_preserved']==3 and len(ren['four_load_bases'])==4,'move-count complete rename-only control')
 require(provider['status'].startswith('PASS genuine signed-int16')and provider['whole_object_sha256']==OBJECT_SHA and provider['source_sha256']==SOURCE_SHA,'move-count genuine provider control');validate_object(p['provider_object'])
 for kind in['provider','rename']:
  g=json.loads(p[kind+'_generation']);t=json.loads(p[kind+'_tool']);require(g['status']=='COMPLETE'and g['actual_C5_calls']==1 and g['source_tool_freshscratch_only']and len(g['guard']['blocked'])==5 and t['exit_code']==0 and t['terminal']and t['reaped']and t['actual_C5_calls']==1,'move-count genuine source-only finite control')
 require(all(not(r['start']<0x8460 and r['start']+r['bytes']>0x845e)for r in review['current_30providers_disjoint'])and len(review['current_30providers_disjoint'])==114,'move-count old30/114near disjoint; append still duplicate-checked by dispatcher')
 ref=build_reference(Path(target).read_bytes());require(ref['original_sha256']==ORIGINAL_SHA256 and len(ref['image'])==0x61eeb and address['counter_physical']==0x6507e and address['counter_beyond_decoded_FILE']and 0x52cc<=0x845e<0x8460<=0xcbe0,'move-count beyond decodedFILE and actual CRT clear')
 crt=json.loads(p['crt_native']);code=bytes.fromhex(crt['normalized_result']['bytes_hex']);require(code==ref['image'][0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in code,'move-count actual CRT clear bytes')
 for key in['advance_native','append_native','reset_native']:require(json.loads(p[key])['subject']['digest']['sha256']==ORIGINAL_SHA256,'move-count original native procedure identity')
 old=read_omf(p['search_old']);new=read_omf(p['search_new']);move=read_omf(p['move_client']);
 for client,name in[(old,b'state_count'),(new,b'move_count'),(move,b'move_count')]:
  data=debug(client);at=0;hits=[]
  while at<len(data):
   n=data[at];v=data[at+1:at+1+n];require(len(v)==n and n>0,'move-count whole client CV symbol')
   if v[0]==5 and len(v)>=8 and v[8:]==name:hits.append(int.from_bytes(v[5:7],'little'))
   at+=n+1
  require(at==len(data)and hits==[0x81],'move-count actual whole client signed81 scalar CV')
 require(old.publics==new.publics and old.names==new.names and {i:('_move_count'if n=='_state_count'else n)for i,n in old.externals.items()}==new.externals,'move-count actual unchanged PUBLICs/identifier identity')
 require(old.segments[1].chunks==new.segments[1].chunks and old.segments[6].chunks==new.segments[6].chunks and sha(p['search_new'])==ren['new_object_sha256'],'move-count whole CODE/DEBTYP exact');require(sha(p['search_source'])==ren['new_source_sha256'],'move-count new complete source pin')
 us=json.loads(p['search_units']);ext=dict(us[0]['externals']);ext['_move_count']=ext.pop('_state_count');base=review['objects']['search']['native_origin'];selected={u['symbol']for u in us};require(len(selected)==19,'move-count complete selected search set')
 for symbol,pub in new.publics.items():
  info=new.function_info(symbol);out,logs=link_function(new,symbol,base+info['offset'],ext,image_origin=base+info['offset']);diff=[{'relative':i,'image':base+info['offset']+i,'source':a,'native':b}for i,(a,b)in enumerate(zip(out,ref['image'][base+info['offset']:base+info['end']]))if a!=b];expected=next(x for x in review['all_whole_procedures']if x['owner']=='search'and x['symbol']==symbol);require(diff==expected['differences'],'move-count whole selected/native and held differences');require(not diff if symbol in selected else len(diff)==3,'move-count19 selected exact/held3 retained')
  emitted=[f['mz_segment_relocation_image_offset']for f in logs if'mz_segment_relocation_image_offset'in f];actual=[s for s in ref['relocations']if base+info['offset']<=s<base+info['end']];require(sorted(emitted)==sorted(actual),'move-count whole source native MZ inventory')
  for load in[0,1,4096,65535]:
   loaded=bytearray(out);expected_native=bytearray(ref['image'][base+info['offset']:base+info['end']])
   for site in emitted:
    at=site-base-info['offset']
    for v in[loaded,expected_native]:v[at:at+2]=((int.from_bytes(v[at:at+2],'little')+load)&65535).to_bytes(2,'little')
   require([i for i,(a,b)in enumerate(zip(loaded,expected_native))if a!=b]==[x['relative']for x in diff],'move-count all selected/held semantics at four load bases')
 for row in review['all_actual_counter_CODE_fields']:
  owner=row['owner'];o=old if owner=='search'else move;f=row['field'];hits=[x for x in o.fixups if x.segment==f['segment']and x.offset==f['object_offset']];require(len(hits)==1,'move-count actual native WORD field');x=hits[0];require(x.width==2 and x.location_type==1 and x.segment_relative and x.frame==(5,None)and x.raw.hex()==f['raw_fixupp']and o.externals[x.target[1]]==row['name'],'move-count typed genuine native counter operand');v=bytearray(o.segments[x.segment].length)
  for at,b in o.segments[x.segment].chunks:v[at:at+len(b)]=b
  value=(0x845e+int.from_bytes(v[x.offset:x.offset+2],'little')+(x.displacement or 0))&65535;require(value.to_bytes(2,'little')==ref['image'][f['image_offset']:f['image_offset']+2]==bytes.fromhex(f['encoded_hex']),'move-count native845E operand exact')
 return [{'symbol':'_move_count','dgroup_segment':'0x5cc2','dgroup_offset':'0x845e','end_exclusive':'0x8460','size':2,'resolved':False,'compatible_logical_type':'signed int16 scalar','initialized_byte_credit':0,'historical_storageclass_TU_MAP_proven':False}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'move-count exact source')
 # Prewarm tempfile runtime before the generation open guard. No target/proof read.
 tempfile.gettempdir()
 with scope(source,project)as events:
  for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/PINS['provider_object']['path'],project/PINS['native_review']['path'],project/'config/units.json']:
   try:forbidden.read_bytes()
   except ValueError:pass
   else:raise ValueError('move-count source-only guard inactive')
  require(sha(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA,'move-count pinned DOSBox')
  c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500',dosbox='/usr/bin/dosbox');require(len(events['blocked'])==5,'move-count exact5 generation denials')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'move-count fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'move-count-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(source_tool_scratch_guard=events,generation_comparison_input=False)
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':2,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_signed16_move_list_length_no_historical_storage_MAP_claim'}
