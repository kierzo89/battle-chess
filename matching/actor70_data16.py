"""One exact initialized C Actor70 contribution; default DATA/LIDATA gates unchanged."""
from pathlib import Path
import json,hashlib,re
from omf import OMFError
from library16 import LibraryError
from actor70_lidata_raw import validate as decode_raw
from actor70_generation_scope import scope
PROFILE=json.loads(Path(__file__).with_name('actor70_data16_profile.json').read_text());BACKEND='msc500-actor70-lidata-omf';SOURCE='src/data/actors_05e0.c';FLAGS=['/AS','/Zl','/Zi']
class ActorDataError(OMFError):pass
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ActorDataError('Actor70 DATA: '+m)
def validate_unit(unit):need(unit==PROFILE['unit'],'exact source/unit/extent/flags/evidence; no overlays/extra allocation')
def validate_raw(raw):
 try:return decode_raw(raw)
 except(AssertionError,ValueError,LibraryError,IndexError,KeyError)as e:raise ActorDataError('Actor70 closed raw/type/writer contract: '+str(e))from e

def compile_source(source,unit,project,*,compiler_fn):
 validate_unit(unit);project=Path(project).resolve();source=Path(source).resolve();need(source==project/SOURCE and sha(source.read_bytes())==PROFILE['source_sha256'],'unchanged genuine source')
 need(sha((project/'config/msc500.json').read_bytes())==PROFILE['config_sha256']and sha(Path('/usr/bin/dosbox').read_bytes())==PROFILE['dosbox_sha256'],'pinned compilerconfig/DOSBox')
 for name,h in PROFILE['tools'].items():need(sha((project/'toolchains/msc500'/name).read_bytes())==h,'pinned compiler tool '+name)
 need(sha((project/'toolchains/msc500/manifest.json').read_bytes())==PROFILE['manifest_sha256'],'pinned compiler manifest')
 probes=[project.parent/'CHESS.EXE',project/'build/exepack/TRIM5_UNPACK.EXE',project/'evidence/actors70-data1960/Actor.OBJ',project/'evidence/actors70-data1960/calibration.json',project/'config/units.json']
 with scope(source,project,probes)as receipt:
  compiled=compiler_fn(source,FLAGS,compiler='msc500')
 return compiled,receipt

def validate_compiled(compiled,source_bytes,unit):
 validate_unit(unit);need(sha(source_bytes)==compiled.source_sha256==PROFILE['source_sha256']and compiled.compiler=='msc500'and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'and compiled.toolchain_manifest_sha256==PROFILE['manifest_sha256']and compiled.tool_hashes==PROFILE['tools'],'source/compiler/fulltool provenance')
 need(list(compiled.command)==['T:\\CL.EXE','/c','/AS','/Zl','/Zi','/FoC:\\UNIT.OBJ','C:\\UNIT.C'],'actual unaltered compiler command')
 data,proof=validate_raw(compiled.object_bytes);proof.update(boundary='complete_genuine_C_DATA1960_LEDATALIDATA',source_literal_bytes=2,source_iterated_bytes=1958,authentic_LINK_alignment_bytes=0,authored_c_function_count=0,emitted_mz_sites=[],raw_OMF_unchanged=True,historical_capacity_TU_storageclass_dynamicindex_and_absoluteplacement_proven=False)
 return data,proof

def validate_evidence(unit,project,reference,actual):
 """Comparison only: owned small calibration, native primary and logical lower bound."""
 validate_unit(unit);project=Path(project).resolve();items={}
 for path,h in PROFILE['owned_evidence'].items():
  p=project/path;raw=p.read_bytes();need(sha(raw)==h,'owned evidence pin '+path);items[Path(path).name]=raw
 need(items['Actor.OBJ']and sha(items['Actor.OBJ'])==PROFILE['raw_object_sha256'],'whole genuine source ActorOBJ calibration')
 certificate=json.loads(items['calibration.json']);need(certificate['status']=='PASS_ONE_FRESH_C5_MAIN_ONE_AUTHENTIC_FULLLIB_LINK_ACTOR_LIDATA1960'and certificate['literal_initialized']==2 and certificate['iterated_initialized']==1958 and certificate['hole_or_BSS_fill']==0 and certificate['actor_MZ']==[]and not certificate['EXE_executed'],'genuine fullLIB LINK calibration certificate')
 need(sha(items['MAIN.OBJ'])==certificate['MAIN_raw_sha256']and sha(items['CONTROL.EXE'])==certificate['actual_EXE_sha256']and sha(items['CONTROL.MAP'])==certificate['actual_MAP_sha256'],'all calibration output bytes')
 exe=items['CONTROL.EXE'];header=int.from_bytes(exe[8:10],'little')*16;at=certificate['actual_MAP_actors'];need(exe[header+at:header+at+1960]==actual,'actual LINK1960 FILE bytes')
 mapping=items['CONTROL.MAP'].decode();section=mapping.split('Publics by Name')[1].split('Publics by Value')[0];mp={name:int(a,16)*16+int(b,16)for a,b,name in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',section,re.M)};need(mp['_actors']==at,'actual MAP Actor origin')
 table=int.from_bytes(exe[24:26],'little');mz=[int.from_bytes(exe[table+i*4+2:table+i*4+4],'little')*16+int.from_bytes(exe[table+i*4:table+i*4+2],'little')for i in range(int.from_bytes(exe[6:8],'little'))];need(not any(at-1<=s<at+1960 for s in mz),'no calibration ActorMZ')
 for phase in ['actor','MAIN','LINK']:
  g=json.loads(items[phase+'-generation.json']);o=json.loads(items[phase+'-root-terminal.json']);need(g['status']=='COMPLETE'and g['guard_closed']and len(g['blocked_probes'])==20 and o['terminal']and o['reaped']and o['exit_code']==0 and o['DOSBox_pid']==g['calls'][0]['pid'],'genuine '+phase+' closed generation')
 minimum=json.loads(items['logical-minimum-proof.json']);need(minimum['status']=='SUPPORTED_COMPATIBLE_MINIMUM70'and minimum['CODE_fields']==61 and minimum['DEBUG_fields']==7 and minimum['max_static_addend']==1950 and minimum['no_fixed_record_above69'],'actual logical minimum70 evidence')
 from reference import validate_expanded_read
 ev=json.loads(items['rea-actors1960.json']);return {'native_primary_id':validate_expanded_read(ev,unit,actual,reference,emitted_mz_sites=[]),'calibration_MAP_origin':at,'calibration_actor_bytes':1960,'source_literal_bytes':2,'source_iterated_bytes':1958,'historical_capacity_dynamicdomain_TU_and_absoluteplacement_proven':False}
