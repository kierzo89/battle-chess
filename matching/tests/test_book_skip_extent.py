import copy,json,sys,tempfile,unittest
from pathlib import Path
from dataclasses import replace
PROJECT=Path(__file__).resolve().parents[1]
HERE=PROJECT/'build/book-skip-extent-stage'
sys.path.insert(0,str(PROJECT))
from omf import read_omf
from book_skip_extent import validate_book_skip_extent,ORIGINAL,NATIVE

class BookSkipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit=json.loads((HERE/'proposed-skip-unit.json').read_text())
        cls.raw=(PROJECT/'build/book-scan-843f/positive800.obj').read_bytes()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.project=Path(self.tmp.name)
        self.u=copy.deepcopy(self.unit);self.obj=read_omf(self.raw)
        for path in [self.u['rea_evidence']]+[v for k,v in self.u['extended_extent'].items()if k!='kind']:
            dest=self.project/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((PROJECT/path).read_bytes())
    def go(self,linked=NATIVE,emitted=None,obj=True):
        return validate_book_skip_extent(self.u,self.project,ORIGINAL,emitted or self.obj.function_info(self.u['symbol']),linked,self.obj if obj else None)
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
            self.obj=copy.deepcopy(original);idx=next(i for i,f in enumerate(self.obj.fixups)if f.offset==734);self.obj.fixups[idx]=replace(self.obj.fixups[idx],**change);self.reject()
        self.obj=copy.deepcopy(original);self.obj.fixups.append(next(f for f in self.obj.fixups if f.offset==734));self.reject()
    def test_raw_addend(self):
        # Robustly mutate the raw field across arbitrarily split LEDATA records.
        self.obj=read_omf(self.raw);s=self.obj.segments[1]
        s.chunks=[(at,b[:739-at]+b'\x01'+b[740-at:]if at<=739<at+len(b)else b)for at,b in s.chunks];self.reject()
    def test_code_tail_or_hole(self):
        self.obj.segments[1].length=801;self.reject()
    def test_wrong_closed_unit(self):
        self.u['size']=2;self.reject()
    def test_fresh_compile_exact_fixture(self):
        from msc import compile_c
        result=compile_c(PROJECT/'build/book-scan-843f/book_context_800_match.c',['/AS','/Gs','/Os','/Zi'],compiler='msc500')
        self.assertEqual(result.object_bytes,self.raw)
        self.obj=read_omf(result.object_bytes);self.go()

if __name__=='__main__':unittest.main()
