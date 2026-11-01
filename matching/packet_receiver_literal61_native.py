"""Fixed DDD3 receiver:412 reachable + EB0C dead bytes in closed CODE714 or856.
Only the explicitly authenticated three- or six-procedure routes are admitted. No generic span,
standalone odd-origin414, frame/capacity override or copied instruction emission.
"""
import hashlib,json
from extent import _evidence,_number
from link16 import link_function
TARGET_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA256='7bd710905b77f3541ef11b16eaf888d49b3d794e05ee7c0047c84b9e6bdb82d3'
NEXT_SHA256='d097009b0f91a1bd539e737ccb5a4665781fb8e035306e535885d1fa5d1d4cad'
CFG_SHA256='a23b7d3d0fe0ee317d7a3c3610b919b490345bdb2423206bca3e7428dabfb16e'
WHOLE_SHA256='f3a00fb3793216cdeec93f830e55f82e1f0f4608cd27a7f692558c8e728a2d99'
FOLLOWING_RAW_SHA256='e8891148fcad807e360d57125c19d16d1341aaff76fdc393e86483977ba93c67'
START,END,SIZE,GAP,RESUME,EPILOGUE=0x1ddd3,0x1df71,414,0x1dec0,0x1dece,0x1df6b
ORIGIN=0xdce2
RANGES=[(START,GAP),(GAP+2,END)]
EXTERNALS={'__chkstk':0xecaa,'_input_reset_state':0x2ec0,'_refresh_stop_11a6':0x11a6,'_read_bytes_dbe3':0xdbe3,'_available_bytes_dc91':0xdc91,'_write_bytes_dbb5':0xdbb5,'_discard_bytes_dc7f':0xdc7f,'_prompt_1296':0x1296}
CONTEXT_BINDINGS=dict(EXTERNALS,_receive_packet_ddd3=0xddd3,_packet_error_51b4=0x51b4,_packet_retry_error_51da=0x51da,_modes=0x53c,_pack_board_8cfa=0x8cfa)
PROCS=[('_send_packet_dce2',0,241),('_receive_packet_ddd3',241,414),('_reset_df71',655,59)]
# Exact compiler field ownership: offset:(external name, segment-relative, raw addend).
FIELDS={7:('__chkstk',False,0),80:('_write_bytes_dbb5',False,0),94:('_write_bytes_dbb5',False,0),106:('_receive_packet_ddd3',False,0),133:('_write_bytes_dbb5',False,0),153:('_write_bytes_dbb5',False,0),167:('_write_bytes_dbb5',False,0),187:('_packet_error_51b4',True,0),191:('_prompt_1296',False,0),226:('_packet_retry_error_51da',True,0),230:('_prompt_1296',False,0),248:('__chkstk',False,0),266:('_read_bytes_dbe3',False,0),298:('_read_bytes_dbe3',False,0),338:('_read_bytes_dbe3',False,0),425:('_refresh_stop_11a6',True,0),432:('_input_reset_state',True,0),466:('_write_bytes_dbb5',False,0),493:('_available_bytes_dc91',False,0),507:('_discard_bytes_dc7f',False,0),511:('_input_reset_state',True,0),517:('_discard_bytes_dc7f',False,0),555:('_read_bytes_dbe3',False,0),608:('_prompt_1296',False,0),614:('_available_bytes_dc91',False,0),628:('_discard_bytes_dc7f',False,0),632:('_input_reset_state',True,0),662:('__chkstk',False,0),667:('_modes',True,0),674:('_modes',True,2),694:('_pack_board_8cfa',False,0)}
WHOLE856_SHA256='64d977cca6f6817510aa92f0f07af7ca9d5f8a3599ee1691b3967e7948bf28e5'
TAIL203_SHA256='7fd8512da8d2e460acf94ca68eb1b905edd4dadfd73dcd937b124acab79b5659'
PROCS856=PROCS+[('_record_dfac',714,55),('_record_kind_dfe3',769,44),('_input_reset_e00f',813,42)]
FIELDS856=dict(FIELDS,**{})
FIELDS856.update({721:('__chkstk',False,0),776:('__chkstk',False,0),820:('__chkstk',False,0),841:('_write_bytes_dbb5',False,0),848:('_input_reset_state',True,0)})
H=lambda b:hashlib.sha256(b).hexdigest()
def _read(e,address,size):
 n=e['normalized_result'];b=bytes.fromhex(n['bytes_hex'])
 if e['parameters']!={'address':hex(address),'length':size}or _number(n['address'])!=address or n.get('complete')is not True or n.get('requested_bytes')!=size or n.get('returned_bytes')!=size or len(b)!=size:raise ValueError('packet receiver complete exact raw context required')
 return b

def _ordinary_native(e,address,size):
 p=e['normalized_result']['procedure'];b=p['body']
 if e['parameters']!={'procedure':hex(address)}or _number(p['address'])!=address or b.get('available')is not True or b.get('contains_entry')is not True or b.get('non_contiguous')is not False or b.get('total_bytes')!=size or b.get('span_bytes')!=size or b.get('ranges')!=[{'start':hex(address),'end':hex(address+size-1)}]:raise ValueError('packet receiver context original procedure boundary differs')


def validate_native(unit,project,target_sha256,emitted,linked):
 m=unit.get('extended_extent');large=isinstance(m,dict)and m.get('context_kind')=='packet856_v1'
 keys={'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence','gap_decoder_evidence','preceding_jump_evidence','context_span_evidence','context_entry_evidence','following_entry_evidence','following_span_evidence'}
 if large:keys|={'context_kind','extended_context_evidence','kind_wrapper_evidence','input_reset_evidence','huff_next_evidence'}
 if target_sha256!=TARGET_SHA256 or unit.get('id')!='receive_packet_ddd3'or unit.get('symbol')!='_receive_packet_ddd3'or unit.get('language')!='c'or unit.get('backend')!='msc500-packet-owned-literals61-omf-v1'or unit.get('flags')!=['/AS','/Zi']or unit.get('compiler_source_name')is not None or unit.get('code_address')is not None or _number(unit.get('image_offset',-1))!=0xddd3 or _number(unit.get('size',-1))!=414 or unit.get('externals')!=EXTERNALS or not isinstance(m,dict)or set(m)!=keys or m['kind']!='packet_receive_switch_cleanup_ddd3_v1'or not isinstance(m['gap_xref_evidence'],list)or len(m['gap_xref_evidence'])!=2:raise ValueError('unsupported fixed packet receiver identity/metadata/bindings')
 body=_evidence(project,unit['rea_evidence'],target_sha256,'analyze_function');raw=_evidence(project,m['raw_span_evidence'],target_sha256,'read_bytes');nxt=_evidence(project,m['next_entry_evidence'],target_sha256,'analyze_function');xs=[_evidence(project,p,target_sha256,'xrefs')for p in m['gap_xref_evidence']];gap=_evidence(project,m['gap_decoder_evidence'],target_sha256,'inspect_native_instruction');prev=_evidence(project,m['preceding_jump_evidence'],target_sha256,'inspect_native_instruction');context=_evidence(project,m['context_span_evidence'],target_sha256,'read_bytes');sender=_evidence(project,m['context_entry_evidence'],target_sha256,'analyze_function');following=_evidence(project,m['following_entry_evidence'],target_sha256,'analyze_function');tail=_evidence(project,m['following_span_evidence'],target_sha256,'read_bytes');all_e=[body,raw,nxt,*xs,gap,prev,context,sender,following,tail]
 if large:
  extra=_evidence(project,m['extended_context_evidence'],target_sha256,'read_bytes');kind=_evidence(project,m['kind_wrapper_evidence'],target_sha256,'analyze_function');reset=_evidence(project,m['input_reset_evidence'],target_sha256,'analyze_function');huff=_evidence(project,m['huff_next_evidence'],target_sha256,'analyze_function');all_e.extend([extra,kind,reset,huff])
 if len({e['evidence_id']for e in all_e})!=(15 if large else 11):raise ValueError('packet receiver requires distinct primary IDs for the explicit714/856 route')
 for e in all_e:
  p=e['analysis_profile'];s=e['subject'];q=p['parameters']
  if p['digest']!=PROFILE or s.get('format')!='dos-mz'or s.get('architecture')!='x86'or e['provider']['id']!='ghidra'or p['provider']['id']!='ghidra'or q.get('target_format')!='dos-mz'or q.get('loader')!='MzLoader'or q.get('address_coordinates')!='linear-byte-offset'or q.get('architecture')!='x86'or q.get('load_segment')!='0x1000'or q.get('language_id')!='x86:LE:16:Real Mode':raise ValueError('packet receiver strict original subject/provider/profile differs')
 if body['parameters']!={'procedure':hex(START)}or gap['parameters']!={'address':hex(GAP)}or prev['parameters']!={'address':hex(GAP-3)}:raise ValueError('packet receiver exact original query parameters differ')
 n=body['normalized_result'];p=n['procedure'];b=p['body'];ranges=[(_number(q['start']),_number(q['end'])+1)for q in b['ranges']]
 if _number(p['address'])!=START or b.get('available')is not True or b.get('contains_entry')is not True or b.get('non_contiguous')is not True or b.get('total_bytes')!=412 or b.get('span_bytes')!=414 or ranges!=RANGES:raise ValueError('packet receiver exact412live/414span/two ranges differ')
 blob=_read(raw,START,473);prefix=_read(context,0x1dce2,655);following_bytes=_read(tail,END,180)
 if not isinstance(linked,bytes)or len(linked)!=SIZE or linked!=blob[:SIZE]or H(linked)!=BODY_SHA256 or H(blob[SIZE:])!=NEXT_SHA256 or prefix[241:]!=linked or following_bytes[:59]!=blob[414:]or H(following_bytes)!=FOLLOWING_RAW_SHA256:raise ValueError('packet receiver full414/reset59/context655/next raw mismatch')
 whole=prefix+blob[414:]
 if len(whole)!=714 or H(whole)!=WHOLE_SHA256:raise ValueError('packet receiver authenticated complete714 differs')
 _ordinary_native(sender,0x1dce2,241);_ordinary_native(nxt,END,59);_ordinary_native(following,0x1dfac,55)
 if large:
  extension=_read(extra,0x1dfac,203)
  if H(extension)!=TAIL203_SHA256 or extension[:59]!=following_bytes[59:118]:raise ValueError('packet receiver full203 extension/overlap differs')
  whole=whole+extension[:142]
  if len(whole)!=856 or H(whole)!=WHOLE856_SHA256 or whole[-1:]!=b'\x90':raise ValueError('packet receiver explicit whole856/native90 differs')
  _ordinary_native(kind,0x1dfe3,44);_ordinary_native(reset,0x1e00f,42);_ordinary_native(huff,0x1e03a,61)
 procs=PROCS856 if large else PROCS;fieldmap=FIELDS856 if large else FIELDS;total=856 if large else 714
 blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(v)for v in q['successors'])))for q in n['basic_blocks'])
 if len(blocks)!=57 or sum(z-a for a,z,_ in blocks)!=412 or H(json.dumps(blocks,separators=(',',':')).encode())!=CFG_SHA256:raise ValueError('packet receiver exact57block/412live CFG differs')
 starts={a for a,_,_ in blocks};merged=[]
 for a,z,succ in blocks:
  if not START<=a<z<=END or any(v not in starts for v in succ):raise ValueError('packet receiver open or invalid CFG')
  if merged and a==merged[-1][1]:merged[-1][1]=z
  else:merged.append([a,z])
 if [tuple(q)for q in merged]!=RANGES:raise ValueError('packet receiver CFG hole/overlap coverage differs')
 graph={a:s for a,_,s in blocks};pending=[START];seen=set()
 while pending:
  a=pending.pop()
  if a not in seen:seen.add(a);pending.extend(graph[a])
 if seen!=starts:raise ValueError('packet receiver claimed liveblock unreachable')
 if sorted(_number(e['parameters']['address'])for e in xs)!=[GAP,GAP+1]or any(e['normalized_result']!=[]for e in xs)or any(_number(q['target_address'])in(GAP,GAP+1)for q in n.get('incoming_references',[])):raise ValueError('packet receiver both gapbytes require empty global refs')
 g=gap['normalized_result'];v=prev['normalized_result']
 if g.get('status')!='undecodable'or g.get('bytes')is not None or g.get('length')is not None or g.get('flow',{}).get('kind')!='unavailable':raise ValueError('packet receiver gap knowledge must remain undecodable')
 if v.get('status')!='decoded'or v.get('bytes')!='e9ab00'or v.get('length')!=3 or v.get('mnemonic')!='JMP'or v.get('flow',{}).get('kind')!='jump'or v['flow'].get('conditional')is not False or v['flow'].get('computed')is not False or v['flow'].get('direct_destinations')!=[hex(EPILOGUE)]:raise ValueError('packet receiver live predecessor bypass differs')
 at=GAP-START
 if linked[at-3:at+2]!=bytes.fromhex('e9ab00eb0c')or GAP+2+int.from_bytes(linked[at+1:at+2],'little',signed=True)!=RESUME or RESUME not in starts or linked[EPILOGUE-START:]!=bytes.fromhex('5e5f8be55dc3'):raise ValueError('packet receiver raw deadjump/target/restore differs')
 return {'receiver_live':412,'receiver_span':414,'closed_CFG_blocks':57,'dead_jump':'eb0c','evidence_ids':[e['evidence_id']for e in all_e],'compiler_allocation_validation_role':'separate exact new3886 profile and whole856 native comparison; old native-only body predicates unchanged'}
