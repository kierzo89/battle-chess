"""One target-free authentic LINK from an in-process SOURCE seal. No EXE execution."""
from pathlib import Path
from unittest.mock import patch
import sys,hashlib,json,os,io,builtins,stat,tempfile,subprocess,re,traceback
from cohort import need,sha
H=sha
D=Path(__file__).resolve().parent

def parse_link_diagnostics(log,status):
 """All LINK3.65 prefixes; only exact unresolved-only diagnostics are partial.

 A successful DOSBox host exit or an emitted MZ cannot override LINK errors.
 The summary counts unresolved names, not the single L2029 heading.
 """
 need(type(log)is str and status in('success','link_failed')and '\x00'not in log,'LINK diagnostic text/status')
 lines=log.splitlines();diagnostics=[];summaries=[];names=[];cases={};current=None;unresolved_line=None
 banner=re.compile(r'^\s*Microsoft\s+\(R\)\s+Overlay\s+Linker\s+Version\s+3\.65\s*$',re.I)
 need(sum(bool(banner.fullmatch(line))for line in lines)==1,'one authentic LINK3.65 banner')
 diag=re.compile(r'^\s*(?:(?P<prefix>\S[^\r\n]*?)\s*:\s*)?(?P<severity>fatal\s+error|error|warning)\s+(?P<code>L\d{4})\s*:\s*(?P<message>\S.*?)\s*$',re.I)
 summary=re.compile(r'^\s*There\s+(?:was|were)\s+(\d+)\s+errors?\s+detected\.?\s*$',re.I)
 symbol=re.compile(r'^\s*([^\s:]+)\s+in\s+file\(s\)\s*:\s*$',re.I)
 suspect=re.compile(r'(?:^|:)\s*(?:fatal(?:\s+error)?|error|warning)\b|\b(?:fatal\s+error|error|warning)\s+L\w*|\bL\d{3,6}\s*:',re.I)
 for number,line in enumerate(lines,1):
  m=diag.fullmatch(line)
  if m:
   d={'line':number,'prefix':(m['prefix']or'').strip(),'severity':' '.join(m['severity'].lower().split()),'code':m['code'].upper(),'message':m['message'],'raw_line':line};diagnostics.append(d)
   if d['code']=='L2029':
    need(unresolved_line is None and d['severity']=='error'and d['message'].lower()=='unresolved externals:','one exact L2029 unresolved heading');unresolved_line=number
   current=None;continue
  m=summary.fullmatch(line)
  if m:summaries.append({'line':number,'count':int(m[1]),'raw_line':line});current=None;continue
  need(not suspect.search(line)and not re.match(r'^\s*There\s+(?:was|were)\b',line,re.I),'unparsed or malformed LINK diagnostic: '+line)
  m=symbol.fullmatch(line)
  if m:
   need(unresolved_line is not None and not summaries,'undefined block outside unresolved section or after summary');current=m[1];need(current not in cases,'duplicate unresolved name block');names.append(current);cases[current]=[];continue
  if not line.strip():continue
  if unresolved_line is not None and not summaries:
   need(current is not None and line[:1].isspace(),'malformed unresolved object-case line');tokens=line.split();need(tokens and all(re.fullmatch(r'[^()\s]+\.(?:OBJ|LIB)(?:\([^()\r\n]+\))?',token,re.I)for token in tokens),'malformed unresolved object-file cases');cases[current].extend(tokens)
 need(all(d['severity']=='error'and d['code']=='L2029'for d in diagnostics),'non-unresolved LINK diagnostic: '+repr(diagnostics))
 need(len(summaries)<=1,'duplicate LINK error summary')
 if status=='success':
  need(not diagnostics and not names and(not summaries or summaries[0]['count']==0),'LINK success marker contradicts diagnostics or summary')
 else:
  need(len(diagnostics)==1 and diagnostics[0]['code']=='L2029'and names and all(cases[n]for n in names),'failed LINK must contain one complete unresolved-only diagnostic')
  need(len(summaries)==1 and summaries[0]['line']>diagnostics[0]['line']and summaries[0]['count']==len(names),'actual LINK summary must equal complete unique unresolved-name count')
 return {'policy':'link365-all-prefix-errors-unresolved-summary-v1','diagnostics':diagnostics,'summary_error_count':summaries[0]['count']if summaries else None,'undefined_symbols':sorted(names),'undefined_object_cases':cases,'all_log_lines_examined':len(lines),'status_marker':status,'non_unresolved_diagnostics':[]}

def emit_link(seal,descriptor,project,components,out):
 from pipeline import SourceSeal
 need(type(seal)is SourceSeal and seal.valid(),'internal same-run SOURCE capability, not arbitrary JSON')
 M=Path(project).resolve();components=Path(components).resolve();out=Path(out).absolute();need(not out.exists(),'exclusive LINK output');bindings={'rows':seal.rows};tools=descriptor['tools'];count=len(seal.rows)
 # Whole SOURCE identities were checked before arming LINK GEN. No target/expected payload enters scratch.
 allowed={Path(r['object_path']).resolve()for r in bindings['rows']};toolpaths={}
 for k in ['LINK','SLIBC','LIBH','DOSBox']:
  p=Path(tools[k]['path']);p=p if p.is_absolute()else M/p;p=p.resolve();need(H(p.read_bytes())==tools[k]['sha256'],'genuine tool '+k);toolpaths[k]=p;allowed.add(p)
 need(len(bindings['rows'])==len(allowed)-4==count,'exact descriptor SOURCE set')
 out.mkdir();(out/'one-LINK.claim').open('x').close();saved={};reads=[];blocked=[];process=None;error=None;rows=[]
 try:
  with tempfile.TemporaryDirectory(prefix='bc-descriptor-link-')as tmp:
   root=Path(tmp).resolve();old=(builtins.open,io.open,os.open)
   def authorize(name,writing,dir_fd=None):
    if isinstance(name,int):
     need(not writing and stat.S_ISFIFO(os.fstat(name).st_mode),'only subprocess PIPE FIFO descriptor');return
    if dir_fd is not None:p=(Path(os.readlink('/proc/self/fd/'+str(dir_fd)))/os.fsdecode(name)).resolve()
    else:p=Path(os.fsdecode(name)).resolve()
    if not(p.is_relative_to(root)or(not writing and p in allowed)):
     blocked.append(str(p));raise ValueError('source-only LINK denied '+str(p))
    if not writing:reads.append(str(p))
   def bop(name,mode='r',*a,**kw):authorize(name,any(x in str(mode)for x in'wax+'));return old[0](name,mode,*a,**kw)
   def iop(name,mode='r',*a,**kw):authorize(name,any(x in str(mode)for x in'wax+'));return old[1](name,mode,*a,**kw)
   def osp(name,flags,*a,**kw):authorize(name,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)),kw.get('dir_fd'));return old[2](name,flags,*a,**kw)
   probes=[M.parent/'CHESS.EXE',M/'build/exepack/TRIM5_UNPACK.EXE',D/'comparison-proof.json',components/'runtime/runtime_crt0.obj',M/'config/units.json']
   with patch.object(builtins,'open',bop),patch.object(io,'open',iop),patch.object(os,'open',osp):
    for p in probes:
     for api,fn in [('Path',lambda q:q.read_bytes()),('builtin',lambda q:builtins.open(q,'rb')),('io',lambda q:io.open(q,'rb')),('os',lambda q:os.open(q,os.O_RDONLY))]:
      try:fn(p)
      except ValueError:pass
      else:raise ValueError('LINK guard failed '+api)
    for row in bindings['rows']:
     raw=Path(row['object_path']).read_bytes();need(H(raw)==row['object_sha256'],'ordinary object unchanged');(root/row['DOS_name']).write_bytes(raw);rows.append(row)
    for k,sub,name in [('LINK','only-link','LINK.EXE'),('SLIBC','only-slibc','SLIBC.LIB'),('LIBH','only-libh','LIBH.LIB')]:
     q=root/sub;q.mkdir();raw=toolpaths[k].read_bytes();need(H(raw)==tools[k]['sha256'],'tool exact');(q/name).write_bytes(raw)
    response='+\r\n'.join(r['DOS_name']for r in rows)+'\r\nPARTIAL.EXE\r\nPARTIAL.MAP\r\nR:\\SLIBC.LIB+H:\\LIBH.LIB;\r\n';(root/'INPUTS.RSP').write_bytes(response.encode('ascii'))
    command='T:\\LINK /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP /STACK:4096 @INPUTS.RSP';batch='@echo off\r\n'+command+' > LINK.LOG\r\nif errorlevel 1 goto failed\r\necho success > RESULT.TXT\r\ngoto done\r\n:failed\r\necho link_failed > RESULT.TXT\r\n:done\r\nexit\r\n';(root/'RUN.BAT').write_bytes(batch.encode('ascii'))
    conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(root)+'"\nmount t "'+str(root/'only-link')+'" -ro\nmount r "'+str(root/'only-slibc')+'" -ro\nmount h "'+str(root/'only-libh')+'" -ro\nc:\nRUN.BAT\n';(root/'dosbox.conf').write_text(conf)
    try:
     p=subprocess.Popen([str(toolpaths['DOSBox']),'-conf',str(root/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
     process={'pid':p.pid,'argv':[str(toolpaths['DOSBox']),'-conf',str(root/'dosbox.conf'),'-noconsole'],'terminal':False,'reaped':False}
     try:stdout,stderr=p.communicate(timeout=90)
     except subprocess.TimeoutExpired:p.kill();stdout,stderr=p.communicate();raise
     process.update(returncode=p.returncode,terminal=True,reaped=True);saved['DOSBOX.STDOUT.bin']=stdout;saved['DOSBOX.STDERR.bin']=stderr
    except BaseException as exc:error=exc
    finally:
     if process is not None and'p'in locals():process.update(returncode=p.poll(),terminal=p.poll()is not None,reaped=p.poll()is not None)
     for pth in root.rglob('*'):
      if pth.is_file():saved[str(pth.relative_to(root))]=pth.read_bytes()
  # GEN guard has closed; retention writes are new output only.
  artifacts={}
  for name,raw in saved.items():
   dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True)
   with dest.open('xb')as f:f.write(raw)
   artifacts[name]=H(raw)
  if error is not None:raise error
  need(process and process['returncode']==0 and process['reaped']and len(blocked)==20 and len(rows)==count,'real closed host process/guards/inputcount')
  need(all(n in saved for n in ['PARTIAL.EXE','PARTIAL.MAP','LINK.LOG','RESULT.TXT']),'complete actual LINK products required')
  log=saved['LINK.LOG'].decode('cp437');status=saved['RESULT.TXT'].decode('ascii').strip();diagnostic_validation=parse_link_diagnostics(log,status);undefined=diagnostic_validation['undefined_symbols']
  exe=saved['PARTIAL.EXE'];need(exe[:2]==b'MZ' and len(exe)>=28,'Real complete MZheader');actual_SP=int.from_bytes(exe[16:18],'little');need(actual_SP==4096,'Actual LINK /STACK:4096 initialSP')
  result={'schema':'descriptor-game-build-LINK-v1','status':'CLOSED_SUCCESS'if status=='success'else'CLOSED_DIAGNOSTIC','source_artifact_class':seal.classification,'objects_count':count,**descriptor['counts'],'source_process_count':None,'source_process_records_reused':False,'source_seal_sha256':seal.digest,'run_id':seal.run_id,'objects':rows,'tools':{k:tools[k]for k in ['LINK','SLIBC','LIBH','DOSBox']},'LINK_calls':1,'LINK_calls_scope':'aggregate_source_only','aggregate_SOURCE_LINK_calls':1,'ordinary_runtime_helper_calibration_LINK_calls':None,'total_LINK_process_count':None,'LINK_command':command,'LINK_stack_configuration':{'declared_bytes':4096,'actual_MZ_SP':actual_SP,'historical_original_switch_proven':False},'process':process,'artifacts':artifacts,'LINK_diagnostic_validation':diagnostic_validation,'undefined_symbols':undefined,'actual_missing_count':len(undefined),'source_only_guard_reads':reads,'active_denied_probes':blocked,'target_or_carrier_or_runtimeOBJ_inputs':False,'extra_alias_stub_or_provider':False,'partial_EXE_executed':False,'full_executable_match':False,'new_credit':0,'root_observed_terminal_receipt_required':True};(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');return result
 except BaseException as exc:
  (out/'HELD.json').write_text(json.dumps({'status':'HELD_NO_RETRY','error':repr(exc),'traceback':traceback.format_exc(),'process':process,'reads':reads,'blocked':blocked,'retained':list(saved),'no_new_source_generation':True},indent=2)+'\n');raise
