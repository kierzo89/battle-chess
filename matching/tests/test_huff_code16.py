import copy,dataclasses,json,sys,tempfile,unittest,shutil
from unittest.mock import patch
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R))
import huff_code16 as h
from omf import read_omf,Public,Segment
from reference import build_reference

class HuffBackendTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  registry=json.loads((R/'config/units.json').read_text());selected=[u for u in registry if u.get('object_profile')=='huffman_core'];cls.units=sorted(selected,key=lambda u:int(u['image_offset'],0)) if len(selected)==9 else json.loads((R/'evidence/huffman-core-omf-unit-fixture.json').read_text());cls.built=h.assemble(R/h.SOURCE,cls.units[0]);cls.obj=read_omf(cls.built.object_bytes);cls.ref=build_reference((R.parent/'CHESS.EXE').read_bytes());cls.image=cls.ref['image']
 def bad_obj(self,edit,message):
  obj=copy.deepcopy(self.obj);edit(obj)
  with self.assertRaisesRegex(ValueError,message):h.extract_code(obj)
 def bad_unit(self,edit,message):
  u=copy.deepcopy(self.units[0]);edit(u)
  with self.assertRaisesRegex(ValueError,message):h.validate_unit(u)
 def test_fresh_whole_segment(self):
  raw,m=h.extract_code(self.obj);self.assertEqual(len(raw),944);self.assertEqual(len(m['fixups']),77);self.assertEqual(len(m['public_extents']),9)
 def test_all_nine_native_bodies(self):
  body=bytearray()
  for u in self.units:
   selected,p=h.validate_comparison(u,self.built,self.image,R,self.ref['relocations']);self.assertEqual(len(selected),u['size']);self.assertTrue(p['whole_bytes_equal']);self.assertEqual(p['matching_credit_added'],0);body.extend(selected)
  self.assertEqual(body,self.image[h.BASE:h.BASE+944])
 def test_no_target_access_during_generation(self):
  source=(R/h.SOURCE).resolve();nasm=Path(shutil.which('nasm')).resolve();real=Path.read_bytes;reads=[]
  def guarded(path):
   path=path.resolve();reads.append(str(path))
   # Only source+NASM are input reads. A fresh private UNIT.OBJ is the
   # assembler output, necessarily consumed after the external process.
   generated=(path.name=='UNIT.OBJ'and path.parent.name.startswith('huff-omf-')and not path.is_relative_to(R))
   if path not in(source,nasm)and not generated:raise AssertionError('forbidden generation read: '+str(path))
   return real(path)
  with patch.object(Path,'read_bytes',guarded):
   with self.assertRaisesRegex(AssertionError,'forbidden generation read'):(R.parent/'CHESS.EXE').read_bytes()
   reads.clear();b=h.assemble(source,self.units[0])
  self.assertEqual(b.code,self.built.code);self.assertIn(str(source),reads);self.assertIn(str(nasm),reads)
  self.assertEqual(len([p for p in reads if Path(p).name=='UNIT.OBJ']),1)
 def evidence_negative(self,edit,relative=None,message='native'):
  relative=relative or h.UNITS[self.units[0]['id']][1]
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp)
   for path in[h.RAW_EVIDENCE]+[p for _,p in h.UNITS.values()]:
    dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((R/path).read_bytes())
   record=json.loads((root/relative).read_text());edit(record);(root/relative).write_text(json.dumps(record))
   with self.assertRaisesRegex(ValueError,message):h.validate_comparison(self.units[0],self.built,self.image,root,self.ref['relocations'])
 def test_wrong_native_format(self):self.evidence_negative(lambda e:e['subject'].update(format='elf'))
 def test_wrong_native_architecture(self):self.evidence_negative(lambda e:e['subject'].update(architecture='x86_64'))
 def test_wrong_native_provider(self):self.evidence_negative(lambda e:e['provider'].update(id='ida'))
 def test_wrong_native_loader(self):self.evidence_negative(lambda e:e['analysis_profile']['parameters'].update(loader='ELF'))
 def test_wrong_native_load_segment(self):self.evidence_negative(lambda e:e['analysis_profile']['parameters'].update(load_segment='0x2000'))
 def test_wrong_native_language(self):self.evidence_negative(lambda e:e['analysis_profile']['parameters'].update(language_id='x86:LE:32:default'))
 def test_wrong_native_coordinates(self):self.evidence_negative(lambda e:e['analysis_profile']['parameters'].update(address_coordinates='segmented'))
 def test_wrong_native_operation(self):self.evidence_negative(lambda e:e.update(operation='read_bytes'),message='boundary')
 def test_wrong_native_parameters(self):self.evidence_negative(lambda e:e.update(parameters={'procedure':'0x1e03b'}),message='boundary')
 def test_extra_native_parameters(self):self.evidence_negative(lambda e:e['parameters'].update(size=61),message='boundary')
 def test_duplicate_native_ids(self):
  paths=[p for _,p in h.UNITS.values()];first=json.loads((R/paths[0]).read_text())['evidence_id']
  self.evidence_negative(lambda e:e.update(evidence_id=first),paths[1],message='Duplicate')
 def test_duplicate_raw_native_id(self):
  first=json.loads((R/h.UNITS[self.units[0]['id']][1]).read_text())['evidence_id']
  self.evidence_negative(lambda e:e.update(evidence_id=first),h.RAW_EVIDENCE,message='Duplicate')
 def test_crop_unit(self):self.bad_unit(lambda u:u.update(size=60),'crop/resize')
 def test_foreign_unit(self):self.bad_unit(lambda u:u.update(id='fake'),'Unknown')
 def test_wrong_public(self):self.bad_unit(lambda u:u.update(symbol='_huff_frame_decode'),'identity')
 def test_wrong_binding(self):self.bad_unit(lambda u:u['externals'].update(_huff_code_table=0x30ce),'binding')
 def test_wrong_source_pin(self):self.bad_unit(lambda u:u.update(source_sha256='0'*64),'pins')
 def test_wrong_tool_pin(self):self.bad_unit(lambda u:u.update(assembler_sha256='0'*64),'pins')
 def test_foreign_ownership(self):self.bad_unit(lambda u:u.update(owned_data={}),'ownership')
 def test_extra_segment(self):self.bad_obj(lambda o:o.segments.update({2:Segment(2,0,0,0,0,0x48)}),'exactly one')
 def test_wrong_segment_length(self):self.bad_obj(lambda o:setattr(o.segments[1],'length',945),'CODE944')
 def test_wrong_alignment(self):self.bad_obj(lambda o:setattr(o.segments[1],'attributes',0x28),'CODE944')
 def test_foreign_public(self):self.bad_obj(lambda o:o.publics.update({'_fake':Public('_fake',1,944,0,0)}),'PUBLIC')
 def test_alias_public(self):self.bad_obj(lambda o:o.publics.update({'_alias':Public('_alias',1,0,0,0)}),'PUBLIC')
 def test_shift_public(self):self.bad_obj(lambda o:o.publics.update({'_huff_frame_decode':Public('_huff_frame_decode',1,350,0,0)}),'PUBLIC')
 def test_extra_external(self):self.bad_obj(lambda o:o.externals.update({15:'_fake'}),'external')
 def test_wrong_external_name(self):self.bad_obj(lambda o:o.externals.update({3:'_fake'}),'external')
 def test_hole(self):self.bad_obj(lambda o:o.segments[1].chunks.__setitem__(0,(1,o.segments[1].chunks[0][1])),'hole/overlap')
 def test_omitted_tail(self):
  def edit(o):a,b=o.segments[1].chunks[-1];o.segments[1].chunks[-1]=(a,b[:-1])
  self.bad_obj(edit,'omitted CODE tail')
 def test_instruction_change(self):
  def edit(o):a,b=o.segments[1].chunks[0];o.segments[1].chunks[0]=(a,bytes([b[0]^1])+b[1:])
  self.bad_obj(edit,'instruction/addend')
 def test_missing_fixup(self):self.bad_obj(lambda o:o.fixups.pop(),'77-field')
 def test_wrong_fixup_frame(self):self.bad_obj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],frame=(0,1))),'frame/type')
 def test_wrong_fixup_target(self):self.bad_obj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],target=(2,2))),'77-field')
 def test_fixup_abs_code(self):self.bad_obj(lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],segment_relative=not o.fixups[0].segment_relative)),'77-field')
 def test_comm_record(self):self.bad_obj(lambda o:o.records.insert(1,(0xb0,0,b'')),'Foreign allocation')
 def test_lidata(self):self.bad_obj(lambda o:o.records.insert(1,(0xa2,0,b'')),'Foreign allocation')
 def test_entry_point(self):
  def edit(o):o.records[-1]=(0x8a,o.records[-1][1],b'\x40')
  self.bad_obj(edit,'entry point')
 def test_native_whole_mismatch_rejects_even_other_unit(self):
  image=bytearray(self.image);image[h.BASE+943]^=1
  with self.assertRaisesRegex(ValueError,'Whole CODE944'):h.validate_comparison(self.units[0],self.built,image,R,self.ref['relocations'])
 def test_original_mz_crossing_start_rejected(self):
  with self.assertRaisesRegex(ValueError,'MZ word'):h.validate_comparison(self.units[0],self.built,self.image,R,[h.BASE-1])
 def test_cropped_metadata_rejected(self):
  m=copy.deepcopy(self.built.metadata);m['public_extents'][0]['size']-=1
  with self.assertRaisesRegex(ValueError,'cropped'):h.public_extent(m,self.units[0]['symbol'])
 def test_source_modified_rejected(self):
  with tempfile.TemporaryDirectory()as d:
   path=Path(d)/'changed.asm';path.write_bytes((R/h.SOURCE).read_bytes()+b';changed\n')
   with self.assertRaisesRegex(ValueError,'Source pin'):h.assemble(path,self.units[0])

if __name__=='__main__':unittest.main(verbosity=2)
