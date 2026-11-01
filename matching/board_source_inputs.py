"""Closed minimum meaningful board COMMON provider; no file/image/function credit.
120 cells is an observed minimum, not a historical source-capacity claim.
"""
import dataclasses,hashlib,json,re,struct
from pathlib import Path
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
BACKEND='msc500-near-common-board-minimum-v1'
SOURCE='src/link/board_storage.c'
COHERENT_CONSUMER='src/board_turn_context_match.c'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_board']
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
SOURCE_SHA='54ea1b36f85a66c7bc586c30862006ca11ed7709f1575251759d60ecfdfabc32'
OBJECT_SHA='b9770aaf9fc0effc46340f0ad329c1635d46ec17db1973c014f35e6ac5a058f0'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOLS={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
COHERENT_SOURCE_SHA='b89843a356eeb6002f6d30eb16a7ed4ee6b810b1789a960545807f81e40d2714'
PINS={'native_proof': {'path': 'evidence/board-bss-native-source-control.json', 'sha256': '58666639991e8383a9739d3aab73dd41a8a08f96e6b1f1d37fb2cb82f1e9fc89'}, 'link_proof': {'path': 'evidence/board-bss-authentic-link-control.json', 'sha256': '93a63a5f39c724922628b442236cf28d3ba70748353e2994828d1cf7aa819c08'}, 'definition': {'path': 'build/board-bss-link/definition-proposal.json', 'sha256': '1289e05fe1e62dd1223b2761889973811e8a3545089f5c6c2c9143c67294cc90'}, 'native_clear': {'path': 'evidence/rea_state_946f.json', 'sha256': 'aca787ff8e310d3119baa788eba129a4aa0914bafc93b01b8a784fbbfb4b8a5f'}, 'native_reset': {'path': 'evidence/rea_moves_reset_948c.json', 'sha256': 'c95d10ae1c3e2a0f325d510cc83f2af5e3e5da061029f212ad2f19a0a275faae'}, 'native_add': {'path': 'evidence/rea_add_piece_96af.json', 'sha256': '85739178b7e4c07b458acada3743822d0f82629502e623b18146807e0663523f'}, 'crt': {'path': 'evidence/rea_crt_startup_500.json', 'sha256': 'f1ef14871734df318dcf05a9ea366706a46bf2484a5623678271df7cf612d1ad'}, 'coherent_source': {'path': 'build/board-storage-identity-audit/coherent-board-turn.c', 'sha256': 'b89843a356eeb6002f6d30eb16a7ed4ee6b810b1789a960545807f81e40d2714'}, 'coherent_proof': {'path': 'build/board-storage-identity-audit/consumer-byte-proof.json', 'sha256': '62b9db0dbdf26b0e2460387093bf509e2783145b2e84d172e1e13bd021967ba2'}, 'coherent_freeze': {'path': 'build/board-storage-identity-audit/freeze-manifest.json', 'sha256': 'c714526d348fba0a256c9a2d045904618caf5f50d77bdc16c08231f360019933'}, 'BOARD-CLEAR-FILL-MAIN_BUILD.BAT': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/BUILD.BAT', 'sha256': 'e347e93cee7f647e140310cafac3e6da9a2cd1b62c9a825cbda7891f72b3fcc8'}, 'BOARD-CLEAR-FILL-MAIN_LINK.RSP': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/LINK.RSP', 'sha256': '4a737abc2114ef9c187bf4a2b82388c94b99d9e063a036f7df14127a5efdb7bc'}, 'BOARD-CLEAR-FILL-MAIN_LINK.LOG': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/LINK.LOG', 'sha256': '36b6176275d2dae3a9d1ca139f6532e8cec8ce20b68acc188e9e28b9f2cb5c74'}, 'BOARD-CLEAR-FILL-MAIN_RUN.LOG': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/RUN.LOG', 'sha256': '68c0efeffc417026cac18ab70a170165f6003edba5a5d370dd4d5a8f6924ecf7'}, 'BOARD-CLEAR-FILL-MAIN_PASS.TXT': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/PASS.TXT', 'sha256': 'c9d7a0682d275afe0a4d41a00294f56d6d82783a4de393ea188806cc8b3ee509'}, 'BOARD-CLEAR-FILL-MAIN_UNIT.EXE': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/UNIT.EXE', 'sha256': '82dbcf9803b4131bcb4d0c8df7e888296642631a0e5ba0779bdb8550a068b886'}, 'BOARD-CLEAR-FILL-MAIN_UNIT.MAP': {'path': 'build/board-bss-link/BOARD-CLEAR-FILL-MAIN/UNIT.MAP', 'sha256': '710ad6967365c0bd0ec30f24db39efa01e373416c52d3a808470b9b50f20c83c'}, 'MAIN-FILL-CLEAR-BOARD_BUILD.BAT': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/BUILD.BAT', 'sha256': 'e347e93cee7f647e140310cafac3e6da9a2cd1b62c9a825cbda7891f72b3fcc8'}, 'MAIN-FILL-CLEAR-BOARD_LINK.RSP': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/LINK.RSP', 'sha256': '1ddbd1fb1ad23b557006e84aa7d7f08f92179b2960265eb03387f346b04fa5b6'}, 'MAIN-FILL-CLEAR-BOARD_LINK.LOG': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/LINK.LOG', 'sha256': '1d7fa58e52521907a4fbe21a313b0db69073b4198c85aaa9e3109629fe739935'}, 'MAIN-FILL-CLEAR-BOARD_RUN.LOG': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/RUN.LOG', 'sha256': '68c0efeffc417026cac18ab70a170165f6003edba5a5d370dd4d5a8f6924ecf7'}, 'MAIN-FILL-CLEAR-BOARD_PASS.TXT': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/PASS.TXT', 'sha256': 'c9d7a0682d275afe0a4d41a00294f56d6d82783a4de393ea188806cc8b3ee509'}, 'MAIN-FILL-CLEAR-BOARD_UNIT.EXE': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/UNIT.EXE', 'sha256': '9bb1beabbf931d4f2437c22c4ccb6be362c4e46702438f2617da582cda8532dc'}, 'MAIN-FILL-CLEAR-BOARD_UNIT.MAP': {'path': 'build/board-bss-link/MAIN-FILL-CLEAR-BOARD/UNIT.MAP', 'sha256': 'f35415464ac2b2983d0c12943b52d0d4a209b8e8c257a736fb083682229ce608'}}
def require(v,m):
 if not v:raise ValueError(m)
def sha(v):return hashlib.sha256(v).hexdigest()
def local(project,name):
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'board COMMON path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'board COMMON unknown fields')
 require(item['id']=='board-minimum-common'and item['backend']==BACKEND and item['compiler']=='msc500'and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'board COMMON source/profile')
 require(item['objects']==[{'symbol':'_board','size':480,'storage':'near-common'}],'board COMMON minimum480 selection')
 require(item['evidence']==PINS,'board COMMON evidence selection')
def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'board COMMON PUBLIC/function')
 expected=[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',14,32),('$$TYPES','DEBTYP',83,32)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'board COMMON loaded/debug allocation')
 require(not any(s.unsupported_data for s in o.segments.values()),'board COMMON LIDATA/reservation')
 defs=[]
 for kind,at,p in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'board COMMON foreign record')
  if kind==0xb0:
   require(p==bytes.fromhex('065f626f61726482076281e001'),'board COMMON exact COMDEF480/array type207')
   c=_Cursor(p);n,t,d,leaf,size=c.name(),c.index(),c.byte(),c.byte(),c.word();c.finish();require((n,t,d,leaf,size)==('_board',0x207,0x62,0x81,480),'board COMMON typed minimum480')
   defs.append({'symbol':n,'size':size,'datatype':d,'type_index':t})
  elif kind==0x9a:require(p==bytes.fromhex('02ff03ff04ff02'),'board COMMON DGROUP')
  elif kind==0x8a:require(p==b'\0','board COMMON entry point')
  elif kind==0x88:require(p in[bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],'board COMMON directive')
 require(len(defs)==1 and o.externals=={1:'__acrtused',2:'_board'},'board COMMON extra/missing definition/external')
 require(all(seg in[5,6]for _,seg,_,_ in o.data_writes),'board COMMON initialized loaded bytes')
 require(len(o.fixups)==1,'board COMMON exact debug field count')
 f=o.fixups[0];require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'board COMMON exact debug field')
 require(o.segments[5].chunks==[(0,bytes.fromhex('0d0500000000070205626f617264'))],'board COMMON complete CodeView symbol')
 require(o.segments[6].chunks==[(0,bytes.fromhex('010100800101008001010080010c00792003830402830502820069010a007f838400838400838100011a007f82046b696e64880082047369646588018205696e6465788802010100800107007885000f830302'))],'board COMMON complete typed Cell/array CodeView')
 require(sha(data)==OBJECT_SHA,'board COMMON whole genuine object identity');return defs

def validate_evidence(project,pins,target):
 require(pins==PINS,'board COMMON evidence identity');payload={k:local(project,r['path']).read_bytes()for k,r in pins.items()}
 for k,b in payload.items():require(sha(b)==pins[k]['sha256'],'board COMMON evidence pin '+k)
 require(sha(local(project,COHERENT_CONSUMER).read_bytes())==COHERENT_SOURCE_SHA and sha(payload['coherent_source'])==COHERENT_SOURCE_SHA,'board COMMON requires coherent consumer Cell view')
 cp=json.loads(payload['coherent_proof']);require(cp['whole_CODE756_original_coherent_equal']and cp['all120_fields_original_coherent_equal']and cp['all5_CV_original_coherent_equal']and cp['existing_native_MZ1_preserved']and cp['all5_ordinary_production_pass']and cp['current_credit']==0,'board COMMON coherent consumer proof')
 native=json.loads(payload['native_proof']);definition=json.loads(payload['definition']);link=json.loads(payload['link_proof'])
 require(definition['minimum_count']==120 and definition['minimum_consumed_bytes']==480 and definition['native_observed_DS_base']=='0xa8ba'and definition['native_minimum_end_exclusive']=='0xaa9a'and definition['matching_credit']==0,'board COMMON minimum constraint')
 require(native['native_last_index']==119 and native['native_last_index_field_DS_range']==['0xaa98','0xaa99']and native['native_clear480_DS_range']==['0xa8ba','0xaa99'],'board COMMON native extent')
 raw=Path(target).read_bytes();require(sha(raw)==ORIGINAL_SHA256,'board COMMON original target');ref=build_reference(raw);image=ref['image']
 for key,strings in [('native_clear',['0x1947a: MOV AX, 0x1e0','0x1947e: MOV AX, 0xa8ba']),('native_reset',['0x194a0: CMP word ptr [BP + -0x2], 0x77','0x194ad: MOV word ptr [BX + 0xa8bc], 0x10']),('native_add',['0x196be: SHL SI, CL','0x196d8: MOV byte ptr [SI + 0xa8ba], AL','0x196df: MOV byte ptr [SI + 0xa8bb], AL','0x196c0: MOV AX, word ptr [SI + 0xa8bc]'])]:
  e=json.loads(payload[key]);require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and all(s in e['normalized_result']['assembly']for s in strings),'board COMMON actual native scalar/stride/loop widths')
 crt=json.loads(payload['crt']);clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa');require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and bytes.fromhex(crt['normalized_result']['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaed+len(clear)]==clear and 0x52cc<=0xa8ba and 0xaa9a<=0xcbe0 and 0x5cc20+0xa8ba>=len(image),'board COMMON native CRT/uninitialized range')
 require(link['matching_credit']==0 and link['original_read_or_mounted']is False and len(link['trials'])==2 and link['compiler_objects']['board']['source_sha256']==SOURCE_SHA and link['compiler_objects']['board']['object_sha256']==OBJECT_SHA,'board COMMON authentic source proof')
 for trial,order in zip(link['trials'],[['BOARD','CLEAR','FILL','MAIN'],['MAIN','FILL','CLEAR','BOARD']]):
  prefix='-'.join(order);exe=payload[prefix+'_UNIT.EXE'];maptext=payload[prefix+'_UNIT.MAP'].decode('cp437').replace('\r\n','\n')
  require(trial['order']==order and trial['command']=='T:\\LINK /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP @LINK.RSP'and trial['ran_successfully']and not trial['original_target_read_or_mounted']and sha(exe)==trial['EXE_sha256']and maptext==trial['MAP']and payload[prefix+'_PASS.TXT'].strip()==b'passed'and 'error L'not in payload[prefix+'_LINK.LOG'].decode('cp437'),'board COMMON retained authentic two-order executed proof')
  h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1] or 512)==len(exe),'board COMMON retained MZ size');load=exe[h[4]*16:];sites=sorted(struct.unpack_from('<H',exe,h[12]+4*i)[0]+16*struct.unpack_from('<H',exe,h[12]+4*i+2)[0]for i in range(h[3]));require(sites==trial['MZ_sites'],'board COMMON retained MZ set')
  part=maptext.split('Publics by Name')[1].split('Publics by Value')[0];pairs=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',part,re.M);pubs={n:[int(s,16),int(o,16)]for s,o,n in pairs};require(len(pubs)==len(pairs)and pubs==trial['publics'],'board COMMON retained actual MAP')
  frame,board=pubs['_board'];ef,start=pubs['_edata'];enf,end=pubs['_end'];require(frame==ef==enf and start<=board and board+480<=end and 16*frame+board>=len(load)and not any(16*frame+board<=s<16*frame+board+480 for s in sites),'board COMMON actual uninitialized allocation/CRT bounds')
  pattern=b'\xbf'+start.to_bytes(2,'little')+b'\xb9'+end.to_bytes(2,'little')+bytes.fromhex('2bcf33c0f3aa');at=trial['actual_CRT_zero_instruction_image_address'];require(load[at:at+len(pattern)]==pattern,'board COMMON actual CRT clear instruction')
 return [{'symbol':'_board','dgroup_segment':'0x5cc2','dgroup_offset':'0xa8ba','end_exclusive':'0xaa9a','inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False,'minimum_observed_bytes':480,'historical_capacity_proven':False}]

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'board COMMON source pin');fn=compile_c if compiler_fn is None else compiler_fn
 # Fresh source generation completes before native/evidence reads.
 c=fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.tool_hashes==TOOLS,'board COMMON fresh compiler provenance')
 definitions=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/'board-minimum-common.obj';p.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(p),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':480,'initialized_bytes':0,'matching_credit':0,'placement_proven':False,'original_map_constraints':constraints,'compiler':meta,'allocation_profile':'minimum_120_four_byte_board_cells','authored_C_function_credit':0,'historical_capacity_proven':False}
