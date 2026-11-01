"""Fixed 67FB complete C extent: one eight-word table and one dead jump.

This profile does not generalize table/gap admission. It authenticates the full
original body and following function, then requires independent fresh CodeView
and own-CODE OMF fixup ownership for every compiler-generated table word.
"""
import hashlib
import json
from extent import _evidence, _number

TARGET_SHA256 = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BODY_SHA256 = 'be3523108d77df90d37e3d0e54258f71135a4ca99ac9cb7fa2ea93d417fa24ab'
NEXT_SHA256 = 'cf746bc9b7ec08cdbcee16c297363242fadf62b407f23273a84733060f83638d'
CFG_SHA256 = 'dd5f1b08f7a9a8a0aa10e0a6dce488e8f5f51d6af06d5242dbd31c7d983a053a'
START, END, SIZE, NEXT_SIZE = 0x167fb, 0x168ea, 239, 455
RANGES = [(START, 0x1687c), (0x1687e, 0x1688e), (0x1689e, END)]
# A fixed, observed descriptor, not a caller-provided or general table policy.
SWITCHES = [(0x1687c, 0x1687e, 0x1688e, 0x1689e,
             [0x16824, 0x16850, 0x16845, 0x1685b, 0x16871, 0x16866, 0x1682f, 0x1683a])]
OMITTED = [0x1687c, 0x1687d, *range(0x1688e, 0x1689e)]


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def validate_task_dispatch_extent(unit, project, target_sha256, emitted, linked):
    """Accept only the fixed whole 239-byte ordinary C5 task dispatcher."""
    meta = unit.get('extended_extent')
    if (not isinstance(meta, dict) or set(meta) != {
            'kind', 'raw_span_evidence', 'next_entry_evidence', 'omitted_byte_xref_evidence'}
            or meta.get('kind') != 'task_dispatch_switch_67fb_v1'
            or target_sha256 != TARGET_SHA256 or unit.get('id') != 'dispatch_tasks_67fb'
            or unit.get('symbol') != '_dispatch_tasks_67fb' or unit.get('language') != 'c'
            or unit.get('backend') != 'msc500-omf' or unit.get('flags') != ['/AS', '/Zi']
            or unit.get('code_address') is not None
            or _number(unit['image_offset']) != START-0x10000 or _number(unit['size']) != SIZE
            or not isinstance(meta['omitted_byte_xref_evidence'], list)
            or len(meta['omitted_byte_xref_evidence']) != len(OMITTED)):
        raise ValueError('unsupported fixed task-dispatch switch C extent identity or proof fields')
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    xrefs = [_evidence(project, path, target_sha256, 'xrefs')
             for path in meta['omitted_byte_xref_evidence']]
    evidence = [dossier, raw, following] + xrefs
    if (len({e['analysis_profile']['digest'] for e in evidence}) != 1
            or any(e['analysis_profile']['parameters'].get('target_format') != 'dos-mz' for e in evidence)
            or len({e['evidence_id'] for e in evidence}) != len(evidence)):
        raise ValueError('task-dispatch switch evidence must have distinct identities and one original DOS profile')
    n = dossier['normalized_result']; proc = n['procedure']; body = proc['body']
    ranges = [(_number(r['start']), _number(r['end'])+1) for r in body.get('ranges', [])]
    if (body.get('available') is not True or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True or _number(proc['address']) != START
            or ranges != RANGES or body.get('total_bytes') != 221 or body.get('span_bytes') != SIZE):
        raise ValueError('task-dispatch switch requires exact three retained ranges and 18 omitted bytes')
    data = raw['normalized_result']; blob = bytes.fromhex(data['bytes_hex'])
    if (data.get('complete') is not True or _number(data['address']) != START
            or _number(raw['parameters']['address']) != START
            or raw['parameters']['length'] != SIZE+NEXT_SIZE
            or data.get('requested_bytes') != SIZE+NEXT_SIZE
            or data.get('returned_bytes') != SIZE+NEXT_SIZE or len(blob) != SIZE+NEXT_SIZE
            or not isinstance(linked, bytes) or len(linked) != SIZE or blob[:SIZE] != linked
            or _hash(linked) != BODY_SHA256 or _hash(blob[SIZE:]) != NEXT_SHA256):
        raise ValueError('task-dispatch switch needs complete original body and authenticated entire next455-byte body')
    next_proc = following['normalized_result']['procedure']; nb = next_proc['body']
    if (nb.get('available') is not True or nb.get('contains_entry') is not True
            or nb.get('non_contiguous') is not False or _number(next_proc['address']) != END
            or nb.get('ranges') != [{'start': hex(END), 'end': hex(END+NEXT_SIZE-1)}]
            or nb.get('span_bytes') != NEXT_SIZE or nb.get('total_bytes') != NEXT_SIZE):
        raise ValueError('task-dispatch switch requires adjacent complete contiguous next455-byte function')
    observed = sorted((_number(b['start']), _number(b['end']),
                       tuple(sorted(_number(a) for a in b['successors'])))
                      for b in n['basic_blocks'])
    if len(observed) != 22 or _hash(json.dumps(observed, separators=(',', ':')).encode()) != CFG_SHA256:
        raise ValueError('task-dispatch switch needs the exact retained22-block CFG')
    starts = {a for a, _, _ in observed}; covered = []; current = None
    for left, right, successors in observed:
        if not START <= left < right <= END or any(a not in starts for a in successors):
            raise ValueError('task-dispatch switch CFG is not closed or has an invalid block')
        if current is not None and left == current[1]: current[1] = right
        else:
            if current is not None: covered.append(tuple(current))
            current = [left, right]
    if current is not None: covered.append(tuple(current))
    if covered != RANGES or sum(b-a for a,b,_ in observed) != 221:
        raise ValueError('task-dispatch switch CFG must cover every retained byte once and no omitted byte')
    reachable = set(); pending = [START]; graph = {a: s for a, _, s in observed}
    while pending:
        a = pending.pop()
        if a not in reachable: reachable.add(a); pending.extend(graph[a])
    if reachable != starts:
        raise ValueError('task-dispatch switch CFG includes an unreachable claimed block')
    for ref in n.get('incoming_references', []):
        if _number(ref['target_address']) in OMITTED:
            raise ValueError('task-dispatch switch incoming reference enters omitted data or dead code')
    if (sorted(_number(e['parameters']['address']) for e in xrefs) != OMITTED
            or any(e['normalized_result'] != [] for e in xrefs)):
        raise ValueError('all18 omitted bytes need distinct empty original global xref results')
    required = {}
    for gap, dispatch, table, resume, targets in SWITCHES:
        g, d, t, r = (x-START for x in (gap, dispatch, table, resume))
        for at in (g-2, g):
            if (linked[at] != 0xeb or START+at+2
                    + int.from_bytes(linked[at+1:at+2], 'little', signed=True) != resume):
                raise ValueError('task-dispatch switch dead jump must duplicate the preceding live jump')
        if (linked[d:d+7] != bytes.fromhex('2d01003d070077')
                or dispatch+8+int.from_bytes(linked[d+7:d+8], 'little', signed=True) != resume
                or linked[d+8:t-2] != bytes.fromhex('03c0932effa7')
                or int.from_bytes(linked[t-2:t], 'little') != table-0x10000
                or [0x10000+int.from_bytes(linked[a:a+2], 'little') for a in range(t,r,2)] != targets
                or any(a not in starts or not START <= a < gap for a in targets)):
            raise ValueError('task-dispatch switch bound, dispatcher, table words or case starts differ')
        required[t-2] = 'dispatch'
        required.update({at: 'table' for at in range(t,r,2)})
    if linked[-6:] != bytes.fromhex('5e5f8be55dc3'):
        raise ValueError('task-dispatch switch final register/stack restoration differs')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != unit['symbol']
            or emitted.get('boundary') != 'codeview3_procedure' or emitted.get('size') != SIZE
            or type(emitted.get('offset')) is not int or emitted['offset'] < 0
            or emitted.get('end') != emitted['offset']+SIZE
            or type(emitted.get('segment')) is not int or emitted['segment'] <= 0
            or not isinstance(emitted.get('fixups'), list)):
        raise ValueError('task-dispatch switch requires entire independent fresh CodeView239 procedure')
    supplied = set(); used = set(); base = emitted['offset']; seg = emitted['segment']
    for f in emitted['fixups']:
        at = f.offset-base
        if (f.segment != seg or type(f.width) is not int or f.width <= 0
                or not 0 <= at < at+f.width <= SIZE
                or used.intersection(range(at,at+f.width))):
            raise ValueError('task-dispatch switch fresh fixup out of bounds or overlapping')
        used.update(range(at,at+f.width))
        omitted_overlap = any(START+x in OMITTED for x in range(at,at+f.width))
        if at in required:
            frame = (5,None) if required[at] == 'dispatch' else (0,seg)
            if (f.width != 2 or f.location_type != 1 or f.segment_relative is not True
                    or f.target != (0,seg) or f.frame != frame or (f.displacement or 0) != 0):
                raise ValueError('task-dispatch switch requires actual own-CODE OFFSET16 table/dispatch fixup')
            supplied.add(at)
        elif omitted_overlap:
            raise ValueError('task-dispatch switch extra fresh fixup overlaps omitted table or dead jump')
    if supplied != set(required):
        raise ValueError('task-dispatch switch fresh OMF must own the dispatch field and all8 table words')
    return {'kind':meta['kind'], 'body_evidence_id':dossier['evidence_id'],
            'raw_span_evidence_id':raw['evidence_id'], 'next_entry_evidence_id':following['evidence_id'],
            'omitted_byte_xref_evidence_ids':[e['evidence_id'] for e in xrefs],
            'span_bytes':SIZE, 'reachable_body_bytes':221, 'closed_cfg_blocks':22,
            'omitted_dead_jump_bytes':2, 'omitted_table_bytes':16, 'compiler_own_CODE_fixups':len(supplied),
            'body_sha256':BODY_SHA256, 'next_complete_body_bytes':NEXT_SIZE,
            'next_complete_body_sha256':NEXT_SHA256, 'next_entry':hex(END),
            'compiler_boundary':'codeview3_procedure'}
