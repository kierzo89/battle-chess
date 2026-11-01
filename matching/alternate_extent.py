"""Fixed alternate-view7E6B proof: 395 live bytes plus 18 compiler CODE words.

No generic switch-size permission is supplied. The entire CV431, all19 actual
own-CODE relocations, complete29-block CFG and each of36 table-byte xrefs are
mandatory. Ordinary six-entry switch profiles remain separate.
"""
import json
from extent import _evidence, _number

KIND='alternate_view_switch_7e6b_v1'
ORIGINAL='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
START,SIZE,TABLE,EPILOGUE=0x17e6b,431,0x17fed,0x18011
TARGETS=(0x17e8e,0x17f38,0x17eab,0x17ebe,0x17ef6,0x17f51,
         0x17eab,0x17eab,0x17eab,0x17eab,0x17f32,0x17eab,
         0x17eab,0x17eb4,0x17eb9,0x17eab,0x17eab,0x17fcc)
# Exact retained native blocks; this profile cannot be reused at another entry.
CFG=((0,27,(27,64)),(27,30,(30,)),
 (30,35,(35,64,73,78,83,139,199,205,230,353)),
 (35,58,(58,64)),(58,64,(64,)),(64,73,(422,)),
 (73,78,(64,)),(78,83,(64,)),(83,98,(64,98)),
 (98,134,(134,)),(134,139,(64,)),(139,154,(64,154)),
 (154,161,(64,161)),(161,199,(134,)),(199,205,(64,)),
 (205,218,(218,221)),(218,221,(64,)),(221,230,(64,)),
 (230,267,(267,285)),(267,285,(320,)),(285,317,(317,320)),
 (317,320,(320,)),(320,333,(333,341)),(333,341,(422,)),
 (341,348,(348,422)),(348,353,(422,)),(353,378,(341,378)),
 (378,386,(422,)),(422,431,()))


def validate_alternate_extent(unit,project,target_sha256,emitted,linked):
    meta=unit.get('extended_extent')
    if (not isinstance(meta,dict)or set(meta)!={
            'kind','raw_span_evidence','next_entry_evidence','table_xref_evidence'}
            or meta.get('kind')!=KIND or target_sha256!=ORIGINAL
            or unit.get('language')!='c'or unit.get('symbol')!='_alternate_view'
            or _number(unit['image_offset'])!=START-0x10000 or _number(unit['size'])!=SIZE
            or unit.get('backend')!='msc500-omf'
            or unit.get('flags')!=['/AS','/Gs','/Os','/Zi']
            or not isinstance(meta['table_xref_evidence'],str)):
        raise ValueError('alternate extent requires the fixed C500 7E6B profile')
    dossier=_evidence(project,unit['rea_evidence'],target_sha256,'analyze_function')
    raw=_evidence(project,meta['raw_span_evidence'],target_sha256,'read_bytes')
    following=_evidence(project,meta['next_entry_evidence'],target_sha256,'analyze_function')
    path=(project/meta['table_xref_evidence']).resolve()
    if not path.is_relative_to(project):raise ValueError('alternate xrefs outside matching project')
    xrefs=json.loads(path.read_text())
    if not isinstance(xrefs,list)or len(xrefs)!=36:raise ValueError('alternate requires all36 table-byte xrefs')
    for e in xrefs:
        profile=e['analysis_profile']['parameters']
        if (e['subject']['digest']['sha256']!=target_sha256 or e['operation']!='xrefs'
                or profile.get('load_segment')!='0x1000'
                or profile.get('language_id')!='x86:LE:16:Real Mode'):
            raise ValueError('alternate xref target/profile/operation mismatch')
    if len({e['analysis_profile']['digest']for e in [dossier,raw,following]+xrefs})!=1:
        raise ValueError('alternate analysis profiles differ')
    n=dossier['normalized_result'];proc=n['procedure'];body=proc['body']
    ranges=[(_number(x['start']),_number(x['end'])+1)for x in body.get('ranges',[])]
    if (body.get('available')is not True or body.get('contains_entry')is not True
            or body.get('non_contiguous')is not True or _number(proc['address'])!=START
            or ranges!=[(START,TABLE),(EPILOGUE,START+SIZE)]
            or body.get('total_bytes')!=395 or body.get('span_bytes')!=SIZE):
        raise ValueError('alternate requires exact native ranges with36 omitted table bytes')
    observed=[(_number(b['start'])-START,_number(b['end'])-START,
               tuple(sorted(_number(x)-START for x in b['successors'])))for b in n['basic_blocks']]
    if sorted(observed)!=sorted(CFG):raise ValueError('alternate requires all29 exact closed CFG blocks')
    addresses=[]
    for e in xrefs:
        addresses.append(_number(e['parameters']['address']))
        if e['normalized_result']!=[]:raise ValueError('alternate table byte has a global reference')
    if sorted(addresses)!=list(range(TABLE,EPILOGUE)):
        raise ValueError('alternate requires one empty global xref per table byte')
    d=raw['normalized_result'];blob=bytes.fromhex(d['bytes_hex'])
    if (d.get('complete')is not True or _number(d['address'])!=START
            or _number(raw['parameters']['address'])!=START
            or raw['parameters']['length']!=len(blob)
            or d.get('requested_bytes')!=len(blob)or d.get('returned_bytes')!=len(blob)
            or len(blob)<SIZE+3):raise ValueError('alternate requires complete raw and next-entry bytes')
    if not isinstance(linked,bytes)or len(linked)!=SIZE or blob[:SIZE]!=linked:
        raise ValueError('alternate complete raw span differs from freshly linked CV bytes')
    if (not isinstance(emitted,dict)or emitted.get('symbol')!='_alternate_view'
            or emitted.get('boundary')!='codeview3_procedure'or emitted.get('size')!=SIZE
            or emitted.get('end',-1)-emitted.get('offset',0)!=SIZE):
        raise ValueError('alternate requires independent complete431 CodeView bytes')
    # SUB AX,1; CMP AX,17; JA retained default; ADD AX,AX; XCHG AX,BX;
    # JMP word CS:[BX+7FED]. The default is a real native block, not the tail.
    if (blob[:8]!=bytes.fromhex('558bec83ec025756')
            or blob[14:35]!=bytes.fromhex('a056982ae42d01003d1100772503c0932effa7ed7f')
            or blob[384:386]!=bytes.fromhex('eb24')
            or blob[422:431]!=bytes.fromhex('e8960a5e5f8be55dc3')):
        raise ValueError('alternate selector bound/default/dispatcher/predecessor/tail differs')
    targets=tuple(0x10000+int.from_bytes(blob[i:i+2],'little')for i in range(386,422,2))
    if targets!=TARGETS:raise ValueError('alternate requires all18 exact native table targets')
    required={emitted['offset']+x for x in (33,*range(386,422,2))};supplied=set()
    for f in emitted.get('fixups',[]):
        if f.offset not in required:
            if any(f.offset<a+2 and f.offset+f.width>a for a in required):
                raise ValueError('alternate has undeclared overlapping CODE fixup')
            if f.segment_relative and f.target == (0,emitted['segment']):
                raise ValueError('unexpected additional alternate own-CODE field')
            continue
        if (f.width!=2 or f.location_type!=1 or not f.segment_relative
                or f.segment!=emitted['segment']or f.target!=(0,emitted['segment'])
                or f.frame not in ((0,emitted['segment']),(5,None))):
            raise ValueError('alternate requires actual own-CODE OFFSET16 fields')
        if f.offset in supplied:raise ValueError('duplicate alternate CODE fixup')
        supplied.add(f.offset)
    if supplied!=required:raise ValueError('alternate requires all19 actual compiler CODE fixups')
    p=following['normalized_result']['procedure'];b=p['body']
    if (b.get('available')is not True or b.get('contains_entry')is not True
            or b.get('non_contiguous')is not False or _number(p['address'])!=START+SIZE
            or b.get('ranges')!=[dict(start='0x1801a',end='0x18060')]
            or b.get('total_bytes')!=71 or b.get('span_bytes')!=71
            or blob[SIZE:SIZE+3]!=bytes.fromhex('c7064a')):
        raise ValueError('alternate requires the actual adjacent flat-view entry/body')
    return dict(kind=KIND,body_evidence_id=dossier['evidence_id'],raw_span_evidence_id=raw['evidence_id'],
                next_entry_evidence_id=following['evidence_id'],span_bytes=431,reachable_body_bytes=395,
                table_address=hex(TABLE),table_bytes=36,case_targets=[hex(x)for x in targets],
                compiler_code_fixups=19,closed_CFG_blocks=29,empty_global_table_byte_xrefs=36,
                next_entry=hex(START+SIZE),compiler_boundary='codeview3_procedure')
