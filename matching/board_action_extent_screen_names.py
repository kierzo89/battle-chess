"""Fixed20D5 C extent: two dead breaks plus a native final state-clear.

The five-byte clear is authenticated, unreferenced and compiler-owned; its
provider decoder remains unknown. No other dead statement or span qualifies.
"""
import hashlib
import json
from extent import _evidence, _number
from reference import build_reference, ORIGINAL_SHA256
START,END,SIZE,NEXT_SIZE=0x120d5,0x122c5,496,60
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA='f972fbe418b4bce5d274a6f46e3eea13774750302b15293e758a2a247a55706e'
PREVIOUS_SHA='a4661a39f77faeb895df03bb2c67526185a7c85a976ab62332b6393bae64e4d8'
NEXT_SHA='a08230085e6b7e61203af4e7fdc12290c147cc33b5410408a81620cf682fa731'
CFG_SHA='78e5bbfec3d512932e08705145ccccd26c9b0fe899eb09531023df63f0df41ea'
NEXT_CFG_SHA='d80d6e642c40f92376501818aef426c350d90b91473ec43b7ed781dbdf9ec43f'
RANGES=[(START,0x121f7),(0x121f9,0x1229e),(0x122a0,0x122ba),(0x122bf,END)]
GAPS=[0x121f7,0x121f8,0x1229e,0x1229f,*range(0x122ba,0x122bf)]
BRANCHES=[(0x121f4,'e9c800',0x122bf),(0x1229c,'eb19',0x122b7),(0x122b7,'e954fe',0x1210e)]
CLEAR_HEX='c606560000'
FIELDS={7,18,22,26,36,42,48,52,59,76,98,134,156,162,170,174,181,189,202,214,218,225,233,237,244,268,274,278,284,359,375,382,400,408,411,415,421,446,487}
RELATIVE={7,22,52,98,134,268,274,359,375,411,446}
MZ={0x2267}

def _hash(b):return hashlib.sha256(b).hexdigest()

def _cfg(e,start,end,ranges,count,digest):
 n=e['normalized_result'];p=n['procedure'];b=p['body']
 if (e['parameters']!={'procedure':hex(start)}or _number(p['address'])!=start
     or b.get('available')is not True or b.get('contains_entry')is not True
     or b.get('non_contiguous')is not(len(ranges)>1)or b.get('span_bytes')!=end-start
     or b.get('total_bytes')!=sum(z-a for a,z in ranges)
     or b.get('ranges')!=[{'start':hex(a),'end':hex(z-1)}for a,z in ranges]):raise ValueError('board-action fixed native body/query differs')
 blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(a)for a in q['successors'])))for q in n['basic_blocks'])
 if len(blocks)!=count or _hash(json.dumps(blocks,separators=(',',':')).encode())!=digest:raise ValueError('board-action fixed closed CFG differs')
 starts={a for a,_,_ in blocks};coverage=[]
 for a,z,succ in blocks:
  if not start<=a<z<=end or any(t not in starts for t in succ):raise ValueError('board-action CFG not closed')
  if coverage and coverage[-1][1]==a:coverage[-1]=(coverage[-1][0],z)
  else:coverage.append((a,z))
 if coverage!=ranges:raise ValueError('board-action CFG lacks exact retained-byte partition')
 graph={a:s for a,_,s in blocks};todo=[start];seen=set()
 while todo:
  a=todo.pop()
  if a not in seen:seen.add(a);todo.extend(graph[a])
 if seen!=starts:raise ValueError('board-action unreachable claimed block')
 for r in n.get('incoming_references',[]):
  a=_number(r['target_address']);s=_number(r['source_address'])
  if a!=start and not(start<=s<end and a in starts):raise ValueError('board-action extra external interior entry')

def validate_board_action_extent(unit,project,target_sha256,emitted,linked,source_object=None):
 m=unit.get('extended_extent');keys={'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence','preceding_jump_evidence','gap_decoder_evidence','live_cleanup_evidence'}
 if (not isinstance(m,dict)or set(m)!=keys or m['kind']!='board_action_screen_names_20d5_v2'
     or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='board_action_20d5'or unit.get('symbol')!='_board_action_20d5'
     or unit.get('language')!='c'or unit.get('backend')!='msc500-omf'or unit.get('flags')!=['/AS','/Zi']
     or unit.get('code_address')is not None or _number(unit['image_offset'])!=0x20d5 or _number(unit['size'])!=SIZE
     or unit.get('externals',{}).get('__chkstk')!=0xecaa or unit['externals'].get('_board_action_active_0056')!=0x56):raise ValueError('unsupported fixed board-action extent identity')
 specs={'raw_span_evidence':('read_bytes',1),'next_entry_evidence':('analyze_function',1),'gap_xref_evidence':('xrefs',9),'preceding_jump_evidence':('inspect_native_instruction',3),'gap_decoder_evidence':('inspect_native_instruction',3),'live_cleanup_evidence':('inspect_native_instruction',2)}
 orig=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function');es={};all_e=[orig]
 for key,(op,count)in specs.items():
  paths=m[key]if count>1 else[m[key]]
  if not isinstance(paths,list)or len(paths)!=count:raise ValueError('board-action requires all fixed independent observations')
  ev=[_evidence(project,p,ORIGINAL_SHA256,op)for p in paths];all_e.extend(ev);es[key]=ev if count>1 else ev[0]
 if (len({e['evidence_id']for e in all_e})!=len(all_e)or any(e['analysis_profile']['digest']!=PROFILE or e['analysis_profile']['parameters'].get('target_format')!='dos-mz'for e in all_e)):raise ValueError('board-action requires distinct fixed original DOS observations')
 ref=build_reference((project.parent/'CHESS.EXE').read_bytes());blob=ref['image'][0x2079:0x2301];r=es['raw_span_evidence'];n=r['normalized_result'];raw=bytes.fromhex(n['bytes_hex'])
 if (r['parameters']!={'address':'0x12079','length':648}or _number(n['address'])!=0x12079 or n.get('complete')is not True
     or n.get('requested_bytes')!=648 or n.get('returned_bytes')!=648 or len(raw)!=648 or raw!=blob
     or _hash(blob[:92])!=PREVIOUS_SHA or _hash(blob[92:588])!=BODY_SHA or _hash(blob[588:])!=NEXT_SHA
     or not isinstance(linked,bytes)or linked!=blob[92:588]
     or {s for s in ref['relocations']if 0x2079<=s<0x2301}!={0x2090,0x20a4,0x20b8,0x20cc,0x2267,0x22f5}):raise ValueError('board-action original whole648/context/MZ or full496 bytes differ')
 _cfg(orig,START,END,RANGES,49,CFG_SHA)
 _cfg(es['next_entry_evidence'],END,END+NEXT_SIZE,[(END,END+NEXT_SIZE)],1,NEXT_CFG_SHA)
 for e,a in zip(es['gap_xref_evidence'],GAPS):
  if e['parameters']!={'address':hex(a)}or e['normalized_result']!=[]:raise ValueError('board-action all nine omitted bytes require empty global xrefs')
 for e,(a,h,target)in zip(es['preceding_jump_evidence'],BRANCHES):
  n=e['normalized_result'];width=len(bytes.fromhex(h))
  if (e['parameters']!={'address':hex(a)}or _number(n['address'])!=a or n.get('procedure')!=hex(START)
      or n.get('status')!='decoded'or n.get('bytes')!=h or n.get('length')!=width or n.get('mnemonic')!='JMP'
      or n['flow'].get('kind')!='jump'or n['flow'].get('conditional')is not False or n['flow'].get('computed')is not False
      or n['flow'].get('direct_destinations')!=[hex(target)]or linked[a-START:a-START+width].hex()!=h
      or a+width+int.from_bytes(bytes.fromhex(h)[1:],'little',signed=True)!=target):raise ValueError('board-action preceding decoded jump differs')
 for a,h,target in[(0x121f7,'eb25',0x1221e),(0x1229e,'eb17',0x122b7)]:
  if linked[a-START:a-START+2].hex()!=h or a+2+int.from_bytes(bytes.fromhex(h)[1:],'little',signed=True)!=target:raise ValueError('board-action exact dead switch break differs')
 for e,a in zip(es['gap_decoder_evidence'],[0x121f7,0x1229e,0x122ba]):
  n=e['normalized_result']
  if (e['parameters']!={'address':hex(a)}or _number(n['address'])!=a or n.get('status')!='undecodable'
      or n.get('bytes')is not None or n.get('length')is not None or n.get('procedure')is not None):raise ValueError('board-action must preserve original unknown dead-gap decodes')
 for e,a in zip(es['live_cleanup_evidence'],[0x121ef,0x12278]):
  n=e['normalized_result']
  if (e['parameters']!={'address':hex(a)}or _number(n['address'])!=a or n.get('procedure')!=hex(START)
      or n.get('status')!='decoded'or n.get('bytes')!=CLEAR_HEX or n.get('length')!=5 or n.get('mnemonic')!='MOV'
      or n['flow'].get('kind')!='fallthrough'or n['flow'].get('direct_destinations')!=[]
      or linked[a-START:a-START+5].hex()!=CLEAR_HEX):raise ValueError('board-action both independently decoded live state clears required')
 if linked[0x122ba-START:0x122bf-START].hex()!=CLEAR_HEX or linked[0x122bf-START:].hex()!='5e5f8be55dc3':raise ValueError('board-action unreachable final cleanup or complete epilogue differs')
 coupled=isinstance(emitted,dict)and emitted.get('offset')==987
 source_proof=None
 if coupled:
  from input_wait_context_screen_names import validate_source_context
  source_proof=validate_source_context(unit,project,emitted,linked,source_object,ref)
 expected_fields=FIELDS-{274,411}if coupled else FIELDS
 expected_count=37 if coupled else 39
 if (not isinstance(emitted,dict)or emitted.get('symbol')!=unit['symbol']or emitted.get('boundary')!='codeview3_procedure'
     or emitted.get('size')!=SIZE or type(emitted.get('offset'))is not int or emitted['offset']not in({987}if coupled else{0,92,205})
     or emitted.get('end')!=emitted['offset']+SIZE or type(emitted.get('segment'))is not int or emitted['segment']<=0
     or not isinstance(emitted.get('fixups'),list)or len(emitted['fixups'])!=expected_count):raise ValueError('board-action requires full CV496 at reviewed classic offset or authenticated coupled987')
 seen=set();mz=set();clear_targets=[]
 for f in emitted['fixups']:
  a=f.offset-emitted['offset'];far=a==400
  if (a not in expected_fields or a in seen or f.segment!=emitted['segment']or f.width!=(4 if far else 2)or f.location_type!=(3 if far else 1)
      or f.segment_relative is not(a not in RELATIVE)or f.frame!=(5,None)or f.target[0]!=2
      or type(f.target[1])is not int or f.target[1]<=0 or(f.displacement or 0)!=0):raise ValueError('board-action compiler external fields differ from reviewed context')
  seen.add(a)
  if far:mz.add(0x20d5+a+2)
  if a in{284,421,487}:clear_targets.append(f.target)
 if mz!=MZ or len(clear_targets)!=3 or len(set(clear_targets))!=1:raise ValueError('board-action full MZ set or real cleanup external-symbol ownership differs')
 return {'kind':m['kind'],'span_bytes':SIZE,'reachable_body_bytes':487,'closed_cfg_blocks':49,'body_sha256':BODY_SHA,'gap_bytes':9,
     'dead_switch_branch_bytes':4,'dead_cleanup_bytes':5,'next_complete_body_bytes':NEXT_SIZE,'next_complete_body_sha256':NEXT_SHA,
     'compiler_fixups':expected_count,'mz_relocations':sorted(MZ),'compiler_boundary':'codeview3_procedure'} | ({'source_owned_context':source_proof}if coupled else{})
