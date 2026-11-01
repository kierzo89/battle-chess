"""Closed seventeen native int COMMON providers; source-only allocation, zero byte credit.

No original BSS order/MAP is imposed. Existing source-input profiles are unchanged.
"""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
BACKEND='msc500-near-common-ui-words-v1'
SOURCE='src/link/ui_word_state.c'
SOURCE_SHA='49d7c139255461b18ae739e0204a9710eacd3a96d14d0d923fb9ccc6f77d1fca'
OBJECT_SHA='1767aaf376b8d354c6e4c172c74a70da3a2bc7e65c8cee647f808051656da8cb'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOL_HASHES={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
PINS={'layout': {'path': 'build/ui-word-common-followup/proof.json', 'sha256': '9927885acccf2a4489334aa5f1c745ffb938a65a787fdda4e2b5389507a5ef99'}, 'native_review': {'path': 'build/ui-word-common-followup/native-type-review.json', 'sha256': 'd9d79226001bf1e5fd276b97a2b0256038323fff713bbd6c304c5b03d52795b0'}, 'crt': {'path': 'evidence/rea_crt_startup_500.json', 'sha256': 'f1ef14871734df318dcf05a9ea366706a46bf2484a5623678271df7cf612d1ad'}, 'native_0': {'path': 'build/restore-region-58b0/rea-native.json', 'sha256': '347b087417bf6619e9ea96bc35e67221dc8824c46e60d240b96b510479b1e27b'}, 'native_1': {'path': 'evidence/rea_pen_move_5b3d.json', 'sha256': '89b8b2731ce69436806ccb6c6fe2728529aee7b4672879bf45cb40ce70ff2bb0'}, 'native_2': {'path': 'evidence/rea_menu_row_527e.json', 'sha256': 'f91c3bc993a48cb06fd235e321a771c6309c26fabbdea64913ee88458e097372'}, 'native_3': {'path': 'evidence/rea_menu_next_512d.json', 'sha256': 'd2c6ca48399c99ee2e35136cc9698e0f686338070683162f22cc9bc8cda205b5'}, 'native_4': {'path': 'evidence/rea_graphics_41a8.json', 'sha256': '88651f91cee4031fb555b54d5f22ba6be4d33b633526b4987ff99999a0aacd1c'}, 'native_5': {'path': 'evidence/rea_main_policy_expanded_0010.json', 'sha256': '493f565a268acefd82de650088e78ec748fcc1437d2ec45975e3631f6e672a75'}, 'native_6': {'path': 'evidence/rea_region_next_5ebc.json', 'sha256': 'ce2c74650577395d2590089b555c2f691fba96d125897db29d9f5fb0fa84bb8e'}, 'native_7': {'path': 'evidence/rea_fill_neighbor_5a7c.json', 'sha256': '9c4f97b1f4663b071fa11c0440ef44bde1a6977c72af3903b88732b98a4e0750'}}
NATIVE_SPECS={'native_0': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x158b0'}, 'operation': 'analyze_function', 'evidence_id': 'ev_993afd93dbd193b958f0a9abb4f8bf85765135a0092f22a9e39bf1cf475f5752'}, 'native_1': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x15b3d'}, 'operation': 'analyze_function', 'evidence_id': 'ev_e6f4964093bcd6935476058173cb18f9b83b95c105322ee81449deb3acd8a907'}, 'native_2': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x1527e'}, 'operation': 'analyze_function', 'evidence_id': 'ev_64ea90a0a15e50b31cbe6843b70325fd7f1b0263d1cba004f9b5f637cb163ad2'}, 'native_3': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x1512d'}, 'operation': 'analyze_function', 'evidence_id': 'ev_44790ecb53c1c91892e9bf60d96df835d977a6109fedca518f97e7b601730dc6'}, 'native_4': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x141a8'}, 'operation': 'analyze_function', 'evidence_id': 'ev_01c6ef4526369b5c6b77942853025b8a0aa11105b900c630e1fc8903ba44ba82'}, 'native_5': {'subject_sha256': 'faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02', 'parameters': {'procedure': '0x10010'}, 'operation': 'analyze_function', 'evidence_id': 'ev_d4f22f7eebbf87428e91be31b11888c9234e523e4d1ee2a7a34054d5efcfb7d7'}, 'native_6': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x15ebc'}, 'operation': 'analyze_function', 'evidence_id': 'ev_45db873825adcdde024a171ef481e3c98eaa50c714e2a9467ffecb6429756fa0'}, 'native_7': {'subject_sha256': 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd', 'parameters': {'procedure': '0x15a7c'}, 'operation': 'analyze_function', 'evidence_id': 'ev_a77bb474fca474f7980f13908c737df6f21bdca4a7f160d06281210e7d9760d7'}}
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_dirty_left', '_dirty_right', '_dirty_top', '_dirty_bottom', '_pen_x', '_pen_y', '_menu_x', '_menu_y', '_menu_columns', '_height', '_border', '_motion_x', '_motion_y', '_stride', '_region_left', '_region_right', '_region_width']
OFFSETS=[37422, 37732, 37752, 36104, 36134, 36138, 36312, 36316, 36306, 36308, 37704, 37730, 37750, 37746, 45242, 38468, 45272]
FIXUPS=[(279, 18), (258, 17), (238, 16), (223, 15), (206, 14), (189, 13), (174, 12), (159, 11), (138, 10), (123, 9), (108, 8), (94, 7), (80, 6), (59, 5), (41, 4), (21, 3), (2, 2)]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
PROFILE_DIGEST='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
def require(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,path):
 p=(Path(project)/path).resolve();require(p.is_relative_to(Path(project).resolve()),'ui-word input path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown ui-word allocation fields')
 require(item['id']=='ui-word-state-common'and item['backend']==BACKEND and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['compiler']=='msc500'and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed ui-word source/profile')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES],'incomplete seventeen-word COMMON selection')
 require(item['evidence']==PINS,'ui-word evidence set/identity changed')
def validate_object(raw):
 o=read_omf(raw)
 require(not o.publics and not o.procedures,'ui-word COMMON defines PUBLIC/function')
 expected=[('_TEXT','CODE',0,0x48),('_DATA','DATA',0,0x48),('CONST','CONST',0,0x48),('_BSS','BSS',0,0x48),('$$SYMBOLS','DEBSYM',298,0x20),('$$TYPES','DEBTYP',0,0x20)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'ui-word loaded/debug allocation changed')
 require(not any(s.unsupported_data for s in o.segments.values()),'ui-word iterated data forbidden')
 require(all(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a}for k,_,_ in o.records),'unreviewed ui-word OMF record')
 definitions=[]
 for kind,_,payload in o.records:
  if kind==0xb0:
   c=_Cursor(payload)
   while c:
    name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte()
    require(datatype==0x62 and size==2 and typ==0x81,'ui-word requires native signed-int near COMMON2')
    definitions.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
  elif kind==0x88:require(payload in (bytes.fromhex('009d30734f'),bytes.fromhex('00a1014356'),bytes.fromhex('00a201')),'unreviewed ui-word linker directive')
  elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'ui-word DGROUP changed')
  elif kind==0x8a:require(payload==b'\0','ui-word allocation has entrypoint')
 require([x['symbol']for x in definitions]==NAMES,'ui-word missing/extra/duplicate/reordered COMMON')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'ui-word external set/order changed')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'ui-word initialized nondebug data')
 require(len(o.fixups)==17,'ui-word debug fixup count changed')
 for f,(off,target)in zip(o.fixups,FIXUPS):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,off,4,3,True,(5,None),(2,target),None),'ui-word nondebug or changed CodeView field')
 require(sha(raw)==OBJECT_SHA,'complete reviewed ui-word OMF/CV object changed')
 return definitions

def validate_evidence(project,pins,target):
 require(pins==PINS,'ui-word evidence identity changed');payloads={}
 for key,pin in pins.items():
  data=local(project,pin['path']).read_bytes();require(sha(data)==pin['sha256'],'ui-word evidence pin mismatch');payloads[key]=json.loads(data)
 target=Path(target);require(sha(target.read_bytes())==ORIGINAL_SHA256,'ui-word original target changed');r=build_reference(target.read_bytes());image=r['image']
 ids=[]
 for key,spec in list(NATIVE_SPECS.items())+[('crt',{'subject_sha256':ORIGINAL_SHA256,'operation':'read_bytes','parameters':{'address':'0x1ea86','length':179},'evidence_id':payloads['native_review']['CRT_primary']['evidence_id']})]:
  e=payloads[key];p=e['analysis_profile']['parameters'];ids.append(e['evidence_id'])
  require(e['subject']['digest']['sha256']==spec['subject_sha256']and e['subject']['format']=='dos-mz'and e['subject']['architecture']=='x86'and e['provider']['id']=='ghidra'and e['analysis_profile']['digest']==PROFILE_DIGEST and p['loader']=='MzLoader'and p['language_id']=='x86:LE:16:Real Mode'and p['load_segment']=='0x1000'and p['address_coordinates']=='linear-byte-offset'and e['operation']==spec['operation']and e['parameters']==spec['parameters']and e['evidence_id']==spec['evidence_id'],'ui-word native subject/profile/operation changed')
 require(len(ids)==len(set(ids))==9,'ui-word duplicate/missing primary IDs')
 review=payloads['native_review'];layout=payloads['layout'];require(review['source_API_compatible']and not review['alias_or_definition_conflicts']and review['existing_canonical_plus_staged_COMMON_count']==57 and not set(NAMES).intersection(review['existing_COMMON_names']),'ui-word source/native identity conflict')
 require(layout['source_sha256']==SOURCE_SHA and layout['object_sha256']==OBJECT_SHA and layout['complete_object']['initialized_bytes']==0 and layout['matching_credit']==0,'ui-word source/model layout proof changed')
 require(len(review['names'])==17,'ui-word native selection changed');constraints=[]
 for name,off,row in zip(NAMES,OFFSETS,review['names']):
  require(row['symbol']==name and row['type']=='int'and row['size']==2 and row['native_DS']==hex(off)and row['file_backed_bytes']==0 and row['source_COMMON_already_supplied']is False and row['native_MAP_or_BSS_allocation_order_proven']is False,'ui-word native scalar model changed')
  assembly=payloads[row['primary_key']]['normalized_result']['assembly'];lines=[l for l in assembly if '['+hex(off)+']'in l];require(lines==row['all_direct_accesses_in_primary']and row['actual_WORD_accesses']and all(l in lines and 'byte ptr'not in l for l in row['actual_WORD_accesses']),'ui-word native WORD evidence changed')
  require(0x52cc<=off and off+2<=0xcbe0 and 0x5cc20+off>=len(image),'ui-word outside native CRT/nonfilebacked interval')
  constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+2),'inside_native_startup_clear':['0x52cc','0xcbe0'],'native_final_MAP_or_BSS_order_proven':False,'resolved':False})
 # Carrier main's border store is independently identical on the unchanged original prefix.
 require(image[0xbd:0xc3]==bytes.fromhex('c70648930100')and not any(0xbd<=x<0xc3 for x in r['relocations']),'ui-word original border WORD store changed')
 cr=payloads['crt']['normalized_result'];clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
 require(cr['complete']and cr['requested_bytes']==cr['returned_bytes']==179 and bytes.fromhex(cr['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaed+len(clear)]==clear,'ui-word full native CRT/clear bounds changed')
 return constraints

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'ui-word source pin mismatch');fn=compile_c if compiler_fn is None else compiler_fn
 # Actual fresh source compilation precedes original/native comparison access.
 c=fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.tool_hashes==TOOL_HASHES,'ui-word fresh compiler/source/tool provenance changed')
 definitions=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/'ui-word-state-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':34,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'seventeen_native_signed_int_UI_scalars','authored_C_function_credit':0,'diagnostic_LINK_or_CRT_execution_claim':False}
