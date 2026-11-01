"""Versioned active event-client closure for unchanged genuine near COMMON pointers."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from msc import compile_c
from omf import read_omf
from reference import build_reference,ORIGINAL_SHA256
import event_pointer_source_inputs as legacy
from event_pointer_unsigned_profile_pins import PINS
import event_text_unsigned_context as context
from event_unsigned_runtime_identity import validate_used_fields,ENTRIES
from event_pointer_unsigned_graphs import pointer_graph
BACKEND='msc500-near-common-event-pointers-unsigned-client-v2'
SOURCE=legacy.SOURCE;SOURCE_SHA=legacy.SOURCE_SHA;OBJECT_SHA=legacy.OBJECT_SHA;FLAGS=legacy.FLAGS;MANIFEST_SHA=legacy.MANIFEST_SHA;NAMES=legacy.NAMES
require=legacy.require;sha=legacy.sha;local=legacy.local;validate_object=legacy.validate_object

def validate_item(item):
 require(isinstance(item,dict)and set(item)==legacy.KEYS,'Unsigned event-pointer exact allocation keys')
 require((item['id'],item['backend'],item['source'],item['source_sha256'],item['compiler'],item['flags'],item['toolchain_manifest_sha256'])==('event-pointer-common',BACKEND,SOURCE,SOURCE_SHA,'msc500',FLAGS,MANIFEST_SHA),'Unsigned event-pointer closed producer contract')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES]and all(type(x['size'])is int for x in item['objects']),'Unsigned event-pointer unchanged pair2+2')
 require(item['evidence']==PINS,'Unsigned event-pointer exact versioned evidence')

def validate_evidence(project,pins,target):
 require(pins==PINS,'Unsigned event-pointer exact pins');payload={}
 for key,row in pins.items():
  raw=local(project,row['path']).read_bytes();require(sha(raw)==row['sha256'],'Unsigned event-pointer changed evidence: '+key);payload[key]=raw
 legacy_rows={key[len('legacy_'):]:row for key,row in pins.items()if key.startswith('legacy_')}
 require(legacy_rows==legacy.PINS,'Unsigned event-pointer historical foundation changed')
 # Explicit historical foundation only. The active source/selection closure is
 # independently checked below; these old frozen consumers are never called active.
 constraints,compiler=legacy.validate_evidence(project,legacy.PINS,target)
 proof=json.loads(payload['active_closure']);require(proof['schema']==1 and proof['classification']=='actual unsigned event plus current main active pointer clients; historical foundation separate','Unsigned active closure schema')
 require(sha(payload['active_event_source'])==context.pins.SOURCE_SHA256 and sha(payload['active_event_object'])==context.pins.OBJECT_SHA256,'Unsigned active genuine source/object mismatch')
 event=context.validate_object(read_omf(payload['active_event_object']));main=read_omf(payload['active_main_object']);provider=read_omf(payload['producer_object']);validate_object(payload['producer_object'])
 require(sha(payload['active_main_source'])==proof['main_source_sha256']and sha(payload['active_main_object'])==proof['main_raw_sha256'],'Unsigned active main source/raw mismatch')
 cfg=json.loads(local(project,'config/units.json').read_text());require(isinstance(cfg,list),'Unsigned active unit registry shape')
 active=[u for u in cfg if u.get('source')==context.SOURCE];require({u['id']for u in active}==set(context.profile()['unit_contracts'])and len(active)==3,'Unsigned active exact3 selected event rows')
 require(not any(u.get('source')=='src/event_text_match.c'for u in cfg),'Historical signed event source must not remain selected')
 for unit in active:context.validate_unit(unit);validate_used_fields(event,unit)
 mainrows=[u for u in cfg if u.get('source')=='src/main_input_exit_match.c'];require(sorted(u['id']for u in mainrows)==sorted(proof['main_selected_ids']),'Unsigned active main selected ownership changed')
 actualgraphs={'provider':{n:pointer_graph(provider,n)for n in NAMES},'event':{n:pointer_graph(event,n)for n in NAMES},'main':{'_current_event':pointer_graph(main,'_current_event')}}
 require(actualgraphs==proof['graphs']and actualgraphs['provider']==actualgraphs['event']and actualgraphs['main']['_current_event']==actualgraphs['provider']['_current_event'],'Unsigned active complete near-pointer pointee graphs mismatch')
 require(actualgraphs['provider']['_event_context']['to']['struct_bits']==96 and actualgraphs['provider']['_current_event']['to']['struct_bits']==160,'Unsigned observed pointee prefix extents changed')
 fields=[]
 for label,obj in [('main',main),('event',event),('provider',provider)]:
  for f in obj.fixups:
   if f.target[0]==2 and obj.externals.get(f.target[1])in NAMES:fields.append({'client':label,'segment':f.segment,'class':obj.segments[f.segment].class_name,'offset':f.offset,'width':f.width,'location_type':f.location_type,'target':obj.externals[f.target[1]]})
 require(fields==proof['pointer_fields']and sum(f['class']=='CODE'for f in fields)==9 and sum(f['class']=='DEBSYM'and f['client']!='provider'for f in fields)==3 and sum(f['client']=='provider'for f in fields)==2,'Unsigned active all9 CODE/3clientDEBUG/2providerDEBUG fields changed')
 control=json.loads(payload['actual_unsigned_comparison']);gen=json.loads(payload['actual_unsigned_generation']);outer=json.loads(payload['actual_unsigned_outer']);compouter=json.loads(payload['actual_unsigned_comparison_outer'])
 require(control['status']=='PASS_GENUINE_UNSIGNED_WHOLE_TU_TYPED_NATIVE_IDENTITY'and control['all208native_equal']and control['typed_source_callee_imports']==['__aNuldiv','__aNulrem']and control['whole_raw_sha256']==context.pins.OBJECT_SHA256,'Unsigned actual complete C5/native/type proof changed')
 require(gen['status']=='COMPLETE'and gen['actual_C5_calls']==1 and gen['guard_closed']and gen['raw_whole_object_sha256']==context.pins.OBJECT_SHA256 and gen['source_sha256']==context.pins.SOURCE_SHA256 and len(gen['blocked_probes'])==20,'Unsigned actual source generation closure changed')
 require(outer['terminal']and outer['reaped']and outer['exit_code']==0 and compouter['terminal']and compouter['exit_code']==0 and compouter['tool_chunk']=='828e2c'and compouter['GEN_retries']==0 and compouter['comparison_sha256']==pins['actual_unsigned_comparison']['sha256'],'Unsigned actual root terminal closure required')
 require(proof['runtime_entries']==ENTRIES,'Unsigned authentic runtime identity table changed')
 ref=build_reference(Path(target).read_bytes())
 for entry in ENTRIES.values():
  ev=json.loads(payload['runtime_'+entry['member']]);v=ev['normalized_result'];profile=ev['analysis_profile']['parameters'];at=entry['offset'];size=entry['bytes']
  require(ev['operation']=='read_bytes'and ev['subject']['digest']['sha256']==ORIGINAL_SHA256 and profile['load_segment']=='0x1000'and profile['language_id']=='x86:LE:16:Real Mode'and ev['parameters']=={'address':hex(0x10000+at),'length':size}and v['complete']and v['requested_bytes']==v['returned_bytes']==size,'Unsigned exact native runtime primary identity changed')
  require(bytes.fromhex(v['bytes_hex'])==ref['image'][at:at+size]and not any(at<=x<at+size for x in ref['relocations']),'Unsigned whole native runtime bytes/MZ changed')
 return constraints,compiler

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();require(not any(x in str(project)for x in ['\r','\n','"']),'Unsafe unsigned event-pointer project path')
 source=local(project,SOURCE);require(source==project/SOURCE and source.resolve()==source,'Unsigned event-pointer source alias');before=source.read_bytes();require(sha(before)==SOURCE_SHA,'Unsigned event-pointer producer source changed')
 c=(compile_c if compiler_fn is None else compiler_fn)(source,FLAGS,compiler='msc500',source_name='UNIT.C')
 require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','Unsigned fresh producer provenance changed')
 definitions=validate_object(c.object_bytes);constraints,frozen=validate_evidence(project,item['evidence'],target);require(c.tool_hashes==frozen['tool_hashes']and list(c.command)==frozen['command'],'Unsigned producer tools/command changed')
 output=Path(output);output.mkdir(parents=True,exist_ok=True);objpath=output/'event-pointer-common.obj';objpath.write_bytes(c.object_bytes);provenance=asdict(c);provenance.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(objpath),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':4,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':provenance,'allocation_profile':'two near typed pointers; actual unsigned-event/current-main active clients, historical foundation separate','historical_allocation_choice_unique':False,'larger_aggregate_ownership_unknown':True,'authored_C_function_credit':0}
