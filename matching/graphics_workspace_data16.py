"""Closed initialized physical graphics workspace DATA; no C or capacity credit."""
from pathlib import Path
from dataclasses import dataclass
import hashlib,subprocess,tempfile,os,re
from graphics_workspace_zero_omf16 import validate_obj,DataError
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
BACKEND='masm510-graphics-workspace-physical-data-omf'
SOURCE_SHA256='38f92a918da850d99b2edbef487802c3b50e7b6a5a1ef8ab8c21e366a2a0e35d'
OBJECT_SHA256='ef8f34c205fda542e2f3827831fadc3f08f6746f452c02dfb2c7423bee033203'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise DataError(s)
def validate_unit(u):
 need(set(u)=={'id','language','backend','source','source_sha256','assembler_sha256','symbols','image_offset','size','reference_region','rea_evidence','boundary_evidence'},'Exact physical DATA metadata keys')
 need((u['id'],u['language'],u['backend'])==('graphics_workspace_physical_data86000','asm-data',BACKEND),'Closed DATA identity')
 need(u['source']=='src/data/graphics_workspace.asm'and u['source_sha256']==SOURCE_SHA256 and u['assembler_sha256']==TOOL_PINS['toolchains/msc510/MASM.EXE'],'Exact source/tool pins')
 need(u['symbols']==['_graphics_workspace','_metadata_workspace']and u['image_offset']=='0x120d0'and type(u['size'])is int and u['size']==86000,'Whole physical DATA only')
 need(u['reference_region']=='exepack-expanded'and u['rea_evidence']=='evidence/rea_graphics_workspace_86000.json','Complete independent expanded REA read')
 need(isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence'].strip()),'Explicit physical boundary provenance')
def extract_data(raw):
 # Validate full raw ownership before accepting this actual compiler output hash.
 pieces,meta=validate_obj(raw);need(H(raw)==OBJECT_SHA256,'Exact actual whole assembler object')
 meta.update(boundary='two_complete_initialized_private_PARA_SEGDEFs',classification='opaque_physical_initialized_DATA',source_partition_is_engineering=True,historical_TU_proven=False,historical_C_capacity_proven=False,original_global_MAP_proven=False,authored_c_credit=0)
 return b''.join(pieces),meta
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 data:bytes
 metadata:dict
 provenance:dict

def _assemble_source(source):
 source=Path(source);content=source.read_bytes();need(H(content)==SOURCE_SHA256,'Exact standalone source bytes')
 tools={name:(M/name).read_bytes()for name in TOOL_PINS}
 for name,b in tools.items():need(H(b)==TOOL_PINS[name],'Pinned source-generation tool '+name)
 need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 with tempfile.TemporaryDirectory(prefix='bc-graphics-data-')as scratch:
  p=Path(scratch);t=p/'tools';t.mkdir();(t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
  batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
  conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
  result=subprocess.run(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45,check=False)
  log=(p/'MASM.LOG').read_bytes().decode('cp437');need(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and '5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM assembly errors: '+log)
  raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437')
 for name,h in TOOL_PINS.items():need(H((M/name).read_bytes())==h,'Tool changed during generation')
 need(source.read_bytes()==content,'Source changed during generation')
 return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'original_absolute_placement_proven':False}
def assemble(source,unit,nasm=None):
 validate_unit(unit);source=Path(source);need(source.resolve()==(M/unit['source']).resolve()and not source.is_symlink(),'Exact regular source path')
 raw,proof=_assemble_source(source);data,metadata=extract_data(raw);need(proof['source_sha256']==unit['source_sha256'],'Source fingerprint mismatch')
 return Build(raw,data,metadata,proof)
