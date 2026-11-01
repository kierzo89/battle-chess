from pathlib import Path
import hashlib,json
from omf import read_omf
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256
import mixed_overlap_generation16 as generation
from mixed_overlap_source16 import compose_fresh
H=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError('Closed mixed overlap: '+message)
PROFILE_SHA256='5bf81c9c5ae7a53750bf786610d285b30432ce26ffacd30d0753f56bcbcf7063'
def profile(kind):
 raw=Path(__file__).with_name('mixed_overlap_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'closed profiles changed');return json.loads(raw)[kind]
def native_objects(b,kind,ref):
 p=profile(kind);units={u['id']:u for u in p['original_units']};ids=p['owners'];origin=p['origin'];size=p['size'];obj=read_omf(b.object_bytes)
 assert [(s.name,s.length,s.attributes) for s in obj.segments.values()]==[('_TEXT',size,72),('_DATA',0,72),('CONST',0,72),('_BSS',0,72)]
 raw=b''
 for at,data in obj.segments[1].chunks:assert at==len(raw);raw+=data
 assert len(raw)==size and not obj.procedures
 bindings={};syms={};at=0
 for id in ids:
  u=units[id];symbol=u.get('symbol') or u['public_symbols'][0];syms[symbol]=at;assert int(u['image_offset'],0)==origin+at
  for n,v in u['externals'].items():assert n not in bindings or bindings[n]==v;bindings[n]=v
  at+=u['size']
 assert {k:v.offset for k,v in obj.publics.items()}==syms and all(p.segment==1 for p in obj.publics.values())
 native=ref['image'][origin:origin+size];ns=sorted(x for x in ref['relocations'] if origin<=x<origin+size);results=[];fields=[]
 for load in [0,1,4096,65535]:
  data=bytearray(raw);sites=[];occupied=set()
  for f in obj.fixups:
   assert f.segment==1 and f.location_type in (1,2,3) and f.width=={1:2,2:2,3:4}[f.location_type]
   assert not occupied.intersection(range(f.offset,f.offset+f.width));occupied.update(range(f.offset,f.offset+f.width));assert 0<=f.offset<=size-f.width
   add=int.from_bytes(raw[f.offset:f.offset+min(2,f.width)],'little');disp=f.displacement or 0
   if f.target[0]==0:
    assert f.target==(0,1) and f.frame==(0,1) and not f.segment_relative and f.location_type==1
    tp=load;to=origin
   else:
    assert f.target[0]==2;name=obj.externals[f.target[1]];v=bindings[name]
    if isinstance(v,dict):assert set(v)=={'segment','offset'};tp=(v['segment']+load)&65535;to=v['offset']
    else:tp=load if not f.segment_relative else (0x5cc2+load)&65535;to=v
   if f.frame==(0,1):frame=load
   elif f.frame==(1,1):frame=(0x5cc2+load)&65535
   elif f.frame==(2,f.target[1]):frame=tp
   else:raise ValueError('Unknown frame '+str(f))
   if f.location_type==2:
    assert f.segment_relative and add==0 and disp==0;encoded=tp.to_bytes(2,'little');sites.append(origin+f.offset)
   elif f.location_type==3:
    assert f.segment_relative and raw[f.offset+2:f.offset+4]==b'\0\0';encoded=((to+disp+add)&65535).to_bytes(2,'little')+tp.to_bytes(2,'little');sites.append(origin+f.offset+2)
   else:
    n=tp*16+to+disp+add-(frame*16 if f.segment_relative else load*16+origin+f.offset+2);encoded=(n&65535).to_bytes(2,'little')
   data[f.offset:f.offset+f.width]=encoded
   if load==0:fields.append({'offset':f.offset,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'frame':list(f.frame),'target':list(f.target),'external':obj.externals.get(f.target[1]) if f.target[0]==2 else None,'displacement':f.displacement,'source_addend':add,'raw_fixupp':f.raw.hex()})
  expected=bytearray(native)
  for s in ns:i=s-origin;expected[i:i+2]=((int.from_bytes(expected[i:i+2],'little')+load)&65535).to_bytes(2,'little')
  results.append({'load':load,'whole_bytes':data==expected,'MZ_sites_equal':sorted(sites)==ns,'first_difference':next((i for i,(a,b) in enumerate(zip(data,expected)) if a!=b),None)})
  if load==0:linked_zero=bytes(data)
 return linked_zero,{'status':'PASS_RETAINED_WHOLE_MIXED' if all(r['whole_bytes'] and r['MZ_sites_equal'] for r in results) else 'HELD','origin':origin,'size':size,'owners':ids,'public_offsets':syms,'fields':fields,'field_count':len(fields),'native_MZ':ns,'loads':results,'canonical_credit_added':0,'retained_FA_not_fresh_generation':False}

def compare(b,kind,reference,project):
 p=profile(kind);r=p['recipe']
 need(type(b) is generation.FreshMixedBuild and b._cap is generation._LIVE_CAP,'same-call guarded generation capability')
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and H(reference['image'])==p['reference_sha256'],'independent original complete reference')
 for actual,key in [(b.object_bytes,'raw_sha256'),(b.c5_sidecar_bytes,'sidecar_sha256'),(b.fresh_fa_bytes,'fa_sha256'),(b.mixed_source_bytes,'mixed_sha256')]:need(H(actual)==p[key],'complete immutable '+key)
 prov=b.provenance
 need(prov['status']=='COMPLETE' and prov['guard_closed'] and prov['source_tools_freshscratch_only'] and not prov['native_original_oldOBJ_profile_inside_GEN'],'guarded generation')
 need(len(prov['guard']['blocked'])==20,'active GEN denials')
 need([x['phase'] for x in prov['processes']]==['C5','MASM'] and all(x['terminal'] and x['reaped'] and x['returncode']==0 for x in prov['processes']),'two real successful phases')
 need(prov['source_SHA256']==r['C_SOURCE_SHA256'] and prov['authored_ASM_SHA256']==r['DECODER_SOURCE_SHA256'],'source roles')
 asm=(Path(project)/r['ASM_SOURCE']).read_bytes();source=(Path(project)/r['C_SOURCE']).read_bytes()
 need(H(source)==r['C_SOURCE_SHA256'] and H(asm)==r['DECODER_SOURCE_SHA256'],'exact reviewed source')
 composed,transform=compose_fresh(b.fresh_fa_bytes,asm,c_source_sha256=H(source));need(composed==b.mixed_source_bytes and transform==prov['transform'],'complete reversible FA/source transformation')
 for key,actual in [('C5/UNIT.C',source),('C5/UNIT.OBJ',b.c5_sidecar_bytes),('C5/UNIT.ASM',b.fresh_fa_bytes),('MASM/UNIT.ASM',b.mixed_source_bytes),('MASM/UNIT.OBJ',b.object_bytes)]:need(b.artifacts[key]==actual,'fresh artifact role '+key)
 c=read_omf(b.c5_sidecar_bytes);crows=[u for u in p['original_units'] if u['language']=='c'];need(set(c.publics)=={u['symbol'] for u in crows} and len(c.procedures)==len(crows),'genuine complete C owners')
 coff=0;sidecars=[]
 for u in crows:
  info=c.function_info(u['symbol']);need(info['boundary']=='codeview3_procedure' and info['offset']==coff and info['size']==u['size'],'genuine typed sidecar extent')
  at=int(u['image_offset'],0);actual,fields=link_function(c,u['symbol'],at,u['externals']);need(actual==reference['image'][at:at+u['size']],'complete genuine C5/native body')
  sidecars.append({'symbol':u['symbol'],'size':u['size'],'offset':coff,'fields':len(fields)});coff+=u['size']
 code,proof=native_objects(b,kind,reference)
 need(proof['status']=='PASS_RETAINED_WHOLE_MIXED' and proof['fields']==p['fields'] and proof['native_MZ']==p['native_MZ'],'closed whole native/raw field/MZ contract')
 proof.update(status='PASS_FRESH_WHOLE_MIXED',whole_native_equal=True,C5_sidecar_not_SOURCE=True,all_fields=[dict(f,object_offset=f['offset']) for f in proof['fields']],load_bases=[{'base':x['load'],'native_equal':x['whole_bytes'],'MZ_equal':x['MZ_sites_equal']} for x in proof['loads']],C5_contracts=sidecars,transform=transform)
 return code,proof
