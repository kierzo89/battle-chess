"""Isolated ordinary owner adapter; fresh generation capability stays in-process."""
from pathlib import Path
from dataclasses import dataclass
import copy
import hashlib
import json
import mixed_remove460_generation16 as generation
import mixed_remove460_compare16 as comparison
from mixed_remove460_source16 import C_SOURCE_SHA256
from omf import read_omf
from link16 import link_function

D = Path(__file__).resolve().parent
H = lambda b: hashlib.sha256(b).hexdigest()
_CAP = object()

def need(v, m):
    if not v:
        raise ValueError(m)

def owners():
    raw = Path(__file__).with_name('mixed_remove460_units.json').read_bytes()
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
    paths = [D / n for n in ('mixed_remove46016.py', 'mixed_remove460_generation16.py',
                            'mixed_remove460_source16.py', 'mixed_remove460_compare16.py',
                            'mixed_remove460_profile.json', 'mixed_remove460_units.json')]
    paths += [Path(__file__), Path(comparison.__file__), Path(__file__).with_name('mixed_remove460_units.json')]
    paths += [D / generation.ASM_SOURCE]
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
    start = int(u['image_offset'], 0); off = start - 0x5934
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
        relocations = [dict(f, field_image_offset=0x5934+f['object_offset'], unit_offset=f['object_offset']-off) for f in proof['all_fields'] if off <= f['object_offset'] < off+u['size']]
        need(not [x for x in proof['native_MZ'] if start <= x < start+u['size']], 'authored prefix has no native loader fixups')
    result = dict(u, status='c_matched' if isc else 'asm_code_matched',
                  expected_size=len(actual), actual_size=len(actual),
                  expected_sha256=H(actual), actual_sha256=H(actual),
                  first_difference=None, expected_byte=None, actual_byte=None,
                  object_sha256=H(b.object_bytes), relocations=relocations,
                  mixed_object_proof=proof, mixed_profile='remove460_v1',
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
        result.update(complete_code_allocation={'whole_object_CODE_bytes': 460,
                                               'owner_offset': off, 'owner_bytes': u['size']},
                      complete_allocation_proof={'whole_bytes_equal': True,
                                                 'whole_original_mz_sites': sites,
                                                 'emitted_mz_sites': sites, 'relocations': relocations})
    if output is not None:
        output = Path(output)
        obj = output / 'mixed-source/remove460.obj'
        side = output / 'typed-sidecars/remove460'
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

OWNERS_SHA256='aa92b1049c6917d5c3133d0dcc06255ab1f3b13f941560d3fae31d27385d5d22'
BACKEND=generation.BACKEND
def validate_unit(u):
 contracts=owners();need(u.get('id')in contracts and u==contracts[u['id']],'exact closed mixed460 owner contract')
def validate_evidence(u,project,target_sha256,reference):
 import remove_actor_code16
 validate_unit(u)
 need(u['language']=='asm-code','C uses unchanged generic native extent evidence gate')
 return remove_actor_code16.validate_evidence(comparison.profile()['original_units'][0],project,target_sha256,reference)
