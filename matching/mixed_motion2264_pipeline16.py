"""Finite staged three-source mixed overlap policy; no generic frame/owner waiver."""
from pathlib import Path
import hashlib
from mixed_overlap_source16 import compose_fresh
KIND='mixed-c-fa-authored-asm-whole-omf'
H=lambda b:hashlib.sha256(b).hexdigest()
def validate_row(row):
 need({k:v for k,v in row.items()if k not in ('order_slot','DOS_name')}==ROW,'exact mixed overlap row/tools/three sources/11 roles')
 return True
def validate_sources(row,project):
 validate_row(row)
 for s in SOURCES:
  p=Path(project)/s['path'];need(p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256'],'source changed '+s['path'])
def validate_selected(spec,selected,components,project):
 validate_sources(spec,project);need([u['id']for u in selected]==OWNERS,'exact closed owners in order')
 sidecars=[]
 for u in selected:
  c=ROW['owner_contracts'][u['id']]
  need(all(u[k]==c[k]for k in ('source','source_sha256','language'))and u['backend']==ROW['backend_set'][0],'exact source/language/backend role')
  need(u['comparison_object_role']==c['comparison_role']and u['object_sha256']==ROW['comparison_expected_raw_sha256'],'exact real mixed output role')
  proof=u['mixed_object_proof'];need(proof['whole_native_equal']and proof['C5_sidecar_not_SOURCE']and len(proof['all_fields'])==FIELD_COUNT and len(proof['native_MZ'])==MZ_COUNT,'complete mixed overlap proof before seal')
  need([b['base']for b in proof['load_bases']]==[0,1,4096,65535]and all(b['native_equal']for b in proof['load_bases']),'all four load bases')
  if u['language']=='c':
   p=Path(u['comparison_object_artifact']).resolve();need(p.is_relative_to(Path(components).resolve()/'typed-sidecars')and p.is_file()and not p.is_symlink()and H(p.read_bytes())==u['comparison_object_sha256'],'genuine typed sidecar separate from SOURCE')
   need(u['comparison_object_artifact']!=u['object_artifact'],'sidecar must not become SOURCE');sidecars.append((str(p),u['comparison_object_sha256']))
 need(len(sidecars)==C_OWNER_COUNT and len(set(sidecars))==1,'all retained C owners share one genuine sidecar')
def seal_extra(spec,selected):
 if spec['kind']!=KIND:return{}
 return {'generation_sources':SOURCES,'owner_contracts':ROW['owner_contracts'],'mixed_transform':TRANSFORM,'typed_C5_sidecar':{'path':selected[C_OWNER_INDEX]['comparison_object_artifact'],'sha256':selected[C_OWNER_INDEX]['comparison_object_sha256'],'role':'comparison_only_excluded_from_SOURCE'}}
def validate_seal_row(row):
 need(row['kind']==KIND and row['source']==SOURCES[0]['path']and row['source_sha256']==C_SOURCE_SHA256 and row['selected_owners']==OWNERS,'exact sealed mixed overlap ownership')
 need(row['generation_sources']==SOURCES and row['owner_contracts']==ROW['owner_contracts']and row['mixed_transform']==TRANSFORM,'sealed source roles')
 need(row['object_sha256']==ROW['comparison_expected_raw_sha256'],'sealed whole object')
 s=row['typed_C5_sidecar'];p=Path(s['path']);need(s['role']=='comparison_only_excluded_from_SOURCE'and str(p)!=row['object_path']and p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256'],'retained sidecar unchanged')
 return True
def need(v,m):
 if not v:raise ValueError('Closed mixed SOURCE: '+m)

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
  reads=event.get('_mixed_read_bytes',{});need(all(k in reads for k in ['C5/UNIT.OBJ','C5/UNIT.ASM']+[s['path']for s in SOURCES]),'Actual same-scratch C5 output and both genuine source reads')
  need(reads['C5/UNIT.OBJ']and all(H(reads[s['path']])==s['sha256']for s in SOURCES),'Real current-call C5 sidecar and exact real sources')
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


# Closed ROW/SOURCES/OWNERS and field counts supplied by integration recipe.
SOURCES=[{'path': 'src/motion_mixed_context_match.c',
  'sha256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9',
  'role': 'genuine_C_source'},
 {'path': 'asm/link/motion_mixed_authored.asm',
  'sha256': '953dbe20cad21a8a8c0202ddb2343f2fbe6d5a3fbedf66fb62690d45cc612dba',
  'role': 'authored_ASM_procedure_source'}]
OWNERS=['init_animation_code1083', 'offset_task_70ef', 'face_task_724d', 'turn_task_code640']
C_SOURCE_SHA256='a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9'
TRANSFORM='motion2264-reviewed-mixed-overlap-source-v1'
FIELD_COUNT=88
MZ_COUNT=3
C_OWNER_COUNT=2
C_OWNER_INDEX=1
ROW={'kind': 'mixed-c-fa-authored-asm-whole-omf',
 'source': 'src/motion_mixed_context_match.c',
 'source_sha256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9',
 'selected_owners': ['init_animation_code1083', 'offset_task_70ef', 'face_task_724d', 'turn_task_code640'],
 'comparison_expected_raw_sha256': '909220367ff0a3197db9192a40e5ce78933cb0d95ec2843f5c9bd0dce9854ecc',
 'compiler_flags': ['/AS', '/Zi'],
 'source_name': 'UNIT.C',
 'compiler': 'msc500',
 'backend_set': ['msc500-fa-masm510-overlap-mixed-v1'],
 'object_profile': 'motion_overlap_v1',
 'generation_tools': {'toolchains/msc500/CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a',
                      'toolchains/msc500/CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504',
                      'toolchains/msc500/C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791',
                      'toolchains/msc500/C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233',
                      'toolchains/msc500/C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1',
                      'toolchains/msc500/C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669',
                      'toolchains/msc500/C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18',
                      'toolchains/msc500/manifest.json': 'd2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82',
                      'config/msc500.json': '2e7ca2bc19d665b35f60e651b65f536d1f35e94d8af8463600d5d30500f01d66',
                      'toolchains/msc510/MASM.EXE': '1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f',
                      'toolchains/msc510/manifest.json': 'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4',
                      'toolchains/msc510/LICENSE': 'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4',
                      'config/msc510.json': '058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'},
 'generator': 'DOSBox',
 'dosbox_keyword': None,
 'generation_sources': [{'path': 'src/motion_mixed_context_match.c',
                         'sha256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9',
                         'role': 'genuine_C_source'},
                        {'path': 'asm/link/motion_mixed_authored.asm',
                         'sha256': '953dbe20cad21a8a8c0202ddb2343f2fbe6d5a3fbedf66fb62690d45cc612dba',
                         'role': 'authored_ASM_procedure_source'}],
 'owner_contracts': {'init_animation_code1083': {'source': 'asm/link/motion_mixed_authored.asm',
                                                 'source_sha256': '953dbe20cad21a8a8c0202ddb2343f2fbe6d5a3fbedf66fb62690d45cc612dba',
                                                 'language': 'asm-code',
                                                 'comparison_role': 'final_mixed_span'},
                     'offset_task_70ef': {'source': 'src/motion_mixed_context_match.c',
                                          'source_sha256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9',
                                          'language': 'c',
                                          'comparison_role': 'genuine_C5_typed_sidecar'},
                     'face_task_724d': {'source': 'src/motion_mixed_context_match.c',
                                        'source_sha256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9',
                                        'language': 'c',
                                        'comparison_role': 'genuine_C5_typed_sidecar'},
                     'turn_task_code640': {'source': 'asm/link/motion_mixed_authored.asm',
                                           'source_sha256': '953dbe20cad21a8a8c0202ddb2343f2fbe6d5a3fbedf66fb62690d45cc612dba',
                                           'language': 'asm-code',
                                           'comparison_role': 'final_mixed_span'}},
 'mixed_transform': 'motion2264-reviewed-mixed-overlap-source-v1',
 'public_adapter': {'module': 'mixed_overlap16',
                    'function': 'assemble',
                    'sha256': '17137ad59316cff3d04c690d5b8b760278738c5eaab286edb0b0543359a6494d'}}
