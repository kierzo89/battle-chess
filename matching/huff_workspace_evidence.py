"""Comparison-only owned Huff native/physical evidence closure; never generation input."""
from pathlib import Path
import json,hashlib
from reference import ORIGINAL_SHA256,validate_expanded_read,validate_data_address
from huff_workspace_omf16 import need
PINS={'evidence/huff-workspace5120/REA-zero5120.json': '14b8428a2bb95d1171feece97294e823bee76c62b5c5600e10f5294f9dc2d77b', 'evidence/huff-workspace5120/actual245-actual-root-tool-result.json': '4c7f16f72d3ce15be54cb7dd7ce77c8b4e477b558bf935e3bf739c73369321fe', 'evidence/huff-workspace5120/actual245-aggregate-result.json': 'c0e43a2645bb86cba587429c95f60ee63eff2a9c72c92afb64e1647d1952d995', 'evidence/huff-workspace5120/actual245-all77-field-comparison.json': '4adff7fdfbf1f554483a6f9d32fa56d69b17e31ef7b68bf808293e90dbb72760', 'evidence/huff-workspace5120/actual245-outer-LINK-tool-result.json': '22e503ee49c1c373c65404c9ff9d314767235854a3c49a725ce245ec3cb6ed86', 'evidence/huff-workspace5120/all-current-client-fields.json': 'b7002159c7143e808dbe1bd5b5942ef877bdd24b7eb77d270d2882405f91cac6', 'evidence/huff-workspace5120/ownership-and-boundaries.json': '867b2f47de5a5483c9d4d25abe444ab9c220a82cc1aea2dd9c4967f20156289f', 'evidence/huff-workspace5120/packet-coverage.json': '478cc31559f6e887466f5051ccdb529d8d2fa9b3b70d80d597478321a0d288ed'}
def validate_data(unit,project,target_sha256,reference):
 project=Path(project).resolve();need(target_sha256==ORIGINAL_SHA256 and reference is not None,'pinned native original reference')
 records={}
 for rel,h in PINS.items():
  p=(project/rel).resolve();need(p.is_relative_to(project)and p.is_file()and not p.is_symlink(),'owned comparison path');b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==h,'owned comparison evidence pin '+rel);records[rel]=json.loads(b)
 A=0x5fcec;Z=0x610ec;data=reference['image'][A:Z];need(len(data)==5120 and not any(data),'complete physical zero component');need(not any(s<Z and s+2>A for s in reference['relocations']),'no native MZ/crossing')
 validate_data_address({'data_address':{'segment':0x5cc2,'offset':0x30cc},'image_offset':'0x5fcec','size':5120},reference)
 owned=records['evidence/huff-workspace5120/ownership-and-boundaries.json'];need(owned['native_image_range']==[A,Z]and owned['DS_range']==[0x30cc,0x44cc]and owned['opaque_tail']['bytes']==2048 and owned['existing_named_providers']==[],'exact native views/opaque tail provenance')
 packet=records['evidence/huff-workspace5120/packet-coverage.json'];need(sum(r['overlap_bytes']for r in packet['packets'])==5120 and packet['original_OMF_literal_vs_reservation_proven']is False,'whole shipped packet coverage, original storage history held')
 fields=records['evidence/huff-workspace5120/all-current-client-fields.json'];need(fields['count']==10 and len(fields['fields'])==10,'whole selected client ten fields')
 validate_link(project)
 return validate_expanded_read(records[unit['rea_evidence']],unit,data,reference,emitted_mz_sites=[])

def validate_link(project):
 project=Path(project).resolve();records={};prefix='evidence/huff-workspace5120/actual245-'
 for rel,h in PINS.items():
  if not rel.startswith(prefix):continue
  path=(project/rel).resolve();need(path.is_relative_to(project)and not path.is_symlink(),'owned actualLINK proof path');b=path.read_bytes();need(hashlib.sha256(b).hexdigest()==h,'actualLINK proof checksum');records[rel[len(prefix):]]=json.loads(b)
 p=records['all77-field-comparison.json'];r=records['aggregate-result.json'];o=records['outer-LINK-tool-result.json']
 need(p['status']=='ACTUAL_EXPLICIT_DGROUP_CALLER245_ALL77_PASS_DIAGNOSTIC_ONLY'and p['actual_objects']==245 and p['actual_undefined']==113 and len(p['all77_actual_field_proof'])==77 and len(p['fields'])==10,'closed diagnostic all77 actual proof')
 need(p['ten_corrected_old64byte_errors']==10 and p['other67_raw_and_actual_values_unchanged']==67 and p['unresolved_Huff_fields_observed_not_invented']==0 and all(f['frame']==[1,1]and f['matches_DGROUP']is True for f in p['fields']),'all10 actual group-frame words and67 others')
 need(p['raw_PUBLIC_group']==0 and p['real_DGROUP_member']==1 and p['provider_whole_initialized_bytes']==5120 and p['opaque_physical_tail2048_capacity_unknown']is True and p['native_absolute_placement_or_whole_native_CODE_claim']is False,'preserve actual PUB0/logical limits')
 need(o['exit_code']==0 and o['terminal']is True and o['reaped']is True and r['objects_count']==245 and r['LINK_calls']==1 and r['process']['returncode']==0 and r['process']['reaped']is True and r['actual_missing_count']==113 and r['adoption']is False,'real closed diagnostic LINK, no admission')
 need(p['aggregate_result_sha256']==hashlib.sha256((project/(prefix+'aggregate-result.json')).read_bytes()).hexdigest()and p['outer_receipt_sha256']==hashlib.sha256((project/(prefix+'outer-LINK-tool-result.json')).read_bytes()).hexdigest(),'cross-bound actual receipts')
 return p
