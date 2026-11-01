"""Fixed 0DAF boundary: original raw bytes and independently complete expanded CFG.

The original analyzer's 93-byte fragment and false 0E0D entry are preserved as
negative observations. This gate grants no general split-boundary exception.
"""
import hashlib
import json
from extent import _evidence, _number
from reference import build_reference, ORIGINAL_SHA256, CARRIER_SHA256
START, SIZE, NEXT_SIZE = 0x10daf, 513, 125
END = START + SIZE
PROFILE = '894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
BODY_SHA = '68344091d09ccca382b5ec9dc992b7fe68c9157722da19613eee64a9f453bef7'
NEXT_SHA = '95bccbc50d68d3bb1200c9b24c504804808ce48ca346f2e80943db5abb91d543'
CFG_SHA = '8a57cf967ef26ff50a024c32615ac45d31b2603e7f1eb014fd263248963e2d9b'
NEXT_CFG_SHA = '85ede6042502b69da8b0cff4df8b063b5bdea0dbc75573a605ddd16d3e50ab0a'
RELATIVE = {7,154,169,198,270,337,374,400,414,429,464,478,493}
POSITIONS = {7,27,61,120,123,134,151,154,163,169,176,184,195,198,207,210,214,231,238,244,252,258,264,270,279,285,292,299,305,313,319,327,331,337,346,352,360,364,368,374,383,388,397,400,411,414,423,429,435,443,446,452,461,464,475,478,487,493,502,505}
FAR = {388,435}
MZ = {0xf35,0xf64}
FALSE = {0x10de6:[0x1dbd3],0x10e0d:[0x10813,0x1082b,0x1db9b]}
FIELDS = {'kind','original_raw_evidence','original_next_evidence','original_overlap_evidence',
 'original_false_xrefs_evidence','expanded_body_evidence','expanded_raw_evidence',
 'expanded_next_evidence','expanded_false_xrefs_evidence','expanded_instruction_evidence',
 'expanded_interior_evidence','expanded_branch_evidence'}


def _hash(b): return hashlib.sha256(b).hexdigest()


def _body(e,start,total,span,ranges):
    if e['parameters'] != {'procedure':hex(start)}:
        raise ValueError('board-pointer native query differs')
    p=e['normalized_result']['procedure'];b=p['body']
    if (_number(p['address'])!=start or b.get('available') is not True
        or b.get('contains_entry') is not True or b.get('total_bytes')!=total
        or b.get('span_bytes')!=span or b.get('non_contiguous') is not (len(ranges)>1)
        or b.get('ranges')!=[{'start':hex(a),'end':hex(z)} for a,z in ranges]):
        raise ValueError('board-pointer independently observed native body differs')


def _raw(e):
    n=e['normalized_result'];b=bytes.fromhex(n['bytes_hex'])
    if (e['parameters']!={'address':hex(START),'length':638}
        or _number(n['address'])!=START or n.get('complete') is not True
        or n.get('requested_bytes')!=638 or n.get('returned_bytes')!=638 or len(b)!=638):
        raise ValueError('board-pointer requires complete original/expanded 638-byte context')
    return b


def _cfg(e,start,size,count,digest):
    n=e['normalized_result']
    blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(a) for a in q['successors']))) for q in n['basic_blocks'])
    if len(blocks)!=count or _hash(json.dumps(blocks,separators=(',',':')).encode())!=digest:
        raise ValueError('board-pointer independently complete CFG differs')
    starts={a for a,_,_ in blocks};cursor=start
    for a,z,s in blocks:
        if a!=cursor or not a<z<=start+size or any(t not in starts for t in s):
            raise ValueError('board-pointer CFG is not a closed complete byte partition')
        cursor=z
    if cursor!=start+size: raise ValueError('board-pointer CFG coverage incomplete')
    graph={a:s for a,_,s in blocks};todo=[start];seen=set()
    while todo:
        a=todo.pop()
        if a not in seen: seen.add(a);todo.extend(graph[a])
    if seen!=starts: raise ValueError('board-pointer CFG has unreachable blocks')
    for r in n.get('incoming_references',[]):
        a=_number(r['target_address']);s=_number(r['source_address'])
        if a!=start and not(start<=s<start+size and a in starts):
            raise ValueError('board-pointer CFG has additional external interior entry')


def validate_board_pointer_extent(unit,project,target_sha256,emitted,linked):
    m=unit.get('extended_extent')
    if (not isinstance(m,dict) or set(m)!=FIELDS or m['kind']!='board_pointer_expanded_0daf_v1'
        or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='board_pointer_0daf'
        or unit.get('symbol')!='_board_pointer_0daf' or unit.get('language')!='c'
        or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
        or unit.get('code_address') is not None or _number(unit['image_offset'])!=0xdaf
        or _number(unit['size'])!=SIZE or unit.get('externals',{}).get('__chkstk')!=0xecaa):
        raise ValueError('unsupported fixed board-pointer extent identity')
    orig=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function')
    es={};all_e=[orig]
    for key in FIELDS-{'kind'}:
        sha=ORIGINAL_SHA256 if key.startswith('original') else CARRIER_SHA256
        op=('xrefs' if 'xrefs' in key else 'read_bytes' if 'raw' in key else
            'inspect_native_instruction' if key in {'expanded_instruction_evidence','expanded_interior_evidence','expanded_branch_evidence'} else 'analyze_function')
        paths=m[key] if 'xrefs' in key else [m[key]]
        if not isinstance(paths,list) or len(paths)!=(2 if 'xrefs' in key else 1):
            raise ValueError('board-pointer requires both fixed false-boundary xref observations')
        items=[_evidence(project,p,sha,op) for p in paths];all_e.extend(items)
        es[key]=items if 'xrefs' in key else items[0]
    if (len({e['evidence_id'] for e in all_e})!=len(all_e)
        or any(e['analysis_profile']['digest']!=PROFILE or e['analysis_profile']['parameters'].get('target_format')!='dos-mz' for e in all_e)):
        raise ValueError('board-pointer requires distinct evidence in fixed native DOS profile')
    _body(orig,START,93,94,[(START,0x10de5),(0x10de7,0x10e0c)])
    _body(es['original_overlap_evidence'],0x10e0d,274,276,[(0x10e0d,0x10e2f),(0x10e31,0x10eb1),(0x10eb3,0x10f20)])
    _body(es['original_next_evidence'],END,124,125,[(END,0x11011),(0x11013,0x1102c)])
    _body(es['expanded_body_evidence'],START,SIZE,SIZE,[(START,END-1)])
    _body(es['expanded_next_evidence'],END,NEXT_SIZE,NEXT_SIZE,[(END,END+NEXT_SIZE-1)])
    for key in ['original_false_xrefs_evidence','expanded_false_xrefs_evidence']:
        for e,address in zip(es[key],FALSE):
            expected=FALSE[address] if key.startswith('original') else []
            if e['parameters']!={'address':hex(address)} or sorted(_number(a) for a in e['normalized_result'])!=expected:
                raise ValueError('board-pointer requires exact false far aliases and empty expanded xrefs')
    ref=build_reference((project.parent/'CHESS.EXE').read_bytes());image=ref['image']
    context=image[0xdaf:0x102d];relocs={s for s in ref['relocations'] if 0xdaf<=s<0x102d}
    expanded=bytearray(context)
    for s in relocs:
        at=s-0xdaf;expanded[at:at+2]=((int.from_bytes(expanded[at:at+2],'little')+0x1000)&0xffff).to_bytes(2,'little')
    if (ref['carrier_sha256']!=CARRIER_SHA256 or relocs!=MZ or context!=_raw(es['original_raw_evidence'])
        or bytes(expanded)!=_raw(es['expanded_raw_evidence']) or _hash(context[:SIZE])!=BODY_SHA
        or _hash(context[SIZE:])!=NEXT_SHA or not isinstance(linked,bytes) or linked!=context[:SIZE]):
        raise ValueError('board-pointer complete original bytes, relocated expanded bytes or MZ set differ')
    for address,sources in FALSE.items():
        for source in sources:
            at=source-0x10000;call=image[at:at+5]
            expected='9ab600d310' if address==0x10de6 else '9add00d310'
            if (call.hex()!=expected or at+3 not in ref['relocations']
                or 0x10000+16*int.from_bytes(call[3:5],'little')+int.from_bytes(call[1:3],'little')!=address+0x10000):
                raise ValueError('board-pointer false aliases lack authentic relocated FAR10D3 calls')
    _cfg(es['expanded_body_evidence'],START,SIZE,44,CFG_SHA)
    _cfg(es['expanded_next_evidence'],END,NEXT_SIZE,4,NEXT_CFG_SHA)
    for key,address,status,hexbytes,length,mnemonic,kind,dests in [
        ('expanded_instruction_evidence',0x10de5,'decoded','b81200',3,'MOV','fallthrough',[]),
        ('expanded_interior_evidence',0x10de6,'not-instruction-boundary',None,None,None,'unavailable',[]),
        ('expanded_branch_evidence',0x10e0d,'decoded','7f03',2,'JG','jump',['0x10e12'])]:
        e=es[key];n=e['normalized_result']
        if (e['parameters']!={'address':hex(address)} or _number(n['address'])!=address
            or n.get('procedure')!=hex(START) or n.get('status')!=status or n.get('bytes')!=hexbytes
            or n.get('length')!=length or n.get('mnemonic')!=mnemonic
            or n['flow'].get('kind')!=kind or n['flow'].get('direct_destinations')!=dests
            or (hexbytes is not None and linked[address-START:address-START+length].hex()!=hexbytes)):
            raise ValueError('board-pointer interior immediate/branch instruction observation differs')
    if (not isinstance(emitted,dict) or emitted.get('symbol')!=unit['symbol']
        or emitted.get('boundary')!='codeview3_procedure' or emitted.get('size')!=SIZE
        or type(emitted.get('offset')) is not int or emitted['offset'] not in {0,65}
        or emitted.get('end')!=emitted['offset']+SIZE or type(emitted.get('segment')) is not int
        or emitted['segment']<=0 or not isinstance(emitted.get('fixups'),list) or len(emitted['fixups'])!=60):
        raise ValueError('board-pointer requires full CV513 at reviewed source-context offset0 or65')
    private_fields = {}
    if unit.get('owned_bss') is not None:
        from owned_bss16 import validate_unit_metadata, FIELD_ADDENDS
        validate_unit_metadata(unit)
        if emitted['offset'] != 65:
            raise ValueError('private BSS owner requires complete578 source context offset65')
        private_fields = dict(FIELD_ADDENDS)
    supplied=set();mz=set()
    for f in emitted['fixups']:
        a=f.offset-emitted['offset'];far=a in FAR;private=a in private_fields
        if (a not in POSITIONS or a in supplied or f.segment!=emitted['segment']
            or f.width!=(4 if far else 2) or f.location_type!=(3 if far else 1)
            or f.segment_relative is not (a not in RELATIVE)
            or f.frame!=((1,1) if private else (5,None))
            or (f.target!=(0,4) if private else (f.target[0]!=2 or type(f.target[1]) is not int or f.target[1]<=0)) or (f.displacement or 0)!=0):
            raise ValueError('board-pointer requires exact sixty external compiler fields')
        if private and int.from_bytes(linked[a:a+2],'little') != 0x52cc + private_fields[a]:
            raise ValueError('private BSS field must identify its complete unsigned word')
        supplied.add(a)
        if far: mz.add(0xdaf+a+2)
    if mz!=MZ: raise ValueError('board-pointer compiler MZ set differs')
    return {'kind':m['kind'],'body_evidence_id':orig['evidence_id'],
        'expanded_body_evidence_id':es['expanded_body_evidence']['evidence_id'],
        'original_sha256':ORIGINAL_SHA256,'expanded_carrier_sha256':CARRIER_SHA256,
        'span_bytes':SIZE,'reachable_body_bytes':SIZE,'closed_cfg_blocks':44,
        'body_sha256':BODY_SHA,'next_complete_body_bytes':NEXT_SIZE,'next_complete_body_sha256':NEXT_SHA,
        'original_native_observation_bytes':93,'original_next_observation_bytes':124,
        'false_far_aliases':4,'actual_far_targets':['0x20de6','0x20e0d'],
        'compiler_fixups':60,'compiler_private_BSS_fields':len(private_fields),'mz_relocations':sorted(MZ),'compiler_boundary':'codeview3_procedure'}
