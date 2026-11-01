"""Closed genuine mixed-width hardware initialized DATA12; zero C credit."""
from pathlib import Path
from dataclasses import dataclass,asdict
import sys,json,hashlib,os,subprocess,tempfile,re
from omf import read_omf,OMFObject,OMFError
import serial248_code16 as pinned
M=next(p for p in Path(__file__).resolve().parents if(p/'config/msc500.json').is_file())
D=M/'build/platform-data-2eae'
H=lambda b:hashlib.sha256(b).hexdigest()
BACKEND='masm510-platform-state-data-omf'
BASE=0x5face
PUBLICS={'_audio_calibration_ticks_2eae':0,'_saved_timer_vector_2eaf':1,'_speed_2eb3':5,'_saved_critical_vector_2eb5':7,'_saved_pic_mask_2eb9':11}
SOURCES={'build/platform-data-2eae/platform_state_grouped.asm': '3a3f99be136f1dcf6689a67de50ca9807b4d9f65acdb28e1d28de775da14b176', 'build/platform-data-2eae/wrong_speed_grouped.asm': 'd4f6c582c5f388b4cba82fc4e9d7c6400f2ddfa02f5174954d7f37e5d2b327ff'}
OBJECT_HASHES={'b90fcf273f1435d36c898d7a8c1cb1564d7909f244280e80005dfcfadf369e23', 'c69e3be81f7cd496c55d828c104d1a381a448b164f441b2c88c75e0dc7cf5edc'}
class HardwareDataError(OMFError):pass
def require(value,message):
 if not value:raise HardwareDataError(message)
def validate_unit(unit):
 require(set(unit)=={'id','language','backend','source','source_sha256','assembler_sha256','symbols','image_offset','size','reference_region','rea_evidence','boundary_evidence'},'Exact hardware DATA metadata keys')
 require((unit['id'],unit['language'],unit['backend'])==('hardware_state_2eae','asm-data',BACKEND),'Closed hardware DATA identity')
 require(unit['source']in SOURCES and unit['source_sha256']==SOURCES[unit['source']]and unit['assembler_sha256']==pinned.MASM_SHA256,'Pinned source/tool required')
 require(unit['symbols']==list(PUBLICS)and unit['image_offset']==hex(BASE)and type(unit['size'])is int and unit['size']==12,'Complete five-symbol DATA12 only')
 require(unit['reference_region']=='exepack-expanded'and unit['rea_evidence']=='build/platform-data-2eae/rea-native12.json','Pinned expanded native extent')
 require(isinstance(unit['boundary_evidence'],str)and bool(unit['boundary_evidence'].strip()),'Boundary explanation')
def validate_object(obj):
 require(isinstance(obj,OMFObject)and set(obj.segments)=={1},'One complete DATA segment only')
 require(not obj.fixups and not obj.externals and not obj.procedures,'No fixup/external/COMMON/procedure allocation')
 require(obj.names==['','','DGROUP','DATA','_DATA'],'Closed names')
 s=obj.segments[1]
 require((s.name,s.class_name,s.length,s.attributes,s.index,s.name_index,s.class_index,s.overlay_index,s.unsupported_data)==('_DATA','DATA',12,72,1,4,3,1,False),'Whole initialized WORD PUBLIC DATA12')
 require([k for k,_,_ in obj.records]==[0x80,0x96,0x98,0x9a,0x90,0x88,0xa0,0x8a],'No extra records/storage/debug/COMM/LIDATA')
 for kind,expected in [(0x80,[b'\x08UNIT.ASM']),(0x9a,[bytes.fromhex('02ff01')]),(0x88,[bytes.fromhex('00a201')]),(0x8a,[b'\0'])]:require([b for k,_,b in obj.records if k==kind]==expected,'Exact header/group/directive/noentry')
 require({n:p.offset for n,p in obj.publics.items()}==PUBLICS and all((p.segment,p.group,p.type_index)==(1,1,0)for p in obj.publics.values()),'Five genuine exact typed-width labels in DGROUP, no alias/partial PUBLIC')
 data=bytearray()
 for at,b in s.chunks:
  require(bool(b)and at==len(data)and at+len(b)<=12,'No hole/overlap/crop/tail');data.extend(b)
 require(len(data)==12,'Complete allocation including each odd-offset field')
 return bytes(data),{'boundary':'complete_asm_DATA_SEGDEF','segment':{'index':1,'name':'_DATA','class_name':'DATA','length':12,'attributes':72},'publics':[asdict(obj.publics[n])for n in PUBLICS],'group':{'index':1,'name':'DGROUP','segments':[1]},'source_field_widths':[1,4,2,4,1],'source_field_offsets':[0,1,5,7,11],'all_initialized_bytes':12,'emitted_mz_sites':[],'fixups':[],'authored_c_credit':0,'function_credit':0,'original_global_MAP_proved':False}
def extract_data(raw):
 require(type(raw)is bytes and H(raw)in OBJECT_HASHES,'Pinned complete unchanged source OMF required')
 return validate_object(read_omf(raw))
@dataclass(frozen=True)
class Build:
 object_bytes:bytes
 data:bytes
 metadata:dict
 provenance:dict

def _assemble_source(source):
 source=Path(source);content=source.read_bytes();assert source.parent.resolve()==D.resolve()
 # Only the two exact meaningful typed scalar sources are admitted.
 expected={'platform_state_grouped.asm': '3a3f99be136f1dcf6689a67de50ca9807b4d9f65acdb28e1d28de775da14b176', 'wrong_speed_grouped.asm': 'd4f6c582c5f388b4cba82fc4e9d7c6400f2ddfa02f5174954d7f37e5d2b327ff'}
 assert source.name in expected and H(content)==expected[source.name]
 tools=M/'toolchains/msc510';paths={'assembler':tools/'MASM.EXE','manifest':tools/'manifest.json','license':tools/'LICENSE','config':M/'config/msc510.json'}
 expected={'assembler':pinned.MASM_SHA256,'manifest':pinned.MANIFEST_SHA256,'license':pinned.LICENSE_SHA256,'config':pinned.CONFIG_SHA256}
 for key,p in paths.items():assert H(p.read_bytes())==expected[key],key
 command='T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;'
 with tempfile.TemporaryDirectory(prefix='input-masm-')as scratch:
  p=Path(scratch);(p/'UNIT.ASM').write_bytes(content)
  batch='@echo off\r\n'+command+' > MASM.LOG\r\nif errorlevel 1 goto failed\r\necho assembled > RESULT.TXT\r\ngoto done\r\n:failed\r\necho failed > RESULT.TXT\r\n:done\r\nexit\r\n';(p/'RUN.BAT').write_bytes(batch.encode('ascii'))
  conf='[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(p)+'"\nmount t "'+str(tools)+'" -ro\nc:\nRUN.BAT\n';(p/'dosbox.conf').write_text(conf)
  result=subprocess.run(['dosbox','-conf',str(p/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=60)
  log=(p/'MASM.LOG').read_text(encoding='cp437');listing=(p/'UNIT.LST').read_text(encoding='cp437')
  assert result.returncode==0 and(p/'RESULT.TXT').read_text().strip()=='assembled',log
  assert re.search(r'\b0 Warning Errors',log)and re.search(r'\b0 Severe\s+Errors',log),log
  raw=(p/'UNIT.OBJ').read_bytes()
 for key,p in paths.items():assert H(p.read_bytes())==expected[key]
 assert source.read_bytes()==content
 return raw,dict(source_sha256=H(content),assembler_sha256=expected['assembler'],assembler_manifest_sha256=expected['manifest'],assembler_license_sha256=expected['license'],assembler_config_sha256=expected['config'],command=command,assembler_log=log,assembler_listing=listing,object_sha256=H(raw),dosbox_conf=conf,batch=batch,stdout=result.stdout.decode('utf-8','replace'),stderr=result.stderr.decode('utf-8','replace'),fresh_scratch=True,generation_target_inputs=False,generation_placement_inputs=False)

def assemble(source,unit,nasm=None):
 validate_unit(unit);source=Path(source);require(source.resolve()==(M/unit['source']).resolve()and not source.is_symlink(),'Exact source path')
 require(H(source.read_bytes())==unit['source_sha256'],'Source pin mismatch')
 raw,provenance=_assemble_source(source);data,metadata=extract_data(raw)
 require(provenance['source_sha256']==unit['source_sha256'],'Generation source changed')
 provenance=provenance|{'build_command':provenance['command'],'object_format':'OMF16','compiler':'Microsoft Macro Assembler5.10','fresh_directory':True,'assembler_configuration_sha256':provenance['assembler_config_sha256'],'deterministic_source_name':'UNIT.ASM','generation_target_input':False,'generation_original_placement_input':False}
 return Build(raw,data,metadata,provenance)
