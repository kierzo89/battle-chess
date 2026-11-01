"""Fixed260C switch cleanup: original240 reachable + EB11 dead bytes = full242.
No generic extent override, byte editing, or source contribution cropping.
"""
import hashlib,json
from extent import _evidence,_number
TARGET_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA256='4c934daaf46b91a57be7441ad953d20ff1bb5177f16d875c5ec3c697501a2929'
NEXT_SHA256='b4863f3e870ddbea33720180f9dd445d14427168aed14104e31f52de1df827f6'
CFG_SHA256='7b9244bd4f9854fb682fceb3712a506e53f778a89fd26b21437e1ffa7fce2e8a'
START,END,SIZE,NEXT_SIZE,GAP,EPILOGUE,RESUME=0x1260c,0x126fe,242,67,0x12673,0x126f8,0x12686
RANGES=[(START,GAP),(GAP+2,END)]
EXTERNALS={'__chkstk':0xecaa,'_command_cursor_0070':0x70,'_event_tick_0072':0x72,'_flash_rank_b0a3':0xb0a3,'_write_command_fd4e':{'offset':0x15e,'segment':0xfbf},'_refresh_panel_1d51':0x1d51,'_select_pen_5b18':0x5b18,'_position_command_22c5':0x22c5,'_graphics_rect_110d_0003':{'offset':3,'segment':0x110d}}
FIELDS={7:('__chkstk',2,1,False),12:('_flash_rank_b0a3',2,1,True),36:('_command_cursor_0070',2,1,True),49:('_command_cursor_0070',2,1,True),58:('_command_cursor_0070',2,1,True),61:('_write_command_fd4e',4,3,True),69:('_command_cursor_0070',2,1,True),76:('_event_tick_0072',2,1,True),87:('_write_command_fd4e',4,3,True),95:('_command_cursor_0070',2,1,True),98:('_refresh_panel_1d51',2,1,False),155:('_flash_rank_b0a3',2,1,True),168:('_select_pen_5b18',2,1,False),174:('_flash_rank_b0a3',2,1,True),202:('_graphics_rect_110d_0003',4,3,True),225:('_position_command_22c5',2,1,False),234:('_flash_rank_b0a3',2,1,True)}
H=lambda b:hashlib.sha256(b).hexdigest()
def validate_input_dialog_extent(unit,project,target_sha256,emitted,linked,source_object=None):
 meta=unit.get('extended_extent')
 if (target_sha256!=TARGET_SHA256 or unit.get('id')!='input_dialog_260c' or unit.get('symbol')!='_input_dialog_260c' or unit.get('language')!='c' or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi'] or _number(unit.get('image_offset',-1))!=START-0x10000 or _number(unit.get('size',-1))!=SIZE or unit.get('code_address')is not None or unit.get('externals')!=EXTERNALS or not isinstance(meta,dict)or set(meta)!={'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence','gap_decoder_evidence','preceding_jump_evidence'}or meta['kind']!='input_dialog_switch_cleanup_260c_v1' or not isinstance(meta['gap_xref_evidence'],list)or len(meta['gap_xref_evidence'])!=2):
  raise ValueError('unsupported fixed input-dialog identity/metadata/bindings')
 body=_evidence(project,unit['rea_evidence'],target_sha256,'analyze_function');raw=_evidence(project,meta['raw_span_evidence'],target_sha256,'read_bytes');nxt=_evidence(project,meta['next_entry_evidence'],target_sha256,'analyze_function');xrefs=[_evidence(project,p,target_sha256,'xrefs')for p in meta['gap_xref_evidence']];gap=_evidence(project,meta['gap_decoder_evidence'],target_sha256,'inspect_native_instruction');prev=_evidence(project,meta['preceding_jump_evidence'],target_sha256,'inspect_native_instruction');ev=[body,raw,nxt]+xrefs+[gap,prev]
 if len({e['evidence_id']for e in ev})!=7:raise ValueError('input-dialog evidence identities must be distinct')
 for e in ev:
  p=e['analysis_profile'];s=e['subject'];params=p['parameters']
  if p['digest']!=PROFILE or s.get('format')!='dos-mz'or s.get('architecture')!='x86'or e['provider']['id']!='ghidra'or p['provider']['id']!='ghidra'or params.get('target_format')!='dos-mz'or params.get('loader')!='MzLoader'or params.get('address_coordinates')!='linear-byte-offset'or params.get('architecture')!='x86':raise ValueError('input-dialog strict original subject/provider/profile differs')
 for e,params in [(body,{'procedure':hex(START)}),(nxt,{'procedure':hex(END)}),(raw,{'address':hex(START),'length':SIZE+NEXT_SIZE}),(gap,{'address':hex(GAP)}),(prev,{'address':hex(GAP-3)})]:
  if e['parameters']!=params:raise ValueError('input-dialog exact primary parameters differ')
 n=body['normalized_result'];proc=n['procedure'];b=proc['body'];ranges=[(_number(q['start']),_number(q['end'])+1)for q in b['ranges']]
 if not b.get('available')or b.get('contains_entry')is not True or b.get('non_contiguous')is not True or _number(proc['address'])!=START or ranges!=RANGES or b.get('total_bytes')!=240 or b.get('span_bytes')!=SIZE:raise ValueError('input-dialog original240 live/two ranges/242span differ')
 rr=raw['normalized_result'];blob=bytes.fromhex(rr['bytes_hex'])
 if rr.get('complete')is not True or _number(rr['address'])!=START or rr.get('requested_bytes')!=309 or rr.get('returned_bytes')!=309 or len(blob)!=309 or not isinstance(linked,bytes)or len(linked)!=SIZE or blob[:SIZE]!=linked or H(linked)!=BODY_SHA256 or H(blob[SIZE:])!=NEXT_SHA256:raise ValueError('input-dialog full original242 + next67 mismatch')
 np=nxt['normalized_result']['procedure'];nb=np['body']
 if not nb.get('available')or nb.get('contains_entry')is not True or nb.get('non_contiguous')is not False or _number(np['address'])!=END or nb.get('ranges')!=[{'start':hex(END),'end':hex(END+NEXT_SIZE-1)}]or nb.get('span_bytes')!=NEXT_SIZE or nb.get('total_bytes')!=NEXT_SIZE:raise ValueError('input-dialog adjacent next67 boundary differs')
 blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(v)for v in q['successors'])))for q in n['basic_blocks'])
 if len(blocks)!=17 or sum(z-a for a,z,_ in blocks)!=240 or H(json.dumps(blocks,separators=(',',':')).encode())!=CFG_SHA256:raise ValueError('input-dialog exact17-block closed CFG differs')
 starts={a for a,_,_ in blocks};covered=[];current=None
 for a,z,succ in blocks:
  if not START<=a<z<=END or any(v not in starts for v in succ):raise ValueError('input-dialog invalid block or open CFG')
  if current and a==current[1]:current[1]=z
  else:
   if current:covered.append(tuple(current))
   current=[a,z]
 if current:covered.append(tuple(current))
 if covered!=RANGES:raise ValueError('input-dialog CFG coverage includes hole/overlap')
 graph={a:s for a,_,s in blocks};pending=[START];seen=set()
 while pending:
  a=pending.pop()
  if a not in seen:seen.add(a);pending.extend(graph[a])
 if seen!=starts:raise ValueError('input-dialog unreachable claimed live block')
 if sorted(_number(e['parameters']['address'])for e in xrefs)!=[GAP,GAP+1]or any(e['normalized_result']!=[]for e in xrefs):raise ValueError('input-dialog both gap bytes require empty global xrefs')
 if any(_number(ref['target_address'])in(GAP,GAP+1)for ref in n.get('incoming_references',[])):raise ValueError('input-dialog incoming reference enters omitted cleanup')
 g=gap['normalized_result'];p=prev['normalized_result']
 if g.get('status')!='undecodable'or g.get('bytes')is not None or g.get('length')is not None or g.get('flow',{}).get('kind')!='unavailable':raise ValueError('input-dialog original undecodable gap observation differs')
 if p.get('status')!='decoded'or p.get('bytes')!='e98500'or p.get('length')!=3 or p.get('mnemonic')!='JMP'or p.get('flow',{}).get('kind')!='jump'or p['flow'].get('conditional')is not False or p['flow'].get('computed')is not False or p['flow'].get('direct_destinations')!=[hex(EPILOGUE)]:raise ValueError('input-dialog live predecessor must bypass cleanup to epilogue')
 at=GAP-START
 if linked[at-3:at]!=bytes.fromhex('e98500')or linked[at:at+2]!=bytes.fromhex('eb11')or GAP+2+int.from_bytes(linked[at+1:at+2],'little',signed=True)!=RESUME or RESUME not in starts or linked[EPILOGUE-START:]!=bytes.fromhex('5e5f8be55dc3'):raise ValueError('input-dialog raw cleanup/predecessor/target/restoration differs')
 if source_object is None:raise ValueError('input-dialog requires actual whole compiler object')
 alloc=[(i,s.name,s.class_name,s.length,s.attributes)for i,s in source_object.segments.items()if s.length and s.class_name not in('DEBSYM','DEBTYP')]
 if alloc!=[(1,'_TEXT','CODE',SIZE,0x48)]or len(source_object.publics)!=1 or len(source_object.procedures)!=1 or source_object.function_info(unit['symbol'])!=emitted:raise ValueError('input-dialog complete sole WORD CODE242/onePUBLIC/CV differs')
 segment=source_object.segments[1];rawcode=bytearray()
 for offset,data in sorted(segment.chunks):
  if offset!=len(rawcode):raise ValueError('input-dialog CODE hole or overlap')
  rawcode.extend(data)
 if len(rawcode)!=SIZE or segment.unsupported_data:raise ValueError('input-dialog incomplete compiler CODE')
 if (emitted.get('symbol')!=unit['symbol']or emitted.get('boundary')!='codeview3_procedure'or emitted.get('segment')!=1 or emitted.get('offset')!=0 or emitted.get('size')!=SIZE or emitted.get('end')!=SIZE or len(emitted.get('fixups',[]))!=17):raise ValueError('input-dialog full CV242 with17fields required')
 found=set()
 for f in emitted['fixups']:
  a=f.offset
  if a not in FIELDS or a in found:raise ValueError('input-dialog unexpected/duplicate compiler field')
  symbol,width,kind,relative=FIELDS[a]
  if f.segment!=1 or f.width!=width or f.location_type!=kind or f.segment_relative is not relative or f.frame!=(5,None)or f.target[0]!=2 or type(f.target[1])is not int or source_object.externals.get(f.target[1])!=symbol or (f.displacement or 0)!=0 or any(rawcode[a:a+width]):raise ValueError('input-dialog compiler field shape/name/addend differs')
  found.add(a)
 if found!=set(FIELDS):raise ValueError('input-dialog incomplete field ownership')
 if sum(f.segment==1 for f in source_object.fixups)!=17:raise ValueError('input-dialog extra CODE fields')
 return dict(kind=meta['kind'],body_evidence_id=body['evidence_id'],raw_span_evidence_id=raw['evidence_id'],next_entry_evidence_id=nxt['evidence_id'],gap_xref_evidence_ids=[e['evidence_id']for e in xrefs],gap_decoder_evidence_id=gap['evidence_id'],preceding_jump_evidence_id=prev['evidence_id'],span_bytes=SIZE,reachable_body_bytes=240,closed_cfg_blocks=17,gap_address=hex(GAP),gap_hex='eb11',gap_provider_status='undecodable',gap_target=hex(RESUME),live_predecessor_target=hex(EPILOGUE),body_sha256=BODY_SHA256,next_body_sha256=NEXT_SHA256,whole_CODE_SEGDEF=242,compiler_fields=17,FAR16_fields=3,expected_MZ_sites=[0x264b,0x2665,0x26d8],compiler_boundary='codeview3_procedure')
