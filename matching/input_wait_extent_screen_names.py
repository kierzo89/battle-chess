"""Fixed1DA9 restored605/607-byte native body and exact source-owned CV607.

Only the coupled real2322-byte contribution is supported; standalone53-field
controls and invented internal-call relocations remain inadmissible.
"""
import json
from pathlib import Path
from extent import _evidence,_number
from reference import build_reference,ORIGINAL_SHA256,CARRIER_SHA256
from input_wait_context_screen_names import _hash,_profile,_raw,native,validate_source_context
from input_wait_native_specs import NATIVE,FALSE_SOURCES,INSTRUCTIONS,BODY_SHA,NEXT_SHA
START=0x11da9;END=0x12008;SIZE=607
FIELDS={'kind','original_raw_evidence','expanded_raw_evidence','expanded_body_evidence','original_next_evidence','expanded_next_evidence','original_partial_evidence','original_false_xrefs_evidence','expanded_false_xrefs_evidence','original_gap_xrefs_evidence','expanded_gap_xrefs_evidence','expanded_instruction_evidence','original_instruction_evidence'}
MZ={0x1ddb,0x1dfe,0x1e18,0x1e37,0x1e90,0x1eaa,0x1fa6,0x1fc0}

def validate_input_wait_extent(unit,project,target_sha256,emitted,linked,source_object=None):
 m=unit.get('extended_extent')
 if(not isinstance(m,dict)or set(m)!=FIELDS or m['kind']!='input_wait_screen_names_1da9_v2'
    or target_sha256!=ORIGINAL_SHA256 or unit.get('id')!='input_wait_1da9'or unit.get('symbol')!='_input_wait_1da9'
    or unit.get('language')!='c'or unit.get('backend')!='msc500-omf'or unit.get('flags')!=['/AS','/Zi']
    or unit.get('code_address')is not None or _number(unit.get('image_offset'))!=0x1da9 or unit.get('size')!=SIZE
    or unit.get('externals',{}).get('__chkstk')!=0xecaa):raise ValueError('unsupported fixed input-wait extent identity')
 specs={'original_raw_evidence':(ORIGINAL_SHA256,'read_bytes',1),'expanded_raw_evidence':(CARRIER_SHA256,'read_bytes',1),
 'expanded_body_evidence':(CARRIER_SHA256,'analyze_function',1),'original_next_evidence':(ORIGINAL_SHA256,'analyze_function',1),
 'expanded_next_evidence':(CARRIER_SHA256,'analyze_function',1),'original_partial_evidence':(ORIGINAL_SHA256,'analyze_function',3),
 'original_false_xrefs_evidence':(ORIGINAL_SHA256,'xrefs',3),'expanded_false_xrefs_evidence':(CARRIER_SHA256,'xrefs',3),
 'original_gap_xrefs_evidence':(ORIGINAL_SHA256,'xrefs',2),'expanded_gap_xrefs_evidence':(CARRIER_SHA256,'xrefs',2),
 'expanded_instruction_evidence':(CARRIER_SHA256,'inspect_native_instruction',7),'original_instruction_evidence':(ORIGINAL_SHA256,'inspect_native_instruction',2)}
 orig=_evidence(project,unit['rea_evidence'],ORIGINAL_SHA256,'analyze_function');all_e=[orig];es={}
 for key,(sha,op,count)in specs.items():
  paths=m[key]if count>1 else[m[key]]
  if not isinstance(paths,list)or len(paths)!=count:raise ValueError('input-wait requires every fixed independent native observation')
  ev=[_evidence(project,p,sha,op)for p in paths];all_e.extend(ev);es[key]=ev if count>1 else ev[0]
 if len({e['evidence_id']for e in all_e})!=len(all_e):raise ValueError('input-wait requires distinct independent evidence IDs')
 for e in all_e:_profile(e)
 native(orig,'rea_input_wait_1da9_original.json')
 native(es['expanded_body_evidence'],'rea_input_wait_1da9_expanded.json',True)
 for e,name in zip(es['original_partial_evidence'],['rea_input_wait_false_1ef0_original.json','rea_input_wait_false_11f0e_original.json','rea_input_wait_false_12002_original.json']):native(e,name)
 native(es['original_next_evidence'],'rea_choose_action_2008_original.json',True)
 native(es['expanded_next_evidence'],'rea_input_wait_next_2008_expanded.json',True)
 ref=build_reference((Path(project).parent/'CHESS.EXE').read_bytes());raw=ref['image'][0x1da9:0x2079]
 if(len(raw)!=720 or _hash(raw[:607])!=BODY_SHA or _hash(raw[607:])!=NEXT_SHA
    or not isinstance(linked,bytes)or linked!=raw[:607]or {s for s in ref['relocations']if 0x1da9<=s<0x2079}!=MZ):raise ValueError('input-wait fixed original full720/body607/next113/MZ differs')
 _raw(es['original_raw_evidence'],START,720,raw);loaded=bytearray(raw)
 for site in MZ:off=site-0x1da9;loaded[off:off+2]=((int.from_bytes(loaded[off:off+2],'little')+0x1000)&65535).to_bytes(2,'little')
 _raw(es['expanded_raw_evidence'],START,720,bytes(loaded))
 for index,(address,sources)in enumerate(FALSE_SOURCES.items()):
  old=es['original_false_xrefs_evidence'][index];new=es['expanded_false_xrefs_evidence'][index]
  if(old['parameters']!={'address':hex(address)}or new['parameters']!={'address':hex(address)}
     or sorted(_number(a)for a in old['normalized_result'])!=sources or new['normalized_result']!=[]):raise ValueError('input-wait complete44 false FAR aliases or expanded empty xrefs differ')
  expected={0x11ef0:'9a0000ef11',0x11f0e:'9a1e00ef11',0x11fa9:'9ab900ef11'}[address]
  for source in sources:
   at=source-0x10000;call=ref['image'][at:at+5]
   if(call.hex()!=expected or at+3 not in ref['relocations']
      or 0x10000+16*int.from_bytes(call[3:5],'little')+int.from_bytes(call[1:3],'little')!=address+0x10000
      or START<=address+0x10000<END):raise ValueError('input-wait false FAR alias lacks exact loader arithmetic')
 for key in ['original_gap_xrefs_evidence','expanded_gap_xrefs_evidence']:
  for e,address in zip(es[key],[0x11eb8,0x11eb9]):
   if e['parameters']!={'address':hex(address)}or e['normalized_result']!=[]:raise ValueError('input-wait both dead gap bytes need empty original/expanded global xrefs')
 for key,target,addresses in[('expanded_instruction_evidence','expanded',['11ef0','11f0e','11fa8','11fa9','12002','11eb5','11eb8']),('original_instruction_evidence','original',['11eb5','11eb8'])]:
  for e,address in zip(es[key],addresses):
   expected=INSTRUCTIONS['rea_input_wait_'+target+'_instruction_'+address+'.json'];n=e['normalized_result']
   if e['parameters']!={'address':'0x'+address}or {k:n.get(k)for k in expected}!=expected:raise ValueError('input-wait exact decoded/interior/unknown-gap observation differs')
   if n['status']=='decoded':
    at=int(address,16)-START
    if linked[at:at+n['length']].hex()!=n['bytes']:raise ValueError('input-wait decoder bytes differ from actual linked code')
 if(linked[0x1eb8-0x1da9:0x1eba-0x1da9]!=bytes.fromhex('eb20')or 0x11eb8+2+0x20!=0x11eda
    or linked[-6:].hex()!='5e5f8be55dc3'):raise ValueError('input-wait exact raw dead break arithmetic/completeepilogue differs')
 if(not isinstance(emitted,dict)or emitted.get('symbol')!=unit['symbol']or emitted.get('boundary')!='codeview3_procedure'
    or emitted.get('segment')!=1 or emitted.get('offset')!=175 or emitted.get('size')!=607 or emitted.get('end')!=782
    or not isinstance(emitted.get('fixups'),list)or len(emitted['fixups'])!=51):raise ValueError('input-wait requires actual coupled fullCV607@175 and51 real compiler fields')
 context=validate_source_context(unit,project,emitted,linked,source_object,ref)
 ids=[e['evidence_id']for e in all_e]+context['raw_context_evidence_ids']
 if len(set(ids))!=len(ids):raise ValueError('input-wait native and source-owned context observations must be distinct')
 return {'kind':m['kind'],'span_bytes':607,'reachable_body_bytes':605,'closed_cfg_blocks':40,'gap_bytes':2,'dead_branch_hex':'eb20','false_far_aliases':44,'body_sha256':BODY_SHA,'next_complete_body_bytes':113,'next_complete_body_sha256':NEXT_SHA,'compiler_fixups':51,'mz_relocations':sorted(MZ),'source_owned_context':context}
