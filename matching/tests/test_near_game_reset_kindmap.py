"""Actual two positive whole OMF fixtures; no generation in focused controls."""
from pathlib import Path
from dataclasses import replace
import copy,hashlib,json,unittest
import near_game_code16 as b
from omf import read_omf
class ClosedResetKindMapView(unittest.TestCase):
 keys=('reset_position08de_kind_map_1168',)
 def raw(self,k):
  filename={'decode_frame_directory289':'decode_directory289'}.get(k,k)
  return(Path(__file__).parent/'fixtures/near_game'/(filename+'.obj')).read_bytes()
 def each(self):
  for k in self.keys:yield k,b.spec(k),self.raw(k)
 def test_actual_whole_objects(self):
  for k,s,r in self.each():self.assertEqual(len(b.extract_code(r,k)[0]),s['size'])
 def test_actual_all_fields(self):
  for k,s,r in self.each():self.assertEqual(len(read_omf(r).fixups),144)
 def test_source_identity(self):
  for k,s,r in self.each():b.source_policy((Path(b.__file__).parent/s['unit']['source']).read_bytes(),s['unit']['source'])
 def test_source_extra_instruction_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.source_policy((Path(b.__file__).parent/s['unit']['source']).read_bytes()+b'\nNOP\n',s['unit']['source'])
 def test_wrong_source_route_rejected(self):
  with self.assertRaises(ValueError):b.source_policy(b'RET\n','asm/link/unknown.asm')
 def test_profiles_not_interchangeable(self):
  closed=('decode_frame_directory289', 'load_group_frames1030', 'load_asset_group178', 'undo_animation327', 'animate_move363', 'save_cc72_610', 'reset_position08de_1168')
  for actual in closed:
   for wrong in closed:
    if actual==wrong:continue
    with self.subTest(actual=actual,wrong=wrong):
     with self.assertRaises(ValueError):b.extract_code(self.raw(actual),wrong)
 def test_all_closed_7_whole_fixtures_regression(self):
  for key in ('decode_frame_directory289', 'load_group_frames1030', 'load_asset_group178', 'undo_animation327', 'animate_move363', 'save_cc72_610', 'reset_position08de_1168'):
   with self.subTest(profile=key):
    raw=self.raw(key);code,metadata=b.extract_code(raw,key);self.assertEqual(len(code),b.spec(key)['size']);self.assertEqual(hashlib.sha256(raw).hexdigest(),b.spec(key)['object_sha256'])
 def test_checksum_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.extract_code(r[:-1]+bytes([r[-1]^1]),k)
 def test_truncation_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.extract_code(r[:-1],k)
 def test_unknown_profile_rejected(self):
  with self.assertRaises(ValueError):b.spec('load_unknown')
 def test_unit_extent_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);u['size']+=1
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_unit_extra_key_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);u['waiver']=True
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_unit_wrong_symbol_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);u['public_symbols']=['_alias']
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_unit_wrong_native_binding_rejected(self):
  for k,s,r in self.each():
   u=copy.deepcopy(s['unit']);n=next(iter(u['externals']));u['externals'][n]+=1
   with self.assertRaises(ValueError):b.validate_unit(u)
 def test_raw_records_missing_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.records=o.records[:-1]
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_raw_records_payload_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);z,at,p=o.records[0];o.records[0]=(z,at,p+b'x')
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_CODE_hole_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);at,p=o.segments[2].chunks[0];o.segments[2].chunks[0]=(1,p)
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_CODE_byte_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);at,p=o.segments[2].chunks[0];o.segments[2].chunks[0]=(at,bytes([p[0]^1])+p[1:])
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_CODE_extent_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.segments[2].length+=1
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_DATA_allocation_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.segments[1].length=1
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_PUBLIC_alias_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.publics['_alias']=next(iter(o.publics.values()))
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_PUBLIC_frame_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);n=next(iter(o.publics));o.publics[n]=replace(o.publics[n],group=1)
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_missing_FIXUP_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups=o.fixups[:-1]
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_FIXUP_frame_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups[0]=replace(o.fixups[0],frame=(5,None))
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_FIXUP_target_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups[0]=replace(o.fixups[0],target=(2,65535))
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_FIXUP_displacement_rejected(self):
  for k,s,r in self.each():
   o=read_omf(r);o.fixups[0]=replace(o.fixups[0],displacement=(o.fixups[0].displacement or 0)+1)
   with self.assertRaises(ValueError):b.validate_object(o,k)
 def test_wrong_load_rejected(self):
  for k,s,r in self.each():
   with self.assertRaises(ValueError):b.link_code(r,k,65536)
 def test_full_native_fourbases(self):
  from reference import build_reference
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for k,s,r in self.each():
   for load in[0,1,4096,65535]:
    code,logs=b.link_code(r,k,load);expected=bytearray(ref['image'][s['base']:s['base']+s['size']])
    for site in s['native_MZ']:
     at=site-s['base'];expected[at:at+2]=((int.from_bytes(expected[at:at+2],'little')+load)&65535).to_bytes(2,'little')
    self.assertEqual(code,expected);self.assertEqual(len(logs),144)
    self.assertEqual(sorted(q['mz_segment_relocation_image_offset']for q in logs if 'mz_segment_relocation_image_offset'in q),s['native_MZ'])
 def test_complete_owned_evidence(self):
  from reference import build_reference,ORIGINAL_SHA256
  ref=build_reference(Path('/home/kierzo/chess/CHESS.EXE').read_bytes())
  for k,s,r in self.each():self.assertTrue(b.validate_evidence(s['unit'],Path(b.__file__).parent,ORIGINAL_SHA256,ref))
 def test_zero_credit_no_storage(self):
  for k,s,r in self.each():
   _,m=b.extract_code(r,k);self.assertEqual(m['C_credit'],0);self.assertEqual(m['DATA_byte_credit'],0);self.assertEqual(len(m['native_MZ']),1)
 def test_actual_single_FAR_frame(self):
  o=read_omf(self.raw(self.keys[0]));far=[f for f in o.fixups if f.width==4]
  self.assertEqual(len(far),1)
  for f in far:self.assertEqual((f.location_type,f.segment_relative,f.frame),(3,True,(2,f.target[1])))
 def test_each_far_frame_rejected(self):
  raw=self.raw(self.keys[0]);o=read_omf(raw)
  for i,f in enumerate(o.fixups):
   if f.width==4:
    q=read_omf(raw);q.fixups[i]=replace(f,frame=(5,None))
    with self.assertRaises(ValueError):b.validate_object(q,self.keys[0])
 def test_each_far_width_rejected(self):
  raw=self.raw(self.keys[0]);o=read_omf(raw)
  for i,f in enumerate(o.fixups):
   if f.width==4:
    q=read_omf(raw);q.fixups[i]=replace(f,width=2)
    with self.assertRaises(ValueError):b.validate_object(q,self.keys[0])
 def test_missing_native_MZ_rejected(self):
  s=b.spec(self.keys[0])
  with self.assertRaises(ValueError):b._sites(s,s['native_MZ'][:-1])
 def test_extra_native_MZ_rejected(self):
  s=b.spec(self.keys[0])
  with self.assertRaises(ValueError):b._sites(s,s['native_MZ']+[s['base']])
 def test_crossing_native_MZ_rejected(self):
  s=b.spec(self.keys[0])
  with self.assertRaises(ValueError):b._sites(s,s['native_MZ']+[s['base']-1])
 def test_actual_CODE_alignment_WORD(self):self.assertEqual(read_omf(self.raw(self.keys[0])).segments[2].attributes,72)
 def test_V1_V2_V3_controls_are_distinct(self):
  s=b.spec(self.keys[0]);P=Path(b.__file__).parent/s['evidence_root'];negative=json.loads((P/'V1-negative-binder.json').read_text());self.assertTrue(negative)
  g=json.loads((P/'generation.json').read_text());self.assertEqual(g['actual_MASM_calls'],1);self.assertEqual(g['status'],'COMPLETE')

 def physical_inputs(self):
  k=self.keys[0];s=b.spec(k);P=Path(b.__file__).parent;r=s['evidence_root'];out={n:json.loads((P/n).read_text())for n in b.EVIDENCE_PINS[k]};pr=out[r+'/primary.json'];return s,pr,pr['normalized_result']['procedure']['body'],pr['analysis_profile']['parameters'],out,r
 def physical(self,v):return b._reset_physical_evidence(*v)
 def test_closed_physical_live_primary(self):self.physical(self.physical_inputs())
 def test_fake_contiguous_live_body_rejected(self):
  v=copy.deepcopy(self.physical_inputs());v[2].update(non_contiguous=False,total_bytes=1168)
  with self.assertRaises(ValueError):self.physical(v)
 def test_wrong_live_ranges_rejected(self):
  v=copy.deepcopy(self.physical_inputs());v[2]['ranges'][0]['end']='0x10d3a'
  with self.assertRaises(ValueError):self.physical(v)
 def test_wrong_read_extent_rejected(self):
  v=copy.deepcopy(self.physical_inputs());v[4][v[5]+'/physical-read.json']['normalized_result']['requested_bytes']=1168
  with self.assertRaises(ValueError):self.physical(v)
 def test_wrong_read_byte_rejected(self):
  v=copy.deepcopy(self.physical_inputs());n=v[4][v[5]+'/physical-read.json']['normalized_result'];raw=bytearray.fromhex(n['bytes_hex']);raw[0]^=1;n['bytes_hex']=raw.hex()
  with self.assertRaises(ValueError):self.physical(v)
 def test_unrelocated_carrier_word_rejected(self):
  v=copy.deepcopy(self.physical_inputs());n=v[4][v[5]+'/physical-read.json']['normalized_result'];raw=bytearray.fromhex(n['bytes_hex']);a=0xd2b-0x8de;raw[a:a+2]=(0xfbf).to_bytes(2,'little');n['bytes_hex']=raw.hex()
  with self.assertRaises(ValueError):self.physical(v)
 def test_fake_positive_gap_instruction_rejected(self):
  v=copy.deepcopy(self.physical_inputs());v[4][v[5]+'/gap-instruction.json']['normalized_result']['status']='decoded'
  with self.assertRaises(ValueError):self.physical(v)
 def test_added_gap_xref_rejected(self):
  v=copy.deepcopy(self.physical_inputs());v[4][v[5]+'/gap-xrefs.json']['normalized_result']=['0x108de']
  with self.assertRaises(ValueError):self.physical(v)
 def test_dead_JMP_as_NOP_rejected(self):
  v=copy.deepcopy(self.physical_inputs());q=next(q for q in v[4][v[5]+'/instruction-ledger.json']if q['image']==0xd39);q['native_hex']='9090'
  with self.assertRaises(ValueError):self.physical(v)
 def test_wrong_live_instruction_rejected(self):
  v=copy.deepcopy(self.physical_inputs());v[0]['instructions']=391
  with self.assertRaises(ValueError):self.physical(v)
 def test_local_EQU_exact_source_only(self):
  s=b.spec(self.keys[0]);raw=(Path(b.__file__).parent/s['unit']['source']).read_bytes();self.assertEqual(raw.count(b'FULLWORD_IMMEDIATE_ZERO EQU 0'),1)
  with self.assertRaises(ValueError):b.source_policy(raw.replace(b'EQU 0',b'EQU 1'),s['unit']['source'])
 def test_two_native_fullword_ANDs(self):
  k=self.keys[0];raw=self.raw(k);code,_=b.link_code(raw,k)
  for a in[0xa2d,0xc67]:self.assertEqual(code[a-0x8de:a-0x8de+4],bytes.fromhex('81e10700'))
 def test_source_no_added_gap_filler(self):
  s=b.spec(self.keys[0]);text=(Path(b.__file__).parent/s['unit']['source']).read_text();self.assertIn('JMP SHORT code_0d65 ; native 0D39',text)
 def test_original_count_failure_preserved(self):
  v=self.physical_inputs();negative=v[4][v[5]+'/original-count-negative.json'];self.assertTrue(negative['error']);self.assertEqual(len(v[4][v[5]+'/comparison.json']['actual_internal_NEAR_fields']),12)

 def test_exact_four_existing_owner_fields(self):
  s=b.spec(self.keys[0]);rows=[r for r in s['external_fields']if r['symbol']=='_kind_map'];self.assertEqual([r['offset']for r in rows],[95,144,677,713]);self.assertTrue(all(r['native_target']==0xf00 and r['source_addend']==1 for r in rows));self.assertFalse([r for r in s['external_fields']if r['symbol']=='_palette_kinds_0f01'])
 def test_old_profile_snapshot_preserved(self):
  self.assertEqual(b.spec('reset_position08de_1168')['source_sha256'],'35d6151b82627a83debf994dd69c753003fe1685c45a7fc8ca42a273c8c4c170');self.assertNotEqual(b.spec('reset_position08de_1168')['object_sha256'],b.spec(self.keys[0])['object_sha256'])
 def test_full_RAW_CODE_same_old_fixture(self):
  p=Path(__file__).parent/'fixtures/near_game/reset_position08de_1168.obj';a,_=b.extract_code(p.read_bytes(),'reset_position08de_1168');z,_=b.extract_code(self.raw(self.keys[0]),self.keys[0]);self.assertEqual(a,z)
 def test_existing_owner_replaces_name_not_public_alias(self):
  o=read_omf(self.raw(self.keys[0]));self.assertIn('_kind_map',o.externals.values());self.assertNotIn('_palette_kinds_0f01',o.externals.values());self.assertEqual(set(o.publics),{'_reset_position_08de'})
 def test_actual_new_terminal_case_preserved(self):
  s=b.spec(self.keys[0]);P=Path(b.__file__).parent/s['evidence_root'];q=json.loads((P/'comparison-terminal.json').read_text());self.assertIn('comparison_SHA256',q);self.assertNotIn('comparison_sha256',q);b._evidence(Path(b.__file__).parent,self.keys[0])
