"""Closed three-long COMMON source-only profile. No match or placement credit."""
import dataclasses
import hashlib
import json
from pathlib import Path
import re
import struct

from msc import compile_c
from omf import read_omf, _Cursor
from reference import build_reference, ORIGINAL_SHA256
from clock_profile_pins import PINS

BACKEND='msc500-near-common-clock-v1'
SOURCE='src/link/clock_state.c'
SOURCE_SHA='86a6b8ac03040e2db15b54723ef05a27059a5bbc4e902668033b27fed3a6d2e5'
OBJECT_SHA='7d58ea231cc3aacca350419a4048dd18858e60d125ae6c76c31fb90ff850f116'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_clock_epoch','_clock_sample','_clock_value']
OFFSETS=[0xcbbe,0xcbc2,0xcbc6]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}


def require(value,message):
    if not value:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()


def local(project,name):
    path=(Path(project)/name).resolve()
    require(path.is_relative_to(Path(project).resolve()),'clock input path escapes project')
    return path


def validate_item(item):
    require(isinstance(item,dict)and set(item)==KEYS,'unknown clock allocation fields')
    require(item['id']=='clock-common'and item['backend']==BACKEND and item['compiler']=='msc500'
        and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['flags']==FLAGS
        and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed clock source/profile')
    require(item['objects']==[{'symbol':n,'size':4,'storage':'near-common'}for n in NAMES],
        'incomplete clock COMMON selection')
    require(item['evidence']==PINS,'clock evidence set/identity changed')


def validate_object(data):
    """Whole immutable OMF: exact 3 near signed-long commons, no loaded bytes."""
    obj=read_omf(data)
    require(not obj.publics and not obj.procedures,'clock COMMON defines PUBLIC/function')
    expected=[('_TEXT','CODE',0,0x48),('_DATA','DATA',0,0x48),('CONST','CONST',0,0x48),
        ('_BSS','BSS',0,0x48),('$$SYMBOLS','DEBSYM',61,0x20),('$$TYPES','DEBTYP',0,0x20)]
    require([(s.name,s.class_name,s.length,s.attributes)for s in obj.segments.values()]==expected,
        'clock COMMON loaded or debug allocation changed')
    require(not any(s.unsupported_data for s in obj.segments.values()),'clock COMMON LIDATA unsupported')
    commons=[]
    for kind,at,payload in obj.records:
        require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'clock COMMON foreign OMF record')
        if kind==0xb0:
            c=_Cursor(payload)
            while c:
                name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte()
                require(datatype==0x62 and size==4,'clock COMMON requires near datatype62 size4')
                require(typ==0x82,'clock COMMON requires signed-long type82')
                commons.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
        elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'clock COMMON DGROUP changed')
        elif kind==0x8a:require(payload==b'\0','clock COMMON entry point forbidden')
        elif kind==0x88:require(payload in [bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],
            'clock COMMON linker directive changed')
    require([c['symbol']for c in commons]==NAMES,'clock COMMON names/count/order changed')
    require(obj.externals==dict(enumerate(['__acrtused']+NAMES,1)),'clock COMMON externals/startup marker changed')
    require(all(seg==5 for _,seg,_,_ in obj.data_writes),'clock COMMON initialized bytes outside debug')
    expected_fixes=[(43,4),(22,3),(2,2)]
    require(len(obj.fixups)==3,'clock COMMON debug fixup count changed')
    for f,(offset,target)in zip(obj.fixups,expected_fixes):
        require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)
            ==(5,offset,4,3,True,(5,None),(2,target),None),'clock COMMON CodeView fixup changed')
    # Pins every CV name/type/zero address and every exact record, thread and
    # overlay directive; hidden debug/other allocations cannot evade this gate.
    require(sha(data)==OBJECT_SHA,'whole reviewed clock COMMON object changed')
    return commons


def validate_evidence(project,pins,target):
    require(pins==PINS,'clock evidence set/identity changed')
    payloads={}
    for key,row in pins.items():
        data=local(project,row['path']).read_bytes()
        require(sha(data)==row['sha256'],'clock evidence pin mismatch: '+key)
        payloads[key]=data
    proof=json.loads(payloads['layout']);proposal=json.loads(payloads['proposal'])
    primaries={k:json.loads(payloads[k])for k in('native_raw','prepare','refresh','crt')}
    for e in primaries.values():
        p=e['analysis_profile']['parameters']
        require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'
            and p['language_id']=='x86:LE:16:Real Mode'and p['target_format']=='dos-mz','clock primary target/profile')
    target_bytes=Path(target).read_bytes();require(sha(target_bytes)==ORIGINAL_SHA256,'clock original target pin')
    ref=build_reference(target_bytes);image=ref['image']
    native=primaries['native_raw']['normalized_result']
    require(native=={'address':'0x185c4','requested_bytes':110,'returned_bytes':110,
        'bytes_hex':image[0x85c4:0x8632].hex(),'complete':True},'clock complete raw110 comparison')
    for key,start,size in [('prepare',0x185c5,24),('refresh',0x185dd,32)]:
        e=primaries[key];body=e['normalized_result']['procedure']['body']
        require(e['parameters']=={'procedure':hex(start)}and body['contains_entry']and not body['non_contiguous']
            and body['total_bytes']==body['span_bytes']==size and body['ranges']==[{'start':hex(start),'end':hex(start+size-1)}],
            'clock native complete consumer extent')
    # Exact primary bytes, not decompiler types, establish 32-bit low/high word
    # stores and SUB/SBB arithmetic. Whole raw110 was already authenticated.
    require(image[0x85ce:0x85dc]==bytes.fromhex('a3becb8916c0cba3c2cb8916c4cb'),
        'clock epoch/sample native low/high stores')
    require(image[0x85e6:0x85fc]==bytes.fromhex('a3c2cb8916c4cb2b06becb1b16c0cba3c6cb8916c8cb'),
        'clock sample/value native 32bit subtraction/stores')
    crt=primaries['crt']['normalized_result'];clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
    require(crt['complete']and crt['address']=='0x1ea86'and crt['requested_bytes']==crt['returned_bytes']==179
        and bytes.fromhex(crt['bytes_hex'])==image[0xea86:0xeb39]
        and image[0xeaed:0xeaed+len(clear)]==clear,'clock original CRT clear proof')
    require(proof['matching_credit']==0 and proof['canonical_changed']is False
        and proof['whole110_executed']is False and len(proof['authentic_LINK_trials'])==2,
        'clock diagnostic scope changed')
    require(proof['compiles']['SCALARS']['source_sha256']==SOURCE_SHA
        and proof['compiles']['SCALARS']['object_sha256']==OBJECT_SHA
        and sha(payloads['source_model'])==SOURCE_SHA and sha(payloads['object'])==OBJECT_SHA,
        'clock source/object evidence identity')
    require(proposal['actual_definitions']==proof['COMMON_definitions']and proposal['original_constraints']==proof['constraints'],
        'clock definition constraints mismatch')
    for i,trial in enumerate(proof['authentic_LINK_trials']):
        prefix=['SCALARS-MAIN','MAIN-SCALARS'][i]
        exe=payloads[prefix+'_exe'];maptext=payloads[prefix+'_map'].decode('cp437').replace('\r\n','\n')
        require(sha(exe)==trial['exe_sha256']and maptext==trial['MAP']and trial['execution_exit_zero']
            and trial['original_or_reference_read_or_mounted']is False and payloads[prefix+'_pass'].strip()==b'passed',
            'clock executed LINK control identity')
        h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1]or 512)==len(exe),'clock diagnostic MZ size')
        load=exe[h[4]*16:];table=h[12]
        sites=[struct.unpack_from('<H',exe,table+4*j)[0]+16*struct.unpack_from('<H',exe,table+4*j+2)[0]for j in range(h[3])]
        require(sorted(sites)==trial['MZ_sites'],'clock diagnostic MZ set')
        part=maptext.split('Publics by Name')[1].split('Publics by Value')[0]
        def public(name):
            hits=re.findall(r'(?im)^\s*([0-9a-f]{4}):([0-9a-f]{4})\s+'+re.escape(name)+r'\s*$',part)
            require(len(hits)==1,'clock diagnostic public missing/ambiguous')
            return tuple(int(x,16)for x in hits[0])
        frame,edata=public('_edata');endframe,end=public('_end')
        require(endframe==frame and trial['CRTzero_range']==[edata,end],'clock diagnostic clear bounds')
        zeros=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa')
        at=trial['CRTzero_instruction_image'];require(load[at:at+len(zeros)]==zeros,'clock diagnostic CRT clear bytes')
        for name in NAMES:
            seg,off=public(name);at=seg*16+off
            require(seg==frame and edata<=off and off+4<=end and at>=len(load)
                and not any(at<=s<at+4 for s in sites),'clock actual allocation not wholly uninitialized')
    constraints=[]
    for name,off,row in zip(NAMES,OFFSETS,proposal['original_constraints']):
        require(row['symbol']==name and row['size']==4 and row['native_DS']==hex(off)
            and row['native_range_inclusive']==[hex(off),hex(off+3)]
            and row['original_allocated_MAP_proven']is False
            and 0x52cc<=off and off+4<=0xcbe0 and 0x5cc20+off>=len(image),
            'clock uninitialized native extent/constraint changed')
        constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),
            'end_exclusive':hex(off+4),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False})
    return constraints,proof


def build_input(item,project,target,output,*,compiler_fn=None):
    validate_item(item);project=Path(project).resolve();output=Path(output).resolve()
    source=local(project,SOURCE);before=source.read_bytes()
    require(sha(before)==SOURCE_SHA,'clock source pin mismatch')
    compiler_fn=compile_c if compiler_fn is None else compiler_fn
    # Source generation precedes comparison and accepts no target parameters.
    compiled=compiler_fn(source,FLAGS,compiler='msc500')
    require(source.read_bytes()==before and compiled.source_sha256==SOURCE_SHA
        and compiled.toolchain_manifest_sha256==MANIFEST_SHA and compiled.compiler=='msc500'
        and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C','clock fresh compiler provenance')
    definitions=validate_object(compiled.object_bytes)
    constraints,proof=validate_evidence(project,item['evidence'],target)
    require(compiled.tool_hashes==proof['compiles']['SCALARS']['tool_hashes']
        and list(compiled.command)==proof['compiles']['SCALARS']['command'],'clock fresh compiler tool/command pins')
    output.mkdir(parents=True,exist_ok=True);objpath=output/'clock-common.obj';objpath.write_bytes(compiled.object_bytes)
    provenance=dataclasses.asdict(compiled);provenance.pop('object_bytes')
    return {'id':item['id'],'source':SOURCE,'object':str(objpath),'object_sha256':sha(compiled.object_bytes),
        'definitions':definitions,'allocation_bytes':12,'initialized_bytes':0,'matching_credit':0,
        'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,
        'allocation_profile':'three_long_clock_scalars','authored_C_function_credit':0}
