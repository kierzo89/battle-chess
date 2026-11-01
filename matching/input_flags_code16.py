"""Closed whole mouse/joystick input CODE388, not a C reconstruction.

Source-only MASM generation is independent of explicit native comparison frames.
No ORG/fill/crop, opcode DB, initialized DATA, hidden fields or function credit.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import sys,json,hashlib,os,subprocess,tempfile,re
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
S=M
if str(S)not in sys.path:sys.path.insert(0,str(S))
from omf import read_omf,OMFError
import serial248_code16 as tools
BACKEND='masm510-input-flags-code-omf'
ORIGINAL_SHA256=tools.ORIGINAL_SHA256
CARRIER_SHA256=tools.CARRIER_SHA256
PROFILE=tools.PROFILE
BASE=0x11f3e;SIZE=388;FRAME=0x11ef;CODE_BASE=0x4e
PUBLICS={'_input_probe_11ef_004e':0,'_input_poll_11ef_00b9':107,'_special_command_1fc2':132}
BINDINGS={'_input_poll_handler_4950':{'segment':0x5cc2,'offset':0x4950},'_input_flags_4952':{'segment':0x5cc2,'offset':0x4952},'_joystick_centre_x_4954':{'segment':0x5cc2,'offset':0x4954},'_joystick_centre_y_4956':{'segment':0x5cc2,'offset':0x4956},'_flag_005b':{'segment':0x5cc2,'offset':0x005b},'_input_x_005c':{'segment':0x5cc2,'offset':0x005c},'_input_y_005e':{'segment':0x5cc2,'offset':0x005e},'_buttons_8d04':{'segment':0x5cc2,'offset':0x8d04}}
SOURCES={'build/input-flags4952-coherent/input_poll_flags.asm': 'd41ea42752d73040853db3a22c06a962ff1e278d26ab4f9d4437db51d9e4e18e', 'build/input-flags4952-coherent/wrong_input_poll_flags.asm': '63d99d3a9e4190a4c39b4b41ccf90ba697c4eb00d93d117289f27043108bb82b'}
OBJECT_HASHES={'65db94c9429c15eec2e9b2637f71ca0a07ae36bb3d664cfa01d30a5984e3a8fe', '260b578c8d95cb28a9140c6512d4c674bfbd6412791afcca4a5b8f926e21e106'}
RAW_CODE_SHA256='e894ce8f0cb95f70e26d2b0b929a2c0ea91fb859907dfee2aa57113f773e9000'
RECORD_PAYLOAD_HASHES=[(128, 0, '4fb390538337b2d69ad7c1ab5d347ae0af0bf4d3e411c89a4431eb22e98a8fd8'), (150, 13, '9a7383100ded185ae9ad03129fcbf38b66d88327abe68b54fbe50771bee0899c'), (152, 61, 'c3ac26c0bd61c0094f0bee15e3788e631d8e55fb5f45d6abfa34341507d44b4b'), (152, 71, '9ce4d6ac954b8d975de7ffd03a6218fbf02d26948ed4e1bafea4009c6e41e4ae'), (154, 81, '7270bf5afdbd1cef0dc73aa616704df89a65b3917892b04b6f0bb18fc2156f41'), (140, 88, 'f8e51d4fa375af8cf76d61ea86f61ac23f37023a650198e27a6d5ac21eb13bdd'), (144, 244, '98bfaa4cba339b75c0c389a841d292c4d17e3d2c58aa23e6e5301f8ed818c611'), (136, 326, 'fd47f9fd11ee91a44ab31c40b4a2771341d5ba747d2b0f2954d92d6ea2137a48'), (160, 333, 'da9c354486bbef3e1ba60d331a6f94c04a5ccabc450efb0bf8fe504c11b82246'), (156, 728, '2b64ceb755057aefcc9826be6ce3f6d2c67019b03b355776abc4f1ed88d6c008'), (138, 936, '6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d')]
EXTERNALS={1: '_input_poll_handler_4950', 2: '_buttons_8d04', 3: '_input_x_005c', 4: '_input_y_005e', 5: '_flag_005b', 6: '_input_flags_4952', 7: '_joystick_centre_x_4954', 8: '_joystick_centre_y_4956'}
FIELD_PROFILE=[(2, 26, 2, 1, True, (1, 1), (2, 1), None, 'c41a160101', 728), (2, 28, 2, 1, True, (0, 2), (0, 2), 112, 'c41c0002027000', 728), (2, 81, 2, 1, True, (1, 1), (2, 1), None, 'c451160101', 728), (2, 83, 2, 1, True, (0, 2), (0, 2), 164, 'c453000202a400', 728), (2, 86, 4, 3, True, (0, 2), (0, 2), 132, 'cc560002028400', 728), (2, 91, 4, 3, True, (0, 2), (0, 2), 132, 'cc5b0002028400', 728), (2, 96, 4, 3, True, (0, 2), (0, 2), 132, 'cc600002028400', 728), (2, 104, 2, 1, True, (1, 1), (2, 5), None, 'c468160105', 728), (2, 108, 2, 1, True, (1, 1), (2, 1), None, 'c46c160101', 728), (2, 120, 2, 1, True, (1, 1), (2, 2), None, 'c478160102', 728), (2, 124, 2, 1, True, (1, 1), (2, 3), None, 'c47c160103', 728), (2, 128, 2, 1, True, (1, 1), (2, 4), None, 'c480160104', 728), (2, 136, 2, 1, True, (1, 1), (2, 1), None, 'c488160101', 728), (2, 138, 2, 1, True, (0, 2), (0, 2), 164, 'c48a000202a400', 728), (2, 143, 4, 3, True, (0, 2), (0, 2), 309, 'cc8f0002023501', 728), (2, 155, 2, 1, True, (1, 1), (2, 7), None, 'c49b160107', 728), (2, 159, 2, 1, True, (1, 1), (2, 8), None, 'c49f160108', 728), (2, 167, 4, 3, True, (0, 2), (0, 2), 309, 'cca70002023501', 728), (2, 173, 2, 1, True, (1, 1), (2, 7), None, 'c4ad160107', 728), (2, 177, 2, 1, True, (1, 1), (2, 8), None, 'c4b1160108', 728), (2, 194, 2, 1, True, (1, 1), (2, 3), None, 'c4c2160103', 728), (2, 211, 2, 1, True, (1, 1), (2, 3), None, 'c4d3160103', 728), (2, 214, 2, 1, True, (1, 1), (2, 4), None, 'c4d6160104', 728), (2, 231, 2, 1, True, (1, 1), (2, 4), None, 'c4e7160104', 728), (2, 252, 2, 1, True, (1, 1), (2, 6), 1, 'c4fc1201060100', 728), (2, 257, 2, 1, True, (1, 1), (2, 6), 1, 'c5011201060100', 728), (2, 260, 4, 3, True, (0, 2), (0, 2), 375, 'cd040002027701', 728), (2, 269, 2, 1, True, (0, 2), (0, 2), 293, 'c50d0002022501', 728), (2, 281, 2, 1, True, (0, 2), (0, 2), 293, 'c5190002022501', 728), (2, 285, 4, 3, True, (0, 2), (0, 2), 375, 'cd1d0002027701', 728), (2, 304, 2, 1, True, (1, 1), (2, 2), None, 'c530160102', 728), (2, 317, 4, 3, True, (0, 2), (0, 2), 375, 'cd3d0002027701', 728), (2, 335, 4, 3, True, (0, 2), (0, 2), 375, 'cd4f0002027701', 728), (2, 354, 4, 3, True, (0, 2), (0, 2), 375, 'cd620002027701', 728)]
EVIDENCE_PINS={'build/input-neighbours-11f3e/rea-whole388.json': 'f1615797a7621e0542e48b0356d4d8007551a0be71cc96358814b81fdf4b38de', 'build/input-neighbours-11f3e/rea-whole-512.json': '24a5ccfff17f02ffae71e75d536d30c34c4c3db48df0255bfacd688db1140a4d', 'build/input-neighbours-11f3e/rea-next16.json': '187991f0424fff34d09ca120f1e0788386bdbe5ef2530748530ca018c4ecbecb', 'build/input-neighbours-11f3e/rea-function-21f3e.json': '63010ed09191f0d399794934971ab6651e081a5892ac83edd2695fd424a67562', 'build/input-neighbours-11f3e/rea-function-21fa9.json': '745bbdb9d48e3e6568f29f40bf2bcb935e36422b9baffb5ff502f40a6603e054', 'build/input-neighbours-11f3e/rea-function-21fc2.json': 'f25c98bb4106d307f46d879f85be0d56591edba8305190fc12e61aa504f739de', 'build/input-neighbours-11f3e/rea-function-22073.json': 'fa6f415ecc1dc02e377cc7c3353e55e5f65eab88d19e196120e6eb6fb7ccf76f', 'build/input-neighbours-11f3e/rea-function-220b5.json': '94d439293f59ba4f303f9a46112e60642bcb28544b2b2e8557daca906f95354f', 'build/input-neighbours-11f3e/rea-function-21fae.json': '3e98cbbdb5869fe3444dc5242e9de621836b1b1445275938264e85c606eeda3d', 'build/input-neighbours-11f3e/rea-function-21fe2.json': 'ad00b21842a1cf95dd8ae1a643f02c2936e11e80f1c77d62b90beaee9f26eade', 'build/input-neighbours-11f3e/rea-mouse-20.json': '74e22e32d736b47cba928b23bfa253ad440a2aa10251538d01a289bfc897729f', 'build/input-neighbours-11f3e/rea-joystick-145.json': 'e8bb5382fc6e65d5fb189ac93dcc6b167d395f25cd12be5949504c13fa1eb485', 'build/input-neighbours-11f3e/rea-instruction-21fac.json': 'a9bad8ff7b69ee4bb8db9c97221cefbc57ef836d0cc74030bc0d5705491be431', 'build/input-neighbours-11f3e/rea-instruction-21fae.json': '4f2e0f6c340e80a537e73ff34e40252c7707beac9de7073975288eba0d5448a1', 'build/input-neighbours-11f3e/rea-instruction-21fe2.json': '559f099a00d7dd5edbdc0d62711bc1cf3b0f90e65586a1decc729f3757a91656', 'build/input-neighbours-11f3e/rea-instruction-22048.json': 'a236b8b9bc7f0a3320d6e07325b590e269bc62a7afb8cdc3aa0914ff27d43736', 'build/input-neighbours-11f3e/rea-instruction-22054.json': 'c247918a6a33143009c777a8683f44d55ea499c3ac57470eec0faff35343ebc7', 'build/input-neighbours-11f3e/rea-instruction-22063.json': '9dcbfcb6edb2ba4ca1c810934e75fff94ad495fb32033965bee3dd8fe4f10780', 'build/input-flags4952-coherent/freeze-manifest.json': '97a66a3713ceb8a2570191ca2c2aeb2504de8ebb7882aaa43cbf8f0888849e54', 'build/input-flags4952-coherent/backend-migration-bindings.json': 'afca13f3e4681a9cba6ab4c0920846ab96b0d08dd9eb3925da12d735c0c10fb1', 'build/input-flags4952-coherent/rea-native-flags2.json': '06d7417e69d189a7c5b6afad58aecd4b2c8a657ea600e78520d05f602cc44d84', 'build/input-flags4952-coherent/rea-latch-compare.json': '635796712bdb658fadbbb36481035b2763129855ffcbae2ccf1d6551bed3907d', 'build/input-flags4952-coherent/rea-latch-store.json': 'dfab94485621d2397c6054f1b4cc9a0545340072fcf7f4aaf9fd7677eca577d7'}

D=M/'build/input-flags4952-coherent'
pinned=tools
H=lambda data:hashlib.sha256(data).hexdigest()
def _assemble_source(source):
 source=Path(source);content=source.read_bytes();require(source.parent.resolve()==D.resolve(),'Exact reviewed source directory required')
 # No opcode blobs, reserve/fill, explicit origin/alignment or includes.
 text=content.decode('ascii')
 for line in text.splitlines():
  words=line.split(';',1)[0].upper().split()
  require(not set(words).intersection({'DB','DW','DD','DQ','DT','DUP','ORG','ALIGN','EVEN','INCBIN','INCLUDE'}),'Unsupported assembly directive: '+line)
 tools=M/'toolchains/msc510';paths={'assembler':tools/'MASM.EXE','manifest':tools/'manifest.json','license':tools/'LICENSE','config':M/'config/msc510.json'}
 expected={'assembler':pinned.MASM_SHA256,'manifest':pinned.MANIFEST_SHA256,'license':pinned.LICENSE_SHA256,'config':pinned.CONFIG_SHA256}
 for key,p in paths.items():require(H(p.read_bytes())==expected[key],'MASM '+key+' pin mismatch')
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 with tempfile.TemporaryDirectory(prefix='input-masm-')as scratch:
  p=Path(scratch);require(not any(c in str(p)for c in (chr(13),chr(10),chr(34))),'Unsafe assembler scratch path');(p/'UNIT.ASM').write_bytes(content)
  batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
  conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(tools)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
  result=subprocess.run(['dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=60)
  log=(p/'MASM.LOG').read_text(encoding='cp437');listing=(p/'UNIT.LST').read_text(encoding='cp437')
  require(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled','MASM generation failed: '+log)
  require('Macro Assembler Version 5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'MASM warnings/errors/version: '+log)
  raw=(p/'UNIT.OBJ').read_bytes()
 for key,p in paths.items():require(H(p.read_bytes())==expected[key],'MASM '+key+' changed during generation')
 require(source.read_bytes()==content,'Source changed during generation')
 return raw,dict(source_sha256=H(content),assembler_sha256=expected['assembler'],assembler_manifest_sha256=expected['manifest'],assembler_license_sha256=expected['license'],assembler_config_sha256=expected['config'],command=command,assembler_log=log,assembler_listing=listing,object_sha256=H(raw),dosbox_conf=conf,batch=batch,stdout=result.stdout.decode('utf-8','replace'),stderr=result.stderr.decode('utf-8','replace'),fresh_scratch=True,generation_target_inputs=False,generation_placement_inputs=False)

class InputCodeError(OMFError):pass
def require(v,message):
 if not v:raise InputCodeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def shape(f):return(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.raw.hex(),f.record_offset)
def validate_unit(unit):
 required={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','boundary_evidence','reference_region'}
 require(type(unit)is dict and set(unit)==required,'Closed388 metadata keys only')
 require((unit['id'],unit['language'],unit['backend'],unit['object_profile'])==('input_poll_code388','asm-code',BACKEND,'input_poll388_flags_v1'),'Exact388 allocation profile required')
 require(unit['source']in SOURCES and unit['source_sha256']==SOURCES[unit['source']]and unit['assembler_sha256']==tools.MASM_SHA256,'Pinned reviewed assembly/tools required')
 require(unit['public_symbols']==list(PUBLICS)and unit['image_offset']==hex(BASE)and type(unit['size'])is int and unit['size']==SIZE,'Complete388/threePUBLICs only, no slicing')
 require(unit['externals']==BINDINGS and unit['reference_region']=='exepack-expanded'and unit['rea_evidence']=='build/input-neighbours-11f3e/rea-whole388.json','Closed frame/state/evidence bindings required')
 require(type(unit['boundary_evidence'])is str and bool(unit['boundary_evidence'].strip()),'Required allocation/native limits description')
def extract_code(raw_object):
 require(type(raw_object)is bytes,'Unchanged raw OMF bytes required')
 obj=read_omf(raw_object)
 require(digest(raw_object)in OBJECT_HASHES,'Unreviewed whole source object')
 require(set(obj.segments)=={1,2}and obj.names==['','','DGROUP','GRAPHICS_INPUT_TEXT','DATA','CODE','_DATA'],'Exact two segments/names/group required')
 require([(s.name,s.class_name,s.length,s.attributes,s.name_index,s.class_index,s.overlay_index)for s in obj.segments.values()]==[('_DATA','DATA',0,72,6,4,1),('GRAPHICS_INPUT_TEXT','CODE',388,72,3,5,1)],'No extra/foreign/short allocation or alignment')
 require(obj.externals==EXTERNALS and not obj.procedures,'Exact eight real storage externals; no invented procedure metadata')
 require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and all((p.segment,p.group,p.type_index)==(2,0,0)for p in obj.publics.values()),'Three actual PUBLICs/frames only')
 require([shape(f)for f in obj.fixups]==FIELD_PROFILE,'All34 actual raw fields/frames/targets/displacements must remain')
 require([k for k,_,_ in obj.records]==[0x80,0x96,0x98,0x98,0x9a,0x8c,0x90,0x88,0xa0,0x9c,0x8a],'Exact records; no COMMON/debug/LIDATA/extra chunks')
 require([b for k,_,b in obj.records if k==0x9a]==[bytes.fromhex('02ff01')],'Exact emptyDATA DGROUP')
 require([b for k,_,b in obj.records if k==0x80]==[b'\x08UNIT.ASM']and[b for k,_,b in obj.records if k==0x88]==[bytes.fromhex('00a201')]and[b for k,_,b in obj.records if k==0x8a]==[b'\0'],'Exact headers/directives')
 require(not obj.segments[1].chunks and not obj.segments[1].unsupported_data and not obj.segments[2].unsupported_data,'No DATA or unsupported record data')
 code=bytearray()
 for at,b in obj.segments[2].chunks:
  require(bool(b)and at==len(code)and at+len(b)<=SIZE,'No hole/overlap/excess')
  code.extend(b)
 require(len(code)==SIZE,'Entire actualCODE allocation and tail required')
 require(digest(bytes(code))==RAW_CODE_SHA256,'Exact full source instructions/addends required')
 require([(k,a,digest(p))for k,a,p in obj.records]==RECORD_PAYLOAD_HASHES,'Exact actual record payloads required')
 return bytes(code),{'boundary':'complete_multi_entry_CODE_SEGDEF','segment':asdict(obj.segments[2])|{'chunks':[{'offset':a,'hex':b.hex()}for a,b in obj.segments[2].chunks]},'publics':[asdict(p)for p in obj.publics.values()],'empty_DATA_bytes':0,'whole_CODE_bytes':SIZE,'all_actual_fields':[asdict(f)|{'raw':f.raw.hex()}for f in obj.fixups],'private_components':[{'kind':'raw_CFG_mouse_handler','offset':112,'bytes':20,'ordinary_REA_procedure_claim':False},{'kind':'raw_CFG_joystick_handler','offset':164,'bytes':145,'ordinary_REA_procedure_claim':False},{'kind':'real_self_modifying_branch','offset':293,'bytes':2,'writes_opcode_byte_at_offset':293,'JA_or_JG':True,'DATA_credit':0}],'authored_c_function_credit':0,'authored_asm_function_credit':0,'function_partition_claim':False,'historical_MODULE_or_MAP_claim':False}
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 code:bytes
 metadata:dict
 provenance:dict
def assemble(source,project):
 require(not Path(source).is_symlink(),'Source symlink forbidden')
 source,project=Path(source).resolve(),Path(project).resolve()
 require(not any(c in str(project)for c in (chr(13),chr(10),chr(34))),'Unsafe assembler project path')
 require(source.is_relative_to(project),'Source outside project')
 key=str(source.relative_to(project));require(key in SOURCES and digest(source.read_bytes())==SOURCES[key],'Source pin mismatch')
 raw,provenance=_assemble_source(source);require(provenance['source_sha256']==SOURCES[key],'Source changed during generation')
 provenance=provenance|{'build_command':provenance['command'],'assembler_configuration_sha256':provenance['assembler_config_sha256'],'compiler':'Microsoft Macro Assembler5.10','object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False}
 code,meta=extract_code(raw);return Build(raw,code,meta,provenance)
def link(raw_object,code_frame=FRAME,code_base=CODE_BASE,dgroup=0x5cc2):
 raw,meta=extract_code(raw_object);obj=read_omf(raw_object);out=bytearray(raw);used=set();logs=[]
 require(type(code_frame)is int and 0<=code_frame<=65535 and type(code_base)is int and code_base>=0 and code_base+SIZE<=65536,'CODE mapping must fit actual explicit frame')
 require(type(dgroup)is int and 0<=dgroup<=65535,'Explicit DGROUP frame')
 for f in obj.fixups:
  require(f.segment==2 and f.segment_relative and f.offset>=0 and f.offset+f.width<=SIZE,'Actual field extent/mode')
  require(not used.intersection(range(f.offset,f.offset+f.width)),'Field overlap');used.update(range(f.offset,f.offset+f.width))
  before=bytes(out[f.offset:f.offset+f.width]);addend=int.from_bytes(before[:2],'little');symbol=None;mz=None
  if f.width==2 and f.location_type==1 and f.frame==(1,1)and f.target[0]==2 and ((f.offset in (252,257) and f.target==(2,6) and f.displacement==1) or (f.offset not in (252,257) and f.displacement is None)):
   symbol=obj.externals[f.target[1]];value=BINDINGS[symbol]['offset']+addend+(f.displacement or 0);encoded=(value&65535).to_bytes(2,'little');mode='DGROUP_external_OFFSET16'
  elif f.width==2 and f.location_type==1 and f.frame==f.target==(0,2)and f.displacement is not None:
   value=code_base+f.displacement+addend;require(code_base<=value<code_base+SIZE,'Own CODE target outside whole allocation');encoded=(value&65535).to_bytes(2,'little');mode='own_CODE_OFFSET16'
  else:
   require(f.width==4 and f.location_type==3 and f.frame==f.target==(0,2)and f.displacement is not None,'Only reviewed own FAR16 shape')
   value=code_base+f.displacement+addend;require(code_base<=value<code_base+SIZE,'Own FAR target outside whole allocation')
   encoded=(value&65535).to_bytes(2,'little')+((code_frame+int.from_bytes(before[2:],'little'))&65535).to_bytes(2,'little');mode='own_CODE_FAR16';mz=BASE+f.offset+2
  out[f.offset:f.offset+f.width]=encoded
  row={'segment':2,'object_offset':f.offset,'image_offset':BASE+f.offset,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'frame':list(f.frame),'target':list(f.target),'displacement':f.displacement,'target_symbol':symbol,'original_field_hex':before.hex(),'encoded_hex':encoded.hex(),'raw_fixupp':f.raw.hex(),'record_offset':f.record_offset,'mode':mode,'CODE_frame':code_frame,'CODE_base':code_base,'DGROUP_frame':dgroup}
  if mz is not None:row['mz_segment_relocation_image_offset']=mz
  logs.append(row)
 return bytes(out),logs
def _forward(data,sites,load):
 result=bytearray(data)
 for s in sites:
  i=s-BASE;require(0<=i and i+2<=len(result),'Relocation crossing whole allocation');result[i:i+2]=((int.from_bytes(result[i:i+2],'little')+load)&65535).to_bytes(2,'little')
 return bytes(result)
def _native_sites(original_sites):
 expected=[BASE+f[1]+2 for f in FIELD_PROFILE if f[2]==4]
 local=sorted(s for s in original_sites if s<BASE+SIZE and s+2>BASE)
 require(local==sorted(expected)and len(local)==10 and all(BASE<=s and s+2<=BASE+SIZE for s in local),'Exact ten native MZ words, no missing/extra/crossing')
 return local
def _evidence(project):
 rows={}
 for rel,pin in EVIDENCE_PINS.items():
  raw=(Path(project)/rel).read_bytes();require(digest(raw)==pin,'Native evidence changed: '+rel);rows[Path(rel).name]=json.loads(raw)
 e=rows['rea-whole388.json'];require(e['subject']['digest']['sha256']==CARRIER_SHA256 and e['analysis_profile']['digest']==PROFILE and e['operation']=='read_bytes'and e['parameters']=={'address':'0x21f3e','length':388},'Exact derived-carrier/load-profile primary required')
 r=e['normalized_result'];require(r['complete']is True and r['requested_bytes']==r['returned_bytes']==388,'Complete primary388');loaded=bytes.fromhex(r['bytes_hex']);require(len(loaded)==388,'Exact primary388 length')
 for name,start,end,size in [('21f3e','0x21f3e','0x21fa8',107),('21fa9','0x21fa9','0x21fad',5),('21fc2','0x21fc2','0x21fe1',32),('22073','0x22073','0x220b4',66),('220b5','0x220b5','0x220c1',13)]:
  p=rows['rea-function-'+name+'.json']['normalized_result']['procedure'];b=p['body'];require(p['address']==start and b['available']and not b['non_contiguous']and b['contains_entry']and b['total_bytes']==b['span_bytes']==size and b['ranges']==[{'start':start,'end':end}],'Actual ordinary/native body changed')
 for name in ['21fae','21fe2']:
  require(rows['rea-function-'+name+'.json'].get('isError')is True and rows['rea-instruction-'+name+'.json']['normalized_result']['status']=='undecodable','Do not invent ordinary native procedures for dispatcher handlers')
 require(loaded[112:132]==bytes.fromhex(rows['rea-mouse-20.json']['normalized_result']['bytes_hex'])and loaded[164:309]==bytes.fromhex(rows['rea-joystick-145.json']['normalized_result']['bytes_hex']),'Private raw CFG bounds')
 require(loaded[293:295]==bytes.fromhex('77f5')and loaded[266:272]==bytes.fromhex('2ec606730177')and loaded[278:284]==bytes.fromhex('2ec60673017f'),'Actual CS-relative self-modification/JA target')
 return loaded,e['evidence_id']
def validate_evidence(unit,project,target_sha256,reference=None):
 validate_unit(unit);require(target_sha256==ORIGINAL_SHA256 and reference is not None and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'Pinned original and derived identity required')
 loaded,id=_evidence(project);sites=_native_sites(reference['relocations']);require(_forward(reference['image'][BASE:BASE+SIZE],sites,0x1000)==loaded,'Entire primary forward loader mismatch')
 require(BASE>=reference['prefix_size'],'Expanded-only profile must not earn file bytes');return id
def validate_comparison(unit,built,image,project,original_sites):
 validate_unit(unit);raw,meta=extract_code(built.object_bytes);require(raw==built.code and meta==built.metadata,'Actual full source allocation changed')
 linked,logs=link(built.object_bytes);sites=_native_sites(original_sites);loaded,id=_evidence(project)
 require(_forward(image[BASE:BASE+SIZE],sites,0x1000)==loaded,'Native primary388 differs from comparison image')
 emitted=sorted(f['mz_segment_relocation_image_offset']for f in logs if'mz_segment_relocation_image_offset'in f);require(emitted==sites and len(logs)==34,'Exact actual field/MZ accounting')
 loads=[]
 for base in [0,1,4096,65535]:
  b,l=link(built.object_bytes,code_frame=(FRAME+base)&65535,dgroup=(0x5cc2+base)&65535);require(b==_forward(linked,sites,base),'Exact forward loader arithmetic');loads.append({'load_paragraph':base,'all388_source_loader_bytes_exact':True,'native_bytes_equal':b==_forward(image[BASE:BASE+SIZE],sites,base),'MZ_words':10,'linked_sha256':digest(b)})
 return linked,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':digest(linked),'whole_bytes_equal':linked==image[BASE:BASE+SIZE],'whole_original_mz_sites':sites,'emitted_mz_sites':emitted,'relocations':logs,'four_load_bases':loads,'native_evidence_id':id,'evidence_sha256':EVIDENCE_PINS,'native_CODE_frame':FRAME,'native_CODE_base':CODE_BASE,'native_segment_prefix_bytes':78,'source_segment_origin_directive_or_padding':False,'authored_c_function_credit':0,'authored_asm_function_credit':0,'function_partition_claim':False,'native_private_CFGs_ordinary_function_claim':False,'DATA_credit':0,'FILE_byte_credit':0,'IMAGE_bytes':388,'original_global_MAP_or_alignment_proven':False,'following_zero_gap_allocated':False,'hardware_execution':False,'remaining_dependencies':list(BINDINGS)}
