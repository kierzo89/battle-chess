"""Closed private-BSS ownership gate for the complete board-pointer C context.

This validates allocation metadata, never emits initialized zeros, links fields,
or credits BSS bytes. Historical private visibility/source ownership is unknown.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
try:
    from .omf import OMFError, OMFObject
    from .owned_data16 import groups_of, complete_bytes
    from .reference import ORIGINAL_SHA256, CARRIER_SHA256, IMAGE_SIZE
except ImportError:
    from omf import OMFError, OMFObject
    from owned_data16 import groups_of, complete_bytes
    from reference import ORIGINAL_SHA256, CARRIER_SHA256, IMAGE_SIZE


class OwnedBSSError(OMFError):
    pass


FIELD_ADDENDS = ((238,2),(244,0),(252,2),(258,0),(264,2),(299,2),
                 (305,0),(313,2),(319,0),(331,2),(360,0),(364,2),(368,2))
CODE_PROCEDURES = {'_show_error_0d6e':(0,31), '_error_message':(31,34),
                   '_board_pointer_0daf':(65,513)}


def selection_descriptor():
    return {'segment':4,'group':1,'size':4,'image_offset':'0x61eec',
        'data_address':{'segment':0x5cc2,'offset':0x52cc},
        'owner_symbol':'_board_pointer_0daf',
        'scalars':{'_selection_xor_52cc':{'offset':0,'size':2},
                   '_selection_colour_52ce':{'offset':2,'size':2}},
        'rea_evidence':'evidence/rea_crt_startup_500.json'}


def _same_descriptor(desc):
    # JSON comparison distinguishes bool from int and rejects additional keys.
    if not isinstance(desc,dict) or json.dumps(desc,sort_keys=True)!=json.dumps(selection_descriptor(),sort_keys=True):
        raise OwnedBSSError('exact complete private selection BSS descriptor required')


def _static_symbols(obj,desc):
    debug=obj.segments[5]
    if (debug.name,debug.class_name,debug.attributes)!=('$$SYMBOLS','DEBSYM',0x20):
        raise OwnedBSSError('real CodeView static-data metadata required')
    # The compiler backpatches debug procedure records; replay those writes.
    data=bytearray(debug.length)
    covered=set()
    for at,body in debug.chunks:
        if at<0 or at+len(body)>debug.length:
            raise OwnedBSSError('invalid debug record write')
        data[at:at+len(body)]=body;covered.update(range(at,at+len(body)))
    if len(covered)!=debug.length:
        raise OwnedBSSError('incomplete debug symbol segment')
    found={};at=0
    wanted={name[1:]:extent for name,extent in desc['scalars'].items()}
    while at<len(data):
        length=data[at]
        if not length or at+1+length>len(data):
            raise OwnedBSSError('invalid CodeView symbol record')
        kind=data[at+1];body=data[at+2:at+1+length]
        if kind==5 and len(body)>=7:
            namelen=body[6]
            if len(body)!=7+namelen:
                raise OwnedBSSError('invalid CodeView data name')
            name=bytes(body[7:]).decode('latin1')
            if name in wanted:
                if name in found:
                    raise OwnedBSSError('duplicate private scalar debug symbol')
                offset=int.from_bytes(body[0:2],'little')
                if (offset!=wanted[name]['offset'] or body[2:4]!=b'\0\0'
                        or int.from_bytes(body[4:6],'little')!=0x85):
                    raise OwnedBSSError('private scalar must be unsigned word at exact BSS offset')
                field=at+2
                fs=[f for f in obj.fixups if f.segment==5 and f.offset==field]
                if (len(fs)!=1 or fs[0].target!=(0,4) or fs[0].frame!=(1,1)
                        or fs[0].width!=4 or fs[0].location_type!=3
                        or not fs[0].segment_relative or fs[0].displacement not in(None,0)):
                    raise OwnedBSSError('static scalar debug field must retain own DGROUP/BSS fixup')
                found[name]={'offset':offset,'size':2,'CV_type_index':0x85,
                             'debug_field_offset':field,'raw_fixupp':fs[0].raw.hex()}
        at+=length+1
    if set(found)!=set(wanted):
        raise OwnedBSSError('both genuine private scalar debug records required')
    owned=[f for f in obj.fixups if f.segment==5 and f.target==(0,4)]
    if len(owned)!=2:
        raise OwnedBSSError('exactly two private scalar debug fields required')
    return found


def _validate_layout(obj,desc):
    _same_descriptor(desc)
    if not isinstance(obj,OMFObject):
        raise OwnedBSSError('strict-reader OMF object required')
    if any(t in(0xa2,0xa3,0xb0,0xb8)for t,_,_ in obj.records):
        raise OwnedBSSError('no iterated or COMMON allocation permitted')
    if set(obj.segments)!={1,2,3,4,5,6}:
        raise OwnedBSSError('exact CODE/DATA/CONST/BSS/debug segment set required')
    expected={1:('_TEXT','CODE',578,0x48),2:('_DATA','DATA',0,0x48),
              3:('CONST','CONST',0,0x48),4:('_BSS','BSS',4,0x48),
              5:('$$SYMBOLS','DEBSYM',None,0x20),6:('$$TYPES','DEBTYP',None,0x20)}
    for index,(name,cls,length,attrs) in expected.items():
        s=obj.segments[index]
        if ((s.name,s.class_name,s.attributes)!=(name,cls,attrs)
                or length is not None and s.length!=length or s.unsupported_data):
            raise OwnedBSSError('complete fixed source allocation shape required')
        if index in(2,3,4) and s.chunks:
            raise OwnedBSSError('private BSS and empty DATA/CONST must have zero LEDATA writes')
    code=complete_bytes(obj.segments[1])
    if set(obj.publics)!=set(CODE_PROCEDURES) or set(obj.procedures)!=set(CODE_PROCEDURES):
        raise OwnedBSSError('exact three independent CODE publics/CV records required')
    for name,(offset,size) in CODE_PROCEDURES.items():
        p=obj.publics[name];info=obj.function_info(name)
        if (p.segment!=1 or p.group!=0 or info['boundary']!='codeview3_procedure'
                or(info['offset'],info['size'])!=(offset,size)):
            raise OwnedBSSError('complete three-CV union must cover CODE578 without gaps/tails')
    if any(n in obj.externals.values()for n in desc['scalars']):
        raise OwnedBSSError('private scalars must not retain external aliases')
    groups=groups_of(obj)
    if groups!=[{'index':1,'name':'DGROUP','segments':[3,4,2]}]:
        raise OwnedBSSError('real unique DATA/CONST/BSS DGROUP required')
    debug=_static_symbols(obj,desc)
    fields=[];codefields=[f for f in obj.fixups if f.segment==1]
    if len(codefields)!=65:
        raise OwnedBSSError('all65 authentic whole-source CODE fields required')
    used=set()
    for f in obj.fixups:
        if f.segment in(2,3,4)or f.segment not in obj.segments:
            raise OwnedBSSError('fixup outside CODE/debug is forbidden')
        if f.segment!=1:continue
        span=set(range(f.offset,f.offset+f.width))
        if f.offset<0 or f.offset+f.width>578 or span&used:
            raise OwnedBSSError('overlapping/outside CODE field')
        used|=span
        owned=(f.target==(0,4)or f.frame==(1,1))
        if not owned:
            if f.target[0]!=2 or f.frame!=(5,None):
                raise OwnedBSSError('unexpected non-owner CODE field target/frame')
            continue
        if (f.target!=(0,4)or f.frame!=(1,1)or f.width!=2 or f.location_type!=1
                or not f.segment_relative or f.displacement not in(None,0)):
            raise OwnedBSSError('owned field requires original group-relative OFFSET16 shape')
        add=int.from_bytes(code[f.offset:f.offset+2],'little')
        fields.append(dict(object_offset=f.offset,function_offset=f.offset-65,original_addend=add,
            frame=list(f.frame),target=list(f.target),width=f.width,location_type=f.location_type,
            segment_relative=f.segment_relative,displacement=f.displacement,
            record_offset=f.record_offset,raw_fixupp=f.raw.hex()))
    if sorted((f['function_offset'],f['original_addend'])for f in fields)!=list(FIELD_ADDENDS):
        raise OwnedBSSError('all and only13 fixed private scalar fields/addends required')
    return {'classification':'complete_compiler_owned_private_BSS',
        'size':4,'segment':asdict(obj.segments[4]),'group':groups[0],
        'owner_symbol':desc['owner_symbol'],'whole_CODE_CV_union_size':578,
        'whole_CODE_sha256':hashlib.sha256(code).hexdigest(),
        'code_references':sorted(fields,key=lambda f:f['object_offset']),
        'private_scalar_debug_metadata':debug,'BSS_initialized_bytes':0,'BSS_byte_credit':0,
        'source_data_credit':0,'complete_BSS_MZ_sites':[],
        'historical_private_visibility_and_source_ownership_unknown':True,
        'omf_records_or_fields_modified':False,'full_source_link_layout_proven':False}


def validate_layout(obj,descriptor):
    """Pure target-free gate -> proof; no filesystem/reference/linker reads."""
    try:return _validate_layout(obj,descriptor)
    except OwnedBSSError:raise
    except (OMFError,KeyError,TypeError,ValueError,IndexError,AttributeError)as exc:
        raise OwnedBSSError('Owned BSS structural validation failed: '+str(exc))from exc


def validate_unit_metadata(unit):
    """Closed owner role before compiling: return an independent descriptor."""
    try:
        if not isinstance(unit,dict):
            raise OwnedBSSError('explicit C unit metadata required')
        desc=unit.get('owned_bss');_same_descriptor(desc)
        if (unit.get('language')!='c' or unit.get('backend')!='msc500-omf'
                or unit.get('symbol')!='_board_pointer_0daf' or unit.get('flags')!=['/AS','/Zi']
                or type(unit.get('size'))is not int or unit['size']!=513
                or unit.get('image_offset')!='0xdaf'
                or unit.get('code_address')is not None
                or unit.get('owned_const')is not None or unit.get('owned_data')is not None
                or not isinstance(unit.get('extended_extent'),dict)
                or unit['extended_extent'].get('kind')!='board_pointer_expanded_0daf_v1'
                or any(n in unit.get('externals',{})for n in desc['scalars'])):
            raise OwnedBSSError('exact genuine board-pointer C unit without scalar aliases required')
        return json.loads(json.dumps(desc))
    except OwnedBSSError:raise
    except (KeyError,TypeError,ValueError,IndexError,AttributeError)as exc:
        raise OwnedBSSError('Owned BSS unit metadata validation failed: '+str(exc))from exc


def validate(unit,obj,project,reference):
    """Return (descriptor, proof); authenticate allocation bounds, never zeros."""
    try:
        desc=validate_unit_metadata(unit)
        proof=validate_layout(obj,desc)
        if (not isinstance(reference,dict)or reference.get('original_sha256')!=ORIGINAL_SHA256
                or reference.get('carrier_sha256')!=CARRIER_SHA256
                or len(reference.get('image',b''))!=IMAGE_SIZE):
            raise OwnedBSSError('pinned original/expanded reference context required')
        image=reference['image'];sites=set(reference.get('relocations',()))
        if (not{0xea91,0xeb1c}<=sites or image[0xea90:0xea93]!=b'\xbf\xc2\x5c'
                or image[0xeb1b:0xeb20]!=b'\xb8\xc2\x5c\x8e\xd8'):
            raise OwnedBSSError('original CRT DGROUP paragraph proof required')
        if len(image)-0x5cc20!=0x52cb or int(desc['image_offset'],0)!=0x5cc20+0x52cc:
            raise OwnedBSSError('private BSS must begin beyond file-backed original DATA')
        project=Path(project).resolve();path=(project/desc['rea_evidence']).resolve()
        if not path.is_relative_to(project):raise OwnedBSSError('primary evidence escaped project')
        raw=path.read_bytes();e=json.loads(raw);norm=e['normalized_result'];profile=e['analysis_profile']['parameters']
        if (e['subject']['digest']['sha256']!=ORIGINAL_SHA256 or e['operation']!='read_bytes'
                or profile.get('load_segment')!='0x1000' or profile.get('language_id')!='x86:LE:16:Real Mode'
                or profile.get('target_format')!='dos-mz' or e['parameters']!={'address':'0x1ea86','length':179}
                or norm.get('address')!='0x1ea86' or norm.get('complete')is not True
                or norm.get('requested_bytes')!=179 or norm.get('returned_bytes')!=179):
            raise OwnedBSSError('complete pinned original CRT startup primary read required')
        body=bytes.fromhex(norm['bytes_hex'])
        pattern=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
        if len(body)!=179 or body!=image[0xea86:0xea86+179] or body.count(pattern)!=1:
            raise OwnedBSSError('exact original runtime zero bounds/CRT bytes required')
        proof.update(descriptor=json.loads(json.dumps(desc)),
            original_sha256=reference['original_sha256'],carrier_sha256=reference['carrier_sha256'],
            original_CRT_zero_range_exclusive=[0x52cc,0xcbe0],
            allocation_within_original_CRT_zero_range=True,
            original_CRT_zero_instruction_image_address=0xea86+body.index(pattern),
            original_CRT_zero_instruction_hex=pattern.hex(),
            original_initialized_DGROUP_end_exclusive=0x52cb,
            rea_evidence_id=e['evidence_id'],rea_evidence_sha256=hashlib.sha256(raw).hexdigest(),
            zero_bytes_compared_or_generated=False)
        return json.loads(json.dumps(desc)),proof
    except OwnedBSSError:raise
    except (OMFError,OSError,KeyError,TypeError,ValueError,IndexError,AttributeError)as exc:
        raise OwnedBSSError('Owned BSS validation failed: '+str(exc))from exc
