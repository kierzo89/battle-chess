#!/usr/bin/env python3
"""Fresh source build + authentic LINK + deferred runtime verification.

Exit 0: complete original executable verified. Exit 1: checked but incomplete.
Exit 2: invalid inputs/output or a failed generation/comparison phase.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
PROJECT=Path(__file__).resolve().parent

def need(v,message):
 if not v:raise ValueError(message)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def project_file(project,name):
 relative=Path(name);need(not relative.is_absolute()and'..'not in relative.parts,'manifest path must be project-relative')
 p=project/relative;walk=project
 for part in relative.parts:
  walk=walk/part;need(not walk.is_symlink(),'manifest input symlink forbidden: '+name)
 need(p.is_file()and p.resolve().is_relative_to(project),'regular in-project input required: '+name);return p

def validate_inputs(project):
 project=Path(project).resolve();m=json.loads(project_file(project,'build_pipeline/manifest.json').read_text());need(m['schema']=='battlechess-fresh-build-manifest-v1','unknown build manifest schema')
 for row in m['engine_files']+m['project_inputs']:need(digest(project_file(project,row['path']))==row['sha256'],'reviewed input changed: '+row['path']+'; rebase the descriptor/manifest explicitly')
 for row in m['system_tools']:
  p=Path(row['path']);need(p.is_absolute()and p.is_file()and not p.is_symlink()and digest(p)==row['sha256'],'pinned system tool differs: '+row['name'])
 descriptor=json.loads(project_file(project,m['descriptor']).read_text());need(descriptor['counts']==m['SOURCE']and descriptor['units']==m['units'],'manifest/cohort mismatch')
 engine=project_file(project,m['engine_entry']);need(engine.parent==project/'build_pipeline/engine_v1','reviewed engine location');return engine,descriptor

def fresh_output(project,value):
 project=Path(project).resolve();raw=Path(value);raw=raw if raw.is_absolute()else project/raw
 need(not raw.is_symlink(),'output must not be a symlink');out=raw.resolve();need(out.parent==project/'build'and out.parent.is_dir(),'output must be a direct new directory under matching/build')
 need(not out.exists(),'output already exists; choose a new directory');return out

def load_engine(path):
 package=path.parent
 for name in ['pipeline','cohort','source_phase','fresh_lifecycle','authentic_link','closed_aggregate','deferred_merge']:
  module=sys.modules.get(name)
  if module is not None:need(Path(module.__file__).resolve()==package/(name+'.py'),'another build engine is already loaded: '+name)
 sys.path.insert(0,str(package));spec=importlib.util.spec_from_file_location('pipeline',path);module=importlib.util.module_from_spec(spec);sys.modules['pipeline']=module;spec.loader.exec_module(module);return module

def run(project,output,compile_workers=1):
 project=Path(project).resolve();out=fresh_output(project,output);engine,descriptor=validate_inputs(project);result=load_engine(engine).run_fresh(project,descriptor,out,compile_workers=compile_workers)
 summary=result['component_summary'];need(summary['failed_units']==0 and result['status']in ('INCOMPLETE','COMPLETE'),'generation/comparison did not complete')
 print('Report: '+str(out/'build-report.json'))
 if result['full_executable_match']:
  need(result['status']=='COMPLETE','full-match status mismatch');print('Complete original executable verified.');return 0
 print('INCOMPLETE: all '+str(summary['reviewed_extents'])+' component comparisons pass; '+str(len(result['undefined_symbols']))+' unresolved names.');return 1

def main(argv=None):
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,help='Fresh directory under matching/build (relative to matching, or absolute). Existing directories are refused.');parser.add_argument('--compile-workers',type=int,choices=range(1,9),default=1);args=parser.parse_args(argv)
 try:return run(PROJECT,args.output,args.compile_workers)
 except (Exception,KeyboardInterrupt)as exc:
  print('Build failed: '+str(exc),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
