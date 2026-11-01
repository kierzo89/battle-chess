"""Fixed 1917/1C77 native switch gaps, verified over full fresh C extents.

Two decoder-omitted short breaks remain ordinary compiler output. This gate
never alters code, infers sizes from a requested slice, or grants layout credit.
"""
import hashlib,json
from extent import _evidence,_number
from reference import build_reference,ORIGINAL_SHA256
START,CONTROL,END,NEXT_END=0x11917,0x11c77,0x11cfa,0x11d51
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
SPECS={
 'handle_input_1917':dict(start=START,end=CONTROL,size=864,offset=0,body_sha='6c0df762bc1cf6b3404aebd54255214a31720b7fdecd236d347f466d50242f5d',cfg_sha='51690c166b0cb397ab3255280d0d8c86ece4525e88fcdeb716497ca68c89af8e',blocks=73,ranges=[(START,0x11c14),(0x11c16,CONTROL)],mz={0x19bb,0x1a0a,0x1a94,0x1acf,0x1ae9,0x1b13,0x1b5b,0x1baa,0x1c3f,0x1c51}),
 'input_control_1c77':dict(start=CONTROL,end=END,size=131,offset=864,body_sha='778ce4349c97fd7cdcbcf2bba2ee1bf2bd15b40144ad345817cf1f697681088c',cfg_sha='81b0b5b37feedb62d61c9c5cb3cc248a925dda5640c6905ffb2f82c0557a61f1',blocks=16,ranges=[(CONTROL,0x11cb7),(0x11cb9,END)],mz={0x1cb3,0x1cee})}
NEXT_SHA='927028373849ccbe481f670e0ac0e6411bdd5947a3813868e43b906d8f2e8792'
NEXT_CFG='4db0bda713be3e3d85fa0a7ba1b935eb5418d4a5ecd2318eafc867051776ef00'
# (preceding unconditional branch, omitted short break, respective destinations)
GAPS=[(0x11c12,'eb1d',0x11c31,0x11c14,'eb1b',0x11c31,START),
      (0x11cb5,'eb3f',0x11cf6,0x11cb7,'eb20',0x11cd9,CONTROL)]
FIELDS={'handle_input_1917': {6: (2, 1, False), 756: (2, 1, True), 745: (2, 1, True), 734: (2, 1, True), 723: (2, 1, True), 712: (2, 1, True), 701: (2, 1, True), 682: (2, 1, True), 672: (2, 1, True), 665: (2, 1, True), 657: (4, 3, True), 654: (2, 1, True), 645: (2, 1, True), 618: (2, 1, False), 612: (2, 1, False), 606: (2, 1, True), 599: (2, 1, True), 586: (2, 1, True), 578: (4, 3, True), 567: (2, 1, True), 562: (2, 1, True), 555: (2, 1, False), 537: (2, 1, False), 524: (2, 1, True), 518: (2, 1, True), 514: (2, 1, True), 506: (4, 3, True), 495: (2, 1, True), 490: (2, 1, True), 483: (2, 1, False), 472: (2, 1, True), 464: (4, 3, True), 453: (2, 1, True), 446: (2, 1, True), 438: (4, 3, True), 435: (2, 1, True), 426: (2, 1, True), 413: (2, 1, True), 403: (2, 1, True), 387: (2, 1, True), 379: (4, 3, True), 376: (2, 1, True), 367: (2, 1, True), 354: (2, 1, True), 347: (2, 1, True), 344: (2, 1, True), 337: (2, 1, True), 334: (2, 1, True), 315: (2, 1, False), 312: (2, 1, True), 298: (2, 1, True), 249: (2, 1, True), 241: (4, 3, True), 238: (2, 1, True), 229: (2, 1, True), 216: (2, 1, True), 210: (2, 1, True), 191: (2, 1, True), 184: (2, 1, True), 177: (2, 1, True), 170: (2, 1, True), 162: (4, 3, True), 159: (2, 1, True), 148: (2, 1, True), 131: (2, 1, True), 124: (2, 1, True), 80: (2, 1, False), 69: (2, 1, True), 59: (2, 1, False), 48: (2, 1, True), 38: (2, 1, False), 27: (2, 1, True), 853: (2, 1, False), 843: (2, 1, False), 837: (2, 1, True), 824: (4, 3, True), 814: (2, 1, True), 806: (4, 3, True), 796: (2, 1, True)}, 'input_control_1c77': {6: (2, 1, False), 125: (2, 1, True), 117: (4, 3, True), 114: (2, 1, True), 107: (2, 1, True), 58: (4, 3, True), 10: (2, 1, True)}}
def _sha(b):return hashlib.sha256(b).hexdigest()
def _cfg(e,start,end,ranges,blocks,digest):
 n=e['normalized_result'];p=n['procedure'];b=p['body']
 if (e['parameters']!={'procedure':hex(start)} or _number(p['address'])!=start
     or b.get('available')is not True or b.get('contains_entry')is not True
     or b.get('non_contiguous')is not(len(ranges)>1) or b.get('span_bytes')!=end-start
     or b.get('total_bytes')!=sum(z-a for a,z in ranges)
     or b.get('ranges')!=[dict(start=hex(a),end=hex(z-1))for a,z in ranges]):raise ValueError('keyboard native body/query differs')
 rows=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(a)for a in q['successors'])))for q in n['basic_blocks'])
 if len(rows)!=blocks or _sha(json.dumps(rows,separators=(',',':')).encode())!=digest:raise ValueError('keyboard closed CFG differs')
 starts={a for a,_,_ in rows};covered=[]
 for a,z,s in rows:
  if not start<=a<z<=end or any(t not in starts for t in s):raise ValueError('keyboard CFG escapes body')
  if covered and covered[-1][1]==a:covered[-1]=(covered[-1][0],z)
  else:covered.append((a,z))
 if covered!=ranges:raise ValueError('keyboard CFG lacks exact retained-byte partition')
 graph={a:s for a,_,s in rows};todo=[start];seen=set()
 while todo:
  a=todo.pop()
  if a not in seen:seen.add(a);todo.extend(graph[a])
 if seen!=starts:raise ValueError('keyboard retained CFG contains unreachable block')
 for r in n.get('incoming_references',[]):
  a=_number(r['target_address']);s=_number(r['source_address'])
  if a!=start and not(start<=s<end and a in starts):raise ValueError('keyboard extra external interior entry')
 return starts

def validate_keyboard_extent(unit,project,target_sha256,emitted,linked):
 m=unit.get('extended_extent');keys={'kind','raw_span_evidence','peer_body_evidence','next_entry_evidence','gap_xref_evidence','preceding_jump_evidence','gap_decoder_evidence'}
 spec=SPECS.get(unit.get('id'))
 if (not spec or not isinstance(m,dict) or set(m)!=keys or m['kind']!='keyboard_switches_1917_v1'
     or target_sha256!=ORIGINAL_SHA256 or unit.get('symbol')!='_'+unit['id']
     or unit.get('language')!='c' or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
     or unit.get('code_address')is not None or any(unit.get(k)is not None for k in ['owned_const','owned_data','owned_bss'])
     or _number(unit['image_offset'])!=spec['start']-0x10000 or unit.get('size')!=spec['size']
     or unit.get('externals',{}).get('__chkstk')!=0xecaa):raise ValueError('unsupported fixed keyboard unit identity')
 own=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function');evs=[own];es={}
 ops={'raw_span_evidence':('read_bytes',1),'peer_body_evidence':('analyze_function',1),'next_entry_evidence':('analyze_function',1),'gap_xref_evidence':('xrefs',4),'preceding_jump_evidence':('inspect_native_instruction',2),'gap_decoder_evidence':('inspect_native_instruction',2)}
 for key,(op,count)in ops.items():
  paths=m[key]if count>1 else[m[key]]
  if not isinstance(paths,list) or len(paths)!=count:raise ValueError('keyboard requires complete independent observations')
  xs=[_evidence(project,p,ORIGINAL_SHA256,op)for p in paths];evs.extend(xs);es[key]=xs if count>1 else xs[0]
 if len({e['evidence_id']for e in evs})!=len(evs) or any(e['analysis_profile']['digest']!=PROFILE or e['analysis_profile']['parameters'].get('target_format')!='dos-mz' for e in evs):raise ValueError('keyboard original profile/identities differ')
 ref=build_reference((project.parent/'CHESS.EXE').read_bytes());blob=ref['image'][START-0x10000:NEXT_END-0x10000]
 e=es['raw_span_evidence'];n=e['normalized_result'];raw=bytes.fromhex(n['bytes_hex'])
 if (e['parameters']!={'address':hex(START),'length':1082} or _number(n['address'])!=START or n.get('complete')is not True or n.get('requested_bytes')!=1082 or n.get('returned_bytes')!=1082 or raw!=blob):raise ValueError('keyboard complete original context differs')
 bodies={unit['id']:own,next(k for k in SPECS if k!=unit['id']):es['peer_body_evidence']};starts={}
 for key,s in SPECS.items():
  if _sha(blob[s['start']-START:s['end']-START])!=s['body_sha']:raise ValueError('keyboard native body hash differs')
  starts[s['start']]=_cfg(bodies[key],s['start'],s['end'],s['ranges'],s['blocks'],s['cfg_sha'])
 starts[END]=_cfg(es['next_entry_evidence'],END,NEXT_END,[(END,NEXT_END)],8,NEXT_CFG)
 if _sha(blob[END-START:])!=NEXT_SHA:raise ValueError('keyboard adjacent complete87 differs')
 addresses=[a for _,_,_,gap,_,_,_ in GAPS for a in [gap,gap+1]]
 for e,a in zip(es['gap_xref_evidence'],addresses):
  if e['parameters']!={'address':hex(a)} or e['normalized_result']!=[]:raise ValueError('keyboard all four gap bytes need empty global xrefs')
 for i,(prev,ph,pt,gap,gh,gt,owner)in enumerate(GAPS):
  for a,h,t in [(prev,ph,pt),(gap,gh,gt)]:
   if blob[a-START:a-START+2].hex()!=h or a+2+int.from_bytes(bytes.fromhex(h)[1:],'little',signed=True)!=t or t not in starts[owner]:raise ValueError('keyboard short branch has wrong bytes/destination')
  e=es['preceding_jump_evidence'][i];n=e['normalized_result'];f=n['flow']
  if (e['parameters']!={'address':hex(prev)} or _number(n['address'])!=prev or n.get('procedure')!=hex(owner) or n.get('status')!='decoded' or n.get('bytes')!=ph or n.get('length')!=2 or n.get('mnemonic')!='JMP' or f.get('kind')!='jump' or f.get('conditional')is not False or f.get('computed')is not False or f.get('direct_destinations')!=[hex(pt)]):raise ValueError('keyboard preceding independently decoded jump differs')
  e=es['gap_decoder_evidence'][i];n=e['normalized_result']
  if (e['parameters']!={'address':hex(gap)} or _number(n['address'])!=gap or n.get('status')!='undecodable' or n.get('bytes')is not None or n.get('length')is not None or n.get('procedure')is not None):raise ValueError('keyboard original unknown decoder result changed')
 if (not isinstance(linked,bytes) or linked!=blob[spec['start']-START:spec['end']-START]
     or {s for s in ref['relocations'] if spec['start']-0x10000<=s<spec['end']-0x10000}!=spec['mz']):raise ValueError('keyboard complete linked bytes/MZ differ')
 if (not isinstance(emitted,dict) or emitted.get('symbol')!=unit['symbol'] or emitted.get('boundary')!='codeview3_procedure' or emitted.get('size')!=spec['size'] or emitted.get('offset')!=spec['offset'] or emitted.get('end')!=spec['offset']+spec['size'] or type(emitted.get('segment'))is not int or emitted['segment']<=0 or not isinstance(emitted.get('fixups'),list) or len(emitted['fixups'])!=len(FIELDS[unit['id']])):raise ValueError('keyboard requires full independent compiler extent at reviewed context offset')
 seen=set()
 for f in emitted['fixups']:
  a=f.offset-spec['offset']
  if (a not in FIELDS[unit['id']] or a in seen or f.segment!=emitted['segment'] or (f.width,f.location_type,f.segment_relative)!=FIELDS[unit['id']][a] or f.frame!=(5,None) or f.target[0]!=2 or type(f.target[1])is not int or f.target[1]<=0 or(f.displacement or 0)!=0):raise ValueError('keyboard actual compiler relocation differs')
  seen.add(a)
 return dict(kind=m['kind'],span_bytes=spec['size'],reachable_body_bytes=spec['size']-2,closed_cfg_blocks=spec['blocks'],body_sha256=spec['body_sha'],peer_complete_span_bytes=995-spec['size'],next_complete_body_bytes=87,all_context_gap_bytes=4,compiler_fixups=len(seen),mz_relocations=sorted(spec['mz']),compiler_boundary='codeview3_procedure',source_context_alignment_proved=False)
