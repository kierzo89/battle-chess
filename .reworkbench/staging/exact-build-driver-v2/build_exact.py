"""Staged single-command independent build. No canonical admission is implied."""
from pathlib import Path
import argparse,concurrent.futures,fcntl,hashlib,json,subprocess,sys,time
P=Path(__file__).resolve().parent;R=Path('/home/kierzo/chess');M=R/'matching';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def preflight(output):
 output=Path(output);need(output.is_absolute(),'absolute output required');need(not output.is_symlink(),'output symlink forbidden');output=output.resolve();need(output.parent==M/'build','output must be direct child of matching/build');base=output.with_name(output.name+'-source269');need(not output.exists()and not base.exists(),'fresh output and base directories required')
 manifest=json.loads((P/'bundle-manifest.json').read_text())
 for row in manifest['files']:
  rel=Path(row['path']);need(not rel.is_absolute()and '..'not in rel.parts,'invalid bundle path');file=P/rel;need(file.is_file()and not file.is_symlink()and H(file)==row['sha256'],'bundle input changed: '+str(rel))
 sys.path.insert(0,str(M));import build_game
 build_game.validate_inputs(M)
 return output,base,manifest

def run(output):
 output,base,manifest=preflight(output)
 with (R/'.reworkbench/exact-build.lock').open('a')as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);output.mkdir();t=time.monotonic();receipts={}
  def persist(name,data):(output/name).write_text(json.dumps(data,indent=2)+'\n')
  persist('bundle-receipt.json',manifest)
  with (output/'base.log').open('wb')as log:
   command=[str(M/'build/test-env/bin/python'),'-B',str(M/'build_game.py'),'--output',str(base),'--compile-workers','8'];proc=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
  need(proc.returncode in (0,1),'base generation failed; inspect base.log, do not retry automatically')
  report=json.loads((base/'build-report.json').read_text());seal=json.loads((base/'source-seal.json').read_text());need(report['component_failed_units']==0 and report['run_id']==seal['run_id'],'base source seal mismatch');need(report['source_seal_sha256']==seal['SOURCE_digest'],'base seal digest mismatch')
  ordinary=json.loads((P/'source-overrides.json').read_text())['ordinary_overrides'];compound=json.loads((P/'compound-recipes.json').read_text())['recipes'];jobs=[('ordinary',k)for k in ordinary]+[('compound',str(r['slot']))for r in compound];need(len(jobs)==38,'override cohort changed');work=output/'overrides';work.mkdir()
  def generate(item):
   kind,key=item;dest=work/(kind+'-'+key);cmd=['/usr/bin/python3','-B',str(P/(kind+'_worker.py')),key,str(dest)]+([str(base)]if kind=='compound'else[])
   r=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(work/(kind+'-'+key+'.log')).write_text(r.stdout+'\n'+r.stderr);need(r.returncode==0,'override held: '+key);receipt=dest/'generation.json';data=json.loads(receipt.read_text());need(not data['guard']['blocked'],'guard denied source generation');need(H(Path(data['object_path']))==data['object_sha256'],'object changed after generation');return key,data,receipt
  with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
   for key,data,path in pool.map(generate,jobs):receipts[key]=(data,path)
  fresh={r['order_slot']:r for r in seal['rows']};rows=[]
  for recipe in json.loads((P/'final-order-recipe.json').read_text())['rows']:
   slot=recipe['source_slot'];key=str(slot)if slot is not None else recipe['name'].removesuffix('.OBJ')
   if recipe['unchanged']:
    row=fresh[slot];source={'base_run_id':seal['run_id'],'source_sha256':row['source_sha256']};obj=Path(row['object_path']);digest=row['object_sha256'];need(obj.resolve().is_relative_to(base),'base object escaped fresh run')
   else:
    row,receipt=receipts[key];source={'receipt':str(receipt),'sha256':H(receipt)};obj=Path(row['object_path']);digest=row['object_sha256'];need(obj.resolve().is_relative_to(work),'override escaped fresh run')
   need(H(obj)==digest,'fresh object mutated');rows.append({**recipe,'object_path':str(obj),'sha256':digest,'provenance':source})
  need(len(rows)==225,'final cohort changed');order={'status':'SAME_RUN_SOURCE_INPUTS_SEALED','base_run_id':seal['run_id'],'rows':rows,'canonical_credit_added':0};persist('fresh-order.json',order)
  import runtime_library,link_pack
  runtime_library.run(output/'runtime');result=link_pack.run(base,output/'fresh-order.json',output/'runtime/verification.json',output/'final');result.update(total_seconds=time.monotonic()-t,bundle_manifest_sha256=H(P/'bundle-manifest.json'),canonical_admission=False);persist('build-report.json',result);print(json.dumps(result,indent=2));need(result['status']=='PASS_FRESH_SOURCE_DERIVED_EXACT_EXECUTABLE','full native verification held');return result
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True);ap.add_argument('--preflight-only',action='store_true');args=ap.parse_args()
 if args.preflight_only:preflight(args.output);print('PREFLIGHT_PASS_NO_GENERATION')
 else:run(args.output)
