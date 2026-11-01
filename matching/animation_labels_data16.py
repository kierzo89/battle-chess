"""Exact source-only string pair:14C literal bytes +1authentic LINK hole.

Never constructs or zero-fills the15-byte image. Complete bytes come ONLY from
fresh real LINK output, MAP-bounded to the untouched whole DATA15 contribution.
The strict generic cdata reader is unchanged and must reject the raw hole.
"""
from pathlib import Path
from dataclasses import asdict
import hashlib,json,re,struct
from animation_labels15_pins import TOOLS,REA_SHA
from reference import ORIGINAL_SHA256,CARRIER_SHA256
from omf import read_omf,OMFError
BACKEND='msc500-link-initialized-animation-labels15-v1'
SOURCE='src/data/animation_labels.c';SOURCE_SHA='80abc33cf30f71e91f33ab80ba02607ba4bd19b75e118100c6990d836133f396';OBJECT_SHA='a7eb10f3b65425fb22367ba5c17f232a8b319fa515c22d6cb13a668fdcfd96ee';FLAGS=['/AS','/Zl']
NAMES=['_animation_black_label_4d96','_animation_white_label_4d9e'];REA='build/animation-command-data-recovery/rea-labels16.json'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
def need(v,m):
 if not v:raise OMFError('animation labels15: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def validate_unit(unit):
 need(unit['id']=='animation_label_pair_4d96'and unit['language']=='c-data'and unit['backend']==BACKEND and unit['source']==SOURCE and unit['symbol']==NAMES[0]and unit['flags']==FLAGS and unit['size']==15 and int(unit['image_offset'],0)==0x619b6 and unit['reference_region']=='exepack-expanded'and unit['rea_evidence']==REA,'exact unit identity')
 need(not unit.get('externals')and not unit.get('extended_extent')and not unit.get('owned_data')and not unit.get('owned_const')and not unit.get('owned_selector_const')and not unit.get('owned_code_address_consts'),'no borrowed CODE/ownership/placement policy')
def validate_raw(raw):
 need(isinstance(raw,bytes),'whole raw bytes');o=read_omf(raw);need(not o.fixups and not o.procedures,'no fixups/procedures')
 need([(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[(1,'_TEXT','CODE',0,72),(2,'_DATA','DATA',15,72),(3,'CONST','CONST',0,72),(4,'_BSS','BSS',0,72)],'exact4segments/DATA15/WORD')
 need(o.externals=={1:'__acrtused'},'exact unused startup-selection marker')
 need({n:(p.segment,p.offset,p.group,p.type_index)for n,p in o.publics.items()}=={NAMES[0]:(2,0,1,0),NAMES[1]:(2,8,1,0)},'exact2PUBLICs')
 need(o.segments[2].chunks==[(0,b'Black:\0'),(8,b'White:\0')]and not any(s.unsupported_data for s in o.segments.values()),'literal14 writes and ONLY natural hole7')
 for k,at,p in o.records:
  need(k in{0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0x90,0xa0,0x8a},'unsupported record')
  if k==0x9a:need(p==bytes.fromhex('02ff03ff04ff02'),'exact DGROUP')
  if k==0x8a:need(p==b'\0','no source entry')
 need(sha(raw)==OBJECT_SHA,'untouched whole genuine OMF hardpin')
 return{'boundary':'complete_raw_DATA15_one_natural_WORD_hole','segment':{'index':2,'name':'_DATA','class_name':'DATA','length':15,'attributes':72},'publics':{n:asdict(p)for n,p in o.publics.items()},'literal_writes':[{'offset':a,'length':len(b),'sha256':sha(b)}for a,b in o.segments[2].chunks],'source_literal_bytes':14,'raw_uninitialized_alignment':{'offset':7,'length':1},'raw_fixups':0,'unused_startup_marker':'__acrtused','raw_OMF_unchanged':True,'authored_c_function_count':0}
def validate_evidence(unit,project,target_sha256,reference):
 validate_unit(unit);p=Path(project)/REA;need(sha(p.read_bytes())==REA_SHA,'exact retained raw primary pin');e=json.loads(p.read_text());n=e['normalized_result'];q=e['analysis_profile']['parameters'];need(target_sha256==reference['original_sha256']==ORIGINAL_SHA256 and e['subject']['digest']['sha256']==reference['carrier_sha256']==CARRIER_SHA256 and q['load_segment']=='0x1000'and q['language_id']=='x86:LE:16:Real Mode'and q['target_format']=='dos-mz'and e['operation']=='read_bytes'and e['parameters']=={'address':'0x719b6','length':16}and n['complete']and n['requested_bytes']==n['returned_bytes']==16,'retained full16 primary')
 need(bytes.fromhex(n['bytes_hex'])==reference['image'][0x619b6:0x619c6],'full observed16 comparison identity');return e['evidence_id']
def validate_link_component(raw,exe,map_text,log_text,link_status):
 proof=validate_raw(raw);need(isinstance(exe,bytes)and len(exe)>=28,'real LINK complete MZ required');w=struct.unpack_from('<14H',exe);need(w[0]==0x5a4d and w[2]>0 and w[1]<512 and w[3]==0 and w[4]>=2 and w[13]==0,'plain relocation-free MZ')
 declared=(w[2]-1)*512+(w[1]or 512);header=w[4]*16;need(declared==len(exe)and header<=declared,'MZ file extent');image=exe[header:declared]
 segments=[]
 for start,stop,size,name,klass in re.findall(r'^\s*([0-9A-Fa-f]+)H\s+([0-9A-Fa-f]+)H\s+([0-9A-Fa-f]+)H\s+(\S+)\s+(\S+)\s*$',map_text,re.M):segments.append((int(start,16),int(stop,16),int(size,16),name,klass))
 need(segments==[(0,15,16,'_TEXT','CODE'),(16,30,15,'_DATA','DATA'),(32,32,0,'CONST','CONST'),(32,32,0,'_BSS','BSS')],'exact actual sole-OBJ LINK segment table including LINK zero prefix')
 need(len(image)==31 and image[:16]==bytes(16),'exact actual LINK zero prefix; no source CODE or prefix byte credit')
 start,stop=16,30
 publics={}
 for seg,off,name in re.findall(r'^\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+(?:Abs\s+)?(\S+)\s*$',map_text,re.M):
  pair=(int(seg,16),int(off,16));need(name not in publics or publics[name]==pair,'conflicting MAP public');publics[name]=pair
 need(set(publics)==set(NAMES)|{'_edata','_end'}and publics['_edata']==(1,16)and publics['_end']==(0,0)and publics[NAMES[0]][0]*16+publics[NAMES[0]][1]==start and publics[NAMES[1]][0]*16+publics[NAMES[1]][1]==start+8,'actual public endpoints0/8')
 actual=image[start:stop+1];need(len(actual)==15 and actual[:7]==b'Black:\0'and actual[8:]==b'White:\0'and actual[7]==0,'actual LINK bytes/literal14/hole1')
 need('Version 3.65'in log_text,'pinned authentic LINK version');errors=re.findall(r'(?im)^LINK : error (L\d+):',log_text);undefined=sorted(set(re.findall(r'(?im)^\s*([^\s:]+)\s+in file\(s\):',log_text)))
 need((errors==[]and undefined==[]and link_status=='success')or(errors==['L2029']and undefined==['__acrtused']and link_status=='link_failed'),'only explicit unused-marker diagnostic or success')
 warnings=re.findall(r'(?im)^LINK : warning (L\d+):\s*(.*)$',log_text)
 for code,text in warnings:need((code,text.strip().lower())in{('L4021','no stack segment'),('L4038','program has no starting address')},'unqualified LINK warning '+code)
 proof.update(LINK_zero_prefix_bytes=16,LINK_zero_prefix_credit=0,LINK_generated_publics=['_edata','_end'],boundary='authentic_LINK_initialized_whole_DATA15',source_literal_bytes=14,LINK_initialized_alignment_bytes=1,LINK_hole={'offset':7,'actual_value':actual[7]},actual_MAP_start=start,actual_MAP_stop=stop,actual_publics=publics,actual_LINK_status=link_status,marker_only_diagnostic=bool(errors),LINK_warnings=warnings,emitted_mz_sites=[],outside16th_byte_credit=0,historical_original_TU_or_placement_proven=False,synthetic_fill_or_serializer_used=False)
 return actual,proof

def validate_compiled(compiled,source_bytes,unit,*,project,output,link_emitter):
 validate_unit(unit);need(sha(source_bytes)==compiled.source_sha256==SOURCE_SHA and compiled.compiler=='msc500'and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'and compiled.toolchain_manifest_sha256==MANIFEST_SHA and compiled.tool_hashes==TOOLS,'exact actual source/compiler provenance');raw=compiled.object_bytes;validate_raw(raw)
 # link_emitter must be the separately root-reviewed fresh one-OBJ implementation.
 # No old positive object or reference is supplied to it.
 artifacts=link_emitter(raw,Path(project),Path(output));need(artifacts['input_object_sha256']==sha(raw)and artifacts['source_objects']==1 and artifacts['libraries']==[]and artifacts['partial_EXE_executed']is False,'fresh source-only soleOBJ LINK receipt')
 actual,proof=validate_link_component(raw,artifacts['exe_bytes'],artifacts['map_text'],artifacts['log_text'],artifacts['link_status']);need(sha(raw)==OBJECT_SHA,'raw OBJ never changed');proof['generation']=artifacts['receipt'];proof['relocations']=[];return actual,proof
