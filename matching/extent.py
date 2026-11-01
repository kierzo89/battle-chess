"""Narrow retained proofs for compiler output omitted from reachable bodies.

This does not relax ordinary REA extent validation. It accepts only the explicit
v1 proof with one five-byte dead return before the shared epilogue, a preceding
backward unconditional jump, a complete raw span, the adjacent next function,
and an independently emitted CodeView3 extent. The separately implemented
inline-switch proof also requires fresh CODE fixups and a bounded dispatcher.
Neither proof edits code or sizes.
The separate forward-jump profile admits only the fixed 31-byte far signed
comparison return shape, with a two-byte dead jump, a closed four-block CFG,
empty global xrefs for both gap bytes, and a fully evidenced adjacent entry.
The fixed signum profile admits only the complete42-byte5C8B C5 return with
both dead jumps, six closed CFG blocks, four empty global xrefs, one fresh
compiler fixup, and the independently pinned full147-byte adjacent body.
"""
import json
import hashlib
from pathlib import Path


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError('invalid address/size')
    return int(value, 0) if isinstance(value, str) else int(value)


def _evidence(project, relative, target_sha256, operation):
    path = (project / relative).resolve()
    if not path.is_relative_to(project):
        raise ValueError('extent evidence outside matching project')
    e = json.loads(path.read_text())
    profile = e['analysis_profile']['parameters']
    if (e['subject']['digest']['sha256'] != target_sha256
            or e['operation'] != operation
            or profile.get('load_segment') != '0x1000'
            or profile.get('language_id') != 'x86:LE:16:Real Mode'):
        raise ValueError('extent evidence target/profile/operation mismatch')
    return e


def validate_extended_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=None):
    """Validate the explicit v1 proof, returning its retained evidence identity.

    ``emitted_procedure`` is the fresh OMF object's ``function_info`` dictionary;
    ``linked_bytes`` is the entire freshly linked procedure, compared to the
    complete retained raw span. Callers also compare against their pinned image.
    No non-contiguous unit without this exact proof is accepted here.
    """
    project = Path(project).resolve()
    meta = unit.get('extended_extent')
    if isinstance(meta, dict) and meta.get('kind') == 'packet_receive_switch_cleanup_ddd3_v1':
        from packet_receive_extent import validate_packet_receive_extent
        return validate_packet_receive_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'command_key_cleanup_fd6a_v1':
        from command_key_extent import validate_command_key_extent
        return validate_command_key_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'input_dialog_switch_cleanup_260c_v1':
        from input_dialog_extent import validate_input_dialog_extent
        return validate_input_dialog_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'shared_book_skip_literals78_8577_v1':
        from shared_book_skip_literals78 import validate_shared_book_skip_extent
        return validate_shared_book_skip_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'shared_book_skip_8577_v1':
        from shared_book_skip_extent2418 import validate_shared_book_skip_extent
        return validate_shared_book_skip_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'book_skip_8577_v1':
        from book_skip_extent import validate_book_skip_extent
        return validate_book_skip_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'alternate_view_switch_7e6b_v1':
        from alternate_extent import validate_alternate_extent
        return validate_alternate_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'step_switch_872a_v1':
        from step_extent import validate_step_extent
        return validate_step_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'input_wait_screen_names_1da9_v2':
        from input_wait_extent_screen_names import validate_input_wait_extent
        return validate_input_wait_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'board_action_screen_names_20d5_v2':
        from board_action_extent_screen_names import validate_board_action_extent
        return validate_board_action_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'input_wait_restored_1da9_v1':
        from input_wait_extent import validate_input_wait_extent
        return validate_input_wait_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'keyboard_switches_1917_v1':
        from keyboard_extent import validate_keyboard_extent
        return validate_keyboard_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'board_action_cleanup_20d5_v1':
        from board_action_extent import validate_board_action_extent
        return validate_board_action_extent(unit, project, target_sha256, emitted_procedure, linked_bytes, source_object=source_object)
    if isinstance(meta, dict) and meta.get('kind') == 'prompt_dead_switches_1296_v1':
        from prompt_extent import validate_prompt_extent
        return validate_prompt_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'board_pointer_expanded_0daf_v1':
        from board_pointer_extent import validate_board_pointer_extent
        return validate_board_pointer_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'obtain_input_dead_branches_0254_v1':
        from obtain_input_extent import validate_obtain_input_extent
        return validate_obtain_input_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'main_unreachable_epilogue_0010_v1':
        from main_extent import validate_main_extent
        return validate_main_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'text_input_expanded_1064_v1':
        from text_input_extent import validate_text_input_extent
        return validate_text_input_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'face_task_gap_724d_v1':
        from face_task_extent import validate_face_task_extent
        return validate_face_task_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'capture_task_gap_75f6_v1':
        from capture_task_extent import validate_capture_task_extent
        return validate_capture_task_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'effect_task_gap_6ab1_v1':
        from effect_task_extent import validate_effect_task_extent
        return validate_effect_task_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'task_dispatch_switch_67fb_v1':
        from task_dispatch_extent import validate_task_dispatch_extent
        return validate_task_dispatch_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'dual_inline_switch_6167_v1':
        from dual_switch_extent import validate_dual_switch_extent
        return validate_dual_switch_extent(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'signed_signum_return_gaps_v1':
        return _validate_signum_return_gaps(unit, project, target_sha256, emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'segmented_evaluation_v1':
        from segmented_extent import validate_segmented_extent
        return validate_segmented_extent(unit, project, target_sha256,
                                         emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') == 'unreachable_forward_jump_gap_v1':
        return _validate_forward_jump_gap(unit, project, target_sha256,
                                          emitted_procedure, linked_bytes)
    if isinstance(meta, dict) and meta.get('kind') in (
            'inline_switch_table_v1', 'inline_switch_zero_return_v1'):
        from switch_extent import validate_switch_extent
        return validate_switch_extent(unit, project, target_sha256,
                                      emitted_procedure, linked_bytes)
    if (not isinstance(meta, dict) or set(meta) !=
            {'kind', 'raw_span_evidence', 'next_entry_evidence'}
            or meta['kind'] != 'unreachable_return_gap_v1'):
        raise ValueError('missing or unsupported extended extent proof')
    if unit.get('language') != 'c':
        raise ValueError('extended extent requires ordinary compiler C output')
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    if len({e['analysis_profile']['digest'] for e in (dossier, raw, following)}) != 1:
        raise ValueError('extended extent analysis profiles differ')
    start, size = 0x10000 + _number(unit['image_offset']), _number(unit['size'])
    end = start + size
    proc = dossier['normalized_result']['procedure']
    body = proc['body']
    ranges = body.get('ranges', [])
    if (not body.get('available') or not body.get('contains_entry')
            or body.get('non_contiguous') is not True or len(ranges) != 2
            or _number(proc['address']) != start):
        raise ValueError('extended extent requires two known function body ranges')
    first_start, first_end = _number(ranges[0]['start']), _number(ranges[0]['end']) + 1
    second_start, second_end = _number(ranges[1]['start']), _number(ranges[1]['end']) + 1
    if (first_start != start or second_end != end or second_start-first_end != 5
            or not start + 3 < first_end < second_start < end
            or body.get('total_bytes') != size - 5 or body.get('span_bytes') != size):
        raise ValueError('extended extent ranges do not establish one five-byte gap')
    data = raw['normalized_result']
    blob = bytes.fromhex(data['bytes_hex'])
    if (data.get('complete') is not True or _number(data['address']) != start
            or _number(raw['parameters']['address']) != start
            or raw['parameters']['length'] != len(blob)
            or data.get('returned_bytes') != len(blob)
            or data.get('requested_bytes') != len(blob) or len(blob) < size + 3):
        raise ValueError('extended extent requires complete raw span and next entry')
    if not isinstance(linked_bytes, bytes) or len(linked_bytes) != size or blob[:size] != linked_bytes:
        raise ValueError('retained raw span differs from complete freshly linked procedure')
    gap = first_end - start
    if blob[gap:gap+5] != bytes.fromhex('8b46feeb00'):
        raise ValueError('gap is not MOV AX,[BP-2]; JMP +0')
    if blob[gap-3] != 0xe9:
        raise ValueError('gap predecessor is not a near unconditional jump')
    branch_target = first_end + int.from_bytes(blob[gap-2:gap], 'little', signed=True)
    if not start <= branch_target < first_end - 3:
        raise ValueError('gap predecessor must jump backward inside the body')
    blocks = dossier['normalized_result']['basic_blocks']
    predecessor = [b for b in blocks if _number(b['start']) == first_end - 3]
    if (len(predecessor) != 1 or _number(predecessor[0]['end']) != first_end
            or [_number(a) for a in predecessor[0]['successors']] != [branch_target]):
        raise ValueError('retained CFG does not prove the gap predecessor jump')
    for block in blocks:
        left, right = _number(block['start']), _number(block['end'])
        if left < second_start and right > first_end:
            raise ValueError('retained CFG block overlaps the dead gap')
        if any(first_end <= _number(a) < second_start for a in block['successors']):
            raise ValueError('retained CFG branches into the purported dead gap')
    next_proc = following['normalized_result']['procedure']
    next_body = next_proc['body']
    if (not next_body.get('available') or not next_body.get('contains_entry')
            or next_body.get('non_contiguous') is not False
            or len(next_body.get('ranges', [])) != 1
            or _number(next_body['ranges'][0]['end']) < end
            or _number(next_proc['address']) != end
            or _number(next_body['ranges'][0]['start']) != end
            or blob[size:size+3] != bytes.fromhex('558bec')):
        raise ValueError('next retained function must begin exactly after the full span')
    if (not isinstance(emitted_procedure, dict)
            or emitted_procedure.get('symbol') != unit.get('symbol')
            or emitted_procedure.get('boundary') != 'codeview3_procedure'
            or emitted_procedure.get('size') != size
            or emitted_procedure.get('end', -1) - emitted_procedure.get('offset', 0) != size):
        raise ValueError('fresh compiler CodeView procedure must cover the entire raw span')
    return {'kind': meta['kind'], 'body_evidence_id': dossier['evidence_id'],
            'raw_span_evidence_id': raw['evidence_id'],
            'next_entry_evidence_id': following['evidence_id'],
            'span_bytes': size, 'gap_address': hex(first_end), 'gap_size': 5,
            'gap_hex': blob[gap:gap+5].hex(), 'predecessor_target': hex(branch_target),
            'next_entry': hex(end), 'compiler_boundary': 'codeview3_procedure'}


def _validate_forward_jump_gap(unit, project, target_sha256, emitted, linked):
    """Prove the single dead EB04 in C5's far signed min/max return shape."""
    meta = unit['extended_extent']
    if (set(meta) != {'kind', 'raw_span_evidence', 'next_entry_evidence', 'gap_xref_evidence'}
            or unit.get('language') != 'c'
            or not isinstance(meta['gap_xref_evidence'], list)
            or len(meta['gap_xref_evidence']) != 2):
        raise ValueError('forward-jump extent requires ordinary C and exact proof fields')
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    xrefs = [_evidence(project, path, target_sha256, 'xrefs') for path in meta['gap_xref_evidence']]
    if len({e['analysis_profile']['digest'] for e in [dossier, raw, following] + xrefs}) != 1:
        raise ValueError('forward-jump extent analysis profiles differ')
    start, size = 0x10000 + _number(unit['image_offset']), _number(unit['size'])
    if size != 31:
        raise ValueError('forward-jump extent requires the complete 31-byte comparison')
    end, gap_start, gap_end, epilogue = start + 31, start + 19, start + 21, start + 25
    proc = dossier['normalized_result']['procedure']
    body = proc['body']
    ranges = [(_number(r['start']), _number(r['end']) + 1) for r in body.get('ranges', [])]
    if (body.get('available') is not True or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True or _number(proc['address']) != start
            or ranges != [(start, gap_start), (gap_end, end)]
            or body.get('total_bytes') != 29 or body.get('span_bytes') != 31):
        raise ValueError('forward-jump extent requires exact two-range body and two-byte gap')
    data = raw['normalized_result']
    blob = bytes.fromhex(data['bytes_hex'])
    if (data.get('complete') is not True or _number(data['address']) != start
            or _number(raw['parameters']['address']) != start
            or raw['parameters']['length'] != len(blob)
            or data.get('returned_bytes') != len(blob) or data.get('requested_bytes') != len(blob)):
        raise ValueError('forward-jump extent requires complete raw read metadata')
    if not isinstance(linked, bytes) or len(linked) != size or blob[:size] != linked:
        raise ValueError('forward-jump raw span differs from complete freshly linked procedure')
    # This is deliberately a shape validator, not a generic unreachable-byte
    # rule: the sole variable instruction is signed JL/JG over the first arm.
    if (linked[:13] != bytes.fromhex('558bec57568b76068b7e083bf7')
            or linked[13] not in (0x7c, 0x7f)
            or linked[14:] != bytes.fromhex('068bc6eb06eb048bc7eb005e5f8be55dcb')):
        raise ValueError('forward-jump extent is not the narrow signed-comparison return shape')
    predecessor_target = start + 19 + int.from_bytes(linked[18:19], 'little', signed=True)
    dead_target = start + 21 + int.from_bytes(linked[20:21], 'little', signed=True)
    if predecessor_target != epilogue or dead_target != epilogue:
        raise ValueError('forward-jump predecessor and dead jump must share the far epilogue')
    blocks = dossier['normalized_result']['basic_blocks']
    observed = []
    for block in blocks:
        left, right = _number(block['start']), _number(block['end'])
        successors = [_number(a) for a in block['successors']]
        if left < gap_end and right > gap_start:
            raise ValueError('forward-jump CFG block overlaps the dead gap')
        if any(gap_start <= a < gap_end for a in successors):
            raise ValueError('forward-jump CFG branches into the dead gap')
        observed.append((left, right, tuple(sorted(successors))))
    expected = [(start, start + 15, (start + 15, gap_end)),
                (start + 15, gap_start, (epilogue,)),
                (gap_end, epilogue, (epilogue,)), (epilogue, end, ())]
    if sorted(observed) != expected:
        raise ValueError('forward-jump CFG must establish the exact four closed blocks')
    for reference in dossier['normalized_result'].get('incoming_references', []):
        target = reference.get('target_address')
        if isinstance(target, str) and target.startswith('0x') and gap_start <= _number(target) < gap_end:
            raise ValueError('forward-jump retained incoming reference enters dead gap')
    if (sorted(_number(e['parameters']['address']) for e in xrefs) != [gap_start, gap_start + 1]
            or any(e['normalized_result'] != [] for e in xrefs)):
        raise ValueError('forward-jump gap bytes require distinct empty global xref evidence')
    next_proc = following['normalized_result']['procedure']
    next_body = next_proc['body']
    next_ranges = [(_number(r['start']), _number(r['end']) + 1)
                   for r in next_body.get('ranges', [])]
    if (next_body.get('available') is not True or next_body.get('contains_entry') is not True
            or not 1 <= len(next_ranges) <= 2 or _number(next_proc['address']) != end
            or next_ranges[0][0] != end
            or any(a >= b for a, b in next_ranges)
            or any(a[1] >= b[0] for a, b in zip(next_ranges, next_ranges[1:]))
            or next_body.get('non_contiguous') is not (len(next_ranges) > 1)
            or next_body.get('span_bytes') != next_ranges[-1][1] - end
            or next_body.get('total_bytes') != sum(b-a for a, b in next_ranges)
            or len(blob) < next_ranges[-1][1] - start
            or blob[size:size + 3] != bytes.fromhex('558bec')):
        raise ValueError('next retained function must begin adjacent with its complete consistent body')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != unit.get('symbol')
            or emitted.get('boundary') != 'codeview3_procedure' or emitted.get('size') != size
            or emitted.get('end', -1) - emitted.get('offset', 0) != size
            or emitted.get('fixups', [])):
        raise ValueError('fresh compiler CodeView procedure must cover all31 relocation-free bytes')
    return {'kind': meta['kind'], 'body_evidence_id': dossier['evidence_id'],
            'raw_span_evidence_id': raw['evidence_id'],
            'next_entry_evidence_id': following['evidence_id'],
            'gap_xref_evidence_ids': [e['evidence_id'] for e in xrefs],
            'span_bytes': size, 'gap_address': hex(gap_start), 'gap_size': 2,
            'gap_hex': linked[19:21].hex(), 'predecessor_target': hex(predecessor_target),
            'dead_jump_target': hex(dead_target), 'next_entry': hex(end),
            'compiler_boundary': 'codeview3_procedure'}


def _validate_signum_return_gaps(unit, project, target_sha256, emitted, linked):
    """Only the complete C5 5C8B three-way sign return, including both dead JMPs.

    This adds no generic permission to crop or join reachable ranges. Identity,
    every instruction, six closed CFG blocks, four global xref results, complete
    adjacent-body raw context and a fresh CV extent/fixup are all mandatory.
    """
    meta = unit['extended_extent']
    if (set(meta) != {'kind', 'raw_span_evidence', 'next_entry_evidence', 'gap_xref_evidence'}
            or unit.get('language') != 'c' or unit.get('backend') != 'msc500-omf'
            or unit.get('symbol') != '_sign_5c8b' or unit.get('id') != 'sign_5c8b'
            or unit.get('flags') != ['/AS', '/Zi'] or unit.get('code_address') is not None
            or _number(unit['image_offset']) != 0x5c8b or _number(unit['size']) != 42
            or not isinstance(meta['gap_xref_evidence'], list)
            or len(meta['gap_xref_evidence']) != 4):
        raise ValueError('signum extent requires the fixed ordinary C5 function and exact proof fields')
    dossier = _evidence(project, unit['rea_evidence'], target_sha256, 'analyze_function')
    raw = _evidence(project, meta['raw_span_evidence'], target_sha256, 'read_bytes')
    following = _evidence(project, meta['next_entry_evidence'], target_sha256, 'analyze_function')
    xrefs = [_evidence(project, p, target_sha256, 'xrefs') for p in meta['gap_xref_evidence']]
    if len({e['analysis_profile']['digest'] for e in [dossier, raw, following] + xrefs}) != 1:
        raise ValueError('signum extent analysis profiles differ')
    start, end, epilogue = 0x15c8b, 0x15cb5, 0x15cb1
    proc = dossier['normalized_result']['procedure']
    body = proc['body']
    ranges = [(_number(r['start']), _number(r['end']) + 1) for r in body.get('ranges', [])]
    if (body.get('available') is not True or body.get('contains_entry') is not True
            or body.get('non_contiguous') is not True or _number(proc['address']) != start
            or ranges != [(start, start+19), (start+21, start+32), (start+34, end)]
            or body.get('total_bytes') != 38 or body.get('span_bytes') != 42):
        raise ValueError('signum extent requires the exact three reachable ranges and both two-byte gaps')
    data = raw['normalized_result']
    blob = bytes.fromhex(data['bytes_hex'])
    if (data.get('complete') is not True or _number(data['address']) != start
            or _number(raw['parameters']['address']) != start
            or raw['parameters']['length'] != len(blob)
            or data.get('requested_bytes') != len(blob) or data.get('returned_bytes') != len(blob)
            or not isinstance(linked, bytes) or len(linked) != 42 or blob[:42] != linked):
        raise ValueError('signum extent requires complete raw bytes equal to the entire fresh C procedure')
    tail = bytes.fromhex('837e04007e07b80100eb13eb11837e04007d07b8ffffeb06eb042bc0eb008be55dc3')
    if (linked[:6] != bytes.fromhex('558bec33c0e8') or linked[8:] != tail
            or (0x5c8b+8+int.from_bytes(linked[6:8], 'little', signed=True)) & 0xffff != 0xecaa
            or unit.get('externals', {}).get('__chkstk') != 0xecaa):
        raise ValueError('signum extent is not the complete signed three-way return and original stack probe')
    # Every live and dead return jump must land at the same near epilogue.
    if any(start+at+2+int.from_bytes(linked[at+1:at+2], 'little', signed=True) != epilogue
           for at in (17, 19, 30, 32, 36)):
        raise ValueError('signum return jumps must share the observed epilogue')
    blocks = dossier['normalized_result']['basic_blocks']
    observed = [(_number(b['start']), _number(b['end']),
                 tuple(sorted(_number(a) for a in b['successors']))) for b in blocks]
    expected = [(start, start+14, (start+14, start+21)),
                (start+14, start+19, (epilogue,)),
                (start+21, start+27, (start+27, start+34)),
                (start+27, start+32, (epilogue,)),
                (start+34, epilogue, (epilogue,)), (epilogue, end, ())]
    if sorted(observed) != expected:
        raise ValueError('signum extent must have exactly six closed observed CFG blocks')
    gap_addresses = [start+19, start+20, start+32, start+33]
    for ref in dossier['normalized_result'].get('incoming_references', []):
        target = ref.get('target_address')
        if isinstance(target, str) and target.startswith('0x') and _number(target) in gap_addresses:
            raise ValueError('signum retained incoming reference enters an unreachable byte')
    if (sorted(_number(e['parameters']['address']) for e in xrefs) != gap_addresses
            or len({e['evidence_id'] for e in xrefs}) != 4
            or any(e['normalized_result'] != [] for e in xrefs)):
        raise ValueError('all four signum gap bytes require distinct empty global xref evidence')
    next_proc = following['normalized_result']['procedure']
    nb = next_proc['body']
    if (nb.get('available') is not True or nb.get('contains_entry') is not True
            or nb.get('non_contiguous') is not False or _number(next_proc['address']) != end
            or nb.get('ranges') != [{'start': hex(end), 'end': '0x15d47'}]
            or nb.get('span_bytes') != 147 or nb.get('total_bytes') != 147
            or len(blob) < 42+147 or blob[42:45] != bytes.fromhex('558bec')
            or hashlib.sha256(blob[42:189]).hexdigest() !=
            '88ce632ad439581e9c2a09990f16cb0ef52ab8e8d84234eef9fbf2c5859331e6'):
        raise ValueError('signum extent requires complete raw context of the adjacent147-byte function')
    if (not isinstance(emitted, dict) or emitted.get('symbol') != unit['symbol']
            or emitted.get('boundary') != 'codeview3_procedure' or emitted.get('size') != 42
            or type(emitted.get('offset')) is not int or emitted['offset'] < 0
            or emitted.get('end', -1) != emitted['offset']+42
            or not isinstance(emitted.get('fixups'), list) or len(emitted['fixups']) != 1):
        raise ValueError('fresh CodeView extent must cover the entire42-byte signum procedure')
    f = emitted['fixups'][0]
    if (f.offset != emitted['offset']+6 or f.width != 2 or f.location_type != 1
            or f.segment != emitted.get('segment') or f.segment_relative is not False
            or f.frame != (5, None) or f.target[0] != 2
            or type(f.target[1]) is not int or f.target[1] <= 0 or (f.displacement or 0) != 0):
        raise ValueError('signum extent permits exactly one compiler-emitted near stack-probe fixup')
    return {'kind': meta['kind'], 'body_evidence_id': dossier['evidence_id'],
            'raw_span_evidence_id': raw['evidence_id'], 'next_entry_evidence_id': following['evidence_id'],
            'gap_xref_evidence_ids': [e['evidence_id'] for e in xrefs],
            'span_bytes': 42, 'reachable_body_bytes': 38,
            'gap_addresses': [hex(start+19), hex(start+32)], 'gap_sizes': [2, 2],
            'gap_hex': [linked[19:21].hex(), linked[32:34].hex()],
            'shared_epilogue': hex(epilogue), 'next_entry': hex(end),
            'compiler_boundary': 'codeview3_procedure', 'compiler_near_fixup_count': 1,
            'next_complete_body_bytes': 147,
            'next_complete_body_sha256': hashlib.sha256(blob[42:189]).hexdigest()}
