"""Closed mixed physical driver carrier: 12 instruction bytes +3604 zero DATA.

No original procedure, C function, capacity, TU or absolute placement claim.
"""
from pathlib import Path
from dataclasses import dataclass
import hashlib,json,subprocess,tempfile,os,re
from graphics_driver_carrier_omf16 import validate_obj,CarrierError,PUBLICS
from reference import validate_expanded_read,ORIGINAL_SHA256,CARRIER_SHA256
BACKEND='masm510-mixed-driver-carrier-code-omf'
SOURCE='asm/link/graphics_driver_carrier.asm'
SOURCE_SHA256='bb8c665e83e378f7a73d8e40edcebcb683719b6d045dbb51f14d2529ec64fb4a'
OBJECT_SHA256='c2f6da20327894eced3ee50645c70a4ed0375327858373b4921cf16fa6b71a4b'
BASE=0x110d0
SIZE=3616
RAW_EVIDENCE='build/graphics-overlay-ownership/rea-expanded-carrier3616.json'
INVENTORY='build/graphics-dynamic-carrier-physical-model/inventory.json'
EVIDENCE_PINS={RAW_EVIDENCE:'1e0f3a396bef7b85377726ee2a7b19b757d25cc6c706acf493d4a4d7572a152c',INVENTORY:'9b7d297c5f6424fd971ceb2464f397918829b1e47a22234e9376b95cf5ba5883'}
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise CarrierError(m)
def validate_unit(u):
 need(set(u)=={'id','language','backend','object_profile','source','source_sha256','assembler_sha256','public_symbols','image_offset','size','externals','rea_evidence','reference_region','boundary_evidence'},'Exact mixed carrier metadata keys')
 need((u['id'],u['language'],u['backend'],u['object_profile'])==('graphics_driver_physical_carrier3616','asm-code',BACKEND,'mixed_driver_carrier_12plus3604'),'Closed mixed allocation identity')
 need(u['source']==SOURCE and u['source_sha256']==SOURCE_SHA256 and u['assembler_sha256']==TOOL_PINS['toolchains/msc510/MASM.EXE'],'Exact source/tool identity')
 need(u['public_symbols']==list(PUBLICS)and u['image_offset']==hex(BASE)and type(u['size'])is int and u['size']==SIZE and u['externals']=={},'Whole physical extent and five actual PUBLICs only')
 need(u['reference_region']=='exepack-expanded'and u['rea_evidence']==RAW_EVIDENCE,'Independent complete physical REA span')
 need(isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence'].strip()),'Explicit physical packet boundary provenance')
def extract_code(raw):
 code,meta=validate_obj(raw);need(H(raw)==OBJECT_SHA256,'Exact actual complete source-produced OMF')
 need(meta['mnemonic_bytes']==12 and meta['physical_zero_DATA_bytes']==3604 and meta['internal_fixups']==4 and not meta['internal_MZ']and meta['procedures']==0,'Separate instruction/DATA/fixup accounting')
 return code,meta
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 code:bytes
 metadata:dict
 provenance:dict
def _assemble_source(source,project):
 source=Path(source);content=source.read_bytes();need(H(content)==SOURCE_SHA256,'Exact standalone source bytes')
 tools={name:(project/name).read_bytes()for name in TOOL_PINS}
 for name,b in tools.items():need(H(b)==TOOL_PINS[name],'Pinned source-generation tool '+name)
 need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 with tempfile.TemporaryDirectory(prefix='bc-driver-carrier-')as scratch:
  p=Path(scratch);t=p/'tools';t.mkdir();(t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
  batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
  conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
  result=subprocess.run(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45,check=False)
  log=(p/'MASM.LOG').read_bytes().decode('cp437');need(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and '5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM assembly errors: '+log)
  raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437')
 for name,h in TOOL_PINS.items():need(H((project/name).read_bytes())==h,'Tool changed during generation')
 need(source.read_bytes()==content,'Source changed during generation')
 return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'physical_instruction_bytes':12,'physical_initialized_zero_data_bytes':3604,'original_absolute_placement_proven':False}
def assemble(source,project):
 project=Path(project).resolve();source=Path(source).resolve()
 need(source==(project/SOURCE).resolve()and source.is_relative_to(project)and not(project/SOURCE).is_symlink(),'Exact regular standalone source path')
 raw,provenance=_assemble_source(source,project);code,meta=extract_code(raw)
 return Build(raw,code,meta,provenance)
def _evidence(project):
 project=Path(project);out={}
 for name,h in EVIDENCE_PINS.items():
  raw=(project/name).read_bytes();need(H(raw)==h,'Physical carrier evidence pin '+name);out[name]=json.loads(raw)
 p=out[INVENTORY];need(p['source_extent']==[BASE,BASE+SIZE]and p['header_literal_original_FILE_range']==[70352,70364],'Exact independent physical prefix extent')
 need(p['zero_packet']=={'ordinal':248,'record':{'command':177,'count':3604,'source_start':69852,'destination_start':69852,'fill':0},'original_FILE_offset':70364,'raw':'00140eb1'},'Actual terminal EXEPACK initialized packet, not default memory')
 return out[RAW_EVIDENCE]
def validate_evidence(unit,project,target_sha256,reference=None):
 validate_unit(unit);need(target_sha256==ORIGINAL_SHA256 and reference is not None and reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and reference['prefix_size']==BASE+12,'Exact pinned original/decoded carrier identity and literal prefix boundary')
 need(not any(BASE<=s<BASE+SIZE or BASE<s+2<=BASE+SIZE for s in reference['relocations']),'No native MZ site intersects this whole carrier')
 e=_evidence(project);return validate_expanded_read(e,unit,reference['image'][BASE:BASE+SIZE],reference,emitted_mz_sites=[])
def validate_comparison(unit,built,image,project,original_sites):
 validate_unit(unit);code,meta=extract_code(built.object_bytes);need(code==built.code and meta==built.metadata,'Exact complete generated object view')
 need(code==image[BASE:BASE+SIZE],'Complete physical carrier byte comparison')
 need(not any(BASE<=s<BASE+SIZE or BASE<s+2<=BASE+SIZE for s in original_sites),'No native internal MZ site')
 e=_evidence(project);fields=[]
 for f in meta['internal_fields']:
  fields.append({'segment':1,'object_offset':f['offset'],'image_offset':BASE+f['offset'],'width':2,'mode':'self_relative_internal_CODE','target_segment':1,'target_offset':3613,'encoded_hex':f['encoded']})
 loads=[{'load_paragraph':b,'all3616_native_equal':code==image[BASE:BASE+SIZE],'self_relative_fields_invariant':True,'native_internal_MZ_sites':[]}for b in [0,1,4096,65535]]
 return code,{'whole_allocation_image_offset':BASE,'whole_allocation_size':SIZE,'whole_allocation_sha256':H(code),'whole_bytes_equal':True,'whole_original_mz_sites':[],'emitted_mz_sites':[],'relocations':fields,'four_load_bases':loads,'native_evidence_id':e['evidence_id'],'evidence_sha256':EVIDENCE_PINS,'mnemonic_bytes':12,'physical_initialized_zero_DATA_bytes':3604,'classification':'mixed_physical_driver_carrier','authored_c_function_credit':0,'authored_asm_function_credit':0,'historical_TU_capacity_or_absolute_placement_proven':False,'original_dynamic_driver_implementation_recovered':False,'unknown14_byte_tail_allocated':False}
