"""Isolated ordinary owner adapter; fresh generation capability stays in-process."""
from pathlib import Path
from dataclasses import dataclass
import copy
import hashlib
import json
import mixed_evaluation_generation16 as generation
import mixed_evaluation_compare16 as comparison
from mixed_evaluation_source16 import SOURCES, C_SOURCE_SHA256
from omf import read_omf
from link16 import link_function

D = Path(__file__).resolve().parent
H = lambda b: hashlib.sha256(b).hexdigest()
_CAP = object()

def need(v, m):
    if not v:
        raise ValueError(m)

def owners():
    raw = Path(__file__).with_name('mixed_evaluation_units.json').read_bytes()
    need(H(raw) == OWNERS_SHA256, 'closed owner contracts changed')
    return json.loads(raw)

def signature(b):
    return tuple(H(v) for v in (b.object_bytes, b.c5_sidecar_bytes,
                                b.fresh_fa_bytes, b.mixed_source_bytes)) + (
        H(json.dumps(b.provenance, sort_keys=True).encode()),)

@dataclass(frozen=True)
class _FreshEntry:
    cap: object
    cache_id: int
    built: object
    signature: tuple
    code: bytes
    proof: dict

def cache_key(project, reference):
    project = Path(project)
    paths = [D / n for n in ('mixed_evaluation16.py', 'mixed_evaluation_generation16.py',
                            'mixed_evaluation_source16.py', 'mixed_evaluation_compare16.py',
                            'mixed_evaluation_profile.json', 'mixed_evaluation_units.json')]
    paths += [Path(__file__), Path(comparison.__file__), Path(__file__).with_name('mixed_evaluation_units.json')]
    paths += [D / s['file'] for s in SOURCES.values()]
    paths += [project / generation.C_SOURCE, Path('/usr/bin/dosbox').resolve(),
              project / 'config/msc500.json', project / 'config/msc510.json',
              project / 'toolchains/msc500/manifest.json',
              project / 'toolchains/msc510/manifest.json',
              project / 'toolchains/msc510/LICENSE', project / 'toolchains/msc510/MASM.EXE']
    paths += [project / 'toolchains/msc500' / r['name']
              for r in json.loads((project / 'config/msc500.json').read_text())['files']]
    return (generation.BACKEND, tuple((str(p.resolve()), H(p.read_bytes())) for p in paths),
            H(reference['image']), tuple(reference['relocations']),
            reference['original_sha256'], reference['carrier_sha256'])

def assemble(source, project):
    return generation.assemble(source, project)

def build_unit(u, image, project, cache, output, reference):
    contracts = owners()
    need(u.get('id') in contracts and u == contracts[u['id']], 'exact owner required')
    need(type(cache) is dict and type(image) is bytes and (image == reference['image'] or (len(image) == 82903 and H(image) == '643f5e20f063f212f496a40ecac9b3242c4fdede18c865fc26ce0be1f37862dc')), 'current cache and exact original MZ or expanded reference image required')
    key = cache_key(project, reference)
    if key not in cache:
        b = assemble(Path(project) / generation.C_SOURCE, project)
        code, proof = comparison.compare(b, reference, project)
        cache[key] = _FreshEntry(_CAP, id(cache), b, signature(b), code, proof)
    e = cache[key]
    need(type(e) is _FreshEntry and e.cap is _CAP and e.cache_id == id(cache),
         'same current-run factory cache; retained fixtures are not fresh')
    need(e.signature == signature(e.built), 'cached actual build mutated')
    b = e.built
    start = int(u['image_offset'], 0); off = start - 0xfdf2
    actual = e.code[off:off + u['size']]
    need(len(actual) == u['size'] and actual == image[start:start + u['size']], 'whole owner bytes')
    isc = u['language'] == 'c'
    proof = copy.deepcopy(e.proof)
    proof.update(whole_native_equal=True, C5_sidecar_not_SOURCE=True)
    if isc:
        c = read_omf(b.c5_sidecar_bytes)
        body, relocations = link_function(c, u['symbol'], u['code_address']['offset'], u['externals'], image_origin=start)
        need(body == actual, 'genuine C sidecar must equal final span')
    else:
        relocations = [dict(f, object_offset=f['raw']['offset'],
                            field_image_offset=0xfdf2 + f['raw']['offset'],
                            unit_offset=f['raw']['offset'] - off)
                       for f in proof['all_fields'] if off <= f['raw']['offset'] < off + u['size']]
        # Derive loader sites from the verified OMF segment fixups. The final
        # checker consumes this common relocation field for every backend.
        for relocation in relocations:
            if relocation['raw']['location_type'] == 2:
                need(relocation['raw']['width'] == 2, 'complete segment relocation word')
                relocation['mz_segment_relocation_image_offset'] = relocation['field_image_offset']
            elif relocation['raw']['location_type'] == 3:
                need(relocation['raw']['width'] == 4, 'complete far pointer relocation')
                relocation['mz_segment_relocation_image_offset'] = relocation['field_image_offset'] + 2
        emitted = {r['mz_segment_relocation_image_offset'] for r in relocations
                   if 'mz_segment_relocation_image_offset' in r}
        need(emitted == {s for s in proof['native_MZ'] if start <= s < start + u['size']},
             'owner OMF segment fixups must equal verified native MZ sites')
    result = dict(u, status='c_matched' if isc else 'asm_code_matched',
                  expected_size=len(actual), actual_size=len(actual),
                  expected_sha256=H(actual), actual_sha256=H(actual),
                  first_difference=None, expected_byte=None, actual_byte=None,
                  object_sha256=H(b.object_bytes), relocations=relocations,
                  mixed_object_proof=proof, mixed_profile='evaluation3902_v1',
                  classification='compiler_produced_C_in_mixed_module' if isc else 'authored_ASM_in_mixed_module',
                  comparison_object_role='genuine_C5_typed_sidecar' if isc else 'final_mixed_span',
                  compiler='Microsoft C 5.00' if isc else None,
                  compiler_flags=['/AM', '/Gs', '/Zi'] if isc else [],
                  build_command=[p['command'] for p in b.provenance['processes']],
                  mixed_generation_provenance=copy.deepcopy(b.provenance),
                  authored_c_function_credit=1 if isc else 0, authored_asm_function_credit=0)
    if isc:
        info = c.function_info(u['symbol'])
        result.update(emitted_procedure={k: v for k, v in info.items() if k != 'fixups'},
                      emitted_procedure_object_role='genuine_C5_sidecar_not_game_SOURCE',
                      comparison_object_sha256=H(b.c5_sidecar_bytes),
                      compiler_tool_hashes=b.provenance['tool_hashes'],
                      toolchain_manifest_sha256=b.provenance['compiler_manifest_SHA256'])
    else:
        sites = [s for s in proof['native_MZ'] if start <= s < start + u['size']]
        result.update(complete_code_allocation={'whole_object_CODE_bytes': 3902,
                                               'owner_offset': off, 'owner_bytes': u['size']},
                      complete_allocation_proof={'whole_bytes_equal': True,
                                                 'whole_original_mz_sites': sites,
                                                 'emitted_mz_sites': sites, 'relocations': relocations})
    if output is not None:
        output = Path(output)
        obj = output / 'mixed-source/evaluation3902.obj'
        side = output / 'typed-sidecars/evaluation3902'
        artifacts = [(obj, b.object_bytes), (side / 'C5.obj', b.c5_sidecar_bytes),
                     (side / 'compiler-FA.asm', b.fresh_fa_bytes),
                     (side / 'composed.asm', b.mixed_source_bytes),
                     (side / 'generation-receipt.json', (json.dumps(b.provenance, indent=2) + '\n').encode())]
        for path, content in artifacts:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                need(path.read_bytes() == content, 'changed current-run artifact')
            else:
                path.write_bytes(content)
        result['object_artifact'] = str(obj.resolve())
        if isc:
            result['comparison_object_artifact'] = str((side / 'C5.obj').resolve())
    return result

OWNERS_SHA256='7c2ad9bfc32a325ee62c70f97a1ddf91d6215595b53776fff9f903320d1b5075'

BACKEND=generation.BACKEND
def validate_evidence(u,project,target_sha256,reference):
 from reference import ORIGINAL_SHA256,CARRIER_SHA256
 validate_unit(u)
 need(target_sha256==ORIGINAL_SHA256 and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'original/carrier identity')
 path=Path(project)/u['rea_evidence'];raw=path.read_bytes()
 need(not path.is_symlink()and H(raw)==REA_PINS[u['rea_evidence']],'exact retained REA evidence')
 e=json.loads(raw);p=e['analysis_profile']['parameters'];r=e['normalized_result']['procedure'];body=r['body'];start=0x10000+int(u['image_offset'],0)
 need(e['operation']=='analyze_function'and e['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode','native REA analysis context')
 if u.get('extended_extent'):
  original=next(v for v in comparison.profile()['canonical_C']if v['id']==u['id'])
  need(u['extended_extent']==original['extended_extent']and int(r['address'],0)==start,'retained original extended extent; full proof checked on fresh C5 sidecar')
 else:
  need(int(r['address'],0)==start and body['available']and not body['non_contiguous']and body['ranges']==[{'start':hex(start),'end':hex(start+u['size']-1)}]and body['total_bytes']==body['span_bytes']==u['size'],'complete native procedure')
 return e['evidence_id']
def validate_unit(u):
 contracts=owners();need(u.get('id')in contracts and u==contracts[u['id']],'exact graphics owner contract')

REA_PINS={'evidence/rea_evaluate_abs_far.json': '51613c90cacc1b51464b0b44e9f33fd430c32eeaf6e4c501e73087bc3df0e79f', 'evidence/rea_evaluation_parity_far.json': '62e62fdc9d4e1189a50911c9839c20fce6547de66b04bf72f51db0dc9f22971a', 'evidence/rea_evaluate_piece_value.json': '1b656dd30920c4541db96ef6e3f66319a43668271b2d715cbee9f8940be6a55a', 'evidence/rea_evaluation_max_far.json': '0e7f9d4c55282aa268c248d60d01d4e3a0ae911f08fa47c74c3ca1c8f9647539', 'evidence/rea_evaluation_min_far.json': '5f5527935f0866dc9c7fc65d6251d3649cb612f58c12dcd97dff5d0fba60ae27', 'evidence/rea_evaluate_pawn_score.json': '8fe93b94ec50ef645fc661c3ad33f39be0552becc663c6b952da8556565e28f8', 'evidence/rea_full_evaluation_fe59.json': '79b6546c42242a8d0c1be9b232c735fbab0192d5cfb3fd04622010d54ef5fa37', 'evidence/rea_evaluate_pawn_file.json': 'd5abad14c0b9a676a0ba096099d16f9fe9c00bca2c033a5a7fe79748cd58e2cf', 'evidence/rea_evaluate_pawn_adjust.json': '932be34bbf6046ea13978677b2f9a52ff70325e1220838cf30b3fe9bd7b65247', 'evidence/rea_moves_af87_far_callee.json': '14dba46fc4898e492d80218052f4ef99200c70000e132096ca2d84b3e9bc4f36', 'evidence/rea_evaluate_pawn_bit_count.json': 'a0e3383fe8ac13ece37d81d1f16648148cb0f83eafd04439a24db55773c59c56'}
