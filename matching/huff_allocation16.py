"""Staged fixed multi-entry ASM CODE95 allocation, never function partitions.

This closed backend contains its own narrowly bounded 10-field relocation
calculation. It does not modify or delegate to a weakened generic linker.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import hashlib,json,re,shutil,struct,subprocess,tempfile
from omf import read_omf,OMFObject,OMFError

class AllocationError(OMFError):pass

def require(test,message):
    if not test:raise AllocationError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
SOURCE='asm/link/huff_helpers_omf.asm'
SOURCE_SHA256='a8d35b4ae268a67dffcf4b0485e84ed7d9d28004dffffb882ade61bccd58a8ac'
NASM_SHA256='57b8fc5957237b0d9b1ff48c8f5823780fb8ce968d9b8434850c06941ad5d5f5'
ORIGINAL_SHA256='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
BASE=0xe3ea
PUBLICS={'_huff_refill_e3ea':0,'_huff_depth_trap_e410':38}
BINDINGS={'_huff_memory_mode':{'segment':0x5cc2,'offset':0x44de},'_huff_memory_cursor':{'segment':0x5cc2,'offset':0x44da},'_huff_input_buffer':{'segment':0x5cc2,'offset':0x2ec2},'_read_asset':{'segment':0,'offset':0xcb8f}}
RAW_EVIDENCE='evidence/rea-huff-helpers-95-raw.json'
NATIVE={'refill':'evidence/rea-huff-refill.json','trap':'evidence/rea-huff-read_count.json'}
PROVIDER_PROOF='evidence/huff-helpers-95-provider.json'
PROVIDER_SHA256='6f691f502bcc1b89cc935cdbfec0655ce8bac013c582851d5a0aafe448e4d84d'
RAW_CODE_SHA256='052a3598d253167d8a0c94dc82d3327d875f964d506035ecf7afed27de795266'
FIXUP_PROFILE=[(2, 2, 1, True, (5, None), (2, 1), None), (21, 2, 1, True, (5, None), (2, 3), None), (27, 2, 1, False, (5, None), (2, 4), None), (45, 2, 1, True, (5, None), (2, 2), None), (55, 2, 1, True, (5, None), (2, 2), None), (64, 2, 2, True, (5, None), (2, 3), None), (69, 2, 1, True, (5, None), (2, 3), None), (79, 2, 1, True, (5, None), (2, 2), None), (84, 2, 1, True, (5, None), (2, 2), None), (87, 2, 1, True, (5, None), (2, 3), None)]
AUTHENTIC_LINK=[{'order': ['HELP', 'CALL', 'MAIN', 'READ'], 'exe': 'build/huff-helpers/HELP-CALL-MAIN-READ/UNIT.EXE', 'exe_sha256': 'b4c1a4fc7a22dd5295dfd98668347588b05ba1cf6a142f69dec01ea5eef28ef6', 'map': 'build/huff-helpers/HELP-CALL-MAIN-READ/UNIT.MAP', 'map_sha256': 'f0aeca8d855cb704d7b0cc6d4732652381b176cbd7fc3881bc4c1b94651d3aef'}, {'order': ['MAIN', 'READ', 'CALL', 'HELP'], 'exe': 'build/huff-helpers/MAIN-READ-CALL-HELP/UNIT.EXE', 'exe_sha256': '9f7c8a071c901d02ed28bdc3db321f779d88df1b727e264b5eff47ac4762e7da', 'map': 'build/huff-helpers/MAIN-READ-CALL-HELP/UNIT.MAP', 'map_sha256': '9957a754191bce2c8e3e9b74f9ba3a0eb2c8d5db24907e126f9eacbeaf211857'}]

def validate_unit(unit):
    if unit.get('object_profile') == 'huff_source_window_120':
        import huff_window_allocation16
        return huff_window_allocation16.validate_unit(unit)
    require((unit.get('id'),unit.get('language'),unit.get('backend'),unit.get('object_profile'),unit.get('source'))==('huff_refill_trap_code','asm-code','nasm-code-contribution-omf','huff_refill_trap',SOURCE),'Requires closed whole Huffman CODE allocation profile')
    require(unit.get('source_sha256')==SOURCE_SHA256 and unit.get('assembler_sha256')==NASM_SHA256,'Requires pinned authored source/NASM')
    require(unit.get('public_symbols')==list(PUBLICS)and unit.get('image_offset')==hex(BASE)and type(unit.get('size'))is int and unit['size']==95,'Whole95 with both actual PUBLICs required; no function crop')
    require(unit.get('externals')==BINDINGS and unit.get('rea_evidence')==RAW_EVIDENCE and unit.get('reference_region','unchanged-prefix')=='unchanged-prefix','Wrong native comparison bindings/evidence')
    require(not any(k in unit for k in('symbol','flags','end_symbol','extended_extent','owned_const','owned_data','owned_bss','data_address','code_address')),'Whole CODE contribution forbids function/ownership/slice metadata')

def extract_code(obj):
    require(isinstance(obj,OMFObject)and set(obj.segments)=={1},'Exactly one complete CODE segment required')
    seg=obj.segments[1]
    require((seg.name,seg.class_name,seg.attributes,seg.length,seg.unsupported_data)==('_TEXT','CODE',0x48,95,False),'Complete WORD PUBLIC USE16 CODE95 required')
    require(obj.externals==dict(enumerate(BINDINGS,1)),'Foreign/missing external')
    require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and len(obj.publics)==2 and all((p.segment,p.group,p.type_index)==(1,0,0)for p in obj.publics.values()),'Requires two actual unaliased PUBLIC entry points')
    for kind,_,payload in obj.records:
        require(kind in(0x80,0x88,0x96,0x98,0x8c,0x90,0xa0,0x9c,0x8a),'Foreign record/allocation/COMM/group/LIDATA')
        if kind==0x88:require(payload.startswith(b'\0\0')or payload==b'\x40\xa2\x01','Foreign linker directive')
        if kind==0x8a:require(payload==b'\0','No executable entry metadata')
    raw=bytearray()
    for offset,data in sorted(seg.chunks):
        require(data and offset==len(raw)and offset+len(data)<=95,'CODE hole/overlap/excess')
        raw.extend(data)
    require(len(raw)==95,'Omitted CODE tail')
    profile=[]
    for f in sorted(obj.fixups,key=lambda f:f.offset):
        require(f.segment==1,'Foreign fixup segment')
        profile.append((f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement))
    require(profile==FIXUP_PROFILE,'Exact10 fields/frame/target/mode required; no generic relocation allowance')
    require(digest(raw)==RAW_CODE_SHA256,'Raw instruction/addend bytes changed')
    require(raw[5:7]==b'\x75\x20'and raw[37:41]==b'\xc3\xcc\x06\x1e'and raw[-1]==0xc3,'Conditional shared-resume/trap/returns changed')
    return bytes(raw),{'boundary':'complete_multi_entry_CODE_SEGDEF','segment':{'index':1,'name':'_TEXT','class_name':'CODE','attributes':0x48,'length':95},'publics':[asdict(p)for p in obj.publics.values()],'native_entry_ownership':{'_huff_refill_e3ea':{'ranges_half_open':[[0,38],[39,95]],'live_bytes':94},'_huff_depth_trap_e410':{'ranges_half_open':[[38,39]],'live_bytes':1,'instruction':'INT3','resume_offset':39}},'raw_sha256':digest(raw),'actual_fixup_count':10,'authored_c_function_credit':0,'authored_asm_function_credit':0,'CODE_contributions':1}

@dataclass(frozen=True)
class Build:
    object_bytes:bytes
    code:bytes
    metadata:dict
    provenance:dict

def assemble(source,unit,nasm='nasm'):
    if unit.get('object_profile') == 'huff_source_window_120':
        import huff_window_allocation16
        return huff_window_allocation16.assemble(source,unit,nasm)
    validate_unit(unit);data=Path(source).read_bytes();require(digest(data)==SOURCE_SHA256,'Source pin mismatch')
    tool=shutil.which(nasm);require(tool is not None,'NASM unavailable');tool=Path(tool).resolve();require(digest(tool.read_bytes())==NASM_SHA256,'NASM pin mismatch')
    with tempfile.TemporaryDirectory(prefix='huff-allocation-')as tmp:
        p=Path(tmp);(p/'UNIT.ASM').write_bytes(data);command=[str(tool),'-f','obj','-Ox','UNIT.ASM','-o','UNIT.OBJ'];run=subprocess.run(command,cwd=p,capture_output=True,text=True,timeout=30)
        require(run.returncode==0 and(p/'UNIT.OBJ').exists(),'NASM failed: '+run.stdout+run.stderr);objbytes=(p/'UNIT.OBJ').read_bytes()
    require(digest(tool.read_bytes())==NASM_SHA256,'NASM changed');raw,metadata=extract_code(read_omf(objbytes))
    return Build(objbytes,raw,metadata,{'source_sha256':SOURCE_SHA256,'assembler_sha256':NASM_SHA256,'assembler_path':str(tool),'build_command':command,'assembler_log':run.stdout+run.stderr,'object_sha256':digest(objbytes),'object_format':'OMF16','fresh_directory':True})

def _link_fixed(obj,origin,bindings):
    """Only this fixed ten-field profile, including exactly BASE16 at+64."""
    raw,_=extract_code(obj);code_paragraph,code_offset=origin
    require(all(type(v)is int and 0<=v<=65535 for v in origin)and code_offset+95<=65536,'Invalid complete CODE placement')
    require(set(bindings)==set(BINDINGS)and all(isinstance(v,dict)and set(v)=={'segment','offset'}and all(type(n)is int and 0<=n<=65535 for n in v.values())for v in bindings.values()),'Invalid complete binding set')
    ds=bindings['_huff_input_buffer']['segment'];require(all(bindings[n]['segment']==ds for n in('_huff_memory_mode','_huff_memory_cursor'))and bindings['_read_asset']['segment']==code_paragraph,'Requires common data frame and same-CS read target')
    linked=bytearray(raw);logs=[]
    for f in sorted(obj.fixups,key=lambda f:f.offset):
        at=f.offset;name=obj.externals[f.target[1]];target=bindings[name];add=int.from_bytes(raw[at:at+2],'little');require(f.displacement is None,'No displacement extension')
        place=code_paragraph*16+code_offset+at;mode='dgroup_offset16';mz=None
        if f.location_type==2:
            require(at==64 and name=='_huff_input_buffer'and f.frame==(5,None)and f.target==(2,3)and f.segment_relative and add==0,'Only reviewed external-buffer GROUP BASE16 allowed')
            value=target['segment'];mode='external_buffer_group_base16';mz=place
        elif not f.segment_relative:
            require(at==27 and name=='_read_asset','Only actual near read call')
            value=target['offset']+add-(code_offset+at+2);mode='self_relative_code'
        else:value=target['offset']+add
        linked[at:at+2]=(value&65535).to_bytes(2,'little');row={'segment':1,'object_offset':at,'image_offset':place,'width':2,'location_type':f.location_type,'mode':mode,'target_symbol':name,'target_segment':target['segment'],'target_offset':target['offset'],'frame':list(f.frame),'target':list(f.target),'original_addend':add,'encoded_value':value&65535,'raw_fixupp':f.raw.hex()}
        if mz is not None:row['mz_segment_relocation_image_offset']=mz
        logs.append(row)
    return bytes(linked),logs

def _subject(e,operation,parameters):
    p=e.get('analysis_profile',{});provider=e.get('provider',{});s=e.get('subject',{})
    require(s.get('digest',{}).get('sha256')==ORIGINAL_SHA256 and s.get('format')=='dos-mz'and s.get('architecture')=='x86'and provider=={'id':'ghidra','name':'Ghidra','version':'12.1.4'}and p.get('provider')==provider and p.get('digest')=='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'and all(p.get('parameters',{}).get(k)==v for k,v in{'loader':'MzLoader','target_format':'dos-mz','language_id':'x86:LE:16:Real Mode','load_segment':'0x1000','address_coordinates':'linear-byte-offset'}.items()),'Wrong primary subject/provider/profile')
    require(e.get('operation')==operation and e.get('parameters')==parameters,'Wrong primary operation/parameters')
    require(re.fullmatch(r'ev_[0-9a-f]{64}',e.get('evidence_id',''))is not None,'Malformed primary ID')

def _native(project):
    project=Path(project);raw=json.loads((project/RAW_EVIDENCE).read_text());_subject(raw,'read_bytes',{'address':'0x1e3ea','length':95});r=raw['normalized_result'];require(r['complete']and r['returned_bytes']==r['requested_bytes']==95 and r['address']=='0x1e3ea'and len(bytes.fromhex(r['bytes_hex']))==95,'Complete95 raw required')
    ids={raw['evidence_id']};proofs={RAW_EVIDENCE:{'id':raw['evidence_id'],'sha256':digest((project/RAW_EVIDENCE).read_bytes())}}
    expected={'refill':(0xe3ea,94,95,[{'start':'0x1e3ea','end':'0x1e40f'},{'start':'0x1e411','end':'0x1e448'}],True),'trap':(0xe410,1,1,[{'start':'0x1e410','end':'0x1e410'}],False)}
    for kind,path in NATIVE.items():
        e=json.loads((project/path).read_text());address,live,span,ranges,disjoint=expected[kind];_subject(e,'analyze_function',{'procedure':hex(address+0x10000)});require(e['evidence_id']not in ids,'Duplicate primary IDs');ids.add(e['evidence_id']);p=e['normalized_result']['procedure'];b=p['body']
        require(p['address']==hex(address+0x10000)and not p['classification']['external']and not p['classification']['thunk']and b['available']and b['contains_entry']and b['total_bytes']==live and b['span_bytes']==span and b['ranges']==ranges and b['non_contiguous']==disjoint,'Native94+INT3 ownership differs')
        if kind=='trap':require(e['normalized_result']['assembly']==['0x1e410: INT3'],'Actual trap instruction required')
        cfg=([{'start':'0x1e3ea','end':'0x1e3f1','successors':['0x1e3f1','0x1e411']},{'start':'0x1e3f1','end':'0x1e410','successors':[]},{'start':'0x1e411','end':'0x1e449','successors':[]}]if kind=='refill'else[{'start':'0x1e410','end':'0x1e411','successors':[]}])
        require(e['normalized_result']['basic_blocks']==cfg,'Complete closed native CFG differs')
        proofs[path]={'id':e['evidence_id'],'sha256':digest((project/path).read_bytes()),'body':b}
    rawbytes=bytes.fromhex(r['bytes_hex']);require(rawbytes[5:7]==b'\x75\x20'and rawbytes[37:41]==b'\xc3\xcc\x06\x1e','Trap/resume ownership raw mismatch')
    provider_bytes=(project/PROVIDER_PROOF).read_bytes();require(digest(provider_bytes)==PROVIDER_SHA256,'Frozen provider proof pin mismatch');provider=json.loads(provider_bytes)
    require(proofs[RAW_EVIDENCE]['sha256']==provider['raw_primary_sha256']and proofs[RAW_EVIDENCE]['id']==provider['raw_primary_id'],'Frozen raw95 primary differs')
    for path in NATIVE.values():
        require(proofs[path]['sha256']==provider['native_primaries'][Path(path).name]['sha256']and proofs[path]['id']==provider['native_primaries'][Path(path).name]['evidence_id'],'Frozen native primary differs')
    return rawbytes,proofs

def _authenticate_links(project,obj):
    project=Path(project);proofbytes=(project/PROVIDER_PROOF).read_bytes();require(digest(proofbytes)==PROVIDER_SHA256,'Frozen two-order provider proof pin mismatch');provider=json.loads(proofbytes)
    require(len(provider['authentic_LINK'])==2,'Two distinct actual LINK orders required');records=[]
    for model,observed in zip(AUTHENTIC_LINK,provider['authentic_LINK']):
        require(observed['object_order']==model['order']and observed['executed']is False and observed['original_read_or_mounted']is False,'LINK context/order/observation changed')
        exe=(project/model['exe']).read_bytes();mapbytes=(project/model['map']).read_bytes();require(digest(exe)==model['exe_sha256']==observed['exe_sha256']and digest(mapbytes)==model['map_sha256'],'Authentic LINK EXE/MAP pin mismatch');text=mapbytes.decode('cp437').replace('\r\n','\n');require(text==observed['map'],'Actual MAP differs')
        pubs=text.split('Publics by Name')[1].split('Publics by Value')[0];names={n:{'segment':int(s,16),'offset':int(o,16)}for s,o,n in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',pubs,re.M)}
        origin=names['_huff_refill_e3ea'];trap=names['_huff_depth_trap_e410'];require(trap=={'segment':origin['segment'],'offset':origin['offset']+38},'Actual two PUBLIC placements changed')
        bindings={n:names[n]for n in BINDINGS};ds=bindings['_huff_input_buffer']['segment'];require(re.search(r'(?im)^\s*'+format(ds,'04X')+r':0\s+DGROUP\s*$',text)is not None,'Input buffer must resolve to actual DGROUP frame')
        linked,logs=_link_fixed(obj,(origin['segment'],origin['offset']),bindings);header=struct.unpack_from('<H',exe,8)[0]*16;image=exe[header:];start=origin['segment']*16+origin['offset'];require(image[start:start+95]==linked,'Entire95 disagrees with actual LINK')
        count,table=struct.unpack_from('<H',exe,6)[0],struct.unpack_from('<H',exe,24)[0];sites=[struct.unpack_from('<H',exe,table+4*i)[0]+16*struct.unpack_from('<H',exe,table+4*i+2)[0]for i in range(count)];owned=sorted(p for p in sites if p<start+95 and p+2>start);require(owned==[start+64],'Actual whole95 MZ set differs')
        require(int.from_bytes(linked[64:66],'little')==ds,'SEG input buffer must equal actual DGROUP, not pointer value or DATA base')
        records.append({'order':model['order'],'origin':origin,'whole95_sha256':digest(linked),'actual_DGROUP':ds,'actual_BASE16_word':int.from_bytes(linked[64:66],'little'),'MZ':owned,'all10_fields':logs,'executed':False})
    return records

def validate_evidence(unit,project,target_sha256,reference=None):
    if unit.get('object_profile') == 'huff_source_window_120':
        import huff_window_allocation16
        return huff_window_allocation16.validate_evidence(unit,project,target_sha256,reference)
    validate_unit(unit);require(target_sha256==ORIGINAL_SHA256,'Wrong target identity');_,proofs=_native(project);return proofs[RAW_EVIDENCE]['id']

def validate_comparison(unit,built,image,project,original_sites):
    if unit.get('object_profile') == 'huff_source_window_120':
        import huff_window_allocation16
        return huff_window_allocation16.validate_comparison(unit,built,image,project,original_sites)
    validate_unit(unit);obj=read_omf(built.object_bytes);raw,metadata=extract_code(obj);require(raw==built.code and metadata==built.metadata,'Build/object mismatch');linked,logs=_link_fixed(obj,(0,BASE),BINDINGS)
    require(image[BASE:BASE+95]==linked,'Complete95 native mismatch; no partial success')
    rawbytes,primary=_native(project);require(rawbytes==linked,'Original raw95 mismatch')
    emitted=[r['mz_segment_relocation_image_offset']for r in logs if'mz_segment_relocation_image_offset'in r];native=sorted(p for p in original_sites if p<BASE+95 and p+2>BASE);require(emitted==native==[BASE+64],'Complete original/emitted MZ set differs or crosses allocation')
    actual=_authenticate_links(project,obj);loads=[]
    for load in[0,1,0x1234,0xee10]:
        a=bytearray(linked);b=bytearray(image[BASE:BASE+95])
        for sites,data in[(emitted,a),(native,b)]:
            for site in sites:k=site-BASE;data[k:k+2]=((int.from_bytes(data[k:k+2],'little')+load)&65535).to_bytes(2,'little')
        require(a==b,'Four-base mismatch');loads.append({'load_paragraph':load,'all95_equal':True,'sha256':digest(a)})
    return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':95,'whole_allocation_sha256':digest(linked),'whole_original_mz_sites':native,'emitted_mz_sites':emitted,'relocations':logs,'four_load_bases':loads,'primary_evidence':primary,'authentic_two_order_LINK':actual,'native_entry_ownership':metadata['native_entry_ownership'],'whole_bytes_equal':True,'authored_c_function_credit':0,'authored_asm_function_credit':0,'ASM_CODE_contributions':1,'function_partition_claim':False,'executed':False}
