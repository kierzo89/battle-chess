"""Adopted closed-runtime controls; all fixtures genuine whole members, no child execution."""
from pathlib import Path
import sys,json,unittest,copy,hashlib,subprocess
from unittest.mock import patch
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file());sys.path.insert(0,str(M));sys.dont_write_bytecode=True
import runtime_external3 as b
from omf import read_omf
from library16 import LibraryError,extract_member
F=M/'tests/fixtures/runtime_external3'
class RuntimeExternal3Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.raw={n:(F/(n+'.obj')).read_bytes()for n in b.SPECS};cls.units={u['member']:u for u in json.loads((F/'units.json').read_text())if u['backend']==b.BACKEND}
 def reject(self,fn,*a,**kw):
  with self.assertRaises((ValueError,KeyError)):fn(*a,**kw)
 def edit(self,name,k,fn,ordinal=0):
  raw=self.raw[name];at=0;found=[]
  while at<len(raw):
   kind=raw[at];n=int.from_bytes(raw[at+1:at+3],'little')
   if kind==k:found.append((at,n,raw[at+3:at+2+n]))
   at+=3+n
  at,n,p=found[ordinal];new=fn(p);self.assertNotEqual(new,p);h=bytes([k])+(len(new)+1).to_bytes(2,'little')+new;r=h+bytes([-sum(h)%256]);return raw[:at]+r+raw[at+3+n:]
 def test_adopted_module(self):self.assertEqual(Path(b.__file__).resolve(),M/'runtime_external3.py')
 def test_three_genuine_raw_profiles(self):
  for n,s in b.SPECS.items():v=b.parse_member(self.raw[n],n);self.assertEqual(len(v['last_writer_bytes']),s['size']);self.assertEqual(sum(len(q['overwritten'])for q in v['writers']),1)
 def test_whole_library_selector(self):
  lib=(M/'toolchains/runtime-libh/LIBH.LIB').read_bytes()
  for n,s in b.SPECS.items():self.assertEqual(extract_member(lib,n,b.LIBSHA,s['sha256'],validate_object=False).data,self.raw[n])
 def test_default_reader_stays_closed(self):
  for raw in self.raw.values():self.reject(read_omf,raw)
 def test_no_signed_LREM_profile(self):self.reject(b.parse_member,self.raw['ULREM'],'LREM')
 def test_unknown_member(self):self.reject(b.parse_member,self.raw['ULDIV'],'ALDIV')
 def test_wrong_member_raw(self):self.reject(b.parse_member,self.raw['ULDIV'],'ULREM')
 def test_checksum(self):v=bytearray(self.raw['LDIV']);v[-1]^=1;self.reject(b.parse_member,bytes(v),'LDIV')
 def test_truncation(self):self.reject(b.parse_member,self.raw['ULDIV'][:-1],'ULDIV')
 def test_trailing_bytes(self):self.reject(b.parse_member,self.raw['ULREM']+b'\0','ULREM')
 def test_unknown_record(self):
  raw=self.raw['ULDIV'];p=bytearray(raw);n=int.from_bytes(p[1:3],'little');p[0]=0x81;p[2+n]=(-sum(p[:2+n]))%256;self.reject(b.parse_member,bytes(p),'ULDIV')
 def test_duplicate_PUBLIC(self):self.reject(b.parse_member,self.edit('ULDIV',0x90,lambda p:p+p[2:]),'ULDIV')
 def test_nonzero_PUBLIC_offset(self):self.reject(b.parse_member,self.edit('ULDIV',0x90,lambda p:p[:-3]+b'\x01'+p[-2:]),'ULDIV')
 def test_nonzero_external_type(self):self.reject(b.parse_member,self.edit('ULDIV',0x8c,lambda p:p[:-1]+b'\x01'),'ULDIV')
 def test_no_signed_mul_name_substitution(self):self.reject(b.parse_member,self.edit('ULDIV',0x8c,lambda p:p.replace(b'__aNulmul',b'__aNlmul_')),'ULDIV')
 def test_no_DATA_allocation(self):self.reject(b.parse_member,self.edit('ULDIV',0x98,lambda p:p[:1]+b'\x01\0'+p[3:],1),'ULDIV')
 def test_wrong_CODE_extent(self):self.reject(b.parse_member,self.edit('ULDIV',0x98,lambda p:p[:1]+b'\x66\0'+p[3:]),'ULDIV')
 def test_first_writer_hole(self):self.reject(b.parse_member,self.edit('ULDIV',0xa0,lambda p:p[:1]+b'\x01\0'+p[3:]),'ULDIV')
 def test_wrong_overlap_site(self):self.reject(b.parse_member,self.edit('ULDIV',0xa0,lambda p:p[:1]+b'\x61\0'+p[3:],1),'ULDIV')
 def test_final_RET_not_invented(self):self.reject(b.parse_member,self.edit('ULDIV',0xa0,lambda p:p[:-2]+b'\0\0',1),'ULDIV')
 def test_no_trimmed_final_writer(self):self.reject(b.parse_member,self.edit('ULDIV',0xa0,lambda p:p[:-1],1),'ULDIV')
 def test_unrelated_payload_authentication(self):self.reject(b.parse_member,self.edit('ULDIV',0xa0,lambda p:p[:3]+bytes([p[3]^1])+p[4:]),'ULDIV')
 def test_wrong_CALL_source(self):
  s=b.SPECS['ULDIV'];self.reject(b.parse_member,self.edit('ULDIV',0xa0,lambda p:p[:3+s['field']]+b'\x01'+p[4+s['field']:]),'ULDIV')
 def test_native_units_exact(self):
  for u in self.units.values():b.validate_unit(u)
 def test_wrong_native_binding(self):
  u=copy.deepcopy(self.units['near_ulrem']);u['externals']['__aNulmul']['offset']+=1;self.reject(b.validate_unit,u)
 def test_wrong_signed_symbol(self):
  u=copy.deepcopy(self.units['near_ulrem']);u['symbol']='__aNlrem';self.reject(b.validate_unit,u)
 def test_no_larger_extent(self):
  u=copy.deepcopy(self.units['near_ldiv']);u['size']+=1;self.reject(b.validate_unit,u)
 def test_closed_real_certificate(self):cert,docs=b._certificate(M);self.assertEqual(len(cert['whole_members']),3)
 def test_certificate_FILE_tamper(self):
  cert,docs=b._certificate(M);d=dict(docs);v=bytearray(d['LINK_EXE']);v[-1]^=1;d['LINK_EXE']=bytes(v);self.reject(b.validate_calibration,cert,d)
 def test_certificate_MAP_tamper(self):
  cert,docs=b._certificate(M);d=dict(docs);d['LINK_MAP']=d['LINK_MAP']+b'\n';self.reject(b.validate_calibration,cert,d)
 def test_certificate_stubs_or_member_injection(self):
  cert,docs=b._certificate(M);d=dict(docs);d['LINK_RSP']=d['LINK_RSP'].replace(b'CONTROL.OBJ',b'CONTROL.OBJ+FAKE.OBJ');self.reject(b.validate_calibration,cert,d)
 def test_certificate_root_terminal(self):
  cert,docs=b._certificate(M);d=dict(docs);o=json.loads(d['LINK_terminal']);o['terminal']=False;d['LINK_terminal']=json.dumps(o).encode();self.reject(b.validate_calibration,cert,d)
 def test_all3_complete_native_reads_and_fourbases(self):
  for n,s in b.SPECS.items():
   result=b.render_for_comparison(self.units[s['id']],M);primary=json.loads((M/('evidence/runtime4-authentic/'+n+'-read.json')).read_text());self.assertEqual(result.image,bytes.fromhex(primary['raw_result']['bytes_hex']));self.assertEqual(result.object_bytes,self.raw[n]);self.assertEqual(result.provenance['native_MZ'],[])
   for paragraph in[0,1,4096,65535]:self.assertEqual(result.image,bytes.fromhex(primary['raw_result']['bytes_hex']))
 def test_renderer_no_target_or_child(self):
  old=Path.read_bytes
  def read(p,*a,**k):
   self.assertNotIn(Path(p).resolve(),[(M.parent/'CHESS.EXE').resolve(),(M/'build/exepack/TRIM5_UNPACK.EXE').resolve()]);return old(p,*a,**k)
  with patch.object(Path,'read_bytes',read),patch.object(subprocess,'Popen',side_effect=AssertionError('no child allowed')),patch.object(subprocess,'run',side_effect=AssertionError('no child allowed')):b.render_for_comparison(self.units['near_uldiv'],M)
 def test_old_ALDIV_gate_not_broadened(self):self.reject(b.old.load_profile,'near_uldiv',M)
 def test_ATOL_uses_existing_generic_route(self):
  from check import runtime_inputs,link_runtime_segment
  u=next(u for u in json.loads((F/'units.json').read_text())if u['member']=='ATOL');cfg,module,member,obj=runtime_inputs(u,M);actual,fixups=link_runtime_segment(obj,module);self.assertEqual(len(actual),3);self.assertEqual(len(fixups),1);self.assertEqual(actual,bytes.fromhex(json.loads((M/u['rea_evidence']).read_text())['raw_result']['bytes_hex']))
if __name__=='__main__':unittest.main()
