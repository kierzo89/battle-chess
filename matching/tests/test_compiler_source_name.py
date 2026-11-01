from pathlib import Path
import sys,json,unittest,importlib.util,hashlib,tempfile,dataclasses
from unittest.mock import patch
M=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(M))
from msc import compile_c
from omf import read_omf
from reference import build_reference
import check
assert Path(check.__file__).resolve()==M/'check.py'
# All generated objects/results stay outside immutable proof fixtures.
_test_outputs=tempfile.TemporaryDirectory(prefix='battlechess-source-name-tests-')
D=Path(_test_outputs.name)
class SourceNameTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.units=json.loads((M/'build/display-source-frame-372/proposed-named-AM-units.json').read_text())
  for u in cls.units:u.pop('compiler_source_name')
  cls.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
  cls.source=M/cls.units[0]['source'];cls.sha=hashlib.sha256(cls.source.read_bytes()).hexdigest()
 def named(self):return dict(self.units[0],compiler_source_name='DISPLAY.C')
 def test_valid_medium_name(self):
  u=self.named();self.assertEqual(check.compiler_input_name(u),'DISPLAY.C');check.validate_units([u],401131,401131)
 def test_default_preserves_legacy_name(self):self.assertEqual(check.compiler_input_name(self.units[0]),'UNIT.C')
 def test_inert_name_validation(self):
  for name in [None,4,'display.c','DISPLAY.C\nexit','../X.C','C:X.C','A B.C','A".C','A;X.C','TOOLONG99.C','CON.C','PRN.C','AUX.C','NUL.C','COM1.C','LPT9.C','1.C','X.H']:
   with self.subTest(name=name),self.assertRaisesRegex(ValueError,'DOS source name'):check.validate_units([dict(self.named(),compiler_source_name=name)],401131,401131)
 def test_name_cannot_apply_to_unproved_backend_or_model(self):
  for edit in [dict(language='asm'),dict(language='c-data'),dict(backend='msc510-omf'),dict(flags=['/AS','/Gs','/Zi'])]:
   with self.subTest(edit=edit),self.assertRaisesRegex(ValueError,'medium-model C unit'):check.compiler_input_name(dict(self.named(),**edit))
 def test_invalid_name_rejected_before_compiler(self):
  with patch.object(check,'compile_c')as c:r=check.build_unit(dict(self.named(),compiler_source_name='NUL.C'),self.reference['image'],M,'nasm',reference=self.reference)
  self.assertEqual(r['status'],'build_error');self.assertIn('DOS source name',r['error']);c.assert_not_called()
 def test_fresh_names_separate_real_segments_cache_and_artifacts(self):
  original=Path.read_bytes;targets={(M.parent/'CHESS.EXE').resolve(),(M/'build/exepack/TRIM5_UNPACK.EXE').resolve()}
  def read(p,*a,**kw):
   if p.resolve()in targets:raise AssertionError('Target read during generation')
   return original(p,*a,**kw)
  cache={}
  with patch.object(Path,'read_bytes',read),patch.object(check,'compile_c',wraps=compile_c)as compiler:
   out=D/'production';a=check.build_unit(self.units[0],self.reference['image'],M,'nasm',c_cache=cache,output=out,reference=self.reference)
   b=check.build_unit(self.named(),self.reference['image'],M,'nasm',c_cache=cache,output=out,reference=self.reference)
   c=check.build_unit(dict(self.units[1],compiler_source_name='DISPLAY.C'),self.reference['image'],M,'nasm',c_cache=cache,output=out,reference=self.reference)
   d=check.build_unit(dict(self.units[2],compiler_source_name='DISPLAY.C'),self.reference['image'],M,'nasm',c_cache=cache,output=out,reference=self.reference)
   self.assertEqual([a['status'],b['status'],c['status'],d['status']],['c_matched']*4,(a,b,c,d));self.assertEqual(compiler.call_count,2);self.assertEqual(len(cache),2)
   self.assertNotEqual(a['object_artifact'],b['object_artifact']);self.assertEqual(b['object_artifact'],c['object_artifact']);self.assertEqual(c['object_artifact'],d['object_artifact'])
   self.assertNotEqual(a['object_sha256'],b['object_sha256'])
   self.assertEqual(read_omf(Path(a['object_artifact']).read_bytes()).segments[1].name,'UNIT_TEXT')
   self.assertEqual(read_omf(Path(b['object_artifact']).read_bytes()).segments[1].name,'DISPLAY_TEXT')
   legacy=('msc500',self.sha,('/AM','/Gs','/Zi'));self.assertEqual(cache[legacy].source_name,'UNIT.C');self.assertEqual(cache[legacy+('DISPLAY.C',)].source_name,'DISPLAY.C')
   (D/'fresh-production.json').write_text(json.dumps({'legacy':a,'named_clear':b,'named_draw':c,'named_write':d,'fresh_compiles':compiler.call_count,'cache_keys':[list(k)for k in cache]},indent=2)+'\n')
 def test_cached_wrong_basename_rejected(self):
  c=compile_c(self.source,['/AM','/Gs','/Zi'],compiler='msc500')
  cache={('msc500',self.sha,('/AM','/Gs','/Zi'),'DISPLAY.C'):c}
  with patch.object(check,'compile_c')as compiler:r=check.build_unit(self.named(),self.reference['image'],M,'nasm',c_cache=cache,reference=self.reference)
  self.assertEqual(r['status'],'build_error');self.assertIn('DOS source name differs',r['error']);compiler.assert_not_called()
 def test_canonical_checker_module(self):
  self.assertEqual(Path(check.__file__).resolve(),M/'check.py')
if __name__=='__main__':unittest.main(verbosity=2)
