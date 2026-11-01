"""Exact optional mixed SOURCE policy; never used for legacy descriptor rows."""
from pathlib import Path
import hashlib,json
from mixed_motion_special_source16 import compose_fresh,C_SOURCE_SHA256,DECODER_SOURCE_SHA256,TRANSFORM
KIND='mixed-c-fa-authored-asm-whole-omf'
SOURCES=[{'path':'src/motion_effect_tasks_match.c','sha256':C_SOURCE_SHA256,'role':'genuine_C_source'},{'path':'asm/link/special_task6bf9.asm','sha256':DECODER_SOURCE_SHA256,'role':'authored_ASM_procedure_source'}]
GEN_TOOL_PINS={'toolchains/msc500/CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'toolchains/msc500/CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'toolchains/msc500/C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'toolchains/msc500/C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'toolchains/msc500/C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'toolchains/msc500/C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'toolchains/msc500/C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18', 'toolchains/msc500/manifest.json': 'd2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82', 'config/msc500.json': '2e7ca2bc19d665b35f60e651b65f536d1f35e94d8af8463600d5d30500f01d66', 'toolchains/msc510/MASM.EXE': '1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f', 'toolchains/msc510/manifest.json': 'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4', 'toolchains/msc510/LICENSE': 'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4', 'config/msc510.json': '058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}
OWNERS=['move_task_68ea', 'effect_task_6ab1', 'special_task_code187']
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError('Closed mixed SOURCE: '+m)
def validate_row(r):
 need(r['generation_tools']==GEN_TOOL_PINS,'Only exact genuine source-tool capabilities; no profile/expected inputs')
 need(r['kind']==KIND and r['generation_sources']==SOURCES and r['source']==SOURCES[0]['path']and r['source_sha256']==C_SOURCE_SHA256,'Two exact frozen real source identities')
 need(r['selected_owners']==OWNERS and r['mixed_transform']==TRANSFORM and r['object_profile']=='motion_special970_v1','Exact whole mixed owner/profile/transform')
 need(r['compiler']=='msc500'and r['compiler_flags']==['/AS','/Zi']and r['source_name']=='UNIT.C'and r['generator']=='DOSBox'and r.get('dosbox_keyword')is None,'Exact compiler source route')
 need(r['public_adapter']['module']=='mixed_motion_special16'and r['public_adapter']['function']=='assemble','Exact public mixed adapter')
 need(r['owner_contracts']=={'move_task_68ea': {'source': 'src/motion_effect_tasks_match.c', 'source_sha256': '7df0efd9e7c26ca02ae1a5169e10e21343ec0a40590bb8fca5c53ea723ee797f', 'language': 'c', 'comparison_role': 'genuine_C5_sidecar_and_final_mixed_span0_455'}, 'effect_task_6ab1': {'source': 'src/motion_effect_tasks_match.c', 'source_sha256': '7df0efd9e7c26ca02ae1a5169e10e21343ec0a40590bb8fca5c53ea723ee797f', 'language': 'c', 'comparison_role': 'genuine_C5_sidecar_and_final_mixed_span455_783'}, 'special_task_code187': {'source': 'asm/link/special_task6bf9.asm', 'source_sha256': 'ac9e3a433f7bbd5beed715b9c6b1324303214d8410daab0bb0b34d894ecb1487', 'language': 'asm-code', 'comparison_role': 'final_mixed_span783_970'}},'Exact three compiler/ASM owner roles')
 return True
def validate_sources(r,project):
 validate_row(r)
 for s in SOURCES:
  p=Path(project)/s['path'];need(p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256'],'source changed '+s['path'])
def record_read(observer,p,raw):
 row,event=observer.current
 if row['kind']!=KIND:return
 p=Path(p).resolve();root=observer.roots[0];key=None
 if p.is_relative_to(root):
  rel=str(p.relative_to(root))
  if rel in ['C5/UNIT.OBJ','C5/UNIT.ASM','MASM/UNIT.OBJ']:key=rel
 else:
  for s in SOURCES:
   if p==observer.project/s['path']:key=s['path']
 if key is not None:
  prior=event.setdefault('_mixed_read_bytes',{}).get(key);need(prior is None or prior==raw,'same fresh file read changed');event['_mixed_read_bytes'][key]=raw

def before_process(observer,row,event,root,argv,kw):
 phase='C5'if len(event['processes'])==0 else'MASM';need(len(event['processes'])<2,'Only one C5 and one MASM process')
 work=root/phase;need(list(argv)==[observer.descriptor['tools']['DOSBox']['path'],'-conf',str(work/'dosbox.conf'),'-noconsole'],'Exact phase executable/argv')
 submitted=event.get('submitted',{});conf=submitted.get(str(work/'dosbox.conf'),b'').decode('ascii');mounts=[x for x in conf.splitlines()if x.lower().startswith('mount ')];toolroot=observer.project/'toolchains'/('msc500'if phase=='C5'else'msc510')
 need(mounts==['mount c "'+str(work)+'"','mount t "'+str(toolroot)+'" -ro'],'Only phase fresh scratch and genuine read-only tool mounts')
 need(not(work/'UNIT.OBJ').exists(),'No stale phase OBJ')
 if phase=='C5':
  need(H(submitted.get(str(work/'UNIT.C'),b''))==C_SOURCE_SHA256,'Actual submitted primary C source')
  command='T:\\CL.EXE /c /AS /Zi /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C'
 else:
  previous=event['processes'][0];need(previous.get('mixed_phase')=='C5'and previous['object'].poll()==0,'Same call actual C5 closed before composition/MASM')
  reads=event.get('_mixed_read_bytes',{});need(all(k in reads for k in ['C5/UNIT.OBJ','C5/UNIT.ASM',SOURCES[0]['path'],SOURCES[1]['path']]),'Actual same-scratch C5 output and both genuine source reads')
  need(reads['C5/UNIT.OBJ']and H(reads[SOURCES[0]['path']])==C_SOURCE_SHA256 and H(reads[SOURCES[1]['path']])==DECODER_SOURCE_SHA256,'Real current-call C5 sidecar and exact real sources')
  composed,_=compose_fresh(reads['C5/UNIT.ASM'],reads[SOURCES[1]['path']],c_source_sha256=H(reads[SOURCES[0]['path']]))
  need(submitted.get(str(work/'UNIT.ASM'))==composed,'MASM input independently derived from actual fresh C5 FA, no archived generation')
  command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 batch=submitted.get(str(work/'BUILD.BAT'),b'').decode('ascii');need(batch.splitlines().count(command+' > C:\\BUILD.LOG')==1,'Exact genuine phase command')
 return phase

def finish_event(observer,row,event,result):
 need(len(event['processes'])==2 and[eventp.get('mixed_phase')for eventp in event['processes']]==['C5','MASM'],'Exactly two real observed mixed phases')
 need(all(x['object'].poll()==0 for x in event['processes']),'Both real child processes reaped successfully')
 reads=event.pop('_mixed_read_bytes');need(reads['MASM/UNIT.OBJ']==result.object_bytes and reads['C5/UNIT.OBJ']==result.c5_sidecar_bytes and reads['C5/UNIT.ASM']==result.fresh_fa_bytes,'Typed result byte roles equal actual fresh scratch reads')
 composed,proof=compose_fresh(reads['C5/UNIT.ASM'],reads[SOURCES[1]['path']],c_source_sha256=H(reads[SOURCES[0]['path']]))
 need(composed==result.mixed_source_bytes,'Same actual current-call composed source result')
 event['mixed_fresh_witness']={'kind':KIND,'generation_sources':SOURCES,'transform':TRANSFORM,'mixed_SHA256':H(result.object_bytes),'C5_sidecar_SHA256':H(result.c5_sidecar_bytes),'fresh_FA_SHA256':H(result.fresh_fa_bytes),'composed_SHA256':H(composed),'C5_sidecar_in_SOURCE':False,'phases':[{'phase':x['mixed_phase'],'pid':x['object'].pid,'returncode':x['object'].returncode}for x in event['processes']]}

def validate_selected(spec,selected,components,project):
 validate_sources(spec,project);need([u['id']for u in selected]==OWNERS,'Exact three ordinary owner IDs')
 for u in selected:
  owner=spec['owner_contracts'][u['id']];need(u['source']==owner['source']and u['source_sha256']==owner['source_sha256']and u['language']==owner['language']and u['backend']=='msc500-fa-masm510-motion-special-mixed-v1','Exact source/owner/backend identity')
  need(u['mixed_profile']=='motion_special970_v1'and u['mixed_object_proof']['whole_native_equal']and u['mixed_object_proof']['C5_sidecar_not_SOURCE'],'Complete mixed comparison before SOURCE seal')
 for c in selected[:2]:
  p=Path(c['comparison_object_artifact']).resolve();need(p.is_relative_to(Path(components).resolve()/'typed-sidecars')and p.is_file()and H(p.read_bytes())==c['comparison_object_sha256'],'Separate genuine C5 typed sidecar artifact')
  need(c['comparison_object_role']=='genuine_C5_typed_sidecar'and c['comparison_object_artifact']!=c['object_artifact'],'C5 sidecar excluded from game SOURCE')
 need(selected[0]['comparison_object_artifact']==selected[1]['comparison_object_artifact']and selected[0]['comparison_object_sha256']==selected[1]['comparison_object_sha256'],'Both genuine C owners share exact whole C5 sidecar')
 need(selected[2]['comparison_object_role']=='final_mixed_span783_970','Authored ASM role')

def seal_extra(spec,selected):
 if spec['kind']!=KIND:return{}
 return {'generation_sources':spec['generation_sources'],'owner_contracts':spec['owner_contracts'],'mixed_transform':spec['mixed_transform'],'typed_C5_sidecar':{'path':selected[0]['comparison_object_artifact'],'sha256':selected[0]['comparison_object_sha256'],'role':'comparison_only_excluded_from_SOURCE'}}
def validate_seal_row(r):
 if r['kind']!=KIND:return True
 need(r['generation_sources']==SOURCES and r['mixed_transform']==TRANSFORM and r['selected_owners']==OWNERS,'Sealed exact dual-source metadata')
 need(r['typed_C5_sidecar']['role']=='comparison_only_excluded_from_SOURCE'and r['typed_C5_sidecar']['path']!=r['object_path'],'Sealed sidecar is not game object')
 p=Path(r['typed_C5_sidecar']['path']);need(p.is_file()and not p.is_symlink()and H(p.read_bytes())==r['typed_C5_sidecar']['sha256'],'Retained genuine typed sidecar unchanged after SOURCE seal')
 return True
