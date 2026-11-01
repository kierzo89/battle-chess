"""Exact ready9856 owner version, retained versions and native full-object gates."""
from pathlib import Path
import copy,dataclasses,hashlib,importlib.util,json,sys,tempfile,unittest
M=Path(__file__).resolve().parents[1];D=M/'build/ready9856-owned-profile-stage';sys.dont_write_bytecode=True;sys.path.insert(0,str(M))
import owned_editor_ready9856_literal_const16 as new
import owned_editor_turn_phase_literal_const16 as old
import owned_editor_state_literal_const16 as legacy
import owned_literal_const16 as dispatch
import owned_const16
from omf import OMFError,Public,read_omf
from reference import build_reference
class Ready9856OwnerControls(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.units=json.loads((D/'units.prospective.json').read_text());c.owners=[copy.deepcopy(u)for u in c.units if u.get('owned_const_profile')==new.PROFILE];[u.update(source='build/ready9856-rename-experiment/sources/src/editor_state_flow_match.c')for u in c.owners];c.u=c.owners[0];c.raw=(M/'build/ready9856-rename-experiment/fresh-2.obj').read_bytes();c.obj=read_omf(c.raw)
  c.oldraw=(M/'build/turn-phase-57cc-ownership/editor_state_flow_match.obj').read_bytes();c.oldobj=read_omf(c.oldraw);c.oldowners=[u for u in old._profile()['units']if u.get('owned_const_profile')==old.PROFILE];c.legacyraw=(M/'build/editor-state-literal264-context/positive-final.obj').read_bytes();c.legacyobj=read_omf(c.legacyraw);c.legacyowners=[u for u in legacy._profile()['units']if u.get('owned_const_profile')==legacy.PROFILE];c.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def full(self,u=None,obj=None,ref=None,project=M):return owned_const16.validate(copy.deepcopy(u or self.u),obj or self.obj,project,ref or self.ref)
 def test_two_new_owners_complete_native_and_four_bases(self):
  before=copy.deepcopy(self.obj)
  for u in self.owners:
   desc,pool,r=self.full(u);self.assertEqual(len(pool),264);self.assertEqual((r['whole_CODE_size'],r['whole_CODE_CV_bytes'],r['whole_CODE_fields'],r['raw_OMF_fixup_count']),(1554,1553,174,237));self.assertEqual(r['four_forward_load_bases'],[0,1,4096,65535]);self.assertEqual(r['whole_CODE_MZ_sites'],[]);self.assertEqual(r['source_data_credit'],0);self.assertEqual(r['uncredited_source_CODE_tail']['bytes_hex'],'90');self.assertEqual(self.obj.segments[5].length,1248)
  self.assertEqual(before,self.obj)
 def test_old_two_versions_positive_unchanged(self):
  for gate,owners,obj in[(old,self.oldowners,self.oldobj),(legacy,self.legacyowners,self.legacyobj)]:
   for u in owners:self.assertEqual(len(dispatch.validate_layout(u,obj)[1]),264)
 def test_three_versions_cross_objects_rejected(self):
  for gate,unit,wrong in[(new,self.u,self.oldobj),(new,self.u,self.legacyobj),(old,self.oldowners[0],self.obj),(legacy,self.legacyowners[0],self.obj)]:
   with self.subTest(gate=gate.PROFILE),self.assertRaises(OMFError):gate.validate_layout(unit,wrong)
 def test_wrong_old_new_profile_metadata_rejected(self):
  for profile in[old.PROFILE,legacy.PROFILE,'editor_state_messages_ready9856_1554_v2',None]:
   with self.subTest(profile=profile),self.assertRaises(OMFError):dispatch.validate_layout(dict(self.u,owned_const_profile=profile),self.obj)
 def test_old_ready_or_input_name_rejected(self):
  for name in['_ready','_input']:
   u=copy.deepcopy(self.u);u['externals'][name]=u['externals'].pop('_ready_9856')
   with self.subTest(name=name),self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_external_binding_missing_extra_drift_rejected(self):
  for mode in['missing','extra','drift']:
   u=copy.deepcopy(self.u)
   if mode=='missing':u['externals'].pop('_ready_9856')
   elif mode=='extra':u['externals']['_alias']=0x9856
   else:u['externals']['_ready_9856']+=1
   with self.subTest(mode=mode),self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_wrong_id_owner_flags_descriptor_rejected(self):
  for changes in[{'id':'wrong'},{'symbol':'_reset_state'},{'size':1},{'flags':['/AS','/Zi']},{'owned_const':dict(self.u['owned_const'],size=263)},{'extended_extent':{}}]:
   with self.subTest(changes=changes),self.assertRaises(OMFError):dispatch.validate_unit_metadata(dict(self.u,**changes))
 def test_source_identity_mismatch_rejected(self):
  with tempfile.TemporaryDirectory(prefix='ready-owner-source-negative-')as t:
   p=Path(t)/self.u['source'];p.parent.mkdir(parents=True);p.write_bytes((M/'build/turn-phase-57cc-ownership/editor_state_flow_match.c').read_bytes())
   with self.assertRaises(OMFError):self.full(project=Path(t))
 def test_new_profile_checksum_pin_rejected(self):
  with tempfile.TemporaryDirectory(prefix='ready-owner-profile-negative-')as t:
   p=Path(t);(p/'gate.py').write_bytes((M/'owned_editor_ready9856_literal_const16.py').read_bytes());raw=(M/'editor_ready9856_literal_const_profile.json').read_bytes();(p/'editor_ready9856_literal_const_profile.json').write_bytes(raw+b' ');spec=importlib.util.spec_from_file_location('isolated_wrong_ready9856_gate',p/'gate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
   with self.assertRaises(OMFError):g.validate_unit_metadata(self.u)
 def test_all237_parsed_fields_rejected_on_drift(self):
  for i,f in enumerate(self.obj.fixups):
   o=copy.deepcopy(self.obj);o.fixups[i]=dataclasses.replace(f,offset=f.offset+1)
   with self.subTest(i=i),self.assertRaises(OMFError):new.validate_layout(self.u,o)
 def test_all264_literal_bytes_rejected_on_drift(self):
  for i in range(264):
   o=copy.deepcopy(self.obj);at,b=o.segments[3].chunks[0];b=bytearray(b);b[i]^=1;o.segments[3].chunks[0]=(at,bytes(b))
   with self.subTest(i=i),self.assertRaises(OMFError):new.validate_layout(self.u,o)
 def test_debug_extent_record_CV_tail_and_foreign_allocation_reject(self):
  for mode in['oldlength','record','debugbyte','CV','tail','extraDATA','extraCONSTpublic']:
   o=copy.deepcopy(self.obj)
   if mode=='oldlength':o.segments[5].length=1243
   elif mode=='record':o.records.pop()
   elif mode=='debugbyte':at,b=o.segments[5].chunks[0];o.segments[5].chunks[0]=(at,bytes([b[0]^1])+b[1:])
   elif mode=='CV':o.procedures.clear()
   elif mode=='tail':o.segments[1].chunks[-1]=(1553,b'\x91')
   elif mode=='extraDATA':o.segments[2].length=1
   else:o.publics['_alias']=Public('_alias',3,0,1,0)
   with self.subTest(mode=mode),self.assertRaises(OMFError):new.validate_layout(self.u,o)
 def test_raw_object_checksum_rejected(self):
  b=bytearray(self.raw);b[-1]^=1
  with self.assertRaises(OMFError):read_omf(bytes(b))
 def test_native_extra_MZ_and_tail_rejected(self):
  for mode in['MZ','tail']:
   r=copy.deepcopy(self.ref)
   if mode=='MZ':r['relocations']=tuple(r['relocations'])+(0x8e38,)
   else:b=bytearray(r['image']);b[0x9447]^=1;r['image']=bytes(b)
   with self.subTest(mode=mode),self.assertRaises(OMFError):self.full(ref=r)
 def test_exact39_metadata_reconciliations_and_two_owner_versions(self):
  before=json.loads((D/'baseline23-units.json').read_text());changed=[(a,b)for a,b in zip(before,self.units)if a!=b];self.assertEqual(len(changed),39);owners=[]
  for a,b in changed:
   keys={k for k in set(a)|set(b)if a.get(k)!=b.get(k)};self.assertTrue(keys<={'externals','owned_const_profile'});self.assertEqual(a['id'],b['id']);self.assertEqual(b['externals'].get('_ready_9856'),0x9856);self.assertNotIn('_ready',b['externals']);self.assertNotIn('_input',b['externals'])
   if'owned_const_profile'in keys:owners.append(a['id'])
  self.assertEqual(sorted(owners),['no_move_900a','validate_editor_8e36']);self.assertEqual(len(before),454)
 def test_old_modules_profiles_and_fixture_files_immutable(self):
  for n,h in json.loads((D/'old-gate-fixture-pins.json').read_text()).items():
   if n=='owned_literal_const16.py':continue
   self.assertEqual(hashlib.sha256((M/n).read_bytes()).hexdigest(),h)
if __name__=='__main__':unittest.main(verbosity=2)
