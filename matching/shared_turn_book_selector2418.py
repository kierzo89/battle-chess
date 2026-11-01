"""Closed shared CODE2418/CONST2 comparison owner; no generation capabilities.

Seventeen full procedures match. Commit408 is retained whole with three exact
observed nonrelocation differences and receives no function/byte credit.
"""
from pathlib import Path
from dataclasses import asdict
import hashlib,json
from omf import OMFError,OMFObject
from reference import validate_data_address,validate_expanded_read,ORIGINAL_SHA256,CARRIER_SHA256
import shared_turn_book_selector2418_pins as pins
KIND='shared_turn_book_selector_2418_v1'
KEYS={'kind','segment','group','size','image_offset','data_address','rea_evidence','code_evidence','target_symbol'}
SOURCE='src/shared_turn_book_context_match.c'
FLAGS=['/AS','/Gs','/Os','/Zi']
OWNERS={'_setup_state','_accept_hint_82db','_scan_book_843f','_rotate_book_8515','_skip_book_8577','_previous_book_858d'}
class SharedSelectorError(OMFError):pass
def require(ok,message):
 if not ok:raise SharedSelectorError(message)
def canonical(v):
 def view(x):
  if isinstance(x,dict):
   require(all(type(k)in (int,str)for k in x),'Shared selector invalid snapshot key type')
   require(len({str(k)for k in x})==len(x),'Shared selector duplicate normalized snapshot key')
   return {str(k):view(y)for k,y in x.items()}
  if isinstance(x,(list,tuple)):return [view(y)for y in x]
  return x
 return json.dumps(view(v),sort_keys=True,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()
def full_bytes(segment,*,debug=False):
 require(not segment.unsupported_data,'Shared selector unsupported/iterated data')
 b=bytearray(segment.length);seen=bytearray(segment.length);cursor=0
 for at,body in segment.chunks:
  require(type(at)is int and 0<=at<=at+len(body)<=segment.length and bool(body),'Shared selector chunk bounds')
  if not debug:require(at==cursor,'Shared selector loaded hole/overlap');cursor+=len(body)
  b[at:at+len(body)]=body;seen[at:at+len(body)]=b'\1'*len(body)
 require(all(seen),'Shared selector incomplete allocation');return bytes(b)
def snapshot(obj):
 """Bind raw record chronology AND all independently parsed mutable views."""
 return {'records':[{'kind':k,'offset':at,'payload_hex':b.hex()}for k,at,b in obj.records],
 'names':obj.names,'externals':obj.externals,'publics':{n:asdict(v)for n,v in obj.publics.items()},'procedures':obj.procedures,'data_writes':obj.data_writes,
 'segments':{i:{**{k:v for k,v in asdict(s).items()if k!='chunks'},'chunks':[{'offset':at,'bytes_hex':b.hex()}for at,b in s.chunks]}for i,s in obj.segments.items()},
 'fixups':[{**asdict(f),'raw':f.raw.hex()}for f in obj.fixups]}
def profile():
 p=Path(__file__).with_name('shared_turn_book_selector2418_profile.json');raw=p.read_bytes()
 require(sha(raw)==pins.PROFILE_SHA256,'Shared selector closed profile SHA changed');return json.loads(raw)
def validate_shared_object(obj):
 require(isinstance(obj,OMFObject),'Shared selector actual OMF required');p=profile()
 require(canonical(snapshot(obj))==canonical(p['object_snapshot']),'Shared selector complete raw/parsed object fingerprint changed')
 require(len(obj.fixups)==456 and sum(f.segment==1 for f in obj.fixups)==362 and sum(f.segment==3 for f in obj.fixups)==1 and sum(f.segment==5 for f in obj.fixups)==93,'Shared selector CODE362/CONST1/DEBUG93')
 require(set(obj.publics)==set(obj.procedures)==set(p['procedures'])and len(obj.publics)==18,'Shared selector exact18 PUBLIC/CVs')
 for name,(at,size)in p['procedures'].items():
  i=obj.function_info(name);pub=obj.publics[name]
  require((pub.group,pub.segment,pub.offset)==(0,1,at)and(i['segment'],i['offset'],i['size'],i['boundary'])==(1,at,size,'codeview3_procedure'),'Shared selector complete independent CV/public boundary')
 code=full_bytes(obj.segments[1]);const=full_bytes(obj.segments[3]);full_bytes(obj.segments[2]);full_bytes(obj.segments[4]);full_bytes(obj.segments[5],debug=True);full_bytes(obj.segments[6],debug=True)
 require(len(code)==2418 and const==b'\0\0','Shared selector natural whole CODE2418/CONST2')
 # Genuine debug patch writes replay in record order, with no arbitrary holes.
 shadow=[]
 for f in obj.fixups:
  overlaps=[(at,sn,off,n)for at,sn,off,n in obj.data_writes if at>f.record_offset and sn==f.segment and off<f.offset+f.width and f.offset<off+n]
  if overlaps:
   require(f.segment==5 and f.width==2 and f.location_type==1,'Shared selector only known early DEBUG OFFSET patches');shadow.append(f.offset)
 require(shadow==p['shadowed_debug_offsets']and len(shadow)==18,'Shared selector exact18 overwritten debug fields')
 refs=[f for f in obj.fixups if f.target==(0,3)]
 require(sorted(f.offset for f in refs)==[97,1752,2115,2140,2255,2276,2352,2384],'Shared selector all eight real owner fields')
 require(all((f.segment,f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(1,2,1,True,(1,1),None)and code[f.offset:f.offset+2]==b'\0\0'for f in refs),'Shared selector own CONST field shapes')
 return p
def validate_unit_metadata(unit):
 require(isinstance(unit,dict),'Shared selector C unit required');d=unit.get('owned_selector_const');p=profile()
 require(isinstance(d,dict)and set(d)==KEYS and canonical(d)==canonical(p['descriptor']),'Shared selector exact closed descriptor')
 n=unit.get('symbol');require(n in OWNERS,'Shared selector actual owner only');at,size=p['procedures'][n]
 require(unit.get('id')==p['owner_ids'][n],'Shared selector exact owner ID')
 require(unit.get('language')=='c'and unit.get('backend')=='msc500-omf'and unit.get('source')==SOURCE and unit.get('image_offset')==hex(0x7c52+at)and type(unit.get('size'))is int and unit['size']==size and unit.get('flags')==FLAGS,'Shared selector exact C source/owner/extent/flags')
 require(not any(unit.get(k)is not None for k in ('owned_const','owned_data','owned_bss','code_address','object_profile')),'Shared selector exclusive ordinary MSC500 owner')
 if n=='_skip_book_8577':require(isinstance(unit.get('extended_extent'),dict)and unit['extended_extent'].get('kind')=='shared_book_skip_8577_v1','Shared selector skip exact new extent required')
 elif n=='_setup_state':require(unit.get('extended_extent')is None,'Shared setup141 ordinary boundary')
 else:require(unit.get('extended_extent')is None,'Shared selector unexpected extent')
 require(canonical(unit.get('externals'))==canonical(p['externals']),'Shared selector full exact same-symbol bindings')
def validate_layout(obj,descriptor,externals):
 p=validate_shared_object(obj)
 require(isinstance(descriptor,dict)and canonical(descriptor)==canonical(p['descriptor']),'Shared selector exact placement/descriptor')
 require(canonical(externals)==canonical(p['externals']),'Shared selector exact typed native bindings')
 return 0x4da6

def compare_context(code,const,fields,reference,p):
 """Strict whole context comparison; never repairs source bytes or reference."""
 require(reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Shared selector pinned reference provenance')
 native=reference['image'][0x7c52:0x85c4]
 require(len(code)==len(native)==2418 and sha(native)==p['native_CODE_sha256']and sha(code)==p['linked_CODE_sha256'],'Shared selector full emitted/native context hash')
 differences=[{'shared_offset':i,'emitted_byte':a,'native_byte':b}for i,(a,b)in enumerate(zip(code,native))if a!=b]
 require(differences==p['held_three_differences'],'Shared selector exact held commit three differences required')
 sites=[r['mz_segment_relocation_image_offset']for r in fields if'mz_segment_relocation_image_offset'in r]
 require(sorted(sites)==[0x7e22,0x82d0,0x82e6,0x837c]and len(sites)==4,'Shared selector all four CODE MZ fields')
 require(len(fields)==362,'Shared selector complete362 actual CODE field logs')
 require([(r['object_offset'],r['width'],r['record_offset'],r['raw_fixupp'])for r in fields]==[(r['offset'],r['width'],r['record_offset'],r['raw'])for r in sorted((f for f in p['object_snapshot']['fixups']if f['segment']==1),key=lambda f:(f['offset'],f['record_offset']))],'Shared selector every raw CODE field logged once in actual order')
 native_sites=set(reference['relocations']);overlap={x for x in native_sites if 0x7c52<=x<0x85c4}
 require(overlap==set(sites)and 0x619c6 in native_sites,'Shared selector native complete CODE/CONST MZ ownership')
 require(const==reference['image'][0x619c6:0x619c8]==b'\x09\x1f','Shared selector actual complete CONST2')
 matched=[]
 for n,(at,size)in p['procedures'].items():
  actual=code[at:at+size];target=native[at:at+size];entry=p['function_hashes'][n]
  require(sha(actual)==entry['emitted']and sha(target)==entry['native'],'Shared selector full per-procedure hashes')
  require((actual==target)==(n!='_commit_turn_810c'),'Shared selector17 full matches/held408 boundary');matched.append(n)if actual==target else None
 four=[]
 for base in [0,1,0x1000,0xffff]:
  a=bytearray(code);b=bytearray(native);ac=bytearray(const);bc=bytearray(reference['image'][0x619c6:0x619c8])
  for site in sorted(sites)+[0x619c6]:
   aa,bb,at=(ac,bc,0)if site==0x619c6 else(a,b,site-0x7c52)
   for buffer in (aa,bb):buffer[at:at+2]=((int.from_bytes(buffer[at:at+2],'little')+base)&65535).to_bytes(2,'little')
  require([i for i,(x,y)in enumerate(zip(a,b))if x!=y]==[1215,1539,1594]and ac==bc,'Shared selector four-base exact differences')
  four.append({'load_paragraph':base,'CODE_differences':[1215,1539,1594],'CONST_equal':True})
 return {'whole_CODE_exact_native':False,'matched_complete_procedures':matched,'matched_complete_procedure_count':17,'matched_complete_procedure_bytes':2010,'held_commit_bytes':408,'held_commit_differences':differences,'four_load_bases':four}
def validate(unit,obj,project,reference,*,function_linker=None):
 validate_unit_metadata(unit);d=unit['owned_selector_const'];p=validate_shared_object(obj);validate_layout(obj,d,unit['externals']);project=Path(project).resolve()
 source=(project/SOURCE).resolve();require(source.is_relative_to(project)and sha(source.read_bytes())==pins.SOURCE_SHA256,'Shared selector genuine source hash')
 evidence={}
 for key,identity in pins.EVIDENCE.items():
  relative=identity['path'];path=(project/relative).resolve();require(not Path(relative).is_absolute()and path.is_relative_to(project),'Shared selector evidence escape');raw=path.read_bytes();require(sha(raw)==identity['sha256'],'Shared selector retained proof changed');evidence[key]=json.loads(raw)
 require(evidence['generation']['actual_compiler_calls']==1 and evidence['generation']['source_tool_scratch_only']and len(evidence['generation']['blocked_probes'])==5,'Shared selector retained genuine source generation closure')
 require(evidence['comparison']['object_sha256']==pins.OBJECT_SHA256 and evidence['comparison']['source_sha256']==pins.SOURCE_SHA256,'Shared selector actual prior source/object proof')
 validate_data_address(dict(d,reference_region='exepack-expanded'),reference);selector=b'\x09\x1f';sid=validate_expanded_read(evidence['selector'],dict(d,reference_region='exepack-expanded'),selector,reference,emitted_mz_sites=[0x619c6])
 if function_linker is None:
  from link16 import link_function
  function_linker=link_function
 code=bytearray();fields=[]
 for name,(at,size)in p['procedures'].items():
  body,relocations=function_linker(obj,name,0x7c52+at,unit['externals'],**({'owned_selector_const':d}if name in OWNERS else{}))
  require(len(code)==at and len(body)==size,'Shared selector all18 complete linked procedure partition');code.extend(body);fields.extend(relocations)
 context=compare_context(bytes(code),selector,fields,reference,p)
 return d,selector,dict(classification='shared_complete_compiler_context_with_explicit_held_commit',authored_c_function_credit=0,source_data_credit=0,size=2,selector_bytes_hex=selector.hex(),complete_MZ_sites=[0x619c6],complete_CODE_bytes=2418,complete_CODE_fields=fields,CODE_MZ_sites=[0x7e22,0x82d0,0x82e6,0x837c],selector_primary_id=sid,selector_primary_sha256=pins.EVIDENCE['selector']['sha256'],code_primary_id='retained-shared2418-comparison:'+pins.EVIDENCE['comparison']['sha256'],code_primary_kind='retained source comparison ledger, not a fabricated REA record',original_global_MAP_proved=False,omf_records_or_fields_modified=False,**context)
