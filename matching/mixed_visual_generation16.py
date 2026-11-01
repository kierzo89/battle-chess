"""Prototype fresh dual-input/two-process generator. No native/profile/OMF parsing.

Not installed or admitted. An independent post-GEN consumer must validate all
returned objects and provenance before any matching or SOURCE seal.
"""
from pathlib import Path
from dataclasses import dataclass
from contextlib import ExitStack
from unittest.mock import patch
import hashlib,json,os,io,builtins,stat,tempfile,subprocess,traceback,locale,codecs,re
from mixed_visual_source16 import compose_fresh,RECIPES
H=lambda b:hashlib.sha256(b).hexdigest()
KIND='mixed-c-fa-authored-asm-whole-omf'
BACKEND='msc500-fa-masm510-visual-mixed-v1'

DOSBOX_SHA256='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
_LIVE_CAP=object()
class MixedGenerationError(RuntimeError):
 def __init__(self,message,receipt,artifacts):super().__init__(message);self.receipt=receipt;self.artifacts=artifacts
@dataclass(frozen=True)
class FreshMixedBuild:
 object_bytes:bytes
 c5_sidecar_bytes:bytes
 sidecars:tuple
 fas:tuple
 fresh_fa_bytes:bytes
 mixed_source_bytes:bytes
 provenance:dict
 artifacts:dict
 _cap:object
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
 project=Path(project).resolve();source=Path(source).resolve();matches=[k for k,r in RECIPES.items()if source==project/r['C_SOURCE']];assert len(matches)==1;kind=matches[0];r=RECIPES[kind];decoder=project/r['ASM_SOURCE']
 import msc
 assert Path(msc.__file__).resolve().parent==project,'executing compiler root differs'
 for p in r['parts']:msc.validate_source((project/p['source']).read_bytes())
 manifest,msc_hashes=msc.validate_toolchain(compiler='msc500')
 toolpins={**{'toolchains/msc500/'+n:h for n,h in msc_hashes.items()},'toolchains/msc500/manifest.json':manifest,'config/msc500.json':H((project/'config/msc500.json').read_bytes()),'toolchains/msc510/MASM.EXE':'1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f','toolchains/msc510/manifest.json':'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4','toolchains/msc510/LICENSE':'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4','config/msc510.json':'058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
 allowed={**{project/p['source']:p['sha256']for p in r['parts']},decoder:r['DECODER_SOURCE_SHA256'],Path('/usr/bin/dosbox').resolve():DOSBOX_SHA256,**{project/n:h for n,h in toolpins.items()}}
 for p,h in allowed.items():assert p.is_file()and not p.is_symlink()and H(p.read_bytes())==h
 prewarm={'locale':locale.getpreferredencoding(False),'utf8':codecs.lookup('utf8').name,'cp437':codecs.lookup('cp437').name};calls=[];artifacts={};error=None;receipt={};raw=mixed=None;sidecars=[];fas=[]
 with tempfile.TemporaryDirectory(prefix='bc-fresh-visual-'+kind+'-')as tmp:
  root=Path(tmp).resolve();aroot=root/'MASM';aroot.mkdir();croots=[]
  for i in range(len(r['parts'])):p=root/('C5'if i==0 else'C5_'+str(i));p.mkdir();croots.append(p)
  guard=Guard(root,allowed)
  try:
   with guard:
    probes=[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'build/motion783-genuine-FA-one-C5-root-actual/scratch/UNIT.OBJ',Path(__file__).with_name('mixed_visual_profile.json'),project/'config/units.json']
    for target in probes:
     for name,fn in [('Path',lambda p:p.read_bytes()),('io',lambda p:io.open(p,'rb')),('builtin',lambda p:builtins.open(p,'rb')),('os',lambda p:os.open(p,os.O_RDONLY))]:
      try:fn(target)
      except ValueError:pass
      else:raise AssertionError('Active GEN denial failed '+name)
    rd,wr=os.pipe()
    try:os.write(wr,b'fifo');assert os.read(rd,4)==b'fifo'
    finally:os.close(rd);os.close(wr)
    for p,h in allowed.items():assert H(p.read_bytes())==h
    decoderbytes=decoder.read_bytes()
    for i,(part,croot)in enumerate(zip(r['parts'],croots)):
     cbytes=(project/part['source']).read_bytes();(croot/'UNIT.C').write_bytes(cbytes)
     command='T:\\CL.EXE /c '+' '.join(part['flags'])+' /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C'
     _process(croot,project/'toolchains/msc500',command,'C5'if i==0 else'C5_'+str(i),calls)
     sidecars.append((croot/'UNIT.OBJ').read_bytes());fas.append((croot/'UNIT.ASM').read_bytes());assert sidecars[-1]and fas[-1]
    mixed,transform=compose_fresh(tuple(fas),decoderbytes,kind=kind,source_hashes=[p['sha256']for p in r['parts']]);(aroot/'UNIT.ASM').write_bytes(mixed)
    alog=_process(aroot,project/'toolchains/msc510','T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;','MASM',calls)
    assert '5.10'in alog and re.search(r'\b0 Warning Errors',alog)and re.search(r'\b0 Severe\s+Errors',alog),alog
    raw=(aroot/'UNIT.OBJ').read_bytes();assert raw
    for p,h in allowed.items():assert H(p.read_bytes())==h
  except BaseException as exc:error={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
  finally:
   artifacts={str(p.relative_to(root)):p.read_bytes()for p in root.rglob('*')if p.is_file()}
   receipt={'status':'FAILED'if error else'COMPLETE','error':error,'kind':KIND,'backend':BACKEND,'profile':kind,'source_SHA256':r['C_SOURCE_SHA256'],'source_hashes':[p['sha256']for p in r['parts']],'authored_ASM_SHA256':r['DECODER_SOURCE_SHA256'],'flags':r['parts'][0]['flags'],'all_flags':[p['flags']for p in r['parts']],'listing_flag':'/FaC:\\UNIT.ASM','MASM_flags':['/Mx'],'tool_hashes':toolpins,'compiler_manifest_SHA256':manifest,'allowed_reads':{str(p):h for p,h in allowed.items()},'processes':calls,'guard':guard.events,'guard_closed':True,'source_tools_freshscratch_only':True,'transform':transform if 'transform'in locals()else None,'raw_mixed_SHA256':H(raw)if raw else None,'C5_sidecar_SHA256':H(sidecars[0])if sidecars else None,'sidecar_hashes':[H(x)for x in sidecars],'FA_hashes':[H(x)for x in fas],'mixed_ASM_SHA256':H(mixed)if mixed else None,'prewarm':prewarm,'native_original_oldOBJ_profile_inside_GEN':False,'credit':0}
 if error:raise MixedGenerationError(error['message'],receipt,artifacts)
 phases=['C5']+['C5_'+str(i)for i in range(1,len(r['parts']))]+['MASM']
 if not([x['phase']for x in calls]==phases and all(x['terminal']and x['reaped']and x['returncode']==0 for x in calls)and len(guard.events['blocked'])==20):raise MixedGenerationError('Incomplete actual processes/guard closure',receipt,artifacts)
 return FreshMixedBuild(raw,sidecars[0],tuple(sidecars),tuple(fas),fas[0],mixed,receipt,artifacts,_LIVE_CAP)
