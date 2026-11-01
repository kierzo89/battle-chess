"""Closed22-byte source extent from a native thunk2 + interior-body20 union.

No ordinary function-manager boundary is changed. Every byte is reachable from
8577; the separate857C provider entry is preserved as an interior entry fact.
"""
from pathlib import Path
import json,hashlib
from extent import _evidence, _number
KIND='shared_book_skip_literals78_8577_v1'
ORIGINAL='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
NEXT_SHA256='6c33f8abba78fb308af5a5ffc514e43a4ea0218fdcc808ad6f642da103f98833'
START=0x18577
NATIVE=bytes.fromhex('eb03e811008b1ed2b08e06a64d26f687ffff4074edc3')
RAW=bytes.fromhex('eb03e800008b1e00008e06000026f687ffff4074edc3')
KEYS={'kind','interior_evidence','raw_span_evidence','next_entry_evidence','next_raw_evidence','instructions_evidence','all_byte_xrefs_evidence'}

def require(ok,message):
    if not ok:raise ValueError(message)

def validate_shared_book_skip_extent(unit,project,target_sha256,emitted,linked,source_object=None):
    p=Path(project).resolve();m=unit.get('extended_extent')
    require(isinstance(m,dict) and set(m)==KEYS and m['kind']==KIND and target_sha256==ORIGINAL,'fixed book-skip profile required')
    require(unit.get('language')=='c' and unit.get('backend')=='msc500-omf' and unit.get('symbol')=='_skip_book_8577' and _number(unit['image_offset'])==0x8577 and _number(unit['size'])==22 and unit.get('flags')==['/AS','/Gs','/Os','/Zi'] and not any(unit.get(k)is not None for k in ('code_address','owned_const','owned_data','owned_bss')),'book-skip C unit identity/profile')
    require(source_object is not None,'fresh complete source object required')
    require(unit.get('source')=='src/shared_turn_book_literals_match.c' and isinstance(unit.get('owned_selector_const'),dict) and unit['owned_selector_const'].get('kind')=='shared_turn_book_literals78_v1','shared source/selector owner identity required')
    obj=source_object
    from shared_turn_book_literals78 import validate_shared_object
    validate_shared_object(obj)
    require(emitted==obj.function_info(unit['symbol']),'fresh emitted procedure does not identify object')
    require((emitted['segment'],emitted['offset'],emitted['size'],emitted['boundary'])==(1,2341,22,'codeview3_procedure'),'natural shared skip complete CV context changed')
    s=obj.segments[1];require((s.name,s.class_name,s.length,s.attributes)==('_TEXT','CODE',2418,0x48) and not s.unsupported_data,'whole natural WORD CODE2418 required')
    code=bytearray()
    for at,body in sorted(s.chunks):
        require(at==len(code) and body,'CODE holes/overlaps');code.extend(body)
    require(len(code)==2418 and code[2341:2363]==RAW,'complete raw compiler skip body changed')
    fields=emitted['fixups'];require(len(fields)==4,'skip requires exact four compiler fields')
    expected={3:(False,(5,None),(2,'_previous_book_858d'),b'\0\0'),7:(True,(5,None),(2,'_book_choice_offset'),b'\0\0'),11:(True,(1,1),(0,3),b'\0\0'),16:(True,(5,None),(2,'_splash_buffer'),b'\xff\xff')}
    seen=set()
    for f in fields:
        at=f.offset-2341;require(at in expected and at not in seen,'foreign/overlapping compiler field');seen.add(at)
        rel,frame,target,addend=expected[at]
        actual_target=(f.target[0],obj.externals.get(f.target[1]))if f.target[0]==2 else f.target
        require((f.segment,f.width,f.location_type,f.segment_relative,f.frame,actual_target,f.displacement)==(1,2,1,rel,frame,target,None) and code[f.offset:f.offset+2]==addend,'compiler field frame/target/addend changed')
    evidence=[]
    def read(path,operation):
        e=_evidence(p,path,ORIGINAL,operation);evidence.append(e);return e
    entry=read(unit['rea_evidence'],'analyze_function')['normalized_result']
    interior=read(m['interior_evidence'],'analyze_function')['normalized_result']
    following=read(m['next_entry_evidence'],'analyze_function')['normalized_result']
    def body(n,address,start,end):
        q=n['procedure'];b=q['body']
        require(_number(q['address'])==address and b.get('available')is True and b.get('contains_entry')is True and b.get('non_contiguous')is False and b.get('total_bytes')==end-start+1 and b.get('span_bytes')==end-start+1 and b.get('ranges')==[{'start':hex(start),'end':hex(end)}],'exact native body/entry partition required')
    body(entry,START,START,START+1);body(interior,START+5,START+2,START+21);body(following,START+22,START+22,START+76)
    require(entry['procedure']['classification'].get('thunk')is True and entry['procedure']['classification'].get('thunk_target')==hex(START+5),'native entry thunk fact required')
    require(interior['procedure']['classification'].get('thunk')is False and following['procedure']['classification'].get('thunk')is False,'interior/next must be native bodies')
    require(entry['basic_blocks']==[{'start':hex(START),'end':hex(START+2),'successors':[]}],'native thunk CFG changed')
    cfg=[(_number(b['start'])-START,_number(b['end'])-START,tuple(_number(x)-START for x in b['successors']))for b in interior['basic_blocks']]
    require(cfg==[(2,5,(5,)),(5,21,(2,21)),(21,22,())],'complete closed native interior loop CFG required')
    def raw(path,at,length):
        e=read(path,'read_bytes');r=e['normalized_result'];b=bytes.fromhex(r['bytes_hex'])
        require(e['parameters']=={'address':hex(at),'length':length} and r.get('complete')is True and r.get('address')==hex(at) and r.get('requested_bytes')==length and r.get('returned_bytes')==length and len(b)==length,'complete exact primary raw span required');return b
    blob=raw(m['raw_span_evidence'],START,23)
    require(blob==NATIVE+b'\x55' and bytes(linked)==NATIVE,'whole22 freshly linked bytes/native raw mismatch')
    next_raw=raw(m['next_raw_evidence'],START+22,55)
    require(hashlib.sha256(next_raw).hexdigest()==NEXT_SHA256 and next_raw[0]==0x55 and next_raw[-1]==0xc3,'complete next55 primary required')
    def bundle(path,operation):
        file=(p/path).resolve();require(file.is_relative_to(p),'evidence bundle escapes project')
        records=json.loads(file.read_text());require(isinstance(records,list),'complete evidence bundle required')
        for e in records:
            require(e['subject']['digest']['sha256']==ORIGINAL and e['operation']==operation and e['analysis_profile']['parameters'].get('load_segment')=='0x1000' and e['analysis_profile']['parameters'].get('language_id')=='x86:LE:16:Real Mode','bundle target/profile/operation mismatch');evidence.append(e)
        return records
    xrefs=bundle(m['all_byte_xrefs_evidence'],'xrefs');require(len(xrefs)==22,'global xrefs for every byte required')
    for index,e in enumerate(xrefs):
        at=START+index;expected_refs={START:['0x18570'],START+2:['0x1858a'],START+5:['0x18577']}.get(at,[])
        require(e['parameters']=={'address':hex(at)} and e['normalized_result']==expected_refs,'foreign/interior/operand incoming reference')
    instructions=bundle(m['instructions_evidence'],'inspect_native_instruction')
    shape=[(0,2,'JMP','jump',False,[START+5]),(2,3,'CALL','call',False,[START+22]),(5,4,'MOV','fallthrough',False,[]),(9,4,'MOV','fallthrough',False,[]),(13,6,'TEST','fallthrough',False,[]),(19,2,'JZ','jump',True,[START+2]),(21,1,'RET','return',False,[]),(22,1,'PUSH','fallthrough',False,[])]
    require(len(instructions)==len(shape),'complete seven instructions plus next required')
    for e,(offset,length,mnemonic,kind,conditional,destinations)in zip(instructions,shape):
        r=e['normalized_result'];f=r['flow']
        require(e['parameters']=={'address':hex(START+offset)} and r['address']==hex(START+offset) and r['status']=='decoded' and r['length']==length and r['mnemonic']==mnemonic and bytes.fromhex(r['bytes'])==blob[offset:offset+length] and f['kind']==kind and f['conditional']==conditional and f['computed']is False and f['direct_destinations']==list(map(hex,destinations)),'native instruction/branch/return shape changed')
    require(len({e['analysis_profile']['digest']for e in evidence})==1,'mixed native analysis profiles')
    return dict(kind=KIND,entry_native_body_bytes=2,interior_native_body_bytes=20,interior_entry=hex(START+5),source_CV_bytes=22,native_union_bytes=22,all_bytes_reachable_from_source_entry=True,global_xref_byte_queries=22,compiler_fields=4,complete_native_MZ_sites=[],native_partition_rewritten=False,evidence_ids=[e['evidence_id']for e in evidence],linked_sha256=hashlib.sha256(bytes(linked)).hexdigest(),source_CODE_bytes=2418,whole_source_link_claim=False)
