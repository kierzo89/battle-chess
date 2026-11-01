"""Fixed FD6A:133 live + authentic EB16 gap =135, followed by native90.
Only whole136 standalone or actual four-procedure508 contribution is accepted.
No generic extent override, instruction patching or allocation cropping.
"""
import hashlib,json
from extent import _evidence,_number
from link16 import link_function
TARGET_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA256='25db654c332a480929f935ad64f4d4e7ee95271093a5102a0918c9823fbc6778'
NEXT_SHA256='202fc0223ab6a04987716f46d55f96dbbd345dcebfa1df8d0a620794d65045bd'
PREFIX_SHA256='c803611de6a1c8e110a08a3c1c15c8f18c93716ecc1b81a6e8811ed275d7549c'
CFG_SHA256='850823007a03ecaf4424dba6e9df5eed3b98b08a2b7f051a3918c61f2827003e'
START,END,SIZE,GAP,ZERO,EPILOGUE,NEXT=0x1fd6a,0x1fdf1,135,0x1fdd1,0x1fde9,0x1fded,0x1fdf2
RANGES=[(START,GAP),(GAP+2,END)]
EXTERNALS={'_cursor_column_0086':0x86,'_cursor_row_0088':0x88}
FIELDS={11:'_cursor_row_0088',17:'_cursor_row_0088',26:'_cursor_row_0088',35:'_cursor_column_0086',41:'_cursor_column_0086',49:'_cursor_column_0086',58:'_cursor_row_0088',64:'_cursor_row_0088',72:'_cursor_row_0088',81:'_cursor_column_0086',87:'_cursor_column_0086',96:'_cursor_column_0086'}
PREFIX_BINDINGS={'_board':0xa8ba,'_cells':0x1166,'_kind_map':0xf00,'_row_mask_9230':0x9230,'_command_words_8d2c':0x8d2c}
PREFIX_FIELDS={52:('_board',0),58:('_kind_map',0),113:('_board',1),140:('_board',1),167:('_board',1),191:('_board',1),231:('_cells',0),262:('_row_mask_9230',0),283:('_cells',0),314:('_row_mask_9230',0),332:('_row_mask_9230',0),354:('_command_words_8d2c',160),361:('_command_words_8d2c',0)}
PREFIX=[('_clear_display_fbf6',0,242),('_draw_fce8',242,102),('_write_command_fd4e',344,28)]
H=lambda b:hashlib.sha256(b).hexdigest()
def validate_command_key_extent(unit,project,target_sha256,emitted,linked,source_object=None):
 small=unit.get('flags')==['/AS','/Gs','/Zi']and unit.get('compiler_source_name')is None
 medium=unit.get('flags')==['/AM','/Gs','/Zi']and unit.get('compiler_source_name')=='DISPLAY.C'
 meta=unit.get('extended_extent');keys={'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence','gap_decoder_evidence','preceding_jump_evidence','alignment_observation_evidence','context_prefix_evidence'}
 if target_sha256!=TARGET_SHA256 or unit.get('id')!='command_key_fd6a'or unit.get('symbol')!='_command_key_fd6a'or unit.get('language')!='c'or unit.get('backend')!='msc500-omf'or not(small or medium)or _number(unit.get('image_offset',-1))!=START-0x10000 or _number(unit.get('size',-1))!=SIZE or unit.get('code_address')!={'segment':0xfbf,'offset':0x17a}or unit.get('externals')!=EXTERNALS or not isinstance(meta,dict)or set(meta)!=keys or meta['kind']!='command_key_cleanup_fd6a_v1'or not isinstance(meta['gap_xref_evidence'],list)or len(meta['gap_xref_evidence'])!=2 or not isinstance(meta['context_prefix_evidence'],list)or len(meta['context_prefix_evidence'])!=2:raise ValueError('unsupported fixed command-key identity/metadata/bindings')
 body=_evidence(project,unit['rea_evidence'],target_sha256,'analyze_function');raw=_evidence(project,meta['raw_span_evidence'],target_sha256,'read_bytes');nxt=_evidence(project,meta['next_entry_evidence'],target_sha256,'analyze_function');xrefs=[_evidence(project,p,target_sha256,'xrefs')for p in meta['gap_xref_evidence']];gap=_evidence(project,meta['gap_decoder_evidence'],target_sha256,'inspect_native_instruction');prev=_evidence(project,meta['preceding_jump_evidence'],target_sha256,'inspect_native_instruction');alignment=_evidence(project,meta['alignment_observation_evidence'],target_sha256,'inspect_native_instruction');prefix=[_evidence(project,p,target_sha256,'read_bytes')for p in meta['context_prefix_evidence']];ev=[body,raw,nxt]+xrefs+[gap,prev,alignment]+prefix
 if len({e['evidence_id']for e in ev})!=10:raise ValueError('command-key evidence identities must be distinct')
 for e in ev:
  p=e['analysis_profile'];s=e['subject'];params=p['parameters']
  if p['digest']!=PROFILE or s.get('format')!='dos-mz'or s.get('architecture')!='x86'or e['provider']['id']!='ghidra'or p['provider']['id']!='ghidra'or params.get('target_format')!='dos-mz'or params.get('loader')!='MzLoader'or params.get('address_coordinates')!='linear-byte-offset'or params.get('architecture')!='x86'or params.get('load_segment')!='0x1000'or params.get('language_id')!='x86:LE:16:Real Mode':raise ValueError('command-key strict original subject/provider/profile differs')
 for e,p in [(body,{'procedure':hex(START)}),(raw,{'address':hex(START),'length':162}),(nxt,{'procedure':hex(NEXT)}),(gap,{'address':hex(GAP)}),(prev,{'address':hex(GAP-2)}),(alignment,{'address':hex(END)}),(prefix[0],{'address':'0x1fbf6','length':344}),(prefix[1],{'address':'0x1fd4e','length':163})]:
  if e['parameters']!=p:raise ValueError('command-key exact primary parameters differ')
 n=body['normalized_result'];proc=n['procedure'];b=proc['body'];ranges=[(_number(q['start']),_number(q['end'])+1)for q in b['ranges']]
 if not b.get('available')or b.get('contains_entry')is not True or b.get('non_contiguous')is not True or _number(proc['address'])!=START or ranges!=RANGES or b.get('total_bytes')!=133 or b.get('span_bytes')!=SIZE:raise ValueError('command-key original133/two ranges/135 differs')
 rr=raw['normalized_result'];blob=bytes.fromhex(rr['bytes_hex'])
 if rr.get('complete')is not True or _number(rr['address'])!=START or rr.get('requested_bytes')!=162 or rr.get('returned_bytes')!=162 or len(blob)!=162 or not isinstance(linked,bytes)or len(linked)!=SIZE or linked!=blob[:SIZE]or H(linked)!=BODY_SHA256 or blob[135]!=0x90 or H(blob[136:])!=NEXT_SHA256:raise ValueError('command-key full135/native90/next26 differs')
 np=nxt['normalized_result']['procedure'];nb=np['body']
 if not nb.get('available')or nb.get('contains_entry')is not True or nb.get('non_contiguous')is not False or _number(np['address'])!=NEXT or nb.get('ranges')!=[{'start':hex(NEXT),'end':hex(NEXT+25)}]or nb.get('total_bytes')!=26 or nb.get('span_bytes')!=26:raise ValueError('command-key true next26 boundary differs')
 blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(v)for v in q['successors'])))for q in n['basic_blocks'])
 if len(blocks)!=24 or sum(z-a for a,z,_ in blocks)!=133 or H(json.dumps(blocks,separators=(',',':')).encode())!=CFG_SHA256:raise ValueError('command-key exact24-block CFG differs')
 starts={a for a,_,_ in blocks};coverage=[]
 for a,z,succ in blocks:
  if not START<=a<z<=END or any(v not in starts for v in succ):raise ValueError('command-key open CFG/invalidblock')
  if coverage and a==coverage[-1][1]:coverage[-1][1]=z
  else:coverage.append([a,z])
 if [tuple(q)for q in coverage]!=RANGES:raise ValueError('command-key livecoverage hole/overlap differs')
 pending=[START];seen=set();graph={a:s for a,_,s in blocks}
 while pending:
  a=pending.pop()
  if a not in seen:seen.add(a);pending.extend(graph[a])
 if seen!=starts:raise ValueError('command-key claimed block unreachable')
 if sorted(_number(e['parameters']['address'])for e in xrefs)!=[GAP,GAP+1]or any(e['normalized_result']!=[]for e in xrefs):raise ValueError('command-key both omittedbytes need empty globalxrefs')
 if any(_number(q['target_address'])in(GAP,GAP+1)for q in n.get('incoming_references',[])):raise ValueError('command-key reference enters omittedgap')
 for e in(gap,alignment):
  g=e['normalized_result']
  if g.get('status')!='undecodable'or g.get('bytes')is not None or g.get('length')is not None or g.get('flow',{}).get('kind')!='unavailable':raise ValueError('command-key provider knowledge must remain undecodable')
 p=prev['normalized_result']
 if p.get('status')!='decoded'or p.get('bytes')!='eb1c'or p.get('length')!=2 or p.get('mnemonic')!='JMP'or p.get('flow',{}).get('kind')!='jump'or p['flow'].get('conditional')is not False or p['flow'].get('computed')is not False or p['flow'].get('direct_destinations')!=[hex(EPILOGUE)]:raise ValueError('command-key live predecessor bypass differs')
 at=GAP-START
 if linked[at-2:at+2]!=bytes.fromhex('eb1ceb16')or GAP+2+int.from_bytes(linked[at+1:at+2],'little',signed=True)!=ZERO or ZERO not in starts or linked[ZERO-START:EPILOGUE-START]!=bytes.fromhex('2bc0eb00')or linked[EPILOGUE-START:]!=bytes.fromhex('8be55dcb'):raise ValueError('command-key raw omittedjump/zero-return/restore differs')
 # Authenticate the real adjacent372 prefix independently even for standalone136.
 pb=[]
 for e,length,address in zip(prefix,(344,163),(0x1fbf6,0x1fd4e)):
  q=e['normalized_result'];data=bytes.fromhex(q['bytes_hex'])
  if q.get('complete')is not True or _number(q['address'])!=address or q.get('requested_bytes')!=length or q.get('returned_bytes')!=length or len(data)!=length:raise ValueError('command-key incomplete prefixcontext primary')
  pb.append(data)
 if pb[1][28:]!=linked:raise ValueError('command-key independent adjacent raw135 differs')
 prefixbytes=pb[0]+pb[1][:28]
 if H(prefixbytes)!=PREFIX_SHA256:raise ValueError('command-key fixed372 nativeprefix differs')
 if source_object is None:raise ValueError('command-key actualwholeobject required')
 if any(k in(0xb0,0xb8,0xa2)for k,_,_ in source_object.records):raise ValueError('command-key communal/iteratedallocations forbidden')
 off=emitted.get('offset');size=136 if off==0 else 508 if off==372 else None
 alloc=[(k,s.name,s.class_name,s.length,s.attributes)for k,s in source_object.segments.items()if s.length and s.class_name not in('DEBSYM','DEBTYP')]
 if size is None or(medium and off!=372)or alloc!=[(1,'DISPLAY_TEXT'if medium else'_TEXT','CODE',size,0x48)]or source_object.function_info(unit['symbol'])!=emitted:raise ValueError('command-key only complete136 or authentic508 CODE context allowed')
 rawcode=bytearray();segment=source_object.segments[1]
 for at,data in sorted(segment.chunks):
  if at!=len(rawcode):raise ValueError('command-key CODEhole/overlap')
  rawcode.extend(data)
 if len(rawcode)!=size or segment.unsupported_data or rawcode[-1:]!=b'\x90':raise ValueError('command-key actualnative90/allCODE required')
 expected=PREFIX+[(unit['symbol'],372,135)]if off else[(unit['symbol'],0,135)]
 if len(source_object.publics)!=len(expected)or len(source_object.procedures)!=len(expected)or set(source_object.publics)!={q[0]for q in expected}:raise ValueError('command-key exactcontext PUBLIC/CV union differs')
 for symbol,a,z in expected:
  q=source_object.function_info(symbol);pub=source_object.publics[symbol]
  if(q['offset'],q['size'],q['end'],q['segment'],q['boundary'])!=(a,z,a+z,1,'codeview3_procedure')or(pub.segment,pub.offset)!=(1,a):raise ValueError('command-key context CV/PUBLIC ownership differs')
 if emitted.get('symbol')!=unit['symbol']or emitted.get('size')!=135 or emitted.get('end')!=off+135 or len(emitted.get('fixups',[]))!=12:raise ValueError('command-key whole135CV/12fields required')
 found=set()
 for f in emitted['fixups']:
  a=f.offset-off
  if a not in FIELDS or a in found or f.segment!=1 or f.width!=2 or f.location_type!=1 or not f.segment_relative or f.frame!=(5,None)or f.target[0]!=2 or source_object.externals.get(f.target[1])!=FIELDS[a]or(f.displacement or 0)!=0 or any(rawcode[f.offset:f.offset+2]):raise ValueError('command-key exactcompilerfield ownership/shape differs')
  found.add(a)
 if found!=set(FIELDS):raise ValueError('command-key field missing')
 if off:
  fullprefix=bytearray()
  for symbol,a,z in PREFIX:
   data,_=link_function(source_object,symbol,0xfbf6+a,PREFIX_BINDINGS);fullprefix.extend(data)
  if bytes(fullprefix)!=prefixbytes:raise ValueError('command-key wholeactual372 prefix mismatch')
  pf=[f for f in source_object.fixups if f.segment==1 and f.offset<off]
  if len(pf)!=13 or {f.offset for f in pf}!=set(PREFIX_FIELDS):raise ValueError('command-key authenticprefix13DSfields required')
  for f in pf:
   symbol,addend=PREFIX_FIELDS[f.offset]
   if f.width!=2 or f.location_type!=1 or not f.segment_relative or f.frame!=(5,None)or f.target[0]!=2 or source_object.externals.get(f.target[1])!=symbol or(f.displacement or 0)!=0 or int.from_bytes(rawcode[f.offset:f.offset+2],'little')!=addend:raise ValueError('command-key exactprefix field/name/addend differs')
 if sum(f.segment==1 for f in source_object.fixups)!=(25 if off else 12):raise ValueError('command-key unowned CODEfield')
 return dict(kind=meta['kind'],span_bytes=135,reachable_body_bytes=133,closed_cfg_blocks=24,gap_hex='eb16',gap_target=hex(ZERO),live_predecessor_target=hex(EPILOGUE),gap_provider_status='undecodable',actual_native_alignment_hex='90',alignment_provider_status='undecodable',whole_CODE_SEGDEF=size,compiler_fields=12,expected_MZ_sites=[],body_sha256=BODY_SHA256,next_body_sha256=NEXT_SHA256,evidence_ids=[e['evidence_id']for e in ev])
