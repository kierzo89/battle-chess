"""Staged source-only allocation inputs. This module awards no match credit.

Candidate for matching/source_inputs.py; no imports from check.py and no score
mutation. The deliberately fixed backend currently admits just one reviewed
8-object COMMON contribution. Broader BSS forms need separate review.
"""
from pathlib import Path
import dataclasses
import hashlib
import json
import re
import struct
import sys

PROJECT = next(p for p in Path(__file__).resolve().parents if (p / 'config/msc500.json').is_file())
sys.path.insert(0, str(PROJECT))
from msc import compile_c
from omf import read_omf, _Cursor
from reference import build_reference, ORIGINAL_SHA256

BACKEND = 'msc500-near-common-source-v1'
FLAGS = ['/AS', '/Zl', '/Zi']
NAMES = ['_setup_offsets', '_setup_lengths', '_asset_offsets', '_asset_lengths',
         '_startup_offsets_9648', '_startup_lengths_a8b6', '_pair_offsets',
         '_pair_directory_lengths']
OFFSETS = [0x9240, 0x987a, 0x8de4, 0x9848, 0x9648, 0xa8b6, 0x817c, 0x8d00]
SOURCE = 'src/link/asset_selectors.c'
SOURCE_SHA = '9787e688f4d797a86f70c854eacef8711f44cc154eb0a941525ff57ec1fd7daa'
OBJECT_SHA = '19ab4b9415bf6c0ccfee51acb3a36cf66267e83502fabba97ce8072a6df4e8de'
MANIFEST_SHA = 'd2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def local(project, name):
    path = (project / name).resolve()
    require(path.is_relative_to(project.resolve()), 'input path escapes project')
    return path


def pinned(project, row):
    data = local(project, row['path']).read_bytes()
    require(sha(data) == row['sha256'], 'source-input evidence pin mismatch')
    return data


def validate_object(data):
    """Check the complete OMF module, including debug-only relocations."""
    obj = read_omf(data)  # validates all record lengths/checksums and MODEND EOF
    require(not obj.publics and not obj.procedures, 'COMMON input defines public/function')
    expected_segments = [('_TEXT', 'CODE', 0, 0x48), ('_DATA', 'DATA', 0, 0x48),
                         ('CONST', 'CONST', 0, 0x48), ('_BSS', 'BSS', 0, 0x48),
                         ('$$SYMBOLS', 'DEBSYM', 198, 0x20),
                         ('$$TYPES', 'DEBTYP', 139, 0x20)]
    require([(s.name, s.class_name, s.length, s.attributes) for s in obj.segments.values()]
            == expected_segments, 'nondebug allocation or unreviewed debug segment')
    allowed = {0x80, 0x88, 0x96, 0x98, 0x9a, 0x8c, 0xb0, 0x9c, 0xa0, 0x8a}
    require(all(kind in allowed for kind, _, _ in obj.records), 'unreviewed OMF record')
    commons = []
    for kind, _, payload in obj.records:
        if kind == 0xb0:
            c = _Cursor(payload)
            while c:
                name, typ, datatype, size = c.name(), c.index(), c.byte(), c.byte()
                require(datatype == 0x62 and size == 4, 'not near COMMON size4')
                commons.append({'symbol': name, 'size': size, 'datatype': datatype,
                                'type_index': typ})
        elif kind == 0x88:
            require(payload in (bytes.fromhex('009d30734f'), bytes.fromhex('00a1014356'),
                                bytes.fromhex('00a201')), 'unreviewed linker directive')
        elif kind == 0x8a:
            require(payload == b'\x00', 'allocation object has entry point')
        elif kind == 0x9a:
            require(payload == bytes.fromhex('02ff03ff04ff02'), 'unreviewed group')
    require([r['symbol'] for r in commons] == NAMES, 'missing/duplicate/extra/reordered COMMON')
    require([r['type_index'] for r in commons] == [524, 524, 198, 198, 198, 198, 525, 525],
            'unreviewed COMMON type')
    require(obj.externals == dict(enumerate(['__acrtused'] + NAMES, 1)),
            'unexpected external definition/dependency')
    require(len(obj.fixups) == 8, 'unreviewed fixup count')
    expected = list(zip([169, 148, 119, 90, 68, 46, 24, 2], range(9, 1, -1)))
    for fixup, (offset, target) in zip(obj.fixups, expected):
        require((fixup.segment, fixup.offset, fixup.width, fixup.location_type,
                 fixup.segment_relative, fixup.frame, fixup.target, fixup.displacement)
                == (5, offset, 4, 3, True, (5, None), (2, target), None),
                'nondebug or unreviewed CodeView fixup')
    require(all(seg in (5, 6) for _, seg, _, _ in obj.data_writes),
            'initialized nondebug bytes')
    # Pin complete CV payloads too: a changed debug type cannot silently turn a
    # far pointer into an unrelated four-byte object under the fixed profile.
    require(sha(data) == OBJECT_SHA, 'complete reviewed COMMON object changed')
    return commons


def validate_evidence(project, pins, target):
    require(set(pins) == {'layout', 'proposals', 'native', 'crt', 'linked_exe', 'linked_map',
            'runtime', 'linker', 'probe', 'setup_source', 'harness_source'}, 'evidence set incomplete')
    proof = json.loads(pinned(project, pins['layout']))
    proposals = json.loads(pinned(project, pins['proposals']))
    native = json.loads(pinned(project, pins['native']))
    crt = json.loads(pinned(project, pins['crt']))
    for record in (native, crt):
        require(record['subject']['digest']['sha256'] == ORIGINAL_SHA256,
                'primary target identity mismatch')
    require(proof['native_primary']['id'] == native['evidence_id'] and
            proof['CRT_primary']['id'] == crt['evidence_id'], 'primary evidence identity')
    body = native['normalized_result']['procedure']['body']
    require(body['total_bytes'] == body['span_bytes'] == 97 and
            body['ranges'] == [{'start': '0x129b9', 'end': '0x12a19'}], 'native store extent')
    raw = target.read_bytes()
    require(sha(raw) == ORIGINAL_SHA256, 'original target pin mismatch')
    reference = build_reference(raw)
    code = reference['image'][0x29b9:0x2a1a]
    require(len(code) == 97 and code[-1] == 0xc3, 'native setup extent/raw return')
    stores = []
    for i in range(16):
        instruction = code[i*6:i*6+6]
        require(instruction[:2] == b'\xc7\x06', 'native WORD store encoding')
        dest, value = struct.unpack_from('<HH', instruction, 2)
        stores.append({'instruction_image': hex(0x29b9+i*6),
                       'DS_destination': hex(dest), 'value': hex(value), 'write_bytes': 2})
    require(stores == proof['native_store_widths'], 'native store proof mismatch')
    clear = bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
    require(reference['image'][0xeaed:0xeaed+len(clear)] == clear, 'native CRT clear')
    cr = crt['normalized_result']
    require(cr['complete'] and cr['requested_bytes'] == cr['returned_bytes'] == 179 and
            cr['address'] == '0x1ea86' and
            bytes.fromhex(cr['bytes_hex'])[0xeaed-0xea86:0xeaed-0xea86+len(clear)] == clear,
            'CRT primary does not authenticate clear bounds')
    require(len(proposals) == 8 and proposals == proof['allocation_manifest_proposals'],
            'allocation proposals differ from reviewed proof')
    constraints = []
    for row, name, offset in zip(proposals, NAMES, OFFSETS):
        require(row['symbol'] == name and row['bytes'] == 4 and row['initializer'] is None and
                row['source_sha256'] == SOURCE_SHA, 'proposal definition mismatch')
        require(row['required_final_map'] == {'dgroup_segment': '0x5cc2',
                'dgroup_offset': hex(offset), 'end_exclusive': hex(offset+4),
                'inside_startup_clear': ['0x52cc', '0xcbe0']}, 'MAP constraint mismatch')
        require(0x52cc <= offset < offset+4 <= 0xcbe0 and
                0x5cc20+offset >= len(reference['image']), 'not uninitialized CRT-cleared storage')
        pair = next(i for i, store in enumerate(stores) if int(store['DS_destination'], 0) == offset)
        require(pair % 2 == 0 and int(stores[pair+1]['DS_destination'], 0) == offset+2 and
                int(stores[pair+1]['value'], 0) == 0x5cc2 and row['native_stores'] == stores[pair:pair+2],
                'native far-pointer store pair mismatch')
        constraints.append({'symbol': name, **row['required_final_map'], 'resolved': False})
    actual = proof['actual_LINK']
    require(actual['harness_exit_zero'] and actual['zero_checked_before_setup'] == 8 and
            actual['all_pointer_identities_checked_after_setup'] == 8 and
            actual['all_four_last_length_records_checked'] and
            actual['original_read_or_mounted_during_build_or_run'] is False and
            proof['original_aggregate_placement_or_order_proven'] is False,
            'real LINK/runtime controls missing')
    require(sha(pinned(project, pins['linked_exe'])) == actual['EXE_sha256'], 'LINK EXE pin')
    require(pinned(project, pins['linked_map']).decode('cp437').replace('\r\n', '\n') == actual['MAP'], 'LINK MAP pin')
    pinned(project, pins['runtime'])
    require(pins['runtime']['sha256'] == actual['runtime_sha256'], 'runtime library pin')
    require(pins['linker']['sha256'] == actual['linker_sha256'], 'LINK tool pin')
    pinned(project, pins['linker'])
    require(sha(pinned(project, pins['probe'])) == proof['probe_sha256'], 'LINK probe pin')
    for key, name in [('setup_source', 'SETUP'), ('harness_source', 'MAIN')]:
        require(sha(pinned(project, pins[key])) == proof['compiles'][name]['source_sha256'],
                'executed source pin')
    exe = pinned(project, pins['linked_exe'])
    header = struct.unpack_from('<H', exe, 8)[0]*16
    image = exe[header:]
    table = struct.unpack_from('<H', exe, 24)[0]
    sites = {struct.unpack_from('<H', exe, table+4*i)[0] +
             16*struct.unpack_from('<H', exe, table+4*i+2)[0]
             for i in range(struct.unpack_from('<H', exe, 6)[0])}
    map_text = actual['MAP'].split('Publics by Name')[1].split('Publics by Value')[0]
    def public(name):
        hits = re.findall(r'(?im)^\s*([0-9a-f]{4}):([0-9a-f]{4})\s+' + re.escape(name) + r'\s*$', map_text)
        require(len(hits) == 1, 'real LINK public missing/ambiguous')
        return tuple(int(part, 16) for part in hits[0])
    dgroup, edata = public('_edata')
    endseg, end = public('_end')
    require(endseg == dgroup and edata == actual['edata'] and end == actual['end'], 'real LINK clear bounds')
    linked_clear = b'\xbf'+struct.pack('<H', edata)+b'\xb9'+struct.pack('<H', end)+b'\x2b\xcf\x33\xc0\xf3\xaa'
    require(image[actual['CRT_clear_image_site']:actual['CRT_clear_image_site']+len(linked_clear)] == linked_clear,
            'actual linked CRT clear encoding')
    allocations = []
    for name in NAMES:
        segment, offset = public(name)
        require(segment == dgroup and edata <= offset < offset+4 <= end and
                segment*16+offset >= len(image) and
                not any(segment*16+offset <= site < segment*16+offset+4 for site in sites),
                'linked COMMON not wholly uninitialized/CRT-cleared')
        allocations.append({'symbol': name, 'segment': segment, 'offset': offset, 'size': 4,
                            'inside_CRT_clear': True, 'file_backed_bytes': 0})
    require(allocations == actual['allocations'], 'actual allocation MAP report differs')
    return constraints


def COMMON_totals(objects):
    """Explicit near bytes versus FAR element-count*element-bytes accounting."""
    out = {'near': {'contributions': 0, 'definitions': 0, 'bytes': 0},
           'far': {'contributions': 0, 'definitions': 0, 'bytes': 0}}
    for obj in objects:
        kinds = set()
        for row in obj['definitions']:
            kind = row.get('communal_kind', 0x62)
            require(type(kind) is int and kind in (0x61, 0x62), 'unknown COMMON kind')
            name = 'far' if kind == 0x61 else 'near'; kinds.add(name)
            require(type(row['size']) is int and row['size'] >= 0, 'invalid COMMON byte size')
            if kind == 0x61:
                require(row.get('storage') == 'far-common' and
                        type(row.get('element_count')) is int and row['element_count'] > 0 and
                        type(row.get('element_bytes')) is int and row['element_bytes'] > 0 and
                        row['size'] == row['element_count'] * row['element_bytes'],
                        'FAR COMMON size must equal element count times element bytes')
            out[name]['definitions'] += 1; out[name]['bytes'] += row['size']
        for name in kinds: out[name]['contributions'] += 1
    return out


def build_source_inputs(project, target, output, config_path=None, defined_symbols=()):
    """No config means no inputs; reports are separate from every match count."""
    project, output = Path(project).resolve(), Path(output).resolve()
    path = Path(config_path) if config_path else project / 'config/source-inputs.json'
    if not path.exists():
        return {'schema_version': 1, 'objects': [], 'placement_proven': False,
                'matching_credit': 0}
    config = json.loads(path.read_text())
    require(set(config) == {'schema_version', 'source_allocations'} and
            config['schema_version'] == 1 and isinstance(config['source_allocations'], list),
            'unsupported source-input registry schema')
    results, ids, sources, symbols = [], set(), set(), set()
    for item in config['source_allocations']:
        require(set(item) == {'id', 'backend', 'source', 'source_sha256', 'compiler',
                'flags', 'toolchain_manifest_sha256', 'objects', 'evidence'}, 'unknown allocation fields')
        if item['backend'] == 'msc500-near-common-square-coordinate-pointers-v1':
            from square_coordinate_pointers_source_inputs import build_input, NAMES as square_pointer_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(square_pointer_names) and
                    not set(defined_symbols).intersection(square_pointer_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(square_pointer_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-screen-coordinate-pointers-v1':
            from screen_coordinate_pointers_source_inputs import build_input, NAMES as screen_pointer_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(screen_pointer_names) and
                    not set(defined_symbols).intersection(screen_pointer_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(screen_pointer_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-conditional-side-piece-counts-v1':
            from side_piece_counts_source_inputs import build_input, NAMES as side_count_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(side_count_names) and
                    not set(defined_symbols).intersection(side_count_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(side_count_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-far-common-native-capacity-model-v1':
            from far_capacity_source_inputs import build_input, NAMES as far_capacity_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(far_capacity_names) and
                    not set(defined_symbols).intersection(far_capacity_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(far_capacity_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-input-saved-bytes-v1':
            from input_saved_bytes_source_inputs import build_input, NAMES as saved_byte_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(saved_byte_names) and
                    not set(defined_symbols).intersection(saved_byte_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(saved_byte_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-left-right-lists-v1':
            from left_right_lists_source_inputs import build_input, NAMES as list_grid_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(list_grid_names) and
                    not set(defined_symbols).intersection(list_grid_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(list_grid_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-independent-control-cells15-v1':
            from independent_control_cells15_source_inputs import build_input, NAMES as control_cell_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(control_cell_names) and
                    not set(defined_symbols).intersection(control_cell_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(control_cell_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-ui-animation-scalars-v1':
            from ui_animation_scalars_source_inputs import build_input, NAMES as ui_animation_scalar_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(ui_animation_scalar_names) and
                    not set(defined_symbols).intersection(ui_animation_scalar_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(ui_animation_scalar_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-animation-counter9602-v1':
            from animation_counter_source_inputs import build_input, NAMES as animation_counter_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(animation_counter_names) and
                    not set(defined_symbols).intersection(animation_counter_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(animation_counter_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-cursor-actor-index-v1':
            from cursor_actor_index_source_inputs import build_input, NAMES as cursor_actor_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(cursor_actor_names) and
                    not set(defined_symbols).intersection(cursor_actor_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(cursor_actor_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-move-count845e-v1':
            from move_count_source_inputs import build_input, NAMES as move_count_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(move_count_names) and
                    not set(defined_symbols).intersection(move_count_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(move_count_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-piece-square-v1':
            from piece_square_source_inputs import build_input, NAMES as piece_square_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(piece_square_names) and
                    not set(defined_symbols).intersection(piece_square_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(piece_square_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-asset-fixed-arrays-v1':
            from asset_fixed_arrays_source_inputs import build_input, NAMES as asset_four_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(asset_four_names) and
                    not set(defined_symbols).intersection(asset_four_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(asset_four_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-move8-state-v1':
            from move8d12_source_inputs import build_input, NAMES as move8_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(move8_names) and
                    not set(defined_symbols).intersection(move8_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(move8_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-menu-paused-v1':
            from menu_paused_source_inputs import build_input, NAMES as paused_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(paused_names) and
                    not set(defined_symbols).intersection(paused_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(paused_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-packed-pen-v1':
            from packed_pen_source_inputs import build_input, NAMES as packed_pen_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(packed_pen_names) and
                    not set(defined_symbols).intersection(packed_pen_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(packed_pen_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-input-timer-pair-v1':
            from input_timer_source_inputs import build_input, NAMES as input_timer_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(input_timer_names) and
                    not set(defined_symbols).intersection(input_timer_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(input_timer_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-turn-phase-v1':
            from turn_phase_source_inputs import build_input, NAMES as turn_phase_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(turn_phase_names) and
                    not set(defined_symbols).intersection(turn_phase_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(turn_phase_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-rays239-v1':
            from rays239_source_inputs import build_input, NAMES as rays239_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(rays239_names) and
                    not set(defined_symbols).intersection(rays239_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(rays239_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-castle-dialog-event-v1':
            from castle_dialog_event_source_inputs import build_input, NAMES as castle_event_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(castle_event_names) and
                    not set(defined_symbols).intersection(castle_event_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(castle_event_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-event-pointers-unsigned-client-v2':
            from event_pointer_unsigned_source_inputs import build_input, NAMES as event_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(event_names) and
                    not set(defined_symbols).intersection(event_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(event_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-event-pointers-v1':
            from event_pointer_source_inputs import build_input, NAMES as event_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(event_names) and
                    not set(defined_symbols).intersection(event_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(event_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-board-minimum-v1':
            from board_source_inputs import build_input, NAMES as board_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(board_names) and
                    not set(defined_symbols).intersection(board_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(board_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-requested-limit-v1':
            from requested_limit_source_inputs import build_input, NAMES as controls_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(controls_names) and
                    not set(defined_symbols).intersection(controls_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(controls_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-current-controls-v1':
            from current_controls_source_inputs import build_input, NAMES as controls_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(controls_names) and
                    not set(defined_symbols).intersection(controls_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(controls_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-input-display-v1':
            from input_display_source_inputs import build_input, NAMES as input_display_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(input_display_names) and
                    not set(defined_symbols).intersection(input_display_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(input_display_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-evaluation-controls-v1':
            from evaluation_control_source_inputs import build_input, NAMES as evaluation_control_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(evaluation_control_names) and
                    not set(defined_symbols).intersection(evaluation_control_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(evaluation_control_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-ui-words-v1':
            from ui_word_source_inputs import build_input, NAMES as ui_word_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(ui_word_names) and
                    not set(defined_symbols).intersection(ui_word_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(ui_word_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-search-words-v1':
            from search_word_source_inputs import build_input, NAMES as search_word_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(search_word_names) and
                    not set(defined_symbols).intersection(search_word_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(search_word_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-serial-ring-v1':
            from serial_ring_source_inputs import build_input, NAMES as serial_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(serial_names) and
                    not set(defined_symbols).intersection(serial_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(serial_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-arena-snapshot-v1':
            from arena_snapshot_source_inputs import build_input, NAMES as arena_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(arena_names) and
                    not set(defined_symbols).intersection(arena_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(arena_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-setup-word-v1':
            from setup_word_source_inputs import build_input, NAMES as setup_word_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(setup_word_names) and
                    not set(defined_symbols).intersection(setup_word_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(setup_word_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-dialog-v1':
            from dialog_source_inputs import build_input, NAMES as dialog_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(dialog_names) and
                    not set(defined_symbols).intersection(dialog_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(dialog_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-book-v1':
            from book_source_inputs import build_input, NAMES as book_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(book_names) and
                    not set(defined_symbols).intersection(book_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(book_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-side-history-v1':
            from side_history_source_inputs import build_input, NAMES as side_history_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(side_history_names) and
                    not set(defined_symbols).intersection(side_history_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(side_history_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-clock-v1':
            from clock_source_inputs import build_input, NAMES as clock_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(clock_names) and
                    not set(defined_symbols).intersection(clock_names),
                    'duplicate allocation symbol or already matched definition')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(clock_names)
            results.append(built)
            continue
        if item['backend'] == 'msc500-near-common-asset-mode-v1':
            from asset_mode_source_inputs import build_input, NAMES as asset_mode_names
            require(item['id'] not in ids and item['source'] not in sources,
                    'duplicate source allocation')
            require(not symbols.intersection(asset_mode_names) and
                    not set(defined_symbols).intersection(asset_mode_names),
                    'duplicate allocation symbol or already matched definition')
            require('_actors_ready' not in symbols and '_actors_ready' not in set(defined_symbols),
                    'asset-mode cannot allocate separate actors_ready for the same native WORD')
            built = build_input(item, project, target, output, compiler_fn=compile_c)
            ids.add(item['id']); sources.add(item['source']); symbols.update(asset_mode_names)
            results.append(built)
            continue
        require(item['id'] == 'asset-selector-common' and item['id'] not in ids and
                item['source'] not in sources, 'duplicate/unreviewed source allocation')
        ids.add(item['id']); sources.add(item['source'])
        require(item['backend'] == BACKEND and item['compiler'] == 'msc500' and
                item['flags'] == FLAGS and item['source'] == SOURCE and
                item['source_sha256'] == SOURCE_SHA and
                item['toolchain_manifest_sha256'] == MANIFEST_SHA, 'unreviewed source/profile')
        require(item['objects'] == [{'symbol': n, 'size': 4, 'storage': 'near-common'} for n in NAMES],
                'incomplete COMMON selection')
        require(not symbols.intersection(NAMES) and not set(defined_symbols).intersection(NAMES),
                'duplicate allocation symbol or already matched definition')
        symbols.update(NAMES)
        source = local(project, item['source'])
        require(sha(source.read_bytes()) == SOURCE_SHA, 'source pin mismatch')
        constraints = validate_evidence(project, item['evidence'], Path(target))
        compiled = compile_c(source, FLAGS, compiler='msc500')
        require(compiled.source_sha256 == SOURCE_SHA and
                compiled.toolchain_manifest_sha256 == MANIFEST_SHA, 'fresh compiler provenance')
        proof = json.loads(pinned(project, item['evidence']['layout']))
        require(compiled.tool_hashes == proof['compiles']['SELECT']['tool_hashes'], 'fresh tool pin mismatch')
        commons = validate_object(compiled.object_bytes)
        output.mkdir(parents=True, exist_ok=True)
        objpath = output / (item['id'] + '.obj')
        objpath.write_bytes(compiled.object_bytes)
        provenance = dataclasses.asdict(compiled); provenance.pop('object_bytes')
        results.append({'id': item['id'], 'source': item['source'], 'object': str(objpath),
                        'object_sha256': sha(compiled.object_bytes), 'definitions': commons,
                        'allocation_bytes': sum(r['size'] for r in commons),
                        'initialized_bytes': 0, 'matching_credit': 0,
                        'original_map_constraints': constraints,
                        'placement_proven': False, 'compiler': provenance})
    result = {'schema_version': 1, 'objects': results, 'placement_proven': False,
              'matching_credit': 0}
    if any(x.get('COMMON_kind') == 'far' for x in results):
        result['COMMON_totals'] = COMMON_totals(results)
    return result


def report_inputs(result):
    """Old near-only reports unchanged; FAR reports preserve kind/count and totals."""
    rows = [{'id': item['id'], 'source': item['source'], 'object': item['object'],
             'object_sha256': item['object_sha256'],
             'definitions': [{'symbol': row['symbol'], 'size': row['size']}
                             for row in item['definitions']]}
            for item in result['objects']]
    if 'COMMON_totals' not in result:
        return rows
    require(result['COMMON_totals'] == COMMON_totals(result['objects']), 'COMMON accounting mismatch')
    for row, item in zip(rows, result['objects']):
        for definition, raw in zip(row['definitions'], item['definitions']):
            kind = raw.get('communal_kind', 0x62)
            definition.update(communal_kind=kind, storage='far-common' if kind == 0x61 else 'near-common')
            if kind == 0x61:
                definition.update(element_count=raw['element_count'], element_bytes=raw['element_bytes'])
        if item.get('COMMON_kind') == 'far':
            row.update(COMMON_totals=result['COMMON_totals'], conditional_native_capacity_model=True)
    return rows


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=PROJECT)
    parser.add_argument('--target', type=Path, default=PROJECT.parent / 'CHESS.EXE')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    result = build_source_inputs(args.project, args.target, args.output, args.config)
    args.report.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'objects': len(result['objects']), 'definitions': sum(len(x['definitions']) for x in result['objects']),
                      'matching_credit': result['matching_credit']}))
