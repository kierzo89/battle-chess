"""Finite staged three-source evaluator policy; no generic frame/owner waiver."""
from pathlib import Path
import hashlib
from mixed_evaluation_source16 import compose_fresh
KIND='mixed-c-fa-authored-asm-whole-omf'
H=lambda b:hashlib.sha256(b).hexdigest()
def validate_row(row):
 need({k:v for k,v in row.items()if k not in ('order_slot','DOS_name')}==ROW,'exact evaluator row/tools/three sources/11 roles')
 return True
def validate_sources(row,project):
 validate_row(row)
 for s in SOURCES:
  p=Path(project)/s['path'];need(p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256'],'source changed '+s['path'])
def validate_selected(spec,selected,components,project):
 validate_sources(spec,project);need([u['id']for u in selected]==OWNERS,'exact 11 owners in order')
 sidecars=[]
 for u in selected:
  c=ROW['owner_contracts'][u['id']]
  need(all(u[k]==c[k]for k in ('source','source_sha256','language'))and u['backend']==ROW['backend_set'][0],'exact source/language/backend role')
  need(u['comparison_object_role']==c['comparison_role']and u['object_sha256']==ROW['comparison_expected_raw_sha256'],'exact real mixed output role')
  proof=u['mixed_object_proof'];need(proof['whole_native_equal']and proof['C5_sidecar_not_SOURCE']and len(proof['all_fields'])==223 and len(proof['native_MZ'])==2,'complete evaluator proof before seal')
  need([b['load']for b in proof['four_bases']]==[0,1,4096,65535]and all(b['whole_equal']for b in proof['four_bases']),'all four load bases')
  if u['language']=='c':
   p=Path(u['comparison_object_artifact']).resolve();need(p.is_relative_to(Path(components).resolve()/'typed-sidecars')and p.is_file()and not p.is_symlink()and H(p.read_bytes())==u['comparison_object_sha256'],'genuine typed sidecar separate from SOURCE')
   need(u['comparison_object_artifact']!=u['object_artifact'],'sidecar must not become SOURCE');sidecars.append((str(p),u['comparison_object_sha256']))
 need(len(sidecars)==9 and len(set(sidecars))==1,'9 retained C owners share one genuine sidecar')
def seal_extra(spec,selected):
 if spec['kind']!=KIND:return{}
 return {'generation_sources':SOURCES,'owner_contracts':ROW['owner_contracts'],'mixed_transform':TRANSFORM,'typed_C5_sidecar':{'path':selected[0]['comparison_object_artifact'],'sha256':selected[0]['comparison_object_sha256'],'role':'comparison_only_excluded_from_SOURCE'}}
def validate_seal_row(row):
 need(row['kind']==KIND and row['source']==SOURCES[0]['path']and row['source_sha256']==C_SOURCE_SHA256 and row['selected_owners']==OWNERS,'exact sealed evaluator ownership')
 need(row['generation_sources']==SOURCES and row['owner_contracts']==ROW['owner_contracts']and row['mixed_transform']==TRANSFORM,'sealed source roles')
 need(row['object_sha256']==ROW['comparison_expected_raw_sha256'],'sealed whole object')
 s=row['typed_C5_sidecar'];p=Path(s['path']);need(s['role']=='comparison_only_excluded_from_SOURCE'and str(p)!=row['object_path']and p.is_file()and not p.is_symlink()and H(p.read_bytes())==s['sha256'],'retained sidecar unchanged')
 return True
SOURCES=[{'path': 'src/full_evaluation_match.c', 'sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'role': 'genuine_C_source'}, {'path': 'asm/link/evaluation3902/pawn_bit_count.asm', 'sha256': '576c7d98b12a07a44e7ec6c628ce2e1aaa836adb6a07d024fde1f6ed806e8c29', 'role': 'authored_ASM_procedure_source'}, {'path': 'asm/link/evaluation3902/evaluate_candidate.asm', 'sha256': 'daa6817283b07efeae64d1384ec470b80c7026bc0a795b3cb7f5172fa338ec1c', 'role': 'authored_ASM_procedure_source'}]
OWNERS=['evaluation_abs_fdf2', 'evaluation_parity_fe4a', 'evaluation_piece_109f9', 'evaluation_max_fe0c', 'evaluation_min_fe2b', 'pawn_score_1097c', 'full_evaluation_fe59', 'evaluation_pawn_remove_10a2c', 'evaluation_pawn_move_10a93', 'evaluate_candidate_code538', 'pawn_bit_count_code48']
C_SOURCE_SHA256='822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a'
TRANSFORM='evaluation3902-two-PROC-exact-source-inverse-v3'
ROW={'kind': 'mixed-c-fa-authored-asm-whole-omf', 'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'selected_owners': ['evaluation_abs_fdf2', 'evaluation_parity_fe4a', 'evaluation_piece_109f9', 'evaluation_max_fe0c', 'evaluation_min_fe2b', 'pawn_score_1097c', 'full_evaluation_fe59', 'evaluation_pawn_remove_10a2c', 'evaluation_pawn_move_10a93', 'evaluate_candidate_code538', 'pawn_bit_count_code48'], 'comparison_expected_raw_sha256': 'a8120c71456edd84cc7f8d566cf51a67a32f759978fe360d762e2c57365c4b65', 'compiler_flags': ['/AM', '/Gs', '/Zi'], 'source_name': 'UNIT.C', 'compiler': 'msc500', 'backend_set': ['msc500-fa-masm510-evaluation3902-mixed-v1'], 'object_profile': 'evaluation3902_v1', 'generation_tools': {'toolchains/msc500/CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'toolchains/msc500/CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'toolchains/msc500/C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'toolchains/msc500/C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'toolchains/msc500/C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'toolchains/msc500/C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'toolchains/msc500/C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18', 'toolchains/msc500/manifest.json': 'd2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82', 'config/msc500.json': '2e7ca2bc19d665b35f60e651b65f536d1f35e94d8af8463600d5d30500f01d66', 'toolchains/msc510/MASM.EXE': '1c6286c69b616160b8475ad17453ee872702a2c98075c2159ec792a1c745275f', 'toolchains/msc510/manifest.json': 'f98c55eaf97fff792dfa8f131d9ea255008c5d97311dd6837cd4fda79c2ebef4', 'toolchains/msc510/LICENSE': 'b5179f780ec212a434efcc989a2295a140deb0bdb17182d2bf9c5f6f1f1a01c4', 'config/msc510.json': '058abeace2a0466b843094d84d5d909a0f2a8e671f357df6e39988199383c618'}, 'generator': 'DOSBox', 'dosbox_keyword': None, 'generation_sources': [{'path': 'src/full_evaluation_match.c', 'sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'role': 'genuine_C_source'}, {'path': 'asm/link/evaluation3902/pawn_bit_count.asm', 'sha256': '576c7d98b12a07a44e7ec6c628ce2e1aaa836adb6a07d024fde1f6ed806e8c29', 'role': 'authored_ASM_procedure_source'}, {'path': 'asm/link/evaluation3902/evaluate_candidate.asm', 'sha256': 'daa6817283b07efeae64d1384ec470b80c7026bc0a795b3cb7f5172fa338ec1c', 'role': 'authored_ASM_procedure_source'}], 'owner_contracts': {'evaluation_abs_fdf2': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluation_parity_fe4a': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluation_piece_109f9': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluation_max_fe0c': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluation_min_fe2b': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'pawn_score_1097c': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'full_evaluation_fe59': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluation_pawn_remove_10a2c': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluation_pawn_move_10a93': {'source': 'src/full_evaluation_match.c', 'source_sha256': '822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a', 'language': 'c', 'comparison_role': 'genuine_C5_typed_sidecar'}, 'evaluate_candidate_code538': {'source': 'asm/link/evaluation3902/evaluate_candidate.asm', 'source_sha256': 'daa6817283b07efeae64d1384ec470b80c7026bc0a795b3cb7f5172fa338ec1c', 'language': 'asm-code', 'comparison_role': 'final_mixed_span'}, 'pawn_bit_count_code48': {'source': 'asm/link/evaluation3902/pawn_bit_count.asm', 'source_sha256': '576c7d98b12a07a44e7ec6c628ce2e1aaa836adb6a07d024fde1f6ed806e8c29', 'language': 'asm-code', 'comparison_role': 'final_mixed_span'}}, 'mixed_transform': 'evaluation3902-two-PROC-exact-source-inverse-v3', 'public_adapter': {'module': 'mixed_evaluation16', 'function': 'assemble', 'sha256': 'c7f39b2fa1782e2b7372e89c69f2481b9efa6778bae75cc7df4bf09c3071bbfb'}}
ASM_SYMBOLS=['_pawn_bit_count', '_evaluate_candidate']
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
  command='T:\\CL.EXE /c /AM /Gs /Zi /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C'
 else:
  previous=event['processes'][0];need(previous.get('mixed_phase')=='C5'and previous['object'].poll()==0,'Same call actual C5 closed before composition/MASM')
  reads=event.get('_mixed_read_bytes',{});need(all(k in reads for k in ['C5/UNIT.OBJ','C5/UNIT.ASM']+[s['path']for s in SOURCES]),'Actual same-scratch C5 output and both genuine source reads')
  need(reads['C5/UNIT.OBJ']and all(H(reads[s['path']])==s['sha256']for s in SOURCES),'Real current-call C5 sidecar and exact real sources')
  composed,_=compose_fresh(reads['C5/UNIT.ASM'],{n:reads[s['path']]for n,s in zip(ASM_SYMBOLS,SOURCES[1:])},c_source_sha256=H(reads[SOURCES[0]['path']]))
  need(submitted.get(str(work/'UNIT.ASM'))==composed,'MASM input independently derived from actual fresh C5 FA, no archived generation')
  command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 batch=submitted.get(str(work/'BUILD.BAT'),b'').decode('ascii');need(batch.splitlines().count(command+' > C:\\BUILD.LOG')==1,'Exact genuine phase command')
 return phase

def finish_event(observer,row,event,result):
 need(len(event['processes'])==2 and[eventp.get('mixed_phase')for eventp in event['processes']]==['C5','MASM'],'Exactly two real observed mixed phases')
 need(all(x['object'].poll()==0 for x in event['processes']),'Both real child processes reaped successfully')
 reads=event.pop('_mixed_read_bytes');need(reads['MASM/UNIT.OBJ']==result.object_bytes and reads['C5/UNIT.OBJ']==result.c5_sidecar_bytes and reads['C5/UNIT.ASM']==result.fresh_fa_bytes,'Typed result byte roles equal actual fresh scratch reads')
 composed,proof=compose_fresh(reads['C5/UNIT.ASM'],{n:reads[s['path']]for n,s in zip(ASM_SYMBOLS,SOURCES[1:])},c_source_sha256=H(reads[SOURCES[0]['path']]))
 need(composed==result.mixed_source_bytes,'Same actual current-call composed source result')
 event['mixed_fresh_witness']={'kind':KIND,'generation_sources':SOURCES,'transform':TRANSFORM,'mixed_SHA256':H(result.object_bytes),'C5_sidecar_SHA256':H(result.c5_sidecar_bytes),'fresh_FA_SHA256':H(result.fresh_fa_bytes),'composed_SHA256':H(composed),'C5_sidecar_in_SOURCE':False,'phases':[{'phase':x['mixed_phase'],'pid':x['object'].pid,'returncode':x['object'].returncode}for x in event['processes']]}

