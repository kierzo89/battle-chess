"""Fixed original 1296 prompt: two compiler switch dead branches, never masked."""
import hashlib
import json
from extent import _evidence, _number
from reference import build_reference, ORIGINAL_SHA256
START,END,SIZE,NEXT_SIZE=0x11296,0x11446,432,123
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA='d055f62193507b8409cbd47e782832a033388210f352368d04c139dff220ee93'
NEXT_SHA='010ea2d232bc61be030c074b8523422e065e5de4bf206ff1b49b728d7f255f1f'
CFG_SHA='864aa108aca27a14b854084c82b712abfcb5d19107de71be6cacd966374811fa'
NEXT_CFG_SHA='b6fe3e8d5fc2988f987a81558e92f63fab433426c3f8b737d32884a6737ec8cc'
RANGES=[(START,0x11370),(0x11372,0x113be),(0x113c0,END)]
GAPS={0x11370:(0x1136e,0x11387,'eb17','eb15'),0x113be:(0x113bc,0x113d1,'eb13','eb11')}
FIELDS={7:False,33:True,37:False,122:True,142:False,149:True,152:True,155:True,158:True,161:True,175:True,179:False,185:True,188:True,196:True,198:True,204:True,206:True,212:True,214:True,253:True,257:False,274:True,276:True,282:True,284:True,290:True,292:True,327:True,331:False,337:False,408:False,414:False,418:True}

def _hash(b):return hashlib.sha256(b).hexdigest()

def _cfg(e,start,end,ranges,count,digest):
    n=e['normalized_result'];p=n['procedure'];b=p['body']
    if (e['parameters']!={'procedure':hex(start)} or _number(p['address'])!=start
        or b.get('available')is not True or b.get('contains_entry')is not True
        or b.get('non_contiguous')is not(len(ranges)>1)or b.get('span_bytes')!=end-start
        or b.get('total_bytes')!=sum(z-a for a,z in ranges)
        or b.get('ranges')!=[{'start':hex(a),'end':hex(z-1)}for a,z in ranges]):
        raise ValueError('prompt fixed native body/query differs')
    blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(a)for a in q['successors'])))for q in n['basic_blocks'])
    if len(blocks)!=count or _hash(json.dumps(blocks,separators=(',',':')).encode())!=digest:
        raise ValueError('prompt fixed closed CFG differs')
    starts={a for a,_,_ in blocks};coverage=[]
    for a,z,succ in blocks:
        if not start<=a<z<=end or any(t not in starts for t in succ):raise ValueError('prompt CFG not closed')
        if coverage and coverage[-1][1]==a:coverage[-1]=(coverage[-1][0],z)
        else:coverage.append((a,z))
    if coverage!=ranges:raise ValueError('prompt CFG does not cover every retained byte once')
    graph={a:s for a,_,s in blocks};todo=[start];seen=set()
    while todo:
        a=todo.pop()
        if a not in seen:seen.add(a);todo.extend(graph[a])
    if seen!=starts:raise ValueError('prompt CFG includes unreachable claimed block')
    for r in n.get('incoming_references',[]):
        a=_number(r['target_address']);s=_number(r['source_address'])
        if a!=start and not(start<=s<end and a in starts):raise ValueError('prompt extra external interior entry')

def validate_prompt_extent(unit,project,target_sha256,emitted,linked):
    m=unit.get('extended_extent');keys={'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence','preceding_jump_evidence','gap_decoder_evidence'}
    if (not isinstance(m,dict)or set(m)!=keys or m['kind']!='prompt_dead_switches_1296_v1'
        or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='prompt_1296' or unit.get('symbol')!='_prompt_1296'
        or unit.get('language')!='c' or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
        or unit.get('code_address')is not None or _number(unit['image_offset'])!=0x1296 or _number(unit['size'])!=SIZE
        or unit.get('externals',{}).get('__chkstk')!=0xecaa):raise ValueError('unsupported fixed prompt extent identity')
    specs={'raw_span_evidence':('read_bytes',1),'next_entry_evidence':('analyze_function',1),'gap_xref_evidence':('xrefs',4),'preceding_jump_evidence':('inspect_native_instruction',2),'gap_decoder_evidence':('inspect_native_instruction',2)}
    orig=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function');es={};all_e=[orig]
    for key,(op,count)in specs.items():
        paths=m[key]if count>1 else[m[key]]
        if not isinstance(paths,list)or len(paths)!=count:raise ValueError('prompt missing complete independent observations')
        ev=[_evidence(project,p,ORIGINAL_SHA256,op)for p in paths];all_e.extend(ev);es[key]=ev if count>1 else ev[0]
    if (len({e['evidence_id']for e in all_e})!=len(all_e)or any(e['analysis_profile']['digest']!=PROFILE or e['analysis_profile']['parameters'].get('target_format')!='dos-mz'for e in all_e)):
        raise ValueError('prompt requires distinct original DOS-profile observations')
    ref=build_reference((project.parent/'CHESS.EXE').read_bytes());blob=ref['image'][0x1296:0x14c1]
    r=es['raw_span_evidence'];n=r['normalized_result'];raw=bytes.fromhex(n['bytes_hex'])
    if (r['parameters']!={'address':hex(START),'length':555}or _number(n['address'])!=START or n.get('complete')is not True
        or n.get('requested_bytes')!=555 or n.get('returned_bytes')!=555 or len(raw)!=555 or raw!=blob
        or _hash(blob[:SIZE])!=BODY_SHA or _hash(blob[SIZE:])!=NEXT_SHA
        or not isinstance(linked,bytes)or linked!=blob[:SIZE]
        or any(0x1296<=s<0x14c1 for s in ref['relocations'])):raise ValueError('prompt complete original432+next123 or empty MZ set differs')
    _cfg(orig,START,END,RANGES,38,CFG_SHA)
    _cfg(es['next_entry_evidence'],END,END+NEXT_SIZE,[(END,END+NEXT_SIZE)],13,NEXT_CFG_SHA)
    addresses=[a for gap in GAPS for a in[gap,gap+1]]
    for e,a in zip(es['gap_xref_evidence'],addresses):
        if e['parameters']!={'address':hex(a)}or e['normalized_result']!=[]:raise ValueError('prompt all four gap bytes require empty global xrefs')
    for at,(gap,(prev,target,prevhex,gaphex))in enumerate(GAPS.items()):
        for a,h in[(prev,prevhex),(gap,gaphex)]:
            if linked[a-START:a-START+2].hex()!=h or a+2+int.from_bytes(bytes.fromhex(h)[1:],'little',signed=True)!=target:
                raise ValueError('prompt dead branch must duplicate preceding live switch-exit branch')
        e=es['preceding_jump_evidence'][at];n=e['normalized_result']
        if (e['parameters']!={'address':hex(prev)}or _number(n['address'])!=prev or n.get('procedure')!=hex(START)
            or n.get('status')!='decoded'or n.get('bytes')!=prevhex or n.get('length')!=2 or n.get('mnemonic')!='JMP'
            or n['flow'].get('kind')!='jump'or n['flow'].get('conditional')is not False or n['flow'].get('computed')is not False
            or n['flow'].get('direct_destinations')!=[hex(target)]):raise ValueError('prompt independently decoded preceding branch differs')
        e=es['gap_decoder_evidence'][at];n=e['normalized_result']
        if (e['parameters']!={'address':hex(gap)}or _number(n['address'])!=gap or n.get('status')!='undecodable'
            or n.get('bytes')is not None or n.get('length')is not None or n.get('procedure')is not None):raise ValueError('prompt must preserve original undecodable gap observation')
    if (not isinstance(emitted,dict)or emitted.get('symbol')!=unit['symbol']or emitted.get('boundary')!='codeview3_procedure'
        or emitted.get('size')!=SIZE or type(emitted.get('offset'))is not int or emitted['offset']!=0
        or emitted.get('end')!=SIZE or type(emitted.get('segment'))is not int or emitted['segment']<=0
        or not isinstance(emitted.get('fixups'),list)or len(emitted['fixups'])!=34):raise ValueError('prompt requires entire standalone CV432')
    seen=set()
    for f in emitted['fixups']:
        a=f.offset
        if (a not in FIELDS or a in seen or f.segment!=emitted['segment']or f.width!=2 or f.location_type!=1
            or f.segment_relative is not FIELDS[a]or f.frame!=(5,None)or f.target[0]!=2
            or type(f.target[1])is not int or f.target[1]<=0 or(f.displacement or 0)!=0):raise ValueError('prompt requires exact34 external compiler OFFSET16 fields')
        seen.add(a)
    return {'kind':m['kind'],'span_bytes':SIZE,'reachable_body_bytes':428,'closed_cfg_blocks':38,'body_sha256':BODY_SHA,
        'next_complete_body_bytes':NEXT_SIZE,'next_complete_body_sha256':NEXT_SHA,'gap_bytes':4,'gap_addresses':[hex(a)for a in GAPS],
        'compiler_fixups':34,'mz_relocations':[],'compiler_boundary':'codeview3_procedure'}
