"""Focused exact version separation and whole genuine OMF/native controls."""
from pathlib import Path
import ast,copy,dataclasses,hashlib,json,sys,tempfile,unittest
M=Path(__file__).resolve().parents[1];D=M/'build/future-turn-phase454-owned-coherent-stage';I=M;sys.dont_write_bytecode=True;sys.path[:0]=[str(I)]
import owned_editor_turn_phase_literal_const16 as new
import owned_editor_state_literal_const16 as old
import owned_literal_const16 as dispatch
from omf import OMFError,Public,read_omf
from reference import build_reference
class TurnPhaseOwnerControls(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.units=json.loads((D/'units.prospective.json').read_text());c.owners=[u for u in c.units if u.get('owned_const_profile')==new.PROFILE];c.u=c.owners[0]
  c.raw=(M/'build/turn-phase-57cc-ownership/editor_state_flow_match.obj').read_bytes();c.obj=read_omf(c.raw);c.oldraw=(M/'build/editor-state-literal264-context/positive-final.obj').read_bytes();c.oldobj=read_omf(c.oldraw);c.oldowners=[u for u in old._profile()['units']if u.get('owned_const_profile')==old.PROFILE];c.ref=build_reference((M.parent/'CHESS.EXE').read_bytes())
 def full(self,u=None,obj=None,ref=None,project=M):
  u=copy.deepcopy(u or self.u);u['source']='build/turn-phase-57cc-ownership/editor_state_flow_match.c';return dispatch.validate(u,obj or self.obj,project,ref or self.ref)
 def test_two_new_owners_complete_native_and_four_bases(self):
  before=copy.deepcopy(self.obj)
  for u in self.owners:
   d,p,r=self.full(u);self.assertEqual(len(p),264);self.assertEqual((r['whole_CODE_size'],r['whole_CODE_CV_bytes'],r['whole_CODE_fields'],r['raw_OMF_fixup_count']),(1554,1553,174,237));self.assertEqual(r['four_forward_load_bases'],[0,1,4096,65535]);self.assertEqual(r['whole_CODE_MZ_sites'],[]);self.assertEqual(r['source_data_credit'],0);self.assertEqual(r['uncredited_source_CODE_tail']['bytes_hex'],'90')
  self.assertEqual(before,self.obj)
 def test_old_profile_and_legacy_dispatch_unchanged_positive(self):
  for u in self.oldowners:self.assertEqual(len(dispatch.validate_layout(u,self.oldobj)[1]),264)
 def test_old_new_cross_objects_rejected_both_directions(self):
  with self.assertRaises(OMFError):new.validate_layout(self.u,self.oldobj)
  with self.assertRaises(OMFError):old.validate_layout(self.oldowners[0],self.obj)
 def test_wrong_old_new_profile_metadata_rejected(self):
  for profile in [old.PROFILE,'editor_state_messages_turn_phase_1554_v2',None]:
   u=copy.deepcopy(self.u);u['owned_const_profile']=profile
   with self.subTest(profile=profile),self.assertRaises(OMFError):dispatch.validate_layout(u,self.obj)
 def test_wrong_old_external_name_rejected(self):
  u=copy.deepcopy(self.u);u['externals']['_state']=u['externals'].pop('_state_57cc')
  with self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_external_binding_missing_extra_drift_rejected(self):
  for mode in ['missing','extra','drift']:
   u=copy.deepcopy(self.u)
   if mode=='missing':u['externals'].pop('_state_57cc')
   elif mode=='extra':u['externals']['_alias']=0x57cc
   else:u['externals']['_state_57cc']+=1
   with self.subTest(mode=mode),self.assertRaises(OMFError):dispatch.validate_unit_metadata(u)
 def test_wrong_id_owner_flags_descriptor_rejected(self):
  for changes in [{'id':'wrong'},{'symbol':'_reset_state'},{'size':1},{'flags':['/AS','/Zi']},{'owned_const':dict(self.u['owned_const'],size=263)},{'extended_extent':{}}]:
   with self.subTest(changes=changes),self.assertRaises(OMFError):dispatch.validate_unit_metadata(dict(self.u,**changes))
 def test_source_identity_mismatch_rejected(self):
  with tempfile.TemporaryDirectory(prefix='turnphase-owner-negative-')as t:
   p=Path(t)/'build/turn-phase-57cc-ownership/editor_state_flow_match.c';p.parent.mkdir(parents=True);p.write_bytes((M/'build/editor-state-literal264-context/editor_state_literals.c').read_bytes())
   with self.assertRaises(OMFError):self.full(project=Path(t))
 def test_new_profile_checksum_pin_rejected(self):
  # Physical profile copy, distinct module namespace; no monkeypatch/global gate mutation.
  import importlib.util
  with tempfile.TemporaryDirectory(prefix='turnphase-profile-negative-')as t:
   p=Path(t);(p/'gate.py').write_bytes((I/'owned_editor_turn_phase_literal_const16.py').read_bytes());raw=(I/'editor_turn_phase_literal_const_profile.json').read_bytes();(p/'editor_turn_phase_literal_const_profile.json').write_bytes(raw+b' ')
   spec=importlib.util.spec_from_file_location('isolated_wrong_turnphase_gate',p/'gate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
   with self.assertRaises(OMFError):g.validate_unit_metadata(self.u)
 def test_all237_parsed_fields_rejected_on_drift(self):
  for i,f in enumerate(self.obj.fixups):
   o=copy.deepcopy(self.obj);o.fixups[i]=dataclasses.replace(f,offset=f.offset+1)
   with self.subTest(i=i),self.assertRaises(OMFError):new.validate_layout(self.u,o)
 def test_all264_literal_bytes_rejected_on_drift(self):
  for i in range(264):
   o=copy.deepcopy(self.obj);at,b=o.segments[3].chunks[0];b=bytearray(b);b[i]^=1;o.segments[3].chunks[0]=(at,bytes(b))
   with self.subTest(i=i),self.assertRaises(OMFError):new.validate_layout(self.u,o)
 def test_debug_segment_extent_and_record_rejected(self):
  for mode in ['oldlength','record','debugbyte','CV','tail','extraDATA','extraCONSTpublic']:
   o=copy.deepcopy(self.obj)
   if mode=='oldlength':o.segments[5].length=1238
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
  for mode in ['MZ','tail']:
   r=copy.deepcopy(self.ref)
   if mode=='MZ':r['relocations']=tuple(r['relocations'])+(0x8e38,)
   else:b=bytearray(r['image']);b[0x9447]^=1;r['image']=bytes(b)
   with self.subTest(mode=mode),self.assertRaises(OMFError):self.full(ref=r)
 def test_only_two_profile_transitions_and_unchanged_old_inputs(self):
  a=json.loads((M/'build/future-turn-phase454-isolated-execution-closed/units.prospective.json').read_text());changed=[(u['id'],[k for k in u if u.get(k)!=v.get(k)])for u,v in zip(self.units,a)if u!=v];self.assertEqual(sorted(changed),[('no_move_900a',['owned_const_profile']),('validate_editor_8e36',['owned_const_profile'])])
  for n,h in json.loads((D/'base-pins.json').read_text()).items():
   if n in ['owned_editor_state_literal_const16.py','editor_state_literal_const_profile.json','tests/test_owned_editor_state_literal_const16.py']:self.assertEqual(hashlib.sha256((M/n).read_bytes()).hexdigest(),h)
if __name__=='__main__':unittest.main(verbosity=2)
