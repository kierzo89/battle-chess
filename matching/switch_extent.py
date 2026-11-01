"""Strict proof of one compiler-emitted six-entry inline switch table.

Every byte still comes from fresh C output and must equal the complete retained
raw span. This proof accounts for two particular omissions from REA's reachable
body: a duplicate short branch and the dispatcher's six code-offset words.
"""
from extent import _evidence, _number

RETURN_TAILS = {
    'inline_switch_table_v1': bytes.fromhex('5e8be55dc3'),
    'inline_switch_zero_return_v1': bytes.fromhex('c746fe00002bc0eb005e5f8be55dc3'),
}


def validate_switch_extent(unit, project, target_sha256, emitted, linked):
    meta = unit.get('extended_extent')
    if (not isinstance(meta, dict) or set(meta) != {
            'kind', 'raw_span_evidence', 'next_entry_evidence'}
            or meta.get('kind') not in RETURN_TAILS
            or unit.get('language') != 'c'):
        raise ValueError('unsupported inline switch extent proof')
    return_tail = RETURN_TAILS[meta['kind']]
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    if len({e['analysis_profile']['digest'] for e in (dossier, raw, following)}) != 1:
        raise ValueError('switch extent analysis profiles differ')
    start, size = 0x10000 + _number(unit['image_offset']), _number(unit['size'])
    end = start + size
    n = dossier['normalized_result']
    proc, body = n['procedure'], n['procedure']['body']
    ranges = body.get('ranges', [])
    if (not body.get('available') or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True or len(ranges) != 3
            or _number(proc['address']) != start):
        raise ValueError('switch proof requires three complete body ranges')
    spans = [(_number(r['start']), _number(r['end']) + 1) for r in ranges]
    (a, branch), (dispatch, table), (epilogue, z) = spans
    if (a != start or z != end or not a < branch < dispatch < table < epilogue < z
            or dispatch - branch != 2 or table - dispatch != 16
            or epilogue - table != 12 or z - epilogue != len(return_tail)
            or body.get('total_bytes') != size - 14 or body.get('span_bytes') != size):
        raise ValueError('switch ranges must account for exactly two omitted regions')
    data = raw['normalized_result']
    blob = bytes.fromhex(data['bytes_hex'])
    if (data.get('complete') is not True or _number(data['address']) != start
            or _number(raw['parameters']['address']) != start
            or raw['parameters']['length'] != len(blob)
            or data.get('returned_bytes') != len(blob)
            or data.get('requested_bytes') != len(blob) or len(blob) < size + 3):
        raise ValueError('switch requires complete raw span and adjacent entry')
    if not isinstance(linked, bytes) or len(linked) != size or blob[:size] != linked:
        raise ValueError('switch raw span differs from complete freshly linked procedure')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != unit.get('symbol')
            or emitted.get('boundary') != 'codeview3_procedure'
            or emitted.get('size') != size
            or emitted.get('end', -1) - emitted.get('offset', 0) != size):
        raise ValueError('fresh CodeView extent must cover entire switch procedure')
    b, d, t, e = (x - start for x in (branch, dispatch, table, epilogue))
    # Both branches end at the shared epilogue. The second is unreachable.
    for offset in (b - 2, b):
        if (blob[offset] != 0xeb or start + offset + 2
                + int.from_bytes(blob[offset+1:offset+2], 'little', signed=True) != epilogue):
            raise ValueError('omitted switch branch must duplicate its predecessor')
    # SUB AX,1; CMP AX,5; JA epilogue; ADD AX,AX; XCHG AX,BX;
    # JMP word ptr CS:[BX+table]. Bound five establishes exactly six words.
    if (blob[d:d+7] != bytes.fromhex('2d01003d050077')
            or dispatch + 8 + int.from_bytes(blob[d+7:d+8], 'little', signed=True) != epilogue
            or blob[d+8:t-2] != bytes.fromhex('03c0932effa7')
            or int.from_bytes(blob[t-2:t], 'little') != table - 0x10000
            or blob[e:e+len(return_tail)] != return_tail):
        raise ValueError('switch dispatcher, bounds, table address or epilogue differ')
    targets = [0x10000 + int.from_bytes(blob[i:i+2], 'little') for i in range(t, e, 2)]
    blocks = n['basic_blocks']
    starts = {_number(block['start']) for block in blocks}
    if any(not start <= target < branch or target not in starts for target in targets):
        raise ValueError('switch table target must begin a retained case block')
    predecessors = [block for block in blocks if _number(block['start']) == branch - 2]
    dispatchers = [block for block in blocks if _number(block['start']) == table - 5]
    bounds = [block for block in blocks if _number(block['start']) == dispatch]
    if (len(predecessors) != 1 or _number(predecessors[0]['end']) != branch
            or [_number(x) for x in predecessors[0]['successors']] != [epilogue]
            or len(dispatchers) != 1 or _number(dispatchers[0]['end']) != table
            or {_number(x) for x in dispatchers[0]['successors']} != set(targets)
            or len(bounds) != 1 or _number(bounds[0]['end']) != dispatch + 8
            or {_number(x) for x in bounds[0]['successors']} != {dispatch + 8, epilogue}):
        raise ValueError('retained CFG must prove bounds, case targets and predecessor')
    if meta['kind'] == 'inline_switch_zero_return_v1':
        zero_return = [block for block in blocks if _number(block['start']) == epilogue]
        restore = [block for block in blocks if _number(block['start']) == epilogue + 9]
        if (len(zero_return) != 1 or _number(zero_return[0]['end']) != epilogue + 9
                or [_number(x) for x in zero_return[0]['successors']] != [epilogue + 9]
                or len(restore) != 1 or _number(restore[0]['end']) != end
                or restore[0]['successors'] != []):
            raise ValueError('switch zero-return tail must reach the shared register restore')
    for block in blocks:
        left, right = _number(block['start']), _number(block['end'])
        for low, high in ((branch, dispatch), (table, epilogue)):
            if left < high and right > low:
                raise ValueError('retained CFG overlaps omitted switch region')
            if any(low <= _number(x) < high for x in block['successors']):
                raise ValueError('retained CFG branches into omitted switch region')
    # Fresh OMF must identify the dispatcher operand and every table word as
    # actual CODE OFFSET16 relocations, rather than merely matching raw values.
    required = {emitted['offset'] + x for x in (t-2, *range(t, e, 2))}
    supplied = set()
    for fixup in emitted.get('fixups', []):
        if fixup.offset in required:
            if (fixup.width != 2 or fixup.location_type != 1 or not fixup.segment_relative
                    or fixup.segment != emitted['segment']
                    or fixup.target != (0, emitted['segment'])
                    or fixup.frame not in ((0, emitted['segment']), (5, None))):
                raise ValueError('switch table requires own-CODE OFFSET16 fixups')
            if fixup.offset in supplied:
                raise ValueError('duplicate switch CODE fixup')
            supplied.add(fixup.offset)
    if supplied != required:
        raise ValueError('fresh compiler must emit all seven switch CODE fixups')
    next_proc = following['normalized_result']['procedure']
    next_body = next_proc['body']
    if (not next_body.get('available') or not next_body.get('contains_entry')
            or next_body.get('non_contiguous') is not False
            or len(next_body.get('ranges', [])) != 1
            or _number(next_proc['address']) != end
            or _number(next_body['ranges'][0]['start']) != end
            or _number(next_body['ranges'][0]['end']) < end
            or blob[size:size+3] != bytes.fromhex('558bec')):
        raise ValueError('switch next retained entry must be adjacent')
    return {'kind': meta['kind'], 'body_evidence_id': dossier['evidence_id'],
            'raw_span_evidence_id': raw['evidence_id'],
            'next_entry_evidence_id': following['evidence_id'], 'span_bytes': size,
            'reachable_body_bytes': size-14, 'unreachable_branch': hex(branch),
            'table_address': hex(table), 'table_bytes': 12,
            'case_targets': [hex(x) for x in targets],
            'compiler_code_fixups': len(supplied), 'next_entry': hex(end),
            'return_tail_address': hex(epilogue), 'return_tail_bytes': len(return_tail),
            'compiler_boundary': 'codeview3_procedure'}
