"""Descriptor validation and fresh SOURCE selection; no generators or target reads."""
from pathlib import Path
import hashlib,json,re
import mixed_source_dispatch_evaluation16 as mixed
import near_bss_layout16 as machine_bss
import packet_literal61 as packet
class BuildHeld(ValueError):pass
def need(v,m):
 if not v:raise BuildHeld(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def regular(p):
 p=Path(p);need(p.is_file()and not p.is_symlink(),'regular file required: '+str(p));return p

def validate_descriptor(d):
 need(d['schema']=='battlechess-reviewed-source-cohort-v1','descriptor schema')
 rows=d['rows'];need(rows and [r['order_slot']for r in rows]==list(range(len(rows))),'exact contiguous explicit order')
 need([r['DOS_name']for r in rows]==['O%03d.OBJ'%i for i in range(len(rows))],'exact DOS vector')
 counts={'C':0,'ASM':0,'COMMON':0,'SOURCE':len(rows)};owners=set();identities=set()
 if any(r['kind']==mixed.KIND for r in rows):counts['MIXED']=0
 if any(r['kind']==machine_bss.KIND for r in rows):counts['BSS']=0
 for r in rows:
  need(r['kind']in ('c-whole-omf','asm-whole-omf','common-whole-omf',mixed.KIND,machine_bss.KIND),'SOURCE role only; no runtime OBJ')
  counts[{'c-whole-omf':'C','asm-whole-omf':'ASM','common-whole-omf':'COMMON',mixed.KIND:'MIXED',machine_bss.KIND:'BSS'}[r['kind']]]+=1
  p=Path(r['source']);need(not p.is_absolute()and'..'not in p.parts and p.suffix.lower()in ('.c','.asm'),'in-project source')
  need(r['selected_owners']and len(set(r['selected_owners']))==len(r['selected_owners'])and not owners.intersection(r['selected_owners']),'unique nonempty selected ownership');owners.update(r['selected_owners'])
  need(re.fullmatch('[0-9a-f]{64}',r['source_sha256'])and re.fullmatch('[0-9a-f]{64}',r['comparison_expected_raw_sha256']),'whole source/raw hash')
  key=(r['kind'],r['source'],tuple(r['compiler_flags']),r['source_name'],r.get('object_profile'));need(key not in identities,'duplicate whole input identity');identities.add(key)
  if r['kind']==mixed.KIND:mixed.validate_row(r)
  elif r['kind']==machine_bss.KIND:machine_bss.validate_row(r)
  elif r['kind']=='asm-whole-omf':need(r['public_adapter']['function']=='assemble'and r['generator']in ('DOSBox','NASM'),'explicit ASM route')
  else:need(r['compiler']in ('msc500','msc510','msc400')and re.fullmatch(r'[A-Z][A-Z0-9_]{0,7}\.C',r['source_name']),'exact compiler/basename')
 need(counts==d['counts'],'all counts derived from vector, no threshold waiver')
 need(d['link']=={'switches':['/NOD','/DOSSEG','/NOFARCALLTRANSLATION','/MAP','/STACK:4096'],'libraries':['SLIBC','LIBH'],'max_calls':1},'reviewed authentic LINK contract')
 jobs=d['deferred_jobs']
 if jobs:
  need(len(jobs)==1 and set(jobs[0])=={'unit_id','policy','adapter_module','adapter_sha256','primitive_sha256','pins_sha256','unit_sha256','profile_sha256','runtime_config_sha256'},'one exact complete deferred registration')
  j=jobs[0];need(j['unit_id']=='runtime_data_crt0_s3'and j['policy']=='crt0-data88-literal12-reservation76-deferred-v2'and j['adapter_module']=='crt0_data88_deferred','sole exact deferred policy/identity')
  need(all(re.fullmatch('[0-9a-f]{64}',str(j[k]))for k in ['adapter_sha256','primitive_sha256','pins_sha256','unit_sha256','profile_sha256','runtime_config_sha256']),'all real reviewed deferred fingerprints required')
  need(d['deferred_crt0_DATA88_status']=='REGISTERED_EXACT_CURRENT_RUN_LINK_ONLY','explicit deferred state')
 else:need(d['deferred_crt0_DATA88_status']=='NOT_REGISTERED_NOT_ADMITTED','no implicit deferred admission')
 packet.registration(d)
 return d

def validate_project(d,project):
 validate_descriptor(d);project=Path(project).resolve()
 for name,h in d['canonical_heads'].items():need(sha(regular(project/name).read_bytes())==h,'descriptor rebase required: '+name)
 for r in d['rows']:
  if r['kind']==mixed.KIND:mixed.validate_sources(r,project)
  need(sha(regular(project/r['source']).read_bytes())==r['source_sha256'],'source rebase required '+r['source'])
  for name,h in r['generation_tools'].items():need(sha(regular(project/name).read_bytes())==h,'generation tool '+name)
  if r.get('public_adapter'):need(sha(regular(project/(r['public_adapter']['module']+'.py')).read_bytes())==r['public_adapter']['sha256'],'public ASM adapter changed')
 for x in d['tools'].values():
  p=Path(x['path']);p=p if p.is_absolute()else project/p;need(sha(regular(p).read_bytes())==x['sha256'],'authentic tool '+str(p))

def select_source(d,report,components,project,observations=None):
 """Artifact report is a selector, never freshness authority; observations seal raw."""
 validate_descriptor(d);components=Path(components).resolve();project=Path(project).resolve()
 need(len(report['units'])==d['units']and report['summary']['failed_units']==0,'all registered component comparisons must pass')
 units={u['id']:u for u in report['units']};common={u['id']:u for u in report['source_allocation_inputs']};layouts={u['id']:u for u in report.get('machine_layout_inputs',[])}
 need(len(layouts)==d['counts'].get('BSS',0),'exact optional machine-layout inputs')
 need(len(common)==d['counts']['COMMON'],'complete source allocation registry')
 need(len(units)==len(report['units']),'duplicate component identity')
 expected_artifacts={u['object_artifact']for u in units.values()if u.get('language')!='runtime'and u.get('object_artifact')}|{u['object']for u in common.values()}|{u['object']for u in layouts.values()}
 rows=[]
 for spec in d['rows']:
  selected=[(layouts if spec['kind']==machine_bss.KIND else common if spec['kind']=='common-whole-omf'else units)[n]for n in spec['selected_owners']]
  paths={u['object']if spec['kind']in ('common-whole-omf',machine_bss.KIND)else u['object_artifact']for u in selected};need(len(paths)==1,'one whole object per descriptor role')
  p=Path(next(iter(paths)));need(p.is_absolute()and p.resolve().is_relative_to(components)and'runtime'not in p.relative_to(components).parts and p.suffix.lower()=='.obj','new component SOURCE only, runtime excluded');raw=regular(p).read_bytes();h=sha(raw)
  need(h==spec['comparison_expected_raw_sha256'],'whole generated object comparison '+spec['source'])
  if spec['kind']==mixed.KIND:
   mixed.validate_selected(spec,selected,components,project);need(all(u['object_sha256']==h for u in selected),'all mixed-owner raw identities')
  else:
   need(all(u['source']==spec['source']and u['object_sha256']==h for u in selected),'all owner source/raw identities')
  need(sha(regular(project/spec['source']).read_bytes())==spec['source_sha256'],'source unchanged after check.run')
  if observations is not None:need(any(e['slot']==spec['order_slot']and e['raw_sha256']==h and e['fresh_witness']is True for e in observations),'no real observed fresh object for '+spec['source'])
  rows.append({'order_slot':spec['order_slot'],'DOS_name':spec['DOS_name'],'kind':spec['kind'],'source':spec['source'],'source_sha256':spec['source_sha256'],'selected_owners':spec['selected_owners'],'object_path':str(p),'object_sha256':h,'size':len(raw)}|mixed.seal_extra(spec,selected))
 need(len({r['object_path']for r in rows})==len(rows)and{r['object_path']for r in rows}==expected_artifacts,'entire SOURCE artifact set exhausted without runtime members/extras')
 return rows

def select_source_phase(d,ordinary_results,allocations,components,project,observations,*,expected_ordinary_ids,machine_layouts=(),packet_context=None,packet_pending=()):
 """Intermediate generator results only; never manufactures a final-success dict."""
 validate_descriptor(d);components=Path(components).resolve();project=Path(project).resolve()
 need([r['id']for r in ordinary_results]==list(expected_ordinary_ids),'exact ordinary result vector before SOURCE seal')
 need(all(r['status']in ('asm_matched','c_matched','c_data_matched','asm_data_matched','asm_code_matched','runtime_matched')for r in ordinary_results),'ordinary generation/comparisons must pass; deferred pending is not included: '+json.dumps([{'id':r.get('id'),'status':r.get('status'),'error':r.get('error')}for r in ordinary_results if r.get('status')not in ('asm_matched','c_matched','c_data_matched','asm_data_matched','asm_code_matched','runtime_matched')][:20]))
 pending_metadata={}
 if packet_context is not None:
  need(packet.registration(d)is not None,'registered finite packet source group');pending_metadata=packet.selector_metadata(packet_context,packet_pending)
 else:need(not packet_pending and packet.registration(d)is None,'no unregistered packet tokens')
 units={u['id']:u for u in ordinary_results};need(not set(units).intersection(pending_metadata),'no duplicate ordinary/pending identities');units.update(pending_metadata);common={u['id']:u for u in allocations};layouts={u['id']:u for u in machine_layouts}
 need(len(layouts)==len(machine_layouts)==d['counts'].get('BSS',0),'exact optional machine-layout input vector')
 need(len(common)==d['counts']['COMMON']and len(units)==len(ordinary_results)+len(pending_metadata),'complete ordinary/privatepending/provider identities')
 expected_artifacts={u['object_artifact']for u in units.values()if u.get('language')!='runtime'and u.get('object_artifact')}|{u['object']for u in common.values()}|{u['object']for u in layouts.values()}
 rows=[]
 for spec in d['rows']:
  selected=[(layouts if spec['kind']==machine_bss.KIND else common if spec['kind']=='common-whole-omf'else units)[n]for n in spec['selected_owners']]
  paths={u['object']if spec['kind']in ('common-whole-omf',machine_bss.KIND)else u['object_artifact']for u in selected};need(len(paths)==1,'one whole object per descriptor role')
  p=Path(next(iter(paths)));need(p.is_absolute()and p.resolve().is_relative_to(components)and'runtime'not in p.relative_to(components).parts and p.suffix.lower()=='.obj','new component SOURCE only, runtime excluded');raw=regular(p).read_bytes();h=sha(raw)
  need(h==spec['comparison_expected_raw_sha256'],'whole generated object comparison '+spec['source'])
  if spec['kind']==mixed.KIND:
   mixed.validate_selected(spec,selected,components,project);need(all(u['object_sha256']==h for u in selected),'all mixed-owner raw identities')
  else:
   need(all(u['source']==spec['source']and u['object_sha256']==h for u in selected),'all owner source/raw identities')
  need(sha(regular(project/spec['source']).read_bytes())==spec['source_sha256'],'source unchanged after check.run')
  if observations is not None:need(any(e['slot']==spec['order_slot']and e['raw_sha256']==h and e['fresh_witness']is True for e in observations),'no real observed fresh object for '+spec['source'])
  rows.append({'order_slot':spec['order_slot'],'DOS_name':spec['DOS_name'],'kind':spec['kind'],'source':spec['source'],'source_sha256':spec['source_sha256'],'selected_owners':spec['selected_owners'],'object_path':str(p),'object_sha256':h,'size':len(raw)}|mixed.seal_extra(spec,selected))
 need(len({r['object_path']for r in rows})==len(rows)and{r['object_path']for r in rows}==expected_artifacts,'entire SOURCE artifact set exhausted without runtime members/extras')
 return rows

def final_status(report,link):
 # No packer/layout verifier has been admitted. Never infer full match from rows.
 return {'status':'INCOMPLETE','component_failed_units':report['summary']['failed_units'],'undefined_symbols':link['undefined_symbols'],'all_names_resolved':not link['undefined_symbols'],'layout_verified':False,'header_verified_against_shipped':False,'packed_file_sha256_verified':False,'full_executable_match':False,'reason':'Exact full layout/header/packing verification remains unimplemented; whole-TU held/unowned CODE also requires reconciliation.','authored_C_function_credit':0,'packed_file_credit':0}
