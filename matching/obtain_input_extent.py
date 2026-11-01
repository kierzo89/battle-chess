"""Fixed0254 source extent:145 native blocks plus seven dead compiler jumps.

Full original1439+next75 bytes, all15 gap-byte global xrefs, native closed CFG,
actual preceding terminating instructions, explicit unknown gap decodes and
fresh full CV/fixup/linked output are mandatory. No general body extension.
"""
import hashlib
import json
from extent import _evidence, _number
from reference import build_reference, ORIGINAL_SHA256
START,END,SIZE,NEXT_SIZE=0x10254,0x107f3,1439,75
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA='2432bdd2e49be5fe9d753bed31505d9b0c70e175706480b87fc42482907a80e7'
NEXT_SHA='da9e5ccd7ba4132b9cdeefc7c2e90227cf35baf471631548cf0ba967a5017f0f'
CFG_SHA='446e04f517f75f5cf2f578c37c566cb3bafc155fb589684cda7b077b79a2bef8'
NEXT_CFG_SHA='1e99820a73b0290d3fe508efd636ebb97c4c8ec14373fa95d8909b95de312656'
RANGES=[(0x10254,0x10393),(0x10395,0x1048e),(0x10490,0x104e5),(0x104e8,0x10711),
        (0x10713,0x1073b),(0x1073d,0x1079c),(0x1079e,0x107c0),(0x107c2,0x107f3)]
# gap start:(fixed bytes, destination, preceding live jump start, its bytes, destination)
GAPS={0x10393:('eb11',0x103a6,0x10391,'eb13',0x103a6),
      0x1048e:('eb55',0x104e5,0x1048b,'e95f03',0x107ed),
      0x104e5:('e90103',0x107e9,0x104e2,'e90803',0x107ed),
      0x10711:('eb03',0x10716,0x1070e,'e9dc00',0x107ed),
      0x1073b:('eb35',0x10772,0x10738,'e9b200',0x107ed),
      0x1079c:('eb14',0x107b2,0x1079a,'eb16',0x107b2),
      0x107c0:('eb27',0x107e9,0x107be,'eb29',0x107e9)}
INTERIOR_TARGETS={0x10716:('eb0c',0x10724),0x10772:('eb05',0x10779)}
MZ_SITES={0x2dc,0x2fa,0x443,0x697}
NEXT_MZ_SITES={0x816,0x829,0x82e}
FIELDS={'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence',
        'gap_decoder_evidence','preceding_jump_evidence','interior_target_evidence'}
# Relative fields of fresh reconstructed C objects, not unavailable original OMF.
FIXUPS={7: (2, 1, False), 15: (2, 1, True), 25: (2, 1, False), 34: (2, 1, True), 44: (2, 1, False), 53: (2, 1, True), 60: (2, 1, True), 66: (2, 1, True), 73: (2, 1, True), 83: (2, 1, False), 95: (2, 1, False), 107: (2, 1, False), 114: (2, 1, True), 121: (2, 1, True), 128: (2, 1, True), 134: (4, 3, True), 140: (2, 1, True), 144: (2, 1, True), 151: (2, 1, True), 158: (2, 1, True), 164: (4, 3, True), 170: (2, 1, True), 174: (2, 1, True), 181: (2, 1, True), 191: (2, 1, True), 201: (2, 1, True), 211: (2, 1, True), 217: (2, 1, False), 228: (2, 1, False), 244: (2, 1, True), 250: (2, 1, True), 254: (2, 1, True), 258: (2, 1, False), 274: (2, 1, True), 303: (2, 1, True), 312: (2, 1, True), 315: (2, 1, False), 340: (2, 1, True), 347: (2, 1, True), 353: (2, 1, True), 360: (2, 1, True), 366: (2, 1, True), 371: (2, 1, True), 374: (2, 1, True), 377: (2, 1, True), 381: (2, 1, True), 384: (2, 1, False), 393: (2, 1, True), 403: (2, 1, True), 407: (2, 1, False), 420: (2, 1, False), 430: (2, 1, True), 434: (2, 1, False), 443: (2, 1, True), 450: (2, 1, True), 461: (2, 1, False), 464: (2, 1, False), 467: (2, 1, True), 478: (2, 1, True), 484: (2, 1, True), 490: (2, 1, True), 493: (4, 3, True), 502: (2, 1, True), 508: (2, 1, True), 522: (2, 1, True), 529: (2, 1, True), 536: (2, 1, True), 543: (2, 1, True), 550: (2, 1, True), 557: (2, 1, True), 560: (2, 1, False), 573: (2, 1, False), 602: (2, 1, True), 608: (2, 1, True), 614: (2, 1, True), 620: (2, 1, True), 629: (2, 1, True), 637: (2, 1, True), 649: (2, 1, True), 662: (2, 1, True), 669: (2, 1, True), 679: (2, 1, True), 688: (2, 1, True), 694: (2, 1, True), 698: (2, 1, False), 708: (2, 1, True), 711: (2, 1, True), 715: (2, 1, True), 722: (2, 1, True), 727: (2, 1, True), 730: (2, 1, True), 738: (2, 1, True), 741: (2, 1, False), 748: (2, 1, True), 755: (2, 1, True), 759: (2, 1, True), 762: (2, 1, False), 768: (2, 1, False), 774: (2, 1, True), 781: (2, 1, True), 787: (2, 1, True), 794: (2, 1, True), 801: (2, 1, True), 808: (2, 1, True), 815: (2, 1, True), 819: (2, 1, True), 822: (2, 1, False), 829: (2, 1, True), 836: (2, 1, True), 842: (2, 1, False), 845: (2, 1, True), 849: (2, 1, True), 856: (2, 1, True), 862: (2, 1, True), 865: (2, 1, True), 869: (2, 1, True), 876: (2, 1, True), 883: (2, 1, True), 887: (2, 1, False), 891: (2, 1, True), 901: (2, 1, True), 910: (2, 1, True), 916: (2, 1, True), 920: (2, 1, False), 930: (2, 1, False), 936: (2, 1, False), 940: (2, 1, True), 944: (2, 1, True), 947: (2, 1, False), 954: (2, 1, True), 960: (2, 1, True), 965: (2, 1, True), 972: (2, 1, True), 978: (2, 1, True), 981: (2, 1, True), 985: (2, 1, True), 992: (2, 1, True), 998: (2, 1, True), 1002: (2, 1, False), 1008: (2, 1, True), 1020: (2, 1, False), 1032: (2, 1, True), 1039: (2, 1, True), 1043: (2, 1, True), 1049: (2, 1, False), 1055: (2, 1, True), 1089: (4, 3, True), 1101: (2, 1, True), 1111: (2, 1, True), 1121: (2, 1, True), 1129: (2, 1, True), 1137: (2, 1, True), 1143: (2, 1, True), 1154: (2, 1, True), 1163: (2, 1, True), 1166: (2, 1, True), 1177: (2, 1, True), 1186: (2, 1, True), 1189: (2, 1, False), 1193: (2, 1, True), 1202: (2, 1, False), 1216: (2, 1, False), 1221: (2, 1, True), 1225: (2, 1, True), 1230: (2, 1, False), 1236: (2, 1, True), 1244: (2, 1, True), 1258: (2, 1, True), 1269: (2, 1, True), 1279: (2, 1, False), 1290: (2, 1, True), 1293: (2, 1, False), 1299: (2, 1, True), 1302: (2, 1, True), 1306: (2, 1, True), 1321: (2, 1, True), 1328: (2, 1, True), 1333: (2, 1, True), 1347: (2, 1, True), 1378: (2, 1, True), 1384: (2, 1, False)}


def _hash(data):return hashlib.sha256(data).hexdigest()


def _native(e,start,ranges,total,span,count,digest):
    n=e['normalized_result'];p=n['procedure'];b=p['body']
    if (e['parameters']!={'procedure':hex(start)} or _number(p['address'])!=start
            or b.get('available')is not True or b.get('contains_entry')is not True
            or b.get('non_contiguous')is not(len(ranges)>1)
            or b.get('ranges')!=[{'start':hex(a),'end':hex(z-1)}for a,z in ranges]
            or b.get('total_bytes')!=total or b.get('span_bytes')!=span):
        raise ValueError('obtain_input native body or adjacent extent differs')
    blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(x)for x in q['successors'])))for q in n['basic_blocks'])
    if len(blocks)!=count or _hash(json.dumps(blocks,separators=(',',':')).encode())!=digest:
        raise ValueError('obtain_input requires exact independently retained native CFG')
    starts={a for a,_,_ in blocks};merged=[]
    for a,z,succ in blocks:
        if not start<=a<z<=start+span or any(t not in starts for t in succ):
            raise ValueError('obtain_input native CFG must be closed')
        if merged and a==merged[-1][1]:merged[-1]=(merged[-1][0],z)
        else:merged.append((a,z))
    if merged!=ranges or sum(z-a for a,z,_ in blocks)!=total:
        raise ValueError('obtain_input CFG must cover each retained byte once and no gap')
    graph={a:s for a,_,s in blocks};pending=[start];seen=set()
    while pending:
        a=pending.pop()
        if a not in seen:seen.add(a);pending.extend(graph[a])
    if seen!=starts:raise ValueError('obtain_input claimed CFG blocks are unreachable')
    return n,blocks,starts


def _branch(address,blob):
    if (len(blob)==2 and blob[0]==0xeb)or(len(blob)==3 and blob[0]==0xe9):
        return address+len(blob)+int.from_bytes(blob[1:],'little',signed=True)
    raise ValueError('obtain_input gap must be complete fixed unconditional branch')


def validate_obtain_input_extent(unit,project,target_sha256,emitted,linked):
    m=unit.get('extended_extent')
    if (not isinstance(m,dict)or set(m)!=FIELDS or m.get('kind')!='obtain_input_dead_branches_0254_v1'
            or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='obtain_input_0254'
            or unit.get('symbol')!='_obtain_input'or unit.get('language')!='c'
            or unit.get('backend')!='msc500-omf'or unit.get('flags')!=['/AS','/Zi']
            or _number(unit['image_offset'])!=0x254 or _number(unit['size'])!=SIZE
            or unit.get('code_address')is not None or unit.get('externals',{}).get('__chkstk')!=0xecaa
            or any(not isinstance(m[k],list)or len(m[k])!=length for k,length in
                [('gap_xref_evidence',15),('gap_decoder_evidence',7),('preceding_jump_evidence',7),('interior_target_evidence',2)])):
        raise ValueError('unsupported fixed obtain_input0254 extent identity')
    body=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function')
    raw=_evidence(project,m['raw_span_evidence'],ORIGINAL_SHA256,'read_bytes')
    following=_evidence(project,m['next_entry_evidence'],ORIGINAL_SHA256,'analyze_function')
    xs=[_evidence(project,p,ORIGINAL_SHA256,'xrefs')for p in m['gap_xref_evidence']]
    dead=[_evidence(project,p,ORIGINAL_SHA256,'inspect_native_instruction')for p in m['gap_decoder_evidence']]
    live=[_evidence(project,p,ORIGINAL_SHA256,'inspect_native_instruction')for p in m['preceding_jump_evidence']]
    interior=[_evidence(project,p,ORIGINAL_SHA256,'inspect_native_instruction')for p in m['interior_target_evidence']]
    all_e=[body,raw,following,*xs,*dead,*live,*interior]
    if (len({e['evidence_id']for e in all_e})!=len(all_e)or any(e['analysis_profile']['digest']!=PROFILE
            or e['analysis_profile']['parameters'].get('target_format')!='dos-mz'
            or e['subject'].get('format')!='dos-mz'or e['subject'].get('architecture')!='x86'for e in all_e)):
        raise ValueError('obtain_input requires distinct primary evidence in fixed original profile')
    n=raw['normalized_result'];blob=bytes.fromhex(n['bytes_hex'])
    reference=build_reference((project.parent/'CHESS.EXE').read_bytes())
    expected=reference['image'][0x254:0x83e]
    if (raw['parameters']!={'address':hex(START),'length':SIZE+NEXT_SIZE}
            or _number(n['address'])!=START or n.get('complete')is not True
            or n.get('requested_bytes')!=SIZE+NEXT_SIZE or n.get('returned_bytes')!=SIZE+NEXT_SIZE
            or len(blob)!=SIZE+NEXT_SIZE or blob!=expected
            or _hash(blob[:SIZE])!=BODY_SHA or _hash(blob[SIZE:])!=NEXT_SHA
            or not isinstance(linked,bytes)or len(linked)!=SIZE or linked!=blob[:SIZE]
            or {a for a in reference['relocations']if 0x254<=a<0x83e}!=MZ_SITES|NEXT_MZ_SITES):
        raise ValueError('obtain_input requires full original/C1439, adjacent75 and exact loader sites')
    native,blocks,starts=_native(body,START,RANGES,1424,SIZE,145,CFG_SHA)
    _native(following,END,[(END,END+NEXT_SIZE)],NEXT_SIZE,NEXT_SIZE,9,NEXT_CFG_SHA)
    gap_bytes={a+j for a,(b,*_)in GAPS.items()for j in range(len(bytes.fromhex(b)))}
    if (sorted(_number(e['parameters']['address'])for e in xs)!=sorted(gap_bytes)
            or any(set(e['parameters'])!={'address'}or e['normalized_result']!=[]for e in xs)):
        raise ValueError('all15 obtain_input gap bytes require empty unfiltered global xrefs')
    if any(_number(r['target_address'])in gap_bytes for r in
           native.get('incoming_references',[])+native.get('outgoing_references',[])
           if not r['target_address'].startswith('stack:')):
        raise ValueError('obtain_input native reference enters omitted jump bytes')
    if sorted(_number(e['parameters']['address'])for e in dead)!=sorted(GAPS):
        raise ValueError('obtain_input requires every fixed gap decoder observation')
    for e in dead:
        n=e['normalized_result'];a=_number(e['parameters']['address'])
        if (e['parameters']!={'address':hex(a)}or _number(n['address'])!=a
                or n.get('status')!='undecodable'or n.get('bytes')is not None
                or n.get('length')is not None or n.get('mnemonic')is not None
                or n.get('procedure')is not None or n['flow'].get('kind')!='unavailable'
                or n['flow'].get('direct_destinations')!=[]or n['flow'].get('conditional')is not False
                or n['flow'].get('computed')is not False):
            raise ValueError('obtain_input omitted branches remain explicitly unknown to native decoder')
    if sorted(_number(e['parameters']['address'])for e in live)!=sorted(v[2]for v in GAPS.values()):
        raise ValueError('obtain_input needs all seven live predecessor jump observations')
    live_by_address={_number(e['parameters']['address']):e for e in live}
    if sorted(_number(e['parameters']['address'])for e in interior)!=sorted(INTERIOR_TARGETS):
        raise ValueError('obtain_input requires the two fixed decoded interior jump targets')
    for e in interior:
        n=e['normalized_result'];a=_number(e['parameters']['address']);b,target=INTERIOR_TARGETS[a];flow=n['flow']
        if (e['parameters']!={'address':hex(a)}or _number(n['address'])!=a
                or n.get('status')!='decoded'or n.get('bytes')!=b or n.get('length')!=2
                or n.get('mnemonic')!='JMP'or n.get('procedure')!=hex(START)
                or flow.get('kind')!='jump'or flow.get('conditional')is not False
                or flow.get('computed')is not False or flow.get('direct_destinations')!=[hex(target)]
                or linked[a-START:a-START+2]!=bytes.fromhex(b)
                or _branch(a,bytes.fromhex(b))!=target or target not in starts
                or not any(left<a<a+2<=right for left,right,_ in blocks)):
            raise ValueError('obtain_input fixed interior gap destination needs decoded branch closure')
    for a,(hexbytes,target,prev,prevhex,prevtarget)in GAPS.items():
        b=bytes.fromhex(hexbytes);p=bytes.fromhex(prevhex)
        if (linked[a-START:a-START+len(b)]!=b or linked[prev-START:a-START]!=p
                or _branch(a,b)!=target or prev+len(p)!=a or _branch(prev,p)!=prevtarget
                or not any(left<=prev<end==a for left,end,_ in blocks)):
            raise ValueError('obtain_input raw gaps must follow complete terminating native branches')
        e=live_by_address[prev];n=e['normalized_result'];flow=n['flow']
        if (e['parameters']!={'address':hex(prev)}or _number(n['address'])!=prev
                or n.get('status')!='decoded'or n.get('bytes')!=prevhex or n.get('length')!=len(p)
                or n.get('mnemonic')!='JMP'or n.get('procedure')!=hex(START)
                or flow.get('kind')!='jump'or flow.get('conditional')is not False
                or flow.get('computed')is not False or flow.get('direct_destinations')!=[hex(prevtarget)]
                or prevtarget not in starts):
            raise ValueError('obtain_input live branch must independently prove no fallthrough into gap')
        # EB55 enters another omitted branch; resolve that fixed dead-only chain.
        seen=set()
        while target in GAPS:
            if target in seen:raise ValueError('obtain_input omitted jump cycle')
            seen.add(target);target=GAPS[target][1]
        if target not in starts and target not in INTERIOR_TARGETS:
            raise ValueError('obtain_input omitted branch must close at proven native instruction')
    if linked[-10:]!=bytes.fromhex('2bc0eb005e5f8be55dc3'):
        raise ValueError('obtain_input complete zero-return/restoration tail differs')
    if (not isinstance(emitted,dict)or emitted.get('symbol')!='_obtain_input'
            or emitted.get('boundary')!='codeview3_procedure'or emitted.get('size')!=SIZE
            or type(emitted.get('offset'))is not int or emitted['offset']not in(0,580)
            or emitted.get('end')!=emitted['offset']+SIZE or emitted.get('segment')!=1
            or type(emitted.get('segment'))is not int or not isinstance(emitted.get('fixups'),list)
            or len(emitted['fixups'])!=len(FIXUPS)):
        raise ValueError('obtain_input needs fresh full1439 CV and all181 reconstructed fields')
    seen=set();mz=set()
    for f in emitted['fixups']:
        at=f.offset-emitted['offset']
        if (type(f.offset)is not int or type(f.segment)is not int or type(f.width)is not int
                or type(f.location_type)is not int or type(f.segment_relative)is not bool
                or not isinstance(f.target,tuple)or len(f.target)!=2
                or (f.displacement is not None and(type(f.displacement)is not int or f.displacement!=0))
                or at not in FIXUPS or at in seen or f.segment!=emitted['segment']
                or(f.width,f.location_type,f.segment_relative)!=FIXUPS[at]
                or f.frame!=(5,None)or f.target[0]!=2 or type(f.target[1])is not int
                or f.target[1]<=0 or(f.displacement or 0)!=0):
            raise ValueError('obtain_input reconstructed external field ownership differs')
        seen.add(at)
        if f.location_type==3:mz.add(0x254+at+2)
    if seen!=set(FIXUPS)or mz!=MZ_SITES:
        raise ValueError('obtain_input reconstructed field/MZ sets are incomplete')
    return dict(kind=m['kind'],body_evidence_id=body['evidence_id'],raw_evidence_id=raw['evidence_id'],
                span_bytes=SIZE,reachable_body_bytes=1424,closed_cfg_blocks=145,gap_bytes=15,
                dead_branch_count=7,empty_global_xrefs=15,gap_decoder_status='undecodable',
                native_terminating_predecessors=7,decoded_interior_targets=2,dead_to_dead_chain=['0x1048e','0x104e5','0x107e9'],
                compiler_boundary='codeview3_procedure',compiler_fixups=len(FIXUPS),
                original_MZ_sites=sorted(mz),body_sha256=BODY_SHA,next_complete_span_bytes=NEXT_SIZE,
                next_closed_cfg_blocks=9,next_complete_span_sha256=NEXT_SHA,original_sha256=ORIGINAL_SHA256)
