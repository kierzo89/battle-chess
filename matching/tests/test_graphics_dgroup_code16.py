"""Saved genuine old/new controls; never invokes an assembler, compiler or LINK.
Positive fixture provenance is fixture-pins.json in the reviewed preparation.
Parsed-object mutations below are rejection-only models, never serialized OMF.
"""
from pathlib import Path
from dataclasses import replace,asdict
import ast,copy,hashlib,json,os,re,sys,unittest
from unittest.mock import patch
M=Path(os.environ.get('GRAPHICS_DGROUP_TEST_PROJECT',Path(__file__).resolve().parents[1])).resolve()
sys.path.insert(0,str(M))
import graphics_dgroup_code16 as g
import graphics1488_dgroup_link16 as a
import graphics_code16 as oldg
import graphics1488_link16 as olda
import check
from omf import read_omf
from library16 import LibraryError
F=Path(__file__).resolve().parent/'fixtures/graphics_dgroup1488'
CHANGED={1247,1372,1377,1380,1447}
def digest(b):return hashlib.sha256(b).hexdigest()
class GraphicsDGROUP1488Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.new=(F/'new.obj').read_bytes();cls.old=(F/'old.obj').read_bytes()
  cls.native=(F/'native.bin').read_bytes();cls.units=json.loads((F/'units.json').read_text())
  cls.newunit=cls.units['new_unit'];cls.oldunit=cls.units['old_unit']
  cls.audit=json.loads((F/'frame-audit.json').read_text())
 def test_new_saved_raw_strict_positive(self):
  obj,code=a.validate_object(self.new);self.assertEqual(len(code),1488);self.assertEqual(len(obj.fixups),84)
  self.assertEqual(digest(self.new),'1801092250398ee23181943911cfdff5d50dbd2135e4da520c87b23650e9feb3')
 def test_old_saved_raw_own_version_positive(self):
  obj,code=olda.validate_object(self.old);raw,_=oldg.extract_code(obj)
  self.assertEqual(raw,code);self.assertEqual(len(obj.fixups),84)
 def test_old_identical_CODE_rejected_by_new_adapter(self):
  self.assertEqual(olda.validate_object(self.old)[1],a.validate_object(self.new)[1])
  with self.assertRaises(LibraryError):a.validate_object(self.old)
 def test_new_rejected_by_old_adapter(self):
  with self.assertRaises(LibraryError):olda.validate_object(self.new)
 def test_new_backend_complete_allocation(self):
  raw,meta=g.extract_code(read_omf(self.new));self.assertEqual(len(raw),1488)
  self.assertEqual(meta['actual_fixup_count'],84);self.assertEqual(meta['DATA_byte_credit'],0)
 def test_exact_five_raw_frames_only(self):
  o,n=read_omf(self.old),read_omf(self.new);self.assertEqual(len(o.fixups),len(n.fixups))
  changed=[]
  for x,y in zip(o.fixups,n.fixups):
   dx,dy=asdict(x),asdict(y)
   if dx!=dy:
    changed.append(x.offset);self.assertEqual(x.frame,(0,1));self.assertEqual(y.frame,(1,1))
    for k in dx:
     if k not in ('frame','raw'):self.assertEqual(dx[k],dy[k])
    diffs=[i for i,(p,q)in enumerate(zip(x.raw,y.raw))if p!=q]
    self.assertEqual(len(diffs),1);i=diffs[0];self.assertEqual(x.raw[i]^y.raw[i],0x10)
  self.assertEqual(set(changed),CHANGED);self.assertEqual(len(changed),5)
 def test_only_fixupp_record_payload_changed(self):
  old,new=read_omf(self.old),read_omf(self.new)
  changed=[(x,y)for x,y in zip(old.records,new.records)if x!=y]
  self.assertEqual(len(changed),1);self.assertEqual(changed[0][0][0],0x9c)
  self.assertEqual(len(self.old),len(self.new))
  self.assertEqual([i for i,(x,y)in enumerate(zip(self.old,self.new))if x!=y],[2284,2294,2299,2304,2309,2341])
 def test_each_new_DS_frame_reversion_rejected(self):
  for offset in sorted(CHANGED):
   with self.subTest(offset=offset):
    o=read_omf(self.new);i=next(i for i,f in enumerate(o.fixups)if f.offset==offset)
    o.fixups[i]=replace(o.fixups[i],frame=(0,1))
    with self.assertRaisesRegex(g.GraphicsCodeError,'Exact84'):g.extract_code(o)
 def test_each_new_DS_frame_foreign_group_rejected(self):
  for offset in sorted(CHANGED):
   with self.subTest(offset=offset):
    o=read_omf(self.new);i=next(i for i,f in enumerate(o.fixups)if f.offset==offset)
    o.fixups[i]=replace(o.fixups[i],frame=(1,2))
    with self.assertRaisesRegex(g.GraphicsCodeError,'Exact84'):g.extract_code(o)
 def test_all_unchanged_trueFAR_and_CS_contracts(self):
  old,new=read_omf(self.old),read_omf(self.new)
  same=[(x,y)for x,y in zip(old.fixups,new.fixups)if x.offset not in CHANGED]
  self.assertEqual(len(same),79)
  self.assertTrue(all(x==y for x,y in same))
  self.assertEqual(sum(x.target==(0,2)for x,y in same),59)
  self.assertEqual(sum(x.location_type in (2,3)for x,y in same),4)
 def test_each_trueFAR_or_CS_wrong_frame_rejected(self):
  indices=[i for i,f in enumerate(read_omf(self.new).fixups)if f.target==(0,2)or f.location_type in (2,3)]
  self.assertEqual(len(indices),63)
  for i in indices:
   with self.subTest(index=i):
    o=read_omf(self.new);o.fixups[i]=replace(o.fixups[i],frame=(1,1))
    with self.assertRaisesRegex(g.GraphicsCodeError,'Exact84'):g.extract_code(o)
 def test_genuine_wrong_colour_semantic_negative(self):
  wrong=(F/'wrong-colour.obj').read_bytes()
  with self.assertRaises(g.GraphicsCodeError):g.extract_code(read_omf(wrong))
  with self.assertRaises(oldg.GraphicsCodeError):oldg.extract_code(read_omf(wrong))
  with self.assertRaises(LibraryError):a.validate_object(wrong)
 def test_semantic_CODE_change_with_valid_84_frames_rejected(self):
  o=read_omf(self.new);seg=o.segments[2];changed=False
  for i,(start,content)in enumerate(seg.chunks):
   if start<=873<start+len(content):
    b=bytearray(content);b[873-start]^=1;seg.chunks[i]=(start,bytes(b));changed=True
  self.assertTrue(changed)
  with self.assertRaisesRegex(g.GraphicsCodeError,'instructions/addends'):g.extract_code(o)
 def test_source_inverse_exact_and_five_qualifiers(self):
  source=(M/g.SOURCE).read_bytes();old=(F/'old.asm').read_bytes()
  self.assertEqual(source.count(b'OFFSET DGROUP:_text_colour_words'),2)
  self.assertEqual(source.count(b'OFFSET DGROUP:_text_glyph_pixels'),2)
  self.assertEqual(source.count(b'OFFSET DGROUP:_font_glyphs'),1)
  inverse=source
  for name in (b'text_colour_words',b'text_glyph_pixels',b'font_glyphs'):
   inverse=inverse.replace(b'OFFSET DGROUP:_'+name,b'OFFSET _'+name)
  self.assertEqual(inverse,old);self.assertEqual(digest(source),g.SOURCE_SHA256)
 def test_whole_native_all84_fourMZ_four_bases(self):
  externals={k:(v['segment'],v['offset'])for k,v in g.BINDINGS.items()}
  self.assertEqual(len(self.native),1488)
  for load in (0,1,0x1000,0xffff):
   with self.subTest(load=load):
    linked,logs=a.link(self.new,{1:((0x5cc2+load)&65535,0),2:(load,g.BASE)},{1:(0x5cc2+load)&65535},{k:((p+load)&65535,o)for k,(p,o)in externals.items()})
    expected=bytearray(self.native)
    for site in g.MZ_SITES:
     at=site-g.BASE;expected[at:at+2]=((int.from_bytes(expected[at:at+2],'little')+load)&65535).to_bytes(2,'little')
    self.assertEqual(linked,bytes(expected));self.assertEqual(len(logs),84)
    self.assertEqual(sorted(f['mz_relocation_image_offset']-load*16 for f in logs if f['mz_relocation_image_offset']is not None),g.MZ_SITES)
 def test_complete_retained_native_evidence_closure(self):
  native,ids=g._evidence(M);self.assertEqual(native,self.native);self.assertEqual(len(set(ids)),7)
 def test_real_four_resolved_LINK_words_show_64_not66(self):
  exe=(F/'old-partial.EXE').read_bytes();header=int.from_bytes(exe[8:10],'little')*16
  mapping=(F/'old-partial.MAP').read_text(errors='replace')
  audit=self.audit['actual_current240_MAP'];self.assertEqual(audit['DATA_byte_start_difference'],66)
  self.assertEqual(audit['DATA_frame_paragraph']*16-audit['DGROUP_paragraph']*16,64)
  rows=[r for r in self.audit['actual_five_near_immediate_fields']if r['resolved']]
  self.assertEqual(len(rows),4)
  for r in rows:
   at=header+r['actual_partial_image_site'];word=int.from_bytes(exe[at:at+2],'little')
   self.assertEqual(word,r['actual_linked_WORD'])
   p,o=r['actual_MAP_public'];name=r['symbol']
   self.assertRegex(mapping,rf'(?i){p:04x}:{o:04x}\s+(?:Abs\s+)?{re.escape(name)}\b')
   target=p*16+o;self.assertEqual((target-word)//16,audit['DATA_frame_paragraph'])
   self.assertEqual(target-audit['DGROUP_linear']-word,64)
 def test_unresolved_old_font_word_not_native_proof(self):
  rows=[r for r in self.audit['actual_five_near_immediate_fields']if not r['resolved']]
  self.assertEqual(len(rows),1);self.assertEqual(rows[0]['symbol'],'_font_glyphs')
  self.assertIsNone(rows[0]['actual_MAP_public'])
 def test_near_external_wrong_frame_binding_rejected(self):
  ex={k:(v['segment'],v['offset'])for k,v in g.BINDINGS.items()};ex['_font_glyphs']=(0x5cc3,0x4524)
  with self.assertRaises(LibraryError):a.link(self.new,{1:(0x5cc2,0),2:(0,g.BASE)},{1:0x5cc2},ex)
 def test_exact_new_unit_and_old_version_still_valid(self):
  g.validate_unit(self.newunit);oldg.validate_unit(self.oldunit)
  with self.assertRaises(g.GraphicsCodeError):g.validate_unit(self.oldunit)
  with self.assertRaises(oldg.GraphicsCodeError):oldg.validate_unit(self.newunit)
 def test_unit_foreign_function_credit_rejected(self):
  u=copy.deepcopy(self.newunit);u['authored_c_function_credit']=1
  with self.assertRaises(g.GraphicsCodeError):g.validate_unit(u)
 def test_checker_accepts_versioned_new_unit(self):
  check.validate_units([self.newunit],0x100000,0x100000)
 def test_checker_routes_new_evidence_without_generation(self):
  with patch.object(g,'validate_evidence',return_value='new-marker')as p,patch.object(oldg,'validate_evidence',side_effect=AssertionError('old route')):
   self.assertEqual(check.validate_rea_extent(self.newunit,M,g.ORIGINAL_SHA256,{}),'new-marker');p.assert_called_once()
 def test_checker_retains_old_evidence_route(self):
  with patch.object(oldg,'validate_evidence',return_value='old-marker')as p,patch.object(g,'validate_evidence',side_effect=AssertionError('new route')):
   self.assertEqual(check.validate_rea_extent(self.oldunit,M,g.ORIGINAL_SHA256,{}),'old-marker');p.assert_called_once()
 def test_checker_assembler_route_is_source_project_not_legacy(self):
  tree=ast.parse((M/'check.py').read_text());build=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_unit')
  choices=[n for n in ast.walk(build)if isinstance(n,ast.IfExp)and isinstance(n.body,ast.Call)and isinstance(n.body.func,ast.Attribute)and n.body.func.attr=='assemble']
  source_route=next(n for n in choices if ast.unparse(n.body)=='backend.assemble(source, project)')
  self.assertIn('graphics_dgroup_code16',ast.unparse(source_route.test))
  self.assertIn('graphics_code16',ast.unparse(source_route.test))
 def test_publics_extents_and_no_credit_added(self):
  old,new=self.oldunit,self.newunit
  for key in ('id','language','image_offset','size','externals','public_symbols','assembler_sha256','rea_evidence'):self.assertEqual(old[key],new[key])
  self.assertEqual(new['size'],1488);self.assertNotEqual(old['backend'],new['backend'])
if __name__=='__main__':unittest.main()
