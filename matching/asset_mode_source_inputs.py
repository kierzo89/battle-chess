"""Closed single signed-int mode_8176 COMMON2. No matched-byte credit.

This profile supplies a C allocation choice, not an original COMMON MAP/order.
The separate actors_ready client spelling is deliberately not defined/aliased.
"""
import dataclasses,hashlib,json,re
from pathlib import Path
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
BACKEND='msc500-near-common-asset-mode-v1'
SOURCE='src/link/asset_mode_state.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_mode_8176'];OFFSETS=[0x8176]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
SOURCE_SHA='8375918ef5384a2a1c2fb56cb9a5a84e65806effb54b80784e8580690d344aa7'
OBJECT_SHA='7264ae27af0748b3d75a06ab7044f55306b7d8fee49c8b0b3965365258cb520c'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
PINS={'review': {'path': 'build/mode8176-common-followup/native-type-review.json', 'sha256': 'aa190a5b9c97f7b56035e957054133e75ac037155a5528040af4532c08a72bca'}, 'compiler_controls': {'path': 'build/mode8176-common-followup/compiler-controls.json', 'sha256': 'fe3823f29287d1d8ea3e85d03ef9fd2194239d8832495e5a4ce20422c1b11303'}, 'native_inventory': {'path': 'build/storage-client-identity-175/survey.json', 'sha256': 'ac73e0c7bc36ecba1c57451cbc3560402d8e23fb1c9260b583d43ae3bac660d7'}, 'source_model': {'path': 'build/mode8176-common-followup/positive.c', 'sha256': '8375918ef5384a2a1c2fb56cb9a5a84e65806effb54b80784e8580690d344aa7'}, 'object': {'path': 'build/mode8176-common-followup/positive.obj', 'sha256': '7264ae27af0748b3d75a06ab7044f55306b7d8fee49c8b0b3965365258cb520c'}, 'crt': {'path': 'evidence/rea_crt_startup_500.json', 'sha256': 'f1ef14871734df318dcf05a9ea366706a46bf2484a5623678271df7cf612d1ad'}, 'native_or_consumer_0': {'path': 'build/poll-input-8aaa/rea-native.json', 'sha256': '714cbb8607a847da7421076607d22165b5026ca1ec8c19ce6b0945a957457e31'}, 'native_or_consumer_1': {'path': 'evidence/rea_audio_next_c924.json', 'sha256': '5048455d5c0b96499a5a278ad7e8698790fc49c62c7ebe1e27a48951c2e0cb38'}, 'native_or_consumer_2': {'path': 'evidence/rea_frame_next_1872a.json', 'sha256': '7062c5c746a77a1a1b68542fbbc18d11952168498772ba4b7aaf09d3155fbdeb'}, 'native_or_consumer_3': {'path': 'evidence/rea_init_display_7bc2.json', 'sha256': 'd939698f83c3f9e1cbb06f358986167b7946c9e1a52a4088d138dfbdf8c2fddf'}, 'native_or_consumer_4': {'path': 'evidence/rea_moves_next_c868.json', 'sha256': 'fc1362b53dd521cb51d558cbb96522019b8f4ae92edac4f35719845283c815b2'}, 'native_or_consumer_5': {'path': 'evidence/rea_ui_92ab.json', 'sha256': '6a34ad4d748e6a0b3bd07b8f77ab158512fcc4fd8b7ed06bd970de9dcfbd30a8'}, 'native_or_consumer_6': {'path': 'evidence/rea_ui_931c.json', 'sha256': '02d48d4b30e0a2860f554ea6a0f67356cf9ba3127d60de8e7920c551caf6554c'}, 'native_or_consumer_7': {'path': 'build/mode8176-common-followup/reviewed-consumers/asset_dispatch_file_context_match.c', 'sha256': '22a2da3cddcb5792b20d03a505a288ec4b40c32e483b82f524c4da651a883319'}, 'native_or_consumer_8': {'path': 'build/mode8176-common-followup/reviewed-consumers/clock_command_context_match.c', 'sha256': '4d0844ddf3539b953a5771be3d88ded48fd3acce62f6b11325c5017a2e2c4068'}, 'native_or_consumer_9': {'path': 'build/mode8176-common-followup/reviewed-consumers/display_history_flow_match.c', 'sha256': 'b04915b734f5451a6fb341fa374fb7e84b96fa5fe69dc21a97e953d3eaa71a14'}, 'native_or_consumer_10': {'path': 'build/mode8176-common-followup/reviewed-consumers/editor_state_flow_match.c', 'sha256': '088e27b34ed96ed288821dac6f2dfe1f3e70b7794f60c32063b890cd17849391'}, 'native_or_consumer_11': {'path': 'build/mode8176-common-followup/reviewed-consumers/poll_input_match.c', 'sha256': 'b41f7ad1baa6cbea3f3d0aa361a0d6906a4dfcb8f7a5c2b6a056c9456d7364cd'}, 'all_selected_audit': {'path': 'build/mode8176-common-followup/all-selected-source-audit.json', 'sha256': 'a9e19e7c5b0a90f80fee312d999e6581081dc72b33a59f7dd4e34bacc6cd2fb0'}, 'client_object_0': {'path': 'build/coherent448-canonical-validation/fresh-output/objects/msc500-088e27b34ed96ed2-a24fc804.obj', 'sha256': '63c7d22a264dca1fce4f7a61bc51d5143da8dc51ccfaaa230b68f2e8b0d5f6ba'}, 'client_object_1': {'path': 'build/coherent448-canonical-validation/fresh-output/objects/msc500-22a2da3cddcb5792-f66d0e09.obj', 'sha256': '5e9395b8b7e6fc442b0a55ace0d0858b4487cadcf6944f1faa0e44990573f18f'}, 'client_object_2': {'path': 'build/coherent448-canonical-validation/fresh-output/objects/msc500-4d0844ddf3539b95-a24fc804.obj', 'sha256': '628a17b387a949fc6c4b10ed720a6fb760271493a287fcdcd405e91b6541563a'}, 'client_object_3': {'path': 'build/coherent448-canonical-validation/fresh-output/objects/msc500-b04915b734f5451a-a24fc804.obj', 'sha256': '5da4743cb4a8a0c8c1aeea2805a5e99bf0f95296fdcf360aeecc8394308752e5'}, 'client_object_4': {'path': 'build/coherent448-canonical-validation/fresh-output/objects/msc500-b41f7ad1baa6cbea-a24fc804.obj', 'sha256': 'b6bca277f9fc1a3b0e6ea5a32516d5fe8912d642be7da2dfff1d810a5d175f39'}}
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,name):
 require(isinstance(name,str)and not Path(name).is_absolute(),'asset-mode relative path required')
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'asset-mode path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'asset-mode fields')
 require((item['id'],item['backend'],item['compiler'],item['source'],item['source_sha256'],item['flags'],item['toolchain_manifest_sha256'])==('asset-mode-common',BACKEND,'msc500',SOURCE,SOURCE_SHA,FLAGS,MANIFEST_SHA),'asset-mode closed source/profile')
 require(item['objects']==[{'symbol':'_mode_8176','size':2,'storage':'near-common'}],'asset-mode exact single WORD selection')
 require(item['evidence']==PINS,'asset-mode evidence selection')
def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'asset-mode PUBLIC/function forbidden')
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_TEXT','CODE',0,72,False),('_DATA','DATA',0,72,False),('CONST','CONST',0,72,False),('_BSS','BSS',0,72,False),('$$SYMBOLS','DEBSYM',18,32,False),('$$TYPES','DEBTYP',0,32,False)],'asset-mode whole loaded/debug allocation')
 defs=[];count=0
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'asset-mode foreign OMF record')
  if kind==0xb0:
   count+=1;c=_Cursor(p)
   while c:defs.append({'symbol':c.name(),'type_index':c.index(),'datatype':c.byte(),'size':c.byte()})
  elif kind==0x80:require(p==b'\x09C:\\UNIT.C','asset-mode input filename')
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'asset-mode DGROUP')
  elif kind==0x8a:require(p==b'\0','asset-mode entry point')
  elif kind==0x88:require(p in[bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],'asset-mode directive')
 require(count==1 and defs==[{'symbol':'_mode_8176','type_index':0x81,'datatype':0x62,'size':2}],'asset-mode exact near signed-int COMDEF2')
 require(o.externals=={1:'__acrtused',2:'_mode_8176'},'asset-mode external/marker')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'asset-mode initialized nondebug bytes')
 require(len(o.fixups)==1,'asset-mode debug fixup count');f=o.fixups[0]
 require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'asset-mode exact CV fixup')
 require(sha(data)==OBJECT_SHA,'asset-mode whole OMF/type/source identity');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'asset-mode evidence identity');payload={}
 for k,row in pins.items():
  payload[k]=local(project,row['path']).read_bytes();require(sha(payload[k])==row['sha256'],'asset-mode evidence pin '+k)
 review=json.loads(payload['review']);audit=json.loads(payload['all_selected_audit']);require(audit['no_existing_mode_or_actors_definition']and audit['no_source_type_coercions']and audit['matching_qualified_declarations']==review['selected_source_declarations'],'asset-mode all selected declaration/definition audit');proof=json.loads(payload['compiler_controls']);sc=proof['compiles']['positive'];require(sc['source_sha256']==SOURCE_SHA and sc['object_sha256']==OBJECT_SHA and sha(payload['source_model'])==SOURCE_SHA and validate_object(payload['object']),'asset-mode source/object proof')
 require(proof['guarded_source_tool_scratch_only']and proof['target_read_after_generation_only']and len(proof['blocked_generation_reads'])==18,'asset-mode target-free generation proof')
 require(review['native_range']==[0x8176,0x8178]and review['native_minimum_consumed_bytes']==2 and review['proposed_complete_C_scalar_bytes']==2 and review['definition_conflicts']==[]and review['source_allocation_only']and review['matching_credit']==0 and not review['canonical_changes']and not review['original_MAP_or_COMMON_order_proven'],'asset-mode native/credit scope')
 require(review['same_native_anchor_spellings']==['_actors_ready','_mode_8176']and review['runtime_CODE_count']==9 and review['mode_name_CODE_count']==4 and review['actors_name_CODE_count']==5,'asset-mode exact client spellings/counts')
 original=Path(target).read_bytes();require(sha(original)==ORIGINAL_SHA256,'asset-mode original target');image=build_reference(original)['image']
 # Every actual runtime field is corroborated by its exact raw source object and
 # original native bytes; the 16bit operand is not itself a storage-size proof.
 ids=set();objects={};primary_by_path={}
 for key,row in pins.items():
  if key.startswith('client_object_'):objects[row['path']]=read_omf(payload[key])
  if row['path'].endswith('.json'):
   e=json.loads(payload[key])
   if e.get('operation')=='analyze_function':primary_by_path[row['path']]=e
 for ref in review['actual_runtime_CODE_fields']:
  f=ref['runtime_field'];o=objects[ref['object']];raw=[v for v in o.fixups if v.segment==f['segment']and v.offset==f['object_offset']];require(len(raw)==1,'asset-mode raw client field unique');raw=raw[0]
  require(o.segments[raw.segment].class_name=='CODE'and raw.raw.hex()==ref['raw_FIXUPP']and raw.target==(2,f['target_index'])and o.externals[raw.target[1]]==ref['symbol']and raw.width==2 and raw.location_type==1 and raw.segment_relative and f['target_offset']==0x8176 and f['mode']=='segment_relative_dgroup'and image[f['image_offset']:f['image_offset']+2]==b'\x76\x81','asset-mode exact runtime field/native DS operand')
  e=primary_by_path[ref['native_primary']['path']];profile=e['analysis_profile'];require(e['evidence_id']==ref['native_primary']['evidence_id']and e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['subject']['format']=='dos-mz'and e['subject']['architecture']=='x86'and profile['provider']['id']=='ghidra'and profile['digest']=='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'and profile['parameters']['loader']=='MzLoader'and profile['parameters']['load_segment']=='0x1000'and profile['parameters']['address_coordinates']=='linear-byte-offset'and profile['parameters']['language_id']=='x86:LE:16:Real Mode'and ref['native_instruction']in e['normalized_result']['assembly'],'asset-mode primary target/profile/instruction')
  require(all(d['type']=='int'and d['storage']=='extern'for d in ref['actual_VarDecls']),'asset-mode actual client signed-int type')
 require(any(ref['symbol']=='_mode_8176'and ref['native_consumed_memory_bytes']==2 and 'MOV word ptr [0x8176], CX'in ref['native_instruction']for ref in review['actual_runtime_CODE_fields']),'asset-mode independent consumed WORD proof')
 crt=json.loads(payload['crt']);r=crt['normalized_result'];require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and crt['parameters']=={'address':'0x1ea86','length':179}and r['complete']and bytes.fromhex(r['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaf9]==bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa'),'asset-mode native CRT clear')
 require(0x52cc<=0x8176<0x8178<=0xcbe0 and 0x5cc20+0x8176>=len(image),'asset-mode nonfilebacked CRT storage')
 return [{'symbol':'_mode_8176','dgroup_segment':'0x5cc2','dgroup_offset':'0x8176','end_exclusive':'0x8178','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'original_TU_or_larger_owner_unknown':True}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'asset-mode source pin')
 fn=compile_c if compiler_fn is None else compiler_fn
 # No original/native/evidence read until fresh source compilation completes.
 c=fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.tool_hashes==TOOLS,'asset-mode fresh tool/source provenance')
 defs=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/'asset-mode-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':defs,'allocation_bytes':2,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'single_signed_int_asset_mode','authored_C_function_credit':0,'actors_ready_alias_definition':False}
