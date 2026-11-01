"""Focused controls for the authored ASM route; no assembler/compiler/LINK calls."""
from pathlib import Path
import sys,json,copy,dataclasses,unittest,tempfile,inspect,builtins,io,os
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];sys.path.insert(0,str(M))
import turn_task_code16 as b
import check
from omf import read_omf
from reference import build_reference
F=Path(__file__).parent/'fixtures/turn_task640'
class TurnTaskTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=(F/'actual.obj').read_bytes();cls.unit=json.loads((F/'unit.json').read_text());cls.obj=read_omf(cls.raw);cls.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def reject(self,fn,*args):
  with self.assertRaises((ValueError,KeyError)):fn(*args)
 def model_negative(self,edit):
  obj=copy.deepcopy(self.obj);edit(obj);self.reject(b.validate_object,obj)
 def test_adopted_route_modules(self):self.assertEqual(Path(b.__file__).resolve(),M/'turn_task_code16.py');self.assertEqual(Path(check.__file__).resolve(),M/'check.py')
 def test_closed_unit(self):b.validate_unit(self.unit);u=copy.deepcopy(self.unit);u['size']=639;self.reject(b.validate_unit,u)
 def test_C_or_unknown_profile_rejected(self):
  for key,value in [('language','c'),('object_profile','generic640'),('backend','masm510-code-contribution-omf')]:
   u=copy.deepcopy(self.unit);u[key]=value;self.reject(b.validate_unit,u)
 def test_no_capacity_or_credit_metadata(self):u=copy.deepcopy(self.unit);u['C_credit']=1;self.reject(b.validate_unit,u)
 def test_exact_whole_object(self):
  code,meta=b.extract_code(self.raw);self.assertEqual(len(code),640);self.assertEqual((meta['actual_external_fields'],meta['actual_internal_fields']),(18,6));self.assertEqual(meta['native_MZ'],[]);self.assertEqual(meta['C_credit'],0);self.assertEqual(code[632:634],bytes.fromhex('eb00'));self.assertEqual(code[634:],bytes.fromhex('5e5f8be55dc3'))
 def test_checksum_corruption(self):raw=bytearray(self.raw);raw[-1]^=1;self.reject(b.extract_code,bytes(raw))
 def test_no_extra_raw_record(self):self.model_negative(lambda o:o.records.append((0xb0,999,b'\0')))
 def test_no_loaded_DATA(self):self.model_negative(lambda o:setattr(o.segments[1],'length',2))
 def test_no_CODE_tail_or_crop(self):
  for size in [639,641]:self.model_negative(lambda o:setattr(o.segments[2],'length',size))
 def test_no_CODE_hole_or_overlap(self):
  for at in [1,-1]:self.model_negative(lambda o:setattr(o.segments[2],'chunks',[(at,o.segments[2].chunks[0][1])]))
 def test_WORD_alignment_required(self):self.model_negative(lambda o:setattr(o.segments[2],'attributes',0x28))
 def test_no_public_alias_or_entry_shift(self):
  self.model_negative(lambda o:o.publics.__setitem__('_alias',dataclasses.replace(o.publics['_turn_task_730c'],name='_alias')))
  self.model_negative(lambda o:o.publics.__setitem__('_turn_task_730c',dataclasses.replace(o.publics['_turn_task_730c'],offset=1)))
 def test_exact_ext_identity(self):self.model_negative(lambda o:o.externals.__setitem__(1,'_different'))
 def test_all_actual_fields_required(self):self.model_negative(lambda o:o.fixups.pop())
 def test_no_duplicate_or_overlapping_field(self):self.model_negative(lambda o:o.fixups.append(o.fixups[0]))
 def test_DATA_frame_not_CODE_or_emptyDATA(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if f.segment_relative);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(0,1))
  self.model_negative(edit)
 def test_external_nearCALL_frame_exact(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if f.target[0]==2 and not f.segment_relative);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(5,None))
  self.model_negative(edit)
 def test_local_jump_not_external_stub(self):
  def edit(o):i=next(i for i,f in enumerate(o.fixups)if f.target==(0,2));o.fixups[i]=dataclasses.replace(o.fixups[i],displacement=180)
  self.model_negative(edit)
 def test_raw_write_provenance_preserved(self):self.model_negative(lambda o:o.data_writes.pop())
 def test_no_opcode_directives_or_source_changes(self):
  src=(M/b.SOURCE).read_bytes();b.source_policy(src)
  for suffix in [b'\nDB 0\n',b'\nINCLUDE x\n',b'\n; changed\n']:self.reject(b.source_policy,src+suffix)
 def test_generation_interface_is_target_free(self):self.assertEqual(list(inspect.signature(b._assemble_source).parameters),['source','project'])
 def test_source_only_guard_denies_native_oldOBJ_and_proof(self):
  with tempfile.TemporaryDirectory()as folder:
   scratch=Path(folder)/'fresh';scratch.mkdir()
   with b.generation_guard(M/b.SOURCE,M,scratch)as events:
    for p in [M.parent/'CHESS.EXE',M/'tests/fixtures/turn_task640/actual.obj',M/b.RAW_EVIDENCE]:self.reject(Path.read_bytes,p)
    self.assertEqual((M/b.SOURCE).read_bytes(),(M/b.SOURCE).read_bytes())
    self.reject(io.open,0,'rb')
   self.assertEqual(len(events['blocked']),3)
 def test_full_native_evidence_and_boundary_MZ(self):
  self.assertEqual(b.validate_evidence(self.unit,M,b.ORIGINAL_SHA256,self.ref),json.loads((M/b.RAW_EVIDENCE).read_text())['evidence_id'])
  for site in [b.BASE-1,b.BASE,b.BASE+639]:self.reject(b._sites,[site])
 def test_full_640_all_fields_fourbases_not_trimmed(self):
  code,meta=b.extract_code(self.raw);built=b.Build(self.raw,code,meta,{})
  linked,proof=b.validate_comparison(self.unit,built,self.ref['image'],M,self.ref['relocations']);self.assertEqual(len(linked),640);self.assertEqual(len(proof['relocations']),24);self.assertEqual(len(proof['four_load_bases']),4);self.assertEqual(proof['authored_c_function_credit'],0)
  wrong=bytearray(self.ref['image']);wrong[b.BASE+4]^=1;self.reject(b.validate_comparison,self.unit,built,bytes(wrong),M,self.ref['relocations'])
 def test_checker_routes_fixture_only_without_generation(self):
  code,meta=b.extract_code(self.raw);built=b.Build(self.raw,code,meta,{'test_fixture_only':True})
  with patch.object(b,'assemble',return_value=built)as fake:
   result=check.build_unit(self.unit,self.ref['image'],M,'nasm',reference=self.ref)
  self.assertEqual(fake.call_count,1);self.assertEqual(result['status'],'asm_code_matched');self.assertEqual(result['authored_c_function_credit'],0)
 def test_each_actual_field_has_exact_typed_contract(self):
  for index in range(24):
   with self.subTest(field=index):
    def edit(o):o.fixups[index]=dataclasses.replace(o.fixups[index],width=4)
    self.model_negative(edit)
 def test_DS_nonzero_symbolic_addends_are_not_zeroed(self):
  code,_=b.extract_code(self.raw);fields=[f for f in self.obj.fixups if f.segment_relative]
  self.assertEqual(len(fields),7)
  self.assertEqual([int.from_bytes(code[f.offset:f.offset+2],'little')for f in fields],[0]*7)
  self.assertEqual(sorted((int.from_bytes(code[f.offset:f.offset+2],'little')+(f.displacement or 0))&65535 for f in fields),[0,0,16,65524,65524,65524,65524])
 def test_wrong_evidence_is_rejected(self):
  from turn_task640_profile import EVIDENCE_PINS
  path=M/next(iter(EVIDENCE_PINS));original=Path.read_bytes
  def read(p):return b'{}' if p==path else original(p)
  with patch.object(Path,'read_bytes',read):self.reject(b._evidence,M)
 def test_no_standalone_C_or_ASM_function_credit(self):
  _,meta=b.extract_code(self.raw);self.assertEqual(meta['C_credit'],0);self.assertEqual(meta['authored_asm_function_credit'],0)
if __name__=='__main__':unittest.main()
