"""One exact CRT88 runtime result, preserving all ordinary rows and order."""
from cohort import need
import re
UNIT_ID='runtime_data_crt0_s3';NATIVE_START=0x61578;NATIVE_MZ=0x61580

def merge_one_crt88(units,ordinary_results,deferred_unit,deferred_result,rea_evidence_id):
 need(deferred_unit['id']==UNIT_ID and deferred_unit['language']=='runtime'and deferred_unit['backend']=='msc500-library'and deferred_unit['runtime_kind']=='initialized_data'and deferred_unit['member']=='CRT0_DATA_3'and deferred_unit['source']=='config/runtime500.json'and int(deferred_unit['image_offset'],0)==NATIVE_START and deferred_unit['size']==88,'sole exact whole CRT0 DATA88 job')
 expected=[u['id']for u in units];ordinary=[u['id']for u in units if u['id']!=UNIT_ID]
 need(expected.count(UNIT_ID)==1 and len(expected)==len(set(expected))and[r['id']for r in ordinary_results]==ordinary,'complete ordinary registry, no extra/missing/duplicate rows')
 need(all(deferred_result.get(k)==v for k,v in deferred_unit.items()),'deferred original unit metadata preserved')
 need(re.fullmatch('[0-9a-f]{64}',str(deferred_result.get('expected_sha256')))and deferred_result['status']=='runtime_matched'and deferred_result['expected_size']==deferred_result['actual_size']==88 and deferred_result['expected_sha256']==deferred_result['actual_sha256']and deferred_result['first_difference']is None,'whole88 actual/native comparison must pass')
 need(deferred_result.get('authored_c_credit')==0,'no C credit from runtime')
 mz=[r['mz_segment_relocation_image_offset']for r in deferred_result.get('relocations',[])if'mz_segment_relocation_image_offset'in r];need(mz==[NATIVE_MZ],'sole complete native BASE16 site61580')
 oldsites={r['mz_segment_relocation_image_offset']for old in ordinary_results for r in old.get('relocations',[])if'mz_segment_relocation_image_offset'in r};need(NATIVE_MZ not in oldsites,'no duplicate preexisting native MZ owner')
 need(isinstance(rea_evidence_id,str)and rea_evidence_id,'complete deferred native primary required')
 byid={r['id']:r for r in ordinary_results};byid[UNIT_ID]=deferred_result;merged=[byid[i]for i in expected];need(all(byid[r['id']]is r for r in ordinary_results),'ordinary row objects retained without mutation')
 return merged,{UNIT_ID:rea_evidence_id}
