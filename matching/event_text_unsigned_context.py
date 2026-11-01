"""Exact whole genuine event CODE208/threeCVs and typed helper source context."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from omf import OMFError,read_omf
import event_text_unsigned_pins as pins
from event_unsigned_runtime_identity import validate_used_fields
SOURCE='src/event_text_unsigned_match.c';FLAGS=['/AS','/Gs','/Os','/Zi']
def require(v,s):
 if not v:raise OMFError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def normalized(x):
 if isinstance(x,dict):
  require(all(type(k)in(int,str)for k in x),'Unsigned context key type');require(len({str(k)for k in x})==len(x),'Unsigned context duplicate normalized key');return {str(k):normalized(v)for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [normalized(v)for v in x]
 return x
def canonical(x):return json.dumps(normalized(x),sort_keys=True,separators=(',',':'))
def snapshot(obj):
 return {'records':[{'kind':k,'offset':a,'payload_hex':b.hex()}for k,a,b in obj.records],'names':obj.names,'externals':obj.externals,'publics':{k:asdict(v)for k,v in obj.publics.items()},'procedures':obj.procedures,'data_writes':obj.data_writes,'segments':{i:{**{k:v for k,v in asdict(s).items()if k!='chunks'},'chunks':[[a,b.hex()]for a,b in s.chunks]}for i,s in obj.segments.items()},'fixups':[{**asdict(f),'raw':f.raw.hex()}for f in obj.fixups]}
def profile():
 raw=Path(__file__).with_name('event_text_unsigned_profile.json').read_bytes();require(sha(raw)==pins.PROFILE_SHA256,'Unsigned context profile SHA');return json.loads(raw)
def validate_object(obj):
 p=profile();require(canonical(snapshot(obj))==canonical(p['object_snapshot']),'Unsigned complete raw/CV/TYPE/field fingerprint mismatch');return obj
FIELDS=['id','image_offset','size','language','backend','source','symbol','flags','externals']
def validate_unit(unit):
 p=profile();expected=p['unit_contracts'].get(unit.get('id'));require(expected is not None,'Unsigned context unknown selected unit');require(all(unit.get(k)==expected[k]for k in FIELDS),'Unsigned context exact unit/source/helper contract changed');return expected

def validate_compiled(unit,compiled,project):
 validate_unit(unit);source=Path(project)/SOURCE;require(source.resolve()==source and sha(source.read_bytes())==pins.SOURCE_SHA256,'Unsigned active source changed/aliased')
 require(compiled.source_sha256==pins.SOURCE_SHA256 and compiled.compiler=='msc500'and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'and compiled.toolchain_manifest_sha256==pins.MANIFEST_SHA256,'Unsigned fresh compiler provenance changed')
 require(sha(compiled.object_bytes)==pins.OBJECT_SHA256,'Unsigned whole genuine compiler object changed');obj=validate_object(read_omf(compiled.object_bytes));used=validate_used_fields(obj,unit)
 return {'whole_CODE_bytes':208,'complete_CV_procedures':3,'raw_fields':25,'loaded_DATA_CONST_BSS':0,'actual_helper_identity':used,'genuine_source_sha256':pins.SOURCE_SHA256,'whole_object_sha256':pins.OBJECT_SHA256,'matching_credit_added':0}
