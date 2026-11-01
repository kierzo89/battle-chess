"""Fixed C5 step872A proof: 236 native code bytes plus 15 own-CODE words.

This profile grants only the observed 266-byte procedure. It does not infer
function boundaries from PUBLICs, accept a generic switch span, or edit OMF.
"""
from extent import _evidence, _number

KIND = 'step_switch_872a_v1'
ORIGINAL = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
START, SIZE, TABLE, EPILOGUE = 0x1872a, 266, 0x18812, 0x18830
TARGETS = (0x1875d, 0x18830, 0x18830, 0x18830, 0x18751,
           0x18789, 0x18791, 0x18799, 0x18830, 0x187a0,
           0x187d2, 0x18830, 0x18830, 0x18762, 0x1877a)
# Complete closed native CFG, offsets relative to the actual native entry.
CFG = (
 (0,8,(8,15)), (8,15,()), (15,28,(28,31)), (28,31,(262,)),
 (31,34,(34,)), (34,39,(39,51,56,80,95,103,111,118,168,262)),
 (39,42,(42,)), (42,51,(262,)), (51,56,(42,)),
 (56,63,(42,63)), (63,69,(69,)), (69,80,(42,)),
 (80,87,(42,87)), (87,95,(69,)), (95,103,(42,)),
 (103,111,(42,)), (111,118,(42,)), (118,125,(125,136)),
 (125,133,(133,136)), (133,136,(136,)), (136,151,(151,154)),
 (151,154,(154,)), (154,161,(42,161)), (161,168,(219,)),
 (168,175,(175,186)), (175,183,(183,186)), (183,186,(186,)),
 (186,201,(201,204)), (201,204,(204,)), (204,211,(211,214)),
 (211,214,(42,)), (214,219,(219,)), (219,221,(221,224)),
 (221,224,(42,)), (224,232,(262,)), (262,266,()))


def validate_step_extent(unit, project, target_sha256, emitted, linked):
    meta = unit.get('extended_extent')
    if (not isinstance(meta, dict) or set(meta) != {
            'kind', 'raw_span_evidence', 'next_entry_evidence', 'table_xref_evidence'}
            or meta.get('kind') != KIND or target_sha256 != ORIGINAL
            or unit.get('language') != 'c' or unit.get('symbol') != '_step_872a'
            or _number(unit['image_offset']) != START-0x10000
            or _number(unit['size']) != SIZE
            or unit.get('backend') != 'msc500-omf'
            or unit.get('flags') != ['/AS', '/Gs', '/Os', '/Zi']
            or not isinstance(meta['table_xref_evidence'], list)
            or len(meta['table_xref_evidence']) != 30):
        raise ValueError('step extent requires the fixed C500 872A profile')
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    xrefs = [_evidence(project, p, target_sha256, 'xrefs') for p in meta['table_xref_evidence']]
    if len({e['analysis_profile']['digest'] for e in [dossier, raw, following]+xrefs}) != 1:
        raise ValueError('step analysis profiles differ')
    n = dossier['normalized_result'];proc = n['procedure'];body = proc['body']
    ranges = [(_number(x['start']), _number(x['end'])+1) for x in body.get('ranges', [])]
    if (body.get('available') is not True or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True
            or _number(proc['address']) != START
            or ranges != [(START, TABLE), (EPILOGUE, START+SIZE)]
            or body.get('total_bytes') != 236 or body.get('span_bytes') != SIZE):
        raise ValueError('step requires the exact two native ranges and 30-byte table')
    observed = [(_number(b['start'])-START, _number(b['end'])-START,
                 tuple(sorted(_number(x)-START for x in b['successors'])))
                for b in n['basic_blocks']]
    if sorted(observed) != sorted(CFG):
        raise ValueError('step requires all 36 exact closed native CFG blocks')
    addresses=[]
    for e in xrefs:
        address=_number(e['parameters']['address']);addresses.append(address)
        if e['normalized_result'] != []:
            raise ValueError('step table byte has a global incoming reference')
    if sorted(addresses) != list(range(TABLE, EPILOGUE)):
        raise ValueError('step requires one global xref query for every table byte')
    d=raw['normalized_result'];blob=bytes.fromhex(d['bytes_hex'])
    if (d.get('complete') is not True or _number(d['address']) != START
            or _number(raw['parameters']['address']) != START
            or raw['parameters']['length'] != len(blob)
            or d.get('requested_bytes') != len(blob) or d.get('returned_bytes') != len(blob)
            or len(blob) < SIZE+4):
        raise ValueError('step requires complete raw bytes including actual adjacent entries')
    if not isinstance(linked, bytes) or len(linked) != SIZE or blob[:SIZE] != linked:
        raise ValueError('step complete raw span differs from freshly linked CV bytes')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != '_step_872a'
            or emitted.get('boundary') != 'codeview3_procedure'
            or emitted.get('size') != SIZE
            or emitted.get('end', -1)-emitted.get('offset',0) != SIZE):
        raise ValueError('step requires the independent complete 266-byte CodeView extent')
    # Unsigned selector range 3..17: SUB AX,3; CMP AX,14; JBE dispatch;
    # JMP poll/return; double index; CS-indirect jump to exactly 15 words.
    if (blob[15:39] != bytes.fromhex('a056982ae42d03003d0e007603e9e70003c0932effa71288')
            or blob[230:232] != bytes.fromhex('eb1e')
            or blob[262:266] != bytes.fromhex('e87702c3')):
        raise ValueError('step selector bounds, dispatcher, table predecessor or epilogue differ')
    targets=tuple(0x10000+int.from_bytes(blob[i:i+2],'little')for i in range(232,262,2))
    if targets != TARGETS:
        raise ValueError('step requires the exact fifteen retained case/default targets')
    required={emitted['offset']+x for x in (37,*range(232,262,2))};supplied=set()
    for f in emitted.get('fixups',[]):
        if f.offset not in required:
            # Any other relocation touching the omitted table must be rejected.
            if any(f.offset < address+2 and f.offset+f.width > address for address in required):
                raise ValueError('step has an undeclared or overlapping table fixup')
            if f.segment_relative and f.target == (0, emitted['segment']):
                raise ValueError('unexpected additional step own-CODE field')
            continue
        if (f.width != 2 or f.location_type != 1 or not f.segment_relative
                or f.segment != emitted['segment'] or f.target != (0,emitted['segment'])
                or f.frame not in ((0,emitted['segment']),(5,None))):
            raise ValueError('step requires actual own-CODE OFFSET16 table/dispatcher fixups')
        if f.offset in supplied:raise ValueError('duplicate step CODE fixup')
        supplied.add(f.offset)
    if supplied != required:
        raise ValueError('step requires all sixteen actual compiler CODE fixups')
    next_n=following['normalized_result'];next_p=next_n['procedure'];next_b=next_p['body']
    if (next_b.get('available') is not True or next_b.get('contains_entry') is not True
            or next_b.get('non_contiguous') is not False
            or _number(next_p['address']) != START+SIZE
            or next_b.get('ranges') != [{'start':hex(START+SIZE),'end':hex(START+SIZE)}]
            or next_b.get('total_bytes') != 1 or next_b.get('span_bytes') != 1
            or next_n['basic_blocks'] != [{'start':hex(START+SIZE),'end':hex(START+SIZE+1),'successors':[]}]
            or blob[SIZE:SIZE+4] != bytes.fromhex('c3b80100')):
        raise ValueError('step must end before the actual adjacent RET1 and prompt entry')
    return dict(kind=KIND,body_evidence_id=dossier['evidence_id'],raw_span_evidence_id=raw['evidence_id'],
                next_entry_evidence_id=following['evidence_id'],span_bytes=SIZE,reachable_body_bytes=236,
                table_address=hex(TABLE),table_bytes=30,case_targets=[hex(x)for x in targets],
                compiler_code_fixups=16,closed_CFG_blocks=36,empty_global_table_byte_xrefs=30,
                next_entry=hex(START+SIZE),compiler_boundary='codeview3_procedure')
