"""Closed genuine nine-procedure/literal-pool ownership; comparison only.

No generator input is obtained from the target. Whole OMF identity and parsed
record congruence authenticate the narrowly reviewed compiler contribution.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from omf import OMFError, OMFObject, read_omf
from link16 import link_function
from reference import validate_data_address, validate_expanded_read

class OwnedLiteralConstError(OMFError):
    pass

PROFILE = 'asset_messages_1036_v1'
PROFILE_SHA256 = '87836432d57ffd49d3495066216fce3189d46fadde6298b3e7d834812c1b04de'

def _sha(b): return hashlib.sha256(b).hexdigest()
def _fail(message): raise OwnedLiteralConstError(message)
def _profile():
    raw = Path(__file__).with_name('asset_literal_const_profile.json').read_bytes()
    if _sha(raw) != PROFILE_SHA256: _fail('Literal ownership profile pin mismatch')
    return json.loads(raw)

def validate_unit_metadata(unit):
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='history_input_literal17_340_v1':
        from history_input_literal_const16 import validate_unit_metadata as history_validate
        return history_validate(unit)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='asset_drive_messages_1036_158_v2':
        from owned_asset_drive_literal_const16 import validate_unit_metadata as asset_drive_validate
        return asset_drive_validate(unit)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_ready9856_sidecounts_1554_v2':
        from owned_editor_side_counts_literal_const16 import validate_unit_metadata as side_counts_validate_unit_metadata
        return side_counts_validate_unit_metadata(unit)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_ready9856_1554_v1':
        from owned_editor_ready9856_literal_const16 import validate_unit_metadata as ready9856_validate_unit_metadata
        return ready9856_validate_unit_metadata(unit)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_turn_phase_1554_v1':
        from owned_editor_turn_phase_literal_const16 import validate_unit_metadata as turn_phase_validate_unit_metadata
        return turn_phase_validate_unit_metadata(unit)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_1554_v1':
        from owned_editor_state_literal_const16 import validate_unit_metadata as editor_state_validate_unit_metadata
        return editor_state_validate_unit_metadata(unit)
    if isinstance(unit, dict) and unit.get('owned_const_profile') == 'arena_messages_1244_v1':
        from owned_arena_literal_const16 import validate_unit_metadata as arena_validate_unit_metadata
        return arena_validate_unit_metadata(unit)
    p = _profile()
    if not isinstance(unit, dict) or unit.get('owned_const_profile') != PROFILE:
        _fail('Unknown literal CONST ownership profile')
    expected = next((u for u in p['units'] if u['symbol'] == unit.get('symbol')), None)
    if expected is None or expected.get('owned_const_profile') != PROFILE:
        _fail('Literal CONST profile requires an actual referencing owner')
    for key in ('language','backend','symbol','size','image_offset','flags','externals','owned_const'):
        if json.dumps(unit.get(key), sort_keys=True) != json.dumps(expected[key], sort_keys=True): _fail('Literal owner metadata mismatch: '+key)
    if any(unit.get(k) is not None for k in ('code_address','extended_extent','owned_data','owned_bss','owned_selector_const')):
        _fail('Literal owner forbids other placement/ownership profiles')
    return dict(p['descriptor'])

def validate_layout(unit, obj):
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='history_input_literal17_340_v1':
        from history_input_literal_const16 import validate_layout as history_validate
        return history_validate(unit,obj)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='asset_drive_messages_1036_158_v2':
        from owned_asset_drive_literal_const16 import validate_layout as asset_drive_validate
        return asset_drive_validate(unit,obj)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_ready9856_sidecounts_1554_v2':
        from owned_editor_side_counts_literal_const16 import validate_layout as side_counts_validate_layout
        return side_counts_validate_layout(unit,obj)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_ready9856_1554_v1':
        from owned_editor_ready9856_literal_const16 import validate_layout as ready9856_validate_layout
        return ready9856_validate_layout(unit,obj)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_turn_phase_1554_v1':
        from owned_editor_turn_phase_literal_const16 import validate_layout as turn_phase_validate_layout
        return turn_phase_validate_layout(unit,obj)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_1554_v1':
        from owned_editor_state_literal_const16 import validate_layout as editor_state_validate_layout
        return editor_state_validate_layout(unit,obj)
    """Pure allocation/record/field validation, without target reads."""
    if isinstance(unit, dict) and unit.get('owned_const_profile') == 'arena_messages_1244_v1':
        from owned_arena_literal_const16 import validate_layout as arena_validate_layout
        return arena_validate_layout(unit, obj)
    desc = validate_unit_metadata(unit); p = _profile()
    if not isinstance(obj, OMFObject): _fail('Strict OMF object required')
    # Reconstitute checksum-validated record identity for authentication only.
    # These bytes are NEVER supplied to compiler, linker or output generation.
    raw = bytearray()
    for kind, offset, payload in obj.records:
        if offset != len(raw): _fail('OMF record offsets are not complete/contiguous')
        record = bytes([kind]) + (len(payload)+1).to_bytes(2,'little') + payload
        raw.extend(record + bytes([(-sum(record)) & 255]))
    if _sha(raw) != p['object_sha256'] or read_omf(bytes(raw)) != obj:
        _fail('Whole genuine OMF identity or parsed-record congruence mismatch')
    expected_segments = [(1,'_TEXT','CODE',1036,72),(2,'_DATA','DATA',0,72),
        (3,'CONST','CONST',112,72),(4,'_BSS','BSS',0,72),
        (5,'$$SYMBOLS','DEBSYM',874,32),(6,'$$TYPES','DEBTYP',562,32)]
    if [(s.index,s.name,s.class_name,s.length,s.attributes) for s in obj.segments.values()] != expected_segments:
        _fail('Literal contribution has foreign/missing allocation')
    if len(obj.fixups)!=124 or len([f for f in obj.fixups if f.segment==1])!=89:
        _fail('Literal contribution field count mismatch')
    cv = sorted((obj.function_info(u['symbol']) for u in p['units']),key=lambda i:i['offset'])
    position=0
    for i in cv:
        expected=next(v for v in p['CV'] if v['symbol']==i['symbol'])
        if any(i[k]!=expected[k] for k in ('symbol','segment','offset','end','size','boundary')) or i['offset']!=position:
            _fail('Literal CODE requires complete contiguous nine CV extents')
        position=i['end']
    if position!=1036 or len(obj.publics)!=9: _fail('Literal CODE/anonymous pool public boundary mismatch')
    fields=[]
    for f in obj.fixups:
        if f.target!=(0,3): continue
        if (f.segment,f.width,f.location_type,f.segment_relative,f.frame,f.displacement)!=(1,2,1,True,(1,1),None):
            _fail('Literal field is not genuine own CONST OFFSET16')
        code=b''.join(chunk for _,chunk in sorted(obj.segments[1].chunks))
        fields.append((f.offset,int.from_bytes(code[f.offset:f.offset+2],'little')))
    fields.sort()
    if fields!=[(582,0),(602,9),(681,18),(733,42),(752,69),(839,98)]:
        _fail('Literal pool consumed offset/owner set mismatch')
    data=b''.join(chunk for _,chunk in obj.segments[3].chunks)
    if len(data)!=112 or obj.segments[3].chunks!=[(0,data)]: _fail('Literal allocation has holes/tail/overlap')
    return desc,data,fields

def validate(unit,obj,project,reference):
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='history_input_literal17_340_v1':
        from history_input_literal_const16 import validate as history_validate
        return history_validate(unit,obj,project,reference)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='asset_drive_messages_1036_158_v2':
        from owned_asset_drive_literal_const16 import validate as asset_drive_validate
        return asset_drive_validate(unit,obj,project,reference)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_ready9856_sidecounts_1554_v2':
        from owned_editor_side_counts_literal_const16 import validate as side_counts_validate
        return side_counts_validate(unit,obj,project,reference)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_ready9856_1554_v1':
        from owned_editor_ready9856_literal_const16 import validate as ready9856_validate
        return ready9856_validate(unit,obj,project,reference)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_turn_phase_1554_v1':
        from owned_editor_turn_phase_literal_const16 import validate as turn_phase_validate
        return turn_phase_validate(unit,obj,project,reference)
    if isinstance(unit,dict) and unit.get('owned_const_profile')=='editor_state_messages_1554_v1':
        from owned_editor_state_literal_const16 import validate as editor_state_validate
        return editor_state_validate(unit,obj,project,reference)
    if isinstance(unit, dict) and unit.get('owned_const_profile') == 'arena_messages_1244_v1':
        from owned_arena_literal_const16 import validate as arena_validate
        return arena_validate(unit, obj, project, reference)
    desc,data,fields=validate_layout(unit,obj);p=_profile();project=Path(project).resolve()
    source=(project/unit['source']).resolve()
    if not source.is_relative_to(project) or _sha(source.read_bytes())!=p['source_sha256']:
        _fail('Literal owner genuine source identity mismatch')
    for path,digest in p['pins'].items():
        actual=(project/path).resolve()
        if not actual.is_relative_to(project) or _sha(actual.read_bytes())!=digest:
            _fail('Literal native/compiler/review pin mismatch: '+path)
    try:
        frame,offset=validate_data_address(dict(desc,reference_region='exepack-expanded'),reference)
        evidence=(project/desc['rea_evidence']).read_bytes()
        evidence_id=validate_expanded_read(json.loads(evidence),dict(desc,reference_region='exepack-expanded'),data,reference)
        code=bytearray();relocations=[];scopes=[]
        for row in sorted(p['units'],key=lambda u:int(u['image_offset'],0)):
            actual,logs=link_function(obj,row['symbol'],int(row['image_offset'],0),row['externals'],owned_const=desc if row.get('owned_const') else None)
            code.extend(actual)
            sites=[r['mz_segment_relocation_image_offset'] for r in logs if 'mz_segment_relocation_image_offset' in r]
            relocations.extend(sites)
            scopes.append({'symbol':row['symbol'],'size':len(actual),'fields':len(logs),'sha256':_sha(actual)})
        # Relocation log segment-word locations are retained by the standard linker.
        expected=reference['image'][0xc83a:0xcc46]
        native=sorted(s for s in reference['relocations'] if s<0xcc46 and 0xc83a<s+2)
        if bytes(code)!=expected or sorted(relocations)!=p['MZ'] or native!=p['MZ']:
            _fail('Whole CODE1036/native MZ mismatch')
        loads=[]
        for base in (0,1,0x1000,0xeeff):
            generated=bytearray(code);original=bytearray(expected)
            for at in native:
                i=at-0xc83a
                for buffer in (generated,original):buffer[i:i+2]=((int.from_bytes(buffer[i:i+2],'little')+base)&65535).to_bytes(2,'little')
            if generated!=original: _fail('Literal whole CODE forward loader comparison mismatch')
            loads.append(base)
    except (ValueError,KeyError,TypeError,OSError) as exc:
        raise OwnedLiteralConstError('Literal whole ownership/reference validation failed: '+str(exc)) from exc
    info=obj.function_info(unit['symbol'])
    return desc,data,{'classification':'complete_compiler_owned_CONST_uncredited_context',
        'profile':PROFILE,'source_data_credit':0,'authored_c_function_count':0,'descriptor':desc,
        'segment':{k:v for k,v in asdict(obj.segments[3]).items() if k!='chunks'},
        'group':{'index':1,'name':'DGROUP','segments':[3,4,2]},
        'data_writes':[{'offset':0,'size':112,'sha256':_sha(data)}],
        'owner':{k:v for k,v in info.items() if k!='fixups'},'size':112,'sha256':_sha(data),'bytes_hex':data.hex(),
        'code_references':[{'object_offset':a,'original_addend':v}for a,v in fields],
        'complete_MZ_sites':[],'whole_CODE_MZ_sites':native,'whole_CODE_scopes':scopes,
        'whole_CODE_size':1036,'whole_CODE_fields':89,'four_forward_load_bases':loads,
        'rea_evidence_id':evidence_id,'rea_evidence_sha256':_sha(evidence),
        'original_sha256':reference['original_sha256'],'carrier_sha256':reference['carrier_sha256'],
        'data_frame':frame,'data_offset':offset,'requires_enclosing_CONST_alignment_context':False,
        'standalone_source_link_layout_proved':False,'owner_CODE_SEGDEF_size':1036,
        'owner_CODE_bytes_outside_procedure':1036-info['size'],'omf_records_or_fields_modified':False}
