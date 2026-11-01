"""Closed seven-int/Move8 COMMON profile. Source-only, zero match credit."""
import dataclasses
import hashlib
import json
from pathlib import Path
import re
import struct
from msc import compile_c
from omf import read_omf,_Cursor
from library16 import link_segment
from reference import build_reference,ORIGINAL_SHA256
from book_profile_pins import PINS

BACKEND='msc500-near-common-book-v1'
SOURCE='src/link/book_state.c'
SOURCE_SHA='94b79e32dbb305fdbc0fcbd64ed7896403a9c8e5ce10c44619554ba1bd12a1c6'
OBJECT_SHA='bc399610c9b25ffc8dbb99eeb4bac46bc1dd41f9922e09951f998788ef862eb3'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_book_choice_offset','_book_saved_index','_book_matches','_hint_score_964c','_book_state_index','_best','_iteration','_working_follow_8bb6']
SIZES=[2]*7+[8]
TYPES=[0x81]*7+[522]
OFFSETS=[0xb0d2,0x9366,0xb0cc,0x964c,0x8cfe,0x8de0,0x8de8,0x8bb6]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}


def require(condition,message):
    if not condition:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()


def local(project,name):
    path=(Path(project)/name).resolve()
    require(path.is_relative_to(Path(project).resolve()),'book input path escapes project')
    return path


def validate_item(item):
    require(isinstance(item,dict)and set(item)==KEYS,'unknown book allocation fields')
    require(item['id']=='book-state-common'and item['backend']==BACKEND and item['source']==SOURCE
        and item['source_sha256']==SOURCE_SHA and item['compiler']=='msc500'and item['flags']==FLAGS
        and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed book source/profile')
    require(item['objects']==[{'symbol':n,'size':s,'storage':'near-common'}for n,s in zip(NAMES,SIZES)],
        'incomplete book COMMON selection')
    require(item['evidence']==PINS,'book evidence set/identity changed')


def validate_object(data):
    """Whole raw OMF, exact COMMON types and complete debug evidence."""
    obj=read_omf(data)
    require(not obj.publics and not obj.procedures,'book COMMON defines PUBLIC/function')
    expected=[('_TEXT','CODE',0,0x48),('_DATA','DATA',0,0x48),('CONST','CONST',0,0x48),
        ('_BSS','BSS',0,0x48),('$$SYMBOLS','DEBSYM',181,0x20),('$$TYPES','DEBTYP',177,0x20)]
    require([(s.name,s.class_name,s.length,s.attributes)for s in obj.segments.values()]==expected,
        'book COMMON loaded or debug allocation changed')
    require(not any(s.unsupported_data for s in obj.segments.values()),'book COMMON LIDATA forbidden')
    definitions=[]
    for kind,at,payload in obj.records:
        require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'book foreign OMF record')
        if kind==0xb0:
            c=_Cursor(payload)
            while c:
                name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte()
                require(datatype==0x62,'book must be near COMMON')
                definitions.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
        elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'book DGROUP changed')
        elif kind==0x8a:require(payload==b'\0','book entry point forbidden')
        elif kind==0x88:require(payload in [bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],
            'book linker directive changed')
    require([d['symbol']for d in definitions]==NAMES,'book COMMON names/count/order changed')
    require([d['size']for d in definitions]==SIZES,'book COMMON sizes changed')
    require([d['type_index']for d in definitions]==TYPES,'book signed-int/Move8 types changed')
    require(obj.externals==dict(enumerate(['__acrtused']+NAMES,1)),'book external/startup marker changed')
    require(all(seg in(5,6)for _,seg,_,_ in obj.data_writes),'book initialized bytes outside debug')
    require(len(obj.fixups)==8,'book debug fixup count changed')
    for f,(off,target)in zip(obj.fixups,[(155,9),(137,8),(124,7),(99,6),(75,5),(54,4),(29,3),(2,2)]):
        require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)
            ==(5,off,4,3,True,(5,None),(2,target),None),'book CodeView fixup changed')
    # Raw hash includes the entire complete CV union/struct definition, field
    # names/types/offsets, all record checksums/lengths and overlays/threads.
    require(sha(data)==OBJECT_SHA,'whole reviewed book COMMON object changed')
    return definitions


def validate_evidence(project,pins,target):
    require(pins==PINS,'book evidence set/identity changed')
    data={}
    for key,pin in pins.items():
        raw=local(project,pin['path']).read_bytes()
        require(sha(raw)==pin['sha256'],'book evidence pin mismatch: '+key);data[key]=raw
    def b(rel):return data[rel]
    def j(rel):return json.loads(b(rel))
    root='build/book-storage-followup/'
    proof=j(root+'common-diagnostic-proof.json');review=j(root+'storage-audit.json')
    require(proof['matching_credit']==0 and not proof['game_executed']and not proof['canonical_changed']
        and proof['source_only_generation_LINK_execution_before_target_comparison']is True
        and proof['historical_storage_owner_class_and_order_proven']is False,'book proof scope')
    require(review['splash_buffer']['definition_proposed']is False and not review['splash_buffer']['capacity_inferred_from_request_or_gaps'],'far splash buffer must remain held')
    require(proof['compiles']['SCALARS']['source_sha256']==SOURCE_SHA and proof['compiles']['SCALARS']['object_sha256']==OBJECT_SHA
        and sha(b(root+'scalars.c'))==SOURCE_SHA and sha(b(root+'SCALARS.OBJ'))==OBJECT_SHA
        and sha(b(root+'main.c'))==proof['compiles']['MAIN']['source_sha256']
        and sha(b(root+'MAIN.OBJ'))==proof['compiles']['MAIN']['object_sha256'],'book source/object identity')
    require(proof['linker_sha256']==sha(b('toolchains/msc510/LINK.EXE'))
        and proof['SLIBC_sha256']==sha(b('toolchains/runtime500/SLIBC.LIB'))
        and proof['LIBH_sha256']==sha(b('toolchains/runtime-libh/LIBH.LIB')),'book linker/runtime pins')
    target_bytes=Path(target).read_bytes();require(sha(target_bytes)==ORIGINAL_SHA256,'book original target pin')
    reference=build_reference(target_bytes);image=reference['image']
    def native(e,carrier=False):
        p=e['analysis_profile']['parameters']
        require(e['subject']['digest']['sha256']==(reference['carrier_sha256']if carrier else ORIGINAL_SHA256) and(p['load_segment'],p['language_id'],p['target_format'])==('0x1000','x86:LE:16:Real Mode','dos-mz'),'book native subject/profile')
    crt=j('evidence/rea_crt_startup_500.json');native(crt);raw=crt['normalized_result']
    require(crt['operation']=='read_bytes'and crt['parameters']=={'address':'0x1ea86','length':179}
        and raw['complete']and raw['address']=='0x1ea86'and raw['requested_bytes']==raw['returned_bytes']==179
        and bytes.fromhex(raw['bytes_hex'])==image[0xea86:0xeb39],'book complete original CRT179 primary')
    require(review['CRT_clear']['evidence_id']==crt['evidence_id']and review['CRT_clear']['start_inclusive']=='0x52cc'
        and review['CRT_clear']['end_exclusive']=='0xcbe0'and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'book original CRTzero interval')
    carrier=j(root+'rea-carrier-load-image.json');native(carrier,carrier=True);load=carrier['normalized_result']
    require(carrier['operation']=='inspect_native_load_image'and load['status']=='verified'and load['target_sha256']==reference['carrier_sha256']
        and load['load_segment']==0x1000 and load['module_bytes']==len(image)==401131 and load['overlay_bytes']==0
        and all(c['matched']is True for c in load['checks']),'book pinned expanded carrier/import not verified')
    boundary=j(root+'rea-initialized-boundary.json');native(boundary,carrier=True);last=boundary['normalized_result']
    require(boundary['operation']=='read_bytes'and boundary['parameters']=={'address':'0x71edc','length':32}
        and last['address']=='0x71edc'and last['returned_bytes']==15 and last['requested_bytes']==32 and last['complete']is False
        and bytes.fromhex(last['bytes_hex'])==image[0x61edc:],'book initialized boundary must not supply gap/BSS zeros')
    require(len(proof['original_constraints'])==len(review['constraints'])==8,'book eight native views required')
    constraints=[]
    for name,offset,size,v,q in zip(NAMES,OFFSETS,SIZES,review['constraints'],proof['original_constraints']):
        require(v['symbol']==q['symbol']==name and v['minimum_size']==q['size']==size and v['native_DS']==q['native_DS']==hex(offset)
            and v['required_final_MAP']=={'segment':'0x5cc2','offset':hex(offset),'end_exclusive':hex(offset+size)}
            and not v['original_owner_common_or_aggregate_proven']and not v['placement_enforced_by_diagnostic']
            and q['original_MAP_placement_not_reproduced']is True,'book native type/extent/unknownMAP identity')
        require(0x52cc<=offset and offset+size<=0xcbe0 and 0x5cc20+offset>=len(image),'book scalar not wholly uninitialized/CRT-cleared')
        read=j(v['read_window']['path']);native(read,carrier=True);r=read['normalized_result']
        require(read['operation']=='read_bytes'and int(read['parameters']['address'],0)==0x6cc20+offset
            and read['parameters']['length']==size and r['address']==hex(0x6cc20+offset)
            and r['requested_bytes']==size and r['returned_bytes']==0 and r['bytes_hex']==''and r['complete']is False,'book primary must not borrow initialized DATA zeros')
        require(v['native_width_proof'],'book native consumed width proof missing')
        for w in v['native_width_proof']:
            e=j(w['path']);native(e)
            require(e['operation']=='analyze_function'and e['evidence_id']==w['evidence_id']and w['observed_instructions']
                and all(ins in e['normalized_result']['assembly']for ins in w['observed_instructions']),'book native consumed instructions absent')
        # WORD scalar views and four MOVSW copying Move8; exact original widths,
        # not adjacent-distance or initialized zero bytes, justify this model.
        if size==2:
            require(any(('word ptr' in ins or 'AX' in ins or 'BX' in ins or 'CX' in ins)and hex(offset)in ins
                for w in v['native_width_proof']for ins in w['observed_instructions']),'book actual word consumer required')
        else:
            ins=v['native_width_proof'][0]['observed_instructions']
            require(ins==['0x1835d: MOV DI, 0x8bb6','0x18360: MOV SI, 0x4e2','0x18363: MOVSW ES:DI, SI','0x18364: MOVSW ES:DI, SI','0x18365: MOVSW ES:DI, SI','0x18366: MOVSW ES:DI, SI']
                and image[0x835d:0x8367]==bytes.fromhex('bfb68bbee204a5a5a5a5'),'book complete Move8 copy proof')
        constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(offset),'end_exclusive':hex(offset+size),
            'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False})
    require(len(proof['authentic_LINK_trials'])==2,'book two-order LINK proof missing')
    for i,trial in enumerate(proof['authentic_LINK_trials']):
        prefix=['SCALARS-MAIN','MAIN-SCALARS'][i];exe=data[root+prefix+'/UNIT.EXE']
        text=data[root+prefix+'/UNIT.MAP'].decode('cp437').replace('\r\n','\n')
        require(trial['order']==prefix.split('-')and sha(exe)==trial['exe_sha256']and text==trial['MAP']
            and trial['execution_exit_zero']and not trial['original_or_reference_read_or_mounted']
            and data[root+prefix+'/PASS.TXT'].strip()==b'passed','book retained LINK/runtime proof identity')
        h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1]or 512)==len(exe),'book diagnostic MZ size')
        load=exe[h[4]*16:];sites=[struct.unpack_from('<H',exe,h[12]+4*j)[0]+16*struct.unpack_from('<H',exe,h[12]+4*j+2)[0]for j in range(h[3])]
        require(sorted(sites)==trial['MZ_sites'],'book diagnostic MZ set')
        part=text.split('Publics by Name')[1].split('Publics by Value')[0]
        def public(name):
            rows=re.findall(r'(?im)^\s*([0-9a-f]{4}):([0-9a-f]{4})\s+'+re.escape(name)+r'\s*$',part)
            require(len(rows)==1,'book diagnostic public missing/ambiguous')
            return tuple(int(x,16)for x in rows[0])
        frame,edata=public('_edata');endframe,end=public('_end')
        require(endframe==frame and trial['CRTzero_range']==[edata,end],'book diagnostic clear bounds')
        zero=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa');at=trial['CRTzero_instruction_image']
        require(load[at:at+len(zero)]==zero,'book diagnostic CRT clear instruction')
        for name,size in zip(NAMES,SIZES):
            seg,off=public(name);at=seg*16+off
            require(seg==frame and edata<=off and off+size<=end and at>=len(load)
                and not any(at<=site<at+size for site in sites),'book actual allocation not wholly COMMON/CRT-cleared')
        # Re-evaluate the entire actual harness contribution at its real MAP,
        # including the uncredited trailing compiler byte and all raw fields.
        public_rows=re.findall(r'(?im)^\s*([0-9a-f]{4}):([0-9a-f]{4})\s+(?:Abs\s+)?(\S+)\s*$',part)
        publics={n:(int(seg,16),int(off,16))for seg,off,n in public_rows}
        main=read_omf(b(root+'MAIN.OBJ'));origin=public('_main');marker=public('_diagnostic_marker')
        placements={1:origin,2:marker,3:(frame,0),4:(frame,0)}
        code,fields=link_segment(main,1,placements,{1:frame},publics)
        actual_data,data_fields=link_segment(main,2,placements,{1:frame},publics)
        code_at=origin[0]*16+origin[1];data_at=marker[0]*16+marker[1]
        require(len(code)==308 and main.function_info('_main')['size']==307 and code[-1:]==b'\x90'
            and load[code_at:code_at+len(code)]==code and code.hex()==trial['complete_CODE']['hex']
            and fields==trial['complete_CODE']['fields']
            and not any(code_at<=site<code_at+len(code)for site in sites),'book complete diagnostic CODE/fields')
        require(actual_data==bytes.fromhex('7856')and load[data_at:data_at+2]==actual_data
            and actual_data.hex()==trial['diagnostic_DATA']['hex']and data_fields==trial['diagnostic_DATA']['fields']
            and not any(data_at<=site<data_at+2 for site in sites),'book complete diagnostic DATA/fields')
    return constraints,proof


def build_input(item,project,target,output,*,compiler_fn=None):
    validate_item(item);project=Path(project).resolve();output=Path(output).resolve()
    source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'book source pin mismatch')
    compiled=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
    require(source.read_bytes()==before and compiled.source_sha256==SOURCE_SHA and compiled.compiler=='msc500'
        and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'
        and compiled.toolchain_manifest_sha256==MANIFEST_SHA,'book fresh compiler provenance')
    definitions=validate_object(compiled.object_bytes)
    constraints,proof=validate_evidence(project,item['evidence'],target)
    require(compiled.tool_hashes==proof['compiles']['SCALARS']['tool_hashes']
        and list(compiled.command)==proof['compiles']['SCALARS']['command'],'book fresh compiler tools/command pins')
    output.mkdir(parents=True,exist_ok=True);artifact=output/'book-state-common.obj';artifact.write_bytes(compiled.object_bytes)
    provenance=dataclasses.asdict(compiled);provenance.pop('object_bytes')
    return {'id':item['id'],'source':SOURCE,'object':str(artifact),'object_sha256':sha(compiled.object_bytes),
        'definitions':definitions,'allocation_bytes':22,'initialized_bytes':0,'matching_credit':0,
        'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,
        'allocation_profile':'seven_ints_and_Move8','authored_C_function_credit':0}
