"""One explicit deferred runtime DATA88 job; no generator and no raw-hole exception."""
from pathlib import Path
from dataclasses import dataclass
import json,hashlib
import crt0_data88_deferred_primitives as p
from reference import ORIGINAL_SHA256,CARRIER_SHA256,validate_expanded_read
POLICY='crt0-data88-literal12-reservation76-deferred-v2';UNIT_ID='runtime_data_crt0_s3';_JOB_TOKEN=object()
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):p.need(v,m)
@dataclass(frozen=True)
class PendingCRT88Job:
 unit_id:str
 rea_evidence_id:str
 project:str
 unit_json:str
 profile_json:str
 config_sha256:str
 rea_sha256:str
 _factory_token:object

def preflight(unit,project,target_sha256,reference):
 """Validate exact unit/member/profile/primary; return pending work, never match."""
 p.validate_unit(unit);project=Path(project).resolve();need(target_sha256==reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'target/reference provenance')
 raw=(project/unit['source']).read_bytes();config=json.loads(raw);need(config['library_sha256']==p.LIB_SHA,'wholeSLIBC config provenance');rows=[r for r in config['members']if r.get('id',r.get('name'))==unit['member']];need(len(rows)==1,'one exact optinCRT0_DATA_3 module');module=rows[0];p.validate_profile(module)
 directory=(project/config['destination']).resolve();need(directory.is_relative_to(project),'runtime source directory escaped');library=(directory/config['library']).read_bytes()if 'library'in config else(directory/'SLIBC.LIB').read_bytes();p.validate_members(library)
 evidence_raw=(project/unit['rea_evidence']).read_bytes();ev=json.loads(evidence_raw);need(H(json.dumps(ev,sort_keys=True).encode())==p.pins()['REA_canonical_sha256'],'exact complete nativeREA88 primary')
 eid=validate_expanded_read(ev,unit,reference['image'][p.START:p.START+88],reference,emitted_mz_sites=p.MZ)
 return PendingCRT88Job(UNIT_ID,eid,str(project),json.dumps(unit,sort_keys=True),json.dumps(module,sort_keys=True),H(raw),H(evidence_raw),_JOB_TOKEN)

def complete(job,aggregate,reference,output):
 """Consume the same-run authenticLINK sealed capability before final report."""
 from closed_aggregate import ClosedAggregateSealV1
 need(type(job)is PendingCRT88Job and job._factory_token is _JOB_TOKEN,'private preflightpending job only')
 need(type(aggregate)is ClosedAggregateSealV1,'exact in-process closed aggregate capability; JSON/fixture ducktyping forbidden');need(aggregate.valid()is True,'closed aggregate validity')
 unit=json.loads(job.unit_json);module=json.loads(job.profile_json);project=Path(job.project);p.validate_unit(unit);p.validate_profile(module)
 need(H((project/unit['source']).read_bytes())==job.config_sha256 and H((project/unit['rea_evidence']).read_bytes())==job.rea_sha256,'preflight inputs unchanged')
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'same original native context')
 need(isinstance(aggregate.run_id,str)and aggregate.run_id and isinstance(aggregate.descriptor_sha256,str)and len(aggregate.descriptor_sha256)==64 and isinstance(aggregate.SOURCE_digest,str)and len(aggregate.SOURCE_digest)==64,'same-run descriptor andSOURCE binding')
 rows=tuple(aggregate.object_rows);source_raws=aggregate.source_raws();need(type(source_raws)is tuple and len(source_raws)==len(rows)>0,'full sealedSOURCE closure')
 contract=[]
 for i,(raw,row)in enumerate(zip(source_raws,rows)):
  need(row['order_slot']==i and row['DOS_name']=='O%03d.OBJ'%i and row['object_sha256']==H(raw)and row['size']==len(raw),'every actualSOURCE identity/order/size')
  contract.append((i,row['DOS_name'],row['object_sha256']))
 library=aggregate.read_artifact('only-slibc/SLIBC.LIB');exe=aggregate.read_artifact('PARTIAL.EXE');mapping=aggregate.read_artifact('PARTIAL.MAP');need(H(library)==p.LIB_SHA,'actualwholeLIB bytes unchanged')
 materialized=p.extract_actual(library,exe,mapping,source_raws,source_contract=tuple(contract));ev=json.loads((project/unit['rea_evidence']).read_text());actual,proof=p.compare_native(materialized,library,unit,module,reference,ev);members,o,d=p.validate_members(library);_,fields=p.literals(o,0x5cc2,0x4958,(0,0xec15));relocations=[]
 for f in fields:
  r={**f,'segment':3,'image_offset':p.START+f['object_offset'],'mode':'base16'if f['object_offset']==8 else'offset16','target_symbol':'__exit'if f['object_offset']==4 else None}
  if r['mz_relocation_image_offset']is not None:r['mz_segment_relocation_image_offset']=r['mz_relocation_image_offset']
  relocations.append(r)
 need([r['mz_segment_relocation_image_offset']for r in relocations if'mz_segment_relocation_image_offset'in r]==[0x61580],'exact nativeMZ one61580')
 need(aggregate.valid()is True,'closed aggregate validity');output=Path(output).resolve();need(output==Path(aggregate.root).resolve().parent/'components/runtime','exact currentrun components/runtime retention, never SOURCE or LINK inputs');output.mkdir(parents=True,exist_ok=True)
 rawpath=output/(UNIT_ID+'.obj');binpath=output/(UNIT_ID+'.bin');need(not rawpath.exists()and not binpath.exists(),'fresh comparison artifacts only');rawpath.write_bytes(members[0].data);binpath.write_bytes(actual)
 result={**unit,'status':'runtime_matched','expected_size':88,'actual_size':88,'expected_sha256':H(reference['image'][p.START:p.START+88]),'actual_sha256':H(actual),'first_difference':None,'expected_byte':None,'actual_byte':None,'source_sha256':job.config_sha256,'classification':'independently_supplied_runtime_library_LINK_materialized_DATA','authored_c_credit':0,'library_sha256':p.LIB_SHA,'member_sha256':p.MEMBER_SHA,'library_member_offset':members[0].offset,'object_sha256':members[0].sha256,'relocations':relocations,'emitted_segment':{'index':3,'length':88,'class_name':'DATA','public':None,'public_offset':None,'literal_initialized_bytes':12,'authentic_LINK_materialized_reservation_bytes':76,'hole_fill_bytes':0,'original_OMF_unchanged':True},'deferred_policy':POLICY,'native_evidence_id':job.rea_evidence_id,'authentic_link_reservation':{'materialization_primitive_proof':materialized.proof,'native_comparison_primitive_proof':proof,'layered_freshness':'Primitive proof itself asserts no process freshness; exact same-run live ClosedAggregateSealV1 above independently proves freshSOURCE→LINK for this accepted runtime row','aggregate_run_id':aggregate.run_id,'descriptor_sha256':aggregate.descriptor_sha256,'SOURCE_digest':aggregate.SOURCE_digest,'actual_LINK_result_sha256':aggregate.link_result_sha256,'SOURCE_objects':len(rows),'same_run_capability':True,'retained_fixture_replay':False},'comparison_object_artifact':str(rawpath),'comparison_data_artifact':str(binpath),'historical_storage_TU_original_MAP_claim':False}
 need(result['expected_sha256']==result['actual_sha256'],'complete native88 equality');return result
