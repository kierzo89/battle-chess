"""Staged production comparison; caller supplies current build and reference.

The native arithmetic and source inverse are retained from the independently
verified prototype. No generation is performed and no canonical credit granted.
"""
from pathlib import Path
import sys,json,hashlib,dataclasses,re
D=Path(__file__).resolve().parent;M=D;P=D
H=lambda b:hashlib.sha256(b).hexdigest();J=lambda p:json.loads(Path(p).read_text())
PROFILE_SHA256='a12649ecc0b0d66ef44dbc46150bb1a2aa036e1dd5863a5dbc359c728fb74869'
def profile():
 raw=(P/'mixed_graphics_profile.json').read_bytes()
 if H(raw)!=PROFILE_SHA256:raise ValueError('changed comparison contract')
 return json.loads(raw)
def need(v,m):
 if not v:raise ValueError('graphics7262: '+m)

def safe(x):
 if dataclasses.is_dataclass(x):return safe(dataclasses.asdict(x))
 if isinstance(x,bytes):return x.hex()
 if isinstance(x,dict):return{str(k):safe(v)for k,v in x.items()}
 if isinstance(x,(tuple,list)):return[safe(v)for v in x]
 return x

def complete_code(o,sn):
 s=o.segments[sn];need(not s.unsupported_data,'unsupported CODE writes');b=bytearray()
 for at,v in s.chunks:need(at==len(b)and v,'complete nonoverlapping chronological CODE');b.extend(v)
 need(len(b)==s.length,'whole CODE initialized');return bytes(b)

def compare(b,reference):
 sys.path[:0]=[str(P),str(M)]
 from mixed_graphics_source16 import compose_fresh,C_SOURCE_SHA256,SOURCES,ORDER
 from omf import read_omf,_Cursor
 from link16 import link_function
 from reference import build_reference,ORIGINAL_SHA256,CARRIER_SHA256,IMAGE_SIZE
 p=profile();ledger=p['ledger'];bindings=p['bindings'];g=b.provenance
 need(g['status']=='COMPLETE'and g['error']is None and g['guard_closed']and g['source_tools_freshscratch_only']and g['native_original_oldOBJ_profile_inside_GEN']is False and len(g['guard']['blocked'])==20 and len({r['path']for r in g['guard']['blocked']})==5 and g['guard']['FIFO'],'closed real source-only denial/FIFO proof')
 calls=g['processes'];need([r['phase']for r in calls]==['C5','MASM']and all(r['terminal']and r['reaped']and r['returncode']==0 and type(r['pid'])is int and r['pid']>0 for r in calls)and len({r['pid']for r in calls})==2,'one actual C5 followed by one actual MASM')
 need(g['flags']==['/AS','/Zi']and g['listing_flag']=='/FaC:\\UNIT.ASM'and g['MASM_flags']==['/Mx']and g['source_SHA256']==C_SOURCE_SHA256,'unchanged genuine compiler source/flags')
 side=b.c5_sidecar_bytes;fa=b.fresh_fa_bytes;raw=b.object_bytes;mixed=b.mixed_source_bytes;authored={n:(P/v['file']).read_bytes()for n,v in SOURCES.items()};composed,proof=compose_fresh(fa,authored,c_source_sha256=C_SOURCE_SHA256)
 need(composed==mixed and proof==g['transform']and len(proof['preserved_C_PROCs'])==15,'same fresh full FA inverse/seven authored sources/fifteen verbatim C PROCs')
 for key,b in [('raw_mixed_SHA256',raw),('C5_sidecar_SHA256',side),('fresh_FA_SHA256',fa),('mixed_ASM_SHA256',mixed)]:need(g[key]==H(b),'actual artifact receipt '+key)
 need(len(side)==20383 and H(side)=='bbf21cc9175467d80a2fbc3ed8471b94a7893c11f27d2cac46f3a563d2022dc3'and H(fa)=='f5b66025231057779f839ec463a33fbd4cd5c472496b904cd4754438e41a7ec1','whole actual C5 sidecar and FA equal genuine baseline; no trimmed/rebuilt typed object')
 need(H(raw)==p['verified_comparison']['whole_raw_SHA256'],'exact calibrated whole RAW');c=read_omf(side);o=read_omf(raw);need(safe({k:getattr(c,k)for k in ['names','segments','publics','externals','procedures','fixups','records','data_writes']})=={k:v for k,v in p['C5_snapshot'].items()if k!='raw_SHA256'},'exact whole C5 parsed snapshot');need(safe({k:getattr(o,k)for k in ['names','segments','publics','externals','fixups','data_writes']})==p['verified_comparison']['whole_OMF_snapshot']and [[k,at,H(v)]for k,at,v in o.records]==p['verified_comparison']['complete_records'],'exact whole mixed parsed snapshot and records');need(c.procedures==p['C5_snapshot']['procedures']and len(c.procedures)==22,'all22 genuine CV procedure bounds')
 codeids=[s.index for s in o.segments.values()if s.class_name=='CODE'];need(codeids==[1]and(o.segments[1].name,o.segments[1].length,o.segments[1].attributes)==('_TEXT',7262,72),'sole complete WORD PUBLIC CODE7262')
 need([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',7262,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72)]and not o.procedures,'exact three empty storage segments/no fake debug/extra storage')
 need(all(not s.chunks and not s.unsupported_data for s in o.segments.values()if s.index!=1),'no hidden initialized storage')
 need(set(o.publics)==set(ORDER)and all((o.publics[r['symbol']].segment,o.publics[r['symbol']].group,o.publics[r['symbol']].offset,o.publics[r['symbol']].type_index)==(1,0,r['module_offset'],0)for r in ledger['rows']),'all22 actual near PUBLIC offsets/whole extent, no aliases')
 groups=[]
 for k,at,payload in o.records:
  need(k in(0x80,0x88,0x8a,0x96,0x98,0x9a,0x8c,0x90,0xa0,0x9c),'no unknown/COMMON/iterated/TYPE/data records')
  if k==0x9a:
   cur=_Cursor(payload);name=o.names[cur.index()];members=[]
   while cur:need(cur.byte()==255,'typed group member');members.append(cur.index())
   groups.append((name,members))
 need(groups==[('DGROUP',[3,4,2])],'genuine FA DGROUP ordering')
 rawcode=complete_code(o,1);need(len(rawcode)==7262 and all(f.segment==1 for f in o.fixups),'every field belongs complete CODE; no raw object rewriting')
 # Only the actual fresh listing's declarations classify established bindings.
 declarations=dict(re.findall(rb'^EXTRN\t([^:\r\n]+):([^\r\n]+)\r$',fa,re.M));declarations={k.decode():v.decode()for k,v in declarations.items()};need(set(o.externals.values())<=set(declarations),'all actual externals declared by same fresh compiler source')
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and len(reference['image'])==IMAGE_SIZE and reference['prefix_size']>=0x578c,'genuine complete unchanged native prefix');native=reference['image'][0x3b2e:0x578c];sites=sorted(x for x in reference['relocations']if 0x3b2e<=x<0x578c);need(sites==ledger['native_MZ']and len(sites)==24,'all24 native MZ (15 authored/nine retained C)')
 occupied=set();fields=[]
 for f in sorted(o.fixups,key=lambda q:q.offset):
  need(f.width in(2,4)and f.location_type in(1,2,3)and 0<=f.offset<f.offset+f.width<=7262 and not occupied.intersection(range(f.offset,f.offset+f.width)),'complete typed disjoint field extents');occupied.update(range(f.offset,f.offset+f.width));need(f.displacement is None or type(f.displacement)is int and 0<=f.displacement<=65535,'explicit optional displacement')
  if f.target[0]==0:need(f.target==(0,1)and f.frame==(0,1)and f.width==2 and f.location_type==1 and not f.segment_relative,'sole own whole CODE internal relative form')
  elif f.target[0]==2:
   name=o.externals[f.target[1]];need(name in bindings and f.frame in((0,1),(1,1),(2,f.target[1])),'exact explicit native symbol/frame domain')
   if f.width==4:need(f.location_type==3 and f.segment_relative and declarations[name]=='FAR'and isinstance(bindings[name],dict)and set(bindings[name])=={'segment','offset'}and f.frame==(2,f.target[1]),'finite genuine external FAR4 frame')
   elif f.location_type==2:need(f.segment_relative and f.frame==(2,f.target[1])and isinstance(bindings[name],dict)and set(bindings[name])=={'segment','offset'}and not f.displacement,'finite external BASE16')
   elif not f.segment_relative:need(declarations[name]=='NEAR'and f.frame==(0,1)and type(bindings[name])is int and rawcode[f.offset-1]in(0xe8,0xe9),'native same-CS external near branch')
   elif name=='__AHSHIFT':need(f.location_type==1 and f.width==2 and f.segment_relative and declarations[name]=='NEAR'and bindings[name]=={'absolute':12}and f.frame==(2,f.target[1])and f.displacement is None and f.offset in[417,646,1777,2459,2484]and rawcode[f.offset-1]==0xb9 and rawcode[f.offset:f.offset+2]==b'\0\0','sole genuine C5 __AHSHIFT absolute12 MOV CX OFFSET16 ABI constant; not CODE/DATA/MZ')
   else:need(f.location_type==1 and declarations[name]not in('NEAR','FAR')and f.frame in((1,1),(2,f.target[1])),'finite actual data/absolute OFFSET16')
  else:raise ValueError('unsupported actual target tuple '+str(f.target))
 absolute_fields=[f for f in o.fixups if f.target[0]==2 and o.externals[f.target[1]]=='__AHSHIFT'];need(sorted(f.offset for f in absolute_fields)==[417,646,1777,2459,2484],'all five and only genuine helper constant fields; no added absolute provider')
 bases=[];zero_fields=None;Cresults=[]
 for load in[0,1,4096,65535]:
  linked=bytearray(rawcode);emitted=[];fieldlog=[]
  for f in sorted(o.fixups,key=lambda q:q.offset):
   add=int.from_bytes(rawcode[f.offset:f.offset+min(f.width,2)],'little');disp=f.displacement or 0;name=None
   if f.target[0]==0:tp=load;to=0x3b2e
   else:
    name=o.externals[f.target[1]];v=bindings[name];typ=declarations[name]
    if isinstance(v,dict)and set(v)=={'segment','offset'}:tp=(v['segment']+load)&65535;to=v['offset']
    elif isinstance(v,dict):need(set(v)=={'absolute'},'only actual absolute compiler ABI constant');tp=0;to=v['absolute']
    else:tp=load if typ=='NEAR'else(0x5cc2+load)&65535;to=v
   if f.width==4:
    need(add==0 and rawcode[f.offset+2:f.offset+4]==b'\0\0'and disp==0,'genuine complete FAR4 zero source addend');encoded=to.to_bytes(2,'little')+tp.to_bytes(2,'little');emitted.append(0x3b2e+f.offset+2)
   elif f.location_type==2:encoded=((tp+add)&65535).to_bytes(2,'little');emitted.append(0x3b2e+f.offset)
   else:
    fp=load if f.frame==(0,1)else((0x5cc2+load)&65535 if f.frame==(1,1)else tp)
    value=add+disp+tp*16+to-(fp*16 if f.segment_relative else load*16+0x3b2e+f.offset+2);encoded=(value&65535).to_bytes(2,'little')
   linked[f.offset:f.offset+f.width]=encoded;fieldlog.append({'raw':safe(f),'symbol':name,'source_addend':add,'displacement':disp,'encoded':encoded.hex()})
  expected=bytearray(native)
  for site in sites:at=site-0x3b2e;expected[at:at+2]=((int.from_bytes(expected[at:at+2],'little')+load)&65535).to_bytes(2,'little')
  need(bytes(linked)==bytes(expected),'every whole7262 byte/native/fourbases (retain any negative)');need(sorted(emitted)==sites,'exact complete emitted/native MZ set')
  bases.append({'load_paragraph':load,'whole_CODE_SHA256':H(linked),'all_native_bytes_equal':True,'MZ':sites})
  if load==0:zero_fields=fieldlog;zero_bytes=bytes(linked)
 for row in ledger['rows']:
  primary=J(M/row['REA_primary']);nr=primary['normalized_result'];np=nr['procedure'];need(primary['subject']['digest']['sha256']==ORIGINAL_SHA256 and primary['operation']=='analyze_function'and int(np['address'],0)==row['native_start']+0x10000 and np['body']['ranges']==[{'start':hex(row['native_start']+0x10000),'end':hex(row['native_end']-1+0x10000)}]and np['body']['total_bytes']==np['body']['span_bytes']==row['size']and not np['body']['non_contiguous']and len(nr['assembly'])==row['instruction_count'],'all22 independent complete contiguous native instruction/entry extents')
  inf=c.function_info(row['symbol']);need({k:inf[k]for k in('offset','size','end','boundary')}==row['CV'],'all original genuine CV bounds')
  body,_=link_function(c,row['symbol'],row['native_start'],bindings,image_origin=row['native_start']);n=native[row['module_offset']:row['module_offset']+row['size']];diff=[{'offset':i,'C5':x,'native':y}for i,(x,y)in enumerate(zip(body,n))if x!=y];need(diff==row['C5_native_differences'],'original seven rejected C frame controls retained exactly')
  if row['current_C_credit']:need(body==n,'15 actual C5 spans equal final mixed/native');Cresults.append({'symbol':row['symbol'],'genuine_CV':row['CV'],'bytes':len(body)})
 need(len(Cresults)==15 and sum(x['bytes']for x in Cresults)==2761 and sum(len(r['native_MZ'])for r in ledger['rows']if not r['current_C_credit'])==15,'strict C2761/ASM4501 separation')
 return zero_bytes,{'status':'PASS_SOURCE_FIRST_GRAPHICS7262_C2761_ASM4501_PROTOTYPE_ONLY','whole_raw_SHA256':H(raw),'whole_raw_bytes':len(raw),'whole_CODE':7262,'C5_whole_sidecar_SHA256':H(side),'source_inverse':proof,'all_fields':zero_fields,'absolute_helper_ABI':{'symbol':'__AHSHIFT','declared_type':'NEAR','binding':{'absolute':12},'offsets':[417,646,1777,2459,2484],'F2_target_frame':True,'MZ':[],'load_dependent':False},'complete_records':[[k,at,H(p)]for k,at,p in o.records],'whole_OMF_snapshot':safe({'names':o.names,'segments':o.segments,'publics':o.publics,'externals':o.externals,'fixups':o.fixups,'data_writes':o.data_writes}),'all22_real_sidecar_CV':safe(c.procedures),'genuine_preserved_C':Cresults,'authored_ASM_procedures':7,'authored_ASM_bytes':4501,'native_MZ':sites,'four_bases':bases,'historical_language_original_TU_or_SEGDEF_claim':False,'canonical_admission':False,'C_ASM_DATA_FILE_credit_delta':0,'GEN_LINK_calls_in_comparison':0}

