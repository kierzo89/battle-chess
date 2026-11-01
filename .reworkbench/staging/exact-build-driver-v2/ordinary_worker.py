"""Staged finite ordinary-source worker. No target/reference/cached-object inputs."""
from pathlib import Path
import json,sys,hashlib,locale,codecs,subprocess
R=Path('/home/kierzo/chess');P=Path(__file__).resolve().parent;M=R/'matching';sys.path.insert(0,str(M))
from mixed_tail_undo_generation16 import _process,Guard
H=lambda b:hashlib.sha256(b).hexdigest()
def run(key,output):
 manifest=json.loads((P/'source-overrides.json').read_text());r=manifest['ordinary_overrides'][str(key)];source=Path(r['source']).resolve();assert H(source.read_bytes())==r['source_sha256'];allowed={source:r['source_sha256']};backend=r['backend'];calls=[]
 if backend=='msc500':
  import msc
  _,pins=msc.validate_toolchain(compiler='msc500')
  for n,h in pins.items():allowed[(M/'toolchains/msc500'/n).resolve()]=h
  tool=Path('/usr/bin/dosbox').resolve();allowed[tool]='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
 elif backend=='nasm':
  tool=Path('/usr/bin/nasm').resolve();allowed[tool]='57b8fc5957237b0d9b1ff48c8f5823780fb8ce968d9b8434850c06941ad5d5f5'
 else:raise ValueError('unknown reviewed backend')
 for p,h in allowed.items():assert H(p.read_bytes())==h
 root=Path(output).resolve();assert not root.exists();root.mkdir();locale.getpreferredencoding(False);codecs.lookup('cp437');guard=Guard(root,allowed)
 with guard:
  if backend=='msc500':
   flags=r['flags'];assert flags in [['/AS','/Zi'],['/AS','/Zl','/Zi'],['/AS','/Gs','/Os','/Zi']];(root/'UNIT.C').write_bytes(source.read_bytes());_process(root,M/'toolchains/msc500','T:\\CL /c '+' '.join(flags)+' C:\\UNIT.C','C5',calls)
  else:
   (root/'UNIT.ASM').write_bytes(source.read_bytes());argv=[str(tool),'-f','obj','-o',str(root/'UNIT.OBJ'),str(root/'UNIT.ASM')];p=subprocess.run(argv,capture_output=True,timeout=30);(root/'STDOUT.bin').write_bytes(p.stdout);(root/'STDERR.bin').write_bytes(p.stderr);assert p.returncode==0;p=None;calls.append({'phase':'NASM','argv':argv,'returncode':0,'terminal':True,'reaped':True})
  digest=H((root/'UNIT.OBJ').read_bytes())
 assert not guard.events['blocked'];result={'status':'FRESH_STAGED_ORDINARY_SOURCE_GENERATION_NOT_ADMISSION','key':key,'source':r,'object_path':str(root/'UNIT.OBJ'),'object_sha256':digest,'tools':{str(k):v for k,v in allowed.items()if k!=source},'calls':calls,'guard':guard.events,'canonical_credit_added':0};(root/'generation.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 r=run(sys.argv[1],sys.argv[2]);print(json.dumps({k:r[k]for k in ['status','key','object_path','object_sha256']}))
