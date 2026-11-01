"""Opt-in signed16 cursor Actor index COMMON2; zero initialized/function credit."""
from pathlib import Path
import dataclasses,hashlib,json,tempfile,re
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
from link16 import link_function
from cursor_actor_index_profile_pins import PINS,TOOLS,MANIFEST_SHA,SOURCE_SHA,OBJECT_SHA,RECORD_PINS,FIELD_PROFILE
from cursor_actor_index_generation_scope import scope
BACKEND='msc500-near-common-cursor-actor-index-v1';SOURCE='src/link/cursor_actor_index.c';DOSBOX_SHA='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477';NAMES=['_cursor_actor_57d0'];FLAGS=['/AS','/Zl','/Zi']
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'cursor-actor relative path');root=Path(project).resolve();p=(root/name).resolve();require(p.is_relative_to(root),'cursor-actor path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'cursor-actor exact registry keys')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('cursor-actor-index-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'cursor-actor exact source/compiler profile')
 require(item['objects']==[{'symbol':'_cursor_actor_57d0','size':2,'storage':'near-common'}]and type(item['objects'][0]['size'])is int,'cursor-actor exact signed WORD storage');require(item['evidence']==PINS,'cursor-actor exact owned evidence selection')
def debug(o):
 s=o.segments[5];v=bytearray(s.length);seen=set()
 for at,b in s.chunks:require(0<=at<=at+len(b)<=s.length,'cursor-actor debug bounds');v[at:at+len(b)]=b;seen.update(range(at,at+len(b)))
 require(len(seen)==s.length,'cursor-actor whole debug coverage');return bytes(v)
def validate_object(raw):
 require(type(raw)is bytes,'cursor-actor whole raw object');o=read_omf(raw)
 require(not o.publics and not o.procedures,'cursor-actor no PUBLIC/procedure/alias')
 require([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',0,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72),(5,'$$SYMBOLS','DEBSYM',26,32),(6,'$$TYPES','DEBTYP',0,32)],'cursor-actor empty loaded segments/exact scalar debug')
 require(all(s==5 for _,s,_,_ in o.data_writes),'cursor-actor no loaded bytes/type arrays')
 defs=[]
 for k,at,p in o.records:
  require(k in[0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a],'cursor-actor unknown/foreign OMF record')
  if k==0xb0:
   c=_Cursor(p)
   while c:
    name,typ,kind,size=c.name(),c.index(),c.byte(),c.byte();require((name,typ,kind,size)==('_cursor_actor_57d0',0x81,0x62,2),'cursor-actor signed81 nearCOMDEF62 size2 only');defs.append({'symbol':name,'type_index':typ,'datatype':kind,'size':size})
 require(defs==[{'symbol':'_cursor_actor_57d0','type_index':0x81,'datatype':0x62,'size':2}],'cursor-actor exact single scalar definition')
 require(o.externals=={1:'__acrtused',2:'_cursor_actor_57d0'},'cursor-actor genuine scalar/debug external binding')
 require(debug(o)==bytes.fromhex('190500000000810011637572736f725f6163746f725f35376430'),'cursor-actor scalar signed81 global CV')
 fields=[[f.segment,f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.raw.hex(),f.record_offset]for f in o.fixups];require(fields==FIELD_PROFILE and len(fields)==1,'cursor-actor only exact debug FAR binding')
 require([(k,at,sha(p))for k,at,p in o.records]==RECORD_PINS,'cursor-actor every raw record accounted');require(sha(raw)==OBJECT_SHA,'cursor-actor exact genuine whole object');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'cursor exact evidence selection');p={}
 for name,row in PINS.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'cursor owned pin '+name);p[name]=raw
 proof=json.loads(p['ownership']);g=json.loads(p['actual_generation']);positive=json.loads(p['actual_comparison']);tool=json.loads(p['actual_tool'])
 require(proof['status'].startswith('SUPPORTED compatible signed-int16')and proof['compatible_declaration']=='int cursor_actor_57d0;'and proof['native_DS_interval']==[0x57d0,0x57d2],'cursor logical index scalar evidence')
 require(proof['current_objects_scanned']==244 and len(proof['clients'])==3 and len(proof['all_actual_fields'])==7 and proof['registry_symbol_coherence'].keys()=={'_cursor_actor_57d0'}and proof['existing_PUBLIC_COMMON_collisions']==[],'cursor all client/name/old provider inventory')
 require(g['status']=='COMPLETE'and g['actual_C5_calls']==1 and g['source_config_pinnedtools_freshscratch_only']and g['source_sha256']==SOURCE_SHA and g['raw_object_sha256']==OBJECT_SHA and g['terminal']and g['child_reaped']and len(g['guard']['blocked'])==5,'cursor actual source-only C5 receipt')
 require(tool['exit_code']==0 and tool['terminal']and tool['reaped']and tool['actual_C5_calls']==1 and positive['raw_object_sha256']==OBJECT_SHA and positive['status'].startswith('PASS actual genuine signed81'),'cursor actual terminal/scalar comparison');validate_object(p['producer_object'])
 ref=build_reference(Path(target).read_bytes());require(ref['original_sha256']==ORIGINAL_SHA256 and len(ref['image'])==0x61eeb and 0x5cc20+0x57d0==0x623f0>len(ref['image']),'cursor outside decodedFILE, no initialized credit')
 crt=json.loads(p['crt_native']);rawcrt=bytes.fromhex(crt['normalized_result']['bytes_hex']);require(rawcrt==ref['image'][0xea86:0xeb39]and bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')in rawcrt and 0x52cc<=0x57d0<0x57d2<=0xcbe0,'cursor real CRT clear bounds')
 require(ref['image'][0x5cc20+0x5c4:0x5cc20+0x5c4+2]==bytes.fromhex('d257')and proof['following_SearchFrame_storage']['begins']==0x57d2 and proof['following_SearchFrame_storage']['pointer_variable_DS_offset']==0x5c4 and proof['following_SearchFrame_storage']['capacity_overlay_bounds_all_prior_holds_preserved'],'cursor distinct from SearchFrame storage/pointer; no new bounds')
 rows=proof['current_32provider_near119_disjoint'];require(len(rows)==119 and all(not(r['start']<0x57d2 and r['start']+r['bytes']>0x57d0)for r in rows)and proof['far_definitions_separate']==2,'cursor old32 near/far separation and no overlap')
 codecount=0;debugcount=0;typed=0
 for client in proof['clients']:
  slot=str(client['slot']);o=read_omf(p['client_'+slot]);src=p['source_'+slot];require(sha(p['client_'+slot])==client['object_sha256']and sha(src)==client['source_sha256'],'cursor whole raw client/source')
  actual=[f for f in o.fixups if f.target[0]==2 and o.externals.get(f.target[1])=='_cursor_actor_57d0'];expected=[r for r in proof['all_actual_fields']if r['slot']==client['slot']];require(len(actual)==len(expected),'cursor every actual client field')
  for f,r in zip(actual,expected):
   model=dataclasses.asdict(f);model.update(raw=f.raw.hex(),frame=list(f.frame),target=list(f.target));require(model==r['field'],'cursor exact raw field/frame/target/boundary')
   if r['kind']=='CODE':
    codecount+=1;require(f.width==2 and f.location_type==1 and f.segment_relative and f.frame in[(5,None),(1,1)]and not f.displacement,'cursor native WORD operand mode');v=bytearray(o.segments[f.segment].length)
    for at,b in o.segments[f.segment].chunks:v[at:at+len(b)]=b
    require(v[f.offset-2:f.offset]==bytes.fromhex('f72e')and v[f.offset:f.offset+2]==b'\0\0','cursor raw signed IMUL/zero symbol addend')
    at=r['native_field'];require(ref['image'][at-2:at+2]==bytes.fromhex('f72ed057')and at not in ref['relocations'],'cursor real native IMUL indexDS57D0/no MZ')
   else:debugcount+=1;require(o.segments[f.segment].class_name=='DEBSYM'and f.width==4,'cursor DEBUG FAR address only')
  if client['debug_globals']:
   typed+=1;data=debug(o);at=0;hits=[]
   while at<len(data):
    n=data[at];v=data[at+1:at+1+n];require(n>0 and len(v)==n,'cursor whole client CV')
    if v[0]==5 and v[8:]==b'cursor_actor_57d0':hits.append((at,v.hex(),int.from_bytes(v[5:7],'little')))
    at+=n+1
   require(len(hits)==1 and hits[0][2]==0x81 and hits[0][1]==client['debug_globals'][0]['raw'],'cursor actual signed16 scalar CV, not pointer')
   text=src.decode('ascii');text=re.sub(r'/\*.*?\*/|//[^\n]*',' ',text,flags=re.S);decls=[m.group(0)for m in re.finditer(r'\bextern\s+int\s+[^;{}]+;',text)if re.search(r'\bcursor_actor_57d0\b',m.group(0))];require(len(decls)==1 and re.search(r'(?:int\s+|,)\s*cursor_actor_57d0\s*(?:,|;)',decls[0]),'cursor genuine scalar extern source declaration')
  else:require(b'_cursor_actor_57d0:WORD'in src,'cursor helper WORD view, scalar type from C clients')
 require((codecount,debugcount,typed)==(5,2,2),'cursor complete5 CODE+2 DEBUG/two signedCV clients')
 editor=json.loads(p['editor_native']);a=editor['normalized_result']['assembly'];a='\n'.join(a)if isinstance(a,list)else a;require(all(x in a for x in['0x10b17: MOV AL, byte ptr [BX + 0x8aa4]','0x10b1b: SUB AH, AH','0x10b1d: MOV [0x57d0], AX','0x10bf7: MOV [0x57d0], AX','0x10ac6: MOV AL, [0x57d0]']),'cursor actual native index writes and byte-map transfer')
 return [{'symbol':'_cursor_actor_57d0','dgroup_segment':'0x5cc2','dgroup_offset':'0x57d0','end_exclusive':'0x57d2','size':2,'resolved':False,'compatible_logical_type':'signed16 cursor Actor index scalar','initialized_byte_credit':0,'actor_capacity_or_SearchFrame_alias_claim':False,'historical_storageclass_TU_MAP_proven':False}]
def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'cursor-actor exact source')
 # Prewarm tempfile runtime before the generation open guard. No target/proof read.
 tempfile.gettempdir()
 with scope(source,project)as events:
  for forbidden in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/PINS['producer_object']['path'],project/PINS['ownership']['path'],project/'config/units.json']:
   try:forbidden.read_bytes()
   except ValueError:pass
   else:raise ValueError('cursor-actor source-only guard inactive')
  require(sha(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA,'cursor-actor pinned DOSBox')
  c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500',dosbox='/usr/bin/dosbox');require(len(events['blocked'])==5,'cursor-actor exact5 generation denials')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.toolchain_manifest_sha256==MANIFEST_SHA and c.tool_hashes==TOOLS,'cursor-actor fresh compiler provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);out=Path(output);out.mkdir(parents=True,exist_ok=True);path=out/'cursor-actor-index-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes');meta.update(source_tool_scratch_guard=events,generation_comparison_input=False)
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':2,'initialized_bytes':0,'matching_credit':0,'authored_C_function_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'compatible_signed16_cursor_Actor_index_no_capacity_or_pointer_alias'}
