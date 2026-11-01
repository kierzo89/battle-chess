"""Pinned public generators; adapter preflight/local checks remain outside GEN.

Each actual fresh TemporaryDirectory arms target-free host file capabilities.
No old object is a generator input. Observe scratch raw read without new reads.
This draft does not assert fine process tracing: source_process_count is null.
"""
from pathlib import Path
from contextlib import contextmanager,ExitStack
from unittest.mock import patch
import builtins,io,os,stat,tempfile,subprocess,importlib,shutil
from cohort import need,sha
import mixed_source_dispatch_evaluation16 as mixed

class SourceObserver:
 def __init__(self,project,descriptor):
  self.project=Path(project).resolve();self.descriptor=descriptor;self.events=[];self.current=None;self.roots=[];self.poisoned=False;self.parallel=None;self._packet_live_results={}
 def select_c(self,source,flags,compiler,source_name,dosbox):
  matches=[r for r in self.descriptor['rows']if r['kind']in ('c-whole-omf','common-whole-omf')and self.project/r['source']==Path(source).resolve()and r['compiler']==compiler and r['compiler_flags']==list(flags)and r['source_name']==source_name]
  need(len(matches)==1,'unreviewed C source/flags/compiler/basename');r=matches[0];need(dosbox==r.get('dosbox_keyword'),'unreviewed C DOSBox override');return r
 @contextmanager
 def install(self,check,source_inputs):
  self.real_c=check.compile_c;self.real_temp=tempfile.TemporaryDirectory;self.old=(builtins.open,io.open,os.open,Path.read_bytes,Path.write_bytes,Path.write_text);self.real_popen=subprocess.Popen
  # Resolve/import pinned modules before source phase; no native/proof capability in GEN.
  modules={r['public_adapter']['module']:importlib.import_module(r['public_adapter']['module'])for r in self.descriptor['rows']if r.get('public_adapter')}
  with ExitStack()as stack:
   for obj,name,new in [(check,'compile_c',self.compile_c),(source_inputs,'compile_c',self.compile_c),(tempfile,'TemporaryDirectory',self.temporary),(builtins,'open',self.bopen),(io,'open',self.iopen),(os,'open',self.osopen),(Path,'read_bytes',lambda p:self.read_bytes(p)),(Path,'write_bytes',lambda p,b:self.write_bytes(p,b)),(Path,'write_text',lambda p,t,*a,**kw:self.write_text(p,t,*a,**kw)),(subprocess,'Popen',self.popen)]:stack.enter_context(patch.object(obj,name,new))
   for name,module in modules.items():
    real=module.assemble
    def wrapped(*a,_name=name,_real=real,**kw):
     matches=[r for r in self.descriptor['rows']if r.get('public_adapter',{}).get('module')==_name and self.project/r['source']==Path(a[0]).resolve()];need(len(matches)==1,'unreviewed ASM source/route');return self.call(matches[0],lambda:_real(*a,**kw))
    stack.enter_context(patch.object(module,'assemble',wrapped))
   yield self
 def compile_c(self,source,flags,*,compiler='msc500',source_name='UNIT.C',dosbox=None):
  r=self.select_c(source,flags,compiler,source_name,dosbox);kw={'compiler':compiler,'source_name':source_name}
  if dosbox is not None:kw['dosbox']=dosbox
  if self.parallel is not None and r["order_slot"]in self.parallel.rows:
   from parallel_compile import ParallelCompiler
   need(type(self.parallel)is ParallelCompiler and self.parallel.observer is self and self.current is None and not self.poisoned,'owned isolated compiler pool')
   try:
    result,event=self.parallel.consume(r);self.events.append(event);return result
   except BaseException:self.poisoned=True;raise
  return self.call(r,lambda:self.real_c(source,flags,**kw))
 def call(self,row,fn):
  if self.parallel is not None:self.parallel.quiesce()
  need(self.current is None and not self.poisoned,'no nested/reused poisoned source phase');event={'slot':row['order_slot'],'raw_reads':[],'processes':[],'denials':[],'roots':[],'fresh_witness':False};self.current=(row,event)
  try:
   result=fn();need(not self.roots and event['roots']and event['processes'],'actual fresh scratch and process required')
   need(all(p['object'].poll()==0 for p in event['processes']),'all source processes closed/reaped successful')
   raw=result.object_bytes;need(raw and any(h==sha(raw)for h in event['raw_reads']),'public raw must equal actual fresh scratch OBJ read')
   if row['kind']=='c-whole-omf':self._packet_live_results[row['order_slot']]=result
   if row['kind']==mixed.KIND:mixed.finish_event(self,row,event,result)
   event.update(raw_sha256=sha(raw),fresh_witness=True,source_process_count=None,process_detail_claim='Observed real Popen objects; fine subprocess lifecycle tracing not implemented')
   event['submitted']={p:{'sha256':sha(b),'size':len(b)}for p,b in event.get('submitted',{}).items()}
   event['processes']=[{'pid':p['object'].pid,'argv':p['argv'],'host_returncode':p['object'].returncode}for p in event['processes']];self.events.append(event);return result
  except BaseException:self.poisoned=True;raise
  finally:self.current=None
 def temporary(self,*a,**kw):
  real=self.real_temp(*a,**kw)
  if self.current is None:return real
  observer=self;root=Path(real.name).resolve();need(not observer.roots,'one fresh generation scratch at a time');observer.roots.append(root);observer.current[1]['roots'].append(str(root))
  # Existing provider contextmanagers sometimes yield obj.name and call cleanup
  # without __enter__. Creation is the genuine fresh scratch boundary in both forms.
  class Scratch:
   closed=False
   def __getattr__(self,n):return getattr(real,n)
   def finish(self,fn):
    try:return fn()
    finally:
     if not self.closed:
      need(observer.roots==[root],'scratch lifetime');observer.roots.pop();self.closed=True
   def __enter__(self):return real.__enter__()
   def __exit__(self,*args):return self.finish(lambda:real.__exit__(*args))
   def cleanup(self):return self.finish(real.cleanup)
  return Scratch()
 def authorize(self,name,writing=False,dir_fd=None):
  if not self.roots:return
  if isinstance(name,int):need(stat.S_ISFIFO(os.fstat(name).st_mode),'only process pipe handles');return
  p=(Path(os.readlink('/proc/self/fd/'+str(dir_fd)))/os.fsdecode(name))if dir_fd is not None else Path(os.fsdecode(name));p=p.resolve();row,event=self.current;root=self.roots[0]
  allowed={self.project/row['source'],*(self.project/n for n in row['generation_tools'])}
  if row['kind']==mixed.KIND:allowed.update(self.project/s['path']for s in row['generation_sources'])
  for k in ['DOSBox','NASM']:
   q=Path(self.descriptor['tools'][k]['path']);allowed.add(q if q.is_absolute()else self.project/q)
  if p.is_relative_to(root):need(not(writing and p.suffix.lower()in('.obj','.lib','.exe')and p.name.upper()!='MASM.EXE'),'no host-written object/library/executable payload');return
  if not writing and p in allowed:return
  event['denials'].append(str(p));raise ValueError('SOURCE GEN denied '+str(p))
 def bopen(self,n,mode='r',*a,**kw):self.authorize(n,any(c in str(mode)for c in'wax+'));return self.old[0](n,mode,*a,**kw)
 def iopen(self,n,mode='r',*a,**kw):self.authorize(n,any(c in str(mode)for c in'wax+'));return self.old[1](n,mode,*a,**kw)
 def osopen(self,n,flags,*a,**kw):self.authorize(n,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)),kw.get('dir_fd'));return self.old[2](n,flags,*a,**kw)
 def read_bytes(self,p):
  raw=self.old[3](p)
  if self.roots and Path(p).resolve().is_relative_to(self.roots[0])and Path(p).suffix.lower()=='.obj':self.current[1]['raw_reads'].append(sha(raw))
  if self.roots and self.current[0]['kind']==mixed.KIND:mixed.record_read(self,p,raw)
  return raw
 def write_bytes(self,p,b):
  if self.roots:self.capture(p,bytes(b))
  return self.old[4](p,b)
 def write_text(self,p,text,*a,**kw):
  if self.roots:self.capture(p,text.encode(kw.get('encoding')or'utf-8'))
  return self.old[5](p,text,*a,**kw)
 def capture(self,p,raw):
  self.authorize(p,True);self.current[1].setdefault('submitted',{})[str(Path(p).resolve())]=raw
 def popen(self,argv,*a,**kw):
  if not self.roots:
   need(self.current is None,'no child process during comparison-only adapter preflight');return self.real_popen(argv,*a,**kw)
  row,event=self.current;root=self.roots[0];need(isinstance(argv,(tuple,list))and argv,'literal process command');exe=Path(shutil.which(str(argv[0]))or str(argv[0])).resolve();tool=self.descriptor['tools'][row['generator']];need(exe==Path(tool['path']).resolve(),'only descriptor source tool executable')
  if row['kind']==mixed.KIND:
   phase=mixed.before_process(self,row,event,root,argv,kw);process=self.real_popen(argv,*a,**kw);event['processes'].append({'object':process,'argv':list(argv),'mixed_phase':phase});return process
  submitted=event.get('submitted',{});source=root/row['source_name'];need(str(source)in submitted and sha(submitted[str(source)])==row['source_sha256'],'exact submitted real source')
  need(not(root/'UNIT.OBJ').exists(),'no stale scratch object')
  if row['generator']=='DOSBox':
   need(list(argv[1:])==['-conf',str(root/'dosbox.conf'),'-noconsole'],'exact source DOSBox invocation');conf=submitted.get(str(root/'dosbox.conf'),b'').decode('ascii');mounts=[x for x in conf.splitlines()if x.lower().startswith('mount ')];need(len(mounts)==2 and mounts[0]=='mount c "'+str(root)+'"','only source scratch mount');toolroots=[self.project/'toolchains'/row['compiler']]if row['kind']!='asm-whole-omf'else[self.project/'toolchains/msc510',root/'tools'];need(mounts[1]in ['mount t "'+str(t)+'" -ro'for t in toolroots],'only genuine tool mount')
   copied=submitted.get(str(root/'tools/MASM.EXE'))
   if copied is not None:need(sha(copied)==row['generation_tools']['toolchains/msc510/MASM.EXE'],'copied MASM identity')
  else:need(Path(kw.get('cwd','')).resolve()==root and list(argv[1:])==row['generator_argv_tail'],'exact symbolic NASM invocation')
  process=self.real_popen(argv,*a,**kw);event['processes'].append({'object':process,'argv':list(argv)});return process
