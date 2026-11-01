"""Fixed724D compiler extent with one observed dead return jump.

Only this exact ordinary C5 body is admitted. Full original-byte authentication,
closed CFG, empty global gap xrefs and fresh CV/fixup ownership are independent
requirements; this is not a general non-contiguous-function allowance.
"""
import hashlib
import json
from extent import _evidence, _number

TARGET_SHA256 = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BODY_SHA256 = '72958f0d5e83978839ea35234dd588369e03f3b2517b87f0dd3b6559a1dc8f52'
NEXT_SHA256 = '69e982d4ad5d4d8b317e227ca48add9148a1019410a28031a67b5356262cd223'
CFG_SHA256 = '8a44e723368f460cab5948f2f343353b156d32fd3ab6b92a9d80512c8341903b'
START, END, SIZE, NEXT_SIZE = 0x1724d, 0x1730c, 191, 640
GAP, EPILOGUE = 0x172fc, 0x17306
RANGES = [(START,GAP),(GAP+2,END)]
# Seven actual external OFFSET16 compiler fields. True is DGROUP-relative;
# False is a self-relative near call. No source byte or relocation is optional.
FIXUP_FIELDS = {7:False,51:True,69:True,89:False,108:False,127:False,152:False}


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def validate_face_task_extent(unit, project, target_sha256, emitted, linked):
    meta=unit.get('extended_extent')
    if (not isinstance(meta,dict) or set(meta)!={
            'kind','raw_span_evidence','next_entry_evidence','gap_xref_evidence'}
            or meta.get('kind')!='face_task_gap_724d_v1'
            or target_sha256!=TARGET_SHA256 or unit.get('id')!='face_task_724d'
            or unit.get('symbol')!='_face_task_724d' or unit.get('language')!='c'
            or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
            or unit.get('code_address') is not None
            or _number(unit['image_offset'])!=START-0x10000 or _number(unit['size'])!=SIZE
            or unit.get('externals',{}).get('__chkstk')!=0xecaa
            or not isinstance(meta['gap_xref_evidence'],list) or len(meta['gap_xref_evidence'])!=2):
        raise ValueError('unsupported fixed face-task C extent identity or fields')
    dossier=_evidence(project,unit['rea_evidence'],target_sha256,'analyze_function')
    raw=_evidence(project,meta['raw_span_evidence'],target_sha256,'read_bytes')
    following=_evidence(project,meta['next_entry_evidence'],target_sha256,'analyze_function')
    xrefs=[_evidence(project,p,target_sha256,'xrefs') for p in meta['gap_xref_evidence']]
    evidence=[dossier,raw,following]+xrefs
    if (len({e['analysis_profile']['digest']for e in evidence})!=1
            or any(e['analysis_profile']['parameters'].get('target_format')!='dos-mz'for e in evidence)
            or len({e['evidence_id']for e in evidence})!=len(evidence)):
        raise ValueError('face-task evidence requires one original DOS profile and distinct identities')
    n=dossier['normalized_result'];proc=n['procedure'];body=proc['body']
    ranges=[(_number(r['start']),_number(r['end'])+1)for r in body.get('ranges',[])]
    if (body.get('available')is not True or body.get('contains_entry')is not True
            or body.get('non_contiguous')is not True or _number(proc['address'])!=START
            or ranges!=RANGES or body.get('total_bytes')!=189 or body.get('span_bytes')!=SIZE):
        raise ValueError('face-task needs exact two ranges,189 reachable bytes and191 span')
    data=raw['normalized_result'];blob=bytes.fromhex(data['bytes_hex'])
    if (data.get('complete')is not True or _number(data['address'])!=START
            or _number(raw['parameters']['address'])!=START
            or raw['parameters']['length']!=SIZE+NEXT_SIZE
            or data.get('requested_bytes')!=SIZE+NEXT_SIZE
            or data.get('returned_bytes')!=SIZE+NEXT_SIZE or len(blob)!=SIZE+NEXT_SIZE
            or not isinstance(linked,bytes) or len(linked)!=SIZE or blob[:SIZE]!=linked
            or _hash(linked)!=BODY_SHA256 or _hash(blob[SIZE:])!=NEXT_SHA256):
        raise ValueError('face-task requires complete original191 and authenticated next640 bytes')
    np=following['normalized_result']['procedure'];nb=np['body']
    if (nb.get('available')is not True or nb.get('contains_entry')is not True
            or nb.get('non_contiguous')is not False or _number(np['address'])!=END
            or nb.get('ranges')!=[{'start':hex(END),'end':hex(END+NEXT_SIZE-1)}]
            or nb.get('span_bytes')!=NEXT_SIZE or nb.get('total_bytes')!=NEXT_SIZE):
        raise ValueError('face-task needs adjacent complete contiguous640-byte function')
    observed=sorted((_number(b['start']),_number(b['end']),tuple(sorted(_number(a)for a in b['successors'])))for b in n['basic_blocks'])
    if len(observed)!=9 or _hash(json.dumps(observed,separators=(',',':')).encode())!=CFG_SHA256:
        raise ValueError('face-task requires exact retained9-block CFG')
    starts={a for a,_,_ in observed};covered=[];current=None
    for left,right,successors in observed:
        if not START<=left<right<=END or any(a not in starts for a in successors):
            raise ValueError('face-task CFG must be closed with valid block intervals')
        if current is not None and left==current[1]:current[1]=right
        else:
            if current is not None:covered.append(tuple(current))
            current=[left,right]
    if current is not None:covered.append(tuple(current))
    if covered!=RANGES or sum(b-a for a,b,_ in observed)!=189:
        raise ValueError('face-task CFG must cover each retained byte once and no gap byte')
    graph={a:s for a,_,s in observed};pending=[START];reachable=set()
    while pending:
        a=pending.pop()
        if a not in reachable:reachable.add(a);pending.extend(graph[a])
    if reachable!=starts:
        raise ValueError('face-task CFG contains an unreachable claimed block')
    if (sorted(_number(e['parameters']['address'])for e in xrefs)!=[GAP,GAP+1]
            or any(e['normalized_result']!=[]for e in xrefs)):
        raise ValueError('both face-task gap bytes require distinct empty global xrefs')
    if any(_number(ref['target_address'])in(GAP,GAP+1)for ref in n.get('incoming_references',[])):
        raise ValueError('face-task incoming reference enters dead return jump')
    for address in (GAP-2,GAP):
        at=address-START
        if linked[at]!=0xeb or address+2+int.from_bytes(linked[at+1:at+2],'little',signed=True)!=EPILOGUE:
            raise ValueError('face-task dead jump must duplicate preceding live epilogue jump')
    if linked[EPILOGUE-START:]!=bytes.fromhex('5e5f8be55dc3'):
        raise ValueError('face-task complete final restoration differs')
    if (not isinstance(emitted,dict) or emitted.get('symbol')!=unit['symbol']
            or emitted.get('boundary')!='codeview3_procedure' or emitted.get('size')!=SIZE
            or type(emitted.get('offset'))is not int or emitted['offset']<0
            or emitted.get('end')!=emitted['offset']+SIZE
            or type(emitted.get('segment'))is not int or emitted['segment']<=0
            or not isinstance(emitted.get('fixups'),list) or len(emitted['fixups'])!=7):
        raise ValueError('face-task requires entire fresh CV191 and exactly7 actual compiler fixups')
    supplied=set()
    for f in emitted['fixups']:
        at=f.offset-emitted['offset']
        if (at not in FIXUP_FIELDS or at in supplied or f.segment!=emitted['segment']
                or f.width!=2 or f.location_type!=1 or f.segment_relative is not FIXUP_FIELDS[at]
                or f.frame!=(5,None) or f.target[0]!=2 or type(f.target[1])is not int
                or f.target[1]<=0 or (f.displacement or 0)!=0):
            raise ValueError('face-task fixups must be exact external OFFSET16 call/DGROUP fields')
        supplied.add(at)
    if supplied!=set(FIXUP_FIELDS):
        raise ValueError('face-task fresh OMF fixup ownership is incomplete')
    return {'kind':meta['kind'],'body_evidence_id':dossier['evidence_id'],
            'raw_span_evidence_id':raw['evidence_id'],'next_entry_evidence_id':following['evidence_id'],
            'gap_xref_evidence_ids':[e['evidence_id']for e in xrefs],
            'span_bytes':SIZE,'reachable_body_bytes':189,'closed_cfg_blocks':9,
            'gap_address':hex(GAP),'gap_bytes':2,'gap_hex':linked[GAP-START:GAP-START+2].hex(),
            'shared_epilogue':hex(EPILOGUE),'body_sha256':BODY_SHA256,
            'next_complete_body_bytes':NEXT_SIZE,'next_complete_body_sha256':NEXT_SHA256,
            'next_entry':hex(END),'compiler_OFFSET16_fixups':len(supplied),
            'compiler_boundary':'codeview3_procedure'}
