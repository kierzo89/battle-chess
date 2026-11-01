"""Fixed1064 boundary restored by the authenticated full EXEPACK image.

No split-function generalization: only this original, full expanded carrier,
unchanged256+306 bytes, native18-block CFG and known false far aliases qualify.
"""
import hashlib
import json
from extent import _evidence, _number
from reference import build_reference, ORIGINAL_SHA256, CARRIER_SHA256

START, END, SIZE, NEXT_SIZE = 0x11064, 0x11164, 256, 306
BODY_SHA = '803e960e44eb41d30033e98bda1209ecebd85ceba1d325798001e1259bce1235'
NEXT_SHA = '2e3adda310f02112538ece1b96329ae23a4efb4bda1504ef972fb41e86697c6b'
CFG_SHA = '7ff313cbd225b3d666dfd0854ad684b163cb0f1e3b65eef9f59ec4dd7f43b9a8'
PROFILE = '894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
FALSE_SOURCES = [0x10694,0x117a6,0x1208d,0x120a1,0x120b5,0x120c9,0x126d5,0x1d547]
FIXUPS = {7:False,19:True,79:True,83:True,87:True,90:True,95:True,99:False,105:False,242:True}
FIELDS = {'kind','original_raw_evidence','original_next_evidence','original_overlap_evidence',
          'original_false_xrefs_evidence','expanded_body_evidence','expanded_raw_evidence',
          'expanded_next_evidence','expanded_false_xrefs_evidence',
          'expanded_instruction_evidence','expanded_interior_evidence'}


def _hash(b):return hashlib.sha256(b).hexdigest()


def _body(e,start,size):
    p=e['normalized_result']['procedure'];b=p['body']
    if (_number(p['address'])!=start or b.get('available')is not True
            or b.get('contains_entry')is not True or b.get('non_contiguous')is not False
            or b.get('ranges')!=[{'start':hex(start),'end':hex(start+size-1)}]
            or b.get('total_bytes')!=size or b.get('span_bytes')!=size):
        raise ValueError('text-input requires exact independently contiguous native body')


def _raw(e):
    p=e['parameters'];n=e['normalized_result'];b=bytes.fromhex(n['bytes_hex'])
    if (set(p)!={'address','length'} or _number(p['address'])!=START or p['length']!=562
            or _number(n['address'])!=START or n.get('complete')is not True
            or n.get('requested_bytes')!=562 or n.get('returned_bytes')!=562 or len(b)!=562):
        raise ValueError('text-input requires complete562-byte native original/expanded context')
    return b


def validate_text_input_extent(unit,project,target_sha256,emitted,linked):
    m=unit.get('extended_extent')
    if (not isinstance(m,dict) or set(m)!=FIELDS or m['kind']!='text_input_expanded_1064_v1'
            or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='text_input_1064'
            or unit.get('symbol')!='_text_input_1064' or unit.get('language')!='c'
            or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
            or unit.get('code_address')is not None or _number(unit['image_offset'])!=0x1064
            or _number(unit['size'])!=SIZE or unit.get('externals',{}).get('__chkstk')!=0xecaa):
        raise ValueError('unsupported fixed text-input extent identity')
    orig=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function')
    specs={'original_raw_evidence':(ORIGINAL_SHA256,'read_bytes'),
           'original_next_evidence':(ORIGINAL_SHA256,'analyze_function'),
           'original_overlap_evidence':(ORIGINAL_SHA256,'analyze_function'),
           'original_false_xrefs_evidence':(ORIGINAL_SHA256,'xrefs'),
           'expanded_body_evidence':(CARRIER_SHA256,'analyze_function'),
           'expanded_raw_evidence':(CARRIER_SHA256,'read_bytes'),
           'expanded_next_evidence':(CARRIER_SHA256,'analyze_function'),
           'expanded_false_xrefs_evidence':(CARRIER_SHA256,'xrefs'),
           'expanded_instruction_evidence':(CARRIER_SHA256,'inspect_native_instruction'),
           'expanded_interior_evidence':(CARRIER_SHA256,'inspect_native_instruction')}
    es={k:_evidence(project,m[k],sha,op)for k,(sha,op)in specs.items()};all_e=[orig,*es.values()]
    if (len({e['evidence_id']for e in all_e})!=len(all_e)
            or any(e['analysis_profile']['digest']!=PROFILE
                   or e['analysis_profile']['parameters'].get('target_format')!='dos-mz' for e in all_e)):
        raise ValueError('text-input requires distinct evidence in the fixed native DOS profile')
    for e,address in [(orig,START),(es['original_overlap_evidence'],0x110d3),
                      (es['expanded_body_evidence'],START),
                      (es['original_next_evidence'],END),(es['expanded_next_evidence'],END)]:
        if e['parameters']!={'procedure':hex(address)}:
            raise ValueError('text-input requires exact native function queries')
    p=orig['normalized_result']['procedure'];b=p['body']
    if (_number(p['address'])!=START or b.get('available')is not True or b.get('contains_entry')is not True
            or b.get('non_contiguous')is not True or b.get('total_bytes')!=107 or b.get('span_bytes')!=110
            or b.get('ranges')!=[{'start':'0x11064','end':'0x11065'},{'start':'0x11067','end':'0x11083'},
                                 {'start':'0x11085','end':'0x110cf'},{'start':'0x110d1','end':'0x110d1'}]):
        raise ValueError('text-input original split observation differs')
    p=es['original_overlap_evidence']['normalized_result']['procedure'];b=p['body']
    if (_number(p['address'])!=0x110d3 or b.get('available')is not True
            or b.get('contains_entry')is not True or b.get('non_contiguous')is not True
            or b.get('total_bytes')!=146 or b.get('span_bytes')!=148
            or b.get('ranges')!=[{'start':'0x110d0','end':'0x110d0'},{'start':'0x110d3','end':'0x11163'}]):
        raise ValueError('text-input original false interior body differs')
    x=es['original_false_xrefs_evidence'];ex=es['expanded_false_xrefs_evidence']
    if (x['parameters']!={'address':'0x110d3'} or ex['parameters']!={'address':'0x110d3'}
            or sorted(_number(a)for a in x['normalized_result'])!=FALSE_SOURCES
            or ex['normalized_result']!=[]):
        raise ValueError('text-input requires all eight original false aliases and no expanded interior xrefs')
    original=(project.parent/'CHESS.EXE').read_bytes();ref=build_reference(original)
    context=ref['image'][0x1064:0x1296]
    if (ref['carrier_sha256']!=CARRIER_SHA256 or context!=_raw(es['original_raw_evidence'])
            or context!=_raw(es['expanded_raw_evidence']) or _hash(context[:SIZE])!=BODY_SHA
            or _hash(context[SIZE:])!=NEXT_SHA or not isinstance(linked,bytes)
            or len(linked)!=SIZE or linked!=context[:SIZE]
            or any(0x1064<=s<0x1296 for s in ref['relocations'])):
        raise ValueError('text-input full original/expanded body or complete next bytes differ')
    for address in FALSE_SOURCES:
        at=address-0x10000;call=ref['image'][at:at+5]
        if (call!=bytes.fromhex('9a03000d11') or at+3 not in ref['relocations']
                or 0x10000+16*int.from_bytes(call[3:5],'little')+int.from_bytes(call[1:3],'little')!=0x210d3):
            raise ValueError('text-input false aliases require original loader-relocated FAR110D:0003 calls')
    _body(es['expanded_body_evidence'],START,SIZE)
    _body(es['original_next_evidence'],END,NEXT_SIZE);_body(es['expanded_next_evidence'],END,NEXT_SIZE)
    native=es['expanded_body_evidence']['normalized_result']
    blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(a)for a in q['successors'])))for q in native['basic_blocks'])
    if len(blocks)!=18 or _hash(json.dumps(blocks,separators=(',',':')).encode())!=CFG_SHA:
        raise ValueError('text-input requires exact independently corrected18-block CFG')
    starts={a for a,_,_ in blocks};cursor=START
    for a,z,succ in blocks:
        if a!=cursor or not a<z<=END or any(t not in starts for t in succ):
            raise ValueError('text-input CFG must cover every byte exactly once and be closed')
        cursor=z
    if cursor!=END:raise ValueError('text-input CFG lacks complete coverage')
    graph={a:s for a,_,s in blocks};pending=[START];seen=set()
    while pending:
        a=pending.pop()
        if a not in seen:seen.add(a);pending.extend(graph[a])
    if seen!=starts:raise ValueError('text-input CFG has unreachable blocks')
    for r in native.get('incoming_references',[]):
        a=_number(r['target_address']);s=_number(r['source_address'])
        if a!=START and not(START<=s<END and a in starts):
            raise ValueError('text-input expanded incoming reference creates an extra interior entry')
    ins=es['expanded_instruction_evidence'];inside=es['expanded_interior_evidence'];n=ins['normalized_result'];i=inside['normalized_result']
    if (ins['parameters']!={'address':'0x110d2'} or inside['parameters']!={'address':'0x110d3'}
            or _number(n['address'])!=0x110d2 or n.get('status')!='decoded' or n.get('bytes')!='2500f0'
            or n.get('length')!=3 or n.get('mnemonic')!='AND' or n.get('procedure')!='0x11064'
            or n['flow'].get('kind')!='fallthrough' or n['flow'].get('direct_destinations')!=[]
            or _number(i['address'])!=0x110d3 or i.get('status')!='not-instruction-boundary'
            or i.get('bytes')is not None or i.get('length')is not None or i.get('procedure')!='0x11064'
            or linked[0x10d2-0x1064:0x10d5-0x1064]!=bytes.fromhex('2500f0')):
        raise ValueError('text-input false entry must be interior to independently decoded AND immediate')
    if (not isinstance(emitted,dict) or emitted.get('symbol')!=unit['symbol']
            or emitted.get('boundary')!='codeview3_procedure' or emitted.get('size')!=SIZE
            or type(emitted.get('offset'))is not int or emitted['offset']<0
            or emitted.get('end')!=emitted['offset']+SIZE or type(emitted.get('segment'))is not int
            or emitted['segment']<=0 or not isinstance(emitted.get('fixups'),list) or len(emitted['fixups'])!=10):
        raise ValueError('text-input requires complete fresh CV256 with ten original compiler fields')
    supplied=set()
    for f in emitted['fixups']:
        a=f.offset-emitted['offset']
        if (a not in FIXUPS or a in supplied or f.segment!=emitted['segment'] or f.width!=2
                or f.location_type!=1 or f.segment_relative is not FIXUPS[a] or f.frame!=(5,None)
                or f.target[0]!=2 or type(f.target[1])is not int or f.target[1]<=0 or (f.displacement or 0)!=0):
            raise ValueError('text-input requires exact ten external OFFSET16 fixup fields')
        supplied.add(a)
    return {'kind':m['kind'],'body_evidence_id':orig['evidence_id'],
            'expanded_body_evidence_id':es['expanded_body_evidence']['evidence_id'],
            'original_sha256':ORIGINAL_SHA256,'expanded_carrier_sha256':CARRIER_SHA256,
            'span_bytes':SIZE,'reachable_body_bytes':SIZE,'closed_cfg_blocks':18,
            'body_sha256':BODY_SHA,'next_complete_body_bytes':NEXT_SIZE,'next_complete_body_sha256':NEXT_SHA,
            'false_entry':'0x110d3','actual_far_target':'0x210d3','false_far_aliases':8,
            'compiler_OFFSET16_fixups':10,'compiler_boundary':'codeview3_procedure'}
