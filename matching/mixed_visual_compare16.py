from pathlib import Path
import hashlib,json
from omf import read_omf
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256
import mixed_visual_generation16 as generation
from mixed_visual_source16 import compose_fresh
H=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError('Closed mixed overlap: '+message)
PROFILE_SHA256='327f5e7cd450cc2847ec09bed0c0000abc99f4f69f97966f38951f6027a52ae3'
def profile(kind):
 raw=Path(__file__).with_name('mixed_visual_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'closed profiles changed');return json.loads(raw)[kind]
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
 p=profile(kind);r=p['recipe'];prov=b.provenance
 need(type(b)is generation.FreshMixedBuild and b._cap is generation._LIVE_CAP,'same-call guarded generation capability')
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256 and H(reference['image'])==p['reference_sha256'],'independent original complete reference')
 need(len(b.sidecars)==len(b.fas)==len(r['parts'])and b.c5_sidecar_bytes==b.sidecars[0]and b.fresh_fa_bytes==b.fas[0],'complete immutable sidecar/listing roles')
 need(H(b.object_bytes)==p['raw_sha256']and[H(x)for x in b.sidecars]==p['sidecar_hashes']and[H(x)for x in b.fas]==p['fa_hashes']and H(b.mixed_source_bytes)==p['mixed_sha256'],'complete immutable generated outputs')
 need(prov['status']=='COMPLETE'and prov['guard_closed']is True and prov['source_tools_freshscratch_only']is True and prov['native_original_oldOBJ_profile_inside_GEN']is False and prov['credit']==0,'guarded source-only generation')
 blocked=prov['guard']['blocked'];need(len(blocked)==20 and len({x['path']for x in blocked})==5 and{x['api']for x in blocked}=={'Path.open','builtins.open','io.open','os.open'}and prov['guard']['FIFO'],'active source-only guard controls')
 phases=['C5']+['C5_'+str(i)for i in range(1,len(r['parts']))]+['MASM'];calls=prov['processes']
 need([x['phase']for x in calls]==phases and len({x['pid']for x in calls})==len(phases)and all(type(x['pid'])is int and x['pid']>0 and x['terminal']is True and x['reaped']is True and x['returncode']==0 for x in calls),'every real compiler/assembler phase closed')
 commands=['T:\\CL.EXE /c '+' '.join(part['flags'])+' /FaC:\\UNIT.ASM /FoC:\\UNIT.OBJ C:\\UNIT.C'for part in r['parts']]+['T:\\MASM /Mx UNIT.ASM,UNIT.OBJ,UNIT.LST,UNIT.CRF;']
 need([x['command']for x in calls]==commands and prov['all_flags']==[part['flags']for part in r['parts']]and prov['profile']==kind and prov['backend']==generation.BACKEND,'exact actual phase flags/commands')
 need(prov['source_SHA256']==r['C_SOURCE_SHA256']and prov['source_hashes']==[part['sha256']for part in r['parts']]and prov['authored_ASM_SHA256']==r['DECODER_SOURCE_SHA256'],'source identities')
 need(prov['raw_mixed_SHA256']==H(b.object_bytes)and prov['C5_sidecar_SHA256']==H(b.sidecars[0])and prov['sidecar_hashes']==[H(x)for x in b.sidecars]and prov['FA_hashes']==[H(x)for x in b.fas]and prov['mixed_ASM_SHA256']==H(b.mixed_source_bytes),'output receipt identities')
 project=Path(project);asm=(project/r['ASM_SOURCE']).read_bytes();need(H(asm)==r['DECODER_SOURCE_SHA256'],'authored ASM unchanged');sources=[]
 for part in r['parts']:
  path=project/part['source'];need(not path.is_symlink(),'regular source');source=path.read_bytes();need(H(source)==part['sha256'],'actual reviewed source unchanged');sources.append(source)
 composed,transform=compose_fresh(b.fas,asm,kind=kind,source_hashes=[H(x)for x in sources]);need(composed==b.mixed_source_bytes and transform==prov['transform'],'every fresh FA/source exact inverse')
 contracts=[];units={u['id']:u for u in p['original_units']}
 for i,part in enumerate(r['parts']):
  phase=phases[i]
  for key,value in [('UNIT.C',sources[i]),('UNIT.OBJ',b.sidecars[i]),('UNIT.ASM',b.fas[i])]:need(b.artifacts[phase+'/'+key]==value,'actual phase source/object/listing roles')
  c=read_omf(b.sidecars[i]);crows=[units[id]for id in part['owners']];need(set(c.publics)=={u['symbol']for u in crows}and len(c.procedures)==len(crows),'whole genuine sidecar PUBLIC/CV owner set')
  coff=0
  for u in crows:
   info=c.function_info(u['symbol']);need(info['boundary']=='codeview3_procedure'and info['offset']==coff and info['size']==u['size'],'complete typed original-compiler extent')
   at=int(u['image_offset'],0);actual,fields=link_function(c,u['symbol'],at,u['externals'],image_origin=at);need(actual==reference['image'][at:at+u['size']],'whole genuine C/native procedure')
   contracts.append({'id':u['id'],'symbol':u['symbol'],'size':u['size'],'sidecar_index':i,'flags':part['flags'],'offset':coff,'fields':len(fields)});coff+=u['size']
 need(b.artifacts['MASM/UNIT.ASM']==b.mixed_source_bytes and b.artifacts['MASM/UNIT.OBJ']==b.object_bytes,'actual MASM artifact roles')
 code,proof=native_objects(b,kind,reference);need(proof['status']=='PASS_RETAINED_WHOLE_MIXED'and proof['fields']==p['fields']and proof['native_MZ']==p['native_MZ'],'all complete native bytes/raw field frames/targets/sites at four bases')
 proof.update(status='PASS_FRESH_WHOLE_MIXED',whole_native_equal=True,C5_sidecar_not_SOURCE=True,all_fields=[dict(f,object_offset=f['offset'])for f in proof['fields']],load_bases=[{'base':x['load'],'native_equal':x['whole_bytes'],'MZ_equal':x['MZ_sites_equal']}for x in proof['loads']],C5_contracts=contracts,transform=transform)
 return code,proof
