"""Strict separate MZ accounting for successful complete authored C DATA.

No compiler generation, matching-byte credit or C-procedure/ASM policy lives
here. Nonempty DATA MZ claims are reauthenticated against the actual output
object/source and the only reviewed FAR16 DATA decoder before inclusion.
"""
from pathlib import Path
import hashlib
import json
import screen_far_pointer_data16 as far
from reference import validate_expanded_read, validate_data_address


def require(test,message):
    if not test:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def canonical(value):return json.dumps(value,sort_keys=True)


def collect_source_data_mz(results,project,reference,original_sites):
    """Return DATA-only sorted unique sites, with whole-unit/native checks.

    Failed/non-C-DATA rows are never read as providers. All matched DATA,
    including relocation-free and existing near pointers, must cover exactly
    the original MZ set within their complete extent. Duplicate IDs/sites or
    malformed fields fail closed. Nonempty claims require actual fresh-build
    source/object provenance and exact independently re-decoded fixup logs.
    """
    project=Path(project).resolve();native=list(original_sites)
    require(isinstance(reference,dict),'C DATA MZ reference required')
    require(all(type(s)is int and s>=0 for s in native)and len(native)==len(set(native))
            and set(native)==set(reference.get('relocations',())), 'C DATA original relocation identity changed')
    native=set(native);ids=set();sites=set();units=[]
    for row in results:
        if row.get('status')!='c_data_matched':continue
        require(row.get('language')=='c-data','Matched C DATA status/language mismatch')
        name=row.get('id');require(isinstance(name,str)and name and name not in ids,'Duplicate/invalid matched C DATA ID');ids.add(name)
        try:start=int(row['image_offset'],0)
        except (KeyError,TypeError,ValueError)as ex:raise ValueError('C DATA complete image extent required')from ex
        size=row.get('size');require(type(size)is int and size>0 and 0<=start<start+size<=len(reference.get('image',b'')),'C DATA invalid complete image extent')
        expected={s for s in native if s<start+size and start<s+2}
        require(all(start<=s and s+2<=start+size for s in expected),'C DATA original MZ crosses complete extent')
        records=row.get('relocations',[]);require(isinstance(records,list),'C DATA actual relocation records required')
        emitted=[]
        for record in records:
            require(isinstance(record,dict),'C DATA malformed relocation record')
            if 'mz_segment_relocation_image_offset'not in record:continue
            site=record['mz_segment_relocation_image_offset']
            require(type(site)is int and start<=site and site+2<=start+size and site in native,'C DATA emitted MZ is outside original whole unit')
            require(site not in emitted,'C DATA duplicate emitted MZ field');emitted.append(site)
        require(set(emitted)==expected,'C DATA MZ set differs from complete original extent')
        require(not sites.intersection(emitted),'C DATA duplicate MZ ownership across matched units')
        artifact_proof=None
        if emitted:
            require(row.get('backend')==far.BACKEND,'C DATA nonempty MZ requires reviewed explicit FAR16 backend')
            require(row.get('object_profile')==far.PROFILE and row.get('flags')==far.FLAGS
                    and row.get('compiler')=='Microsoft C 5.00','C DATA MZ closed source/compiler profile changed')
            source=(project/row['source']).resolve();require(source.is_relative_to(project),'C DATA MZ source escapes project')
            source_bytes=source.read_bytes();source_sha=sha(source_bytes)
            require(source_sha==row.get('source_sha256')and source_sha==far.SOURCE_SHA256,'C DATA MZ source identity changed')
            require(row.get('compiler_flags')==far.FLAGS and row.get('compiler_tool_hashes')==far.TOOL_HASHES
                    and row.get('toolchain_manifest_sha256')==far.MANIFEST_SHA256,'C DATA MZ actual compiler provenance changed')
            artifact=row.get('object_artifact');require(isinstance(artifact,str)and Path(artifact).is_absolute(),'C DATA MZ actual output object path required')
            raw=Path(artifact).read_bytes();require(sha(raw)==row.get('object_sha256'),'C DATA MZ actual object fingerprint changed')
            address=row.get('data_address');require(isinstance(address,dict)and set(address)=={'segment','offset'},'C DATA MZ explicit DATA placement required')
            validate_data_address(row,reference)
            linked,meta=far.link_data(raw,row['symbol'],start,address['segment'],row['externals'])
            require(canonical(records)==canonical(meta['relocations']),'C DATA MZ actual decoded relocation records differ')
            info=dict(meta);info.pop('relocations')
            require(canonical(row.get('emitted_data_segment'))==canonical(info),'C DATA MZ complete emitted DATA metadata differs')
            evidence=json.loads((project/row['rea_evidence']).read_text())
            validate_expanded_read(evidence,row,linked,reference,emitted_mz_sites=meta['emitted_mz_sites'])
            artifact_proof={'source':row['source'],'source_sha256':source_sha,'object_artifact':artifact,
                'object_sha256':sha(raw),'whole_DATA_sha256':sha(linked),'raw_field_count':len(meta['all_raw_fixups']),
                'image_MZ_count':len(emitted),'actual_relocations':records}
        units.append({'unit':name,'image_offset':start,'size':size,'sites':sorted(emitted),'actual_artifact_proof':artifact_proof})
        sites.update(emitted)
    return {'sites':sorted(sites),'matched_DATA_units':units,'class':'authored_C_DATA_MZ','byte_credit':0,'function_credit':0}
