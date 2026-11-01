import copy,json,sys,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
from dataclasses import replace
PROJECT=Path(__file__).resolve().parents[1]
HERE=PROJECT/'tests/fixtures/shared_book_skip2418'
sys.path.insert(0,str(PROJECT))
from omf import read_omf
from shared_book_skip_extent2418 import validate_shared_book_skip_extent,ORIGINAL,NATIVE

class SharedBookSkip2418Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit=json.loads((HERE/'unit.json').read_text())
        cls.raw=(HERE/'actual.obj').read_bytes()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name)
        self.u=copy.deepcopy(self.unit);self.obj=read_omf(self.raw)
        for path in [self.u['rea_evidence']]+[v for k,v in self.u['extended_extent'].items()if k!='kind']:
            dest=self.project/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((PROJECT/path).read_bytes())
    def go(self,linked=NATIVE,emitted=None,obj=True):
        return validate_shared_book_skip_extent(self.u,self.project,ORIGINAL,emitted or self.obj.function_info(self.u['symbol']),linked,self.obj if obj else None)
    def mutate(self,key,fn):
        path=self.u['rea_evidence']if key=='entry'else self.u['extended_extent'][key]
        p=self.project/path;e=json.loads(p.read_text());fn(e);p.write_text(json.dumps(e))
    def reject(self):
        with self.assertRaises((ValueError,KeyError,TypeError)):self.go()
    def test_actual_source_fixture_positive(self):
        p=self.go();self.assertEqual((p['entry_native_body_bytes'],p['interior_native_body_bytes'],p['source_CV_bytes']),(2,20,22));self.assertFalse(p['native_partition_rewritten'])
    def test_all22_generated_byte_corruptions(self):
        for at in range(22):
            with self.subTest(at=at),self.assertRaises(ValueError):self.go(NATIVE[:at]+bytes([NATIVE[at]^1])+NATIVE[at+1:])
    def test_truncation_or_tail(self):
        for b in (NATIVE[:2],NATIVE[:-1],NATIVE+b'\x55'):
            with self.subTest(length=len(b)),self.assertRaises(ValueError):self.go(b)
    def test_no_source_object(self):
        with self.assertRaises(ValueError):self.go(obj=False)
    def test_wrong_cv_boundary(self):
        e=self.obj.function_info(self.u['symbol']);e['boundary']='public_to_next'
        with self.assertRaises(ValueError):self.go(emitted=e)
    def test_no_native_two_to22_relabel(self):
        self.mutate('entry',lambda e:e['normalized_result']['procedure']['body'].update(total_bytes=22));self.reject()
    def test_interior_entry_kept(self):
        self.mutate('interior_evidence',lambda e:e['normalized_result']['procedure'].update(address='0x18579'));self.reject()
    def test_partition_no_gap(self):
        self.mutate('interior_evidence',lambda e:e['normalized_result']['procedure']['body']['ranges'][0].update(start='0x1857a'));self.reject()
    def test_next_full_boundary(self):
        self.mutate('next_entry_evidence',lambda e:e['normalized_result']['procedure']['body'].update(contains_entry=False));self.reject()
    def test_incomplete_raw(self):
        self.mutate('raw_span_evidence',lambda e:e['normalized_result'].update(complete=False));self.reject()
    def test_wrong_raw_address(self):
        self.mutate('raw_span_evidence',lambda e:e['parameters'].update(address='0x18579'));self.reject()
    def test_next_raw_middle_mutation(self):
        self.mutate('next_raw_evidence',lambda e:e['normalized_result'].update(bytes_hex=e['normalized_result']['bytes_hex'][:8]+'00'+e['normalized_result']['bytes_hex'][10:]));self.reject()
    def test_mixed_profile(self):
        self.mutate('next_entry_evidence',lambda e:e['analysis_profile'].update(digest='foreign'));self.reject()
    def test_wrong_target(self):
        self.mutate('entry',lambda e:e['subject']['digest'].update(sha256='0'*64));self.reject()
    def test_all_byte_xrefs_required(self):
        self.mutate('all_byte_xrefs_evidence',lambda e:e.pop());self.reject()
    def test_external_interior_entry_rejected(self):
        self.mutate('all_byte_xrefs_evidence',lambda e:e[5]['normalized_result'].append('0x11234'));self.reject()
    def test_operand_entry_rejected(self):
        self.mutate('all_byte_xrefs_evidence',lambda e:e[1]['normalized_result'].append('0x11234'));self.reject()
    def test_cfg_loop_target(self):
        self.mutate('interior_evidence',lambda e:e['normalized_result']['basic_blocks'][1].update(successors=['0x1857a','0x1858c']));self.reject()
    def test_instruction_call_target(self):
        self.mutate('instructions_evidence',lambda e:e[1]['normalized_result']['flow'].update(direct_destinations=['0x1858e']));self.reject()
    def test_instruction_return(self):
        self.mutate('instructions_evidence',lambda e:e[6]['normalized_result'].update(mnemonic='RETF'));self.reject()
    def test_field_frame_target_width_and_extra(self):
        original=copy.deepcopy(self.obj)
        for change in ({'width':4},{'frame':(5,None)},{'target':(0,2)},{'segment_relative':False}):
            self.obj=copy.deepcopy(original);idx=next(i for i,f in enumerate(self.obj.fixups)if f.offset==2352);self.obj.fixups[idx]=replace(self.obj.fixups[idx],**change);self.reject()
        self.obj=copy.deepcopy(original);self.obj.fixups.append(next(f for f in self.obj.fixups if f.offset==2352));self.reject()
    def test_raw_addend(self):
        # Robustly mutate the raw field across arbitrarily split LEDATA records.
        self.obj=read_omf(self.raw);s=self.obj.segments[1]
        s.chunks=[(at,b[:2357-at]+b'\x01'+b[2358-at:]if at<=2357<at+len(b)else b)for at,b in s.chunks];self.reject()
    def test_code_tail_or_hole(self):
        self.obj.segments[1].length=2419;self.reject()
    def test_wrong_closed_unit(self):
        self.u['size']=2;self.reject()

    def test_shared_context_and_relative_field_coordinates(self):
        import shared_turn_book_selector2418 as helper
        before=copy.deepcopy(self.obj.__dict__)
        with patch.object(helper,'validate_shared_object',wraps=helper.validate_shared_object)as selected:
            result=self.go();self.assertEqual(selected.call_count,1)
        self.assertEqual(self.obj.__dict__,before)
        self.assertEqual(result['source_CODE_bytes'],2418)
        emitted=self.obj.function_info('_skip_book_8577')
        self.assertEqual((emitted['offset'],emitted['size']),(2341,22))
        self.assertEqual([f.offset-2341 for f in emitted['fixups']],[16,11,7,3])
        self.assertEqual(sorted(f.offset-2341 for f in emitted['fixups']),[3,7,11,16])
    def test_selector_raw_record_order_and_exact_eight_addresses(self):
        from shared_turn_book_selector2418 import validate_shared_object
        before=copy.deepcopy(self.obj.__dict__)
        validate_shared_object(self.obj)
        offsets=[f.offset for f in self.obj.fixups if f.target==(0,3)]
        self.assertEqual(offsets,[97,1752,2140,2115,2276,2255,2352,2384])
        self.assertNotEqual(offsets,sorted(offsets))
        self.assertEqual(sorted(offsets),[97,1752,2115,2140,2255,2276,2352,2384])
        self.assertEqual(len(offsets),8)
        self.assertEqual(self.obj.__dict__,before)

    def test_new_kind_exact_dispatch(self):
        from extent import validate_extended_extent
        result=validate_extended_extent(self.u,self.project,ORIGINAL,self.obj.function_info(self.u['symbol']),NATIVE,self.obj)
        self.assertEqual(result['kind'],'shared_book_skip_8577_v1')
    def test_old_kind_rejects_new_context(self):
        from book_skip_extent import validate_book_skip_extent
        self.u['extended_extent']['kind']='book_skip_8577_v1'
        with self.assertRaises(ValueError):validate_book_skip_extent(self.u,self.project,ORIGINAL,self.obj.function_info(self.u['symbol']),NATIVE,self.obj)
    def test_old800_fixture_and_gate_preserved(self):
        from book_skip_extent import validate_book_skip_extent
        legacy=read_omf((HERE/'legacy800.obj').read_bytes());unit=copy.deepcopy(self.u);unit['source']='src/book_context_match.c';unit['extended_extent']['kind']='book_skip_8577_v1';unit['owned_selector_const']['kind']='book_far_array_selector_800_v1'
        result=validate_book_skip_extent(unit,self.project,ORIGINAL,legacy.function_info(unit['symbol']),NATIVE,legacy)
        self.assertEqual(result['source_CODE_bytes'],800)
    def test_new_context_rejects_old800(self):
        self.obj=read_omf((HERE/'legacy800.obj').read_bytes());self.reject()
    def test_shared_source_required(self):
        self.u['source']='src/book_context_match.c';self.reject()
    def test_shared_selector_required(self):
        self.u['owned_selector_const']['kind']='book_far_array_selector_800_v1';self.reject()
    def test_no_selector_contract_rejected(self):
        self.u.pop('owned_selector_const');self.reject()
    def test_foreign_non_skip_context_rejected(self):
        self.obj.segments[1].chunks=[(at,bytes([body[0]^1])+body[1:]if at==0 else body)for at,body in self.obj.segments[1].chunks];self.reject()
    def test_eighteen_CV_and_all_fields_required(self):
        self.obj.procedures.pop('_setup_state');self.reject()

if __name__=='__main__':unittest.main()
