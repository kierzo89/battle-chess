"""Exact actual4-LIDATA physical Huff DATA5120, no C/capacity claim."""
from pathlib import Path
from dataclasses import dataclass
import hashlib,subprocess,tempfile,os,re,json
from huff_workspace_omf16 import extract_data,HuffWorkspaceError
BACKEND='masm510-huff-workspace-physical-data-omf-v1'
SOURCE='asm/link/huff_workspace5120_omf.asm'
SOURCE_SHA256='a2ffebf6ccbeb1d543d6b09bcd42b6a56694dad65171eb5fb8932773fc642218'
TOOL_PINS={'toolchains/msc510/MASM.EXE': '1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f', 'toolchains/msc510/manifest.json': 'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4', 'toolchains/msc510/LICENSE': 'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4', 'config/msc510.json': '058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise HuffWorkspaceError(m)
def validate_unit(u):
 need(set(u)=={'id','language','backend','source','source_sha256','assembler_sha256','symbols','image_offset','size','reference_region','rea_evidence','boundary_evidence'},'closed complete DATA metadata')
 need((u['id'],u['language'],u['backend'],u['source'],u['source_sha256'])==('huff_workspace_physical_data5120','asm-data',BACKEND,SOURCE,SOURCE_SHA256),'whole physical component source identity')
 need(u['assembler_sha256']==TOOL_PINS['toolchains/msc510/MASM.EXE']and u['symbols']==['_huff_code_table','_huff_fast_lookup','_huff_long_records']and u['image_offset']=='0x5fcec'and type(u['size'])is int and u['size']==5120,'no extent/view/tool change')
 need(u['reference_region']=='exepack-expanded'and u['rea_evidence']=='evidence/huff-workspace5120/REA-zero5120.json'and isinstance(u['boundary_evidence'],str)and bool(u['boundary_evidence']),'exact complete native read and physical limitations')
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 data:bytes
 metadata:dict
 provenance:dict

def _assemble_source(source):
 source=Path(source);project=source.resolve().parents[2];content=source.read_bytes();need(H(content)==SOURCE_SHA256,'Exact standalone source bytes')
 tools={name:(project/name).read_bytes()for name in TOOL_PINS}
 for name,b in tools.items():need(H(b)==TOOL_PINS[name],'Pinned source-generation tool '+name)
 need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 with tempfile.TemporaryDirectory(prefix='bc-huff-data-')as scratch:
  p=Path(scratch);t=p/'tools';t.mkdir();(t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
  batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
  conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
  result=subprocess.run(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45,check=False)
  log=(p/'MASM.LOG').read_bytes().decode('cp437');need(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and '5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM assembly errors: '+log)
  raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437')
 for name,h in TOOL_PINS.items():need(H((project/name).read_bytes())==h,'Tool changed during generation')
 need(source.read_bytes()==content,'Source changed during generation')
 return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'original_absolute_placement_proven':False}
def assemble(source,unit,nasm=None):
 validate_unit(unit);source=Path(source).resolve();project=source.parents[2];need(source==(project/SOURCE).resolve(),'exact canonical source path')
 raw,proof=_assemble_source(source);data,metadata=extract_data(raw);need(proof['source_sha256']==unit['source_sha256'],'source fingerprint');return Build(raw,data,metadata,proof)

def validate_evidence(unit,project,target_sha256,reference=None):
 validate_unit(unit)
 from huff_workspace_evidence import validate_data
 return validate_data(unit,project,target_sha256,reference)
