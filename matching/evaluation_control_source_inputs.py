"""Closed thirteen native int COMMON providers; source-only allocation, zero byte credit.

No original BSS order/MAP is imposed. Existing source-input profiles are unchanged.
"""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
BACKEND='msc500-near-common-evaluation-controls-v1'
SOURCE='src/link/evaluation_control_state.c'
SOURCE_SHA='7ff96dab9d53e1e81e5e7e8ffb43b74e24a35698e34cf420469a69db1cf0484c'
OBJECT_SHA='effcc178dd6aa310f112c80c7195ee2505824c5beea422c8699d692fbfc5121f'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOL_HASHES={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
PINS={'layout': {'path': 'build/evaluation-control-common-followup/proof.json', 'sha256': 'f397f6f770f8fcd25b4d62206962ea3cd0a0374e14405ce6fad9178d498abea3'}, 'native_review': {'path': 'build/evaluation-control-common-followup/native-type-review.json', 'sha256': 'efb0509aa87bf5e764bb8ba7e4b7be68ed4246c9f3d871824d5c97b02128b0df'}, 'crt': {'path': 'evidence/rea_crt_startup_500.json', 'sha256': 'f1ef14871734df318dcf05a9ea366706a46bf2484a5623678271df7cf612d1ad'}, 'native_0': {'path': 'evidence/rea_full_evaluation_fe59.json', 'sha256': '79b6546c42242a8d0c1be9b232c735fbab0192d5cfb3fd04622010d54ef5fa37'}, 'native_1': {'path': 'evidence/rea_search_next_b9ba.json', 'sha256': '4440608b7af46e9a1a9d30b47b3b3057a1632d21affa322dc3ecac2d89bb26d7'}, 'native_2': {'path': 'evidence/rea_ui_92ab.json', 'sha256': '6a34ad4d748e6a0b3bd07b8f77ab158512fcc4fd8b7ed06bd970de9dcfbd30a8'}, 'native_3': {'path': 'evidence/rea_obtain_input_0254_original.json', 'sha256': 'c03e3645fafa8275ce00aea6f4e8e6c20fd6a7849c5a21a0eb8add9aee77ca86'}, 'native_4': {'path': 'evidence/rea_position_command_next_2301_original.json', 'sha256': 'ea2c68123200bde542c16833c346e5757239c70268b44c0f5ce2ece1e27cf921'}, 'native_5': {'path': 'evidence/rea-root-c9d0.json', 'sha256': '21d618821365f5f241f973db77bdc4efc9f41e020571261951eecece5954a87f'}, 'native_6': {'path': 'evidence/rea_menu_next_4e5d.json', 'sha256': '06eae1b987507622e8cf67d6e56a61ed53f513dd5a9bd1c9e02008734ccaba38'}, 'native_7': {'path': 'evidence/rea_advance_a4d4.json', 'sha256': '67f1d37eea790ee07f3b0235deed215dc761d8288dfa69cd399d73895a59b6b9'}}
NATIVE_SPECS={'native_0': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x1fe59'}, 'operation': 'analyze_function', 'evidence_id': 'ev_10c8a80db899ed31b9c1b4d3650d43e6ab3d32fde4ad91ecd70d50df1290e1ec'}, 'native_1': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x1b9ba'}, 'operation': 'analyze_function', 'evidence_id': 'ev_f6cb41e864b0d048eecc29633642a64c433e6406e7b845cdd26898be67d6eb10'}, 'native_2': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x192ab'}, 'operation': 'analyze_function', 'evidence_id': 'ev_e582531592b95ac35d56461e222a8f96c9cfbc766e51f0c3d6cf8390bbf64200'}, 'native_3': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x10254'}, 'operation': 'analyze_function', 'evidence_id': 'ev_fac4e34ca8097981a6ad7a7c4fef988d9f4b505c798515f1ec320d4b5f140abe'}, 'native_4': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x12301'}, 'operation': 'analyze_function', 'evidence_id': 'ev_e7a756d7ba9274a25152db743608b56bd0b6b7e62db18f64384c21fb0bea064d'}, 'native_5': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x1c9d0'}, 'operation': 'analyze_function', 'evidence_id': 'ev_d77fb5b578e8d2a21489b81d49f2b0c7590ed302e3ab78868d0aed529f064809'}, 'native_6': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x14e5d'}, 'operation': 'analyze_function', 'evidence_id': 'ev_6d537e6ead8dc789af9c41e0eab446713e304ec0f1cb09394979e5397bb4d3d5'}, 'native_7': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x1a4d4'}, 'operation': 'analyze_function', 'evidence_id': 'ev_1810a2a772f951e0d8a454c8e141e7631a5b2286597c9646e2743d30959c27e4'}}
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_pawn_material', '_phase', '_saved_history_index', '_mode_8188', '_material_balance', '_last_key_8dcc', '_total_material', '_endgame', '_previous_buttons_9888', '_asset_drive_count', '_asset_drive_fallback', '_menu_last', '_state_index']
OFFSETS=[22464, 33154, 33156, 33160, 36136, 36300, 45220, 45270, 39048, 39050, 22478, 45274, 43090]
FIXUPS=[(273, 14), (255, 13), (226, 12), (200, 11), (170, 10), (154, 9), (131, 8), (109, 7), (84, 6), (66, 5), (38, 4), (24, 3), (2, 2)]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
PROFILE_DIGEST='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
def require(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,path):
 p=(Path(project)/path).resolve();require(p.is_relative_to(Path(project).resolve()),'evaluation-control input path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown evaluation-control allocation fields')
 require(item['id']=='evaluation-control-common'and item['backend']==BACKEND and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['compiler']=='msc500'and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed evaluation-control source/profile')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES],'incomplete thirteen-word COMMON selection')
 require(item['evidence']==PINS,'evaluation-control evidence set/identity changed')
def validate_object(raw):
 o=read_omf(raw)
 require(not o.publics and not o.procedures,'evaluation-control COMMON defines PUBLIC/function')
 expected=[('_TEXT','CODE',0,0x48),('_DATA','DATA',0,0x48),('CONST','CONST',0,0x48),('_BSS','BSS',0,0x48),('$$SYMBOLS','DEBSYM',291,0x20),('$$TYPES','DEBTYP',0,0x20)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'evaluation-control loaded/debug allocation changed')
 require(not any(s.unsupported_data for s in o.segments.values()),'evaluation-control iterated data forbidden')
 require(all(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a}for k,_,_ in o.records),'unreviewed evaluation-control OMF record')
 definitions=[]
 for kind,_,payload in o.records:
  if kind==0xb0:
   c=_Cursor(payload)
   while c:
    name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte()
    require(datatype==0x62 and size==2 and typ==0x81,'evaluation-control requires native signed-int near COMMON2')
    definitions.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
  elif kind==0x88:require(payload in (bytes.fromhex('009d30734f'),bytes.fromhex('00a1014356'),bytes.fromhex('00a201')),'unreviewed evaluation-control linker directive')
  elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'evaluation-control DGROUP changed')
  elif kind==0x8a:require(payload==b'\0','evaluation-control allocation has entrypoint')
 require([x['symbol']for x in definitions]==NAMES,'evaluation-control missing/extra/duplicate/reordered COMMON')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'evaluation-control external set/order changed')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'evaluation-control initialized nondebug data')
 require(len(o.fixups)==13,'evaluation-control debug fixup count changed')
 for f,(off,target)in zip(o.fixups,FIXUPS):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,off,4,3,True,(5,None),(2,target),None),'evaluation-control nondebug or changed CodeView field')
 require(sha(raw)==OBJECT_SHA,'complete reviewed evaluation-control OMF/CV object changed')
 return definitions

def validate_evidence(project,pins,target):
 require(pins==PINS,'evaluation-control evidence identity changed');payloads={}
 for key,pin in pins.items():
  data=local(project,pin['path']).read_bytes();require(sha(data)==pin['sha256'],'evaluation-control evidence pin mismatch');payloads[key]=json.loads(data)
 target=Path(target);require(sha(target.read_bytes())==ORIGINAL_SHA256,'evaluation-control original target changed');r=build_reference(target.read_bytes());image=r['image']
 ids=[]
 for key,spec in list(NATIVE_SPECS.items())+[('crt',{'subject_sha256':ORIGINAL_SHA256,'operation':'read_bytes','parameters':{'address':'0x1ea86','length':179},'evidence_id':payloads['native_review']['CRT_primary']['evidence_id']})]:
  e=payloads[key];p=e['analysis_profile']['parameters'];ids.append(e['evidence_id'])
  require(e['subject']['digest']['sha256']==spec['subject_sha256']and e['subject']['format']=='dos-mz'and e['subject']['architecture']=='x86'and e['provider']['id']=='ghidra'and e['analysis_profile']['digest']==PROFILE_DIGEST and p['loader']=='MzLoader'and p['language_id']=='x86:LE:16:Real Mode'and p['load_segment']=='0x1000'and p['address_coordinates']=='linear-byte-offset'and e['operation']==spec['operation']and e['parameters']==spec['parameters']and e['evidence_id']==spec['evidence_id'],'evaluation-control native subject/profile/operation changed')
 require(len(ids)==len(set(ids))==9,'evaluation-control duplicate/missing primary IDs')
 review=payloads['native_review'];layout=payloads['layout'];require(review['source_API_compatible']and not review['alias_or_definition_conflicts']and review['existing_canonical_plus_staged_COMMON_count']==74 and not set(NAMES).intersection(review['existing_COMMON_names']),'evaluation-control source/native identity conflict')
 require(layout['source_sha256']==SOURCE_SHA and layout['object_sha256']==OBJECT_SHA and layout['complete_object']['initialized_bytes']==0 and layout['matching_credit']==0,'evaluation-control source/model layout proof changed')
 require(len(review['names'])==13,'evaluation-control native selection changed');constraints=[]
 require(len(review['existing_native_COMMON_ranges'])==74 and len({r['symbol']for r in review['existing_native_COMMON_ranges']})==74,'evaluation-control existing COMMON range inventory changed')
 for name,off,row in zip(NAMES,OFFSETS,review['names']):
  require(row['symbol']==name and row['type']=='int'and row['size']==2 and row['native_DS']==hex(off)and row['file_backed_bytes']==0 and row['source_COMMON_already_supplied']is False and row['native_MAP_or_BSS_allocation_order_proven']is False,'evaluation-control native scalar model changed')
  assembly=payloads[row['primary_key']]['normalized_result']['assembly'];lines=[l for l in assembly if '['+hex(off)+']'in l];require(lines==row['all_direct_accesses_in_primary']and row['actual_WORD_accesses']and all(l in lines and 'byte ptr'not in l for l in row['actual_WORD_accesses']),'evaluation-control native WORD evidence changed')
  require(not any(r['start']<off+2 and r['end']>off for r in review['existing_native_COMMON_ranges']),'evaluation-control overlaps existing COMMON physical extent')
  require(0x52cc<=off and off+2<=0xcbe0 and 0x5cc20+off>=len(image),'evaluation-control outside native CRT/nonfilebacked interval')
  constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+2),'inside_native_startup_clear':['0x52cc','0xcbe0'],'native_final_MAP_or_BSS_order_proven':False,'resolved':False})
 cr=payloads['crt']['normalized_result'];clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
 require(cr['complete']and cr['requested_bytes']==cr['returned_bytes']==179 and bytes.fromhex(cr['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaed+len(clear)]==clear,'evaluation-control full native CRT/clear bounds changed')
 return constraints

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'evaluation-control source pin mismatch');fn=compile_c if compiler_fn is None else compiler_fn
 # Actual fresh source compilation precedes original/native comparison access.
 c=fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.tool_hashes==TOOL_HASHES,'evaluation-control fresh compiler/source/tool provenance changed')
 definitions=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/'evaluation-control-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':26,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'thirteen_native_signed_int_evaluation_input_scalars','authored_C_function_credit':0,'diagnostic_LINK_or_CRT_execution_claim':False}
