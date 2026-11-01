from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import os,io,builtins,stat,tempfile,json
@contextmanager
def scope(source,project):
 M=Path(project).resolve()
 cfg=M/'config/msc500.json';config=json.loads(cfg.read_text());allowed={source.resolve(),cfg.resolve(),(M/'toolchains/msc500/manifest.json').resolve(),Path('/usr/bin/dosbox').resolve()}|{(M/'toolchains/msc500'/r['name']).resolve()for r in config['files']};old=(builtins.open,io.open,os.open,tempfile.TemporaryDirectory);roots=set();events={'reads':[],'writes':[],'blocked':[],'pipe_FDs_for_subprocess_only':[]}
 def check(name,write,dir_fd=None):
  if isinstance(name,int):
   # subprocess.PIPE is a fresh OS pipe, never a regular reference-file descriptor.
   if not write and stat.S_ISFIFO(os.fstat(name).st_mode):events['pipe_FDs_for_subprocess_only'].append(name);return
   raise ValueError('Regular/inherited file descriptor forbidden')
  if dir_fd is not None:
   root=Path(os.readlink('/proc/self/fd/'+str(dir_fd))).resolve();p=(root/os.fsdecode(name)).resolve()
  else:p=Path(os.fsdecode(name)).resolve()
  ok=any(p==root or p.is_relative_to(root)for root in roots)or(not write and p in allowed)
  if not ok:events['blocked'].append(str(p));raise ValueError('Source-only generation denied '+str(p))
  events['writes'if write else'reads'].append(str(p))
 def op(name,mode='r',*a,**k):check(name,any(v in str(mode)for v in'wax+'));return old[0](name,mode,*a,**k)
 def ip(name,mode='r',*a,**k):check(name,any(v in str(mode)for v in'wax+'));return old[1](name,mode,*a,**k)
 def osp(name,flags,*a,**k):check(name,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)),k.get('dir_fd'));return old[2](name,flags,*a,**k)
 @contextmanager
 def td(*a,**k):
  obj=old[3](*a,**k);root=Path(obj.name).resolve();roots.add(root)
  try:yield obj.name
  finally:obj.cleanup();roots.remove(root)
 with patch.object(builtins,'open',op),patch.object(io,'open',ip),patch.object(os,'open',osp),patch.object(tempfile,'TemporaryDirectory',td):yield events
