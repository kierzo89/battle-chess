"""Fixed 6167 complete C extent: two dispatch tables and two dead jumps.

This profile does not generalize table/gap admission. It authenticates the full
original body and following function, then requires independent fresh CodeView
and own-CODE OMF fixup ownership for every compiler-generated table word.
"""
import hashlib
import json
from extent import _evidence, _number

TARGET_SHA256 = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BODY_SHA256 = '95f0a8797b4462a0e965035362ba8ef68d9e98cdb453f0e6f091bbf38e13cfa2'
NEXT_SHA256 = 'd7a237b4ba1983a8bbe4be0445d1a7cb1869e580a47795a00029bf2f4828f7b4'
CFG_SHA256 = 'b3e92a29ce57493bbab98533ed9866d2bcc98e34f9e8a06a59e90644a283147e'
START, END, SIZE, NEXT_SIZE = 0x16167, 0x16796, 1583, 53
RANGES = [(START, 0x162fa), (0x162fc, 0x1630c), (0x1631c, 0x1675c),
          (0x1675e, 0x1676e), (0x1677e, END)]
SWITCHES = [(0x162fa, 0x162fc, 0x1630c, 0x1631c,
             [0x1620f, 0x162f3, 0x16275, 0x162f3, 0x162ee, 0x162f3, 0x161f3, 0x16240]),
            (0x1675c, 0x1675e, 0x1676e, 0x1677e,
             [0x16376, 0x16624, 0x1666d, 0x16448, 0x163ea, 0x166ec, 0x16523, 0x164c0])]
OMITTED = sorted(a for gap, _, table, resume, _ in SWITCHES
                 for a in [gap, gap+1, *range(table, resume)])


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def validate_dual_switch_extent(unit, project, target_sha256, emitted, linked):
    """Accept only the fixed whole 1583-byte ordinary C5 command executor."""
    meta = unit.get('extended_extent')
    if (not isinstance(meta, dict) or set(meta) != {
            'kind', 'raw_span_evidence', 'next_entry_evidence', 'omitted_byte_xref_evidence'}
            or meta.get('kind') != 'dual_inline_switch_6167_v1'
            or target_sha256 != TARGET_SHA256 or unit.get('id') != 'run_command_6167'
            or unit.get('symbol') != '_run_command_6167' or unit.get('language') != 'c'
            or unit.get('backend') != 'msc500-omf' or unit.get('flags') != ['/AS', '/Zi']
            or unit.get('code_address') is not None
            or _number(unit['image_offset']) != START-0x10000 or _number(unit['size']) != SIZE
            or not isinstance(meta['omitted_byte_xref_evidence'], list)
            or len(meta['omitted_byte_xref_evidence']) != len(OMITTED)):
        raise ValueError('unsupported fixed dual-switch C extent identity or proof fields')
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    xrefs = [_evidence(project, path, target_sha256, 'xrefs')
             for path in meta['omitted_byte_xref_evidence']]
    evidence = [dossier, raw, following] + xrefs
    if (len({e['analysis_profile']['digest'] for e in evidence}) != 1
            or any(e['analysis_profile']['parameters'].get('target_format') != 'dos-mz' for e in evidence)
            or len({e['evidence_id'] for e in evidence}) != len(evidence)):
        raise ValueError('dual-switch evidence must have distinct identities and one original DOS profile')
    n = dossier['normalized_result']; proc = n['procedure']; body = proc['body']
    ranges = [(_number(r['start']), _number(r['end'])+1) for r in body.get('ranges', [])]
    if (body.get('available') is not True or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True or _number(proc['address']) != START
            or ranges != RANGES or body.get('total_bytes') != 1547 or body.get('span_bytes') != SIZE):
        raise ValueError('dual-switch requires exact five retained ranges and 36 omitted bytes')
    data = raw['normalized_result']; blob = bytes.fromhex(data['bytes_hex'])
    if (data.get('complete') is not True or _number(data['address']) != START
            or _number(raw['parameters']['address']) != START
            or raw['parameters']['length'] != SIZE+NEXT_SIZE
            or data.get('requested_bytes') != SIZE+NEXT_SIZE
            or data.get('returned_bytes') != SIZE+NEXT_SIZE or len(blob) != SIZE+NEXT_SIZE
            or not isinstance(linked, bytes) or len(linked) != SIZE or blob[:SIZE] != linked
            or _hash(linked) != BODY_SHA256 or _hash(blob[SIZE:]) != NEXT_SHA256):
        raise ValueError('dual-switch needs complete original body and authenticated entire next53-byte body')
    next_proc = following['normalized_result']['procedure']; nb = next_proc['body']
    if (nb.get('available') is not True or nb.get('contains_entry') is not True
            or nb.get('non_contiguous') is not False or _number(next_proc['address']) != END
            or nb.get('ranges') != [{'start': hex(END), 'end': hex(END+NEXT_SIZE-1)}]
            or nb.get('span_bytes') != NEXT_SIZE or nb.get('total_bytes') != NEXT_SIZE):
        raise ValueError('dual-switch requires adjacent complete contiguous next53-byte function')
    observed = sorted((_number(b['start']), _number(b['end']),
                       tuple(sorted(_number(a) for a in b['successors'])))
                      for b in n['basic_blocks'])
    if len(observed) != 87 or _hash(json.dumps(observed, separators=(',', ':')).encode()) != CFG_SHA256:
        raise ValueError('dual-switch needs the exact retained87-block CFG')
    starts = {a for a, _, _ in observed}; covered = []; current = None
    for left, right, successors in observed:
        if not START <= left < right <= END or any(a not in starts for a in successors):
            raise ValueError('dual-switch CFG is not closed or has an invalid block')
        if current is not None and left == current[1]: current[1] = right
        else:
            if current is not None: covered.append(tuple(current))
            current = [left, right]
    if current is not None: covered.append(tuple(current))
    if covered != RANGES or sum(b-a for a,b,_ in observed) != 1547:
        raise ValueError('dual-switch CFG must cover every retained byte once and no omitted byte')
    reachable = set(); pending = [START]; graph = {a: s for a, _, s in observed}
    while pending:
        a = pending.pop()
        if a not in reachable: reachable.add(a); pending.extend(graph[a])
    if reachable != starts:
        raise ValueError('dual-switch CFG includes an unreachable claimed block')
    for ref in n.get('incoming_references', []):
        if _number(ref['target_address']) in OMITTED:
            raise ValueError('dual-switch incoming reference enters omitted data or dead code')
    if (sorted(_number(e['parameters']['address']) for e in xrefs) != OMITTED
            or any(e['normalized_result'] != [] for e in xrefs)):
        raise ValueError('all36 omitted bytes need distinct empty original global xref results')
    required = {}
    for gap, dispatch, table, resume, targets in SWITCHES:
        g, d, t, r = (x-START for x in (gap, dispatch, table, resume))
        for at in (g-2, g):
            if (linked[at] != 0xeb or START+at+2
                    + int.from_bytes(linked[at+1:at+2], 'little', signed=True) != resume):
                raise ValueError('dual-switch dead jump must duplicate the preceding live jump')
        if (linked[d:d+7] != bytes.fromhex('2d01003d070077')
                or dispatch+8+int.from_bytes(linked[d+7:d+8], 'little', signed=True) != resume
                or linked[d+8:t-2] != bytes.fromhex('03c0932effa7')
                or int.from_bytes(linked[t-2:t], 'little') != table-0x10000
                or [0x10000+int.from_bytes(linked[a:a+2], 'little') for a in range(t,r,2)] != targets
                or any(a not in starts or not START <= a < gap for a in targets)):
            raise ValueError('dual-switch bound, dispatcher, table words or case starts differ')
        required[t-2] = 'dispatch'
        required.update({at: 'table' for at in range(t,r,2)})
    if linked[-6:] != bytes.fromhex('5e5f8be55dc3'):
        raise ValueError('dual-switch final register/stack restoration differs')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != unit['symbol']
            or emitted.get('boundary') != 'codeview3_procedure' or emitted.get('size') != SIZE
            or type(emitted.get('offset')) is not int or emitted['offset'] < 0
            or emitted.get('end') != emitted['offset']+SIZE
            or type(emitted.get('segment')) is not int or emitted['segment'] <= 0
            or not isinstance(emitted.get('fixups'), list)):
        raise ValueError('dual-switch requires entire independent fresh CodeView1583 procedure')
    supplied = set(); used = set(); base = emitted['offset']; seg = emitted['segment']
    for f in emitted['fixups']:
        at = f.offset-base
        if (f.segment != seg or type(f.width) is not int or f.width <= 0
                or not 0 <= at < at+f.width <= SIZE
                or used.intersection(range(at,at+f.width))):
            raise ValueError('dual-switch fresh fixup out of bounds or overlapping')
        used.update(range(at,at+f.width))
        omitted_overlap = any(START+x in OMITTED for x in range(at,at+f.width))
        if at in required:
            frame = (5,None) if required[at] == 'dispatch' else (0,seg)
            if (f.width != 2 or f.location_type != 1 or f.segment_relative is not True
                    or f.target != (0,seg) or f.frame != frame or (f.displacement or 0) != 0):
                raise ValueError('dual-switch requires actual own-CODE OFFSET16 table/dispatch fixup')
            supplied.add(at)
        elif omitted_overlap:
            raise ValueError('dual-switch extra fresh fixup overlaps omitted table or dead jump')
    if supplied != set(required):
        raise ValueError('dual-switch fresh OMF must own both dispatch fields and all16 table words')
    return {'kind':meta['kind'], 'body_evidence_id':dossier['evidence_id'],
            'raw_span_evidence_id':raw['evidence_id'], 'next_entry_evidence_id':following['evidence_id'],
            'omitted_byte_xref_evidence_ids':[e['evidence_id'] for e in xrefs],
            'span_bytes':SIZE, 'reachable_body_bytes':1547, 'closed_cfg_blocks':87,
            'omitted_dead_jump_bytes':4, 'omitted_table_bytes':32, 'compiler_own_CODE_fixups':len(supplied),
            'body_sha256':BODY_SHA256, 'next_complete_body_bytes':NEXT_SIZE,
            'next_complete_body_sha256':NEXT_SHA256, 'next_entry':hex(END),
            'compiler_boundary':'codeview3_procedure'}
