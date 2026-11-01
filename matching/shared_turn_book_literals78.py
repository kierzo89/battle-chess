"""Closed shared CODE2418/CONST78 mixed-pool comparison owner; no generation capabilities.

Seventeen full procedures match. Commit408 is retained whole with three exact
observed nonrelocation differences and receives no function/byte credit.
"""
from pathlib import Path
from dataclasses import asdict
import hashlib,json
from omf import OMFError,OMFObject
from reference import validate_data_address,validate_expanded_read,ORIGINAL_SHA256,CARRIER_SHA256
import shared_turn_book_literals78_pins as pins
KIND='shared_turn_book_literals78_v1'
KEYS={'kind','segment','group','size','image_offset','data_address','rea_evidence','code_evidence','target_symbol'}
SOURCE='src/shared_turn_book_literals_match.c'
FLAGS=['/AS','/Gs','/Os','/Zi']
OWNERS={'_setup_state','_accept_hint_82db','_scan_book_843f','_rotate_book_8515','_skip_book_8577','_previous_book_858d','_alternate_view','_commit_turn_810c'}
REGISTERED_OWNERS=OWNERS-{'_commit_turn_810c'}
class SharedLiteralsError(OMFError):pass
def require(ok,message):
 if not ok:raise SharedLiteralsError(message)
def canonical(v):
 def view(x):
  if isinstance(x,dict):
   require(all(type(k)in (int,str)for k in x),'Shared literals invalid snapshot key type')
   require(len({str(k)for k in x})==len(x),'Shared literals duplicate normalized snapshot key')
   return {str(k):view(y)for k,y in x.items()}
  if isinstance(x,(list,tuple)):return [view(y)for y in x]
  return x
 return json.dumps(view(v),sort_keys=True,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()
def full_bytes(segment,*,debug=False):
 require(not segment.unsupported_data,'Shared literals unsupported/iterated data')
 b=bytearray(segment.length);seen=bytearray(segment.length);cursor=0
 for at,body in (segment.chunks if debug else sorted(segment.chunks)):
  require(type(at)is int and 0<=at<=at+len(body)<=segment.length and bool(body),'Shared literals chunk bounds')
  if not debug:require(at==cursor,'Shared literals loaded hole/overlap');cursor+=len(body)
  b[at:at+len(body)]=body;seen[at:at+len(body)]=b'\1'*len(body)
 require(all(seen),'Shared literals incomplete allocation');return bytes(b)
def snapshot(obj):
 """Bind raw record chronology AND all independently parsed mutable views."""
 return {'records':[{'kind':k,'offset':at,'payload_hex':b.hex()}for k,at,b in obj.records],
 'names':obj.names,'externals':obj.externals,'publics':{n:asdict(v)for n,v in obj.publics.items()},'procedures':obj.procedures,'data_writes':obj.data_writes,
 'segments':{i:{**{k:v for k,v in asdict(s).items()if k!='chunks'},'chunks':[{'offset':at,'bytes_hex':b.hex()}for at,b in s.chunks]}for i,s in obj.segments.items()},
 'fixups':[{**asdict(f),'raw':f.raw.hex()}for f in obj.fixups]}
def profile():
 p=Path(__file__).with_name('shared_turn_book_literals78_profile.json');raw=p.read_bytes()
 require(sha(raw)==pins.PROFILE_SHA256,'Shared literals closed profile SHA changed');return json.loads(raw)
def validate_shared_object(obj):
 require(isinstance(obj,OMFObject),'Shared literals actual OMF required');p=profile()
 require(canonical(snapshot(obj))==canonical(p['object_snapshot']),'Shared literals complete raw/parsed object fingerprint changed')
 require(len(obj.fixups)==451 and sum(f.segment==1 for f in obj.fixups)==362 and sum(f.segment==3 for f in obj.fixups)==1 and sum(f.segment==5 for f in obj.fixups)==88,'Shared literals CODE362/CONST1/DEBUG88')
 require(set(obj.publics)==set(obj.procedures)==set(p['procedures'])and len(obj.publics)==18,'Shared literals exact18 PUBLIC/CVs')
 for name,(at,size)in p['procedures'].items():
  i=obj.function_info(name);pub=obj.publics[name]
  require((pub.group,pub.segment,pub.offset)==(0,1,at)and(i['segment'],i['offset'],i['size'],i['boundary'])==(1,at,size,'codeview3_procedure'),'Shared literals complete independent CV/public boundary')
 code=full_bytes(obj.segments[1]);const=full_bytes(obj.segments[3]);full_bytes(obj.segments[2]);full_bytes(obj.segments[4]);full_bytes(obj.segments[5],debug=True);full_bytes(obj.segments[6],debug=True)
 require(len(code)==2418 and const==bytes.fromhex(p['raw_CONST_hex'])and len(const)==78,'Shared literals natural whole CODE2418/CONST78')
 require(obj.segments[3].chunks==[(2,const[2:]),(0,b'\0\0')],'Shared literals exact disjoint CONST chronology76then2')
 # Genuine debug patch writes replay in record order, with no arbitrary holes.
 shadow=[]
 for f in obj.fixups:
  overlaps=[(at,sn,off,n)for at,sn,off,n in obj.data_writes if at>f.record_offset and sn==f.segment and off<f.offset+f.width and f.offset<off+n]
  if overlaps:
   require(f.segment==5 and f.width==2 and f.location_type==1,'Shared literals only known early DEBUG OFFSET patches');shadow.append(f.offset)
 require(shadow==p['shadowed_debug_offsets']and len(shadow)==18,'Shared literals exact18 overwritten debug fields')
 refs=[f for f in obj.fixups if f.target==(0,3)]
 require(sorted((f.offset,int.from_bytes(code[f.offset:f.offset+2],'little'))for f in refs)==[tuple(x)for x in p['CONST_references']]and len(refs)==13,'Shared literals all thirteen real ownCONST fields/addends')
 require(all((f.segment,f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(1,2,1,True,(1,1),None)for f in refs),'Shared literals own CONST field shapes')
 cf=[f for f in obj.fixups if f.segment==3];require(len(cf)==1,'Shared literals sole CONST field');f=cf[0]
 require((f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(0,2,2,True,(5,None),None)and f.target[0]==2 and obj.externals.get(f.target[1])=='_splash_buffer'and const[:2]==b'\0\0','Shared literals actual typed selector BASE16 only')
 return p
def validate_unit_metadata(unit):
 require(isinstance(unit,dict),'Shared literals C unit required');d=unit.get('owned_selector_const');p=profile()
 require(isinstance(d,dict)and set(d)==KEYS and canonical(d)==canonical(p['descriptor']),'Shared literals exact closed descriptor')
 n=unit.get('symbol');require(n in REGISTERED_OWNERS,'Shared literals actual matched owner only; commit remains held');at,size=p['procedures'][n]
 require(unit.get('id')==p['owner_ids'][n],'Shared literals exact owner ID')
 require(unit.get('language')=='c'and unit.get('backend')=='msc500-omf'and unit.get('source')==SOURCE and unit.get('image_offset')==hex(0x7c52+at)and type(unit.get('size'))is int and unit['size']==size and unit.get('flags')==FLAGS,'Shared literals exact C source/owner/extent/flags')
 require(not any(unit.get(k)is not None for k in ('owned_const','owned_data','owned_bss','code_address','object_profile')),'Shared literals exclusive ordinary MSC500 owner')
 if n=='_skip_book_8577':require(isinstance(unit.get('extended_extent'),dict)and unit['extended_extent'].get('kind')=='shared_book_skip_literals78_8577_v1','Shared literals skip exact new extent required')
 elif n=='_alternate_view':require(isinstance(unit.get('extended_extent'),dict)and unit['extended_extent'].get('kind')=='alternate_view_switch_7e6b_v1','Shared literals alternate keeps native extent')
 elif n=='_setup_state':require(unit.get('extended_extent')is None,'Shared setup141 ordinary boundary')
 else:require(unit.get('extended_extent')is None,'Shared literals unexpected extent')
 require(canonical(unit.get('externals'))==canonical(p['externals']),'Shared literals full exact same-symbol bindings')
def validate_layout(obj,descriptor,externals):
 p=validate_shared_object(obj)
 require(isinstance(descriptor,dict)and canonical(descriptor)==canonical(p['descriptor']),'Shared literals exact placement/descriptor')
 require(canonical(externals)==canonical(p['externals']),'Shared literals exact typed native bindings')
 return 0x4da6

def compare_context(code,const,fields,reference,p):
 """Strict whole context comparison; never repairs source bytes or reference."""
 require(reference.get('original_sha256')==ORIGINAL_SHA256 and reference.get('carrier_sha256')==CARRIER_SHA256,'Shared literals pinned reference provenance')
 native=reference['image'][0x7c52:0x85c4]
 require(len(code)==len(native)==2418 and sha(native)==p['native_CODE_sha256']and sha(code)==p['linked_CODE_sha256'],'Shared literals full emitted/native context hash')
 differences=[{'shared_offset':i,'emitted_byte':a,'native_byte':b}for i,(a,b)in enumerate(zip(code,native))if a!=b]
 require(differences==p['held_three_differences'],'Shared literals exact held commit three differences required')
 sites=[r['mz_segment_relocation_image_offset']for r in fields if'mz_segment_relocation_image_offset'in r]
 require(sorted(sites)==[0x7e22,0x82d0,0x82e6,0x837c]and len(sites)==4,'Shared literals all four CODE MZ fields')
 require(len(fields)==362,'Shared literals complete362 actual CODE field logs')
 require([(r['object_offset'],r['width'],r['record_offset'],r['raw_fixupp'])for r in fields]==[(r['offset'],r['width'],r['record_offset'],r['raw'])for r in sorted((f for f in p['object_snapshot']['fixups']if f['segment']==1),key=lambda f:(f['offset'],f['record_offset']))],'Shared literals every raw CODE field logged once in actual order')
 native_sites=set(reference['relocations']);overlap={x for x in native_sites if 0x7c52<=x<0x85c4}
 require(overlap==set(sites)and 0x619c6 in native_sites,'Shared literals native complete CODE/CONST MZ ownership')
 require(len(const)==78 and const==reference['image'][0x619c6:0x61a14]and sha(const)==p['native_CONST_sha256'],'Shared literals actual complete CONST78')
 matched=[]
 for n,(at,size)in p['procedures'].items():
  actual=code[at:at+size];target=native[at:at+size];entry=p['function_hashes'][n]
  require(sha(actual)==entry['emitted']and sha(target)==entry['native'],'Shared literals full per-procedure hashes')
  require((actual==target)==(n!='_commit_turn_810c'),'Shared literals17 full matches/held408 boundary');matched.append(n)if actual==target else None
 four=[]
 for base in [0,1,0x1000,0xffff]:
  a=bytearray(code);b=bytearray(native);ac=bytearray(const);bc=bytearray(reference['image'][0x619c6:0x61a14])
  for site in sorted(sites)+[0x619c6]:
   aa,bb,at=(ac,bc,0)if site==0x619c6 else(a,b,site-0x7c52)
   for buffer in (aa,bb):buffer[at:at+2]=((int.from_bytes(buffer[at:at+2],'little')+base)&65535).to_bytes(2,'little')
  require([i for i,(x,y)in enumerate(zip(a,b))if x!=y]==[1215,1539,1594]and ac==bc,'Shared literals four-base exact differences')
  four.append({'load_paragraph':base,'CODE_differences':[1215,1539,1594],'CONST_equal':True})
 return {'whole_CODE_exact_native':False,'matched_complete_procedures':matched,'matched_complete_procedure_count':17,'matched_complete_procedure_bytes':2010,'held_commit_bytes':408,'held_commit_differences':differences,'four_load_bases':four}
def validate(unit,obj,project,reference,*,function_linker=None):
 validate_unit_metadata(unit);d=unit['owned_selector_const'];p=validate_shared_object(obj);validate_layout(obj,d,unit['externals']);project=Path(project).resolve()
 source=(project/SOURCE).resolve();require(source.is_relative_to(project)and sha(source.read_bytes())==pins.SOURCE_SHA256,'Shared literals genuine source hash')
 evidence={}
 for key,identity in pins.EVIDENCE.items():
  relative=identity['path'];path=(project/relative).resolve();require(not Path(relative).is_absolute()and path.is_relative_to(project),'Shared literals evidence escape');raw=path.read_bytes();require(sha(raw)==identity['sha256'],'Shared literals retained proof changed');evidence[key]=json.loads(raw)
 g=evidence['generation'];t=evidence['terminal'];require(g['status']=='COMPLETE'and g['guard_closed']is True and g['actual_C5_calls']==1 and len(g['calls'])==1 and g['calls'][0]['terminal']and g['calls'][0]['reaped']and g['calls'][0]['returncode']==0 and g['source_tools_new_scratch_only']is True and g['native_original_oldOBJ_comparison_inputs_inside_GEN']is False and len(g['blocked_probes'])==20 and g['raw_whole_object_sha256']==pins.OBJECT_SHA256 and g['source_sha256']==pins.SOURCE_SHA256 and g['compiler']=='msc500'and g['flags']==FLAGS and g['source_name']=='UNIT.C','Shared literals retained genuine source generation closure')
 require(t['exit_code']==0 and t['actual_C5_calls']==1 and t['terminal']is True and t['reaped']is True and t['generation_receipt_sha256']==pins.EVIDENCE['generation']['sha256'],'Shared literals root observed closed oneC5')
 require(evidence['comparison']['whole_object_sha256']==pins.OBJECT_SHA256 and evidence['comparison']['source_sha256']==pins.SOURCE_SHA256 and evidence['comparison']['all_raw_FIXUPPs']==451 and evidence['comparison']['whole_CODE_differences']==[1215,1539,1594],'Shared literals actual prior source/object proof')
 validate_data_address(dict(d,reference_region='exepack-expanded'),reference)
 # Derive a local linked comparison view from actual compiler CONST and its genuine BASE16 field.
 pool=bytearray(full_bytes(obj.segments[3]));f=next(f for f in obj.fixups if f.segment==3);target=unit['externals'][obj.externals[f.target[1]]];value=(target['segment']+int.from_bytes(pool[:2],'little'))&65535;pool[:2]=value.to_bytes(2,'little');pool=bytes(pool)
 sid=validate_expanded_read(evidence['pool'],dict(d,reference_region='exepack-expanded'),pool,reference,emitted_mz_sites=[0x619c6])
 if function_linker is None:
  from link16 import link_function
  function_linker=link_function
 code=bytearray();fields=[]
 for name,(at,size)in p['procedures'].items():
  body,relocations=function_linker(obj,name,0x7c52+at,unit['externals'],**({'owned_selector_const':d}if name in OWNERS else{}))
  require(len(code)==at and len(body)==size,'Shared literals all18 complete linked procedure partition');code.extend(body);fields.extend(relocations)
 context=compare_context(bytes(code),pool,fields,reference,p)
 return d,pool,dict(classification='shared_complete_compiler_mixed_pool_with_explicit_held_commit',authored_c_function_credit=0,source_data_credit=0,size=78,complete_CONST_bytes=78,literal_bytes_future_unregistered=76,selector_word_bytes=2,selector_bytes_hex=pool.hex(),complete_MZ_sites=[0x619c6],complete_CODE_bytes=2418,complete_CODE_fields=fields,CODE_MZ_sites=[0x7e22,0x82d0,0x82e6,0x837c],selector_primary_id=sid,selector_primary_sha256=pins.EVIDENCE['pool']['sha256'],code_primary_id='retained-shared-literals78-comparison:'+pins.EVIDENCE['comparison']['sha256'],code_primary_kind='retained source comparison ledger, not a fabricated REA record',original_global_MAP_proved=False,omf_records_or_fields_modified=False,**context)
