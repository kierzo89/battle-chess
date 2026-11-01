"""Reviewed fresh SOURCE/LINK/deferred runtime engine; called by build_game.py.

All source generators and comparison consumers are the validated finite490
implementations. No agent release, cached component or outer receipt is required.
"""
from pathlib import Path
import sys,json,uuid,traceback,importlib.util
sys.dont_write_bytecode=True
from cohort import need,sha,load,validate_project,final_status
_CAP=object()
class SourceSeal:
 def __init__(self,cap,run_id,rows,classification):
  need(cap is _CAP,'private source seal factory');self._cap=cap;self.run_id=run_id;self.rows=json.loads(json.dumps(rows));self.classification=classification;self.digest=sha(json.dumps(self.rows,sort_keys=True).encode())
 def valid(self):return self._cap is _CAP and self.digest==sha(json.dumps(self.rows,sort_keys=True).encode())

def write(p,value):
 with Path(p).open('x')as f:json.dump(value,f,indent=2);f.write('\n')
def run_fresh(project,descriptor,out,compile_workers=1):
 project=Path(project).resolve();out=Path(out);package=Path(__file__).resolve().parent
 need(package.parents[1]==project,'engine must be installed at project/build_pipeline/engine_v1')
 validate_project(descriptor,project);out.mkdir();(out/'build.claim').open('x').close();write(out/'descriptor.json',descriptor);run_id=uuid.uuid4().hex
 try:
  sys.path.insert(0,str(project));import source_inputs
  from source_phase import SourceObserver
  from fresh_lifecycle import FreshLifecycle
  from authentic_link import emit_link
  spec=importlib.util.spec_from_file_location('reviewed_checker_lifecycle',package/'check_lifecycle_proposed.py');check=importlib.util.module_from_spec(spec);sys.modules[spec.name]=check;spec.loader.exec_module(check)
  components=out/'components';need(not components.exists(),'exclusive fresh components');observer=SourceObserver(project,descriptor)
  if compile_workers>1:
   from parallel_compile import ParallelCompiler
   observer.parallel=ParallelCompiler(observer,compile_workers)
  lifecycle=FreshLifecycle(descriptor,project,out,components,observer,lambda rid,rows,kind:SourceSeal(_CAP,rid,rows,kind),emit_link)
  with observer.install(check,source_inputs):report=check.run(project.parent,project,project.parent/'CHESS.EXE',components,descriptor['tools']['NASM']['path'],lifecycle=lifecycle)
  need(not observer.poisoned and lifecycle.phase=='FINALIZE_ALLOWED','same-run SOURCE/LINK/deferred finalization')
  validate_project(descriptor,project);result=final_status(report,lifecycle.link)
  result.update(schema='battlechess-fresh-game-build-v1',run_id=lifecycle.run_id,classification='FRESH_SINGLE_CHECKER_LIFECYCLE_SOURCE_THEN_LINK_THEN_FINAL_REPORT',component_summary=report['summary'],SOURCE=descriptor['counts'],observed_source_public_callbacks=len(observer.events),source_process_count=None,aggregate_SOURCE_LINK_calls=1,ordinary_runtime_helper_calibration_LINK_calls=None,total_LINK_process_count=None,actual_LINK_status=lifecycle.link['status'],source_seal_sha256=lifecycle.seal.digest,LINK_result_sha256=sha((out/'LINK/result.json').read_bytes()),deferred_CRT0_DATA88='CONSUMED_ONLY_FROM_SAME_FRESH_TYPED_AGGREGATE',EXE_execution=False,canonical_changes=False,host_python=sys.version)
  write(out/'build-report.json',result);return result
 except BaseException as exc:
  if 'observer'in locals()and observer.parallel is not None:observer.parallel.close(False)
  write(out/'HELD.json',{'status':'HELD_NO_RETRY','error':repr(exc),'traceback':traceback.format_exc(),'run_id':run_id,'full_executable_match':False});raise
