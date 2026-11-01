from pathlib import Path
import sys,json,copy,dataclasses,unittest
from unittest.mock import patch
M=Path(__file__).resolve().parents[1];D=M/'build/pen-selector-560-support';P=M;sys.path.insert(0,str(P))
import pen_selector_const16 as pen
import owned_selector_const16 as dispatch
import owned_context_mz
from omf import read_omf
from reference import build_reference
class PenSelector560Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.report=json.loads((D/'fresh-output-final/report.json').read_text());c.row=next(r for r in c.report['units']if r['symbol']=='_select_pen_5b18');c.raw=Path(c.row['object_artifact']).read_bytes();c.unit=json.loads((D/'proposed-new-unit.json').read_text());c.reference=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def obj(self):return read_omf(self.raw)
 def layout(self,o=None,d=None,e=None):return pen.validate_layout(self.obj()if o is None else o,self.unit['owned_selector_const']if d is None else d,self.unit['externals']if e is None else e)
 def bad(self,fn):
  o=self.obj();fn(o)
  with self.assertRaises(ValueError):self.layout(o)
 def test_complete560_and_fiveCVs_and65rawfields(self):
  o=self.obj();self.assertEqual(self.layout(o),0x4d94);self.assertEqual(len(o.fixups),65);self.assertEqual(set(o.procedures),set(pen.PROCEDURES))
 def test_actual_minimal_normal_pass_and_separate_ownedMZ(self):
  s=self.report['summary'];self.assertEqual((s['c_matched_functions'],s['c_matched_bytes']),(5,560));self.assertEqual(s['owned_context_emitted_mz_sites'],[0x619b4]);self.assertEqual(s['source_emitted_mz_relocations'],0)
 def test_actual_full_native_comparison_and_fourbases(self):
  d,b,p=dispatch.validate(self.unit,self.obj(),P,self.reference);self.assertEqual(b,b'\r\x11');self.assertEqual(p['complete_CODE_bytes'],560);self.assertEqual(p['complete_MZ_sites'],[0x619b4]);self.assertEqual(len(p['complete_CODE_fields']),43)
  for base in [0,1,0x1000,0xffff]:self.assertEqual(((int.from_bytes(b,'little')+base)&65535),((0x110d+base)&65535))
 def test_semantic_wrongmask_shape_passes_then_native_rejects(self):
  o=read_omf((D/'actual-negative.obj').read_bytes());self.layout(o)
  with self.assertRaisesRegex(ValueError,'raw-byte comparison mismatch'):dispatch.validate(self.unit,o,P,self.reference)
 def test_wrong_descriptor_kind_and_extra_key(self):
  for change in [{'kind':'book_far_array_selector_800_v1'},{'fake':1}]:
   d=dict(self.unit['owned_selector_const'],**change)
   with self.assertRaises(ValueError):self.layout(d=d)
 def test_wrong_unit_flags_extent_or_symbol(self):
  for change in [{'flags':['/AS','/Gs','/Zi']},{'size':38},{'symbol':'_move_pen_5b3d'},{'image_offset':'0x5b19'},{'extended_extent':{}},{'owned_const':{}}]:
   with self.assertRaises(ValueError):pen.validate_unit_metadata(dict(self.unit,**change))
 def test_wrong_native_placement_and_selector_size(self):
  for change in [{'image_offset':'0x619b6'},{'size':4},{'group':2},{'segment':2},{'target_symbol':'_pen_state'},{'data_address':{'segment':0x5cc2,'offset':0x4d96}}]:
   with self.assertRaises(ValueError):self.layout(d=dict(self.unit['owned_selector_const'],**change))
 def test_wrong_external_values_and_bool_or_float(self):
  for value in [{'segment':0x110e,'offset':0},{'segment':0x110d,'offset':1},{'segment':0x110d,'offset':False},{'segment':0x110d,'offset':0.0}]:
   e=copy.deepcopy(self.unit['externals']);e['_graphics_copy']=value
   with self.assertRaises(ValueError):self.layout(e=e)
 def test_missing_extra_or_wrong_absolute_external(self):
  for change in ['missing','extra','absolute']:
   e=copy.deepcopy(self.unit['externals'])
   if change=='missing':e.pop('_packed_pen')
   elif change=='extra':e['_fake']=0
   else:e['__AHSHIFT']={'absolute':11}
   with self.assertRaises(ValueError):self.layout(e=e)
 def test_truncated_checksum_rawOMF_rejected(self):
  for raw in [self.raw[:-1],self.raw[:10]+bytes([self.raw[10]^1])+self.raw[11:]]:
   with self.assertRaises(ValueError):read_omf(raw)
 def test_extra_or_missing_PUBLIC_and_alias(self):
  self.bad(lambda o:o.publics.update(_alias=next(iter(o.publics.values()))));self.bad(lambda o:o.publics.pop('_copy_5cb5'))
 def test_PUBLICgroup_one_rejected(self):
  self.bad(lambda o:o.publics.__setitem__('_select_pen_5b18',dataclasses.replace(o.publics['_select_pen_5b18'],group=1)))
 def test_extra_hidden_CV_rejected(self):self.bad(lambda o:o.procedures.update(_hidden=copy.deepcopy(o.procedures['_copy_5cb5'])))
 def test_wrong_CV_extent_rejected(self):self.bad(lambda o:o.procedures['_select_pen_5b18'].update(length=38))
 def test_CODE_tail_hole_overlap_and_reserved_rejected(self):
  self.bad(lambda o:setattr(o.segments[1],'length',562));self.bad(lambda o:o.segments[1].chunks.pop());self.bad(lambda o:o.segments[1].chunks.append(o.segments[1].chunks[0]));self.bad(lambda o:setattr(o.segments[1],'unsupported_data',True))
 def test_extra_loaded_allocation_and_foreign_segment_rejected(self):
  self.bad(lambda o:setattr(o.segments[2],'length',2));self.bad(lambda o:o.segments.__setitem__(7,copy.deepcopy(o.segments[2])))
 def test_CONST_nonzero_and_missing_field_rejected(self):
  self.bad(lambda o:setattr(o.segments[3],'chunks',[(0,b'\1\0')]));self.bad(lambda o:setattr(o,'fixups',[f for f in o.fixups if f.segment!=3]))
 def test_selector_field_frame_target_width_addend_rejected(self):
  for change in [{'frame':(1,1)},{'location_type':1},{'width':4},{'segment_relative':False},{'displacement':1}]:
   def mutate(o):
    i=next(i for i,f in enumerate(o.fixups)if f.segment==3);o.fixups[i]=dataclasses.replace(o.fixups[i],**change)
   self.bad(mutate)
 def test_owner_CODEfield_missing_or_frame_changed(self):
  self.bad(lambda o:setattr(o,'fixups',[f for f in o.fixups if not(f.segment==1 and f.offset==10)]))
  def mutate(o):
   i=next(i for i,f in enumerate(o.fixups)if f.segment==1 and f.offset==10);o.fixups[i]=dataclasses.replace(o.fixups[i],frame=(5,None))
  self.bad(mutate)
 def test_debug_patch_offset_and_byte_tamper_rejected(self):
  def offset(o):at,data=o.segments[5].chunks[0];o.segments[5].chunks[0]=(at+1,data)
  def body(o):at,data=o.segments[5].chunks[0];o.segments[5].chunks[0]=(at,bytes([data[0]^1])+data[1:])
  self.bad(offset);self.bad(body)
 def test_unknown_COMDAT_or_hidden_record_rejected(self):
  self.bad(lambda o:o.records.append((0xc2,0,b'\0')))
 def test_profile_hash_cannot_grant_changed_layout(self):
  original=Path.read_bytes
  def tamper(p,*a,**k):
   data=original(p,*a,**k);return data+b' 'if p.name=='pen_selector_profile.json'else data
  with patch.object(Path,'read_bytes',tamper),self.assertRaisesRegex(ValueError,'structuralprofile'):self.layout()
 def test_relative_primary_escape_rejected(self):
  u=copy.deepcopy(self.unit);u['owned_selector_const']['code_evidence']='../CHESS.EXE'
  with self.assertRaises(ValueError):dispatch.validate(u,self.obj(),P,self.reference)
 def test_changed_native_image_rejected(self):
  r=dict(self.reference);r['image']=r['image'][:0x5b28]+bytes([r['image'][0x5b28]^1])+r['image'][0x5b29:]
  with self.assertRaises(ValueError):dispatch.validate(self.unit,self.obj(),P,r)
 def test_owned_MZ_reauthenticates_actual_source_object_proof(self):
  p=owned_context_mz.collect_owned_context_mz(self.report['units'],P,self.reference,self.reference['relocations']);self.assertEqual(p['sites'],[0x619b4])
  for change in [{'source_sha256':'0'*64},{'object_sha256':'0'*64}]:
   row=copy.deepcopy(self.row);row.update(change)
   with self.assertRaises(ValueError):owned_context_mz.collect_owned_context_mz([row],P,self.reference,self.reference['relocations'])
 def test_forged_proof_and_duplicate_owner_rejected(self):
  row=copy.deepcopy(self.row);row['owned_selector_const_proof']['complete_CODE_bytes']=558
  with self.assertRaises(ValueError):owned_context_mz.collect_owned_context_mz([row],P,self.reference,self.reference['relocations'])
  with self.assertRaises(ValueError):owned_context_mz.collect_owned_context_mz([self.row,self.row],P,self.reference,self.reference['relocations'])
 def test_no_decoder_original_reads_or_generation(self):
  original=Path.read_bytes
  def guarded(p,*a,**k):
   if p.name!='pen_selector_profile.json':raise AssertionError('decoder unexpectedread')
   return original(p,*a,**k)
  with patch.object(Path,'read_bytes',guarded):self.assertEqual(self.layout(),0x4d94)
if __name__=='__main__':unittest.main()
