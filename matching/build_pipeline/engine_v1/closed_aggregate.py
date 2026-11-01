"""Typed same-process fresh aggregate capability for post-LINK comparisons.

No JSON loader creates this capability. A retained EXE/MAP pair is insufficient.
Only the reviewed lifecycle may register an observed fresh SOURCE seal and close
its one real LINK result. Reads here occur after all source/LINK GEN guards close.
"""
from pathlib import Path
import json,re
from collections import Counter
from cohort import need,sha,regular
import mixed_source_dispatch_evaluation16 as mixed
import near_bss_layout16 as machine_bss
_CAP=object();_REGISTERED={};_CLOSED=set()

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def register_fresh_source(source,descriptor,observer):
 from pipeline import SourceSeal
 from source_phase import SourceObserver
 need(type(source)is SourceSeal and type(observer)is SourceObserver,'exact live producer capability types, no duck-typed fixture')
 need(source.valid()and source.classification=='FRESH_INTERMEDIATE_SOURCE_BEFORE_FINAL_REPORT','fresh intermediate SOURCE capability only')
 need(observer.current is None and observer.roots==[]and not observer.poisoned,'all GEN scopes closed')
 need(len(source.rows)==descriptor['counts']['SOURCE']and all(any(e['slot']==r['order_slot']and e['raw_sha256']==r['object_sha256']and e['fresh_witness']is True for e in observer.events)for r in source.rows),'complete actual fresh whole SOURCE witnesses')
 for row in source.rows:
  if row['kind']==mixed.KIND:
   mixed.validate_seal_row(row);need(any(e['slot']==row['order_slot']and e.get('mixed_fresh_witness',{}).get('generation_sources')==row['generation_sources']and e.get('mixed_fresh_witness',{}).get('mixed_SHA256')==row['object_sha256']for e in observer.events),'actual dual-source two-process mixed witness required')
 need(id(source)not in _REGISTERED,'one live source registration');_REGISTERED[id(source)]=(source,sha(canonical(descriptor)))

class ClosedAggregateSealV1:
 def __init__(self,cap,source,descriptor,root,result):
  need(cap is _CAP,'private aggregate constructor');self._cap=cap;self._source=source;self._descriptor=descriptor;self.root=Path(root).resolve();self._result=json.loads(json.dumps(result));self.run_id=source.run_id;self.descriptor_sha256=sha(canonical(descriptor));self.SOURCE_digest=source.digest;self.link_result_sha256=sha((self.root/'result.json').read_bytes());self.object_rows=json.loads(json.dumps(source.rows));self._snapshot=sha(canonical(self._result));self._validate()
 def _validate(self):
  need(self._cap is _CAP and self._source.valid()and id(self._source)in _REGISTERED,'live source capability')
  need(self._source.classification=='FRESH_INTERMEDIATE_SOURCE_BEFORE_FINAL_REPORT','fresh source role remains unchanged')
  need([r['order_slot']for r in self.object_rows]==list(range(len(self.object_rows)))and[r['DOS_name']for r in self.object_rows]==['O%03d.OBJ'%i for i in range(len(self.object_rows))]and len({r['object_path']for r in self.object_rows})==len(self.object_rows),'independent complete source order/path uniqueness')
  need(all(r['kind']in ('c-whole-omf','asm-whole-omf','common-whole-omf',mixed.KIND,machine_bss.KIND)for r in self.object_rows),'no runtime/member object source role')
  for row in self.object_rows:mixed.validate_seal_row(row)
  source,dh=_REGISTERED[id(self._source)];need(source is self._source and dh==self.descriptor_sha256==sha(canonical(self._descriptor)),'same reviewed descriptor and source object')
  need(sha(canonical(self._result))==self._snapshot and sha(regular(self.root/'result.json').read_bytes())==self.link_result_sha256 and json.loads((self.root/'result.json').read_text())==self._result,'unchanged actual LINK result')
  r=self._result;p=r['process'];need(r['run_id']==self.run_id and r['source_seal_sha256']==self.SOURCE_digest and r['objects']==self.object_rows and r['objects_count']==len(self.object_rows)==self._descriptor['counts']['SOURCE'],'same exact ordered source matrix/run')
  need(r['LINK_calls']==1 and p['terminal']is True and p['reaped']is True and p['returncode']==0 and type(p['pid'])is int and p['pid']>0,'real one closed/reaped source-only host child')
  need(r['partial_EXE_executed']is False and r['target_or_carrier_or_runtimeOBJ_inputs']is False and r['extra_alias_stub_or_provider']is False and sorted(Counter(r['active_denied_probes']).values())==[4]*5,'exact source-only LINK guard/roles')
  need(r['LINK_command']=='T:\\LINK /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP /STACK:4096 @INPUTS.RSP','exact reviewed LINK command')
  argv=p['argv'];need(len(argv)==4 and argv[0]==self._descriptor['tools']['DOSBox']['path']and argv[1]=='-conf'and argv[3]=='-noconsole'and Path(argv[2]).name=='dosbox.conf','actual pinned DOSBox command')
  scratch=Path(argv[2]).parent;mounts=[line for line in self._read('dosbox.conf').decode('ascii').splitlines()if line.startswith('mount ')];need(mounts==['mount c \"'+str(scratch)+'\"','mount t \"'+str(scratch/'only-link')+'\" -ro','mount r \"'+str(scratch/'only-slibc')+'\" -ro','mount h \"'+str(scratch/'only-libh')+'\" -ro'],'only exact fresh input/tool/full-library mounts')
  for name,h in r['artifacts'].items():
   q=(self.root/name);need(not Path(name).is_absolute()and'..'not in Path(name).parts and q.resolve().is_relative_to(self.root)and sha(regular(q).read_bytes())==h,'whole actual aggregate artifact '+name)
  for row in self.object_rows:need(self._read(row['DOS_name'])and sha(self._read(row['DOS_name']))==row['object_sha256'],'ordered raw source object copied unchanged')
  for spec,row in zip(self._descriptor['rows'],self.object_rows):
   if row['kind']==machine_bss.KIND:machine_bss.validate_row(spec);machine_bss.inspect(self._read(row['DOS_name']))
  expected=('+\r\n'.join(x['DOS_name']for x in self.object_rows)+'\r\nPARTIAL.EXE\r\nPARTIAL.MAP\r\nR:\\SLIBC.LIB+H:\\LIBH.LIB;\r\n').encode('ascii');need(self._read('INPUTS.RSP')==expected,'exact response order/full libraries/no extra objects')
  for key,name in [('LINK','only-link/LINK.EXE'),('SLIBC','only-slibc/SLIBC.LIB'),('LIBH','only-libh/LIBH.LIB')]:need(sha(self._read(name))==self._descriptor['tools'][key]['sha256'],'genuine complete selected tool/library')
  log=self._read('LINK.LOG').decode('cp437');errors=re.findall(r'(?im)^LINK : error (L\d+):',log);undefined=sorted(set(re.findall(r'(?im)^\s*([^\s:]+)\s+in file\(s\):',log)));status=self._read('RESULT.TXT').decode('ascii').strip();need(undefined==r['undefined_symbols']and((status=='success'and not errors and not undefined)or(status=='link_failed'and errors==['L2029']and undefined)),'exact actual diagnostic, never infer full match')
  return True
 def _read(self,name):
  need(name in self._result['artifacts'],'closed aggregate member only');q=self.root/name;raw=regular(q).read_bytes();need(sha(raw)==self._result['artifacts'][name],'artifact hash');return raw
 def valid(self):return self._validate()
 def read_artifact(self,name):self._validate();return self._read(name)
 def source_raws(self):self._validate();return tuple(self._read(r['DOS_name'])for r in self.object_rows)

def close_after_link(source,descriptor,root,result):
 need(id(source)in _REGISTERED and id(source)not in _CLOSED,'one closure after actual same-process fresh source registration')
 seal=ClosedAggregateSealV1(_CAP,source,descriptor,root,result);_CLOSED.add(id(source));return seal
