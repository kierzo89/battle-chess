"""Fixed main0010: closed native575-byte infinite loop plus dead5-byte C return.

The original and full authenticated expanded MZ are distinct subjects. Exact
raw original bytes, loader arithmetic, native CFG, empty gap references and
fresh complete compiler output are all mandatory, without patching metadata.
"""
import hashlib
import json
from extent import _evidence, _number
from reference import build_reference, ORIGINAL_SHA256, CARRIER_SHA256
START,GAP,END,SIZE,NEXT_SIZE=0x10010,0x1024f,0x10254,580,1439
BODY_SHA='b7180b005ddce9d41182ec0f9795c963adbe1d1a2c130a61a323d37bce1d968f'
NEXT_SHA='2432bdd2e49be5fe9d753bed31505d9b0c70e175706480b87fc42482907a80e7'
CFG_SHA='3b38db11030e6f6ea06844dfb6b41ae2a6f50b99566654824597973a84491c1d'
NEXT_CFG_SHA='446e04f517f75f5cf2f578c37c566cb3bafc155fb589684cda7b077b79a2bef8'
PROFILE='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
NEXT_RANGES=[(0x10254,0x10393),(0x10395,0x1048e),(0x10490,0x104e5),(0x104e8,0x10711),
             (0x10713,0x1073b),(0x1073d,0x1079c),(0x1079e,0x107c0),(0x107c2,0x107f3)]
MZ_SITES={152,303,343,472,498,576,584}
NEXT_MZ={0x2dc,0x2fa,0x443,0x697}
FIXUPS = {7:(2,1,False),12:(2,1,True),34:(2,1,True),48:(2,1,False),59:(2,1,True),63:(2,1,True),77:(2,1,False),88:(2,1,True),92:(2,1,True),106:(2,1,False),116:(2,1,False),122:(2,1,True),125:(2,1,False),128:(2,1,True),134:(4,3,True),143:(2,1,True),150:(2,1,True),157:(2,1,True),163:(2,1,True),169:(2,1,True),175:(2,1,True),183:(2,1,True),189:(2,1,True),195:(2,1,True),201:(2,1,True),206:(2,1,True),212:(2,1,False),218:(2,1,False),224:(2,1,False),231:(2,1,True),243:(2,1,True),254:(2,1,False),261:(2,1,True),273:(2,1,True),284:(2,5,True),287:(2,2,True),292:(2,1,False),299:(2,1,True),303:(2,1,True),309:(2,1,True),315:(2,1,True),318:(2,1,False),322:(2,1,True),325:(4,3,True),330:(2,1,False),334:(2,1,True),337:(2,1,False),344:(2,1,False),350:(2,1,False),365:(2,1,False),389:(2,1,False),399:(2,1,False),403:(2,1,False),420:(2,1,False),427:(2,1,True),438:(2,1,False),444:(2,1,False),453:(2,1,True),456:(2,2,True),461:(2,1,False),467:(2,1,False),470:(2,1,False),474:(2,1,True),480:(4,3,True),485:(2,1,True),489:(2,1,True),503:(2,1,True),507:(2,1,False),519:(2,1,True),526:(2,1,True),530:(2,1,False),534:(2,1,True),540:(2,1,True),546:(2,1,True),548:(2,1,True),552:(2,1,True),558:(4,3,True),563:(2,1,False),566:(4,3,True),571:(2,1,False)}
FIELDS={'kind','original_raw_evidence','expanded_raw_evidence','next_entry_evidence','jump_evidence',
        'original_gap_xrefs','expanded_gap_xrefs','epilogue_decoder_evidence'}


def _hash(b):return hashlib.sha256(b).hexdigest()


def _raw(e):
    p=e['parameters'];n=e['normalized_result'];b=bytes.fromhex(n['bytes_hex'])
    if (p!={'address':hex(START),'length':SIZE+NEXT_SIZE} or _number(n['address'])!=START
            or n.get('complete')is not True or n.get('requested_bytes')!=SIZE+NEXT_SIZE
            or n.get('returned_bytes')!=SIZE+NEXT_SIZE or len(b)!=SIZE+NEXT_SIZE):
        raise ValueError('main requires complete original/expanded2019-byte context')
    return b


def _native(e,start,ranges,total,span,count,digest):
    n=e['normalized_result'];p=n['procedure'];b=p['body']
    if (e['parameters']!={'procedure':hex(start)} or _number(p['address'])!=start
            or b.get('available')is not True or b.get('contains_entry')is not True
            or b.get('non_contiguous')is not(len(ranges)>1)
            or b.get('ranges')!=[{'start':hex(a),'end':hex(z-1)}for a,z in ranges]
            or b.get('total_bytes')!=total or b.get('span_bytes')!=span):
        raise ValueError('main native body/adjacent function extent differs')
    blocks=sorted((_number(q['start']),_number(q['end']),tuple(sorted(_number(a)for a in q['successors'])))for q in n['basic_blocks'])
    if len(blocks)!=count or _hash(json.dumps(blocks,separators=(',',':')).encode())!=digest:
        raise ValueError('main requires exact independently retained native CFG')
    starts={a for a,_,_ in blocks};merged=[]
    for a,z,succ in blocks:
        if not a<z or any(t not in starts for t in succ):raise ValueError('main native CFG must be closed')
        if merged and a==merged[-1][1]:merged[-1]=(merged[-1][0],z)
        else:merged.append((a,z))
    if merged!=ranges or sum(z-a for a,z,_ in blocks)!=total:
        raise ValueError('main native CFG must own each reachable byte exactly once')
    graph={a:s for a,_,s in blocks};pending=[start];seen=set()
    while pending:
        a=pending.pop()
        if a not in seen:seen.add(a);pending.extend(graph[a])
    if seen!=starts:raise ValueError('main native CFG has unreachable claimed blocks')
    return n


def validate_main_extent(unit,project,target_sha256,emitted,linked):
    m=unit.get('extended_extent')
    if (not isinstance(m,dict) or set(m)!=FIELDS or m['kind']!='main_unreachable_epilogue_0010_v1'
            or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='main_0010' or unit.get('symbol')!='_main'
            or unit.get('language')!='c' or unit.get('backend')!='msc500-omf' or unit.get('flags')!=['/AS','/Zi']
            or _number(unit['image_offset'])!=0x10 or _number(unit['size'])!=SIZE
            or unit.get('code_address')is not None or unit.get('externals',{}).get('__chkstk')!=0xecaa
            or not all(isinstance(m[k],list)and len(m[k])==5 for k in ['original_gap_xrefs','expanded_gap_xrefs'])
            or not isinstance(m['epilogue_decoder_evidence'],list)or len(m['epilogue_decoder_evidence'])!=4):
        raise ValueError('unsupported fixed main0010 extent identity')
    body=_evidence(project,unit['rea_evidence'],CARRIER_SHA256,'analyze_function')
    raw=_evidence(project,m['original_raw_evidence'],ORIGINAL_SHA256,'read_bytes')
    expanded=_evidence(project,m['expanded_raw_evidence'],CARRIER_SHA256,'read_bytes')
    following=_evidence(project,m['next_entry_evidence'],CARRIER_SHA256,'analyze_function')
    jump=_evidence(project,m['jump_evidence'],CARRIER_SHA256,'inspect_native_instruction')
    xs=[_evidence(project,p,ORIGINAL_SHA256,'xrefs')for p in m['original_gap_xrefs']]
    exs=[_evidence(project,p,CARRIER_SHA256,'xrefs')for p in m['expanded_gap_xrefs']]
    dec=[_evidence(project,p,CARRIER_SHA256,'inspect_native_instruction')for p in m['epilogue_decoder_evidence']]
    all_e=[body,raw,expanded,following,jump,*xs,*exs,*dec]
    if (len({e['evidence_id']for e in all_e})!=len(all_e)or any(e['analysis_profile']['digest']!=PROFILE
            or e['analysis_profile']['parameters'].get('target_format')!='dos-mz'for e in all_e)):
        raise ValueError('main requires distinct original/expanded evidence in fixed native profile')
    reference=build_reference((project.parent/'CHESS.EXE').read_bytes());context=reference['image'][0x10:0x7f3]
    sites={s for s in reference['relocations']if 0x10<=s<0x7f3}
    loaded=bytearray(context)
    for s in sites:
        a=s-0x10;loaded[a:a+2]=((int.from_bytes(context[a:a+2],'little')+0x1000)&0xffff).to_bytes(2,'little')
    if (sites!=MZ_SITES|NEXT_MZ or context!=_raw(raw) or bytes(loaded)!=_raw(expanded)
            or _hash(context[:SIZE])!=BODY_SHA or _hash(context[SIZE:])!=NEXT_SHA
            or not isinstance(linked,bytes)or len(linked)!=SIZE or linked!=context[:SIZE]
            or linked[-7:]!=bytes.fromhex('ebfb5e8be55dc3')):
        raise ValueError('main complete original/C bytes, expanded loader arithmetic or next1439 bytes differ')
    native=_native(body,START,[(START,GAP)],575,575,32,CFG_SHA)
    _native(following,END,NEXT_RANGES,1424,1439,145,NEXT_CFG_SHA)
    for group in [xs,exs]:
        if (sorted(_number(e['parameters']['address'])for e in group)!=list(range(GAP,END))
                or any(set(e['parameters'])!={'address'}or e['normalized_result']!=[]for e in group)):
            raise ValueError('main five dead epilogue bytes need empty global xrefs in both images')
    if any(GAP<=_number(r['target_address'])<END for r in native.get('incoming_references',[])):
        raise ValueError('main dead epilogue cannot have an incoming reference')
    j=jump['normalized_result']
    if (jump['parameters']!={'address':'0x1024d'}or _number(j['address'])!=0x1024d
            or j.get('status')!='decoded'or j.get('bytes')!='ebfb'or j.get('length')!=2
            or j.get('mnemonic')!='JMP'or j.get('procedure')!='0x10010'
            or j['flow'].get('kind')!='jump'or j['flow'].get('conditional')is not False
            or j['flow'].get('computed')is not False or j['flow'].get('direct_destinations')!=['0x1024a']):
        raise ValueError('main requires independently decoded closed backward EBFB loop')
    if sorted(_number(e['parameters']['address'])for e in dec)!=[GAP,GAP+1,GAP+3,GAP+4]:
        raise ValueError('main requires retained decoder observations for every raw epilogue operation')
    for e in dec:
        n=e['normalized_result']
        if (set(e['parameters'])!={'address'}or _number(n['address'])!=_number(e['parameters']['address'])
                or n.get('status')!='undecodable'or n.get('length')is not None or n.get('bytes')is not None):
            raise ValueError('main unreachable epilogue native decoder remains explicitly unknown')
    if (not isinstance(emitted,dict)or emitted.get('symbol')!='_main'or emitted.get('boundary')!='codeview3_procedure'
            or emitted.get('size')!=SIZE or type(emitted.get('offset'))is not int or emitted['offset']<0
            or emitted.get('end')!=emitted['offset']+SIZE or type(emitted.get('segment'))is not int
            or emitted['segment']<=0 or not isinstance(emitted.get('fixups'),list)or len(emitted['fixups'])!=80):
        raise ValueError('main requires fresh complete580-byte CV extent and all80 reconstructed OMF fields')
    seen=set();mz=set()
    for f in emitted['fixups']:
        a=f.offset-emitted['offset']
        if (a not in FIXUPS or a in seen or f.segment!=emitted['segment']
                or (f.width,f.location_type,f.segment_relative)!=FIXUPS[a]or f.frame!=(5,None)
                or f.target[0]!=2 or type(f.target[1])is not int or f.target[1]<=0 or(f.displacement or 0)!=0):
            raise ValueError('main reconstructed external OFFSET16/BASE16/FAR16 fixup ownership differs')
        seen.add(a)
        if f.location_type in(2,3):mz.add(0x10+a+(2 if f.location_type==3 else 0))
    if mz!=MZ_SITES:raise ValueError('main complete MZ fields differ from original loader-site set')
    return {'kind':m['kind'],'expanded_body_evidence_id':body['evidence_id'],
            'original_raw_evidence_id':raw['evidence_id'],'expanded_raw_evidence_id':expanded['evidence_id'],
            'span_bytes':580,'reachable_body_bytes':575,'closed_cfg_blocks':32,
            'gap_address':hex(GAP),'gap_bytes':5,'gap_hex':'5e8be55dc3','decoder_status':'undecodable',
            'compiler_boundary':'codeview3_procedure','compiler_fixups':80,'original_MZ_sites':sorted(mz),
            'body_sha256':BODY_SHA,'next_complete_span_bytes':1439,'next_reachable_body_bytes':1424,
            'next_closed_cfg_blocks':145,'next_complete_span_sha256':NEXT_SHA,
            'original_sha256':ORIGINAL_SHA256,'expanded_carrier_sha256':CARRIER_SHA256}
