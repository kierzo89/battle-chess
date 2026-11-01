"""Two exact observed whole OMF profiles; no generators/reference reads or old-gate edits."""
from pathlib import Path
from dataclasses import asdict
import hashlib,json
from omf import read_omf,_Cursor
PROFILE_SHA='e125c9b6660bc2a844daaeb576719c515216ff831eb0b6f6c2a95468606b2af0'
class HuffWorkspaceError(ValueError):pass
def need(v,m):
 if not v:raise HuffWorkspaceError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def profile():
 b=Path(__file__).with_name('huff_workspace_profile.json').read_bytes();need(sha(b)==PROFILE_SHA,'Huff workspace profile checksum');return json.loads(b)
def extract_code(raw):
 p=profile();need(isinstance(raw,bytes)and sha(raw)==p['code_object_sha256'],'Exact genuine whole caller91cf object');return _code_structure(read_omf(raw))
def _code_structure(o):
 p=profile();need(set(o.segments)=={1},'one CODE segment only');s=o.segments[1]
 need((s.name,s.class_name,s.attributes,s.length,s.unsupported_data)==('_TEXT','CODE',72,944,False),'whole CODE944 shape');need(o.names==['','','_TEXT','CODE','DGROUP'],'exact new name inventory')
 need(o.externals==dict(enumerate(p['EXTERNALS'],1))and{n:q.offset for n,q in o.publics.items()}==p['PUBLICS']and len(o.publics)==9 and all((q.segment,q.group,q.type_index)==(1,0,0)for q in o.publics.values()),'same nine PUBLIC/fourteen EXTDEF')
 need([b for k,at,b in o.records if k==0x9a]==[b'\x04'],'one empty DGROUP1; no invented DATA segment');need(not o.procedures,'no extra procedure/debug allocation')
 for k,at,b in o.records:
  need(k in(0x80,0x88,0x96,0x98,0x9a,0x8c,0x90,0xa0,0x9c,0x8a),'closed CODE records only')
  if k==0x8a:need(b==b'\0','no entrypoint')
 code=bytearray()
 for at,b in sorted(s.chunks):need(b and at==len(code)and at+len(b)<=944,'contiguous complete CODE');code.extend(b)
 need(len(code)==944 and sha(code)==p['code_raw_sha256'],'unchanged all944 instructions/addends');fields=[]
 for f in sorted(o.fixups,key=lambda f:f.offset):
  need(f.segment==1 and f.target[0]==2,'CODE fields use exact external targets');fields.append({'offset':f.offset,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'frame':list(f.frame),'target_symbol':o.externals.get(f.target[1]),'displacement':f.displacement})
 need(fields==p['code_semantic_fields']and len(fields)==77,'exact ten group1/sixtyseven default frames; no broad frame allowance')
 pubs=sorted(o.publics.values(),key=lambda q:q.offset);extents=[{'symbol':q.name,'offset':q.offset,'size':(pubs[i+1].offset if i+1<len(pubs)else 944)-q.offset}for i,q in enumerate(pubs)]
 return bytes(code),{'boundary':'complete_asm_CODE_SEGDEF','segment':{'index':1,'name':'_TEXT','class_name':'CODE','attributes':72,'length':944},'publics':[asdict(q)for q in pubs],'public_extents':extents,'raw_code_sha256':sha(code),'fixups':fields,'emitted_mz_sites':[],'additional_matching_credit':0,'authored_c_credit':0,'empty_DGROUP1':True}
def link_code(raw,*,cs=0,ds=0x5cc2):
 code,meta=extract_code(raw);p=profile();o=read_omf(raw);out=bytearray(code);logs=[];base=0xe03a;names=set(p['group_names'])
 need(all(type(x)is int and 0<=x<=65535 for x in(cs,ds)),'bounded explicit source/native placement')
 for f in sorted(o.fixups,key=lambda f:f.offset):
  n=o.externals[f.target[1]];target=p['EXTERNALS'][n];add=int.from_bytes(code[f.offset:f.offset+2],'little');disp=f.displacement or 0
  if f.frame==(1,1):need(n in names and f.segment_relative,'only exact three-name GROUP contract');value=(ds*16+target)-ds*16+add+disp;mode='segment_relative_dgroup_explicit1'
  elif f.segment_relative:need(f.frame==(5,None)and n not in names,'unchanged old preferred frame');value=target+add+disp;mode='segment_relative_dgroup'
  else:need(f.frame==(5,None)and n in['_huff_refill_e3ea','_huff_depth_trap_e410'],'unchanged native near CALL');value=cs*16+target+add+disp-(cs*16+base+f.offset+2);mode='self_relative_code'
  v=value&65535;out[f.offset:f.offset+2]=v.to_bytes(2,'little');logs.append({'segment':1,'object_offset':f.offset,'image_offset':cs*16+base+f.offset,'width':2,'mode':mode,'frame':list(f.frame),'target':list(f.target),'target_symbol':n,'original_addend':add,'target_displacement':disp,'encoded_value':v,'encoded_hex':v.to_bytes(2,'little').hex(),'raw_fixupp':f.raw.hex(),'record_offset':f.record_offset})
 return bytes(out),logs

def _decode_observed_tree(encoded,limit):
 q=_Cursor(encoded);nodes=0
 def block(depth):
  nonlocal nodes
  nodes+=1;need(nodes<=2 and depth<=2,'exact bounded two-node tree');repeat=q.word();children=q.word();need(1<=repeat<=1024 and children<=1,'finite actual repeat/child shape')
  if children:data,child=block(depth+1);tree={'repeat':repeat,'children':[child]}
  else:n=q.byte();need(n==2,'only actual literal WORD');data=q.take(n);need(data==bytes(2),'actual zero leaf');tree={'repeat':repeat,'literal_hex':data.hex()}
  need(len(data)*repeat<=limit,'declared component extent');return data*repeat,tree
 data,tree=block(1);q.finish();need(nodes==2,'observed outer/child only');return data,tree

def extract_data(raw):
 p=profile();need(isinstance(raw,bytes)and sha(raw)==p['data_object_sha256'],'Exact genuine whole DATA0e1c object');return _data_structure(read_omf(raw))
def _data_structure(o):
 p=profile();need(set(o.segments)=={1},'one DATA only');s=o.segments[1]
 need((s.name,s.class_name,s.attributes,s.length,s.unsupported_data,s.chunks)==('_DATA','DATA',72,5120,True,[]),'actual LIDATA shape; never invent LEDATA chunks')
 need(o.names==['','','DGROUP','DATA','_DATA']and not o.fixups and not o.externals and not o.procedures,'no new names/fixups/externals/procedures')
 need({n:(q.segment,q.offset,q.group,q.type_index)for n,q in o.publics.items()}=={'_huff_code_table':(1,0,0,0),'_huff_fast_lookup':(1,1024,0,0),'_huff_long_records':(1,2048,0,0)},'preserve actual PUB0, no alias/metadata normalization')
 need([k for k,at,b in o.records]==[0x80,0x96,0x98,0x9a,0x90,0x88,0xa2,0xa2,0xa2,0xa2,0x8a]and[b for k,at,b in o.records if k==0x9a]==[bytes.fromhex('02ff01')],'exact DATA record grammar/group1 member1')
 parts=[];writes=[]
 for(k,at,b),(off,size,repeat)in zip([(k,at,b)for k,at,b in o.records if k==0xa2],[(0,1024,512),(1024,1024,512),(2048,1024,512),(3072,2048,1024)]):
  q=_Cursor(b);need(q.index()==1 and q.word()==off,'whole four record order/ownership');enc=q.take(len(b)-q.pos);data,tree=_decode_observed_tree(enc,size);need(len(data)==size and tree['repeat']==repeat and tree['children']==[{'repeat':1,'literal_hex':'0000'}],'exact observed raw initialized trees');parts.append(data);writes.append({'record_offset':at,'offset':off,'size':size,'payload_hex':b.hex(),'tree':tree})
 data=b''.join(parts);need(len(data)==5120 and sha(data)==p['data_sha256'],'complete initialized5120, no hole/reservation fill')
 return data,{'boundary':'complete_initialized_DATA5120_exact_LIDATA4','segment':{'index':1,'name':'_DATA','class_name':'DATA','attributes':72,'length':5120},'publics':[asdict(q)for q in o.publics.values()],'group':{'index':1,'name':'DGROUP','members':[1]},'actual_PUBLIC_group':0,'initialized_LIDATA_bytes':5120,'raw_literal_leaf_bytes':8,'unwritten_reservation_bytes':0,'source_records':writes,'opaque_tail_bytes':2048,'historical_capacity_TU_original_storageclass_proven':False,'source_partition_is_engineering':True,'C_credit':0}
