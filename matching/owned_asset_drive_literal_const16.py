"""Closed source CODE1036/consumed literal CONST158 ownership. No generation."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from omf import OMFError,OMFObject
from link16 import link_function
from reference import validate_data_address,validate_expanded_read
import asset_drive_literal158_pins as pins
PROFILE='asset_drive_messages_1036_158_v2'
SOURCE='src/asset_dispatch_drive_literals_match.c'
OWNERS={'_load_asset_index','_select_asset_file','_seek_asset'}
class AssetDriveLiteralError(OMFError):pass
def require(ok,message):
 if not ok:raise AssetDriveLiteralError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):
 def view(x):
  if isinstance(x,dict):
   require(all(type(k)in (str,int)for k in x)and len({str(k)for k in x})==len(x),'Asset snapshot key identity')
   return {str(k):view(y)for k,y in x.items()}
  if isinstance(x,(list,tuple)):return [view(y)for y in x]
  return x
 return json.dumps(view(v),sort_keys=True,separators=(',',':'))
def snapshot(o):
 return {'records':[{'kind':k,'offset':at,'payload_hex':b.hex()}for k,at,b in o.records],'names':o.names,'externals':o.externals,'publics':{n:asdict(p)for n,p in o.publics.items()},'procedures':o.procedures,'data_writes':o.data_writes,'segments':{i:{**{k:v for k,v in asdict(s).items()if k!='chunks'},'chunks':[{'offset':at,'bytes_hex':b.hex()}for at,b in s.chunks]}for i,s in o.segments.items()},'fixups':[{**asdict(f),'raw':f.raw.hex()}for f in o.fixups]}
def profile():
 raw=Path(__file__).with_name('asset_drive_literal158_profile.json').read_bytes();require(sha(raw)==pins.PROFILE_SHA256,'Asset158 fixed profile hash');return json.loads(raw)
def full_bytes(s,debug=False):
 require(not s.unsupported_data,'Asset158 opaque/iterated allocation');b=bytearray(s.length);seen=bytearray(s.length);cursor=0
 for at,body in (s.chunks if debug else sorted(s.chunks)):
  require(type(at)is int and 0<=at<=at+len(body)<=s.length and bool(body),'Asset158 write bounds')
  if not debug:require(at==cursor,'Asset158 allocation hole/overlap');cursor+=len(body)
  b[at:at+len(body)]=body;seen[at:at+len(body)]=b'\1'*len(body)
 require(all(seen),'Asset158 complete allocation');return bytes(b)
def validate_shared_object(obj):
 require(isinstance(obj,OMFObject),'Asset158 genuine OMF required');p=profile();require(canonical(snapshot(obj))==canonical(p['object_snapshot']),'Asset158 complete raw record and parsed congruence')
 require(len(obj.fixups)==121 and sum(f.segment==1 for f in obj.fixups)==89 and sum(f.segment==5 for f in obj.fixups)==32,'Asset158 exact89CODE/32DEBUG')
 require(set(obj.publics)==set(obj.procedures)==set(p['procedures'])and len(obj.publics)==9,'Asset158 nine PUBLIC/CVs')
 cursor=0
 for name,(at,size)in p['procedures'].items():
  i=obj.function_info(name);pub=obj.publics[name];require(at==cursor and(pub.group,pub.segment,pub.offset)==(0,1,at)and(i['segment'],i['offset'],i['size'],i['boundary'])==(1,at,size,'codeview3_procedure'),'Asset158 complete natural CV boundaries');cursor+=size
 require(cursor==1036,'Asset158 completeCODE1036');code=full_bytes(obj.segments[1]);data=full_bytes(obj.segments[3]);require(len(data)==158 and obj.segments[3].chunks==[(0,data)],'Asset158 exact natural onechunk158')
 for i in [2,4]:require(full_bytes(obj.segments[i])==b'','Asset158 no DATA/BSS storage')
 full_bytes(obj.segments[5],True);types=full_bytes(obj.segments[6],True);at=0
 while at<len(types):
  require(at+3<=len(types)and types[at]==1,'Asset158 complete CV type header');n=int.from_bytes(types[at+1:at+3],'little');require(n>0 and at+3+n<=len(types),'Asset158 complete CV type record');at+=3+n
 refs=[f for f in obj.fixups if f.target==(0,3)]
 require(sorted((f.offset,int.from_bytes(code[f.offset:f.offset+2],'little'))for f in refs)==[tuple(x)for x in p['CONST_references']]and len(refs)==9,'Asset158 all nine consumed references')
 require(all((f.segment,f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(1,2,1,True,(1,1),None)for f in refs),'Asset158 exact ownCONST frames')
 require(not any(f.segment==3 for f in obj.fixups)and not any(x.segment==3 for x in obj.publics.values()),'Asset158 anonymous pure literals no DATA fixups/PUBLICs')
 return p
def validate_unit_metadata(unit):
 require(isinstance(unit,dict)and unit.get('owned_const_profile')==PROFILE,'Asset158 exact new ownership kind');p=profile();require(unit.get('symbol')in OWNERS,'Asset158 actual consuming owner only');expected=next(u for u in p['units']if u['symbol']==unit['symbol'])
 for key in ['id','language','backend','source','symbol','size','image_offset','flags','externals','owned_const','owned_const_profile']:require(canonical(unit.get(key))==canonical(expected.get(key)),'Asset158 exact owner metadata '+key)
 require(not any(unit.get(k)is not None for k in ['code_address','extended_extent','owned_data','owned_bss','owned_selector_const','object_profile']),'Asset158 exclusive ordinary C ownership')
 return dict(p['descriptor'])
def validate_layout(unit,obj):
 desc=validate_unit_metadata(unit);p=validate_shared_object(obj);data=full_bytes(obj.segments[3]);return desc,data,[tuple(x)for x in p['CONST_references']]
def validate(unit,obj,project,reference):
 desc,data,refs=validate_layout(unit,obj);p=profile();project=Path(project).resolve();source=(project/SOURCE).resolve();require(source.is_relative_to(project)and sha(source.read_bytes())==pins.SOURCE_SHA256,'Asset158 source hash')
 evidence={}
 for key,row in pins.EVIDENCE.items():
  path=(project/row['path']).resolve();require(not Path(row['path']).is_absolute()and path.is_relative_to(project),'Asset158 proof path');raw=path.read_bytes();require(sha(raw)==row['sha256'],'Asset158 proof hash');evidence[key]=json.loads(raw)
 g=evidence['generation'];t=evidence['terminal'];require(g['status']=='COMPLETE'and g['guard_closed']is True and g['actual_C5_calls']==1 and len(g['calls'])==1 and all(c['terminal']and c['reaped']and c['returncode']==0 for c in g['calls'])and len(g['blocked_probes'])==20 and g['source_tools_new_scratch_only']is True and g['native_original_oldOBJ_comparison_inputs_inside_GEN']is False and g['source_sha256']==pins.SOURCE_SHA256 and g['raw_whole_object_sha256']==pins.OBJECT_SHA256 and g['compiler']=='msc500'and g['flags']==['/AS','/Os','/Zi']and g['source_name']=='UNIT.C','Asset158 genuine single C5 source closure')
 require(t['exit_code']==0 and t['actual_C5_calls']==1 and t['terminal']is True and t['reaped']is True,'Asset158 root observed terminal closure')
 require(evidence['comparison']['source_sha256']==pins.SOURCE_SHA256 and evidence['comparison']['object_sha256']==pins.OBJECT_SHA256 and evidence['comparison']['all_raw_fields']==121,'Asset158 prior actual comparison closure')
 frame,offset=validate_data_address(dict(desc,reference_region='exepack-expanded'),reference);eid=validate_expanded_read(evidence['pool'],dict(desc,reference_region='exepack-expanded'),data,reference)
 code=bytearray();fields=[];scopes=[]
 for row in p['units']:
  b,logs=link_function(obj,row['symbol'],int(row['image_offset'],0),row['externals'],**({'owned_const':desc}if row.get('owned_const')else{}));info=obj.function_info(row['symbol']);require(len(code)==info['offset']and len(b)==info['size'],'Asset158 full linked procedure partition');code.extend(b);fields.extend(logs);require(sha(b)==p['function_hashes'][row['symbol']],'Asset158 whole native procedure hash');scopes.append({'symbol':row['symbol'],'size':len(b),'fields':len(logs),'sha256':sha(b)})
 native=reference['image'][0xc83a:0xcc46];require(len(code)==1036 and bytes(code)==native,'Asset158 all nine native procedures exact')
 require([(f['object_offset'],f['width'],f['record_offset'],f['raw_fixupp'])for f in fields]==[(f['offset'],f['width'],f['record_offset'],f['raw'])for f in sorted((f for f in p['object_snapshot']['fixups']if f['segment']==1),key=lambda f:(f['offset'],f['record_offset']))],'Asset158 all89 actual field logs')
 sites=sorted(f['mz_segment_relocation_image_offset']for f in fields if'mz_segment_relocation_image_offset'in f);require(sites==[51483,51654,52257]and sites==sorted(x for x in reference['relocations']if 0xc83a<=x<0xcc46),'Asset158 exactthree native MZ')
 loads=[]
 for base in [0,1,4096,65535]:
  a=bytearray(code);b=bytearray(native)
  for site in sites:
   at=site-0xc83a
   for buf in [a,b]:buf[at:at+2]=((int.from_bytes(buf[at:at+2],'little')+base)&65535).to_bytes(2,'little')
  require(a==b,'Asset158 full four-base forward comparison');loads.append(base)
 info=obj.function_info(unit['symbol']);return desc,data,{'classification':'complete_compiler_owned_CONST_uncredited_context','profile':PROFILE,'source_data_credit':0,'authored_c_function_count':0,'descriptor':desc,'size':158,'sha256':sha(data),'bytes_hex':data.hex(),'code_references':[{'object_offset':at,'original_addend':v}for at,v in refs],'complete_MZ_sites':[],'whole_CODE_MZ_sites':sites,'whole_CODE_scopes':scopes,'whole_CODE_size':1036,'whole_CODE_fields':89,'four_forward_load_bases':loads,'rea_evidence_id':eid,'rea_evidence_sha256':pins.EVIDENCE['pool']['sha256'],'data_frame':frame,'data_offset':offset,'owner_CODE_SEGDEF_size':1036,'owner_CODE_bytes_outside_procedure':1036-info['size'],'omf_records_or_fields_modified':False,'standalone_source_link_layout_proved':False}
