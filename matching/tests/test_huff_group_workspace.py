"""Saved genuine controls; parsed mutations are negative-only, no generators."""
from pathlib import Path
from dataclasses import replace
import copy,json,os,sys,unittest
from unittest.mock import patch
M=Path(os.environ.get('HUFF_CODE_DATA_TEST_PROJECT',Path(__file__).resolve().parents[1])).resolve();sys.path.insert(0,str(M))
import huff_workspace_omf16 as a
import huff_dgroup_code16 as c
import huff_workspace_data16 as d
import huff_code16 as old
import check
from omf import read_omf
from library16 import link_segment,LibraryError
from link16 import link_function,LinkError
from reference import build_reference
F=Path(__file__).resolve().parent/'fixtures/huff_group_data'
class HuffGroupWorkspaceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.new=(F/'code91.obj').read_bytes();cls.old=(F/'code-old.obj').read_bytes();cls.data=(F/'data0e.obj').read_bytes();cls.p=a.profile();cls.nativecode=(F/'code944.bin').read_bytes();cls.nativedata=(F/'data5120.bin').read_bytes()
  cls.unit=json.loads((F/'data-unit.json').read_text());cls.codeunit=json.loads((F/'code-unit.json').read_text());cls.ref=build_reference((Path(os.environ.get('HUFF_ORIGINAL_ROOT',M.parent))/'CHESS.EXE').read_bytes())
 def test_saved_new_CODE_positive(self):
  b,m=a.extract_code(self.new);self.assertEqual(len(b),944);self.assertEqual(len(m['fixups']),77)
 def test_saved_DATA_positive(self):
  b,m=a.extract_data(self.data);self.assertEqual(b,self.nativedata);self.assertEqual(m['initialized_LIDATA_bytes'],5120)
 def test_old_gate_accepts_saved_old(self):self.assertEqual(len(old.extract_code(read_omf(self.old))[0]),944)
 def test_new_gate_rejects_saved_old(self):
  with self.assertRaises(a.HuffWorkspaceError):a.extract_code(self.old)
 def test_old_gate_rejects_saved_new(self):
  with self.assertRaises(old.HuffCodeError):old.extract_code(read_omf(self.new))
 def test_generic_frame5_linker_stays_closed(self):
  with self.assertRaises(LinkError):link_function(read_omf(self.new),'_prepare_asset_decode',0xe03a,self.p['EXTERNALS'])
 def test_generic_DATA_parser_stays_closed(self):
  with self.assertRaises(LibraryError):link_segment(read_omf(self.data),1,{1:(0x5cc2,0x30cc)},{1:0x5cc2},{})
 def test_all944_native_and77fields_fourbases(self):
  for load in(0,1,4096,65535):
   with self.subTest(load=load):
    b,l=a.link_code(self.new,cs=load,ds=(0x5cc2+load)&65535);self.assertEqual(b,self.nativecode);self.assertEqual(len(l),77);self.assertEqual(sum(f['frame']==[1,1]for f in l),10)
 def test_nine_PUBLIC_andfourteen_EXTs(self):
  o=read_omf(self.new);self.assertEqual(len(o.publics),9);self.assertEqual(len(o.externals),14);self.assertEqual(set(o.segments),{1})
 def test_each_ten_group_frame_reversion_rejected(self):
  for off in[22,94,159,162,197,273,453,539,727,813]:
   with self.subTest(offset=off):
    o=read_omf(self.new);i=next(i for i,f in enumerate(o.fixups)if f.offset==off);o.fixups[i]=replace(o.fixups[i],frame=(5,None))
    with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_each_other67_new_group_frame_rejected(self):
  for i,f in enumerate(read_omf(self.new).fixups):
   if f.frame!=(5,None):continue
   with self.subTest(offset=f.offset):
    o=read_omf(self.new);o.fixups[i]=replace(o.fixups[i],frame=(1,1))
    with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_wrong_group_index_rejected(self):
  o=read_omf(self.new);i=next(i for i,f in enumerate(o.fixups)if f.frame==(1,1));o.fixups[i]=replace(o.fixups[i],frame=(1,2))
  with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_target_change_rejected(self):
  o=read_omf(self.new);o.fixups[0]=replace(o.fixups[0],target=(2,14))
  with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_CODE_semantic_byte_change_rejected(self):
  o=read_omf(self.new);at,b=o.segments[1].chunks[0];v=bytearray(b);v[0]^=1;o.segments[1].chunks[0]=(at,bytes(v))
  with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_CODE_extra_DATA_segment_rejected(self):
  o=read_omf(self.new);o.segments[2]=copy.deepcopy(o.segments[1]);o.segments[2].length=0
  with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_empty_group_membership_must_stay_empty(self):
  o=read_omf(self.new);i=next(i for i,(k,at,b)in enumerate(o.records)if k==0x9a);k,at,b=o.records[i];o.records[i]=(k,at,b+b'\xff\x01')
  with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_CODE_PUBLIC_change_rejected(self):
  o=read_omf(self.new);n=next(iter(o.publics));o.publics[n]=replace(o.publics[n],offset=1)
  with self.assertRaises(a.HuffWorkspaceError):a._code_structure(o)
 def test_DATA_preserves_PUBzero_GROUPmembership1(self):
  b,m=a.extract_data(self.data);self.assertEqual(m['actual_PUBLIC_group'],0);self.assertEqual(m['group'],{'index':1,'name':'DGROUP','members':[1]})
 def test_DATA_PUBone_normalization_rejected(self):
  o=read_omf(self.data);n=next(iter(o.publics));o.publics[n]=replace(o.publics[n],group=1)
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_alias_added_rejected(self):
  o=read_omf(self.data);o.publics['_fake']=o.publics['_huff_code_table']
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_extra_segment_rejected(self):
  o=read_omf(self.data);o.segments[2]=copy.deepcopy(o.segments[1])
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_LIDATA_wrong_repeat_rejected(self):
  o=read_omf(self.data);i=next(i for i,(k,at,b)in enumerate(o.records)if k==0xa2);k,at,b=o.records[i];v=bytearray(b);v[3:5]=(511).to_bytes(2,'little');o.records[i]=(k,at,bytes(v))
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_LIDATA_nonzero_leaf_rejected(self):
  o=read_omf(self.data);i=next(i for i,(k,at,b)in enumerate(o.records)if k==0xa2);k,at,b=o.records[i];o.records[i]=(k,at,b[:-1]+b'\x01')
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_missing_record_no_hole_fill(self):
  o=read_omf(self.data);i=next(i for i,(k,at,b)in enumerate(o.records)if k==0xa2);del o.records[i]
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_record_offset_overlap_rejected(self):
  o=read_omf(self.data);idx=[i for i,(k,at,b)in enumerate(o.records)if k==0xa2][1];k,at,b=o.records[idx];o.records[idx]=(k,at,b[:1]+bytes(2)+b[3:])
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_unwritten_reservation_never_filled(self):
  b,m=a.extract_data(self.data);self.assertEqual(m['unwritten_reservation_bytes'],0);self.assertEqual(m['raw_literal_leaf_bytes'],8);self.assertEqual(read_omf(self.data).segments[1].chunks,[])
 def test_DATA_opaque_tail_no_capacity_credit(self):
  b,m=a.extract_data(self.data);self.assertEqual(m['opaque_tail_bytes'],2048);self.assertFalse(m['historical_capacity_TU_original_storageclass_proven']);self.assertEqual(m['C_credit'],0)
 def test_DATA_unit_wrong_extent_and_credit_rejected(self):
  for k,v in[('size',1024),('authored_c_credit',1),('source_sha256','0'*64)]:
   with self.subTest(key=k):
    u=dict(self.unit);u[k]=v
    with self.assertRaises(a.HuffWorkspaceError):d.validate_unit(u)
 def test_CODE_unit_old_profile_rejected(self):
  u=dict(self.codeunit);u['object_profile']='huffman_core'
  with self.assertRaises(a.HuffWorkspaceError):c.validate_unit(u)
 def test_profile_checksum_rejection(self):
  with patch.object(Path,'read_bytes',return_value=b'{}'):
   with self.assertRaises(a.HuffWorkspaceError):a.profile()
 def test_exact_SOURCE_inverse_CODE(self):
  new=(M/c.SOURCE).read_text();oldsrc=(F/'old-source.asm').read_text();s=new.replace('group DGROUP\n','',1)
  for n in self.p['group_names']:s=s.replace('extern '+n+':wrt DGROUP\n','extern '+n+'\n')
  self.assertEqual(s,oldsrc)
 def test_checker_validates_two_versioned_units(self):check.validate_units([self.codeunit,self.unit],0x100000,0x100000)
 def test_checker_DATA_evidence_route(self):
  with patch.object(d,'validate_evidence',return_value='data-marker')as fn:
   self.assertEqual(check.validate_rea_extent(self.unit,M,'x',{}),'data-marker');fn.assert_called_once()
 def test_saved_CODE_whole_native_comparison_no_generation(self):
  raw,meta=a.extract_code(self.new);built=c.Build(self.new,raw,meta,{});body,proof=c.validate_comparison(self.codeunit,built,self.ref['image'],M,self.ref['relocations']);self.assertEqual(len(body),self.codeunit['size']);self.assertEqual(len(proof['complete77_relocations']),77)
 def test_owned_DATA_evidence_route_checks_native(self):
  self.assertTrue(d.validate_evidence(self.unit,M,self.ref['original_sha256'],self.ref).startswith('ev_'))
 def test_registry_duplicate_UNIT_rejected(self):
  with self.assertRaises(ValueError):check.validate_units([self.unit,self.unit],0x100000,0x100000)
 def test_unknown_DATA_backend_rejected(self):
  u=dict(self.unit);u['backend']='masm510-huff-workspace-anyzero'
  with self.assertRaises(ValueError):check.validate_units([u],0x100000,0x100000)
 def test_CODE_source_checksum_unit_rejected(self):
  u=dict(self.codeunit);u['source_sha256']='0'*64
  with self.assertRaises(a.HuffWorkspaceError):c.validate_unit(u)
 def test_DATA_source_exact_checksum(self):self.assertEqual(a.sha((M/d.SOURCE).read_bytes()),d.SOURCE_SHA256)
 def test_owned_evidence_checksum_rejected(self):
  original=Path.read_bytes
  def bad(p):return b'{}'if str(p).endswith('/packet-coverage.json')else original(p)
  with patch.object(Path,'read_bytes',bad):
   with self.assertRaises(a.HuffWorkspaceError):d.validate_evidence(self.unit,M,self.ref['original_sha256'],self.ref)
 def test_DATA_wrong_group_membership_rejected(self):
  o=read_omf(self.data);i=next(i for i,(k,at,b)in enumerate(o.records)if k==0x9a);k,at,b=o.records[i];o.records[i]=(k,at,b[:1])
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_DATA_fake_LEDData_fill_rejected(self):
  o=read_omf(self.data);o.segments[1].unsupported_data=False;o.segments[1].chunks=[(0,bytes(5120))]
  with self.assertRaises(a.HuffWorkspaceError):a._data_structure(o)
 def test_bounded_decoder_unknown_repeat_rejected(self):
  encoded=bytes.fromhex('0104010001000000020000')
  with self.assertRaises(a.HuffWorkspaceError):a._decode_observed_tree(encoded,5120)
if __name__=='__main__':unittest.main()
