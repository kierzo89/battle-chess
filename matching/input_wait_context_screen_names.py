"""Fixed source-owned2322 CODE and four real compiler-resolved refresh calls.

No synthetic FIXUPP records or callable-name-only ownership assertions.
"""
import hashlib,json
from pathlib import Path
from omf import OMFObject
from link16 import link_function
from extent import _evidence
from reference import ORIGINAL_SHA256,CARRIER_SHA256
from input_wait_context_specs_screen_names import LAYOUT,FIELDS,BINDINGS
from input_wait_native_specs import NATIVE,CONTEXT_SHA,REFRESH_SHA
BASE=0x1cfa
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'

def _hash(b):return hashlib.sha256(b).hexdigest()

def native(e,basename,closed=False):
 s=NATIVE[basename];n=e['normalized_result'];p=n['procedure'];b=p['body']
 if e['parameters']!=s['query']or p['address']!=s['address']or b!=s['body']:raise ValueError('input-wait fixed native body/query differs')
 blocks=sorted((int(q['start'],0),int(q['end'],0),tuple(sorted(int(a,0)for a in q['successors'])))for q in n['basic_blocks'])
 if len(blocks)!=s['CFG_count']or _hash(json.dumps(blocks,separators=(',',':')).encode())!=s['CFG_sha256']:raise ValueError('input-wait fixed native CFG differs')
 if closed:
  starts={a for a,z,succ in blocks};parts=[]
  for a,z,succ in blocks:
   if a>=z or any(t not in starts for t in succ):raise ValueError('input-wait CFG not closed')
   if parts and a==parts[-1][1]:parts[-1]=(parts[-1][0],z)
   else:parts.append((a,z))
  expected=[(int(r['start'],0),int(r['end'],0)+1)for r in b['ranges']]
  if parts!=expected:raise ValueError('input-wait CFG does not partition complete retained ranges')
  graph={a:s for a,z,s in blocks};todo=[int(p['address'],0)];seen=set()
  while todo:
   a=todo.pop()
   if a not in seen:seen.add(a);todo.extend(graph[a])
  if seen!=starts:raise ValueError('input-wait unreachable claimed CFG block')
  for r in n.get('incoming_references',[]):
   target=int(r['target_address'],0);source=int(r['source_address'],0)
   if target!=int(p['address'],0)and not any(a<=source<z and target in starts for a,z in expected):raise ValueError('input-wait external interior entry')
 return blocks

def _profile(e):
 p=e['analysis_profile'];d=p['parameters']
 if p['digest']!=PROFILE or d.get('target_format')!='dos-mz':raise ValueError('input-wait fixed DOS profile differs')

def _raw(e,address,size,want):
 n=e['normalized_result']
 if (e['parameters']!={'address':hex(address),'length':size}or n.get('address')!=hex(address)
     or n.get('complete')is not True or n.get('requested_bytes')!=size or n.get('returned_bytes')!=size
     or bytes.fromhex(n['bytes_hex'])!=want or len(want)!=size):raise ValueError('input-wait complete original/expanded raw context differs')

def validate_source_context(unit,project,emitted,linked,obj,ref):
 if not isinstance(obj,OMFObject):raise ValueError('input-wait/board coupled extent requires the actual fresh OMF object')
 if emitted!=obj.function_info(unit['symbol']):raise ValueError('input-wait emitted CV/fixups differ from actual source-owned object')
 expected_names={s for s,a,n in LAYOUT}
 if set(obj.publics)!=expected_names or set(obj.procedures)!=expected_names:raise ValueError('input-wait requires exactly nine matching genuine source CODE PUBLIC/CV definitions')
 seg=obj.segments.get(1)
 if seg is None or(seg.name,seg.class_name,seg.attributes,seg.length)!=('_TEXT','CODE',0x48,2322):raise ValueError('input-wait complete source CODE2322/WORD allocation differs')
 if set(obj.segments)!={1,2,3,4,5,6}:raise ValueError('input-wait requires only the six canonical MSC segments')
 for index,name,kind in[(2,'_DATA','DATA'),(3,'CONST','CONST'),(4,'_BSS','BSS')]:
  s=obj.segments[index]
  if(s.index,s.name,s.class_name,s.attributes,s.length)!=(index,name,kind,0x48,0)or s.chunks or s.unsupported_data:raise ValueError('input-wait canonical empty DATA/CONST/BSS storage differs')
 for index,name,kind in[(5,'$$SYMBOLS','DEBSYM'),(6,'$$TYPES','DEBTYP')]:
  s=obj.segments[index]
  if(s.index,s.name,s.class_name,s.attributes)!=(index,name,kind,0x20)or s.unsupported_data:raise ValueError('input-wait canonical CodeView segment identity differs')
 raw=bytearray()
 for at,b in sorted(seg.chunks):
  if not b or at!=len(raw):raise ValueError('input-wait complete CODE has a hole/overlap')
  raw.extend(b)
 if len(raw)!=2322 or seg.unsupported_data:raise ValueError('input-wait incomplete or iterated CODE allocation')
 codefixups=[f for f in obj.fixups if f.segment==1]
 if len(codefixups)!=199:raise ValueError('input-wait actual CODE field set differs from199')
 linked_context=bytearray();logs=[];field_bytes=set();raw_audit=[]
 for symbol,at,size in LAYOUT:
  info=obj.function_info(symbol);p=obj.publics[symbol]
  if(info['boundary']!='codeview3_procedure'or info['offset']!=at or info['size']!=size or info['end']!=at+size or info['segment']!=1 or(p.segment,p.offset,p.group)!=(1,at,0)):raise ValueError('input-wait independent PUBLIC/CV layout differs')
  expected=FIELDS[symbol];seen=set()
  for f in info['fixups']:
   if not isinstance(f.target,tuple)or len(f.target)!=2 or type(f.target[1])is not int or f.target[1]<=0:raise ValueError('input-wait invalid compiler external target')
   rel=f.offset-at;name=obj.externals.get(f.target[1]);shape=(f.width,f.location_type,f.segment_relative,f.frame,name,f.displacement or 0,bytes(raw[f.offset:f.offset+f.width]).hex())
   if(f.segment!=1 or f.target[0]!=2 or rel not in expected or rel in seen or shape!=expected[rel]
      or not at<=f.offset<f.offset+f.width<=at+size or field_bytes.intersection(range(f.offset,f.offset+f.width))):raise ValueError('input-wait exact actual compiler field ownership differs')
   if not any(k==0x9c and loc==f.record_offset and f.raw and f.raw in payload for k,loc,payload in obj.records):raise ValueError('input-wait compiler field lacks actual raw FIXUPP record')
   field_bytes.update(range(f.offset,f.offset+f.width));seen.add(rel)
   if symbol==unit['symbol']and unit.get('externals',{}).get(name)!=BINDINGS[name]:raise ValueError('input-wait canonical external binding differs')
   raw_audit.append({'symbol':symbol,'relative':rel,'target':name,'raw_FIXUPP':f.raw.hex()})
  if seen!=set(expected):raise ValueError('input-wait missing actual compiler field')
  body,fixups=link_function(obj,symbol,BASE+at,BINDINGS);linked_context.extend(body);logs.extend(fixups)
 if len(raw_audit)!=199 or len(linked_context)!=2322 or _hash(linked_context)!=CONTEXT_SHA or linked_context!=ref['image'][BASE:0x260c]:raise ValueError('input-wait freshly linked complete source context differs')
 # Independent raw field arithmetic resolves every compiler-owned field.
 manual=bytearray(raw);mz=[]
 for f in codefixups:
  target=BINDINGS[obj.externals[f.target[1]]];at=f.offset;add=int.from_bytes(raw[at:at+2],'little')+(f.displacement or 0)
  if f.location_type==3:
   value=target['offset']+add;sg=target['segment']+int.from_bytes(raw[at+2:at+4],'little');manual[at+2:at+4]=(sg&65535).to_bytes(2,'little');mz.append(BASE+at+2)
  elif f.location_type==2:value=target['segment']+add;mz.append(BASE+at)
  else:
   value=(target.get('absolute',target.get('offset'))if isinstance(target,dict)else target)+add
   if not f.segment_relative:value-=BASE+at+2
  manual[at:at+2]=(value&65535).to_bytes(2,'little')
 original_mz=sorted(s for s in ref['relocations']if BASE<=s<0x260c)
 if manual!=linked_context or sorted(mz)!=original_mz or len(mz)!=26:raise ValueError('input-wait all raw fields or full original26MZ differ')
 # Authenticate the actually defined refresh88, not merely a PUBLIC name.
 e=_evidence(project,'evidence/rea_low_control_refresh_panel_1d51.json',ORIGINAL_SHA256,'analyze_function');_profile(e);native(e,'rea_low_control_refresh_panel_1d51.json',True)
 refresh_evidence_id=e['evidence_id']
 refresh=bytes(linked_context[87:175])
 if _hash(refresh)!=REFRESH_SHA or {s for s in mz if 0x1d51<=s<0x1da9}!={0x1d9c}:raise ValueError('input-wait actual source-owned refresh88/MZ differs')
 calls=[]
 for symbol,rels in[('_input_wait_1da9',[120,266]),('_board_action_20d5',[274,411])]:
  info=obj.function_info(symbol)
  for relative in rels:
   at=info['offset']+relative
   if raw[at-1]!=0xe8 or field_bytes.intersection([at,at+1]):raise ValueError('input-wait real internal CALL has an invented relocation or wrong opcode')
   disp=int.from_bytes(raw[at:at+2],'little',signed=True)
   if at+2+disp!=87 or bytes(raw[at-1:at+2])!=ref['image'][BASE+at-1:BASE+at+2]or BASE+at+2+disp!=0x1d51:raise ValueError('input-wait internal CALL bytes/destination do not reach actual refresh definition')
   calls.append({'caller':symbol,'relative_operand':relative,'raw_CALL_hex':raw[at-1:at+2].hex(),'source_PUBLIC':87,'target_image':0x1d51,'actual_fixup_present':False})
 # Whole native original and independently loader-relocated expanded2322.
 all_e=[refresh_evidence_id]
 for which,sha in[('original',ORIGINAL_SHA256),('expanded',CARRIER_SHA256)]:
  e=_evidence(project,'evidence/rea_input_wait_command_full_2322_'+which+'.json',sha,'read_bytes');_profile(e);want=bytearray(linked_context)
  if which=='expanded':
   for site in mz:off=site-BASE;want[off:off+2]=((int.from_bytes(want[off:off+2],'little')+0x1000)&65535).to_bytes(2,'little')
  _raw(e,BASE+0x10000,2322,bytes(want));all_e.append(e['evidence_id'])
 if len(set(all_e))!=3:raise ValueError('input-wait requires distinct original/expanded context primaries')
 loads=[]
 for load in[0,1,0x1234,0xee10]:
  actual=bytearray(manual);expected=bytearray(ref['image'][BASE:0x260c])
  for array in[actual,expected]:
   for site in mz:off=site-BASE;array[off:off+2]=((int.from_bytes(array[off:off+2],'little')+load)&65535).to_bytes(2,'little')
  if actual!=expected:raise ValueError('input-wait complete source context load-base equality differs')
  loads.append({'load_paragraph':load,'complete2322_exact':True,'sha256':_hash(actual)})
 return {'four_load_bases':loads,'whole_source_CODE_bytes':2322,'actual_raw_fixups':199,'complete_MZ_sites':sorted(mz),'actual_refresh_PUBLIC':87,'actual_refresh_CV_size':88,'real_internal_CALLs':calls,'raw_context_evidence_ids':all_e,'fresh_source_owned_context':True}
