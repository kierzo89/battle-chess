"""Closed library-only CRT0DAT DATA80 view; default strict OMF/LIDATA stays unchanged."""
from dataclasses import dataclass
from pathlib import Path
import hashlib,json
from omf import _Cursor,OMFError
from library16 import LibraryError,_placement,_word
from runtime_lidata16_pins import PROFILE,PINS
POLICY='omf86-lidata16-no-fixups-v1'
MEMBER_SHA='7de3c7cc3fbe49972516b099306c89568daa34f6e46529b2c0ba79ba598952a5'
LIBRARY_SHA='7eabd615308e9a05de24f6e6e82e61a65f733eb64d12b5318d8b3ed569e389b9'
SOURCE_SHA='405444c9f977dfbfb75db7e325abb8718f874731987b41cad1ab062f9a8d7e6a'
WANTED_WRITES=[(444,0xa0,0,40),(491,0xa2,40,3),(508,0xa2,43,2),(525,0xa2,45,15),(542,0xa0,60,20)]

def require(v,msg):
 if not v:raise LibraryError('LIDATA16: '+msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def validate_profile(module):
 require(module==PROFILE,'only exact declared CRT0DAT DATA3 profile/policy allowed')
def validate_unit(unit):
 require((unit.get('id'),unit.get('image_offset'),unit.get('size'),unit.get('language'),unit.get('backend'),unit.get('source'),unit.get('member'),unit.get('runtime_kind'),unit.get('reference_region'))==('runtime_data_crt0dat_s3','0x615d0',80,'runtime','msc500-library','config/runtime500.json','CRT0DAT_DATA_3','initialized_data','exepack-expanded'),'Runtime independent segment/public extent mismatch: exact whole DATA80 unit required')
 require(type(unit['size'])is int and not unit.get('symbol')and unit.get('rea_evidence')==PINS['REA']['path'],'Runtime independent segment/public extent mismatch: whole SEGDEF boundary/REA selection required')

def decode_blocks(encoded,*,limit=65536,max_depth=32):
 """Decode bounded OMF86 16-bit recursive block stream, no relocation support."""
 require(isinstance(encoded,bytes)and type(limit)is int and 0<=limit<=65536 and type(max_depth)is int and 1<=max_depth<=64,'invalid bounded decoder inputs')
 q=_Cursor(encoded);nodes=0;budget=len(encoded)//4
 def block(depth):
  nonlocal nodes
  require(depth<=max_depth,'nesting limit exceeded');nodes+=1;require(nodes<=budget,'encoded node budget exceeded')
  begin=q.pos;repeat,children=q.word(),q.word();tree={'encoded_start':begin,'repeat':repeat,'child_blocks':children}
  if children:
   parts=[];trees=[];size=0
   for _ in range(children):
    content,child=block(depth+1);size+=len(content);require(size<=limit,'child expansion exceeds declared bound');parts.append(content);trees.append(child)
   one=b''.join(parts);tree['children']=trees
  else:
   one=q.take(q.byte());tree['literal_hex']=one.hex()
  require(not len(one)or repeat<=limit//len(one),'repeat expansion exceeds declared bound')
  content=one*repeat;tree.update(encoded_end=q.pos,expanded_bytes=len(content));return content,tree
 try:
  parts=[];trees=[];total=0
  while q:
   part,tree=block(1);total+=len(part);require(total<=limit,'root expansion exceeds declared bound');parts.append(part);trees.append(tree)
  require(bool(trees),'empty LIDATA block stream');q.finish();return b''.join(parts),trees
 except (OMFError,IndexError)as exc:raise LibraryError('LIDATA16: malformed iterated tree: '+str(exc))from exc

@dataclass(frozen=True)
class InitializedView:
 data:bytes
 records:tuple
 iterated_ranges:tuple


def initialized_view(obj,segment,*,policy):
 """Decode actual A0/A2 records; never changes obj, segment.chunks or raw records."""
 require(policy==POLICY,'unknown initialized record policy');require(segment in obj.segments,'undefined selected segment');seg=obj.segments[segment];require(type(seg.length)is int and 0<seg.length<=65536,'invalid whole segment extent')
 writes=[];raw_chunks=[];occupied=[];iterated=[]
 for kind,at,payload in obj.records:
  if kind not in [0xa0,0xa2]:continue
  q=_Cursor(payload)
  try:index,offset=q.index(),q.word()
  except (OMFError,IndexError)as exc:raise LibraryError('LIDATA16: malformed data header')from exc
  require(index!=0 and index in obj.segments,'undefined/zero data segment index')
  if index!=segment:continue
  require(offset<=seg.length,'record offset exceeds segment')
  encoded=q.take(len(payload)-q.pos);q.finish()
  if kind==0xa0:content=encoded;tree=None;raw_chunks.append((offset,content))
  else:content,tree=decode_blocks(encoded,limit=seg.length-offset);iterated.append((offset,offset+len(content)))
  require(offset+len(content)<=seg.length,'data exceeds selected SEGDEF')
  require(not any(offset<end and start<offset+len(content)for start,end,_ in occupied),'overlapping A0/A2 initialized records')
  occupied.append((offset,offset+len(content),content));writes.append({'record_offset':at,'record_kind':kind,'offset':offset,'size':len(content),'encoded_bytes':len(encoded),'payload_sha256':sha(payload),'expanded_sha256':sha(content),'blocks':tree})
 require(bool(iterated)and seg.unsupported_data,'policy requires actual strict-parser iterated-data marker')
 require(raw_chunks==seg.chunks,'raw LEDATA chunks/records disagree')
 cursor=0;parts=[]
 for start,end,content in sorted(occupied):
  require(start==cursor,'hole in complete initialized contribution');parts.append(content);cursor=end
 require(cursor==seg.length,'incomplete initialized SEGDEF')
 for f in obj.fixups:
  if f.segment!=segment:continue
  require(not any(f.offset<end and start<f.offset+f.width for start,end in iterated),'FIXUPP inside/crossing iterated initialization unsupported')
  owners=[w for w in writes if w['offset']<=f.offset and f.offset+f.width<=w['offset']+w['size']]
  require(len(owners)==1 and owners[0]['record_kind']==0xa0 and owners[0]['record_offset']<f.record_offset,'fixup lacks genuine preceding LEDATA ownership')
 return InitializedView(b''.join(parts),tuple(writes),tuple(iterated))


def link_segment(obj,module):
 """Emit the whole closed authentic DATA80 from raw library records/placements only."""
 validate_profile(module);segment=module['segment'];seg=obj.segments.get(segment);require(seg is not None and(seg.name,seg.class_name,seg.length,seg.attributes)==('_DATA','DATA',80,0x48),'exact declared DATA80 SEGDEF required')
 pubs={n:p.offset for n,p in obj.publics.items()if p.segment==3};require(pubs==module['publics']and all(p.group==1 and p.type_index==0 for p in obj.publics.values()if p.segment==3),'actual whole DATA PUBLIC table mismatch')
 view=initialized_view(obj,segment,policy=module['initialized_record_policy']);require([(w['record_offset'],w['record_kind'],w['offset'],w['size'])for w in view.records]==WANTED_WRITES,'authentic source record ownership mismatch');require(sha(view.data)==SOURCE_SHA,'authentic raw initialized content mismatch')
 fs=sorted((f for f in obj.fixups if f.segment==3),key=lambda f:f.offset)
 require([(f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.record_offset,f.raw.hex())for f in fs]==[(66,2,1,True,(1,1),(0,3),70,569,'c4061001034600'),(68,2,2,True,(1,1),(1,1),None,569,'c808150101')],'exact two genuine DATA FIXUPPs required')
 segments={int(k):_placement(v)for k,v in module['segments'].items()};groups={int(k):_word(v)for k,v in module['groups'].items()};paragraph,base=segments[3];require(base+80<=65536,'whole DATA crosses frame')
 def address(pair):
  method,datum=pair
  if method==0 and datum in segments:return segments[datum]
  if method==1 and datum in groups:return groups[datum],0
  raise LibraryError('LIDATA16: unsupported/unresolved data address')
 out=bytearray(view.data);log=[];used=set()
 for f in fs:
  require(0<=f.offset and f.offset+f.width<=len(out)and not({f.offset,f.offset+1}&used),'fixup extent/overlap');used.update((f.offset,f.offset+1));tp,to=address(f.target);fp=tp if f.frame==(5,None)else address(f.frame)[0];addend=int.from_bytes(out[f.offset:f.offset+2],'little');displacement=0 if f.displacement is None else _word(f.displacement)
  if f.location_type==2:
   require(f.segment_relative and not displacement and f.target[0]==1 and f.frame==f.target,'BASE16 explicit DGROUP target/frame required');value=tp+addend;mode='base16'
  else:
   require(f.location_type==1 and f.segment_relative,'only segment-relative OFFSET16 data location supported');value=tp*16+to+displacement-fp*16+addend;mode='offset16'
  encoded=value&65535;out[f.offset:f.offset+2]=encoded.to_bytes(2,'little');place=paragraph*16+base+f.offset
  log.append({'segment':3,'object_offset':f.offset,'image_offset':place,'mode':mode,'frame':list(f.frame),'target':list(f.target),'target_symbol':None,'target_paragraph':tp,'target_offset':to,'frame_paragraph':fp,'original_addend':addend,'displacement':displacement,'arithmetic_result':value,'encoded_value':encoded,'raw_fixupp':f.raw.hex(),'record_offset':f.record_offset,'mz_relocation_image_offset':place if mode=='base16'else None})
 return bytes(out),log


def describe_input(obj,module):
 validate_profile(module);view=initialized_view(obj,3,policy=POLICY)
 return {'initialized_record_policy':POLICY,'normalization':'Decoded initialized-record view only; original OMF unchanged','source_records':list(view.records),'iterated_ranges':[list(x)for x in view.iterated_ranges],'raw_initialized_sha256':sha(view.data),'literal_initialized_bytes':sum(w['size']for w in view.records if w['record_kind']==0xa0),'iterated_initialized_bytes':sum(w['size']for w in view.records if w['record_kind']==0xa2),'BSS_or_hole_fill_bytes':0,'source_generation_reference_read':False}


def validate_evidence(unit,project,target_sha,reference,linked,fixups):
 """Comparison-only evidence/loader validation, after target-free library emission."""
 from reference import ORIGINAL_SHA256,validate_expanded_read
 validate_unit(unit);require(target_sha==ORIGINAL_SHA256 and reference.get('original_sha256')==ORIGINAL_SHA256,'native comparison identity mismatch');project=Path(project).resolve();items={}
 for name,row in PINS.items():
  path=(project/row['path']).resolve();require(path.is_relative_to(project),'evidence escaped project');raw=path.read_bytes();require(sha(raw)==row['sha256'],'evidence pin mismatch '+name);items[name]=json.loads(raw)
 require(items['worker']['all80_native_bytes_equal']and items['worker']['original_OMF_or_parser_mutated']is False and items['worker']['member']['sha256']==MEMBER_SHA,'closed independent source/native proof mismatch')
 require(items['root']['status']=='PASS source/native/REA80 and exact original single MZ via forward load adjustment'and items['root']['exact_original_MZ_set']==[0x61614],'independent root proof mismatch')
 sites=[f['mz_relocation_image_offset']for f in fixups if f['mz_relocation_image_offset']is not None];require(sites==[0x61614],'whole DATA80 exact emitted MZ set required')
 return validate_expanded_read(items['REA'],unit,linked,reference,emitted_mz_sites=sites)
