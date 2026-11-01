"""Closed five-int/Move8 COMMON profile. Source-only, zero match credit."""
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
from side_history_profile_pins import PINS

BACKEND='msc500-near-common-side-history-v1'
SOURCE='src/link/side_history_state.c'
SOURCE_SHA='b3facd1c18b816973cc66531fe2b565206df4b8790fc8bddb4a8da7270126bb5'
OBJECT_SHA='f19d359ef5f142aa9cf3fe0f6dac5ad6062132a772b116ec53490aedc1df547f'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_temporary','_current_side','_history_move_counter','_history_index','_opponent','_selected_move']
SIZES=[2,2,2,2,2,8]
TYPES=[0x81]*5+[522]
OFFSETS=[0x57c8,0x9846,0x984c,0x9880,0xa836,0xb0ac]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}


def require(condition,message):
    if not condition:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()


def local(project,name):
    path=(Path(project)/name).resolve()
    require(path.is_relative_to(Path(project).resolve()),'side/history input path escapes project')
    return path


def validate_item(item):
    require(isinstance(item,dict)and set(item)==KEYS,'unknown side/history allocation fields')
    require(item['id']=='side-history-common'and item['backend']==BACKEND and item['source']==SOURCE
        and item['source_sha256']==SOURCE_SHA and item['compiler']=='msc500'and item['flags']==FLAGS
        and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed side/history source/profile')
    require(item['objects']==[{'symbol':n,'size':s,'storage':'near-common'}for n,s in zip(NAMES,SIZES)],
        'incomplete side/history COMMON selection')
    require(item['evidence']==PINS,'side/history evidence set/identity changed')


def validate_object(data):
    """Whole raw OMF, exact COMMON types and complete debug evidence."""
    obj=read_omf(data)
    require(not obj.publics and not obj.procedures,'side/history COMMON defines PUBLIC/function')
    expected=[('_TEXT','CODE',0,0x48),('_DATA','DATA',0,0x48),('CONST','CONST',0,0x48),
        ('_BSS','BSS',0,0x48),('$$SYMBOLS','DEBSYM',129,0x20),('$$TYPES','DEBTYP',177,0x20)]
    require([(s.name,s.class_name,s.length,s.attributes)for s in obj.segments.values()]==expected,
        'side/history COMMON loaded or debug allocation changed')
    require(not any(s.unsupported_data for s in obj.segments.values()),'side/history COMMON LIDATA forbidden')
    definitions=[]
    for kind,at,payload in obj.records:
        require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'side/history foreign OMF record')
        if kind==0xb0:
            c=_Cursor(payload)
            while c:
                name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte()
                require(datatype==0x62,'side/history must be near COMMON')
                definitions.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
        elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'side/history DGROUP changed')
        elif kind==0x8a:require(payload==b'\0','side/history entry point forbidden')
        elif kind==0x88:require(payload in [bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],
            'side/history linker directive changed')
    require([d['symbol']for d in definitions]==NAMES,'side/history COMMON names/count/order changed')
    require([d['size']for d in definitions]==SIZES,'side/history COMMON sizes changed')
    require([d['type_index']for d in definitions]==TYPES,'side/history signed-int/Move8 types changed')
    require(obj.externals==dict(enumerate(['__acrtused']+NAMES,1)),'side/history external/startup marker changed')
    require(all(seg in(5,6)for _,seg,_,_ in obj.data_writes),'side/history initialized bytes outside debug')
    require(len(obj.fixups)==6,'side/history debug fixup count changed')
    for f,(off,target)in zip(obj.fixups,[(109,7),(92,6),(70,5),(41,4),(20,3),(2,2)]):
        require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)
            ==(5,off,4,3,True,(5,None),(2,target),None),'side/history CodeView fixup changed')
    # Raw hash includes the entire complete CV union/struct definition, field
    # names/types/offsets, all record checksums/lengths and overlays/threads.
    require(sha(data)==OBJECT_SHA,'whole reviewed side/history COMMON object changed')
    return definitions


def validate_evidence(project,pins,target):
    require(pins==PINS,'side/history evidence set/identity changed')
    data={}
    for key,pin in pins.items():
        raw=local(project,pin['path']).read_bytes()
        require(sha(raw)==pin['sha256'],'side/history evidence pin mismatch: '+key);data[key]=raw
    proof=json.loads(data['layout']);review=json.loads(data['review'])
    require(proof['matching_credit']==0 and proof['game_executed']is False and proof['canonical_changed']is False
        and proof['source_only_generation_LINK_execution_before_target_comparison']is True,'side/history proof scope')
    require(review['matching_credit']==0 and review['root_pending_proofs_mutated']is False
        and review['defined_type_issues']==review['function_call_ABI_issues']==[], 'side/history review scope/types')
    require(proof['compiles']['SCALARS']['source_sha256']==SOURCE_SHA
        and proof['compiles']['SCALARS']['object_sha256']==OBJECT_SHA
        and sha(data['source_model'])==SOURCE_SHA and sha(data['object'])==OBJECT_SHA
        and sha(data['harness'])==proof['compiles']['MAIN']['source_sha256']
        and sha(data['main_object'])==proof['compiles']['MAIN']['object_sha256'],'side/history source/object identity')
    require(proof['linker_sha256']==sha(data['linker'])and proof['SLIBC_sha256']==sha(data['runtime'])
        and proof['LIBH_sha256']==sha(data['helper_library']),'side/history tool/runtime pins')
    target_bytes=Path(target).read_bytes();require(sha(target_bytes)==ORIGINAL_SHA256,'side/history original target pin')
    reference=build_reference(target_bytes);image=reference['image']
    crt=json.loads(data['crt']);profile=crt['analysis_profile']['parameters'];raw=crt['normalized_result']
    require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256
        and(profile['load_segment'],profile['language_id'],profile['target_format'])==('0x1000','x86:LE:16:Real Mode','dos-mz')
        and crt['parameters']=={'address':'0x1ea86','length':179},'side/history original CRT subject/profile/read')
    require(raw['complete']and raw['address']=='0x1ea86'and raw['requested_bytes']==raw['returned_bytes']==179
        and bytes.fromhex(raw['bytes_hex'])==image[0xea86:0xeb39],'side/history complete original CRT bytes')
    clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
    require(image[0xeaed:0xeaed+len(clear)]==clear,'side/history native CRT zero bounds')
    crtclaim=review['original_CRT_primary']
    require(crtclaim['evidence_id']==crt['evidence_id']and crtclaim['sha256']==pins['crt']['sha256']
        and crtclaim['clear_DS_exclusive']==['0x52cc','0xcbe0'],'side/history reviewed CRT primary binding')
    primary_by_path={pin['path']:json.loads(data[key])for key,pin in pins.items()if key.startswith('native_')}
    require(len(review['native_bindings'])==6 and len(proof['original_constraints'])==6,'side/history native view count')
    constraints=[]
    for name,offset,size,view,proposed in zip(NAMES,OFFSETS,SIZES,review['native_bindings'],proof['original_constraints']):
        require(view['symbol']==proposed['symbol']==name and view['DS']==proposed['native_DS']==hex(offset)
            and view['size']==proposed['size']==size and proposed['native_range_inclusive']==[hex(offset),hex(offset+size-1)],
            'side/history scalar extent identity')
        require(0x52cc<=offset and offset+size<=0xcbe0 and 0x5cc20+offset>=len(image)
            and proposed['original_allocated_MAP_proven']is False,'side/history storage not wholly uninitialized/CRT-cleared')
        require(view['native_access_fields'],'side/history native field proof missing')
        for access in view['native_access_fields']:
            e=primary_by_path.get(access['primary']);require(e is not None,'side/history native primary missing')
            p=e['analysis_profile']['parameters']
            require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['evidence_id']==access['evidence_id']
                and(p['load_segment'],p['language_id'],p['target_format'])==('0x1000','x86:LE:16:Real Mode','dos-mz'),
                'side/history native subject/profile/identity')
            at=access['image_field'];encoded=bytes.fromhex(access['encoded_hex'])
            require(len(encoded)==2 and int.from_bytes(encoded,'little')==offset and image[at:at+2]==encoded,
                'side/history original native operand mismatch')
        constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(offset),
            'end_exclusive':hex(offset+size),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False})
    expected_windows=[(0x905e,'a3c857'),(0x7d98,'c70646980000'),(0x8674,'ff064c98'),
        (0x7daa,'c7068098ffff'),(0x7d9e,'c70636a80100'),(0x864e,'bfacb0becacba5a5a5a5')]
    require([(int(w['image'],0),w['hex'])for w in review['native_width_windows']]==expected_windows,
        'side/history native width windows changed')
    for at,h in expected_windows:
        require(image[at:at+len(bytes.fromhex(h))]==bytes.fromhex(h),'side/history native WORD/Move8 access changed')
    require(len(proof['authentic_LINK_trials'])==2,'side/history two-order LINK proof missing')
    for i,trial in enumerate(proof['authentic_LINK_trials']):
        prefix=['SCALARS-MAIN','MAIN-SCALARS'][i];exe=data[prefix+'_exe']
        text=data[prefix+'_map'].decode('cp437').replace('\r\n','\n')
        require(trial['order']==prefix.split('-')and sha(exe)==trial['exe_sha256']and text==trial['MAP']
            and trial['execution_exit_zero']and not trial['original_or_reference_read_or_mounted']
            and data[prefix+'_pass'].strip()==b'passed','side/history retained LINK/runtime proof identity')
        h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1]or 512)==len(exe),'side/history diagnostic MZ size')
        load=exe[h[4]*16:];sites=[struct.unpack_from('<H',exe,h[12]+4*j)[0]+16*struct.unpack_from('<H',exe,h[12]+4*j+2)[0]for j in range(h[3])]
        require(sorted(sites)==trial['MZ_sites'],'side/history diagnostic MZ set')
        part=text.split('Publics by Name')[1].split('Publics by Value')[0]
        def public(name):
            rows=re.findall(r'(?im)^\s*([0-9a-f]{4}):([0-9a-f]{4})\s+'+re.escape(name)+r'\s*$',part)
            require(len(rows)==1,'side/history diagnostic public missing/ambiguous')
            return tuple(int(x,16)for x in rows[0])
        frame,edata=public('_edata');endframe,end=public('_end')
        require(endframe==frame and trial['CRTzero_range']==[edata,end],'side/history diagnostic clear bounds')
        zero=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa');at=trial['CRTzero_instruction_image']
        require(load[at:at+len(zero)]==zero,'side/history diagnostic CRT clear instruction')
        for name,size in zip(NAMES,SIZES):
            seg,off=public(name);at=seg*16+off
            require(seg==frame and edata<=off and off+size<=end and at>=len(load)
                and not any(at<=site<at+size for site in sites),'side/history actual allocation not wholly COMMON/CRT-cleared')
        # Re-evaluate the entire actual harness contribution at its real MAP,
        # including the uncredited trailing compiler byte and all raw fields.
        public_rows=re.findall(r'(?im)^\s*([0-9a-f]{4}):([0-9a-f]{4})\s+(?:Abs\s+)?(\S+)\s*$',part)
        publics={n:(int(seg,16),int(off,16))for seg,off,n in public_rows}
        main=read_omf(data['main_object']);origin=public('_main');marker=public('_diagnostic_marker')
        placements={1:origin,2:marker,3:(frame,0),4:(frame,0)}
        code,fields=link_segment(main,1,placements,{1:frame},publics)
        actual_data,data_fields=link_segment(main,2,placements,{1:frame},publics)
        code_at=origin[0]*16+origin[1];data_at=marker[0]*16+marker[1]
        require(len(code)==264 and main.function_info('_main')['size']==263 and code[-1:]==b'\x90'
            and load[code_at:code_at+len(code)]==code and code.hex()==trial['complete_CODE']['hex']
            and fields==trial['complete_CODE']['fields']
            and not any(code_at<=site<code_at+len(code)for site in sites),'side/history complete diagnostic CODE/fields')
        require(actual_data==bytes.fromhex('7856')and load[data_at:data_at+2]==actual_data
            and actual_data.hex()==trial['diagnostic_DATA']['hex']and data_fields==trial['diagnostic_DATA']['fields']
            and not any(data_at<=site<data_at+2 for site in sites),'side/history complete diagnostic DATA/fields')
    return constraints,proof


def build_input(item,project,target,output,*,compiler_fn=None):
    validate_item(item);project=Path(project).resolve();output=Path(output).resolve()
    source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'side/history source pin mismatch')
    compiled=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500')
    require(source.read_bytes()==before and compiled.source_sha256==SOURCE_SHA and compiled.compiler=='msc500'
        and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'
        and compiled.toolchain_manifest_sha256==MANIFEST_SHA,'side/history fresh compiler provenance')
    definitions=validate_object(compiled.object_bytes)
    constraints,proof=validate_evidence(project,item['evidence'],target)
    require(compiled.tool_hashes==proof['compiles']['SCALARS']['tool_hashes']
        and list(compiled.command)==proof['compiles']['SCALARS']['command'],'side/history fresh compiler tools/command pins')
    output.mkdir(parents=True,exist_ok=True);artifact=output/'side-history-common.obj';artifact.write_bytes(compiled.object_bytes)
    provenance=dataclasses.asdict(compiled);provenance.pop('object_bytes')
    return {'id':item['id'],'source':SOURCE,'object':str(artifact),'object_sha256':sha(compiled.object_bytes),
        'definitions':definitions,'allocation_bytes':18,'initialized_bytes':0,'matching_credit':0,
        'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,
        'allocation_profile':'five_ints_and_Move8','authored_C_function_credit':0}
