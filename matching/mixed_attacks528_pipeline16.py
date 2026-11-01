"""Finite one/two-C5-source mixed visual policy. Constants supplied by integration."""
from pathlib import Path
import hashlib
from mixed_visual_source16 import compose_fresh
KIND='mixed-c-fa-authored-asm-whole-omf'
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError('Closed visual SOURCE: '+m)
def phases():return['C5']+['C5_'+str(i)for i in range(1,len(PARTS))]+['MASM']
def validate_row(row):
 need({k:v for k,v in row.items()if k not in('order_slot','DOS_name')}==ROW,'exact visual row/tools/source roles');return True
def validate_sources(row,project):
 validate_row(row)
 for s in SOURCES:
  p=Path(project)/s['path'];need(p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256'],'actual source identity')
def validate_selected(spec,selected,components,project):
 validate_sources(spec,project);need([u['id']for u in selected]==OWNERS,'exact owners/order');retained={}
 for u in selected:
  c=ROW['owner_contracts'][u['id']];need(all(u[k]==c[k]for k in('source','source_sha256','language'))and u['backend']==ROW['backend_set'][0],'source/language/backend role')
  need(u['comparison_object_role']==c['comparison_role']and u['object_sha256']==ROW['comparison_expected_raw_sha256'],'real mixed output role');proof=u['mixed_object_proof'];need(proof['whole_native_equal']and proof['C5_sidecar_not_SOURCE']and len(proof['all_fields'])==FIELD_COUNT and len(proof['native_MZ'])==MZ_COUNT,'complete whole mixed proof');need([b['base']for b in proof['load_bases']]==[0,1,4096,65535]and all(b['native_equal']for b in proof['load_bases']),'four load bases')
  if u['language']=='c':
   i=next(i for i,part in enumerate(PARTS)if u['id']in part['owners']);p=Path(u['comparison_object_artifact']).resolve();need(p.is_relative_to(Path(components).resolve()/'typed-sidecars')and p.is_file()and not p.is_symlink()and H(p.read_bytes())==u['comparison_object_sha256']==SIDECAR_HASHES[i],'genuine unchanged typed sidecar');need(u['compiler_flags']==PARTS[i]['flags']and str(p)!=u['object_artifact'],'sidecar flags/excludedSOURCE');value=(str(p),u['comparison_object_sha256']);need(i not in retained or retained[i]==value,'one genuine sidecar per compile group');retained[i]=value
 need(set(retained)==set(range(len(PARTS)))and len(set(retained.values()))==len(PARTS),'all distinct sidecars retained')
def seal_extra(spec,selected):
 if spec['kind']!=KIND:return{}
 parts=[]
 for i,part in enumerate(PARTS):
  u=next(u for u in selected if u['id']==part['owners'][0]);parts.append({'path':u['comparison_object_artifact'],'sha256':u['comparison_object_sha256'],'role':'comparison_only_excluded_from_SOURCE','owners':part['owners'],'flags':part['flags']})
 return{'generation_sources':SOURCES,'owner_contracts':ROW['owner_contracts'],'mixed_transform':TRANSFORM,'typed_C5_sidecars':parts}
def validate_seal_row(row):
 need(row['kind']==KIND and row['source']==SOURCES[0]['path']and row['source_sha256']==C_SOURCE_SHA256 and row['selected_owners']==OWNERS,'exact sealed visual ownership');need(row['generation_sources']==SOURCES and row['owner_contracts']==ROW['owner_contracts']and row['mixed_transform']==TRANSFORM,'sealed source roles');need(row['object_sha256']==ROW['comparison_expected_raw_sha256'],'sealed whole object')
 parts=row['typed_C5_sidecars'];need(len(parts)==len(PARTS),'all sidecars sealed')
 for i,s in enumerate(parts):
  p=Path(s['path']);need(s['role']=='comparison_only_excluded_from_SOURCE'and str(p)!=row['object_path']and p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256']==SIDECAR_HASHES[i]and s['owners']==PARTS[i]['owners']and s['flags']==PARTS[i]['flags'],'retained sidecar role unchanged')
 return True

def record_read(observer,p,raw):
 row,event=observer.current
 if row['kind']!=KIND:return
 p=Path(p).resolve();root=observer.roots[0];key=None
 if p.is_relative_to(root):
  rel=str(p.relative_to(root))
  if rel in [phase+'/'+name for phase in phases()[:-1]for name in('UNIT.OBJ','UNIT.ASM')]+['MASM/UNIT.OBJ']:key=rel
 else:
  for s in SOURCES:
   if p==observer.project/s['path']:key=s['path']
 if key is not None:
  prior=event.setdefault('_mixed_read_bytes',{}).get(key);need(prior is None or prior==raw,'fresh source/artifact read changed');event['_mixed_read_bytes'][key]=raw

def before_process(observer,row,event,root,argv,kw):
 count=len(event['processes']);need(count<len(phases()),'no extra process');phase=phases()[count];work=root/phase
 need(list(argv)==[observer.descriptor['tools']['DOSBox']['path'],'-conf',str(work/'dosbox.conf'),'-noconsole'],'exact genuine phase executable/argv')
 submitted=event.get('submitted',{});conf=submitted.get(str(work/'dosbox.conf'),b'').decode('ascii');mounts=[x for x in conf.splitlines()if x.lower().startswith('mount ')];toolroot=observer.project/'toolchains'/('msc510'if phase=='MASM'else'msc500');need(mounts==['mount c "'+str(work)+'"','mount t "'+str(toolroot)+'" -ro'],'only phase scratch and genuine tools mounted');need(not(work/'UNIT.OBJ').exists(),'no stale phase object')
 if phase!='MASM':
  part=PARTS[count];need(H(submitted.get(str(work/'UNIT.C'),b''))==part['sha256'],'actual submitted C source role');command='T:\\CL.EXE /c '+' '.join(part['flags'])+' /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C'
 else:
  need([p.get('mixed_phase')for p in event['processes']]==phases()[:-1]and all(p['object'].poll()==0 for p in event['processes']),'every genuine C5 process closed before MASM')
  reads=event.get('_mixed_read_bytes',{});need(all(k in reads for k in[phase+'/'+name for phase in phases()[:-1]for name in('UNIT.OBJ','UNIT.ASM')]+[s['path']for s in SOURCES]),'all actual fresh C5/source reads');need(all(H(reads[s['path']])==s['sha256']for s in SOURCES),'actual source pins')
  composed,_=compose_fresh(tuple(reads[phase+'/UNIT.ASM']for phase in phases()[:-1]),reads[ASM_SOURCE],kind=PROFILE_KIND,source_hashes=[H(reads[p['source']])for p in PARTS]);need(submitted.get(str(work/'UNIT.ASM'))==composed,'actual MASM input from all fresh FA/source roles');command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 batch=submitted.get(str(work/'BUILD.BAT'),b'').decode('ascii');need(batch.splitlines().count(command+' > C:\\BUILD.LOG')==1,'exact genuine command/settings');return phase

def finish_event(observer,row,event,result):
 need([p.get('mixed_phase')for p in event['processes']]==phases()and all(p['object'].poll()==0 for p in event['processes']),'all real processes closed');reads=event.pop('_mixed_read_bytes');need(reads['MASM/UNIT.OBJ']==result.object_bytes,'whole actual mixed object')
 for i,phase in enumerate(phases()[:-1]):need(reads[phase+'/UNIT.OBJ']==result.sidecars[i]and reads[phase+'/UNIT.ASM']==result.fas[i],'each actual sidecar/listing role')
 composed,proof=compose_fresh(result.fas,reads[ASM_SOURCE],kind=PROFILE_KIND,source_hashes=[H(reads[p['source']])for p in PARTS]);need(composed==result.mixed_source_bytes,'same actual composed output')
 event['mixed_fresh_witness']={'kind':KIND,'generation_sources':SOURCES,'transform':TRANSFORM,'mixed_SHA256':H(result.object_bytes),'C5_sidecar_SHA256':H(result.sidecars[0]),'sidecar_SHA256s':[H(x)for x in result.sidecars],'fresh_FA_SHA256s':[H(x)for x in result.fas],'composed_SHA256':H(composed),'C5_sidecar_in_SOURCE':False,'phases':[{'phase':p['mixed_phase'],'pid':p['object'].pid,'returncode':p['object'].returncode}for p in event['processes']]}
# Integration must supply closed ROW/SOURCES/OWNERS/PARTS/SIDECAR_HASHES,
# C_SOURCE_SHA256/ASM_SOURCE/PROFILE_KIND/TRANSFORM/FIELD_COUNT/MZ_COUNT.
SOURCES=[{'path': 'src/attacks_neighbors_match.c',
  'sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd',
  'role': 'genuine_C_source'},
 {'path': 'asm/link/init_rays9840.asm',
  'sha256': 'b71de6aca2db4a609e21b31e6c1552b519d12be5e8e3dbfef66813346db52caf',
  'role': 'authored_ASM_procedure_source'}]
OWNERS=['init_rays_code185', 'piece_attacks_98f9', 'pawn_attacks_99be']
PARTS=[{'source': 'src/attacks_neighbors_match.c',
  'flags': ['/AS', '/Zi'],
  'owners': ['piece_attacks_98f9', 'pawn_attacks_99be'],
  'sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd'}]
SIDECAR_HASHES=['e17087c543a6fdf5d02478d93eb60db6fa473abd48d04ca803a067b77c7c7345']
C_SOURCE_SHA256='c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd'
ASM_SOURCE='asm/link/init_rays9840.asm'
PROFILE_KIND='attacks528'
TRANSFORM='attacks528-reviewed-mixed-visual-source-v1'
FIELD_COUNT=30
MZ_COUNT=0
ROW={'kind': 'mixed-c-fa-authored-asm-whole-omf',
 'source': 'src/attacks_neighbors_match.c',
 'source_sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd',
 'selected_owners': ['init_rays_code185', 'piece_attacks_98f9', 'pawn_attacks_99be'],
 'comparison_expected_raw_sha256': 'db232231fe3e9ba1ce80e672cc19b4841d0f0818f49fab820aaf5013559c2648',
 'compiler_flags': ['/AS', '/Zi'],
 'source_name': 'UNIT.C',
 'compiler': 'msc500',
 'backend_set': ['msc500-fa-masm510-visual-mixed-v1'],
 'object_profile': 'attacks528_visual_v1',
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
 'generation_sources': [{'path': 'src/attacks_neighbors_match.c',
                         'sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd',
                         'role': 'genuine_C_source'},
                        {'path': 'asm/link/init_rays9840.asm',
                         'sha256': 'b71de6aca2db4a609e21b31e6c1552b519d12be5e8e3dbfef66813346db52caf',
                         'role': 'authored_ASM_procedure_source'}],
 'owner_contracts': {'init_rays_code185': {'source': 'asm/link/init_rays9840.asm',
                                           'source_sha256': 'b71de6aca2db4a609e21b31e6c1552b519d12be5e8e3dbfef66813346db52caf',
                                           'language': 'asm-code',
                                           'comparison_role': 'final_mixed_span'},
                     'piece_attacks_98f9': {'source': 'src/attacks_neighbors_match.c',
                                            'source_sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd',
                                            'language': 'c',
                                            'comparison_role': 'genuine_C5_typed_sidecar'},
                     'pawn_attacks_99be': {'source': 'src/attacks_neighbors_match.c',
                                           'source_sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd',
                                           'language': 'c',
                                           'comparison_role': 'genuine_C5_typed_sidecar'}},
 'mixed_transform': 'attacks528-reviewed-mixed-visual-source-v1',
 'public_adapter': {'module': 'mixed_visual16',
                    'function': 'assemble',
                    'sha256': 'b834d4a98f42c3d194b38c0ebfa0aced9ba551e9bbcc10f4dfbed37e66ce1db1'}}
