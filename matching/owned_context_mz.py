"""Account authenticated compiler-owned selector MZ sites; no byte credit.

This is deliberately not a generic proof-dictionary collector. Only matched
closed selector owners are accepted, and the actual output object, source hash,
complete native context and selector evidence are revalidated by the existing
selector checker before a site enters aggregate coverage.
"""
import hashlib
import json
from pathlib import Path
from omf import read_omf
import owned_selector_const16 as selector


def collect_owned_context_mz(results, project, reference, original_sites):
    """Return sorted unique sites and provenance from exact matched owners.

    Five procedure owners can reference the same complete object/CONST. Their
    verified context is counted once; duplicate unit IDs, conflicting context
    claims and malformed/foreign proofs fail closed. Failed procedures never
    contribute, even if an earlier ownership check produced a proof.
    """
    project = Path(project).resolve()
    if not isinstance(reference, dict):
        raise ValueError('Owned-context accounting requires native reference')
    native = list(original_sites)
    if (any(type(s) is not int or s < 0 for s in native)
            or len(native) != len(set(native))
            or set(native) != set(reference.get('relocations', ()))):
        raise ValueError('Owned-context original relocation identity changed')
    sites, identities, unit_ids, contexts = set(), {}, set(), []
    for result in results:
        if result.get('status') != 'c_matched':
            continue
        descriptor = result.get('owned_selector_const')
        proof = result.get('owned_selector_const_proof')
        if descriptor is None and proof is None:
            continue
        if descriptor is None or not isinstance(proof, dict):
            raise ValueError('Matched owner requires authenticated selector metadata/proof')
        selector.validate_unit_metadata(result)
        unit_id = result.get('id')
        if not isinstance(unit_id, str) or not unit_id or unit_id in unit_ids:
            raise ValueError('Duplicate or invalid matched selector owner ID')
        unit_ids.add(unit_id)
        source = (project/result['source']).resolve()
        if not source.is_relative_to(project):
            raise ValueError('Owned-context source escapes project')
        source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        if source_sha != result.get('source_sha256'):
            raise ValueError('Owned-context source fingerprint changed')
        artifact = result.get('object_artifact')
        if not isinstance(artifact, str) or not Path(artifact).is_absolute():
            raise ValueError('Owned-context requires actual output object artifact')
        raw = Path(artifact).read_bytes()
        object_sha = hashlib.sha256(raw).hexdigest()
        if object_sha != result.get('object_sha256'):
            raise ValueError('Owned-context object fingerprint changed')
        _, _, authenticated = selector.validate(result, read_omf(raw), project, reference)
        # Report JSON represents OMF tuples as arrays; compare canonical JSON.
        authenticated = json.loads(json.dumps(authenticated))
        if json.loads(json.dumps(proof)) != authenticated:
            raise ValueError('Owned-context reported proof differs from native/object validation')
        owned = authenticated['complete_MZ_sites']
        if (not isinstance(owned, list) or not owned
                or any(type(s) is not int for s in owned)
                or len(owned) != len(set(owned))):
            raise ValueError('Owned-context malformed or duplicated native sites')
        start = int(descriptor['image_offset'], 0)
        mixed78 = descriptor.get('kind') == 'shared_turn_book_literals78_v1'
        if mixed78 and (descriptor.get('size') != 78 or type(descriptor.get('size')) is not int
                or authenticated.get('complete_CONST_bytes') != 78 or type(authenticated.get('complete_CONST_bytes')) is not int
                or authenticated.get('authored_c_function_credit') != 0 or type(authenticated.get('authored_c_function_credit')) is not int
                or authenticated.get('source_data_credit') != 0 or type(authenticated.get('source_data_credit')) is not int):
            raise ValueError('Mixed selector/literal context requires exact full78 and zero context credits')
        if (owned != [start] or (descriptor['size'] != 78 if mixed78 else descriptor['size'] != 2)
                or not set(owned) <= set(native)
                or any(s + 2 > start + descriptor['size'] for s in owned)):
            raise ValueError('Owned-context sites escape exact native selector extent')
        identity = (source_sha, object_sha, authenticated)
        key = tuple(owned)
        if key in identities:
            if identities[key] != identity:
                raise ValueError('Conflicting owners claim one native context')
        else:
            if sites.intersection(owned):
                raise ValueError('Overlapping owned native contexts')
            identities[key] = identity
            contexts.append({'sites': owned, 'source_sha256': source_sha,
                             'object_sha256': object_sha,
                             'profile': descriptor['kind'],
                             'selector_primary_id': authenticated['selector_primary_id'],
                             'code_primary_id': authenticated['code_primary_id']})
        sites.update(owned)
    return {'sites': sorted(sites), 'contexts': contexts,
            'matched_owner_units': sorted(unit_ids), 'byte_credit': 0,
            'function_credit': 0}
