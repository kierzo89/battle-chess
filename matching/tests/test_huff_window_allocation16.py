import copy,dataclasses,importlib.util,json,shutil,sys,unittest
from pathlib import Path
from unittest.mock import patch
D=Path(__file__).resolve().parent;M=D.parent;sys.path[:0]=[str(M),str(D)]
import huff_window_allocation16 as h
import huff_allocation16 as old
from omf import read_omf,Public,Segment
from reference import build_reference

class WindowTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  rows=json.loads((M/'config/units.json').read_text());selected=[u for u in rows if u.get('object_profile')=='huff_source_window_120'];cls.unit=selected[0]if selected else json.loads((D/'huff-source-window-120-unit.json').read_text());cls.built=h.assemble(M/h.SOURCE,cls.unit);cls.obj=read_omf(cls.built.object_bytes);cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def bad_obj(self,edit,message):
  o=copy.deepcopy(self.obj);edit(o)
  with self.assertRaisesRegex(ValueError,message):h.extract_code(o)
 def bad_unit(self,edit,message):
  u=copy.deepcopy(self.unit);edit(u)
  with self.assertRaisesRegex(ValueError,message):h.validate_unit(u)
 def bad_primary(self,path,edit,message):
  real=Path.read_text;j=json.loads((M/path).read_text());edit(j)
  def read(p,*a,**kw):return json.dumps(j)if p.resolve()==(M/path).resolve()else real(p,*a,**kw)
  with patch.object(Path,'read_text',read):
   with self.assertRaisesRegex(ValueError,message):h._native(M)
 def test_fresh_whole120(self):
  raw,m=h.extract_code(self.obj);self.assertEqual(len(raw),120);self.assertEqual(len(self.obj.fixups),14);self.assertEqual({n:p.offset for n,p in self.obj.publics.items()},h.PUBLICS)
 def test_full_comparison_two_link_orders(self):
  b,p=h.validate_comparison(self.unit,self.built,self.ref['image'],M,self.ref['relocations']);self.assertEqual(len(b),120);self.assertEqual(p['whole_original_mz_sites'],[0xe42a]);self.assertEqual(len(p['authentic_two_order_LINK']),2);self.assertEqual(len(p['four_load_bases']),4);self.assertEqual(p['authored_c_function_credit'],0);self.assertFalse(p['function_partition_claim'])
 def test_guarded_generation(self):
  source=(M/h.SOURCE).resolve();tool=Path(shutil.which('nasm')).resolve();real=Path.read_bytes;reads=[]
  def read(p):
   q=p.resolve();reads.append(q);scratch=q.name=='UNIT.OBJ'and q.parent.name.startswith('huff-window-allocation-')and not q.is_relative_to(M)
   if q not in(source,tool)and not scratch:raise AssertionError('forbidden generation input')
   return real(p)
  with patch.object(Path,'read_bytes',read):
   with self.assertRaises(AssertionError):(M.parent/'CHESS.EXE').read_bytes()
   reads.clear();h.assemble(source,self.unit)
  self.assertIn(source,reads);self.assertIn(tool,reads)
 def test_crop95_rejected(self):self.bad_unit(lambda u:u.update(size=95),'Whole120')
 def test_crop25_rejected(self):self.bad_unit(lambda u:u.update(size=25),'Whole120')
 def test_function_model_rejected(self):self.bad_unit(lambda u:u.update(symbol='_begin_asset_decode'),'function/ownership')
 def test_foreign_profile_rejected(self):self.bad_unit(lambda u:u.update(object_profile='anything'),'Closed')
 def test_old_profile_not_silently_replaced(self):
  u=json.loads((D/'huff-refill-trap-95-fixture.json').read_text());b=old.assemble(M/old.SOURCE,u);self.assertEqual(len(b.code),95)
  with self.assertRaises(ValueError):h.validate_unit(u)
 def test_wrong_source_pin(self):self.bad_unit(lambda u:u.update(source_sha256='0'*64),'Pinned')
 def test_wrong_tool_pin(self):self.bad_unit(lambda u:u.update(assembler_sha256='0'*64),'Pinned')
 def test_data_binding_changed(self):self.bad_unit(lambda u:u['externals']['_huff_memory_cursor'].update(offset=0x44dc),'bindings')
 def test_extra_segment(self):self.bad_obj(lambda o:o.segments.update({2:Segment(2,0,0,0,0,0x48)}),'one CODE')
 def test_wrong_size(self):self.bad_obj(lambda o:setattr(o.segments[1],'length',119),'CODE120')
 def test_wrong_alignment(self):self.bad_obj(lambda o:setattr(o.segments[1],'attributes',0x28),'CODE120')
 def test_omitted_public(self):self.bad_obj(lambda o:o.publics.pop('_end_asset_decode'),'PUBLIC')
 def test_false_public_location(self):self.bad_obj(lambda o:o.publics.update({'_begin_asset_decode':Public('_begin_asset_decode',1,96,0,0)}),'PUBLIC')
 def test_extra_public(self):self.bad_obj(lambda o:o.publics.update({'_fake':Public('_fake',1,39,0,0)}),'PUBLIC')
 def test_extra_external(self):self.bad_obj(lambda o:o.externals.update({5:'_fake'}),'external')
 def test_code_hole(self):self.bad_obj(lambda o:o.segments[1].chunks.__setitem__(0,(1,o.segments[1].chunks[0][1])),'Hole')
 def test_missing_tail(self):
  def edit(o):a,b=o.segments[1].chunks[-1];o.segments[1].chunks[-1]=(a,b[:-1])
  self.bad_obj(edit,'tail')
 def test_mutate_each_raw_byte(self):
  for i in range(120):
   with self.subTest(i=i):
    def edit(o):
     a,b=o.segments[1].chunks[0];v=bytearray(b);v[i]^=1;o.segments[1].chunks[0]=(a,bytes(v))
    self.bad_obj(edit,'Instruction')
 def test_mutate_each_field(self):
  for i in range(14):
   with self.subTest(i=i):self.bad_obj(lambda o:o.fixups.__setitem__(i,dataclasses.replace(o.fixups[i],segment_relative=not o.fixups[i].segment_relative)),'Exact14')
 def test_missing_fixup(self):self.bad_obj(lambda o:o.fixups.pop(),'Exact14')
 def test_wrong_wrapper_target(self):self.bad_obj(lambda o:o.fixups.__setitem__(10,dataclasses.replace(o.fixups[10],target=(2,1))),'Exact14')
 def test_wrong_base_frame(self):self.bad_obj(lambda o:o.fixups.__setitem__(5,dataclasses.replace(o.fixups[5],frame=(1,1))),'Exact14')
 def test_COMM_record(self):self.bad_obj(lambda o:o.records.insert(1,(0xb0,0,b'')),'Foreign record')
 def test_wrong_native_provider(self):self.bad_primary(h.WRAPPERS['begin'][0],lambda e:e['provider'].update(id='ida'),'profile')
 def test_wrong_native_parameters(self):self.bad_primary(h.WRAPPERS['end'][0],lambda e:e.update(parameters={'procedure':'0x1e45d'}),'parameters')
 def test_wrong_native_extent(self):self.bad_primary(h.WRAPPERS['begin'][0],lambda e:e['normalized_result']['procedure']['body'].update(total_bytes=18),'extent')
 def test_wrong_wrapper_instruction(self):self.bad_primary(h.WRAPPERS['begin'][0],lambda e:e['normalized_result']['assembly'].__setitem__(0,'0x1e449: RET'),'instructions')
 def test_wrong_wrapper_CFG(self):self.bad_primary(h.WRAPPERS['end'][0],lambda e:e['normalized_result']['basic_blocks'][0].update(successors=['0x1e462']),'CFG')
 def test_duplicate_primary_ID(self):
  other=json.loads((M/h.WRAPPERS['end'][0]).read_text())['evidence_id']
  self.bad_primary(h.WRAPPERS['begin'][0],lambda e:e.update(evidence_id=other),'Duplicate')
 def test_wrong_raw120(self):self.bad_primary(h.RAW_EVIDENCE,lambda e:e['normalized_result'].update(returned_bytes=119),'raw120')
 def test_wrong_original_byte(self):
  im=bytearray(self.ref['image']);im[h.BASE+119]^=1
  with self.assertRaisesRegex(ValueError,'Complete120'):h.validate_comparison(self.unit,self.built,im,M,self.ref['relocations'])
 def test_missing_MZ(self):
  with self.assertRaisesRegex(ValueError,'MZ set'):h.validate_comparison(self.unit,self.built,self.ref['image'],M,[])
 def test_crossing_MZ(self):
  with self.assertRaisesRegex(ValueError,'MZ set'):h.validate_comparison(self.unit,self.built,self.ref['image'],M,[h.BASE-1,h.BASE+64])
 def test_changed_LINK_proof(self):
  real=Path.read_bytes
  def read(p):return b'{}'if p.resolve()==(M/h.LINK_PROOF).resolve()else real(p)
  with patch.object(Path,'read_bytes',read):
   with self.assertRaisesRegex(ValueError,'LINK proof pin'):h._authenticate_links(M,self.obj)

if __name__=='__main__':unittest.main()
