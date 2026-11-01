"""One authoritative ordinary SOURCE -> authentic aggregate LINK -> CRT88 merge.

Only the one explicitly registered policy is supported. All ordinary generator,
comparison, parser, cache and checker accounting paths are preserved.
"""
from pathlib import Path
import json,uuid,hashlib,importlib,sys
from cohort import need,sha,validate_project,select_source_phase
from closed_aggregate import register_fresh_source,close_after_link
from deferred_merge import merge_one_crt88,UNIT_ID
import packet_literal61 as packet
POLICY='crt0-data88-literal12-reservation76-deferred-v2'
class FreshLifecycle:
 def __init__(self,descriptor,project,output,components,observer,seal_factory,link_emitter):
  self.descriptor=descriptor;self.project=Path(project).resolve();self.output=Path(output);self.components=Path(components);self.observer=observer;self.seal_factory=seal_factory;self.link_emitter=link_emitter;self.phase='NEW';self.run_id=uuid.uuid4().hex;self.seal=None;self.link=None;self.receipt=None;self.pending=None;self.adapter=None;self.packet_context=None
 def partition_jobs(self,*,units,project,target_sha256,reference):
  need(self.phase=='NEW'and Path(project).resolve()==self.project,'single lifecycle partition/project')
  need(len(units)==self.descriptor['units']and len({u['id']for u in units})==len(units),'complete exact registry metadata')
  if packet.registration(self.descriptor)is not None:self.packet_context=packet.new_run_context(self,units)
  jobs=self.descriptor['deferred_jobs'];need(len(jobs)==1 and jobs[0]['unit_id']==UNIT_ID and jobs[0]['policy']==POLICY and jobs[0]['adapter_module']=='crt0_data88_deferred','sole closed deferred CRT88 registration')
  registration=jobs[0];matches=[u for u in units if u['id']==UNIT_ID];need(len(matches)==1,'one exact registered runtime unit');unit=matches[0]
  need(sha(json.dumps(unit,sort_keys=True).encode())==registration['unit_sha256'],'whole registered deferred unit fingerprint')
  directory=Path(__file__).resolve().parent/'implementation';module_path=directory/'crt0_data88_deferred.py';need(sha(module_path.read_bytes())==registration['adapter_sha256'],'reviewed adapter code');sys.path.insert(0,str(directory));adapter=importlib.import_module('crt0_data88_deferred');need(Path(adapter.__file__).resolve()==module_path.resolve()and adapter.POLICY==POLICY and adapter.UNIT_ID==UNIT_ID,'exact adapter module origin/API')
  need(Path(adapter.p.__file__).resolve()==(directory/'crt0_data88_deferred_primitives.py').resolve()and sha((directory/'crt0_data88_deferred_primitives.py').read_bytes())==registration['primitive_sha256']and sha((directory/'crt0_data88_deferred_pins.json').read_bytes())==registration['pins_sha256'],'exact adapter primitive/pins closure')
  self.pending=adapter.preflight(unit,self.project,target_sha256,reference);need(type(self.pending)is adapter.PendingCRT88Job and self.pending.unit_id==UNIT_ID and isinstance(self.pending.rea_evidence_id,str)and self.pending.rea_evidence_id,'pending preflight token with complete native primary, no match row')
  need(sha(self.pending.profile_json.encode())==registration['profile_sha256']and self.pending.config_sha256==registration['runtime_config_sha256'],'exact admitted module/config profile');self.adapter=adapter;self.unit_ids=[u['id']for u in units];self.deferred_unit=unit;self.ordinary_ids=[u['id']for u in units if u['id']!=UNIT_ID];self.phase='PARTITIONED_PENDING_CRT88';return[u for u in units if u['id']!=UNIT_ID],[unit]
 def finish_source_phase(self,*,units,ordinary_units,deferred_jobs,results,source_inputs,project,output,reference):
  need(self.phase=='PARTITIONED_PENDING_CRT88'and Path(project).resolve()==self.project and Path(output).resolve()==self.components.resolve(),'single same-run source phase')
  need([u['id']for u in units]==self.unit_ids and[u['id']for u in ordinary_units]==self.ordinary_ids and deferred_jobs==[self.deferred_unit],'exact ordinary/pending partition; no other omitted row')
  need(not self.observer.poisoned and self.observer.current is None and self.observer.roots==[],'all source GEN scopes closed')
  if self.observer.parallel is not None:self.observer.parallel.close(True)
  from source_inputs import report_inputs
  machine_layouts=[]
  if self.descriptor['counts'].get('BSS',0):
   import near_bss_layout16
   machine_layouts=near_bss_layout16.generate(self.descriptor,self.project,self.components)
  need(not self.observer.poisoned and self.observer.current is None and self.observer.roots==[],'machine-layout GEN must close before SOURCE seal')
  source_results=results;packet_pending=[];source_ordinary_ids=self.ordinary_ids
  if self.packet_context is not None:
   source_results,packet_pending=packet.split_source_results(results,self.packet_context);source_ordinary_ids=[i for i in self.ordinary_ids if i not in packet.contracts()]
  rows=select_source_phase(self.descriptor,source_results,report_inputs(source_inputs),self.components,self.project,self.observer.events,expected_ordinary_ids=source_ordinary_ids,machine_layouts=machine_layouts,packet_context=self.packet_context,packet_pending=packet_pending)
  validate_project(self.descriptor,self.project);self.seal=self.seal_factory(self.run_id,rows,'FRESH_INTERMEDIATE_SOURCE_BEFORE_FINAL_REPORT')
  if self.packet_context is not None:packet.bind_before_source(self.packet_context,self.seal,self.observer)
  register_fresh_source(self.seal,self.descriptor,self.observer)
  need(not(self.components/'report.json').exists(),'final report must not predate SOURCE/LINK/deferred comparison');self.write('source-observations.json',self.observer.events);self.write('source-seal.json',{'schema':'source-phase-before-deferred-final-report-v1','run_id':self.run_id,'descriptor_sha256':sha(json.dumps(self.descriptor,sort_keys=True,separators=(',',':')).encode()),'SOURCE_digest':self.seal.digest,'rows':rows,'counts':self.descriptor['counts'],'source_process_count':None,'final_report_required':False,'runtime_OBJ_in_SOURCE':False,'deferred_jobs_pending':[UNIT_ID]})
  self.phase='SOURCE_SEALED';self.link=self.link_emitter(self.seal,self.descriptor,self.project,self.components,self.output/'LINK');self.phase='AGGREGATE_LINK_CLOSED';aggregate=close_after_link(self.seal,self.descriptor,self.output/'LINK',self.link)
  # Postterminal comparison only. It cannot add a SOURCE object or call a generator.
  machine_layout_proof=None
  if machine_layouts:
   import near_bss_layout_post16
   machine_layout_proof=near_bss_layout_post16.complete(aggregate);self.write('machine-layout-comparison.json',machine_layout_proof)
  packet_proof=None
  if self.packet_context is not None:
   completed_packet,packet_proof=packet.complete(self.packet_context,packet_pending,aggregate,reference);results=packet.restore_result_order(results,source_results,completed_packet);self.write('packet-allocation-comparison.json',packet_proof)
  deferred=self.adapter.complete(self.pending,aggregate,reference,self.components/'runtime');aggregate.valid();merged,rea=merge_one_crt88(units,results,self.deferred_unit,deferred,self.pending.rea_evidence_id)
  self.receipt={'schema':'single-generation-deferred-runtime-lifecycle-v1','run_id':self.run_id,'SOURCE_digest':self.seal.digest,'descriptor_sha256':aggregate.descriptor_sha256,'SOURCE_count':len(rows),'SOURCE_process_count':None,'aggregate_SOURCE_LINK_calls':1,'ordinary_runtime_helper_calibration_LINK_calls':None,'total_LINK_process_count':None,'LINK_result_sha256':aggregate.link_result_sha256,'LINK_status':self.link['status'],'undefined_symbols':self.link['undefined_symbols'],'deferred_completed':[UNIT_ID],'deferred_literal_runtime_bytes':12,'deferred_LINK_materialized_runtime_bytes':76,'deferred_physical_runtime_bytes':88,'deferred_C_function_credit':0,'deferred_SOURCE_object_additions':0,'final_report_is_output_only':True,'full_executable_match':False};self.receipt.update({'machine_layout_inputs':machine_layouts,'machine_layout_comparison_sha256':sha(json.dumps(machine_layout_proof,sort_keys=True).encode()),'machine_layout_matching_credit':0}if machine_layouts else{});self.receipt.update({'packet_source_allocation':packet_proof,'packet_alignment_matching_credit':0}if packet_proof is not None else{});self.phase='FINALIZE_ALLOWED';return merged,rea,self.receipt
 def write(self,name,value):
  with(self.output/name).open('x')as f:json.dump(value,f,indent=2);f.write('\n')
