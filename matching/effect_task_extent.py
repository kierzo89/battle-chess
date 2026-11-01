"""Fixed6AB1 compiler extent with one observed dead return jump.

Only this exact ordinary C5 body is admitted. Full original-byte authentication,
closed CFG, empty global gap xrefs and fresh CV/fixup ownership are independent
requirements; this is not a general non-contiguous-function allowance.
"""
import hashlib
import json
from extent import _evidence, _number

TARGET_SHA256 = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BODY_SHA256 = '939d511f0a9f8fb077fc7d8f86d0d348cdcb2a867032cb0c8c6a7c03626561cc'
NEXT_SHA256 = '9d03c22879cf936c25fa4c4e492645f076239efff9e4adb3fed1a48b7b36e682'
CFG_SHA256 = '7e0788534542ad11e0a538612c349fa414a1579893f5c6f9d3b48a676c58367e'
START, END, SIZE, NEXT_SIZE = 0x16ab1, 0x16bf9, 328, 187
GAP, EPILOGUE = 0x16be8, 0x16bf3
RANGES = [(START,GAP),(GAP+2,END)]
# All12 observed compiler OFFSET16 fields, relative to the full CV procedure.
# True means DGROUP/segment-relative; False means a near self-relative call.
FIXUP_FIELDS = {7:False,16:False,56:True,116:True,134:True,154:False,
                173:False,192:False,233:False,254:True,258:True,261:False}


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def validate_effect_task_extent(unit, project, target_sha256, emitted, linked):
    meta=unit.get('extended_extent')
    if (not isinstance(meta,dict) or set(meta)!={
            'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence'}
            or meta.get('kind')!='effect_task_gap_6ab1_v1'
            or target_sha256!=TARGET_SHA256 or unit.get('id')!='effect_task_6ab1'
            or unit.get('symbol')!='_effect_task_6ab1' or unit.get('language')!='c'
            or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
            or unit.get('code_address') is not None
            or _number(unit['image_offset'])!=START-0x10000 or _number(unit['size'])!=SIZE
            or unit.get('externals',{}).get('__chkstk')!=0xecaa
            or not isinstance(meta['gap_xref_evidence'],list) or len(meta['gap_xref_evidence'])!=2):
        raise ValueError('unsupported fixed effect-task C extent identity or fields')
    dossier=_evidence(project,unit['rea_evidence'],target_sha256,'analyze_function')
    raw=_evidence(project,meta['raw_span_evidence'],target_sha256,'read_bytes')
    following=_evidence(project,meta['next_entry_evidence'],target_sha256,'analyze_function')
    xrefs=[_evidence(project,p,target_sha256,'xrefs') for p in meta['gap_xref_evidence']]
    evidence=[dossier,raw,following]+xrefs
    if (len({e['analysis_profile']['digest']for e in evidence})!=1
            or any(e['analysis_profile']['parameters'].get('target_format')!='dos-mz'for e in evidence)
            or len({e['evidence_id']for e in evidence})!=len(evidence)):
        raise ValueError('effect-task evidence requires one original DOS profile and distinct identities')
    n=dossier['normalized_result'];proc=n['procedure'];body=proc['body']
    ranges=[(_number(r['start']),_number(r['end'])+1)for r in body.get('ranges',[])]
    if (body.get('available')is not True or body.get('contains_entry')is not True
            or body.get('non_contiguous')is not True or _number(proc['address'])!=START
            or ranges!=RANGES or body.get('total_bytes')!=326 or body.get('span_bytes')!=SIZE):
        raise ValueError('effect-task needs exact two ranges,326 reachable bytes and328 span')
    data=raw['normalized_result'];blob=bytes.fromhex(data['bytes_hex'])
    if (data.get('complete')is not True or _number(data['address'])!=START
            or _number(raw['parameters']['address'])!=START
            or raw['parameters']['length']!=SIZE+NEXT_SIZE
            or data.get('requested_bytes')!=SIZE+NEXT_SIZE
            or data.get('returned_bytes')!=SIZE+NEXT_SIZE or len(blob)!=SIZE+NEXT_SIZE
            or not isinstance(linked,bytes) or len(linked)!=SIZE or blob[:SIZE]!=linked
            or _hash(linked)!=BODY_SHA256 or _hash(blob[SIZE:])!=NEXT_SHA256):
        raise ValueError('effect-task requires complete original328 and authenticated next187 bytes')
    np=following['normalized_result']['procedure'];nb=np['body']
    if (nb.get('available')is not True or nb.get('contains_entry')is not True
            or nb.get('non_contiguous')is not False or _number(np['address'])!=END
            or nb.get('ranges')!=[{'start':hex(END),'end':hex(END+NEXT_SIZE-1)}]
            or nb.get('span_bytes')!=NEXT_SIZE or nb.get('total_bytes')!=NEXT_SIZE):
        raise ValueError('effect-task needs adjacent complete contiguous187-byte function')
    observed=sorted((_number(b['start']),_number(b['end']),tuple(sorted(_number(a)for a in b['successors'])))for b in n['basic_blocks'])
    if len(observed)!=13 or _hash(json.dumps(observed,separators=(',',':')).encode())!=CFG_SHA256:
        raise ValueError('effect-task requires exact retained13-block CFG')
    starts={a for a,_,_ in observed};covered=[];current=None
    for left,right,successors in observed:
        if not START<=left<right<=END or any(a not in starts for a in successors):
            raise ValueError('effect-task CFG must be closed with valid block intervals')
        if current is not None and left==current[1]:current[1]=right
        else:
            if current is not None:covered.append(tuple(current))
            current=[left,right]
    if current is not None:covered.append(tuple(current))
    if covered!=RANGES or sum(b-a for a,b,_ in observed)!=326:
        raise ValueError('effect-task CFG must cover each retained byte once and no gap byte')
    graph={a:s for a,_,s in observed};pending=[START];reachable=set()
    while pending:
        a=pending.pop()
        if a not in reachable:reachable.add(a);pending.extend(graph[a])
    if reachable!=starts:
        raise ValueError('effect-task CFG contains an unreachable claimed block')
    if (sorted(_number(e['parameters']['address'])for e in xrefs)!=[GAP,GAP+1]
            or any(e['normalized_result']!=[]for e in xrefs)):
        raise ValueError('both effect-task gap bytes require distinct empty global xrefs')
    if any(_number(ref['target_address'])in(GAP,GAP+1)for ref in n.get('incoming_references',[])):
        raise ValueError('effect-task incoming reference enters dead return jump')
    for address in (GAP-2,GAP):
        at=address-START
        if linked[at]!=0xeb or address+2+int.from_bytes(linked[at+1:at+2],'little',signed=True)!=EPILOGUE:
            raise ValueError('effect-task dead jump must duplicate preceding live epilogue jump')
    if linked[EPILOGUE-START:]!=bytes.fromhex('5e5f8be55dc3'):
        raise ValueError('effect-task complete final restoration differs')
    if (not isinstance(emitted,dict) or emitted.get('symbol')!=unit['symbol']
            or emitted.get('boundary')!='codeview3_procedure' or emitted.get('size')!=SIZE
            or type(emitted.get('offset'))is not int or emitted['offset']<0
            or emitted.get('end')!=emitted['offset']+SIZE
            or type(emitted.get('segment'))is not int or emitted['segment']<=0
            or not isinstance(emitted.get('fixups'),list) or len(emitted['fixups'])!=12):
        raise ValueError('effect-task requires entire fresh CV328 and exactly12 actual compiler fixups')
    supplied=set()
    for f in emitted['fixups']:
        at=f.offset-emitted['offset']
        if (at not in FIXUP_FIELDS or at in supplied or f.segment!=emitted['segment']
                or f.width!=2 or f.location_type!=1 or f.segment_relative is not FIXUP_FIELDS[at]
                or f.frame!=(5,None) or f.target[0]!=2 or type(f.target[1])is not int
                or f.target[1]<=0 or (f.displacement or 0)!=0):
            raise ValueError('effect-task fixups must be exact external OFFSET16 call/DGROUP fields')
        supplied.add(at)
    if supplied!=set(FIXUP_FIELDS):
        raise ValueError('effect-task fresh OMF fixup ownership is incomplete')
    return {'kind':meta['kind'],'body_evidence_id':dossier['evidence_id'],
            'raw_span_evidence_id':raw['evidence_id'],'next_entry_evidence_id':following['evidence_id'],
            'gap_xref_evidence_ids':[e['evidence_id']for e in xrefs],
            'span_bytes':SIZE,'reachable_body_bytes':326,'closed_cfg_blocks':13,
            'gap_address':hex(GAP),'gap_bytes':2,'gap_hex':linked[GAP-START:GAP-START+2].hex(),
            'shared_epilogue':hex(EPILOGUE),'body_sha256':BODY_SHA256,
            'next_complete_body_bytes':NEXT_SIZE,'next_complete_body_sha256':NEXT_SHA256,
            'next_entry':hex(END),'compiler_OFFSET16_fixups':len(supplied),
            'compiler_boundary':'codeview3_procedure'}
