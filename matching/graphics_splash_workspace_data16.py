"""Closed initialized physical graphics workspace DATA; no C or capacity credit."""
from pathlib import Path
from dataclasses import dataclass
import hashlib,subprocess,tempfile,os,re,json
from contextlib import contextmanager
from unittest.mock import patch
from graphics_splash_workspace_zero_omf16 import validate_obj,DataError
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
BACKEND='masm510-graphics-splash-workspace-physical-data-omf'
SOURCE_SHA256='596cfdca4229773b9b182b0bb10c3f339846845f50a086bb565e8390719ae7ad'
OBJECT_SHA256='e9e03ae41cd7c8e1de971bf946e0d66e61f7d3f85e2b1d8067a91f45ba1ec8d7'
TOOL_PINS={'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise DataError(s)
PROFILE_SHA256='c1e915d9ca081ea1f61101b0c580736d2d97b153f89c50ad410e185a2481a844'
def validate_unit(u):
 raw=(M/'graphics_splash_workspace_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'Exact closed physical partition profile');profile=json.loads(raw)
 need(profile['schema']=='graphics-splash-workspace-physical-data-v1' and profile['backend']==BACKEND and u==profile['unit'],'Exact versioned physical unit metadata')
 need(profile['whole_object_sha256']==OBJECT_SHA256 and profile['complete_initialized_bytes']==86000,'Exact actual whole object and unchanged extent')
 for row in profile['proof_pins']:need(H((M/row['path']).read_bytes())==row['sha256'],'Immutable comparison proof '+row['path'])
def extract_data(raw):
 # Validate full raw ownership before accepting this actual compiler output hash.
 pieces,meta=validate_obj(raw);need(H(raw)==OBJECT_SHA256,'Exact actual whole assembler object')
 meta.update(boundary='two_complete_initialized_private_PARA_SEGDEFs_53184_32816_three_PUBLICs',classification='opaque_physical_initialized_DATA',source_partition_is_engineering=True,historical_TU_proven=False,historical_C_capacity_proven=False,original_global_MAP_proven=False,authored_c_credit=0)
 return b''.join(pieces),meta
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 data:bytes
 metadata:dict
 provenance:dict

def _assemble_source_guarded(source,scratch):
 source=Path(source);content=source.read_bytes();need(H(content)==SOURCE_SHA256,'Exact standalone source bytes')
 tools={name:(M/name).read_bytes()for name in TOOL_PINS}
 for name,b in tools.items():need(H(b)==TOOL_PINS[name],'Pinned source-generation tool '+name)
 need(H(Path('/usr/bin/dosbox').read_bytes())==DOSBOX_SHA256,'Pinned DOSBox')
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 p=Path(scratch);t=p/'tools';t.mkdir();(t/'MASM.EXE').write_bytes(tools['toolchains/msc510/MASM.EXE']);(p/'UNIT.ASM').write_bytes(content)
 batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
 conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(t)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
 result=subprocess.run(['/usr/bin/dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45,check=False)
 log=(p/'MASM.LOG').read_bytes().decode('cp437');need(result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled'and '5.10'in log and re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),'Genuine MASM assembly errors: '+log)
 raw=(p/'UNIT.OBJ').read_bytes();listing=(p/'UNIT.LST').read_bytes().decode('cp437')
 for name,h in TOOL_PINS.items():need(H((M/name).read_bytes())==h,'Tool changed during generation')
 need(source.read_bytes()==content,'Source changed during generation')
 return raw,{'source_sha256':H(content),'assembler_sha256':TOOL_PINS['toolchains/msc510/MASM.EXE'],'assembler_tool_hashes':dict(TOOL_PINS),'dosbox_sha256':DOSBOX_SHA256,'build_command':command,'assembler_log':log,'assembler_listing':listing,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False,'C_function_credit':0,'C_DATA_credit':0,'original_absolute_placement_proven':False}
@contextmanager
def _generation_scope(source,scratch):
 allowed={Path(source).resolve(),Path('/usr/bin/dosbox').resolve(),*((M/name).resolve()for name in TOOL_PINS)};scratch=Path(scratch).resolve();reads=[];denied=[];old_rb=Path.read_bytes;old_rt=Path.read_text
 def permit(p):
  q=Path(p).resolve()
  if q not in allowed and not q.is_relative_to(scratch):denied.append(str(q));raise DataError('Forbidden source generation read '+str(q))
  reads.append(str(q))
 def rb(p,*a,**k):permit(p);return old_rb(p,*a,**k)
 def rt(p,*a,**k):permit(p);return old_rt(p,*a,**k)
 with patch.object(Path,'read_bytes',rb),patch.object(Path,'read_text',rt):
  for p in [M.parent/'CHESS.EXE',M/'build/exepack/TRIM5_UNPACK.EXE',M/'tests/fixtures/graphics_workspace/actual.obj',M/'graphics_splash_workspace_profile.json',Path(__file__)]:
   try:p.read_bytes()
   except DataError:pass
   else:raise DataError('Source generation guard inactive')
  yield reads,denied
 need(len(denied)==5,'Exactly five denied comparison-input probes')
def _assemble_source(source):
 with tempfile.TemporaryDirectory(prefix='bc-splash-data-')as scratch:
  with _generation_scope(source,scratch)as(reads,denied):raw,proof=_assemble_source_guarded(source,scratch)
 proof.update(source_tool_scratch_only=True,generation_reads=reads,blocked_comparison_probes=denied,comparison_reads_separate=True)
 return raw,proof
def assemble(source,unit,nasm=None):
 validate_unit(unit);source=Path(source);need(source.resolve()==(M/unit['source']).resolve()and not source.is_symlink(),'Exact regular source path')
 raw,proof=_assemble_source(source);data,metadata=extract_data(raw);need(proof['source_sha256']==unit['source_sha256'],'Source fingerprint mismatch')
 return Build(raw,data,metadata,proof)
