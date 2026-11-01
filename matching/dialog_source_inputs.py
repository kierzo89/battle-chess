"""Closed two-int dialog COMMON input. No file/image/function matching credit."""
import dataclasses,hashlib,json,re,struct
from pathlib import Path
from msc import compile_c
from omf import read_omf,_Cursor
from library16 import link_segment
from reference import build_reference,ORIGINAL_SHA256
from dialog_profile_pins import PINS
BACKEND='msc500-near-common-dialog-v1'
SOURCE='src/link/dialog_state.c'
SOURCE_SHA='eda9cc81a5c17dbf2ee72301cbd65850fd9fe6bc72a5cca360de405a7669ef04'
OBJECT_SHA='81dd77153d4fb80e1e2a22203a68549a32d6ec1e3fb6784d72ef02b274f2d74b'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
FLAGS=['/AS','/Zl','/Zi'];NAMES=['_dialog_selected','_saved_name_count_52d4'];OFFSETS=[0x52d2,0x52d4]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
def require(v,msg):
 if not v:raise ValueError(msg)
def sha(v):return hashlib.sha256(v).hexdigest()
def local(project,name):
 p=(Path(project)/name).resolve();require(p.is_relative_to(Path(project).resolve()),'dialog input path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown dialog allocation fields')
 require(item['id']=='dialog-selection-common'and item['backend']==BACKEND and item['compiler']=='msc500'and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed dialog source/profile')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES],'incomplete dialog COMMON selection')
 require(item['evidence']==PINS,'dialog evidence selection changed')
def validate_object(data):
 o=read_omf(data);require(not o.publics and not o.procedures,'dialog COMMON PUBLIC/function forbidden')
 expected=[('_TEXT','CODE',0,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',54,32),('$$TYPES','DEBTYP',0,32)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'dialog loaded/debug allocation changed')
 require(not any(s.unsupported_data for s in o.segments.values()),'dialog COMMON reserved/LIDATA data forbidden')
 commons=[]
 for kind,at,payload in o.records:
  require(kind in {0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0xb0,0xa0,0x8a},'dialog foreign OMF record')
  if kind==0xb0:
   c=_Cursor(payload)
   while c:
    name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte();require((typ,datatype,size)==(0x81,0x62,2),'dialog requires near signed-int type81/datatype62/size2');commons.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
  elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'dialog DGROUP changed')
  elif kind==0x8a:require(payload==b'\0','dialog entry point forbidden')
  elif kind==0x88:require(payload in[bytes.fromhex(x)for x in('009d30734f','00a1014356','00a201')],'dialog linker directive changed')
 require([c['symbol']for c in commons]==NAMES,'dialog COMMON count/name/order changed')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'dialog external/marker changed')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'dialog initialized nondebug bytes')
 require(len(o.fixups)==2,'dialog debug fixup count changed')
 for f,(offset,target)in zip(o.fixups,[(26,3),(2,2)]):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,offset,4,3,True,(5,None),(2,target),None),'dialog exact CodeView field changed')
 require(sha(data)==OBJECT_SHA,'whole genuine dialog COMMON OMF changed');return commons

def validate_evidence(project,pins,target):
 require(pins==PINS,'dialog evidence set/identity changed');payloads={k:local(project,row['path']).read_bytes()for k,row in pins.items()}
 for k,data in payloads.items():require(sha(data)==pins[k]['sha256'],'dialog evidence pin mismatch: '+k)
 proof=json.loads(payloads['layout']);require(proof['matching_credit']==0 and proof['canonical_changed']is False and proof['game_executed']is False and proof['source_only_generation_LINK_execution_before_target_comparison']and proof['generation_target_reads_actively_forbidden']and proof['cross_TU_access_checked'],'dialog diagnostic scope changed')
 sc=proof['compiles']['SCALARS'];require(sc['source_sha256']==SOURCE_SHA and sc['object_sha256']==OBJECT_SHA and sha(payloads['source_model'])==SOURCE_SHA and sha(payloads['object'])==OBJECT_SHA,'dialog actual source/object identity')
 require(proof['COMMON_definitions']==[dict(x,record_offset=216,raw_record=bytes.fromhex('105f6469616c6f675f73656c656374656480816202165f73617665645f6e616d655f636f756e745f3532643480816202').hex())for x in validate_object(payloads['object'])],'dialog raw COMDEF proof changed')
 for key,start,size in [('native_setup',0x1d2cc,17),('native_count',0x1d2dd,136),('native_selected',0x1d66c,250),('native_count_read',0x1ced4,1016)]:
  e=json.loads(payloads[key]);p=e['analysis_profile']['parameters'];body=e['normalized_result']['procedure']['body']
  require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode'and p['target_format']=='dos-mz'and e['parameters']=={'procedure':hex(start)}and body['contains_entry']and not body['non_contiguous']and body['total_bytes']==body['span_bytes']==size and body['ranges']==[{'start':hex(start),'end':hex(start+size-1)}],'dialog native consumer identity/extent')
 target_bytes=Path(target).read_bytes();require(sha(target_bytes)==ORIGINAL_SHA256,'dialog original target pin');ref=build_reference(target_bytes);image=ref['image']
 for at,hexbytes in [(0xd2d6,'c706d252ffffc3'),(0xd35b,'893ed452'),(0xd673,'a1d252'),(0xd698,'8b16d252'),(0xd6ce,'f72ed252'),(0xd75e,'a3d252'),(0xd0cf,'a1d452')]:
  expected=bytes.fromhex(hexbytes);require(image[at:at+len(expected)]==expected,'dialog native scalar word field changed')
 crt=json.loads(payloads['crt']);p=crt['analysis_profile']['parameters'];raw=crt['normalized_result'];clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
 require(crt['subject']['digest']['sha256']==ORIGINAL_SHA256 and p['load_segment']=='0x1000'and p['language_id']=='x86:LE:16:Real Mode'and crt['parameters']=={'address':'0x1ea86','length':179}and raw['complete']and raw['requested_bytes']==raw['returned_bytes']==179 and bytes.fromhex(raw['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaed+len(clear)]==clear,'dialog complete native CRT179/clear range')
 require(len(proof['authentic_LINK_trials'])==2,'dialog requires two real object orders')
 main=read_omf(payloads['harness_object']);access=read_omf(payloads['access_object'])
 require(sha(payloads['harness_source'])==proof['compiles']['MAIN']['source_sha256']and sha(payloads['access_source'])==proof['compiles']['ACCESS']['source_sha256']and sha(payloads['harness_object'])==proof['compiles']['MAIN']['object_sha256']and sha(payloads['access_object'])==proof['compiles']['ACCESS']['object_sha256'],'dialog independent access/input provenance')
 for trial,order in zip(proof['authentic_LINK_trials'],[['SCALARS','ACCESS','MAIN'],['MAIN','ACCESS','SCALARS']]):
  prefix='-'.join(order);exe=payloads[prefix+'_exe'];maptext=payloads[prefix+'_map'].decode('cp437').replace('\r\n','\n')
  require(trial['order']==order and trial['command']=='T:\\LINK /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP @LINK.RSP'and trial['original_or_reference_read_or_mounted']is False and trial['execution_exit_zero']and payloads[prefix+'_pass'].strip()==b'passed'and 'error L'not in payloads[prefix+'_linklog'].decode('cp437')and sha(exe)==trial['exe_sha256']and maptext==trial['MAP'],'dialog authentic executed LINK proof')
  h=struct.unpack_from('<14H',exe);require(exe[:2]==b'MZ'and(h[2]-1)*512+(h[1] or 512)==len(exe),'dialog diagnostic MZ complete size');load=exe[h[4]*16:];sites=sorted(struct.unpack_from('<H',exe,h[12]+4*j+2)[0]*16+struct.unpack_from('<H',exe,h[12]+4*j)[0]for j in range(h[3]));require(sites==trial['MZ_sites'],'dialog diagnostic complete MZ set')
  part=maptext.split('Publics by Name')[1].split('Publics by Value')[0];pairs=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',part,re.M);pubs={n:[int(s,16),int(o,16)]for s,o,n in pairs};require(len(pubs)==len(pairs),'dialog ambiguous actual MAP publics')
  frame,edata=pubs['_edata'];endframe,end=pubs['_end'];require(frame==endframe and trial['CRTzero_range']==[edata,end],'dialog actual CRT clear bounds')
  zeros=b'\xbf'+struct.pack('<H',edata)+b'\xb9'+struct.pack('<H',end)+bytes.fromhex('2bcf33c0f3aa');at=trial['CRTzero_instruction_image'];require(load[at:at+len(zeros)]==zeros,'dialog actual CRT zero instruction')
  for name in NAMES:
   seg,off=pubs[name];where=seg*16+off;require(seg==frame and edata<=off and off+2<=end and where>=len(load)and not any(where<=s<where+2 for s in sites),'dialog actual COMMON not wholly uninitialized CRT storage')
  origins=[(main,pubs['_main'],'complete_CODE'),(access,pubs['_diagnostic_write_selected'],'independent_access_CODE')]
  for obj,origin,key in origins:
   placements={1:origin,2:pubs['_diagnostic_marker']if obj is main else[frame,0],3:[frame,0],4:[frame,0]};code,fields=link_segment(obj,1,placements,{1:frame},pubs);where=origin[0]*16+origin[1];require(load[where:where+len(code)]==code and trial[key]['hex']==code.hex()and trial[key]['size']==len(code)and trial[key]['fields']==fields and not any(where<=s<where+len(code)for s in sites),'dialog complete diagnostic source CODE including compiler tail')
  placements={1:pubs['_main'],2:pubs['_diagnostic_marker'],3:[frame,0],4:[frame,0]};data,fields=link_segment(main,2,placements,{1:frame},pubs);where=16*pubs['_diagnostic_marker'][0]+pubs['_diagnostic_marker'][1];require(data==b'\x78\x56'and load[where:where+2]==data and trial['diagnostic_DATA']=={'size':2,'hex':data.hex(),'fields':fields},'dialog initialized diagnostic marker identity')
 constraints=[]
 for name,offset,row in zip(NAMES,OFFSETS,proof['original_constraints']):
  require(row=={'symbol':name,'size':2,'native_DS':hex(offset),'native_range_inclusive':[hex(offset),hex(offset+1)],'inside_original_CRTzero':[0x52cc,0xcbe0],'file_backed_bytes':0,'original_allocated_MAP_proven':False}and 0x52cc<=offset and offset+2<=0xcbe0 and 0x5cc20+offset>=len(image),'dialog native extent/CRT constraint changed')
  constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(offset),'end_exclusive':hex(offset+2),'inside_startup_clear':['0x52cc','0xcbe0'],'resolved':False})
 return constraints,proof

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'dialog source pin mismatch');compiler_fn=compile_c if compiler_fn is None else compiler_fn
 # No target or native evidence is read until fresh source generation finishes.
 c=compiler_fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','dialog fresh compiler provenance')
 definitions=validate_object(c.object_bytes);constraints,proof=validate_evidence(project,item['evidence'],target);require(c.tool_hashes==proof['compiles']['SCALARS']['tool_hashes']and list(c.command)==proof['compiles']['SCALARS']['command'],'dialog compiler tool/command changed');output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/'dialog-selection-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return{'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'two_int_dialog_selection_scalars','authored_C_function_credit':0}
