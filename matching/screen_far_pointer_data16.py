"""Closed source-only C5 huge-char pointer DATA, with explicit external FAR16.

Complete WORD DATA is derived from untouched, checksum-validated OMF. The
pointee is only an external consumed view: no backing allocation or capacity.
No ordinary cdata, near-pointer, library or OMF parser gate is changed.
"""
from dataclasses import asdict
import hashlib
from msc import validate_toolchain
from omf import read_omf, OMFError
from cdata_pointer import _whole, _groups, _debug

BACKEND = 'msc500-screen-far-pointer-data-omf'
SYMBOL = '_screen'
EXTERNAL = '_screen_pixels'
FLAGS = ['/AS', '/Zl', '/Zi']
PROFILE = 'screen_external_view_v1'
SOURCE_SHA256 = '6bfdf54eb6fefa054241129bf7aca0620617b274d40c64a41a6362b5e4444e09'
NEGATIVE_SOURCE_SHA256 = '2388a1df08d9f6bb2d76a303624565c64847088a8df4245c7254c685ff2f5746'
MANIFEST_SHA256 = 'd2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOL_HASHES = {'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
REVIEWED_SOURCE_HASHES = {SOURCE_SHA256, NEGATIVE_SOURCE_SHA256}
CV = bytes.fromhex('0101008001010080010100800105007800838000')
KINDS = [0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0x90,0x88,0xa0,0x9c,0xa0,0x9c,0xa0,0x8a]

class FarPointerDataError(OMFError):
    pass


def require(condition, message):
    if not condition:
        raise FarPointerDataError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def word(value):
    require(type(value) is int and 0 <= value <= 65535, 'FAR16 explicit unsigned16 address required')
    return value


def resolve_external_far16(fixup, raw_field, binding, image_place):
    """Resolve one genuine frame=target FAR16 field, without normalization.

    OMF frame method5 means the external target's frame. Both words of the
    actual field are retained as addends. This closed shape requires a zero
    selector addend; offset addition must fit16 bits rather than silently
    normalize a huge pointer or carry into its selector. Only the selector
    gets an MZ loader relocation. No target bytes participate.
    """
    require(fixup.width == 4 and fixup.location_type == 3 and fixup.segment_relative is True
            and fixup.frame == (5,None) and fixup.target[0] == 2
            and type(fixup.target[1]) is int and fixup.target[1] > 0
            and fixup.displacement is None, 'FAR16 requires exact frame5 external-target shape')
    require(isinstance(raw_field,bytes) and len(raw_field)==4, 'FAR16 complete actual4-byte field required')
    require(isinstance(binding,dict) and set(binding)=={'segment','offset'}, 'FAR16 explicit named segment/offset binding required')
    segment,offset = word(binding['segment']),word(binding['offset'])
    require(type(image_place) is int and 0 <= image_place <= 0x10ffec, 'FAR16 image field placement invalid')
    addend = int.from_bytes(raw_field[:2],'little')
    selector_addend = int.from_bytes(raw_field[2:],'little')
    require(selector_addend == 0, 'FAR16 nonzero selector addend unsupported')
    require(offset + addend <= 65535, 'FAR16 offset addend overflow is unsupported')
    value = offset + addend
    encoded = value.to_bytes(2,'little') + segment.to_bytes(2,'little')
    return encoded, {'mode':'far16_pointer','image_offset':image_place,
        'object_offset':fixup.offset,'frame_method':5,'frame_datum':None,
        'target_method':2,'target_datum':fixup.target[1],
        'target_offset':offset,'target_segment':segment,'original_addend':addend,
        'original_selector_addend':selector_addend,'displacement':None,
        'encoded_offset':value,'encoded_segment':segment,
        'record_offset':fixup.record_offset,'raw_fixupp':fixup.raw.hex(),
        'mz_segment_relocation_image_offset':image_place+2}


def validate_unit(unit):
    keys={'id','language','backend','source','symbol','image_offset','size','reference_region',
          'flags','externals','rea_evidence','data_address','object_profile','boundary_evidence'}
    require(isinstance(unit,dict) and set(unit)<=keys, 'screen pointer unsupported unit metadata')
    require(unit.get('language')=='c-data' and unit.get('backend')==BACKEND
            and unit.get('object_profile')==PROFILE, 'screen pointer closed backend/profile required')
    require(unit.get('symbol')==SYMBOL and unit.get('flags')==FLAGS
            and unit.get('size')==4 and unit.get('reference_region')=='exepack-expanded',
            'screen pointer source type/profile/whole4-byte comparison required')
    address=unit.get('data_address')
    require(isinstance(address,dict) and set(address)=={'segment','offset'}, 'screen pointer complete DATA placement required')
    frame,offset=word(address['segment']),word(address['offset'])
    origin=unit.get('image_offset')
    require(isinstance(origin,str), 'screen pointer image offset must be explicit hexadecimal text')
    try:origin=int(origin,0)
    except ValueError as ex:raise FarPointerDataError('screen pointer invalid image offset') from ex
    require(origin==frame*16+offset and offset%2==0 and offset+4<=65536,
            'screen pointer natural WORD DATA placement required')
    bindings=unit.get('externals')
    require(isinstance(bindings,dict) and set(bindings)=={EXTERNAL}, 'screen pointer exact external consumed-view name required')
    binding=bindings[EXTERNAL]
    require(isinstance(binding,dict) and set(binding)=={'segment','offset'}, 'screen pointer explicit external frame/offset required')
    word(binding['segment']);word(binding['offset'])


def link_data(object_bytes, symbol, origin, dgroup_segment, externals):
    """Strict raw-object decoder and complete FAR16 DATA relocation.

    No unit size, source text, reference image, historical bytes or pointee
    storage is supplied to this decoder. The accepted segment/PUBLIC/type
    contract is the actual C5 emitted huge-char pointer plus incomplete far
    char external view, including its complete debug types and fixup.
    """
    require(isinstance(object_bytes,bytes), 'screen pointer requires untouched raw OMF bytes')
    obj=read_omf(object_bytes)
    require(symbol==SYMBOL, 'screen pointer public selection changed')
    require([k for k,_,_ in obj.records]==KINDS, 'screen pointer record/allocation sequence changed')
    expected=[('_TEXT','CODE',0,72),('_DATA','DATA',4,72),('CONST','CONST',0,72),
              ('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',22,32),('$$TYPES','DEBTYP',20,32)]
    require([(s.name,s.class_name,s.length,s.attributes)for s in obj.segments.values()]==expected,
            'screen pointer complete allocations/types changed')
    require(not obj.procedures and set(obj.publics)=={SYMBOL}, 'screen pointer no procedures or alias PUBLICs allowed')
    p=obj.publics[SYMBOL]
    require((p.segment,p.offset,p.group,p.type_index)==(2,0,1,224), 'screen pointer PUBLIC0 huge-char type224 required')
    require(all(s.index==i and s.overlay_index==1 for i,s in obj.segments.items()), 'screen pointer SEGDEF identities changed')
    for i in (1,3,4):
        require(not obj.segments[i].chunks and not obj.segments[i].unsupported_data, 'screen pointer extra empty-segment data')
    groups=_groups(obj)
    require(groups==[{'index':1,'name':'DGROUP','segments':[3,4,2]}], 'screen pointer unique complete DGROUP required')
    require(obj.externals=={1:'__acrtused',2:EXTERNAL}, 'screen pointer exact startup/consumed EXTDEFs required')
    require([b.hex()for k,_,b in obj.records if k==0x8c]==['0a5f5f6163727475736564010e5f73637265656e5f706978656c738203'],
            'screen pointer EXTDEF far-char-array type identity changed')
    raw,writes=_whole(obj.segments[2])
    require(obj.segments[6].chunks==[(0,CV)] and not obj.segments[6].unsupported_data,
            'screen pointer complete far-char-array CV type stream changed')
    debug=_debug(obj,2,{EXTERNAL})
    require(debug['external_symbol_records'][0]['type_index']==0x203,
            'screen pointer external far-char array debug type changed')
    require(len(obj.fixups)==2, 'screen pointer one DATA field plus one exact debug field required')
    fs=[f for f in obj.fixups if f.segment==2]
    require(len(fs)==1 and fs[0].offset==0, 'screen pointer complete nonoverlapping FAR16 field required')
    fixed={0x80:[b'\x09C:\\UNIT.C'],0x88:[bytes.fromhex(x)for x in ('009d30734f','00a1014356','00a201')],
           0x8a:[b'\0']}
    for kind,payloads in fixed.items():
        require([b for k,_,b in obj.records if k==kind]==payloads, 'screen pointer header/directive/entry changed')
    # Raw FIXUPP sequence includes the real C5 frame threads. Strict parsing
    # plus exact raw field records ensures no hidden foreign/thread rewrites.
    require([b.hex()for k,_,b in obj.records if k==0x9c]==
            ['000301020201030440014501','cc005602','cc025602'], 'screen pointer raw FIXUPP/thread layout changed')
    dgroup_segment=word(dgroup_segment)
    base=origin-16*dgroup_segment if type(origin)is int else -1
    require(0<=base<=65532 and base%2==0, 'screen pointer natural complete WORD DATA placement required')
    require(isinstance(externals,dict) and set(externals)=={EXTERNAL}, 'screen pointer missing/extra external placement')
    linked,log=resolve_external_far16(fs[0],raw,externals[EXTERNAL],origin)
    log['target_symbol']=EXTERNAL
    return linked,{'boundary':'complete_omf_far_pointer_data_segment','symbol':symbol,
        'segment':{k:v for k,v in asdict(obj.segments[2]).items()if k!='chunks'},
        'public':asdict(p),'publics':{symbol:asdict(p)},'group':groups[0],
        'data_writes':writes,'origin':origin,'dgroup_segment':dgroup_segment,'dgroup_offset':base,
        'object_sha256':sha(object_bytes),'unlinked_sha256':sha(raw),'sha256':sha(linked),
        'all_raw_fixups':[asdict(f)|{'raw':f.raw.hex()}for f in obj.fixups],
        'relocations':[log],'emitted_mz_sites':[origin+2],'debug':debug,
        'source_declared_type':'char huge *','external_view_type':'extern char far []',
        'externals':externals,'startup_marker_unused':True,'authored_c_function_count':0,
        'pointee_allocated':False,'pointee_capacity_proved':False,'net_LINK_closure_claim':False}


def validate_compiled(compiled, source_bytes, unit):
    validate_unit(unit)
    require(sha(source_bytes)in REVIEWED_SOURCE_HASHES and compiled.source_sha256==sha(source_bytes),
            'screen pointer unreviewed source identity')
    require(compiled.compiler=='msc500' and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C',
            'screen pointer compiler flags/model/source-name changed')
    require(compiled.toolchain_manifest_sha256==MANIFEST_SHA256 and compiled.tool_hashes==TOOL_HASHES,
            'screen pointer compiler manifest/tool provenance changed')
    require(tuple(compiled.command)==('T:\\CL.EXE','/c',*FLAGS,'/FoC:\\UNIT.OBJ','C:\\UNIT.C'),
            'screen pointer compiler command changed')
    return link_data(compiled.object_bytes,unit['symbol'],int(unit['image_offset'],0),
                     unit['data_address']['segment'],unit['externals'])
