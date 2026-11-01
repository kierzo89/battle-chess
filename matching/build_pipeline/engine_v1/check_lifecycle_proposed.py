#!/usr/bin/env python3
"""Rebuild reviewed units and compare every byte with a pinned DOS executable.

No relocation masks, cached binaries, fuzzy matches, or pseudocode credit.
The provisional function inventory is evidence, not a code-size denominator.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

# Permit both direct execution and importlib-based unit-test loading.
if str(HERE_IMPORT := Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(HERE_IMPORT))
from msc import compile_c
from source_inputs import build_source_inputs, report_inputs
from omf import read_omf
from link16 import link_function
from exepack import unpack_exepack
from library16 import extract_member, link_segment
from setup_runtime import validate_runtime
from reference import build_reference, validate_expanded_read, validate_data_address, CARRIER_SHA256, ORIGINAL_SHA256
from extent import validate_extended_extent
import runtime_libh
import runtime_external16
import runtime_external3
import runtime_lidata16
import owned_const16
import history_input_literal_const16
import packet_literal61
import owned_literal_const16
import owned_selector_const16
import owned_context_mz
from source_data_mz import collect_source_data_mz
import owned_data16
import owned_bss16
from cdata import extract_data
import actor70_data16
import buffer_data16
import text_colour_data16
import glyph_pixels_data16
import blit_prefix_data16
import screen_far_pointer_data16
import asm_data16
import graphics_workspace_data16
import graphics_splash_workspace_data16
import graphics_buffer_views_workspace_data16
import graphics_screen_view_workspace_data16
import animation_labels_data16
import pixel_callback_data16
from animation_labels_link import emit_new_object as emit_animation_labels
import graphics_driver_carrier_code16
import animation_init_code16
import begin_end_input_code16
import outline_piece_code16
import special_task_code16
import turn_task_code16
import remove_actor_code16
import input_dialog_code16
import near_game_code16
import mixed_refresh_chat16
import mixed_restore_decoder16
import mixed_motion_special16
import mixed_tail_undo16
import mixed_graphics16 as graphics_backend
import mixed_evaluation16 as evaluation_backend
import mixed_remove46016 as remove460_backend
import mixed_overlap16 as overlap_backend
import mixed_visual16 as visual_backend
import hardware_state_data16
import asm_code16
import huff_code16
import huff_dgroup_code16
import huff_workspace_data16
import huff_allocation16
import serial_code16
import blit_code16
import graphics_code16
import graphics_dgroup_code16
import platform_code16
import bios_pixel_word_code16
import bios_pixel_text_code16
import graphics_wrapper_code16
import graphics_wrapper_flags_code16
import input_flags_code16

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    if digest(data) != expected:
        raise ValueError(f"SHA-256 mismatch: {path}")
    return data


def mz_image(data: bytes) -> tuple[int, bytes]:
    if len(data) < 28 or data[:2] != b'MZ':
        raise ValueError('Target is not an MZ executable')
    tail, pages, relocations, paragraphs = struct.unpack_from('<4H', data, 2)
    if not pages or tail > 511:
        raise ValueError('Invalid MZ file size')
    size = (pages - 1) * 512 + (tail or 512)
    header = paragraphs * 16
    if not 28 <= header <= size <= len(data):
        raise ValueError('Invalid MZ module bounds')
    if relocations:
        raise ValueError('MZ relocations need an explicit supported policy')
    return header, data[header:size]


def compiler_input_name(unit: dict) -> str:
    """Preserve the DOS C basename that determines a medium-model CODE segment."""
    if 'compiler_source_name' not in unit:
        return 'UNIT.C'
    name = unit['compiler_source_name']
    if (unit.get('language') != 'c' or unit.get('backend') != 'msc500-omf'
            or '/AM' not in unit.get('flags', [])):
        raise ValueError('Explicit compiler source name requires a Microsoft C 5.00 medium-model C unit')
    if (not isinstance(name, str)
            or not re.fullmatch(r'[A-Z][A-Z0-9_]{0,7}\.C', name)
            or name[:-2] in {'CON', 'PRN', 'AUX', 'NUL'}
            or re.fullmatch(r'(?:COM|LPT)[1-9]\.C', name)):
        raise ValueError('DOS source name must be an uppercase non-device 8.3 C filename')
    return name


def validate_units(units: list[dict], image_size: int, expanded_size: int | None = None) -> None:
    names, spans = set(), []
    for u in units:
        compiler_input_name(u)
        a, n = int(u['image_offset'], 0), u['size']
        if u['id'] in names or not re.fullmatch(r'[a-z][a-z0-9_]*', u['id']):
            raise ValueError(f"Duplicate or invalid unit id: {u['id']}")
        names.add(u['id'])
        region = u.get('reference_region', 'unchanged-prefix')
        if region not in ('unchanged-prefix', 'exepack-expanded'):
            raise ValueError('Unknown reference region')
        limit = expanded_size if region == 'exepack-expanded' else image_size
        if type(n) is not int or n <= 0 or a < 0 or limit is None or a + n > limit:
            raise ValueError(f"Invalid extent: {u['id']}")
        if (u['language'], u['backend']) not in [('c', packet_literal61.BACKEND), ('c-data', packet_literal61.BACKEND), ('asm', 'nasm-bin'), ('asm', 'nasm-code-omf'), ('asm-data', 'nasm-data-omf'), ('asm-data', huff_workspace_data16.BACKEND), ('asm-data', hardware_state_data16.BACKEND), ('asm-data', graphics_workspace_data16.BACKEND), ('asm-data', graphics_splash_workspace_data16.BACKEND), ('asm-data', graphics_buffer_views_workspace_data16.BACKEND), ('asm-data', graphics_screen_view_workspace_data16.BACKEND), ('asm-code', 'nasm-code-contribution-omf'), ('asm-code', 'masm510-code-contribution-omf'), ('asm-code', 'masm510-blit-code-contribution-omf'), ('asm-code', 'masm510-graphics-code-contribution-omf'), ('asm-code', graphics_dgroup_code16.BACKEND), ('asm-code', 'masm510-platform-code-contribution-omf'), ('asm-code', bios_pixel_word_code16.BACKEND), ('asm-code', bios_pixel_text_code16.BACKEND), ('asm-code', graphics_driver_carrier_code16.BACKEND), ('asm-code', animation_init_code16.BACKEND), ('asm-code', begin_end_input_code16.BACKEND), ('asm-code', outline_piece_code16.BACKEND), ('asm-code', special_task_code16.BACKEND), ('asm-code', turn_task_code16.BACKEND), ('asm-code', remove_actor_code16.BACKEND), ('asm-code', input_dialog_code16.BACKEND), ('asm-code', near_game_code16.BACKEND), ('asm-code', 'masm510-graphics-wrapper-code-omf'), ('asm-code', 'masm510-graphics-wrapper-flags-code-omf'), ('asm-code', 'masm510-input-flags-code-omf'), ('c', mixed_refresh_chat16.BACKEND), ('asm-code', mixed_refresh_chat16.BACKEND), ('c', mixed_restore_decoder16.BACKEND), ('asm-code', mixed_restore_decoder16.BACKEND), ('c', mixed_motion_special16.BACKEND), ('asm-code', mixed_motion_special16.BACKEND), ('c', mixed_tail_undo16.BACKEND), ('asm-code', mixed_tail_undo16.BACKEND), ('c', graphics_backend.BACKEND), ('asm-code', graphics_backend.BACKEND), ('c', evaluation_backend.BACKEND), ('asm-code', evaluation_backend.BACKEND), ('c', remove460_backend.BACKEND), ('asm-code', remove460_backend.BACKEND), ('c', overlap_backend.BACKEND), ('asm-code', overlap_backend.BACKEND), ('c', visual_backend.BACKEND), ('asm-code', visual_backend.BACKEND), ('c', 'msc510-omf'), ('c', 'msc500-omf'), ('c', 'msc400-omf'), ('c-data', 'msc500-data-omf'), ('c-data', history_input_literal_const16.BACKEND), ('c-data', actor70_data16.BACKEND), ('c-data', animation_labels_data16.BACKEND), ('c-data', pixel_callback_data16.BACKEND), ('c-data', 'msc500-buffer-data-omf'), ('c-data', 'msc500-text-colour-data-omf'), ('c-data', 'msc500-glyph-pixels-data-omf'), ('c-data', 'msc500-blit-prefix-data-omf'), ('c-data', 'msc500-owned-data-omf'), ('c-data', 'msc500-pointer-data-omf'), ('c-data', screen_far_pointer_data16.BACKEND), ('runtime', 'msc500-library'), ('runtime', 'msc500-authentic-link'), ('runtime', 'msc500-authentic-external16'), ('runtime', runtime_external3.BACKEND)]:
            raise ValueError('Unsupported language/backend combination')
        if u['backend'] == packet_literal61.BACKEND:
            packet_literal61.validate_unit(u)
        if u['language'] in ('c', 'c-data') and (not u.get('symbol') or not u.get('flags')):
            raise ValueError('C units require compiler flags and a public symbol')
        if 'code_address' in u:
            address = u['code_address']
            if (u['language'] != 'c' or not isinstance(address, dict)
                    or set(address) != {'segment', 'offset'}
                    or any(type(address[k]) is not int or not 0 <= address[k] <= 0xffff
                           for k in ('segment', 'offset'))
                    or address['segment'] * 16 + address['offset'] != a
                    or address['offset'] + n > 0x10000):
                raise ValueError('C code address must give the exact complete CS:offset image mapping')
        kind = u.get('runtime_kind', 'code')
        runtime_source = runtime_external3.SOURCE if u['backend'] == runtime_external3.BACKEND else 'config/runtime_libh.json' if u['backend'] in ('msc500-authentic-link', 'msc500-authentic-external16') else 'config/runtime500.json'
        if u['language'] == 'runtime' and (not u.get('member') or u.get('source') != runtime_source
                or kind not in ('code', 'initialized_data') or (kind == 'code' and not u.get('symbol'))):
            raise ValueError('Runtime units require the pinned runtime profile, member and code public symbol')
        if (region == 'exepack-expanded') != (u['language'] in ('c-data', 'asm-data') or (u['language'] == 'runtime' and kind == 'initialized_data') or (u['language'] == 'asm-code' and u['backend'] in (graphics_wrapper_code16.BACKEND, graphics_wrapper_flags_code16.BACKEND, input_flags_code16.BACKEND, graphics_driver_carrier_code16.BACKEND))):
            raise ValueError('Expanded references require independently initialized data or the closed authenticated wrapper78 or coherent flags78/388 CODE profiles')
        if u['backend'] == runtime_external3.BACKEND:
            runtime_external3.validate_unit(u)
        if u['backend'] == 'nasm-code-omf':
            (huff_dgroup_code16 if u.get('object_profile') == 'huffman_core_dgroup1' else huff_code16 if u.get('object_profile') == 'huffman_core' else asm_code16).validate_unit(u)
        if u['backend'] in (mixed_refresh_chat16.BACKEND, mixed_restore_decoder16.BACKEND, mixed_motion_special16.BACKEND, mixed_tail_undo16.BACKEND, graphics_backend.BACKEND, evaluation_backend.BACKEND, remove460_backend.BACKEND, overlap_backend.BACKEND, visual_backend.BACKEND):
            (visual_backend if u['backend'] == visual_backend.BACKEND else overlap_backend if u['backend'] == overlap_backend.BACKEND else remove460_backend if u['backend'] == remove460_backend.BACKEND else evaluation_backend if u['backend'] == evaluation_backend.BACKEND else graphics_backend if u['backend'] == graphics_backend.BACKEND else mixed_tail_undo16 if u['backend'] == mixed_tail_undo16.BACKEND else mixed_motion_special16 if u['backend'] == mixed_motion_special16.BACKEND else mixed_restore_decoder16 if u['backend'] == mixed_restore_decoder16.BACKEND else mixed_refresh_chat16).validate_unit(u)
        if u['language'] == 'asm-code' and u['backend'] not in (mixed_refresh_chat16.BACKEND, mixed_restore_decoder16.BACKEND, mixed_motion_special16.BACKEND, mixed_tail_undo16.BACKEND, graphics_backend.BACKEND, evaluation_backend.BACKEND, remove460_backend.BACKEND, overlap_backend.BACKEND, visual_backend.BACKEND):
            (near_game_code16 if u['backend'] == near_game_code16.BACKEND else input_dialog_code16 if u['backend'] == input_dialog_code16.BACKEND else remove_actor_code16 if u['backend'] == remove_actor_code16.BACKEND else turn_task_code16 if u['backend'] == turn_task_code16.BACKEND else special_task_code16 if u['backend'] == special_task_code16.BACKEND else outline_piece_code16 if u['backend'] == outline_piece_code16.BACKEND else begin_end_input_code16 if u['backend'] == begin_end_input_code16.BACKEND else animation_init_code16 if u['backend'] == animation_init_code16.BACKEND else graphics_driver_carrier_code16 if u['backend'] == graphics_driver_carrier_code16.BACKEND else bios_pixel_text_code16 if u['backend'] == bios_pixel_text_code16.BACKEND else bios_pixel_word_code16 if u['backend'] == bios_pixel_word_code16.BACKEND else platform_code16 if u['backend'] == platform_code16.BACKEND else graphics_wrapper_flags_code16 if u['backend'] == graphics_wrapper_flags_code16.BACKEND else input_flags_code16 if u['backend'] == input_flags_code16.BACKEND else graphics_wrapper_code16 if u['backend'] == graphics_wrapper_code16.BACKEND else graphics_dgroup_code16 if u['backend'] == graphics_dgroup_code16.BACKEND else graphics_code16 if u['backend'] == graphics_code16.BACKEND else blit_code16 if u['backend'] == blit_code16.BACKEND else serial_code16 if u['backend'] == serial_code16.BACKEND else huff_allocation16).validate_unit(u)
        if u['language'] == 'asm-data':
            (huff_workspace_data16 if u['backend'] == huff_workspace_data16.BACKEND else graphics_screen_view_workspace_data16 if u['backend'] == graphics_screen_view_workspace_data16.BACKEND else graphics_buffer_views_workspace_data16 if u['backend'] == graphics_buffer_views_workspace_data16.BACKEND else graphics_splash_workspace_data16 if u['backend'] == graphics_splash_workspace_data16.BACKEND else graphics_workspace_data16 if u['backend'] == graphics_workspace_data16.BACKEND else hardware_state_data16 if u['backend'] == hardware_state_data16.BACKEND else asm_data16).validate_unit(u)
        if 'code_externals' in u and u['backend'] != pixel_callback_data16.BACKEND:
            raise ValueError('CODE DATA bindings require the dedicated callback backend')
        if u['backend'] == actor70_data16.BACKEND:
            actor70_data16.validate_unit(u)
        if u['backend'] == pixel_callback_data16.BACKEND:
            pixel_callback_data16.validate_unit(u)
        if u['backend'] == animation_labels_data16.BACKEND:
            animation_labels_data16.validate_unit(u)
        if u['backend'] == buffer_data16.BACKEND:
            buffer_data16.validate_unit(u)
        if u['backend'] == text_colour_data16.BACKEND:
            text_colour_data16.validate_unit(u)
        if u['backend'] == glyph_pixels_data16.BACKEND:
            glyph_pixels_data16.validate_unit(u)
        if u['backend'] == blit_prefix_data16.BACKEND:
            blit_prefix_data16.validate_unit(u)
        pointer_data = u['backend'] == 'msc500-pointer-data-omf'
        if pointer_data:
            address = u.get('data_address')
            if (not isinstance(address, dict) or set(address) != {'segment', 'offset'}
                    or any(type(address[k]) is not int or not 0 <= address[k] <= 0xffff
                           for k in ('segment', 'offset'))
                    or address['segment'] * 16 + address['offset'] != a
                    or address['offset'] + n > 0x10000
                    or not isinstance(u.get('externals'), dict) or not u['externals']
                    or any(not isinstance(k, str) or type(v) is not int or not 0 <= v <= 0xffff
                           for k, v in u['externals'].items())
                    or u.get('extended_extent')):
                raise ValueError('Pointer C DATA requires an explicit complete DGROUP placement and named near offsets')
        elif u['backend'] == screen_far_pointer_data16.BACKEND:
            screen_far_pointer_data16.validate_unit(u)
        elif u['backend'] == history_input_literal_const16.BACKEND:
            history_input_literal_const16.validate_unit(u)
        elif u['backend'] == 'msc500-owned-data-omf':
            owned_data16.validate_unit_metadata(u)
        elif u.get('data_address') is not None:
            raise ValueError('Explicit DATA placement is supported only by the pointer DATA backend')
        elif u['language'] == 'c-data' and (u.get('externals') or u.get('extended_extent')):
            raise ValueError('Standalone C data permits no external placements or code extent proofs')
        if u['backend'] in ('msc500-authentic-link', 'msc500-authentic-external16') and kind != 'code':
            raise ValueError('Authentic helper LINK currently supports only complete CODE segments')
        if u.get('owned_selector_const') is not None:
            owned_selector_const16.validate_unit_metadata(u)
        if u.get('owned_const_profile') is not None:
            owned_literal_const16.validate_unit_metadata(u)
        if u.get('owned_const') is not None and (u['language'] != 'c'
                or u['backend'] != 'msc500-omf' or not isinstance(u['owned_const'], dict)
                or set(u['owned_const']) != {'segment', 'group', 'size', 'image_offset', 'data_address', 'rea_evidence'}
                or u.get('extended_extent')):
            raise ValueError('Owned CONST requires ordinary MSC500 C and a complete explicit allocation descriptor')
        if u.get('owned_data') is not None:
            if u.get('owned_const') is not None or u.get('extended_extent'):
                raise ValueError('Owned PUBLIC DATA requires an exclusive complete allocation contract')
            owned_data16.validate_unit_metadata(u)
        if u.get('owned_bss') is not None:
            owned_bss16.validate_unit_metadata(u)
        if not u.get('boundary_evidence'):
            raise ValueError(f"Missing boundary evidence: {u['id']}")
        spans.append((a, a + n))
    spans.sort()
    if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):
        raise ValueError('Reviewed unit extents overlap')
    validate_shared_external_bindings(units)


def validate_shared_external_bindings(units: list[dict]) -> dict:
    """One authored-C source name must denote one comparison address.

    Known C CODE symbols normalize near CS offsets and explicit far pointers
    to image addresses. Other values retain their distinct DATA/absolute/far
    contracts. This supplies no definitions or original global MAP claim.
    """
    code_symbols = {u['symbol'] for u in units if u['language'] == 'c'}
    bindings = {}
    def add(name, value, unit):
        key = json.dumps(value, sort_keys=True)
        bindings.setdefault(name, {}).setdefault(key, []).append(unit)
    for unit in units:
        if unit['language'] not in ('c', 'c-data'):
            continue
        if unit['language'] == 'c':
            add(unit['symbol'], int(unit['image_offset'], 0), unit['id'])
        for name, value in unit.get('externals', {}).items():
            if unit['language'] == 'c' and name in code_symbols:
                if isinstance(value, dict) and set(value) == {'segment', 'offset'}:
                    value = value['segment'] * 16 + value['offset']
                elif type(value) is int:
                    value += unit.get('code_address', {}).get('segment', 0) * 16
            add(name, value, unit['id'])
    conflicts = {name: values for name, values in bindings.items() if len(values) > 1}
    if conflicts:
        raise ValueError('Conflicting shared C comparison bindings: ' + json.dumps(conflicts, sort_keys=True))
    return bindings


def compare(expected: bytes, actual: bytes) -> dict:
    first = next((i for i, (a, b) in enumerate(zip(expected, actual)) if a != b), None)
    if first is None and len(expected) != len(actual):
        first = min(len(expected), len(actual))
    return {
        'status': 'asm_matched' if first is None else 'mismatch',
        'expected_size': len(expected), 'actual_size': len(actual),
        'expected_sha256': digest(expected), 'actual_sha256': digest(actual),
        'first_difference': first,
        'expected_byte': expected[first] if first is not None and first < len(expected) else None,
        'actual_byte': actual[first] if first is not None and first < len(actual) else None,
    }


def runtime_inputs(unit: dict, project: Path):
    """Re-read independent library inputs; no expected executable bytes enter."""
    if unit.get('source') != 'config/runtime500.json' or unit.get('backend') != 'msc500-library':
        raise ValueError('Runtime backend requires its pinned config source')
    config_path = project / 'config/runtime500.json'
    config = json.loads(config_path.read_text())
    modules = [m for m in config['members'] if m.get('id', m['name']) == unit['member']]
    if len(modules) != 1:
        raise ValueError('Runtime member does not identify one pinned module')
    module = modules[0]
    directory = (project / config['destination']).resolve()
    if not directory.is_relative_to(project.resolve()):
        raise ValueError('Runtime installation lies outside matching project')
    library = validate_runtime(directory, config)
    member = extract_member(library, module['name'], config['library_sha256'], module['member_sha256'])
    if member.offset != module['library_offset']:
        raise ValueError('Runtime member library offset mismatch')
    obj = read_omf(member.data)
    if module.get('initialized_record_policy') is not None:
        runtime_lidata16.validate_profile(module)
        runtime_lidata16.validate_unit(unit)
    segment = obj.segments[module['segment']]
    public = obj.publics.get(unit.get('symbol'))
    placement = module['segments'][str(module['segment'])]
    data_kind = unit.get('runtime_kind', 'code') == 'initialized_data'
    if ((not data_kind and (public is None or public.segment != segment.index or public.offset != 0
                            or segment.class_name != 'CODE'))
            or (data_kind and (segment.class_name not in ('DATA', 'MSG')
                or segment.class_name != module.get('class_name')
                or segment.name != module.get('segment_name')
                or (unit.get('symbol') and (public is None or public.segment != segment.index
                                          or public.offset != module['publics'].get(unit['symbol'])))))
            or segment.length != unit['size']
            or placement[0] * 16 + placement[1] != int(unit['image_offset'], 0)):
        raise ValueError('Runtime independent segment/public extent mismatch')
    return config, module, member, obj


def link_runtime_segment(obj, module):
    """Default LEDATA contract stays exact; one declared DATA policy has its own view."""
    if module.get('initialized_record_policy') is not None:
        return runtime_lidata16.link_segment(obj, module)
    return link_segment(obj, module['segment'],
                        {int(k): v for k, v in module['segments'].items()},
                        {int(k): v for k, v in module['groups'].items()}, module['externals'])


def libh_inputs(unit: dict, project: Path):
    if unit.get('source') != 'config/runtime_libh.json' or unit.get('backend') != 'msc500-authentic-link':
        raise ValueError('Authentic helper backend requires its pinned config source')
    config, profile, member, layout = runtime_libh.load_member(unit['member'], project)
    public = layout['publics'].get(unit.get('symbol'))
    if (unit.get('runtime_kind', 'code') != 'code' or unit.get('reference_region', 'unchanged-prefix') != 'unchanged-prefix'
            or int(profile['image_offset'], 0) != int(unit['image_offset'], 0)
            or layout['segment']['length'] != unit['size'] or public is None
            or public['segment'] != layout['segment']['index'] or public['offset'] != 0):
        raise ValueError('Authentic helper independent segment/public extent mismatch')
    return config, profile, member, layout


def external16_inputs(unit: dict, project: Path):
    """Admit the pinned complete ALDIV contribution and its explicit call binding."""
    if (unit.get('source') != 'config/runtime_libh.json'
            or unit.get('backend') != 'msc500-authentic-external16'
            or unit.get('runtime_kind', 'code') != 'code'
            or unit.get('reference_region', 'unchanged-prefix') != 'unchanged-prefix'
            or unit.get('member') != 'near_aldiv' or unit.get('symbol') != '__aNNaldiv'
            or unit.get('size') != 34 or int(unit['image_offset'], 0) != 0xf37a
            or unit.get('externals') != {'__aNldiv': {'segment': 0, 'offset': 0xf87c}}):
        raise ValueError('External16 runtime independent segment/public extent mismatch: requires complete pinned ALDIV and explicit original call binding')
    return runtime_external16.load_profile(unit['member'], project)


def raw_runtime_extent(e: dict, unit: dict, linked: bytes | None = None):
    start = 0x10000 + int(unit['image_offset'], 0)
    raw = e['normalized_result']
    observed = bytes.fromhex(raw['bytes_hex'])
    if (e['operation'] != 'read_bytes' or int(e['parameters']['address'], 0) != start
            or e['parameters']['length'] != unit['size'] or raw.get('complete') is not True
            or int(raw['address'], 0) != start or raw['returned_bytes'] != unit['size']
            or raw['requested_bytes'] != unit['size'] or len(observed) != unit['size']
            or (linked is not None and observed != linked)):
        raise ValueError(f"REA runtime raw-byte extent mismatch: {unit['id']}")
    return observed


def validate_rea_extent(unit: dict, project: Path, target_sha256: str, reference=None) -> str:
    if unit['backend'] == huff_workspace_data16.BACKEND:
        return huff_workspace_data16.validate_evidence(unit, project, target_sha256, reference)
    if unit['backend'] == graphics_screen_view_workspace_data16.BACKEND:
        return graphics_screen_view_workspace_data16.validate_evidence(unit, project, target_sha256, reference)
    if unit['backend'] == graphics_buffer_views_workspace_data16.BACKEND:
        return graphics_buffer_views_workspace_data16.validate_evidence(unit, project, target_sha256, reference)
    if unit['backend'] == animation_labels_data16.BACKEND:
        return animation_labels_data16.validate_evidence(unit, project, target_sha256, reference)
    """Require retained REA body evidence bound to this target and load profile."""
    if unit['language'] == 'asm-code' and unit['backend'] in (mixed_refresh_chat16.BACKEND, mixed_restore_decoder16.BACKEND, mixed_motion_special16.BACKEND, mixed_tail_undo16.BACKEND, graphics_backend.BACKEND, evaluation_backend.BACKEND, remove460_backend.BACKEND, overlap_backend.BACKEND, visual_backend.BACKEND):
        return (visual_backend if unit['backend'] == visual_backend.BACKEND else overlap_backend if unit['backend'] == overlap_backend.BACKEND else remove460_backend if unit['backend'] == remove460_backend.BACKEND else evaluation_backend if unit['backend'] == evaluation_backend.BACKEND else graphics_backend if unit['backend'] == graphics_backend.BACKEND else mixed_tail_undo16 if unit['backend'] == mixed_tail_undo16.BACKEND else mixed_motion_special16 if unit['backend'] == mixed_motion_special16.BACKEND else mixed_restore_decoder16 if unit['backend'] == mixed_restore_decoder16.BACKEND else mixed_refresh_chat16).validate_evidence(unit, project, target_sha256, reference)
    if unit['language'] == 'asm-code':
        backend = near_game_code16 if unit['backend'] == near_game_code16.BACKEND else input_dialog_code16 if unit['backend'] == input_dialog_code16.BACKEND else remove_actor_code16 if unit['backend'] == remove_actor_code16.BACKEND else turn_task_code16 if unit['backend'] == turn_task_code16.BACKEND else special_task_code16 if unit['backend'] == special_task_code16.BACKEND else outline_piece_code16 if unit['backend'] == outline_piece_code16.BACKEND else begin_end_input_code16 if unit['backend'] == begin_end_input_code16.BACKEND else animation_init_code16 if unit['backend'] == animation_init_code16.BACKEND else graphics_driver_carrier_code16 if unit['backend'] == graphics_driver_carrier_code16.BACKEND else bios_pixel_text_code16 if unit['backend'] == bios_pixel_text_code16.BACKEND else bios_pixel_word_code16 if unit['backend'] == bios_pixel_word_code16.BACKEND else platform_code16 if unit['backend'] == platform_code16.BACKEND else graphics_wrapper_flags_code16 if unit['backend'] == graphics_wrapper_flags_code16.BACKEND else input_flags_code16 if unit['backend'] == input_flags_code16.BACKEND else graphics_wrapper_code16 if unit['backend'] == graphics_wrapper_code16.BACKEND else graphics_dgroup_code16 if unit['backend'] == graphics_dgroup_code16.BACKEND else graphics_code16 if unit['backend'] == graphics_code16.BACKEND else blit_code16 if unit['backend'] == blit_code16.BACKEND else serial_code16 if unit['backend'] == serial_code16.BACKEND else huff_allocation16
        return backend.validate_evidence(unit, project, target_sha256, reference)
    path = (project / unit['rea_evidence']).resolve()
    if not path.is_relative_to(project.resolve()):
        raise ValueError('REA evidence is outside matching project')
    e = json.loads(path.read_text())
    if unit['language'] in ('c-data', 'asm-data'):
        if (reference is None or reference['original_sha256'] != target_sha256
                or unit.get('reference_region') != 'exepack-expanded'):
            raise ValueError('C data requires the pinned expanded comparison reference')
        if unit['backend'] in ('msc500-pointer-data-omf', 'msc500-owned-data-omf', screen_far_pointer_data16.BACKEND):
            validate_data_address(unit, reference)
        profile = e.get('analysis_profile', {}).get('parameters', {})
        if (e['subject']['digest']['sha256'] != reference['carrier_sha256']
                or profile.get('load_segment') != '0x1000'
                or profile.get('language_id') != 'x86:LE:16:Real Mode'
                or profile.get('target_format') != 'dos-mz'):
            raise ValueError('C data REA target/profile mismatch')
        raw_runtime_extent(e, unit)
        # Full raw/unrelocated equality is checked after fresh C compilation.
        return e['evidence_id']
    if unit.get('reference_region') == 'exepack-expanded':
        if unit['language'] != 'runtime' or unit.get('runtime_kind') != 'initialized_data':
            raise ValueError(f"REA evidence target/profile mismatch: {unit['id']}")
        if reference is None or reference['original_sha256'] != target_sha256:
            raise ValueError('Expanded reference provenance is missing or mismatched')
        _, module, _, obj = runtime_inputs(unit, project)
        linked, fields = link_runtime_segment(obj, module)
        if module.get('initialized_record_policy') is not None:
            return runtime_lidata16.validate_evidence(unit, project, target_sha256, reference, linked, fields)
        validate_expanded_read(e, unit, linked, reference)
        return e['evidence_id']
    profile = e['analysis_profile']['parameters']
    # Packed MZ analysis does not discover main. Its fixed proof authenticates
    # this full expanded carrier against the original, including every loader
    # relocation, after fresh complete C compilation below.
    expected_evidence_sha = target_sha256
    if (unit.get('extended_extent') or {}).get('kind') == 'main_unreachable_epilogue_0010_v1':
        if target_sha256 != ORIGINAL_SHA256 or unit['id'] != 'main_0010' or unit['language'] != 'c':
            raise ValueError('Unsupported expanded main evidence identity')
        expected_evidence_sha = CARRIER_SHA256
    if (e['subject']['digest']['sha256'] != expected_evidence_sha
            or profile.get('load_segment') != '0x1000'
            or profile.get('language_id') != 'x86:LE:16:Real Mode'):
        raise ValueError(f"REA evidence target/profile mismatch: {unit['id']}")
    if unit['language'] == 'runtime':
        if unit['backend'] == runtime_external3.BACKEND:
            runtime_external3.validate_unit(unit)
            raw_runtime_extent(e, unit)
            return e['evidence_id']
        if unit['backend'] == 'msc500-authentic-external16':
            external16_inputs(unit, project)
            raw_runtime_extent(e, unit)
            return e['evidence_id']
        if unit['backend'] == 'msc500-authentic-link':
            libh_inputs(unit, project)
            raw_runtime_extent(e, unit)
            return e['evidence_id']
        config, module, member, obj = runtime_inputs(unit, project)
        linked, _ = link_runtime_segment(obj, module)
        raw_runtime_extent(e, unit, linked)
        return e['evidence_id']
    if e['operation'] != 'analyze_function':
        raise ValueError(f"REA evidence target/profile mismatch: {unit['id']}")
    if unit.get('extended_extent'):
        if unit['language'] != 'c' or unit['extended_extent'].get('kind') not in (
                'packet_receive_switch_cleanup_ddd3_v1', 'command_key_cleanup_fd6a_v1', 'input_dialog_switch_cleanup_260c_v1', 'book_skip_8577_v1', 'shared_book_skip_8577_v1', 'shared_book_skip_literals78_8577_v1', 'unreachable_return_gap_v1', 'unreachable_forward_jump_gap_v1', 'segmented_evaluation_v1',
                'inline_switch_table_v1', 'inline_switch_zero_return_v1', 'step_switch_872a_v1', 'alternate_view_switch_7e6b_v1', 'signed_signum_return_gaps_v1',
                'dual_inline_switch_6167_v1', 'task_dispatch_switch_67fb_v1',
                'effect_task_gap_6ab1_v1', 'capture_task_gap_75f6_v1',
                'face_task_gap_724d_v1', 'text_input_expanded_1064_v1',
                'obtain_input_dead_branches_0254_v1', 'board_pointer_expanded_0daf_v1', 'prompt_dead_switches_1296_v1',
                'keyboard_switches_1917_v1', 'board_action_cleanup_20d5_v1', 'input_wait_restored_1da9_v1',
                'input_wait_screen_names_1da9_v2', 'board_action_screen_names_20d5_v2',
                'main_unreachable_epilogue_0010_v1'):
            raise ValueError('Extended code extents require a supported compiler-proved C boundary')
        # The complete extra-byte proof is checked after fresh compilation, with
        # its independent CodeView length. This identity check earns no credit.
        return e['evidence_id']
    proc = e['normalized_result']['procedure']
    body = proc['body']
    start = 0x10000 + int(unit['image_offset'], 0)
    ranges = [{'start': hex(start), 'end': hex(start + unit['size'] - 1)}]
    if (not body.get('available') or body.get('non_contiguous')
            or body['ranges'] != ranges or body['total_bytes'] != unit['size']
            or int(proc['address'], 0) != start):
        raise ValueError(f"REA evidence extent mismatch: {unit['id']}")
    return e['evidence_id']


def build_unit(unit: dict, image: bytes, project: Path, nasm: str, c_cache=None, output=None, reference=None, packet_context=None) -> dict:
    if unit['backend'] == packet_literal61.BACKEND:
        try:
            return packet_literal61.stage_owner(unit, project, c_cache, output, reference, compile_c, packet_context)
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return dict(unit, status='build_error', error=str(exc))
    if unit.get('owned_const_profile') is not None:
        owned_literal_const16.validate_unit_metadata(unit)
    if unit['backend'] in (mixed_refresh_chat16.BACKEND, mixed_restore_decoder16.BACKEND, mixed_motion_special16.BACKEND, mixed_tail_undo16.BACKEND, graphics_backend.BACKEND, evaluation_backend.BACKEND, remove460_backend.BACKEND, overlap_backend.BACKEND, visual_backend.BACKEND):
        try:
            if c_cache is None:
                c_cache = {}
            return (visual_backend if unit['backend'] == visual_backend.BACKEND else overlap_backend if unit['backend'] == overlap_backend.BACKEND else remove460_backend if unit['backend'] == remove460_backend.BACKEND else evaluation_backend if unit['backend'] == evaluation_backend.BACKEND else graphics_backend if unit['backend'] == graphics_backend.BACKEND else mixed_tail_undo16 if unit['backend'] == mixed_tail_undo16.BACKEND else mixed_motion_special16 if unit['backend'] == mixed_motion_special16.BACKEND else mixed_restore_decoder16 if unit['backend'] == mixed_restore_decoder16.BACKEND else mixed_refresh_chat16).build_unit(unit, image, project, c_cache, output, reference)
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return dict(unit, status='build_error', error=str(exc))
    if unit['language'] == 'asm-code':
        source = (project / unit['source']).resolve()
        if not source.is_relative_to(project.resolve()):
            raise ValueError('ASM CODE source is outside project')
        result = dict(unit)
        try:
            backend = near_game_code16 if unit['backend'] == near_game_code16.BACKEND else input_dialog_code16 if unit['backend'] == input_dialog_code16.BACKEND else remove_actor_code16 if unit['backend'] == remove_actor_code16.BACKEND else turn_task_code16 if unit['backend'] == turn_task_code16.BACKEND else special_task_code16 if unit['backend'] == special_task_code16.BACKEND else outline_piece_code16 if unit['backend'] == outline_piece_code16.BACKEND else begin_end_input_code16 if unit['backend'] == begin_end_input_code16.BACKEND else animation_init_code16 if unit['backend'] == animation_init_code16.BACKEND else graphics_driver_carrier_code16 if unit['backend'] == graphics_driver_carrier_code16.BACKEND else bios_pixel_text_code16 if unit['backend'] == bios_pixel_text_code16.BACKEND else bios_pixel_word_code16 if unit['backend'] == bios_pixel_word_code16.BACKEND else platform_code16 if unit['backend'] == platform_code16.BACKEND else graphics_wrapper_flags_code16 if unit['backend'] == graphics_wrapper_flags_code16.BACKEND else input_flags_code16 if unit['backend'] == input_flags_code16.BACKEND else graphics_wrapper_code16 if unit['backend'] == graphics_wrapper_code16.BACKEND else graphics_dgroup_code16 if unit['backend'] == graphics_dgroup_code16.BACKEND else graphics_code16 if unit['backend'] == graphics_code16.BACKEND else blit_code16 if unit['backend'] == blit_code16.BACKEND else serial_code16 if unit['backend'] == serial_code16.BACKEND else huff_allocation16
            if reference is None or reference.get('original_sha256') != backend.ORIGINAL_SHA256:
                raise ValueError('ASM CODE allocation requires original relocation context')
            built = backend.assemble(source, project) if backend in (serial_code16, blit_code16, graphics_code16, graphics_dgroup_code16, graphics_wrapper_code16, graphics_wrapper_flags_code16, input_flags_code16, platform_code16, bios_pixel_word_code16, bios_pixel_text_code16, graphics_driver_carrier_code16, animation_init_code16, begin_end_input_code16, outline_piece_code16, special_task_code16, turn_task_code16, remove_actor_code16, input_dialog_code16, near_game_code16) else backend.assemble(source, unit, nasm)
            linked, proof = backend.validate_comparison(unit, built, image, project, reference['relocations'])
            compared = compare(image[int(unit['image_offset'], 0):int(unit['image_offset'], 0)+unit['size']], linked)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'asm_code_matched'
            result.update(compared, **built.provenance)
            result.update(complete_code_allocation=built.metadata,
                          complete_allocation_proof=proof, relocations=proof['relocations'],
                          classification=('authored_near_game_CODE_component' if backend is near_game_code16 else 'authored_input_dialog_CODE_component' if backend is input_dialog_code16 else 'authored_remove_actor_CODE_component' if backend is remove_actor_code16 else 'authored_turn_task_CODE_component' if backend is turn_task_code16 else 'authored_special_task_CODE_component' if backend is special_task_code16 else 'authored_outline_piece_CODE_component' if backend is outline_piece_code16 else 'authored_begin_end_input_CODE_component' if backend is begin_end_input_code16 else 'authored_required_animation_CODE_component' if backend is animation_init_code16 else 'mixed_physical_driver_carrier' if backend is graphics_driver_carrier_code16 else 'authored_multi_entry_assembly_CODE_contribution'),
                          authored_c_function_credit=0, authored_asm_function_credit=0)
            if output is not None:
                artifact = output / 'asm-code-contributions' / (unit['id'] + '.obj')
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(built.object_bytes)
                artifact.with_suffix('.bin').write_bytes(linked)
                result['object_artifact'] = str(artifact.resolve())
            return result
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    if unit['language'] == 'runtime' and unit['backend'] == runtime_external3.BACKEND:
        result = dict(unit)
        try:
            built = runtime_external3.render_for_comparison(unit, project)
            original_sha = json.loads((project / 'config/target.json').read_text())['sha256']
            validate_rea_extent(unit, project, original_sha)
            evidence = json.loads((project / unit['rea_evidence']).read_text())
            raw_runtime_extent(evidence, unit, built.image)
            start = int(unit['image_offset'], 0)
            compared = compare(image[start:start + unit['size']], built.image)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'runtime_matched'
            result.update(compared, source_sha256=built.provenance['config_sha256'],
                          classification=built.provenance['classification'], authored_c_credit=0,
                          library_sha256=built.provenance['library_sha256'],
                          member_sha256=built.provenance['member_sha256'],
                          object_sha256=digest(built.object_bytes),
                          relocations=[built.provenance['comparison_relocation']],
                          emitted_segment=built.provenance['segment'],
                          certified_raw_record_interpretation=built.provenance)
            if output is not None:
                directory = output / 'runtime'
                directory.mkdir(parents=True, exist_ok=True)
                (directory / (unit['id'] + '.obj')).write_bytes(built.object_bytes)
                (directory / (unit['id'] + '.bin')).write_bytes(built.image)
            return result
        except (OSError, ValueError, RuntimeError) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    if unit['language'] == 'runtime' and unit['backend'] == 'msc500-authentic-external16':
        result = dict(unit)
        try:
            external16_inputs(unit, project)
            authentic = runtime_external16.build(unit['member'], project)
            built = runtime_external16.relocate_for_comparison(unit, authentic)
            original_sha = json.loads((project / 'config/target.json').read_text())['sha256']
            validate_rea_extent(unit, project, original_sha)
            evidence = json.loads((project / unit['rea_evidence']).read_text())
            raw_runtime_extent(evidence, unit, built.image)
            start = int(unit['image_offset'], 0)
            compared = compare(image[start:start + unit['size']], built.image)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'runtime_matched'
            result.update(compared, source_sha256=built.provenance['config_sha256'],
                          classification=built.provenance['classification'], authored_c_credit=0,
                          library_sha256=built.provenance['library_sha256'],
                          member_sha256=runtime_external16.SPECS['ALDIV']['sha256'],
                          object_sha256=digest(built.object_bytes),
                          relocations=[built.provenance['comparison_relocation']],
                          emitted_segment=built.provenance['members']['ALDIV']['segment'],
                          authentic_link=built.provenance)
            if output is not None:
                directory = output / 'runtime'
                directory.mkdir(parents=True, exist_ok=True)
                (directory / (unit['id'] + '.obj')).write_bytes(built.object_bytes)
                (directory / (unit['id'] + '.authentic.bin')).write_bytes(authentic.image)
                (directory / (unit['id'] + '.bin')).write_bytes(built.image)
            return result
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    if unit['language'] == 'runtime' and unit['backend'] == 'msc500-authentic-link':
        result = dict(unit)
        try:
            libh_inputs(unit, project)
            built = runtime_libh.link_member(unit['member'], project=project)
            original_sha = json.loads((project / 'config/target.json').read_text())['sha256']
            validate_rea_extent(unit, project, original_sha)
            evidence = json.loads((project / unit['rea_evidence']).read_text())
            raw_runtime_extent(evidence, unit, built.image)
            start = int(unit['image_offset'], 0)
            compared = compare(image[start:start + unit['size']], built.image)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'runtime_matched'
            result.update(compared, source_sha256=built.provenance['config_sha256'],
                          classification=built.provenance['classification'], authored_c_credit=0,
                          library_sha256=built.provenance['library_sha256'],
                          member_sha256=built.provenance['member_sha256'],
                          object_sha256=digest(built.object_bytes), relocations=[],
                          emitted_segment=built.provenance['segment'], authentic_link=built.provenance)
            if output is not None:
                directory = output / 'runtime'
                directory.mkdir(parents=True, exist_ok=True)
                (directory / (unit['id'] + '.obj')).write_bytes(built.object_bytes)
                (directory / (unit['id'] + '.bin')).write_bytes(built.image)
            return result
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    if unit['language'] == 'runtime':
        result = dict(unit)
        try:
            config, module, member, obj = runtime_inputs(unit, project)
            actual, relocations = link_runtime_segment(obj, module)
            start = int(unit['image_offset'], 0)
            compared = compare(image[start:start + unit['size']], actual)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'runtime_matched'
            for relocation in relocations:
                if relocation['mz_relocation_image_offset'] is not None:
                    relocation['mz_segment_relocation_image_offset'] = relocation['mz_relocation_image_offset']
            result.update(compared, source_sha256=digest((project / unit['source']).read_bytes()),
                          classification='independently_supplied_runtime_library', authored_c_credit=0,
                          library_sha256=config['library_sha256'], member_sha256=member.sha256,
                          runtime_archive={'url': config['archive_url'], 'sha256': config['archive_sha256']},
                          library_member_offset=member.offset, object_sha256=member.sha256,
                          relocations=relocations, emitted_segment={'index': module['segment'],
                          'length': obj.segments[module['segment']].length, 'class_name': obj.segments[module['segment']].class_name,
                          'public': unit.get('symbol'), 'public_offset': obj.publics[unit['symbol']].offset if unit.get('symbol') else None})
            if module.get('initialized_record_policy') is not None:
                result['emitted_segment'].update(runtime_lidata16.describe_input(obj, module))
            if output is not None:
                directory = output / 'runtime'
                directory.mkdir(parents=True, exist_ok=True)
                (directory / (unit['id'] + '.obj')).write_bytes(member.data)
                (directory / (unit['id'] + '.bin')).write_bytes(actual)
            return result
        except (OSError, ValueError, RuntimeError) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    source = (project / unit['source']).resolve()
    if not source.is_relative_to(project.resolve()):
        raise ValueError('Source is outside matching project')
    result = dict(unit)
    result['source_sha256'] = digest(source.read_bytes())
    if unit['backend'] == 'nasm-code-omf':
        try:
            code_backend = huff_dgroup_code16 if unit.get('object_profile') == 'huffman_core_dgroup1' else huff_code16 if unit.get('object_profile') == 'huffman_core' else asm_code16
            if reference is None or reference.get('original_sha256') != code_backend.ORIGINAL_SHA256:
                raise ValueError('Relocatable ASM CODE requires pinned original relocation context')
            built = code_backend.assemble(source, unit, nasm)
            if built.provenance['source_sha256'] != result['source_sha256']:
                raise ValueError('ASM CODE source changed during generation')
            selected, proof = code_backend.validate_comparison(
                unit, built, image, project, reference['relocations'])
            start = int(unit['image_offset'], 0)
            result.update(compare(image[start:start + unit['size']], selected),
                          **built.provenance, emitted_code_segment=built.metadata,
                          complete_allocation_proof=proof, relocations=proof.get('relocations', []),
                          classification='authored_relocatable_assembly_code', authored_c_credit=0)
            if output is not None:
                artifact = output / 'asm-code' / (unit['object_profile'] + '.obj')
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(built.object_bytes)
                artifact.with_suffix('.bin').write_bytes(bytes.fromhex(proof['whole_linked_code_hex']) if 'whole_linked_code_hex' in proof else built.code)
                result['object_artifact'] = str(artifact.resolve())
            return result
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    if unit['language'] == 'asm-data':
        try:
            if reference is None:
                raise ValueError('ASM DATA requires the pinned expanded comparison reference')
            built = (huff_workspace_data16 if unit['backend'] == huff_workspace_data16.BACKEND else graphics_screen_view_workspace_data16 if unit['backend'] == graphics_screen_view_workspace_data16.BACKEND else graphics_buffer_views_workspace_data16 if unit['backend'] == graphics_buffer_views_workspace_data16.BACKEND else graphics_splash_workspace_data16 if unit['backend'] == graphics_splash_workspace_data16.BACKEND else graphics_workspace_data16 if unit['backend'] == graphics_workspace_data16.BACKEND else hardware_state_data16 if unit['backend'] == hardware_state_data16.BACKEND else asm_data16).assemble(source, unit, nasm)
            if built.provenance['source_sha256'] != result['source_sha256']:
                raise ValueError('ASM DATA source changed between fingerprinting and assembly')
            evidence = json.loads((project / unit['rea_evidence']).read_text())
            validate_expanded_read(evidence, unit, built.data, reference, emitted_mz_sites=[])
            start = int(unit['image_offset'], 0)
            compared = compare(image[start:start + unit['size']], built.data)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'asm_data_matched'
            result.update(compared, **built.provenance, emitted_data_segment=built.metadata,
                          classification='authored_assembly_initialized_data', relocations=[],
                          authored_c_function_credit=0, authored_c_data_credit=0)
            if output is not None:
                artifact = output / 'asm-data' / (unit['id'] + '.obj')
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(built.object_bytes)
                (artifact.with_suffix('.bin')).write_bytes(built.data)
                result['object_artifact'] = str(artifact.resolve())
            return result
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    if unit['language'] in ('c', 'c-data'):
        try:
            compiler = unit['backend'].split('-')[0]
            key = (compiler, result['source_sha256'], tuple(unit['flags']))
            source_name = compiler_input_name(unit)
            if source_name != 'UNIT.C':
                key += (source_name,)
            if c_cache is None:
                c_cache = {}
            if key not in c_cache or unit['backend'] == actor70_data16.BACKEND:
                naming = {'source_name': source_name} if source_name != 'UNIT.C' else {}
                if unit['backend'] == actor70_data16.BACKEND:
                    candidate, result['actor_source_only_generation'] = actor70_data16.compile_source(source, unit, project, compiler_fn=compile_c)
                else:
                    candidate = compile_c(source, unit['flags'], compiler=compiler, **naming)
                if candidate.source_sha256 != result['source_sha256']:
                    raise ValueError('C source changed between fingerprinting and compilation; rerun')
                c_cache[key] = candidate
            compiled = c_cache[key]
            if compiled.source_sha256 != result['source_sha256']:
                raise ValueError('Cached C object source fingerprint differs from this unit')
            if getattr(compiled, 'source_name', 'UNIT.C') != source_name:
                raise ValueError('Cached C object DOS source name differs from this unit')
            obj = read_omf(compiled.object_bytes)
            if unit['source'] == history_input_literal_const16.SOURCE:
                result['history_literal_context'] = history_input_literal_const16.validate_compiled(unit, compiled, project)
            if unit['source'] == 'src/data/number_label_4c28.c':
                result['complete_char_array_type'] = input_dialog_code16.validate_label_compiled(unit, compiled, project)
            if unit['source'] == 'src/event_text_unsigned_match.c':
                import event_text_unsigned_context
                result['typed_runtime_helper_identity'] = event_text_unsigned_context.validate_compiled(unit, compiled, project)
            if unit['language'] == 'c-data':
                if reference is None:
                    raise ValueError('C data requires the pinned expanded comparison reference')
                if unit['backend'] == actor70_data16.BACKEND:
                    actual, info = actor70_data16.validate_compiled(compiled, source.read_bytes(), unit)
                    result['actor70_evidence'] = actor70_data16.validate_evidence(unit, project, reference, actual)
                    relocations = []
                elif unit['backend'] == pixel_callback_data16.BACKEND:
                    actual, info = pixel_callback_data16.validate_compiled(compiled, source.read_bytes(), unit)
                    info = dict(info)
                    relocations = info['relocations']
                    pixel_callback_data16.validate_evidence(unit, project, reference, actual, relocations)
                elif unit['backend'] == animation_labels_data16.BACKEND:
                    if output is None:
                        raise ValueError('Labels DATA requires a retained fresh LINK output root')
                    actual, info = animation_labels_data16.validate_compiled(compiled, source.read_bytes(), unit,
                        project=project, output=output / 'labels-LINK', link_emitter=emit_animation_labels)
                    relocations = []
                elif unit['backend'] == screen_far_pointer_data16.BACKEND:
                    validate_data_address(unit, reference)
                    actual, info = screen_far_pointer_data16.validate_compiled(compiled, source.read_bytes(), unit)
                    info = dict(info)
                    relocations = info.pop('relocations')
                elif unit['backend'] == 'msc500-pointer-data-omf':
                    from cdata_pointer import link_pointer_data
                    frame, _ = validate_data_address(unit, reference)
                    actual, info = link_pointer_data(obj, unit['symbol'],
                        int(unit['image_offset'], 0), frame, unit['externals'])
                    info = dict(info)
                    relocations = info.pop('relocations')
                elif unit['backend'] == text_colour_data16.BACKEND:
                    text_colour_data16.validate_unit(unit)
                    actual, info = text_colour_data16.validate_compiled(compiled, source.read_bytes())
                    relocations = []
                elif unit['backend'] == glyph_pixels_data16.BACKEND:
                    glyph_pixels_data16.validate_unit(unit)
                    actual, info = glyph_pixels_data16.validate_compiled(compiled, source.read_bytes())
                    relocations = []
                elif unit['backend'] == blit_prefix_data16.BACKEND:
                    blit_prefix_data16.validate_unit(unit)
                    actual, info = blit_prefix_data16.validate_compiled(compiled, source.read_bytes())
                    relocations = []
                elif unit['backend'] == buffer_data16.BACKEND:
                    buffer_data16.validate_unit(unit)
                    actual, info = buffer_data16.validate_compiled(compiled, source.read_bytes())
                    relocations = []
                elif unit['backend'] == history_input_literal_const16.BACKEND:
                    actual, info = history_input_literal_const16.extract_pool(unit, obj, project, reference)
                    relocations = []
                elif unit['backend'] == 'msc500-owned-data-omf':
                    actual, info = owned_data16.extract_public(unit, obj, project, reference)
                    result['owned_data_proof'] = info['owned_data_proof']
                    result['owned_data_additional_credit'] = 0
                    relocations = []
                else:
                    actual, info = extract_data(obj, unit['symbol'])
                    relocations = []
                evidence = json.loads((project / unit['rea_evidence']).read_text())
                if unit['backend'] == animation_labels_data16.BACKEND:
                    animation_labels_data16.validate_evidence(unit, project, reference['original_sha256'], reference)
                else:
                    validate_expanded_read(evidence, unit, actual, reference,
                        emitted_mz_sites=info['emitted_mz_sites'] if unit['backend'] == screen_far_pointer_data16.BACKEND else [])
            else:
                info = obj.function_info(unit['symbol'])
                if info['boundary'] != 'codeview3_procedure':
                    raise ValueError('C matching requires an emitted CodeView procedure extent')
                address = unit.get('code_address')
                image_origin = int(unit['image_offset'], 0)
                ownership = None
                selector_ownership = None
                data_ownership = None
                bss_ownership = None
                if unit.get('owned_selector_const') is not None:
                    selector_ownership, selector_bytes, proof = owned_selector_const16.validate(unit, obj, project, reference)
                    result['owned_selector_const_proof'] = proof
                    result['owned_selector_const_data_credit'] = 0
                    if output is not None:
                        directory = output / 'owned-selector-const'
                        directory.mkdir(parents=True, exist_ok=True)
                        (directory / (unit['id'] + '.bin')).write_bytes(selector_bytes)
                if unit.get('owned_const') is not None:
                    ownership, const_bytes, proof = owned_const16.validate(unit, obj, project, reference)
                    result['owned_const_proof'] = proof
                    result['owned_const_data_credit'] = 0
                    if output is not None:
                        directory = output / 'owned-const'
                        directory.mkdir(parents=True, exist_ok=True)
                        (directory / (unit['id'] + '.bin')).write_bytes(const_bytes)
                if unit.get('owned_data') is not None:
                    data_ownership, data_bytes, proof = owned_data16.validate(unit, obj, project, reference)
                    result['owned_data_proof'] = proof
                    result['owned_data_additional_credit'] = 0
                    if output is not None:
                        directory = output / 'owned-data'
                        directory.mkdir(parents=True, exist_ok=True)
                        (directory / (unit['id'] + '.bin')).write_bytes(data_bytes)
                if unit.get('owned_bss') is not None:
                    bss_ownership, proof = owned_bss16.validate(unit, obj, project, reference)
                    result['owned_bss_proof'] = proof
                    result['owned_bss_additional_credit'] = 0
                actual, relocations = link_function(obj, unit['symbol'],
                    address['offset'] if address is not None else image_origin,
                    unit.get('externals', {}), image_origin=image_origin, owned_const=ownership, owned_data=data_ownership, owned_bss=bss_ownership, owned_selector_const=selector_ownership)
            if unit.get('extended_extent'):
                target_sha = json.loads((project / 'config/target.json').read_text())['sha256']
                result['extended_extent_proof'] = validate_extended_extent(unit, project, target_sha, info, actual, source_object=obj)
            start = int(unit['image_offset'], 0)
            compared = compare(image[start:start + unit['size']], actual)
            if compared['status'] == 'asm_matched':
                compared['status'] = 'c_data_matched' if unit['language'] == 'c-data' else 'c_matched'
            result.update(compared)
            result.update(compiler='Microsoft C ' + {'msc400': '4.00', 'msc500': '5.00', 'msc510': '5.10'}[compiled.compiler], compiler_flags=list(compiled.flags),
                          build_command=list(compiled.command), object_sha256=digest(compiled.object_bytes),
                          compiler_log=compiled.compiler_log,
                          compiler_tool_hashes=compiled.tool_hashes,
                          relocations=relocations,
                          toolchain_manifest_sha256=compiled.toolchain_manifest_sha256,
                          **{('emitted_data_segment' if unit['language'] == 'c-data' else 'emitted_procedure'):
                             {k: v for k, v in info.items() if k != 'fixups'}})
            if unit['backend'] == actor70_data16.BACKEND:
                result.update(source_literal_bytes=2, source_iterated_bytes=1958, authentic_LINK_alignment_bytes=0)
            if unit['backend'] == animation_labels_data16.BACKEND:
                result.update(source_literal_bytes=14, authentic_LINK_alignment_bytes=1, LINK_zero_prefix_credit=0, outside_extent_credit=0)
            if unit['language'] == 'c-data':
                result.update(classification=('authored_c_initialized_pointer_data'
                    if unit['backend'] in ('msc500-pointer-data-omf', screen_far_pointer_data16.BACKEND) else 'authored_c_initialized_data'),
                    authored_c_function_credit=0)
            if output is not None:
                flag_id = digest(json.dumps(unit['flags']).encode())[:8]
                if source_name != 'UNIT.C':
                    flag_id = digest(json.dumps({'flags': unit['flags'], 'source_name': source_name}, sort_keys=True).encode())[:8]
                artifact = output / 'objects' / (compiler + '-' + result['source_sha256'][:16] + '-' + flag_id + '.obj')
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(compiled.object_bytes)
                result['object_artifact'] = str(artifact.resolve())
            return result
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
    # A fresh directory on every build prevents stale output from earning credit.
    with tempfile.TemporaryDirectory(prefix='bc-match-') as tmp:
        output = Path(tmp) / 'unit.bin'
        cmd = [nasm, '-f', 'bin', '-Ox', str(source), '-o', str(output)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return result | {'status': 'build_error', 'error': str(exc)}
        result['build_command'] = cmd[:-1] + ['<fresh-temp>/unit.bin']
        if p.returncode or not output.is_file():
            return result | {'status': 'build_error', 'error': (p.stderr or p.stdout).strip()}
        start = int(unit['image_offset'], 0)
        return result | compare(image[start:start + unit['size']], output.read_bytes())


def validate_emitted_mz_sites(unit: dict, original_sites) -> None:
    """Require every loader relocation in a complete matched C/runtime extent."""
    start = int(unit['image_offset'], 0)
    end = start + unit['size']
    expected = {p for p in original_sites if start <= p < end}
    if any(p + 2 > end for p in expected):
        raise ValueError('Original MZ relocation crosses the complete unit extent')
    emitted = {r['mz_segment_relocation_image_offset'] for r in unit.get('relocations', [])
               if 'mz_segment_relocation_image_offset' in r}
    if emitted != expected:
        label = {'c': 'C', 'c-data': 'C DATA', 'asm-data': 'ASM DATA', 'asm-code': 'ASM CODE'}.get(unit['language'], 'Runtime')
        raise ValueError(f'{label} MZ relocation set differs from complete original extent')


def inventory(root: Path, index: bytes, units: list[dict]) -> list[dict]:
    reviewed = {int(u['image_offset'], 0): u for u in units}
    rows, seen = [], set()
    for line in index.decode().splitlines():
        address, blocks, size, name = line.split()
        a = int(address, 0)
        if a in seen:
            raise ValueError('Duplicate legacy candidate')
        seen.add(a)
        files = sorted((root / 'docs/decompiled/funcs').glob(f'{address}_*.c'))
        unit = reviewed.get(a)
        rows.append({
            'image_offset': f'0x{a:05x}', 'legacy_name': name,
            'legacy_reported_size': int(size), 'legacy_basic_blocks': int(blocks),
            'boundary_status': 'reviewed' if unit else 'unreviewed',
            'reviewed_size': unit['size'] if unit else '',
            'c_match_status': 'todo',
            'pseudocode_status': ('nonempty' if files[0].read_bytes().strip() else 'empty') if len(files) == 1 else 'missing_or_ambiguous',
            'pseudocode_path': str(files[0].relative_to(root)) if len(files) == 1 else '',
            'unit': unit['id'] if unit else '',
        })
    # The legacy candidate inventory is incomplete. Reviewed units absent from
    # it remain in report.units and byte coverage; never invent legacy rows or
    # count those entries in the pinned 371-candidate denominator. Every reviewed
    # extent has already passed its independent REA/backend boundary checks.
    return sorted(rows, key=lambda r: int(r['image_offset'], 0))


def reconcile_candidates(project: Path, rows: list[dict], target_sha256: str) -> list[dict]:
    e = json.loads((project / 'evidence/rea_procedures.json').read_text())
    if e['subject']['digest']['sha256'] != target_sha256:
        raise ValueError('REA candidate inventory belongs to a different target')
    legacy = {int(r['image_offset'], 0): r['legacy_name'] for r in rows}
    ghidra = {int(r['address'], 0) - 0x10000: r['value'] for r in e['normalized_result']}
    return [dict(image_offset=hex(a), r2_name=legacy.get(a, ''),
                 rea_ghidra_name=ghidra.get(a, ''),
                 discovery=('both' if a in legacy and a in ghidra else 'r2_only' if a in legacy else 'ghidra_only'),
                 function_status='candidate_requires_review')
            for a in sorted(set(legacy) | set(ghidra))]


def report_markdown(report: dict) -> str:
    s = report['summary']
    lines = [
        '# Battle Chess matching progress', '',
        'Generated by `python3 matching/check.py`; do not edit these figures by hand.', '',
        f"Target SHA-256: `{report['target']['sha256']}`.", '',
        '| Measure | Verified result |', '|---|---:|',
        f"| C/C++ functions rebuilt to matching bytes | {s['c_matched_functions']} |",
        f"| Matching C-generated code bytes | {s['c_matched_bytes']} |",
        f"| Standalone authored C data contributions | {s['source_data_units']} |",
        f"| Verified C-source DATA span bytes (zero function credit) | {s['source_data_bytes']} |",
        f"| C-emitted literal DATA bytes | {s.get('source_data_literal_bytes', s['source_data_bytes'])} |",
        f"| C-emitted iterated DATA bytes | {s.get('source_data_iterated_bytes', 0)} |",
        f"| Authentic LINK alignment bytes (zero C credit) | {s.get('source_data_authentic_LINK_alignment_bytes', 0)} |",
        f"| Assembly functions rebuilt to matching bytes | {s['asm_matched_functions']} |",
        f"| Matching assembly bytes | {s['asm_matched_bytes']} |",
        f"| Assembly initialized DATA contributions (zero C/function credit) | {s.get('asm_data_matched_units', 0)} |",
        f"| Matching assembly initialized DATA bytes | {s.get('asm_data_matched_bytes', 0)} |",
        f"| Assembly CODE contributions (zero function/C credit) | {s.get('asm_code_matched_units', 0)} |",
        f"| Matching assembly CODE contribution bytes | {s.get('asm_code_matched_bytes', 0)} |",
        f"| Assembly CODE contribution MZ sites | {s.get('asm_code_emitted_mz_relocations', 0)} |",
        f"| Independently linked runtime library units | {s['runtime_matched_units']} |",
        f"| Matching runtime library bytes (zero C/ASM credit) | {s['runtime_matched_bytes']} |",
        f"| Of those, initialized data bytes in the expanded image | {s['runtime_matched_data_bytes']} |",
        f"| Runtime-emitted MZ segment relocations verified | {s['runtime_emitted_mz_relocations']} |",
        f"| C procedure-emitted MZ segment relocations verified | {s['source_emitted_mz_relocations']} / {report['full_build_requirements']['mz_relocation_count']} |",
        f"| C DATA-emitted MZ segment relocations verified | {s.get('sourcedata_emitted_mz_relocations', 0)} |",
        f"| Verified union MZ segment relocations | {s.get('verified_emitted_mz_relocations', 0)} / {report['full_build_requirements']['mz_relocation_count']} |",
        f"| Compiler-owned context MZ sites (zero extra byte credit) | {s.get('owned_context_emitted_mz_relocations', 0)} |",
        f"| Reviewed code/data extents | {s['reviewed_extents']} |",
        f"| Extents corroborated by retained REA MCP evidence | {s['rea_confirmed_extents']} |",
        f"| Legacy r2 function candidates | {s['legacy_candidates']} |",
        f"| Nonempty autogenerated pseudocode files | {s['nonempty_pseudocode']} |",
        f"| Empty autogenerated pseudocode files | {s['empty_pseudocode']} |",
        f"| Failed reviewed builds/comparisons | {s['failed_units']} |", '',
        '**Goal: reproduce all original executable bytes.** The full executable '
        'has not been built. Function matches are intermediate evidence, not a '
        'claim of a complete executable match.', '',
        f"Verified source-built and independently linked runtime spans currently cover {s['verified_file_span_bytes']} "
        f"of {report['target']['file_bytes']:,} file bytes "
        f"({s['verified_file_span_percent']:.3f}%). Headers, data, alignment, remaining runtime "
        'and packing must also be independently rebuilt. See `file_coverage.json` '
        'for every covered and remaining file range.', '',
        f"Verified expanded-image spans cover {s['verified_image_span_bytes']} of "
        f"{s['expanded_image_bytes']:,} prepack image bytes. Initialized data inside "
        'the compressed region earns no packed-file byte credit. See `image_coverage.json` '
        'for its separate exact-byte accounting.', '',
        f"Assembly matches cover {s['asm_matched_functions']}/{s['legacy_candidates']} "
        f"legacy candidates ({100*s['asm_matched_functions']/s['legacy_candidates']:.2f}%). "
        'This is provisional candidate coverage, not a whole-game completion percentage.', '',
        f"The packed initialized MZ image contains {report['target']['image_bytes']:,} bytes, including "
        'code, compressed data and the unpacker. Its length is **not** a code-size denominator. The old inventories '
        'have incomplete/false function extents; a trustworthy total code-byte denominator '
        'and whole-program completion percentage are still unknown.', '',
        f"REA/Ghidra and r2 agree on {s['candidate_overlap']} candidate entries; "
        f"{s['r2_only_candidates']} occur only in r2 and {s['ghidra_only_candidates']} only "
        'in Ghidra. See `analysis_candidates.csv`; disagreement does not establish '
        'that a candidate is code or data.', '',
        'C matches are emitted by pinned Microsoft C 4.00/5.00/5.10 compilers inside DOSBox, '
        'with function extents taken from its CodeView records. No inline assembly, '
        'opcode emission, target-dependent trimming or address masking earns C credit. '
        'Portable semantic C source and the Rust engine receive no byte-match credit. '
        'This establishes a reproducing toolchain for the matched functions; exact '
        'historical release attribution and other modules\' flags remain under investigation. '
        'No complete executable is rebuilt yet.', '',
        '## Reviewed units', '',
        '| Image offset | Function | Bytes | Status |', '|---|---|---:|---|',
    ]
    for u in report['units']:
        lines.append(f"| `{u['image_offset']}` | {u['id']} | {u['size']} | {u['status']} |")
    return '\n'.join(lines) + '\n'


def run(root: Path, project: Path, target: Path, output: Path, nasm: str, *, lifecycle=None) -> dict:
    config = json.loads((project / 'config/target.json').read_text())
    data = pinned(target, config['sha256'])
    header, image = mz_image(data)
    unpacked = unpack_exepack(data)
    reference = build_reference(data)
    index = pinned(root / config['legacy_index']['path'], config['legacy_index']['sha256'])
    units = json.loads((project / 'config/units.json').read_text())
    validate_units(units, len(image), len(reference['image']))
    ordinary_units, deferred_jobs = (units, []) if lifecycle is None else lifecycle.partition_jobs(
        units=units, project=project, target_sha256=digest(data), reference=reference)
    source_inputs = build_source_inputs(project, target, output / 'source-allocations',
                                       defined_symbols={u['symbol'] for u in units if 'symbol' in u})
    if any(int(u['image_offset'], 0) + u['size'] > unpacked.prefix_size for u in units
           if u.get('reference_region') != 'exepack-expanded'):
        raise ValueError('Direct-file function match crosses into the compressed EXEPACK tail')
    for u in units:
        if u.get('runtime_entry') and (u['language'] != 'runtime' or
                unpacked.saved_cs * 16 + unpacked.saved_ip != int(u['image_offset'], 0)):
            raise ValueError('Runtime startup does not match original saved EXEPACK entry')
    rea_ids = {u['id']: validate_rea_extent(u, project, digest(data), reference) for u in ordinary_units}
    rows = inventory(root, index, units)
    reconciled = reconcile_candidates(project, rows, digest(data))
    c_cache = {}
    results = [build_unit(u, reference['image'] if u.get('reference_region') == 'exepack-expanded' else image,
                          project, nasm, c_cache, output, reference=reference,
                          packet_context=lifecycle.packet_context if lifecycle is not None else None) for u in ordinary_units]
    if lifecycle is not None:
        results, deferred_rea_ids, lifecycle_receipt = lifecycle.finish_source_phase(
            units=units, ordinary_units=ordinary_units, deferred_jobs=deferred_jobs,
            results=results, source_inputs=source_inputs, project=project, output=output,
            reference=reference)
        if set(deferred_rea_ids) != {u['id'] for u in deferred_jobs}:
            raise ValueError('Deferred runtime evidence ID set differs from the exact partition')
        if [r['id'] for r in results] != [u['id'] for u in units]:
            raise ValueError('Lifecycle returned missing/duplicate/reordered unit results')
        rea_ids.update(deferred_rea_ids)
    for result in results:
        result['rea_evidence_id'] = rea_ids[result['id']]
        result['comparison_reference'] = {
            'region': result.get('reference_region', 'unchanged-prefix'),
            'original_sha256': digest(data),
            'carrier_sha256': reference['carrier_sha256'] if result.get('reference_region') == 'exepack-expanded' else None,
            'masked_bytes': 0,
        }
        for relocation in result.get('relocations', []):
            position = relocation.get('mz_segment_relocation_image_offset')
            if position is not None and position not in unpacked.relocations:
                result.update(status='build_error', error=f'Emitted MZ segment relocation absent from original: {position:#x}')
        if result['status'] in ('c_matched', 'c_data_matched', 'asm_data_matched', 'asm_code_matched', 'runtime_matched'):
            try:
                validate_emitted_mz_sites(result, unpacked.relocations)
            except ValueError as exc:
                result.update(status='build_error', error=str(exc))
    for row in rows:
        unit = next((u for u in results if u['id'] == row['unit']), None)
        row['match_status'] = unit['status'] if unit else 'todo'
        if unit and unit['language'] == 'c':
            row['c_match_status'] = unit['status']
    matched = [u for u in results if u['status'] == 'asm_matched']
    c_matched = [u for u in results if u['status'] == 'c_matched']
    data_matched = [u for u in results if u['status'] == 'c_data_matched']
    asm_data_matched = [u for u in results if u['status'] == 'asm_data_matched']
    asm_code_matched = [u for u in results if u['status'] == 'asm_code_matched']
    runtime_matched = [u for u in results if u['status'] == 'runtime_matched']
    verified = sorted(matched + c_matched + data_matched + asm_data_matched + asm_code_matched + runtime_matched, key=lambda u: int(u['image_offset'], 0))
    file_verified = [u for u in verified if u.get('reference_region') != 'exepack-expanded']
    coverage = []
    cursor = 0
    for u in file_verified:
        start = header + int(u['image_offset'], 0)
        if cursor < start:
            coverage.append({'start': cursor, 'end': start, 'status': 'unreconstructed'})
        coverage.append({'start': start, 'end': start + u['size'], 'status': u['status'],
                         'unit': u['id'], 'source': u['source'], 'source_sha256': u['source_sha256']})
        cursor = start + u['size']
    if cursor < len(data):
        coverage.append({'start': cursor, 'end': len(data), 'status': 'unreconstructed'})
    verified_bytes = sum(u['size'] for u in file_verified)
    image_coverage, cursor = [], 0
    for u in verified:
        start = int(u['image_offset'], 0)
        if cursor < start:
            image_coverage.append({'start': cursor, 'end': start, 'status': 'unreconstructed'})
        image_coverage.append({'start': start, 'end': start + u['size'], 'status': u['status'],
                               'unit': u['id'], 'source': u['source'], 'source_sha256': u['source_sha256']})
        cursor = start + u['size']
    if cursor < len(reference['image']):
        image_coverage.append({'start': cursor, 'end': len(reference['image']), 'status': 'unreconstructed'})
    emitted_mz_relocations = sorted({r['mz_segment_relocation_image_offset']
                                     for u in c_matched for r in u.get('relocations', [])
                                     if 'mz_segment_relocation_image_offset' in r})
    runtime_mz_relocations = sorted({r['mz_segment_relocation_image_offset'] for u in runtime_matched for r in u.get('relocations', []) if 'mz_segment_relocation_image_offset' in r})
    asm_code_mz_relocations = sorted({r['mz_segment_relocation_image_offset'] for u in asm_code_matched for r in u.get('relocations', []) if 'mz_segment_relocation_image_offset' in r})
    sourcedata_mz_proof = collect_source_data_mz(results, project, reference, unpacked.relocations)
    sourcedata_mz_relocations = sourcedata_mz_proof['sites']
    owned_context_mz_proof = owned_context_mz.collect_owned_context_mz(
        results, project, reference, unpacked.relocations)
    owned_context_mz_relocations = owned_context_mz_proof['sites']
    verified_mz_relocations = sorted(set(emitted_mz_relocations) | set(runtime_mz_relocations) | set(asm_code_mz_relocations) | set(owned_context_mz_relocations) | set(sourcedata_mz_relocations))
    try:
        version = subprocess.run([nasm, '-v'], capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        version = 'unavailable'
    report = {
        'schema_version': 4,
        'target': {'sha256': digest(data), 'file_bytes': len(data), 'header_bytes': header, 'image_bytes': len(image)},
        'policy': {'comparison': 'exact_original_prefix_or_provenance_bound_expanded_image', 'masked_bytes': 0,
                   'c_backend': 'msc-omf', 'runtime_backend': 'independently_pinned_omf_library', 'runtime_c_credit': 0, 'inventory': 'legacy_r2_candidates_not_exhaustive',
                   'reference_region': 'verified_unchanged_EXEPACK_prefix_and_explicit_provenance_bound_expanded_contributions',
                   'reference_prefix_bytes': unpacked.prefix_size,
                   'expanded_carrier_sha256': reference['carrier_sha256'],
                   'expanded_data_earns_packed_file_credit': False,
                   'c_data_backend': 'complete_standalone_initialized_omf_data_or_explicit_DGROUP_near_pointers_or_closed_screen_FAR16',
                   'c_data_no_fixup_backend_unchanged': True,
                   'asm_data_backend': 'whole_numeric_DD_WORD_nasm_DATA_or_closed_mixed_width_MASM_hardware_DATA',
                   'asm_data_c_credit': 0,
                   'asm_data_function_credit': 0,
                   'asm_code_backend': 'closed_complete_multi_entry_OMF_CODE_allocation',
                   'asm_code_c_credit': 0,
                   'asm_code_function_credit': 0,
                   'complete_asm_code_mz_sets_required': True,
                   'pointer_data_backend': 'whole_SEGDEF_named_OFFSET16_DGROUP_CV3_debug_validated',
                   'far_pointer_data_backend': 'closed_whole_DATA4_frame5_external_FAR16_selector_MZ',
                   'far_pointer_pointee_allocation_claim': False,
                   'c_data_function_credit': 0,
                   'far_segment_relocations_checked': True,
                   'complete_c_runtime_mz_sets_required': True},
        'full_build_requirements': {'uncompressed_image_bytes': 401131,
                                    'mz_relocation_count': len(unpacked.relocations),
                                    'packer': 'Microsoft EXEPACK 4.06',
                                    'source_built_image_available': False},
        'toolchain': {'nasm': version,
                      'c_profiles_used': sorted({u['backend'].split('-')[0] for u in units if u['language'] in ('c', 'c-data')}),
                      'c_provenance_configs': ['config/' + p + '.json' for p in sorted({u['backend'].split('-')[0] for u in units if u['language'] in ('c', 'c-data')})],
                      'best_supported_original_compiler': 'Microsoft C 5.00',
                      'historical_attribution': 'C5.00 default optimization and explicit size-optimized profiles reproduce every current C unit; archived runtime links exactly. C4.00 reproduces some ambiguous outputs but is not required. Exact historical commands remain unproven'},
        'summary': {
            'c_matched_functions': len(c_matched), 'c_matched_bytes': sum(u['size'] for u in c_matched),
            'asm_code_matched_units': len(asm_code_matched),
            'asm_code_matched_bytes': sum(u['size'] for u in asm_code_matched),
            'asm_code_emitted_mz_relocations': len(asm_code_mz_relocations),
            'asm_data_matched_units': len(asm_data_matched),
            'asm_data_matched_bytes': sum(u['size'] for u in asm_data_matched),
            'source_data_units': len(data_matched), 'source_data_bytes': sum(u['size'] for u in data_matched),
            'source_data_literal_bytes': sum(u.get('source_literal_bytes', u['size']) for u in data_matched),
            'source_data_iterated_bytes': sum(u.get('source_iterated_bytes', 0) for u in data_matched),
            'source_data_authentic_LINK_alignment_bytes': sum(u.get('authentic_LINK_alignment_bytes', 0) for u in data_matched),
            'asm_matched_functions': len(matched), 'asm_matched_bytes': sum(u['size'] for u in matched),
            'runtime_matched_units': len(runtime_matched), 'runtime_matched_bytes': sum(u['size'] for u in runtime_matched),
            'runtime_matched_data_bytes': sum(u['size'] for u in runtime_matched if u.get('runtime_kind') == 'initialized_data'),
            'runtime_emitted_mz_relocations': len(runtime_mz_relocations),
            'reviewed_extents': len(units), 'legacy_candidates': len(rows),
            'rea_confirmed_extents': len(rea_ids),
            'candidate_overlap': sum(r['discovery'] == 'both' for r in reconciled),
            'r2_only_candidates': sum(r['discovery'] == 'r2_only' for r in reconciled),
            'ghidra_only_candidates': sum(r['discovery'] == 'ghidra_only' for r in reconciled),
            'nonempty_pseudocode': sum(r['pseudocode_status'] == 'nonempty' for r in rows),
            'empty_pseudocode': sum(r['pseudocode_status'] == 'empty' for r in rows),
            'failed_units': len(units) - len(matched) - len(c_matched) - len(data_matched) - len(asm_data_matched) - len(asm_code_matched) - len(runtime_matched),
            'whole_program_completion_percent': None,
            'verified_file_span_bytes': verified_bytes,
            'verified_file_span_percent': 100 * verified_bytes / len(data),
            'remaining_file_span_bytes': len(data) - verified_bytes,
            'verified_image_span_bytes': sum(u['size'] for u in verified),
            'expanded_image_bytes': len(reference['image']),
            'full_executable_match': False,
            'source_emitted_mz_relocations': len(emitted_mz_relocations),
            'sourcedata_emitted_mz_relocations': len(sourcedata_mz_relocations),
            'sourcedata_emitted_mz_sites': sourcedata_mz_relocations,
            'verified_emitted_mz_relocations': len(verified_mz_relocations),
            'owned_context_emitted_mz_relocations': len(owned_context_mz_relocations),
            'owned_context_emitted_mz_sites': owned_context_mz_relocations,
        },
        'source_allocation_inputs': report_inputs(source_inputs),
        'units': results,
    }
    if lifecycle is not None:
        report['build_lifecycle'] = lifecycle_receipt
        if lifecycle_receipt.get('machine_layout_inputs'):
            report['machine_layout_inputs'] = lifecycle_receipt['machine_layout_inputs']
    output.mkdir(parents=True, exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'PROGRESS.md').write_text(report_markdown(report))
    (output / 'file_coverage.json').write_text(json.dumps({
        'target_sha256': digest(data), 'total_bytes': len(data),
        'rebuilt_executable': None, 'full_executable_match': False,
        'ranges_are_half_open': True, 'ranges': coverage,
    }, indent=2) + '\n')
    (output / 'image_coverage.json').write_text(json.dumps({
        'original_sha256': digest(data), 'carrier_sha256': reference['carrier_sha256'],
        'total_bytes': len(reference['image']), 'rebuilt_executable': None,
        'full_executable_match': False, 'ranges_are_half_open': True,
        'packed_file_credit': False, 'ranges': image_coverage,
    }, indent=2) + '\n')
    (output / 'relocation_coverage.json').write_text(json.dumps({
        'original_image_relocation_sites': list(unpacked.relocations),
        'source_emitted_sites': emitted_mz_relocations,
        'sourcedata_emitted_sites': sourcedata_mz_relocations,
        'sourcedata_proof': sourcedata_mz_proof,
        'runtime_emitted_sites': runtime_mz_relocations,
        'asm_code_emitted_sites': asm_code_mz_relocations,
        'owned_context_emitted_sites': owned_context_mz_relocations,
        'owned_context_proof': owned_context_mz_proof,
        'verified_emitted_sites': verified_mz_relocations,
        'remaining_sites': [p for p in unpacked.relocations if p not in verified_mz_relocations],
        'complete': set(verified_mz_relocations) == set(unpacked.relocations),
    }, indent=2) + '\n')
    with (output / 'functions.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (output / 'analysis_candidates.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(reconciled[0]))
        writer.writeheader()
        writer.writerows(reconciled)
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target', type=Path, default=ROOT / 'CHESS.EXE')
    p.add_argument('--output', type=Path, default=HERE / 'build')
    p.add_argument('--nasm', default='nasm')
    p.add_argument('--require-complete', action='store_true', help='Fail until an independently rebuilt full executable matches')
    args = p.parse_args()
    try:
        report = run(ROOT, HERE, args.target, args.output, args.nasm)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        # Do not leave an old successful report at the requested report location.
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'report.json').write_text(json.dumps({'status': 'error', 'error': str(exc)}, indent=2) + '\n')
        (args.output / 'PROGRESS.md').write_text(f'# Verification failed\n\n{exc}\n')
        (args.output / 'functions.csv').unlink(missing_ok=True)
        (args.output / 'analysis_candidates.csv').unlink(missing_ok=True)
        (args.output / 'file_coverage.json').unlink(missing_ok=True)
        (args.output / 'relocation_coverage.json').unlink(missing_ok=True)
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    for u in report['units']:
        print(f"{u['status']:12s} {u['image_offset']} {u['id']} ({u['size']} bytes)")
        if u.get('error'):
            print(u['error'])
        if u.get('first_difference') is not None:
            print(f"  first difference at +0x{u['first_difference']:x}; expected {u['expected_byte']}, actual {u['actual_byte']}")
    s = report['summary']
    print(f"C matches: {s['c_matched_functions']} ({s['c_matched_bytes']} bytes); C data: {s['source_data_units']} ({s['source_data_bytes']} bytes); ASM matches: {s['asm_matched_functions']} ({s['asm_matched_bytes']} bytes); ASM DATA: {s['asm_data_matched_units']} ({s['asm_data_matched_bytes']} bytes); ASM CODE contributions: {s['asm_code_matched_units']} ({s['asm_code_matched_bytes']} bytes); runtime matches: {s['runtime_matched_units']} ({s['runtime_matched_bytes']} bytes); {s['legacy_candidates']} legacy candidates")
    print(f'Reports: {args.output.resolve()}')
    return int(bool(s['failed_units'] or (args.require_complete and not s['full_executable_match'])))


if __name__ == '__main__':
    raise SystemExit(main())
