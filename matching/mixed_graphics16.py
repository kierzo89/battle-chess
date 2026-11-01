"""Isolated ordinary owner adapter; fresh generation capability stays in-process."""
from pathlib import Path
from dataclasses import dataclass
import copy
import hashlib
import json
import mixed_graphics_generation16 as generation
import mixed_graphics_compare16 as comparison
from mixed_graphics_source16 import SOURCES, C_SOURCE_SHA256
from omf import read_omf
from link16 import link_function

D = Path(__file__).resolve().parent
H = lambda b: hashlib.sha256(b).hexdigest()
_CAP = object()

def need(v, m):
    if not v:
        raise ValueError(m)

def owners():
    raw = Path(__file__).with_name('mixed_graphics_units.json').read_bytes()
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
    paths = [D / n for n in ('mixed_graphics16.py', 'mixed_graphics_generation16.py',
                            'mixed_graphics_source16.py', 'mixed_graphics_compare16.py',
                            'mixed_graphics_profile.json', 'mixed_graphics_units.json')]
    paths += [Path(__file__), Path(comparison.__file__), Path(__file__).with_name('mixed_graphics_units.json')]
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
        code, proof = comparison.compare(b, reference)
        cache[key] = _FreshEntry(_CAP, id(cache), b, signature(b), code, proof)
    e = cache[key]
    need(type(e) is _FreshEntry and e.cap is _CAP and e.cache_id == id(cache),
         'same current-run factory cache; retained fixtures are not fresh')
    need(e.signature == signature(e.built), 'cached actual build mutated')
    b = e.built
    start = int(u['image_offset'], 0); off = start - 0x3b2e
    actual = e.code[off:off + u['size']]
    need(len(actual) == u['size'] and actual == image[start:start + u['size']], 'whole owner bytes')
    isc = u['language'] == 'c'
    proof = copy.deepcopy(e.proof)
    proof.update(whole_native_equal=True, C5_sidecar_not_SOURCE=True)
    if isc:
        c = read_omf(b.c5_sidecar_bytes)
        body, relocations = link_function(c, u['symbol'], start, u['externals'], image_origin=start)
        need(body == actual, 'genuine C sidecar must equal final span')
    else:
        relocations = [dict(f, object_offset=f['raw']['offset'],
                            field_image_offset=0x3b2e + f['raw']['offset'],
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
                  mixed_object_proof=proof, mixed_profile='graphics7262_v1',
                  classification='compiler_produced_C_in_mixed_module' if isc else 'authored_ASM_in_mixed_module',
                  comparison_object_role='genuine_C5_typed_sidecar' if isc else 'final_mixed_span',
                  compiler='Microsoft C 5.00' if isc else None,
                  compiler_flags=['/AS', '/Zi'] if isc else [],
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
        result.update(complete_code_allocation={'whole_object_CODE_bytes': 7262,
                                               'owner_offset': off, 'owner_bytes': u['size']},
                      complete_allocation_proof={'whole_bytes_equal': True,
                                                 'whole_original_mz_sites': sites,
                                                 'emitted_mz_sites': sites, 'relocations': relocations})
    if output is not None:
        output = Path(output)
        obj = output / 'mixed-source/graphics7262.obj'
        side = output / 'typed-sidecars/graphics7262'
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

OWNERS_SHA256='1ad8301deddfdaf7c7031180f1c87c322e598990539218576bd0bbc7d37491d0'

BACKEND=generation.BACKEND
def validate_evidence(u,project,target_sha256,reference):
 from reference import ORIGINAL_SHA256,CARRIER_SHA256
 validate_unit(u)
 need(target_sha256==ORIGINAL_SHA256 and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'original/carrier identity')
 path=Path(project)/u['rea_evidence'];raw=path.read_bytes()
 need(not path.is_symlink()and H(raw)==REA_PINS[u['rea_evidence']],'exact retained REA evidence')
 e=json.loads(raw);p=e['analysis_profile']['parameters'];r=e['normalized_result']['procedure'];body=r['body'];start=0x10000+int(u['image_offset'],0)
 need(e['operation']=='analyze_function'and e['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode','native REA analysis context')
 need(int(r['address'],0)==start and body['available']and not body['non_contiguous']and body['ranges']==[{'start':hex(start),'end':hex(start+u['size']-1)}]and body['total_bytes']==body['span_bytes']==u['size'],'complete native procedure')
 return e['evidence_id']
def validate_unit(u):
 contracts=owners();need(u.get('id')in contracts and u==contracts[u['id']],'exact graphics owner contract')

REA_PINS={'evidence/rea_empty_3b2e.json': 'c0d6d0824166af531da51d19c88af19e96cf627674dbf6d584c84f1f2a056628', 'evidence/rea_animation_task_driver_3b3a.json': 'dbc61489eff3884eafde1ad6b286893c8cb236e53e8ecbbf7dc62472368e4424', 'evidence/rea_actor_reset_3e4f.json': 'd5d13d121a4f09b917f889b012c836f1fc340d35aab6960f98813c7cbc46ffcd', 'evidence/rea_actor_next_3e81.json': 'ee7d69449609aff30fe4424bf4f11a3c46e792e9c82a9d7ab667722146cb0405', 'evidence/rea_insert_actor_3eb1.json': 'adb0ee022b3dabaf60779bb79015bb37f18f60babab5fa86cb5a3ad4f715c08d', 'evidence/rea_attach_actor_3f0f.json': 'a26e53967308cb63fc43156c0d1c065a7ba036990c7777fb9abc25dcd0a5cc2a', 'evidence/rea_detach_actor_3f49.json': 'b14d271dc7f24246fd61085c4fdd3e038cec58a4cf4c7fc97db05f7252dbdd14', 'evidence/rea_detach_all_3f7f.json': '85d17e1026a574e0af696e127c2ff5ae0d627df538f180086a959afbd43c1b5e', 'evidence/rea_actor_next_3f9e.json': '49ad97c44c6debf3d8ce273137e46362ba962e3743bdb0edbda13427e0bed551', 'evidence/rea_graphics_41a8.json': '88651f91cee4031fb555b54d5f22ba6be4d33b633526b4987ff99999a0aacd1c', 'evidence/rea_frame_context_render42a0.json': '80ecad229e13b5840078176de59470b19aeec18e60c11e54a2fd81863c279601', 'evidence/rea_prepare_color_4575.json': '753c2aaeabc4c5d70b2844692fe186f678a954157da1d465cbb6dd4e8fecf7ee', 'evidence/rea_frame_present_45a2.json': 'f1684458ec9d519cdf1c39c7654a65b81ae92115b778779942572986bc22ddf1', 'evidence/rea_graphics_next_466b.json': 'a9c370d6c26d923526f1d8fa9834b7d49bc2fe2e7ebfc59c5f4ca571b024fdbc', 'evidence/rea_menu_next_4c74.json': 'f72e0b94790f1a8f091c61ca711fe1bb1c24ed82f733dfbdadba23dd2b21f475', 'evidence/rea_menu_next_4e5d.json': '06eae1b987507622e8cf67d6e56a61ed53f513dd5a9bd1c9e02008734ccaba38', 'evidence/rea_menu_next_5035.json': 'bccd6eccd0beb6fa2a67b3471fbfd281b1b591fb40893af6637adfb079c93c82', 'evidence/rea_menu_next_50af.json': 'a43eda3be5b3884f022f0bf6f8caf2bd22ff48002cf50cfc95314b442a1e5c32', 'evidence/rea_menu_next_512d.json': 'd2c6ca48399c99ee2e35136cc9698e0f686338070683162f22cc9bc8cda205b5', 'evidence/rea_menu_row_527e.json': 'f91c3bc993a48cb06fd235e321a771c6309c26fabbdea64913ee88458e097372', 'evidence/rea_menu_advance_5381.json': '0d9416c913a6f55defa993744d1a283cf78f68cca5e09740b278f5d8ccdc46ea', 'evidence/rea_menu_driver_543a.json': 'cd7ba4fde7b60ef3cc665e4390a233e4c58f02ae163d4c9137eaa7a52d0f3dca'}
