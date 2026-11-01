"""Focused immutable-object and inert-negative controls; no compiler/LINK runs."""
from pathlib import Path
import copy,dataclasses,json,os,sys,unittest
D=Path(__file__).resolve().parent;M=next(p for p in D.parents if(p/'config/msc500.json').is_file());I=Path(os.environ.get('BC_PIXEL_CALLBACK_IMPLEMENTATION',D.parent/'implementation'));sys.dont_write_bytecode=True;sys.path[:0]=[str(I),str(M)]
import pixel_callback_data16 as h
from omf import read_omf
from types import SimpleNamespace
F=D/'fixtures/pixel_callbacks';RAW=(F/'pixel_callbacks.obj').read_bytes();SOURCE=(F/'pixel_callbacks.c').read_bytes();U=json.loads((F/'unit.json').read_text());G=json.loads((F/'generation.json').read_text())['pixel_callbacks']['compiler']
class PixelCallbackDataControls(unittest.TestCase):
 def obj(self):return read_omf(RAW)
 def reject(self,change):
  o=self.obj();change(o)
  with self.assertRaises(h.PixelCallbackError):h.validate_shape(o)
 def fix(self,**kw):return lambda o:o.fixups.__setitem__(0,dataclasses.replace(o.fixups[0],**kw))
 def test_actual_whole6_three_CODE_fields(self):
  b,p=h.link_code_callbacks(RAW,h.CODE);self.assertEqual(b.hex(),'7c5a7c5a64ea');self.assertEqual(len(b),6);self.assertEqual(len(p['relocations']),3);self.assertEqual(p['emitted_mz_sites'],[])
 def test_target_frame_is_CODE_zero_not_DGROUP(self):
  b,p=h.link_code_callbacks(RAW,h.CODE);self.assertTrue(all(f['target_paragraph']==f['frame_paragraph']==0 for f in p['relocations']));self.assertEqual(p['DATA_DGROUP'],{'paragraph':0x5cc2,'offset':0x4a6})
 def test_DS_bindings_rejected(self):
  with self.assertRaises(h.PixelCallbackError):h.link_code_callbacks(RAW,{n:[0x5cc2,v[1]]for n,v in h.CODE.items()})
 def test_missing_CODE_binding(self):
  with self.assertRaises(h.PixelCallbackError):h.link_code_callbacks(RAW,{'_plot_region_5a7c':[0,0x5a7c]})
 def test_extra_CODE_binding(self):
  with self.assertRaises(h.PixelCallbackError):h.link_code_callbacks(RAW,h.CODE|{'extra':[0,0]})
 def test_changed_CODE_offset(self):
  with self.assertRaises(h.PixelCallbackError):h.link_code_callbacks(RAW,h.CODE|{'_plot_region_5a7c':[0,0x5a7d]})
 def test_boolean_CODE_frame_forbidden(self):
  with self.assertRaises(h.PixelCallbackError):h.link_code_callbacks(RAW,h.CODE|{'_plot_region_5a7c':[False,0x5a7c]})
 def test_far_pointer_field_forbidden(self):self.reject(self.fix(width=4,location_type=3))
 def test_DS_group_frame_forbidden(self):self.reject(self.fix(frame=(1,1)))
 def test_SELFREL_field_forbidden(self):self.reject(self.fix(segment_relative=False))
 def test_BASE_field_forbidden(self):self.reject(self.fix(location_type=2))
 def test_marker_target_forbidden(self):self.reject(self.fix(target=(2,1)))
 def test_displacement_forbidden(self):self.reject(self.fix(displacement=2))
 def test_duplicate_field_forbidden(self):self.reject(lambda o:o.fixups.append(o.fixups[0]))
 def test_missing_field_forbidden(self):self.reject(lambda o:o.fixups.pop())
 def test_DATA_hole_forbidden(self):self.reject(lambda o:setattr(o.segments[2],'chunks',[(0,bytes(2)),(4,bytes(2))]))
 def test_DATA_nonzero_addend_forbidden(self):self.reject(lambda o:setattr(o.segments[2],'chunks',[(0,b'\x01'+bytes(5))]))
 def test_DATA_tail_forbidden(self):self.reject(lambda o:setattr(o.segments[2],'length',8))
 def test_other_loaded_allocation_forbidden(self):self.reject(lambda o:setattr(o.segments[3],'length',2))
 def test_alias_PUBLIC_forbidden(self):self.reject(lambda o:o.publics.__setitem__('alias',dataclasses.replace(o.publics['_plot_pixel'],name='alias')))
 def test_array_PUBLIC_offset2_required(self):self.reject(lambda o:o.publics.__setitem__('_pixel_writers',dataclasses.replace(o.publics['_pixel_writers'],offset=0)))
 def test_lidata_forbidden(self):self.reject(lambda o:setattr(o.segments[2],'unsupported_data',True))
 def test_startup_marker_remains_unused(self):self.assertEqual(self.obj().externals[1],'__acrtused');self.assertNotIn(1,[f.target[1]for f in self.obj().fixups])
 def test_checksum_rejected(self):
  with self.assertRaises(ValueError):h.validate_raw(RAW[:-1]+bytes([RAW[-1]^1]))
 def test_wrong_flags_provenance_before_link(self):
  c=SimpleNamespace(**{k:v for k,v in G.items()if k not in['compiler_log','command']},object_bytes=RAW);c.flags=['/AS','/Zi']
  with self.assertRaises(h.PixelCallbackError):h.validate_compiled(c,SOURCE,U)
 def test_pointer_source_uses_function_names_not_numeric_casts(self):
  self.assertEqual(h.sha(SOURCE),h.SOURCE_SHA);self.assertIn(b'pixel_writers[]',SOURCE);self.assertIn(b'= {plot_region_5a7c,bios_plot_pixel_ea64}',SOURCE);self.assertNotIn(b'0x',SOURCE)
 def test_generic_DS_module_not_a_new_route(self):
  from cdata_pointer import link_pointer_data,CDataPointerError
  # DS parser's existing contract remains as-is; this proposal explicitly never
  # routes CODE pairs through it. Pair values are not valid unsigned DS words.
  with self.assertRaises(CDataPointerError):link_pointer_data(self.obj(),'_plot_pixel',h.ORIGIN,h.DS,h.CODE)
 def test_wrong_unit_extent(self):
  u=copy.deepcopy(U);u['size']=8
  with self.assertRaises(h.PixelCallbackError):h.validate_unit(u)
if __name__=='__main__':unittest.main()
