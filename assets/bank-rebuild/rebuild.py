from pathlib import Path
import argparse,json,importlib.util
spec=importlib.util.spec_from_file_location("packaged_repack",Path(__file__).with_name("repack.py"))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);rebuild=m.rebuild
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise ValueError('Fresh output directory required')
a.output.mkdir(parents=True)
base=Path(__file__).resolve().parent
results={name:rebuild(base/name,a.output/name) for name in ('ALLCANM1','ALLCANM2')}
(a.output/'report.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
