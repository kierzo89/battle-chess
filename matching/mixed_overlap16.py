"""Isolated ordinary owner adapter; fresh generation capability stays in-process."""
from pathlib import Path
from dataclasses import dataclass
import copy
import hashlib
import json
import mixed_overlap_generation16 as generation
import mixed_overlap_compare16 as comparison
from mixed_overlap_source16 import RECIPES
from omf import read_omf
from link16 import link_function

D = Path(__file__).resolve().parent
H = lambda b: hashlib.sha256(b).hexdigest()
_CAP = object()

def need(v, m):
    if not v:
        raise ValueError(m)

def owners():
    raw = Path(__file__).with_name('mixed_overlap_units.json').read_bytes()
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

def cache_key(project, reference, kind):
    project=Path(project);r=comparison.profile(kind)['recipe']
    paths=[Path(__file__).with_name(n) for n in ['mixed_overlap16.py','mixed_overlap_source16.py','mixed_overlap_generation16.py','mixed_overlap_compare16.py','mixed_overlap_profile.json','mixed_overlap_units.json']]
    paths += [project/r['C_SOURCE'],project/r['ASM_SOURCE'],Path('/usr/bin/dosbox').resolve(),project/'config/msc500.json',project/'config/msc510.json',project/'toolchains/msc500/manifest.json',project/'toolchains/msc510/manifest.json',project/'toolchains/msc510/LICENSE',project/'toolchains/msc510/MASM.EXE']
    paths += [project/'toolchains/msc500'/row['name'] for row in json.loads((project/'config/msc500.json').read_text())['files']]
    return (generation.BACKEND,kind,tuple((str(p.resolve()),H(p.read_bytes())) for p in paths),H(reference['image']),tuple(reference['relocations']),reference['original_sha256'],reference['carrier_sha256'])

def assemble(source, project):
    return generation.assemble(source, project)

def build_unit(u, image, project, cache, output, reference):
    contracts = owners()
    need(u.get('id') in contracts and u == contracts[u['id']], 'exact owner required')
    need(type(cache) is dict and type(image) is bytes and (image == reference['image'] or (len(image) == 82903 and H(image) == '643f5e20f063f212f496a40ecac9b3242c4fdede18c865fc26ce0be1f37862dc')), 'current cache and exact original MZ or expanded reference image required')
    kind=u['mixed_profile'].replace('_overlap_v1','');profile=comparison.profile(kind);recipe=profile['recipe']
    key = cache_key(project, reference, kind)
    if key not in cache:
        b = assemble(Path(project) / recipe['C_SOURCE'], project)
        code, proof = comparison.compare(b, kind, reference, project)
        cache[key] = _FreshEntry(_CAP, id(cache), b, signature(b), code, proof)
    e = cache[key]
    need(type(e) is _FreshEntry and e.cap is _CAP and e.cache_id == id(cache),
         'same current-run factory cache; retained fixtures are not fresh')
    need(e.signature == signature(e.built), 'cached actual build mutated')
    b = e.built
    start = int(u['image_offset'], 0); off = start - profile['origin']
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
        relocations = [dict(f, field_image_offset=profile['origin']+f['object_offset'], unit_offset=f['object_offset']-off) for f in proof['all_fields'] if off <= f['object_offset'] < off+u['size']]
        for field in relocations:
            kind_of_field=field['location_type']
            need(kind_of_field in (1,2,3) and field['width']=={1:2,2:2,3:4}[kind_of_field], 'known complete typed field')
            need(field['field_image_offset']+field['width']<=start+u['size'], 'whole field inside owner extent')
            if kind_of_field in (2,3):
                site=field['field_image_offset']+(2 if kind_of_field==3 else 0)
                need(site in proof['native_MZ'], 'typed emitted segment word independently equals native MZ site')
                field['mz_segment_relocation_image_offset']=site
        need(sorted(f['mz_segment_relocation_image_offset'] for f in relocations if 'mz_segment_relocation_image_offset' in f)==[s for s in proof['native_MZ'] if start<=s<start+u['size']], 'complete emitted owner MZ census')
    result = dict(u, status='c_matched' if isc else 'asm_code_matched',
                  expected_size=len(actual), actual_size=len(actual),
                  expected_sha256=H(actual), actual_sha256=H(actual),
                  first_difference=None, expected_byte=None, actual_byte=None,
                  object_sha256=H(b.object_bytes), relocations=relocations,
                  mixed_object_proof=proof, mixed_profile=kind+'_overlap_v1',
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
        result.update(complete_code_allocation={'whole_object_CODE_bytes': profile['size'],
                                               'owner_offset': off, 'owner_bytes': u['size']},
                      complete_allocation_proof={'whole_bytes_equal': True,
                                                 'whole_original_mz_sites': sites,
                                                 'emitted_mz_sites': sites, 'relocations': relocations})
    if output is not None:
        output = Path(output)
        obj = output / ('mixed-source/'+kind+'-overlap.obj')
        side = output / ('typed-sidecars/'+kind+'-overlap')
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

OWNERS_SHA256='b6b465e240f0609fb1b59073f3397b24dd544354676398ae55318cc414327a5d'
BACKEND=generation.BACKEND
def validate_unit(u):
 contracts=owners();need(u.get('id')in contracts and u==contracts[u['id']],'exact closed mixed460 owner contract')
def validate_evidence(u,project,target_sha256,reference):
 import check
 validate_unit(u)
 need(u['language']=='asm-code','C retains generic evidence gate')
 kind=u['mixed_profile'].replace('_overlap_v1','');original=next(x for x in comparison.profile(kind)['original_units'] if x['id']==u['id'])
 return check.validate_rea_extent(original,project,target_sha256,reference)
