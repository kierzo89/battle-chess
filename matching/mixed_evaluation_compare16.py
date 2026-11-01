"""Finite evaluator verifier; current source-produced build supplied by caller."""
from pathlib import Path
import json,hashlib,dataclasses,re
from omf import read_omf
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256,IMAGE_SIZE
from mixed_evaluation_source16 import compose_fresh,SOURCES,C_SOURCE_SHA256,ORDER
D=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError('evaluation3902: '+m)
def safe(x):
 if dataclasses.is_dataclass(x):return safe(dataclasses.asdict(x))
 if isinstance(x,bytes):return x.hex()
 if isinstance(x,dict):return {str(k):safe(v)for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [safe(v)for v in x]
 return x
def profile():
 data=(D/'mixed_evaluation_profile.json').read_bytes();need(H(data)==PROFILE_SHA256,'immutable profile');return json.loads(data)
def compare(b,reference,project=None):
 M=Path(project)if project is not None else D
 p=profile();
 for relative,digest in p['REA_pins'].items():need(H((M/relative).read_bytes())==digest,'all retained native extent inputs')
 g=b.provenance;raw=b.object_bytes;side_raw=b.c5_sidecar_bytes;fa=b.fresh_fa_bytes
 need(g['status']=='COMPLETE'and g['error']is None and g['guard_closed']and g['source_tools_freshscratch_only']and g['native_original_oldOBJ_profile_inside_GEN']is False,'closed source-only generator')
 need(len(g['guard']['blocked'])==20 and len({r['path']for r in g['guard']['blocked']})==5 and g['guard']['FIFO'],'active denial and FIFO proof')
 calls=g['processes'];need([x['phase']for x in calls]==['C5','MASM']and all(x['terminal']and x['reaped']and x['returncode']==0 and type(x['pid'])is int and x['pid']>0 for x in calls)and len({x['pid']for x in calls})==2,'one real C5 plus MASM')
 need(g['flags']==['/AM','/Gs','/Zi']and g['MASM_flags']==['/Mx']and g['listing_flag']=='/FaC:\\UNIT.ASM'and g['source_SHA256']==C_SOURCE_SHA256,'exact C5 source and flags')
 need(H((M/'src/full_evaluation_match.c').read_bytes())==C_SOURCE_SHA256,'source context')
 for key,data in [('raw_mixed_SHA256',raw),('C5_sidecar_SHA256',side_raw),('fresh_FA_SHA256',fa),('mixed_ASM_SHA256',b.mixed_source_bytes)]:need(g[key]==H(data),'artifact receipt')
 for path,digest in g['allowed_reads'].items():need(H(Path(path).read_bytes())==digest,'actual source/tool context')
 authored={n:(D/v['file']).read_bytes()for n,v in SOURCES.items()};composed,proof=compose_fresh(fa,authored,c_source_sha256=C_SOURCE_SHA256)
 need(composed==b.mixed_source_bytes and proof==g['transform']and g['authored_ASM_SHA256']=={n:H(v)for n,v in authored.items()},'exact current source inverse')
 need(H(raw)==p['raw_SHA256']and H(side_raw)==p['side_SHA256']and H(fa)==p['FA_SHA256'],'whole calibrated raw and real C5 sidecar/FA')
 o=read_omf(raw);side=read_omf(side_raw)
 for obj,key in [(o,'raw_snapshot'),(side,'C5_snapshot')]:need(safe({k:getattr(obj,k)for k in ['names','segments','publics','externals','procedures','fixups','records','data_writes']})==p[key],'all parsed records/segments/CV/publics/fixups/data writes')
 need(len(o.fixups)==223 and len(o.publics)==11 and len(side.procedures)==11 and not o.procedures,'complete mixed and genuine typed sidecar')
 code=bytearray()
 for at,data in o.segments[1].chunks:need(at==len(code)and data,'chronological initialized CODE');code.extend(data)
 need(len(code)==3902 and code[-1:]==b'\x90','whole CODE and actual outside-PROC NOP')
 units=p['units'];bindings=p['bindings'];current=p['canonical_C'];start=0xfdf2
 need(set(o.publics)==set(ORDER),'eleven real publics')
 for u in units:
  pub=o.publics[u['symbol']];need((pub.segment,pub.group,pub.type_index,pub.offset)==(1,0,0,int(u['image_offset'],0)-start),'all native public offsets')
  ep=M/u['rea_evidence'];need(not ep.is_symlink()and H(ep.read_bytes())==p['REA_pins'][u['rea_evidence']],'pinned native REA evidence');e=json.loads(ep.read_text());proc=e['normalized_result']['procedure'];body=proc['body'];a=int(u['image_offset'],0)+0x10000
  need(e['operation']=='analyze_function'and e['subject']['digest']['sha256']==ORIGINAL_SHA256 and int(proc['address'],0)==a,'native original primary entry')
  if not u.get('extended_extent'):
   need(body['ranges']==[{'start':hex(a),'end':hex(a+u['size']-1)}]and body['total_bytes']==body['span_bytes']==u['size']and not body['non_contiguous'],'real whole native procedure')
  else:
   need(u in current and u['extended_extent']['kind']in('unreachable_forward_jump_gap_v1','segmented_evaluation_v1'),'only existing original C extended proofs')
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and len(reference['image'])==IMAGE_SIZE and reference['prefix_size']>=0x10d30,'full native reference')
 native=reference['image'][start:start+3902];sites=sorted(s for s in reference['relocations']if start<=s<start+3902);need(sites==[0x1004c,0x10b45],'two whole native MZ sites')
 retained=[]
 for u in current:
  linked,fields=link_function(side,u['symbol'],u['code_address']['offset'],u['externals'],image_origin=int(u['image_offset'],0));a=int(u['image_offset'],0)-start;need(len(linked)==u['size']and linked==native[a:a+u['size']],'genuine retained C equals native');retained.append({'symbol':u['symbol'],'bytes':len(linked)})
  if u.get('extended_extent'):
   from extent import validate_extended_extent
   retained[-1]['extended_extent_proof']=validate_extended_extent(u,M,ORIGINAL_SHA256,side.function_info(u['symbol']),linked,source_object=side)
 need(len(retained)==9 and sum(x['bytes']for x in retained)==3315,'C credit separate from two ASM586')
 def link_load(load):
  value=bytearray(code);used=set();emitted=[];ledger=[]
  for q in o.fixups:
   at=q.offset;assert q.segment==1 and at>=0 and at+q.width<=len(code);assert not used.intersection(range(at,at+q.width));used.update(range(at,at+q.width));add=int.from_bytes(code[at:at+2],'little')+(q.displacement or 0)
   if q.target[0]==0:
    assert q.width==2 and q.location_type==1 and q.frame==q.target==(0,1)and not q.segment_relative and 0<=add<len(code)
    assert code[at-1]in(0xe8,0xe9)
    if code[at-1]==0xe8:assert code[at-2]==0x0e and add in {p.offset for p in o.publics.values()}
    encoded=((add-at-2)&65535).to_bytes(2,'little');symbol='own_CODE';role='OWN_CODE_RELATIVE'
   else:
    assert q.target[0]==2;symbol=o.externals[q.target[1]];target=bindings[symbol]
    if q.width==4:
     assert q.location_type==3 and q.segment_relative and q.frame==q.target and q.displacement is None and code[at:at+4]==bytes(4)and code[at-1]==0x9a
     assert symbol in ('_castle_95df','_castle_flags_9ad5')and target['segment']==0
     encoded=target['offset'].to_bytes(2,'little')+((target['segment']+load)&65535).to_bytes(2,'little');emitted.append(start+at+2);role='EXTERNAL_FAR_CALL'
    else:
     assert q.width==2 and q.location_type==1 and q.segment_relative and isinstance(target,int)and q.frame in[(1,1),q.target]and symbol not in p['near_same_frame_symbols']
     encoded=((target+add)&65535).to_bytes(2,'little');role='DGROUP_DATA_OFFSET'
   value[at:at+q.width]=encoded;ledger.append({'field':safe(q),'symbol':symbol,'role':role,'effective_addend':add,'encoded':encoded.hex()})
  expected=bytearray(native)
  for site in sites:
   i=site-start;expected[i:i+2]=((int.from_bytes(expected[i:i+2],'little')+load)&65535).to_bytes(2,'little')
  diffs=[i for i,(a,b)in enumerate(zip(value,expected))if a!=b]
  assert not diffs,{'load':load,'differing_bytes':len(diffs),'first20':diffs[:20]}
  assert sorted(emitted)==sites
  return {'load':load,'whole_equal':True,'sha256':H(value),'native_MZ':sites},ledger
 loads=[];zero_fields=None
 for load in (0,1,4096,65535):
  r,fields=link_load(load);loads.append(r)
  if load==0:zero_fields=fields
 actual=bytearray(code)
 for f in zero_fields:
  q=f['field'];actual[q['offset']:q['offset']+q['width']]=bytes.fromhex(f['encoded'])
 need(bytes(actual)==native,'return only generated and relocation-resolved bytes')
 return bytes(actual),{'status':'PASS_EVALUATION3902_C3315_ASM586_CANDIDATE','whole_raw_SHA256':H(raw),'whole_CODE':3902,'all_fields':[{'raw':f['field'],**{k:v for k,v in f.items()if k!='field'}}for f in zero_fields],'native_MZ':sites,'four_bases':loads,'genuine_preserved_C':retained,'authored_ASM_procedures':2,'authored_ASM_bytes':586,'outside_PROC_NOP':1,'source_inverse':proof,'canonical_admission':False,'C_ASM_DATA_FILE_credit_delta':0,'GEN_LINK_calls_in_comparison':0}

PROFILE_SHA256='09a2bd45888543981a6fc12095ea650535587715ae6ec03db78c6e8282f8aba4'
