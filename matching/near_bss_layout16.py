"""One explicit uninitialized machine-layout SOURCE object; zero matching credit."""
from pathlib import Path
from dataclasses import dataclass
import hashlib,json,tempfile,subprocess
from omf import read_omf
import near_bss_layout_model as model
KIND='bss-layout-whole-omf'
BACKEND='nasm-native-near-bss-machineview-layout-omf-v1'
SOURCE='asm/link/native_near_bss190.asm'
SOURCE_SHA256='931a98e6349a5b5bf09e17337a5bf2c4e4033b9b462c5e08aa9fcf0bca79de1f'
RAW_SHA256='1f908f7bfe9115a07f485fe206e70f072455e72eb118150a97b98bbc7d64522c'
NASM_SHA256='57b8fc5957237b0d9b1ff48c8f5823780fb8ce968d9b8434850c06941ad5d5f5'
OWNER='native_near_bss190_machine_views'
SPEC_SHA256='7439ed2ea86b0678e28a352fd75a3fb039395d0457c8a949597fd1d78788fad2'
EVIDENCE_PINS_SHA256='16cc5faffaeda929ccbbc5cacbe0f84640f1efcdb3b9521e1f91c1f59c0609a4'
D=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
def spec():
 b=(D/'near_bss_layout_spec.json').read_bytes();assert H(b)==SPEC_SHA256;return model.validate(json.loads(b))
def validate_evidence():
 data=(D/'near_bss_layout_evidence_pins.json').read_bytes();assert H(data)==EVIDENCE_PINS_SHA256
 pins=json.loads(data);mapping={r['original_path']:r for r in pins}
 for r in pins:assert H((D/r['owned_path']).read_bytes())==r['sha256']
 for r in spec()['PUBLICs']:assert mapping[r['evidence']['path']]['sha256']==r['evidence']['sha256']
 clear=json.loads((D/pins[2]['owned_path']).read_text());markers=json.loads((D/pins[5]['owned_path']).read_text())
 assert clear['native_CRT_clear_DS']==[0x52cc,0xcbe0]and clear['clear_and4096_fit_DOS_minimum']is True and markers['native_clear']['clear_bytes']==30996 and markers['native_30prefix']['bytes']==30
 return {'native_clear_DS':[0x52cc,0xcbe0],'native_clear_bytes':30996,'private_C4_excluded':True,'190_machine_views_proved':True,'historical_C_identity_capacity_TU_proven':False}
def inspect(raw):
 assert H(raw)==RAW_SHA256,'Unreviewed complete BSS190 OMF'
 shape=model.inspect(raw,spec());assert shape['physical_uninitialized_bytes']==30986
 return shape
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 metadata:dict
 provenance:dict
def assemble(source,project):
 p=Path(project).resolve();source=Path(source).resolve();assert source==(p/SOURCE).resolve()and source.is_relative_to(p)and H(source.read_bytes())==SOURCE_SHA256
 binary=Path('/usr/bin/nasm').resolve();assert H(binary.read_bytes())==NASM_SHA256
 validate_evidence()
 from near_bss_layout_generation_scope import scope
 probes=[p.parent/'CHESS.EXE',p/'build/exepack/TRIM5_UNPACK.EXE',p/'build/near-BSS190-one-NASM-root-actual/scratch/UNIT.OBJ',p/'near_bss_layout_spec.json',p/'config/units.json']
 with scope(source,p,probes)as guard:
  with tempfile.TemporaryDirectory(prefix='near-bss190-')as tmp:
   root=Path(tmp);(root/'UNIT.ASM').write_bytes(source.read_bytes());r=subprocess.run([str(binary),'-f','obj','-o','UNIT.OBJ','UNIT.ASM'],cwd=root,capture_output=True,timeout=45)
   assert r.returncode==0 and not r.stderr,r.stderr;raw=(root/'UNIT.OBJ').read_bytes()
 # Parser/native/layout evidence is comparison-only, after actual source GEN closes.
 assert H(source.read_bytes())==SOURCE_SHA256 and H(binary.read_bytes())==NASM_SHA256
 shape=inspect(raw)
 return Build(raw,shape,{'source_sha256':SOURCE_SHA256,'object_sha256':H(raw),'generator':'NASM','build_command':['/usr/bin/nasm','-f','obj','-o','UNIT.OBJ','UNIT.ASM'],'fresh_directory':True,'source_tools_new_scratch_only':True,'generation_guard':guard,'initialized_bytes':0,'uninitialized_machine_layout_bytes':30986,'authored_C_function_credit':0,'FILE_or_native_MZ_credit':0,'historical_C_identity_capacity_TU_proven':False})
def validate_row(row):
 assert row['kind']==KIND and row['source']==SOURCE and row['source_sha256']==SOURCE_SHA256 and row['comparison_expected_raw_sha256']==RAW_SHA256
 assert row['selected_owners']==[OWNER]and row['source_name']=='UNIT.ASM'and row['compiler_flags']==[]and row['generator']=='NASM'and row['generator_argv_tail']==['-f','obj','-o','UNIT.OBJ','UNIT.ASM']and row['object_profile']=='native_near_bss190_v1'
 assert row['public_adapter']['module']=='near_bss_layout16'and row['public_adapter']['function']=='assemble'and row['generation_tools']=={}
def generate(descriptor,project,components):
 import importlib
 rows=[r for r in descriptor['rows']if r['kind']==KIND];assert len(rows)<=1
 result=[]
 for row in rows:
  validate_row(row);built=assemble(Path(project)/SOURCE,project);out=Path(components)/'machine-layouts'/('native_near_bss190.obj');out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists();out.write_bytes(built.object_bytes)
  result.append({'id':OWNER,'kind':KIND,'source':SOURCE,'source_sha256':SOURCE_SHA256,'object':str(out.resolve()),'object_sha256':H(built.object_bytes),'status':'uninitialized_machine_layout_generated','uninitialized_bytes':30986,'PUBLIC_views':190,'physical_positions':186,'no_initialized_or_C_function_or_FILE_credit':True,'comparison':built.metadata,'provenance':built.provenance})
 return result
