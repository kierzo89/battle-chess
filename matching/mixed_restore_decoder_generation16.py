"""Prototype fresh dual-input/two-process generator. No native/profile/OMF parsing.

Not installed or admitted. An independent post-GEN consumer must validate all
returned objects and provenance before any matching or SOURCE seal.
"""
from pathlib import Path
from dataclasses import dataclass
from contextlib import ExitStack
from unittest.mock import patch
import hashlib,json,os,io,builtins,stat,tempfile,subprocess,traceback,locale,codecs,re
from mixed_restore_decoder_source16 import compose_fresh,C_SOURCE_SHA256,DECODER_SOURCE_SHA256
H=lambda b:hashlib.sha256(b).hexdigest()
KIND='mixed-c-fa-authored-asm-whole-omf'
BACKEND='msc500-fa-masm510-restore-decoder-mixed-v1'
C_SOURCE='src/restore_active_arena_match.c';ASM_SOURCE='asm/link/decode_frame_directory2d13.asm'
DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
class MixedGenerationError(RuntimeError):
 def __init__(self,message,receipt,artifacts):super().__init__(message);self.receipt=receipt;self.artifacts=artifacts
@dataclass(frozen=True)
class FreshMixedBuild:
 object_bytes:bytes
 c5_sidecar_bytes:bytes
 fresh_fa_bytes:bytes
 mixed_source_bytes:bytes
 provenance:dict
 artifacts:dict
class Guard:
 def __init__(self,root,allowed):self.root=root;self.allowed=allowed;self.events={'reads':[],'writes':[],'blocked':[],'FIFO':[]};self.fds={}
 def allow(self,name,write,api):
  if isinstance(name,int):
   if name in self.fds:p,w=self.fds[name];assert not write or w
   else:assert stat.S_ISFIFO(os.fstat(name).st_mode),'Only process PIPE/FIFO descriptors';self.events['FIFO'].append({'fd':name,'api':api});return
  else:p=Path(name).resolve()
  if not(p.is_relative_to(self.root)or(not write and p in self.allowed)):
   self.events['blocked'].append({'path':str(p),'api':api,'writing':write});raise ValueError('Mixed source-only GEN denied '+str(p))
  if write and p.suffix.lower()in ('.obj','.lib','.exe'):raise ValueError('No host-written executable/library/object payload')
  self.events['writes'if write else'reads'].append({'path':str(p),'api':api})
 def __enter__(self):
  self.original=(Path.open,builtins.open,io.open,os.open,os.read,os.write,os.close);po,bo,io_,oo,rd,wr,cl=self.original
  writing=lambda mode:any(x in str(mode)for x in'wax+')
  def popen(p,mode='r',*a,**kw):self.allow(p,writing(mode),'Path.open');return po(p,mode,*a,**kw)
  def bopen(p,mode='r',*a,**kw):self.allow(p,writing(mode),'builtins.open');return bo(p,mode,*a,**kw)
  def iopen(p,mode='r',*a,**kw):self.allow(p,writing(mode),'io.open');return io_(p,mode,*a,**kw)
  def osopen(p,flags,*a,**kw):
   assert kw.get('dir_fd')is None,'No relative descriptor bypass';w=bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND));self.allow(p,w,'os.open');fd=oo(p,flags,*a,**kw);self.fds[fd]=(Path(p).resolve(),w);return fd
  def read(fd,n):self.allow(fd,False,'os.read');return rd(fd,n)
  def write(fd,b):self.allow(fd,True,'os.write');return wr(fd,b)
  def close(fd):self.fds.pop(fd,None);return cl(fd)
  self.stack=ExitStack()
  for obj,name,fn in [(Path,'open',popen),(builtins,'open',bopen),(io,'open',iopen),(os,'open',osopen),(os,'read',read),(os,'write',write),(os,'close',close)]:self.stack.enter_context(patch.object(obj,name,fn))
  return self
 def __exit__(self,*a):return self.stack.__exit__(*a)
def _process(root,toolroot,command,phase,calls):
 assert not(root/'UNIT.OBJ').exists(),'No old scratch OBJ'
 batch='@echo off\r\nset PATH=T:\\\r\n'+command+' > C:\\BUILD.LOG\r\nif errorlevel 1 goto failed\r\necho success > SUCCESS.TXT\r\ngoto done\r\n:failed\r\necho failed > FAILED.TXT\r\n:done\r\nexit\r\n';(root/'BUILD.BAT').write_bytes(batch.encode('ascii'))
 conf='[sdl]\nfullscreen=false\noutput=surface\n[dosbox]\nmemsize=16\n[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n[autoexec]\nmount c "'+str(root)+'"\nmount t "'+str(toolroot)+'" -ro\nc:\nBUILD.BAT\n';(root/'dosbox.conf').write_text(conf)
 argv=['/usr/bin/dosbox','-conf',str(root/'dosbox.conf'),'-noconsole'];p=subprocess.Popen(argv,env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.PIPE);row={'phase':phase,'pid':p.pid,'argv':argv,'command':command,'terminal':False,'reaped':False};calls.append(row)
 try:out,err=p.communicate(timeout=45)
 except subprocess.TimeoutExpired:
  p.kill();out,err=p.communicate();row.update(terminal=True,reaped=True,returncode=p.returncode,timeout=True);raise
 row.update(terminal=True,reaped=True,returncode=p.returncode);(root/'STDOUT.bin').write_bytes(out);(root/'STDERR.bin').write_bytes(err)
 log=(root/'BUILD.LOG').read_bytes().decode('cp437');assert p.returncode==0 and(root/'SUCCESS.TXT').exists()and not(root/'FAILED.TXT').exists(),log
 return log

def assemble(source,project):
 """One public callback, one fresh C5 and one fresh MASM; never reads a fixture."""
 project=Path(project).resolve();source=Path(source).resolve();decoder=project/ASM_SOURCE
 assert source==project/C_SOURCE and not source.is_symlink()and not decoder.is_symlink()
 # Source/tools configuration only; these hashes never describe target payload.
 import msc
 msc.validate_source(source.read_bytes());manifest,msc_hashes=msc.validate_toolchain(compiler='msc500')
 toolpins={**{'toolchains/msc500/'+n:h for n,h in msc_hashes.items()},'toolchains/msc500/manifest.json':manifest,'config/msc500.json':H((project/'config/msc500.json').read_bytes()),'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
 allowed={source:C_SOURCE_SHA256,decoder:DECODER_SOURCE_SHA256,Path('/usr/bin/dosbox').resolve():DOSBOX_SHA256,**{project/n:h for n,h in toolpins.items()}}
 for p,h in allowed.items():assert p.is_file()and not p.is_symlink()and H(p.read_bytes())==h
 prewarm={'locale':locale.getpreferredencoding(False),'utf8':codecs.lookup('utf8').name,'cp437':codecs.lookup('cp437').name};calls=[];artifacts={};error=None;receipt={};raw=sidecar=fa=mixed=None
 with tempfile.TemporaryDirectory(prefix='bc-fresh-mixed-restore-decoder-')as tmp:
  root=Path(tmp).resolve();croot=root/'C5';aroot=root/'MASM';croot.mkdir();aroot.mkdir();guard=Guard(root,allowed)
  try:
   with guard:
    probes=[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'build/restore51-genuine-FA-one-C5-root-actual/scratch/UNIT.OBJ',Path(__file__).with_name('mixed_restore_decoder_profile.json'),project/'config/units.json']
    for target in probes:
     for name,fn in [('Path',lambda p:p.read_bytes()),('io',lambda p:io.open(p,'rb')),('builtin',lambda p:builtins.open(p,'rb')),('os',lambda p:os.open(p,os.O_RDONLY))]:
      try:fn(target)
      except ValueError:pass
      else:raise AssertionError('Active GEN denial failed '+name)
    r,w=os.pipe()
    try:os.write(w,b'fifo');assert os.read(r,4)==b'fifo'
    finally:os.close(r);os.close(w)
    for p,h in allowed.items():assert H(p.read_bytes())==h
    cbytes=source.read_bytes();decoderbytes=decoder.read_bytes();(croot/'UNIT.C').write_bytes(cbytes)
    clog=_process(croot,project/'toolchains/msc500','T:\\CL.EXE /c /AS /Gs /Os /Zi /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C','C5',calls)
    sidecar=(croot/'UNIT.OBJ').read_bytes();fa=(croot/'UNIT.ASM').read_bytes();assert sidecar and fa
    mixed,transform=compose_fresh(fa,decoderbytes,c_source_sha256=H(cbytes));(aroot/'UNIT.ASM').write_bytes(mixed)
    alog=_process(aroot,project/'toolchains/msc510','T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;','MASM',calls)
    assert '5.10'in alog and re.search(r'\b0 Warning Errors',alog)and re.search(r'\b0 Severe\s+Errors',alog),alog
    raw=(aroot/'UNIT.OBJ').read_bytes();assert raw
    for p,h in allowed.items():assert H(p.read_bytes())==h
  except BaseException as exc:error={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
  finally:
   # Scope is closed before retention. This inventory is never fed to a generator.
   artifacts={str(p.relative_to(root)):p.read_bytes()for p in root.rglob('*')if p.is_file()}
   receipt={'status':'FAILED'if error else'COMPLETE','error':error,'kind':KIND,'backend':BACKEND,'source_SHA256':C_SOURCE_SHA256,'authored_ASM_SHA256':DECODER_SOURCE_SHA256,'flags':['/AS','/Gs','/Os','/Zi'],'listing_flag':'/FaC:\\UNIT.ASM','MASM_flags':['/Mx'],'tool_hashes':toolpins,'compiler_manifest_SHA256':manifest,'allowed_reads':{str(p):h for p,h in allowed.items()},'processes':calls,'guard':guard.events,'guard_closed':True,'source_tools_freshscratch_only':True,'transform':transform if 'transform'in locals()else None,'raw_mixed_SHA256':H(raw)if raw else None,'C5_sidecar_SHA256':H(sidecar)if sidecar else None,'fresh_FA_SHA256':H(fa)if fa else None,'mixed_ASM_SHA256':H(mixed)if mixed else None,'prewarm':prewarm,'native_original_oldOBJ_profile_inside_GEN':False,'credit':0}
 if error:raise MixedGenerationError(error['message'],receipt,artifacts)
 if not([x['phase']for x in calls]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 for x in calls)and len(guard.events['blocked'])==20):raise MixedGenerationError('Incomplete real two-phase process/guard closure',receipt,artifacts)
 return FreshMixedBuild(raw,sidecar,fa,mixed,receipt,artifacts)
