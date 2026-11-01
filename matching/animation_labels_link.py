"""Exactly one new OBJ/authentic LINK/tool/scratch emission, no reference reads."""
from pathlib import Path
import hashlib,json,os,subprocess,tempfile,traceback
from unittest.mock import patch
from animation_labels15_pins import LINK_SHA,DOSBOX_SHA
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();SHA=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError('labels LINK emission: '+m)
def emit_new_object(raw,project,output):
 project=Path(project).resolve();output=Path(output).resolve();need(not output.exists(),'new output root required; preserve failed attempts');output.mkdir(parents=True);(output/'one-LINK-call.claim').open('x').close();newobj=output/'fresh-labels.obj';newobj.write_bytes(raw);need(H(newobj)==SHA(raw),'whole new compiled object retained')
 tool=project/'toolchains/msc510/LINK.EXE';dosbox=Path('/usr/bin/dosbox');need(H(tool)==LINK_SHA and H(dosbox)==DOSBOX_SHA,'exact authentic tools');reads=[];blocked=[];retained={};process=None;error=None
 try:
  with tempfile.TemporaryDirectory(prefix='bc-labels15-link-')as temporary:
   scratch=Path(temporary);original=Path.open;allowed={newobj,tool,dosbox}
   def guard(p,mode='r',*a,**k):
    if isinstance(p,int):return original(p,mode,*a,**k)
    p=Path(p).resolve();writing=any(x in mode for x in'wax+')
    if(writing and not p.is_relative_to(scratch))or(not writing and p not in allowed and not p.is_relative_to(scratch)):blocked.append(str(p));raise ValueError('source-only LINK read/write denied '+str(p))
    if not writing:reads.append(str(p))
    return original(p,mode,*a,**k)
   with patch.object(Path,'open',guard):
    for p in[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'build/animation-command-data-recovery/labels.obj',project/'build/animation-data238-native-order-LINK/LINK/PARTIAL.EXE']:
     try:p.read_bytes()
     except ValueError:pass
     else:raise AssertionError('LINK source-only guard inactive')
    (scratch/'LABELS.OBJ').write_bytes(newobj.read_bytes());tools=scratch/'only-tools';tools.mkdir();(tools/'LINK.EXE').write_bytes(tool.read_bytes())
    response='LABELS.OBJ\r\nLABELS.EXE\r\nLABELS.MAP\r\n;\r\n';(scratch/'INPUTS.RSP').write_bytes(response.encode('ascii'))
    command='T:\\LINK /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP @INPUTS.RSP';batch='@echo off\r\n'+command+' > LINK.LOG\r\nif errorlevel 1 goto failed\r\necho success > RESULT.TXT\r\ngoto done\r\n:failed\r\necho link_failed > RESULT.TXT\r\n:done\r\nexit\r\n';(scratch/'RUN.BAT').write_bytes(batch.encode('ascii'))
    conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(scratch)+'"\nmount t "'+str(tools)+'" -ro\nc:\nRUN.BAT\n';(scratch/'dosbox.conf').write_text(conf)
    run_error=None
    try:
     p=subprocess.run([str(dosbox),'-conf',str(scratch/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=45);process={'returncode':p.returncode,'reaped':True,'stdout':p.stdout.decode('utf8',errors='replace'),'stderr':p.stderr.decode('utf8',errors='replace'),'argv':[str(dosbox),'-conf',str(scratch/'dosbox.conf'),'-noconsole']}
    except BaseException as exc:run_error=exc;process={'raised':repr(exc),'no_second_attempt':True}
    finally:
     # Read inside the guard; persist all partial/complete products afterwards.
     saved={n:(scratch/n).read_bytes()for n in['LABELS.OBJ','INPUTS.RSP','RUN.BAT','dosbox.conf','LINK.LOG','RESULT.TXT','LABELS.EXE','LABELS.MAP']if(scratch/n).is_file()}
   for n,b in saved.items():(output/n).write_bytes(b);retained[n]=SHA(b)
   if run_error is not None:raise run_error
   need(p.returncode==0 and len(blocked)==4,'actual tool closure/4denied probes');need(all(n in saved for n in['LINK.LOG','RESULT.TXT','LABELS.EXE','LABELS.MAP']),'HELD: no complete verifiable DATA EXE/MAP; no fallback')
   need(saved['LABELS.OBJ']==raw and H(newobj)==SHA(raw),'raw original OBJ unchanged');status=saved['RESULT.TXT'].decode('ascii').strip();receipt={'status':'CLOSED_SOURCE_ONLY_REAL_LINK_PENDING_DATA_VALIDATION','input_object_sha256':SHA(raw),'source_objects':1,'libraries':[],'LINK_sha256':LINK_SHA,'DOSBox_sha256':DOSBOX_SHA,'command':command,'input_response':response,'actual_LINK_status':status,'process':process,'reads':reads,'blocked_probes':blocked,'artifacts':retained,'partial_EXE_executed':False};(output/'LINK-generation.json').write_text(json.dumps(receipt,indent=2)+'\n')
   return{'input_object_sha256':SHA(raw),'source_objects':1,'libraries':[],'exe_bytes':saved['LABELS.EXE'],'map_text':saved['LABELS.MAP'].decode('cp437'),'log_text':saved['LINK.LOG'].decode('cp437'),'link_status':status,'partial_EXE_executed':False,'receipt':receipt}
 except BaseException as e:
  error={'status':'HELD_AFTER_SINGLE_BOUNDED_ATTEMPT','error':repr(e),'traceback':traceback.format_exc(),'process':process,'reads':reads,'blocked_probes':blocked,'artifacts':retained,'no_fallback_or_extra_objects_libraries_or_entry_stub':True};(output/'HELD.json').write_text(json.dumps(error,indent=2)+'\n');raise
