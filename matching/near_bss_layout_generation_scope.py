"""NearBSS190 source/tools/new compiler scratch only. No comparison inputs in scope."""
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import builtins,io,os,stat,tempfile,locale,codecs,json
@contextmanager
def scope(source,project,probes):
 source=Path(source).resolve();M=Path(project).resolve();allowed={source,Path('/usr/bin/nasm').resolve()}
 tempfile.gettempdir();locale.getpreferredencoding(False);codecs.lookup('utf8');codecs.lookup('cp437');r,w=os.pipe();os.close(r);os.close(w)
 old=(Path.open,builtins.open,io.open,os.open,os.read,os.write,os.close,tempfile.TemporaryDirectory);roots=set();fds={};events={'reads':[],'writes':[],'blocked':[],'FIFO_descriptors':[],'source_tools_new_scratch_only':True,'native_fixture_evidence_inputs':False}
 def check(name,write=False,dir_fd=None):
  if isinstance(name,int):
   if name in fds:return check(fds[name],write)
   if stat.S_ISFIFO(os.fstat(name).st_mode):events['FIFO_descriptors'].append(name);return
   raise ValueError('NearBSS190 regular/inherited descriptor denied')
  p=(Path(os.readlink('/proc/self/fd/'+str(dir_fd)))/os.fsdecode(name)).resolve()if dir_fd is not None else Path(os.fsdecode(name)).resolve()
  if not(any(p==root or p.is_relative_to(root)for root in roots)or(not write and p in allowed)):events['blocked'].append(str(p));raise ValueError('NearBSS190 source-only denied '+str(p))
  events['writes'if write else'reads'].append(str(p));return p
 def mw(mode):return any(c in str(mode)for c in'wax+')
 def po(p,mode='r',*a,**k):check(p,mw(mode));return old[0](p,mode,*a,**k)
 def bo(p,mode='r',*a,**k):check(p,mw(mode));return old[1](p,mode,*a,**k)
 def ip(p,mode='r',*a,**k):check(p,mw(mode));return old[2](p,mode,*a,**k)
 def oo(p,flags,*a,**k):
  path=check(p,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)),k.get('dir_fd'));fd=old[3](p,flags,*a,**k);fds[fd]=path;return fd
 def rd(fd,n):check(fd);return old[4](fd,n)
 def wr(fd,b):check(fd,True);return old[5](fd,b)
 def cl(fd):fds.pop(fd,None);return old[6](fd)
 @contextmanager
 def td(*a,**k):
  obj=old[7](*a,**k);root=Path(obj.name).resolve();roots.add(root)
  try:yield obj.name
  finally:obj.cleanup();roots.remove(root)
 with patch.object(Path,'open',po),patch.object(builtins,'open',bo),patch.object(io,'open',ip),patch.object(os,'open',oo),patch.object(os,'read',rd),patch.object(os,'write',wr),patch.object(os,'close',cl),patch.object(tempfile,'TemporaryDirectory',td):
  for p in probes:
   for fn in [lambda p:p.read_bytes(),lambda p:builtins.open(p,'rb'),lambda p:io.open(p,'rb'),lambda p:os.open(p,os.O_RDONLY)]:
    try:fn(Path(p))
    except ValueError:pass
    else:raise ValueError('NearBSS190 guard denial probe accepted')
  yield events
 assert len(events['blocked'])==20 and len(set(events['blocked']))==5
