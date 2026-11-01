"""Pure reconstructed RAM layout model. No generation, payload serialization or fallback."""
from pathlib import Path
import json,hashlib,re
D=Path(__file__).resolve().parent
def validate(spec):
 assert spec['schema']=='opaque-native-near-BSS-machineview-v1'and spec['native_clear']==[0x52cc,0xcbe0]and spec['private_C_BSS']==[0x52cc,0x52d0]and spec['early_bank']==[0x52d0,0x52ea]and spec['late_bank']==[0x52f0,0xcbe0]
 rows=spec['PUBLICs'];assert len(rows)==190 and len({q['symbol']for q in rows})==190 and sum(q['role']=='existing_typed_COMMON_view'for q in rows)==142 and sum(q['role']=='native_machine_address_view'for q in rows)==48;assert not({q['symbol']for q in rows}&set(spec['reserved_runtime_symbols_never_exported']))
 for q in rows:
  assert re.fullmatch(r'_[A-Za-z0-9_]+',q['symbol']);a=q['native_DS'];assert 0x52d0<=a<0x52ea or 0x52f0<=a<0xcbe0
  e=q['evidence'];assert e['entry_symbol']==q['symbol']and re.fullmatch('[0-9a-f]{64}',e['sha256'])
  if q['role']=='existing_typed_COMMON_view':assert q['logical_view_size']>0 and q['native_interval']==[a,a+q['logical_view_size']]and q['native_interval'][1]<=0xcbe0
  else:assert e['matched_CODE_fields']+e['native_DATA_pointer_fields']+e['direct_original_instruction_fields']>0
 assert sum(q['logical_view_size']for q in rows if q['role']=='existing_typed_COMMON_view')==4978
 actual={a:sorted(q['symbol']for q in rows if q['native_DS']==a)for a in{q['native_DS']for q in rows}};actual={a:n for a,n in actual.items()if len(n)>1};claimed={q['native_DS']:sorted(q['symbols'])for q in spec['coincident_machine_views']};assert actual==claimed and all(q['physical_machine_address_coincidence_independently_observed']and q['not_a_historical_C_alias_union_container_or_capacity_claim']for q in spec['coincident_machine_views']);return spec
def render(spec):
 validate(spec);lines=['; Reconstructed uninitialized native RAM machine views; not historical C objects.','; Extent from CRTclear52CC..CBE0 and originalDOS minimum allocation, not address-gap C capacities.','; Existing C private BSS4 remains outside this module; no initialized bytes or byte credit.','bits 16','cpu 8086',"segment _BSS public align=2 class=BSS use16","segment XOB public align=2 class=BSS use16","segment XO public align=2 class=BSS use16","segment XOE public align=2 class=BSS use16","segment BC_NATIVE_LATE public align=16 class=BSS use16",'group DGROUP _BSS XOB XO XOE BC_NATIVE_LATE']
 for q in sorted(spec['PUBLICs'],key=lambda q:q['symbol']):lines.append('global '+q['symbol'])
 for segment,start,end in[('_BSS',0x52d0,0x52ea),('BC_NATIVE_LATE',0x52f0,0xcbe0)]:
  lines.append('segment '+segment);cursor=start
  for at in sorted({q['native_DS']for q in spec['PUBLICs']if start<=q['native_DS']<end}):
   if at>cursor:lines.append('    resb '+str(at-cursor)+' ; opaque RAM reserve; no per-object capacity claim')
   for q in sorted([q for q in spec['PUBLICs']if q['native_DS']==at],key=lambda q:q['symbol']):lines.append(q['symbol']+': ; native DS '+format(at,'04X')+' machine address')
   cursor=at
  if cursor<end:lines.append('    resb '+str(end-cursor)+' ; complete aggregate CRT-cleared RAM span')
 return ('\n'.join(lines)+'\n').encode('ascii')
def inspect(raw,spec):
 from omf import read_omf,_Cursor
 from dataclasses import asdict
 validate(spec);o=read_omf(raw);want=[(1,'_BSS','BSS',26,72),(2,'XOB','BSS',0,72),(3,'XO','BSS',0,72),(4,'XOE','BSS',0,72),(5,'BC_NATIVE_LATE','BSS',30960,104)];assert [(s.index,s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==want;assert not o.fixups and not o.procedures and not o.externals and all(not s.chunks for s in o.segments.values());assert not any(k in[0xa0,0xa2,0xb0,0xb8]for k,at,p in o.records);assert set(o.publics)=={q['symbol']for q in spec['PUBLICs']}
 for q in spec['PUBLICs']:
  p=o.publics[q['symbol']];early=q['native_DS']<0x52ea;assert(p.group,p.segment,p.offset,p.type_index)==(1,1 if early else 5,q['native_DS']-(0x52d0 if early else 0x52f0),0)
 groups=[]
 for k,at,p in o.records:
  if k==0x9a:
   c=_Cursor(p);name=o.names[c.index()];members=[]
   while c:assert c.byte()==255;members.append(c.index())
   groups.append((name,members))
 assert groups==[('DGROUP',[1,2,3,4,5])];return {'PUBLICs':{n:asdict(p)for n,p in o.publics.items()},'all190_group1_labels':True,'physical_uninitialized_bytes':30986,'initialized_bytes':0,'CODE_bytes':0,'fixups':[],'COMMON_definitions_in_this_object':0,'FILE_C_runtime_MZ_credit':0,'record_kinds':[k for k,at,p in o.records]}
