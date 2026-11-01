"""Fixed FE59 proof for original bytes analyzed in their recovered CS frame.

Analysis carriers are reconstructed only for identity checks, never used as
compiler/linker inputs. This is deliberately not a general rebasing facility.
"""
import hashlib
import json
from pathlib import Path
import struct

TARGET = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
PROFILE = '394ece2538bed893dc845d9dc51ef77bd51bbe6e8caaa085003f3d8135fe775d'
MAPPING = 'original_image=derived_loaded_address-0x10000+0xfdf0'


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError('invalid segmented extent number')
    return int(value, 0) if isinstance(value, str) else value


def _read(project, relative):
    if not isinstance(relative, str):
        raise ValueError('segmented evidence path must be a string')
    path = (project / relative).resolve()
    if not path.is_relative_to(project):
        raise ValueError('segmented evidence outside matching project')
    return json.loads(path.read_text())


def _evidence(project, relative, digest, name, operation):
    e = _read(project, relative)
    profile = json.dumps(e['analysis_profile'], sort_keys=True, separators=(',', ':')).encode()
    subject = e['subject']
    if (subject['digest']['sha256'] != digest or subject['name'] != name
            or subject['format'] != 'dos-mz' or subject['architecture'] != 'x86'
            or e['operation'] != operation or _sha(profile) != PROFILE):
        raise ValueError('segmented evidence subject/profile/operation mismatch')
    return e


def _carriers(project, meta, original):
    manifest = _read(project, meta['carrier_evidence'])
    code = original[512 + 0xfdf0:512 + 0x10d30]
    if (len(code) != 3904 or manifest['original_sha256'] != TARGET
            or manifest['original_code_sha256'] != _sha(code)
            or manifest['original_image_start'] != '0xfdf0'
            or manifest['original_image_end'] != '0x10d30'
            or manifest['mapping'] != MAPPING or len(manifest['carriers']) != 2):
        raise ValueError('segmented carrier original bytes/mapping mismatch')
    digests = {}
    for record, name, stub in zip(manifest['carriers'], ['EVALCS0.EXE', 'EVALCALL.EXE'],
                                   [b'', bytes.fromhex('9a69000000b8004ccd21')]):
        size = 32 + len(code) + len(stub)
        entry = len(code) if stub else 0x69
        header = bytearray(32)
        struct.pack_into('<14H', header, 0, 0x5a4d, size % 512, (size+511)//512,
                         int(bool(stub)), 2, 0, 0xffff, 0, 0xfffe, 0, entry, 0, 0x1c, 0)
        if stub:
            struct.pack_into('<HH', header, 0x1c, len(code)+3, 0)
        digest = _sha(bytes(header) + code + stub)
        if (Path(record['path']).name != name or record['sha256'] != digest
                or record['header_hex'] != header.hex()
                or record['image_bytes'] != len(code)+len(stub)
                or record['original_code_bytes'] != len(code)
                or record['entry_ip'] != hex(entry)
                or record['analysis_stub_hex'] != stub.hex()
                or record['mz_sites'] != ([len(code)+3] if stub else [])):
            raise ValueError('segmented carrier header/stub/hash mismatch')
        digests[name] = digest
    return digests['EVALCALL.EXE']


def validate_segmented_extent(unit, project, target_sha256, emitted, linked):
    """Accept only the original FE59/2803 corrected-CS dossier and dead EB2F.

    The caller supplies fresh complete CodeView metadata and linked bytes; no
    credit is possible until every one of the 2803 bytes equals the original.
    """
    project = Path(project).resolve()
    meta = unit.get('extended_extent')
    keys = {'kind', 'carrier_evidence', 'derived_body_evidence', 'raw_span_evidence',
            'next_entry_evidence', 'gap_xref_evidence'}
    if (not isinstance(meta, dict) or set(meta) != keys
            or meta['kind'] != 'segmented_evaluation_v1' or unit.get('language') != 'c'
            or _number(unit['image_offset']) != 0xfe59 or _number(unit['size']) != 2803
            or unit.get('code_address') != {'segment': 0xfdf, 'offset': 0x69}
            or not isinstance(meta['gap_xref_evidence'], list)
            or len(meta['gap_xref_evidence']) != 2):
        raise ValueError('segmented extent is restricted to FE59 CS0FDF:0069 size2803')
    original = (project.parent / 'CHESS.EXE').read_bytes()
    if (target_sha256 != TARGET or _sha(original) != TARGET or original[:2] != b'MZ'
            or struct.unpack_from('<H', original, 8)[0] * 16 != 512):
        raise ValueError('segmented extent original target hash/header mismatch')
    derived_sha = _carriers(project, meta, original)
    weak = _evidence(project, unit['rea_evidence'], TARGET, 'CHESS.EXE', 'analyze_function')
    dossier = _evidence(project, meta['derived_body_evidence'], derived_sha,
                        'EVALCALL.EXE', 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], derived_sha, 'EVALCALL.EXE', 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], TARGET, 'CHESS.EXE', 'analyze_function')
    xrefs = [_evidence(project, path, derived_sha, 'EVALCALL.EXE', 'xrefs')
             for path in meta['gap_xref_evidence']]
    weak_proc = weak['normalized_result']['procedure']
    if (_number(weak_proc['address']) != 0x1fe59
            or weak['parameters']['procedure'] != '0x1fe59'
            or weak_proc['body']['total_bytes'] != 448 or weak_proc['body']['span_bytes'] != 456):
        raise ValueError('segmented proof must retain the original weak FE59 dossier')
    proc = dossier['normalized_result']['procedure']
    body = proc['body']
    if (_number(proc['address']) != 0x10069 or dossier['parameters']['procedure'] != '0x10069'
            or body.get('available') is not True or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True
            or body.get('total_bytes') != 2801 or body.get('span_bytes') != 2803
            or body.get('ranges') != [{'start': '0x10069', 'end': '0x106c1'},
                                      {'start': '0x106c4', 'end': '0x10b5b'}]):
        raise ValueError('segmented body must establish exact corrected ranges')
    data = raw['normalized_result']
    blob = bytes.fromhex(data['bytes_hex'])
    expected = original[512+0xfe59:512+0x1097c]
    if (raw['parameters'] != {'address': '0x10069', 'length': 2851}
            or data.get('complete') is not True or data.get('address') != '0x10069'
            or data.get('requested_bytes') != 2851 or data.get('returned_bytes') != 2851
            or len(blob) != 2851 or blob != expected):
        raise ValueError('segmented raw span/next48 must equal complete pinned original bytes')
    if not isinstance(linked, bytes) or len(linked) != 2803 or linked != blob[:2803]:
        raise ValueError('segmented proof requires all2803 freshly linked bytes equal original')
    gap = 0x106c2 - 0x10069
    if blob[gap-2:gap+2] != bytes.fromhex('eb31eb2f'):
        raise ValueError('segmented gap/predecessor must be EB31 EB2F')
    # Both short jumps target 106F3, beyond the omitted two bytes.
    if 0x106c2 + int.from_bytes(blob[gap-1:gap], 'little', signed=True) != 0x106f3 or \
            0x106c4 + int.from_bytes(blob[gap+1:gap+2], 'little', signed=True) != 0x106f3:
        raise ValueError('segmented gap jumps must share exact forward target')
    blocks = dossier['normalized_result']['basic_blocks']
    observed = sorted((_number(b['start']), _number(b['end']),
                       tuple(_number(a) for a in b['successors'])) for b in blocks)
    if len(observed) != 265 or len({a for a, _, _ in observed}) != 265:
        raise ValueError('segmented CFG requires265 distinct blocks')
    covered, edges = set(), {}
    for left, right, successors in observed:
        if not 0x10069 <= left < right <= 0x10b5c:
            raise ValueError('segmented CFG block outside fixed body')
        span = set(range(left, right))
        if covered & span or span & {0x106c2, 0x106c3}:
            raise ValueError('segmented CFG overlaps blocks or dead gap')
        covered.update(span)
        edges[left] = successors
    if (covered != set(range(0x10069, 0x10b5c)) - {0x106c2, 0x106c3}
            or (0x106c0, 0x106c2, (0x106f3,)) not in observed
            or any(a not in edges for successors in edges.values() for a in successors)):
        raise ValueError('segmented CFG must cover2801 bytes with closed successors')
    pending, reachable = [0x10069], set()
    while pending:
        address = pending.pop()
        if address not in reachable:
            reachable.add(address)
            pending.extend(edges[address])
    if len(reachable) != 265:
        raise ValueError('segmented CFG contains unreachable retained blocks')
    for reference in (dossier['normalized_result'].get('incoming_references', []) +
                      dossier['normalized_result'].get('outgoing_references', [])):
        target = reference.get('target_address')
        if (isinstance(target, str) and target.lower().startswith('0x')
                and _number(target) in (0x106c2, 0x106c3)):
            raise ValueError('segmented retained reference enters dead gap')
    if (sorted(_number(e['parameters']['address']) for e in xrefs) != [0x106c2, 0x106c3]
            or any(e['normalized_result'] != [] for e in xrefs)):
        raise ValueError('segmented gap needs two distinct empty global xref dossiers')
    next_proc = following['normalized_result']['procedure']
    next_body = next_proc['body']
    if (following['parameters']['procedure'] != '0x2094c'
            or _number(next_proc['address']) != 0x2094c
            or next_body.get('available') is not True or next_body.get('contains_entry') is not True
            or next_body.get('non_contiguous') is not False
            or next_body.get('total_bytes') != 48 or next_body.get('span_bytes') != 48
            or next_body.get('ranges') != [{'start': '0x2094c', 'end': '0x2097b'}]
            or blob[2803:2806] != bytes.fromhex('558bec')):
        raise ValueError('segmented next entry must be complete original bitcount1094C/48')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != unit.get('symbol')
            or emitted.get('boundary') != 'codeview3_procedure' or emitted.get('size') != 2803
            or emitted.get('end', -1)-emitted.get('offset', 0) != 2803):
        raise ValueError('segmented proof requires fresh complete CodeView size2803')
    return {'kind': meta['kind'], 'original_body_evidence_id': weak['evidence_id'],
            'derived_body_evidence_id': dossier['evidence_id'], 'carrier_sha256': derived_sha,
            'raw_span_evidence_id': raw['evidence_id'], 'next_entry_evidence_id': following['evidence_id'],
            'gap_xref_evidence_ids': [e['evidence_id'] for e in xrefs],
            'span_bytes': 2803, 'reachable_bytes': 2801, 'cfg_blocks': 265,
            'gap_address': '0x104b2', 'derived_gap_address': '0x106c2',
            'gap_size': 2, 'gap_hex': 'eb2f', 'predecessor_target': '0x104e3',
            'next_entry': '0x1094c', 'compiler_boundary': 'codeview3_procedure'}
