"""Finite staged source-only worker. Results are unadmitted; no target comparisons here."""
from pathlib import Path
import json,sys,hashlib,re,importlib.util,locale,codecs
R=Path('/home/kierzo/chess');P=Path(__file__).resolve().parent;M=R/'matching';sys.path.insert(0,str(M))
from mixed_tail_undo_generation16 import _process,Guard
from omf import read_omf
H=lambda b:hashlib.sha256(b).hexdigest()
def clean_listing(fa,recipe):
 result=fa;omitted=[]
 for n,k in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  x=(n+"\tSEGMENT  BYTE PUBLIC '"+k+"'\r\n"+n+'\tENDS\r\n').encode();assert result.count(x)==1;result=result.replace(x,b'',1);omitted.append(x)
 replacement=recipe.get('authored_replacement');proof={'empty_debug_declarations_omitted':True,'C_listing_sha256':H(fa)}
 if replacement:
  pin=replacement['source'];asm=Path(pin['path']).read_bytes();assert H(asm)==pin['sha256'];body=asm.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n');symbol=re.escape(replacement['symbol'].encode());pattern=symbol+rb'\tPROC NEAR\r\n.*?'+symbol+rb'\tENDP\r\n';matches=list(re.finditer(pattern,result,re.S));assert len(matches)==1;m=matches[0];original=m.group();result=result[:m.start()]+body+result[m.end():];proof.update(authored_symbol=replacement['symbol'],authored_source_sha256=pin['sha256'],authored_credit='assembly_only');inverse=result.replace(body,original,1)
 else:inverse=result
 assert inverse.replace(b'DGROUP\tGROUP\tCONST, _BSS, _DATA\r\n',b''.join(omitted)+b'DGROUP\tGROUP\tCONST, _BSS, _DATA\r\n',1)==fa
 dialect=recipe.get('dialect','none')
 if dialect=='input_REPNE8_AND_CX_WORD2':
  assert result.count(b'\trep\tmovsw\r\n')==8 and result.count(b'\tand\tcx,2\r\n')==1;before=result;result=result.replace(b'\trep\tmovsw\r\n',b'\trepne\tmovsw\r\n').replace(b'\tand\tcx,2\r\n',b'\tand\tcx,WORD PTR 2\r\n');assert result.replace(b'\trepne\tmovsw\r\n',b'\trep\tmovsw\r\n').replace(b'\tand\tcx,WORD PTR 2\r\n',b'\tand\tcx,2\r\n')==before
 elif dialect=='outside_ENDP_RET':
  tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n';assert result.endswith(b'_save_active_arena\tENDP\r\n'+tail);result=result[:-len(tail)]+b'\tret\r\n_TEXT\tENDS\r\nEND\r\n';proof['outside_ENDP_authored_RET_bytes']=1
 else:assert dialect=='none'
 proof.update(dialect=dialect,source_inverse_before_explicit_dialect_changes=True,composed_sha256=H(result));return result,proof

def run(slot,output,fresh_base):
 manifest=json.loads((P/'compound-recipes.json').read_text());recipe=next(x for x in manifest['recipes']if x['slot']==slot);pins=[];mode=recipe['mode'];fresh_base=Path(fresh_base).resolve()
 if mode=='same_run_fresh_composed_source':
  report=json.loads((fresh_base/'build-report.json').read_text());seal=json.loads((fresh_base/'source-seal.json').read_text());assert report['component_summary']['failed_units']==0;assert report['run_id']==seal['run_id'];source=fresh_base/recipe['relative_source'];pins.append({'path':str(source),'sha256':recipe['source_sha256']})
 else:source=Path(recipe['source']['path']);pins.append(recipe['source'])
 if recipe.get('authored_replacement'):pins.append(recipe['authored_replacement']['source'])
 modulepin=manifest['placement_module'];assert H(Path(modulepin['path']).read_bytes())==modulepin['sha256'];spec=importlib.util.spec_from_file_location('checked_placement',modulepin['path']);placement=importlib.util.module_from_spec(spec);spec.loader.exec_module(placement)
 import msc
 allowed={Path(x['path']).resolve():x['sha256']for x in pins}
 for compiler in ['msc500','msc510']:
  manifest_hash,hashes=msc.validate_toolchain(compiler=compiler)
  for name,digest in hashes.items():allowed[(M/'toolchains'/compiler/name).resolve()]=digest
  for rel in ['toolchains/'+compiler+'/manifest.json','config/'+compiler+'.json']:
   p=M/rel;allowed[p.resolve()]=H(p.read_bytes())
 dosbox=Path('/usr/bin/dosbox');allowed[dosbox.resolve()]='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
 for path,digest in allowed.items():assert H(path.read_bytes())==digest
 root=Path(output).resolve();assert not root.exists();root.mkdir();calls=[];proof={};locale.getpreferredencoding(False);codecs.lookup('cp437');guard=Guard(root,allowed)
 with guard:
  if mode=='fresh_C_listing':
   c=root/'C5';c.mkdir();(c/'UNIT.C').write_bytes(source.read_bytes());flags=recipe['flags'];assert flags in [['/AS','/Zi'],['/AS','/Gs','/Os','/Zi']];_process(c,M/'toolchains/msc500','T:\\CL /c '+' '.join(flags)+' /FaC:\\UNIT.ASM C:\\UNIT.C','C5',calls);asm,proof=clean_listing((c/'UNIT.ASM').read_bytes(),recipe)
  else:asm=source.read_bytes()
  base=root/'baseline';base.mkdir();(base/'UNIT.ASM').write_bytes(asm);_process(base,M/'toolchains/msc510','T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;','MASM-baseline',calls);obj=base/'UNIT.OBJ'
  if recipe['placement_order']:
   placed,layout=placement.compose(asm,(base/'UNIT.LST').read_bytes(),recipe['placement_order']);q=root/'placed';q.mkdir();(q/'UNIT.ASM').write_bytes(placed);_process(q,M/'toolchains/msc510','T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;','MASM-placed',calls);obj=q/'UNIT.OBJ';proof['placement']=layout
  if recipe['placement_order']:
   before=read_omf((base/'UNIT.OBJ').read_bytes());after=read_omf(obj.read_bytes())
   def segments(o):
    result={}
    for k,s in o.segments.items():
     buf=bytearray(s.length);seen=set()
     assert not s.unsupported_data
     for offset,data in s.chunks:
      positions=set(range(offset,offset+len(data)));assert not seen.intersection(positions);assert 0<=offset<=offset+len(data)<=s.length;seen.update(positions);buf[offset:offset+len(data)]=data
     result[k]=(s.name,s.class_name,s.attributes,s.length,bytes(buf),sorted(seen))
    return result
   fixups=lambda o:sorted((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in o.fixups)
   assert segments(before)==segments(after)
   assert before.publics==after.publics and before.externals==after.externals
   assert fixups(before)==fixups(after)
   proof['placement_whole_segments_publics_externals_fixups_equal']=True
  digest=H(obj.read_bytes())
 assert not guard.events['blocked'];receipt={'status':'FRESH_STAGED_COMPOUND_SOURCE_GENERATION_NOT_ADMISSION','slot':slot,'object_path':str(obj),'object_sha256':digest,'source_pins':pins,'tools':{str(k):v for k,v in allowed.items()if k not in [Path(x['path'])for x in pins]},'calls':calls,'proof':proof,'guard':guard.events,'canonical_credit_added':0};(root/'generation.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
if __name__=='__main__':
 result=run(int(sys.argv[1]),sys.argv[2],sys.argv[3]);print(json.dumps({k:result[k]for k in ['status','slot','object_path','object_sha256']}))
