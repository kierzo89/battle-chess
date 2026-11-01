"""Closed real near-CODE helper identities; applied only to actual used event fields."""
from omf import OMFError
ENTRIES={'_atol':{'offset':0xfb0e,'member':'ATOL','bytes':3,'arithmetic':'signed-long-from-string'},'__aNldiv':{'offset':0xf87c,'member':'LDIV','bytes':163,'arithmetic':'signed-long-quotient'},'__aNuldiv':{'offset':0xf39c,'member':'ULDIV','bytes':101,'arithmetic':'unsigned-long-quotient'},'__aNulrem':{'offset':0xf402,'member':'ULREM','bytes':109,'arithmetic':'unsigned-long-remainder'}}
EVENT_IDS={'wait_exit_event_5d48','wait_pointer_event_5d7a','decimal_digits_5dca'}
def require(ok,message):
 if not ok:raise OMFError(message)
def validate_used_fields(obj,unit):
 require(unit.get('id')in EVENT_IDS,'Unsigned runtime identity only supports the three reviewed event units')
 symbol=unit.get('symbol');info=obj.function_info(symbol);seg=obj.segments[info['segment']];body=bytearray()
 for at,b in seg.chunks:require(at==len(body),'Unsigned helper CODE hole/overlap');body.extend(b)
 used=[];consumed=set()
 for f in obj.fixups:
  if f.segment!=info['segment']or not(info['offset']<=f.offset and f.offset+f.width<=info['end'])or f.target[0]!=2:continue
  name=obj.externals.get(f.target[1]);require(name is not None,'Unsigned helper undefined EXTDEF')
  if name!='_atol'and not name.startswith('__aN'):continue
  require(name in ENTRIES,'Unsupported or incorrectly signed runtime helper: '+name)
  entry=ENTRIES[name];binding=unit.get('externals',{}).get(name)
  require(type(binding)is int and binding==entry['offset'],'Runtime helper name/native identity mismatch: '+name)
  require((f.width,f.location_type,f.segment_relative,f.frame,f.target[0],f.displacement)==(2,1,False,(5,None),2,None),'Runtime helper requires genuine near relative CALL field')
  require(f.offset>0 and body[f.offset-1]==0xe8 and body[f.offset:f.offset+2]==b'\0\0','Runtime helper actual near CALL/zero source operand required')
  used.append({'symbol':name,'native_offset':binding,'actual_CODE_field':f.offset,'function_field':f.offset-info['offset'],'member':entry['member'],'whole_member_bytes':entry['bytes'],'arithmetic':entry['arithmetic']});consumed.add(name)
 expected={'__aNuldiv','__aNulrem'}if unit['id']=='decimal_digits_5dca'else set()
 require(consumed==expected and len(used)==len(expected),'Reviewed event helper use set changed')
 unused={n:v for n,v in unit.get('externals',{}).items()if(n=='_atol'or n.startswith('__aN'))and n not in consumed}
 return {'used_real_helpers':used,'unused_metadata_bindings':unused,'unused_metadata_is_not_callee_ownership_proof':True,'scope':'three event units only; no global name normalization'}
