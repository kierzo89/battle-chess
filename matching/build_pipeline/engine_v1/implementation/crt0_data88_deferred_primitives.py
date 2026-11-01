"""Exact CRT0 DATA88 authentic-LINK FILE reservation consumer, never a generator.

Raw twelve literal bytes and seventy-six allocated unwritten bytes stay distinct.
No initialized_view, LEDATA insertion, generic hole/MZ exception or LIDATA tag.
Only primitives here. Runtime matching is permitted solely through the separate same-run typed aggregate adapter. No generation or generic parser changes.
"""
from pathlib import Path
from dataclasses import dataclass
import hashlib,json,re,struct
from omf import read_omf,_Cursor
from library16 import extract_member,link_segment,LibraryError
POLICY='crt0-data88-literal12-reservation76-deferred-v2'
PINS_SHA256='2fa07854a40b6c71b4beecc750c4aa49aaf3b47f5a1f194e45d02fc45a2ff414'
MEMBER_SHA='c8fa9ca0b70762defb91b280d9676eafda5fceb47475344937eb3f281c9a8705'
DAT_SHA='7de3c7cc3fbe49972516b099306c89568daa34f6e46529b2c0ba79ba598952a5'
LIB_SHA='7eabd615308e9a05de24f6e6e82e61a65f733eb64d12b5318d8b3ed569e389b9'
PUBLICS={'__asizds':0,'__atopsp':2,'__aexit_rtn':4,'__abrktb':6,'__abrktbe':86,'__abrkp':86}
START=0x61578;SIZE=88;MZ=[START+8]
class ReservationError(LibraryError):pass
def need(v,m):
 if not v:raise ReservationError('CRT0 DATA88: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pins():
 p=Path(__file__).with_name('crt0_data88_deferred_pins.json');b=p.read_bytes();need(sha(b)==PINS_SHA256,'exact versioned pins');return json.loads(b)
def validate_profile(module):need(module==pins()['profile'],'sole exact opt-in DATA88 profile; no default hole exception')
def validate_unit(unit):need(unit==pins()['unit'],'sole whole88 runtime unit; no slices/credit/foreign metadata')
def validate_structure(o):
 """Strict parsed structure rejection gate; does not fill missing source writes."""
 s=o.segments.get(3);need(s is not None and(s.name,s.class_name,s.attributes,s.length,s.unsupported_data)==('_DATA','DATA',72,88,False),'exact DATA88 SEGDEF')
 need(s.chunks==[(0,bytes(10)),(86,bytes(2))],'exact two genuine literal writes12; reservation76 remains unwritten')
 pubs={n:p.offset for n,p in o.publics.items()if p.segment==3}
 need(pubs==PUBLICS and all(p.group==1 and p.type_index==0 for p in o.publics.values()if p.segment==3),'all six authentic PUBLICs; only existing abrktbe/abrkp alias')
 fs=[f for f in o.fixups if f.segment==3]
 shape=[[f.offset,f.width,f.location_type,f.segment_relative,list(f.frame),list(f.target),f.displacement,f.record_offset,f.raw.hex()]for f in fs]
 need(shape==pins()['DATA_fields']and o.externals.get(8)=='__exit','exact three owned actual FIXUPPs')
 need(not any(k in (0xa2,0xb0,0xb2)for k,_,_ in o.records),'no LIDATA/COMMON change')
 owned={a+i:v for a,data in s.chunks for i,v in enumerate(data)}
 need(set(owned)==set(range(10))|{86,87},'twelve owned source bytes only')
 for f in fs:need(all(f.offset+i in owned for i in range(f.width)),'fixup must own real literal bytes, never reservation')
 return owned,fs
def validate_members(library):
 need(isinstance(library,bytes)and sha(library)==LIB_SHA,'whole unchanged authentic SLIBC')
 p=pins();members=[]
 for name,key,h in [('CRT0','CRT0_row',MEMBER_SHA),('CRT0DAT','CRT0DAT_row',DAT_SHA)]:
  m=extract_member(library,name,LIB_SHA,h);need(m.offset==p[key]['library_offset'],'authentic complete selected member offset');members.append(m)
 o,d=(read_omf(m.data)for m in members);validate_structure(o)
 q=d.publics.get('__exit');need(q is not None and(q.segment,q.offset,q.group,q.type_index)==(1,219,0,0),'genuine CRT0DAT __exit PUBLIC')
 need(d.publics['__cinit'].offset==0,'genuine CRT0DAT base anchor')
 return members,o,d

def parse_actual(exe,map_bytes):
 need(isinstance(exe,bytes)and len(exe)>=28,'actual complete EXE');w=struct.unpack_from('<14H',exe)
 need(w[0]==0x5a4d and w[2]>0 and w[1]<512 and(w[2]-1)*512+(w[1]or 512)==len(exe)and 28<=w[4]*16<=len(exe)and w[12]+4*w[3]<=w[4]*16,'strict full MZ length/header')
 image=exe[w[4]*16:];mz=[struct.unpack_from('<H',exe,w[12]+i*4)[0]+16*struct.unpack_from('<H',exe,w[12]+i*4+2)[0]for i in range(w[3])]
 need(len(mz)==len(set(mz))and all(s+2<=len(image)for s in mz),'actual MZ distinct/bounded')
 text=map_bytes.decode('cp437');parts=text.split('Publics by Name');need(len(parts)==2,'one actual PUBLIC section');part=parts[1].split('Publics by Value')[0];pub={}
 for a,b,n in re.findall(r'^\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+(?:Abs\s+)?(\S+)\s*$',part,re.M):
  need(n not in pub,'no duplicate named PUBLIC');pub[n]=(int(a,16),int(b,16))
 g=re.findall(r'^\s*([0-9A-Fa-f]{4}):0\s+DGROUP\s*$',text,re.M);need(len(g)==1,'one actual DGROUP')
 rows=[(int(a,16),int(n,16),name,klass)for a,z,n,name,klass in re.findall(r'^\s*([0-9A-Fa-f]+)H\s+([0-9A-Fa-f]+)H\s+([0-9A-Fa-f]+)H\s+(\S+)\s+(\S+)\s*$',text,re.M)]
 return image,mz,pub,int(g[0],16),rows,w[4]*16

def literals(o,group,data_offset,exit_place,load=0):
 """Return a twelve-key literal map, never a manufactured contiguous segment."""
 need(type(group)is int and 0<=group<=65535 and type(data_offset)is int and 0<=data_offset<=65536-88 and len(exit_place)==2 and all(type(x)is int and 0<=x<=65535 for x in exit_place),'bounded real placements')
 values,fs=validate_structure(o);rows=[]
 for f in fs:
  add=values[f.offset]|values[f.offset+1]<<8;disp=f.displacement or 0
  if f.offset==4:value=exit_place[0]*16+exit_place[1]-(exit_place[0]*16)+add+disp
  elif f.offset==8:value=((group+load)&65535)+add
  else:value=data_offset+add+disp
  encoded=value&65535;values[f.offset]=encoded&255;values[f.offset+1]=encoded>>8
  rows.append({'object_offset':f.offset,'width':2,'kind':'BASE16'if f.offset==8 else'OFFSET16','frame':list(f.frame),'target':list(f.target),'raw_fixupp':f.raw.hex(),'original_addend':add,'displacement':disp,'encoded_value':encoded,'mz_relocation_image_offset':group*16+data_offset+f.offset if f.offset==8 else None})
 need(len(values)==12,'do not fill reservation in raw source model');return values,rows

def code_identity(o,d,image,pub,group,maprows,mz):
 """Require both actual whole authentic CODE segments and all67 real fields."""
 result=[]
 for z,anchor,rawsha,count in[(o,'__astart',MEMBER_SHA,24),(d,'__cinit',DAT_SHA,43)]:
  need(anchor in pub,'selected member actual CODE anchor');q=z.publics[anchor];base=(pub[anchor][0],pub[anchor][1]-q.offset)
  need(0<=base[1]and base[1]+z.segments[1].length<=65536,'whole CODE within frame')
  placements={1:base,3:(group,pub['__asizds'if z is o else'__acfinfo'][1])}
  if z is d:placements[2]=(group,pub['__fpinit'][1]-2)
  needed={f.target[1]for f in z.fixups if f.segment==1 and f.target[0]==0}|{f.frame[1]for f in z.fixups if f.segment==1 and f.frame[0]==0}
  for index in needed-set(placements):
   candidates=[r for r in maprows if r[2]==z.segments[index].name];need(len(candidates)==1,'unique actual additional CODE frame');placements[index]=(group,candidates[0][0]-group*16)
  for n,p in z.publics.items():
   if p.segment==1:need(pub.get(n)==(base[0],base[1]+p.offset),'all actual CODE PUBLICs from exact member')
  linked,fields=link_segment(z,1,placements,{1:group},{n:pub[n]for n in z.externals.values()if n in pub});where=base[0]*16+base[1]
  need(len(fields)==count and linked==image[where:where+len(linked)],'whole authentic CODE templates and all actual fields')
  actual_sites=sorted(s for s in mz if s<where+len(linked)and s+2>where)
  emitted=sorted(f['mz_relocation_image_offset']for f in fields if f['mz_relocation_image_offset']is not None)
  need(actual_sites==emitted,'whole authentic CODE actual MZ equals all genuine emitted fields')
  result.append({'member':'CRT0'if z is o else'CRT0DAT','raw_sha256':rawsha,'whole_CODE_bytes':len(linked),'all_fields':len(fields),'actual_CODE_start':where})
 need(pub.get('__exit')==(pub['__cinit'][0],pub['__cinit'][1]+219)and pub['__astart'][0]==pub['__cinit'][0],'__exit derives genuine PUBLIC with same actual CODE frame, not numeric alias');return result

@dataclass(frozen=True)
class Materialized:
 actual:bytes
 literal_offsets:tuple
 proof:dict

def extract_actual(library,exe,map_bytes,source_raws,*,source_contract):
 """Primitive only: retained fixtures do not prove a fresh process or earn credit."""
 members,o,d=validate_members(library);image,mz,pub,group,maprows,header=parse_actual(exe,map_bytes)
 need('__asizds'in pub and pub['__asizds'][0]==group,'actual own DATA frame from genuine asizds');start=group*16+pub['__asizds'][1];end=start+88
 need(0<=start and end<len(image),'all88 materially inside FILE before initialized tail; no minalloc substitution')
 for n,off in PUBLICS.items():need(pub.get(n)==(group,pub['__asizds'][1]+off),'six exact actual DATA PUBLIC offsets')
 need(any(name=='_DATA'and klass=='DATA'and a<=start<end<=a+n for a,n,name,klass in maprows),'whole88 contained in actual initialized _DATA output segment')
 expected_names=set(PUBLICS)|{'__exit','__cinit','__astart'}
 need(type(source_raws)is tuple and type(source_contract)is tuple and len(source_raws)==len(source_contract)>0,'exact complete descriptor-sealed SOURCE vector required')
 for i,(raw,row)in enumerate(zip(source_raws,source_contract)):
  need(type(raw)is bytes and row==(i,'O%03d.OBJ'%i,sha(raw)),'exact sealedSOURCE identity/order/rawsha; no arbitrarycountwaiver')
 for raw in source_raws:
  z=read_omf(raw);need(not(expected_names&set(z.publics)),'no competing source PUBLIC provider')
  for kind,record_at,payload in z.records:
   if kind not in(0xb0,0xb8):continue
   cursor=_Cursor(payload)
   def communal_number():
    leaf=cursor.byte()
    if leaf<=0x80:return leaf
    need(leaf in(0x81,0x84,0x88),'bounded communal numeric leaf');return int.from_bytes(cursor.take({0x81:2,0x84:3,0x88:4}[leaf]),'little')
   while cursor:
    name=cursor.name();cursor.index();storage=cursor.byte();need(storage in(0x61,0x62),'real near/far communal class');communal_number()
    if storage==0x61:communal_number()
    need(name not in expected_names,'no competing source COMMON runtime provider')
 code=code_identity(o,d,image,pub,group,maprows,mz);actual=image[start:end];values,fields=literals(o,group,pub['__asizds'][1],pub['__exit'])
 need(all(actual[i]==v for i,v in values.items()),'all12 literal bytes at real three field bindings')
 need(actual[10:86]==bytes(76),'all76 actual FILE reservation bytes zero')
 need(sorted(s-start for s in mz if s<end and s+2>start)==[8],'one actual BASE16 only; reject missing/extra/cross-boundary MZ')
 loads=[]
 for load in(0,1,4096,65535):
  view,_=literals(o,group,pub['__asizds'][1],pub['__exit'],load);loaded=bytearray(actual);loaded[8:10]=((int.from_bytes(loaded[8:10],'little')+load)&65535).to_bytes(2,'little')
  need(all(loaded[i]==v for i,v in view.items())and loaded[10:86]==actual[10:86],'actual four-base literal/reservation split');loads.append(load)
 return Materialized(actual,tuple(sorted(values)),{'primitive_only_not_fresh':True,'actual_range':[start,end],'actual_FILE_range':[header+start,header+end],'actual_group':group,'actual_DATA_offset':pub['__asizds'][1],'actual_exit':pub['__exit'],'all_literal_fields':fields,'actual_MZ':[start+8],'member_sha256':members[0].sha256,'member_library_offset':members[0].offset,'whole_selected_CODE':code,'runtime_physical_span':88,'literal_bytes':12,'authentic_LINK_materialized_reservation_bytes':76,'new_source_storage':0,'four_bases':loads,'C_credit':0,'native_MZ_credit':0})

def compare_native(materialized,library,unit,module,reference,evidence):
 """Compare actual FILE bytes; only three genuine raw fields are normalized."""
 from reference import validate_expanded_read
 validate_unit(unit);validate_profile(module);need(isinstance(materialized,Materialized),'real materialized result required')
 _,o,d=validate_members(library);p=pins();codepara,codebase=p['CRT0DAT_row']['segments']['1'];exitpub=d.publics['__exit'];native_exit=(codepara,codebase+exitpub.offset)
 need(native_exit==(0,0xec15),'__exit native CODE/public-derived placement');native=reference['image'][START:START+88]
 need(len(native)==88 and sorted(s for s in reference['relocations']if s<START+88 and s+2>START)==MZ,'exact one native BASE16/no crossing')
 need(materialized.literal_offsets==tuple(list(range(10))+[86,87]),'exact literal ownership category')
 values,fields=literals(o,0x5cc2,0x4958,native_exit);normalized=bytearray(materialized.actual)
 for f in fields:
  at=f['object_offset'];normalized[at:at+2]=f['encoded_value'].to_bytes(2,'little')
 need(bytes(normalized)==native and all(native[i]==v for i,v in values.items()),'all88 native, literal12/reservation76 distinct')
 need(normalized[10:86]==materialized.actual[10:86]==bytes(76),'reservation remains real actual bytes, never source fill')
 loaded=[]
 for load in(0,1,4096,65535):
  v,_=literals(o,0x5cc2,0x4958,native_exit,load);b=bytearray(normalized);b[8:10]=((int.from_bytes(b[8:10],'little')+load)&65535).to_bytes(2,'little');need(all(b[i]==x for i,x in v.items()),'native four bases');loaded.append(load)
 need(sha(json.dumps(evidence,sort_keys=True).encode())==p['REA_canonical_sha256'],'exact retained complete REA88 content')
 # The narrow existing API explicitly receives precisely this emitted site list.
 eid=validate_expanded_read(evidence,unit,bytes(normalized),reference,emitted_mz_sites=MZ)
 return bytes(normalized),{'native_evidence_id':eid,'literal_bytes':12,'authentic_LINK_materialized_reservation_bytes':76,'runtime_physical_span':88,'normalized_only_real_fields':[4,8,86],'emitted_mz_sites':MZ,'four_bases':loaded,'authored_C_credit':0,'historical_TU_original_MAP_claim':False,'primitive_only_not_fresh':materialized.proof['primitive_only_not_fresh']}
