"""Closed mixed460 post-generation comparator; native bytes never enter GEN."""
from pathlib import Path
import hashlib,json
from omf import read_omf,_Cursor
from link16 import link_function
from reference import ORIGINAL_SHA256,CARRIER_SHA256
from remove_actor247_profile import FIELD_PROFILE,EXTERNALS
from mixed_remove460_source16 import compose_fresh,C_SOURCE_SHA256,DECODER_SOURCE_SHA256,TRANSFORM
import mixed_remove460_generation16 as generation
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError('mixed460 comparison: '+m)
def profile():
 raw=Path(__file__).with_name('mixed_remove460_profile.json').read_bytes()
 need(H(raw)==PROFILE_SHA256,'closed original owner/source/output contracts')
 return json.loads(raw)
def code(obj):
    s=obj.segments[1];out=bytearray();need(not s.unsupported_data,'unsupported CODE data')
    for at,b in s.chunks:
        need(at==len(out) and b,'whole chronological CODE no holes/overlap');out.extend(b)
    need(len(out)==s.length,'whole initialized CODE');return bytes(out)
def native_objects(o,c,rows,ref):
    origin=int(rows[0]['image_offset'],0);size=sum(u['size'] for u in rows);prefix=rows[0]['size']
    need((origin,size,prefix)==(0x5934,460,247),'reviewed finite native scope')
    need(ref['original_sha256']==ORIGINAL_SHA256 and ref['carrier_sha256']==CARRIER_SHA256 and ref['prefix_size']>=origin+size,'independent original native identity')
    need([(s.name,s.class_name,s.length,s.attributes) for s in o.segments.values()]==[('_TEXT','CODE',size,72),('_DATA','DATA',0,72),('CONST','CONST',0,72),('_BSS','BSS',0,72)],'whole mixed CODE and three empty segments')
    need(not o.procedures and all(not s.chunks and not s.unsupported_data for s in o.segments.values() if s.index!=1),'no fabricated debug or hidden data')
    groups=[]
    for kind,at,payload in o.records:
        need(kind in (0x80,0x88,0x8a,0x96,0x98,0x9a,0x8c,0x90,0xa0,0x9c),'no unknown/COMMON/iterated records')
        if kind==0x9a:
            cur=_Cursor(payload);name=o.names[cur.index()];members=[]
            while cur:need(cur.byte()==255,'group member tag');members.append(cur.index())
            groups.append((name,members))
    need(groups==[('DGROUP',[3,4,2])],'genuine compiler group order')
    symbols=[u.get('symbol') or u['public_symbols'][0] for u in rows]
    need(set(o.publics)==set(symbols),'exact six publics/no aliases')
    position=0;bindings={};contracts=[]
    for u,symbol in zip(rows,symbols):
        at=int(u['image_offset'],0);p=o.publics[symbol]
        need(at==origin+position and (p.segment,p.group,p.offset,p.type_index)==(1,0,position,0),'complete contiguous native owner order')
        if u['language']=='c':
            info=c.function_info(symbol);need(info['boundary']=='codeview3_procedure' and (info['offset'],info['size'])==(position-prefix,u['size']),'unchanged genuine C5 typed extent')
            value,fields=link_function(c,symbol,at,u['externals']);need(value==ref['image'][at:at+u['size']],'complete original C5 sidecar/native span')
            contracts.append({'symbol':symbol,'size':u['size'],'offset':info['offset'],'fields':len(fields)})
        for name,value in u['externals'].items():
            need(name not in bindings or bindings[name]==value,'consistent canonical symbol bindings');bindings[name]=value
        position+=u['size']
    need(set(c.publics)==set(symbols[1:]) and len(c.procedures)==5 and code(c)[-1:]==b'\x90' and c.segments[1].length==214,'all five C procedures and unaltered whole sidecar EOF retained')
    expected=[(v[1],v[2],v[3],v[4],EXTERNALS[v[6][1]]) for v in FIELD_PROFILE]
    for f in c.fixups:
        if f.segment==1:
            need(f.target[0]==2,'known C5 external target');expected.append((prefix+f.offset,f.width,f.location_type,f.segment_relative,c.externals[f.target[1]]))
    actual=[(f.offset,f.width,f.location_type,f.segment_relative,o.externals.get(f.target[1]) if f.target[0]==2 else None) for f in o.fixups]
    need(sorted(actual)==sorted(expected) and len(actual)==21 and len({x[0] for x in actual})==21,'all21 exact ASM/C-sidecar field identities; no omissions/additions')
    raw=code(o);near={'__chkstk','_rand','_attach_actor','_detach_actor'};occupied=set()
    for f in o.fixups:
        need(f.segment==1 and f.width==2 and f.location_type in (1,2) and f.target[0]==2 and 0<=f.offset<=size-2,'complete supported typed field')
        need(not occupied.intersection((f.offset,f.offset+1)),'disjoint relocation fields');occupied.update((f.offset,f.offset+1))
        name=o.externals[f.target[1]];value=bindings[name]
        need(f.displacement is None and raw[f.offset:f.offset+2]==b'\0\0','unaltered zero source addend and no displacement')
        if not f.segment_relative:
            need(name in near and f.location_type==1 and f.frame==(0,1) and raw[f.offset-1]==0xe8,'explicit same-CS near CALL')
        elif name=='_dissolve_masks_0486':need(f.location_type==1 and f.frame==(1,1),'actual authored DGROUP mask reference')
        else:
            need(f.frame==(2,f.target[1]),'actual external target frame')
            if f.location_type==2:need(isinstance(value,dict) and set(value)=={'offset','segment'},'explicit native far BASE16 binding')
            if name in ('__AHINCR','__AHSHIFT'):
                need(value=={'absolute':4096 if name=='__AHINCR' else 12} and f.location_type==1,'exact existing compiler ABI constant')
    sites=sorted(s for s in ref['relocations'] if s<origin+size and s+2>origin)
    need(sites==[0x5ac4,0x5af2],'complete native MZ sites including crossing boundaries')
    loads=[];logs=[]
    for load in (0,1,4096,65535):
        linked=bytearray(raw);emitted=[];fields=[]
        for f in o.fixups:
            name=o.externals[f.target[1]];v=bindings[name]
            if isinstance(v,dict):
                tp,to=((0,v['absolute']) if set(v)=={'absolute'} else ((v['segment']+load)&65535,v['offset']))
            else:tp,to=(load if name in near else (0x5cc2+load)&65535),v
            if f.location_type==2:value=tp;emitted.append(origin+f.offset)
            elif not f.segment_relative:value=tp*16+to-(load*16+origin+f.offset+2)
            else:
                frame=(0x5cc2+load)&65535 if f.frame==(1,1) else tp
                value=tp*16+to-frame*16
            encoded=(value&65535).to_bytes(2,'little');linked[f.offset:f.offset+2]=encoded
            fields.append({'object_offset':f.offset,'symbol':name,'frame':f.frame,'target':f.target,'encoded':encoded.hex(),'raw_fixupp':f.raw.hex()})
        expected_bytes=bytearray(ref['image'][origin:origin+size])
        for site in sites:
            at=site-origin;expected_bytes[at:at+2]=((int.from_bytes(expected_bytes[at:at+2],'little')+load)&65535).to_bytes(2,'little')
        need(bytes(linked)==bytes(expected_bytes),'whole mixed native460 comparison at load '+str(load));need(sorted(emitted)==sites,'exact emitted MZ set')
        loads.append({'base':load,'native_equal':True,'sha256':H(linked)})
        if load==0:logs=fields;whole=bytes(linked)
    return whole,{'status':'PASS_RETAINED_MIXED460_NATIVE_FIELDS','native_review_pass':True,'whole_CODE_bytes':size,'all_fields':logs,'native_MZ':sites,'load_bases':loads,'genuine_C5':contracts,'C_bytes':213,'ASM_bytes':247,'canonical_credit_added':0,'actual_LINK_proven':False,'compiler_calls':0}

def compare(b,reference,project):
 need(type(b)is generation.FreshMixedBuild and b._cap is generation._LIVE_CAP,'live generator factory result required')
 p=profile();r=b.provenance
 need(r['status']=='COMPLETE' and r['guard_closed'] is True and r['source_tools_freshscratch_only'] is True and r['native_original_oldOBJ_profile_inside_GEN'] is False and r['credit']==0,'source-only closed generation provenance')
 need(r['kind']==generation.KIND and r['backend']==generation.BACKEND and r['source_SHA256']==C_SOURCE_SHA256 and r['authored_ASM_SHA256']==DECODER_SOURCE_SHA256,'generation identity')
 need(r['flags']==['/AS','/Zi'] and r['MASM_flags']==['/Mx'] and r['listing_flag']=='/FaC:\\UNIT.ASM','exact compiler flags')
 calls=r['processes'];need(len(calls)==2 and [x['phase']for x in calls]==['C5','MASM'] and len({x['pid']for x in calls})==2 and all(type(x['pid'])is int and x['pid']>0 and x['terminal']is True and x['reaped']is True and x['returncode']==0 for x in calls),'two distinct real closed process receipts')
 blocked=r['guard']['blocked'];need(len(blocked)==20 and len({x['path']for x in blocked})==5 and {x['api']for x in blocked}=={'Path.open','builtins.open','io.open','os.open'} and r['guard']['FIFO'],'active generation denial witnesses')
 sources=[Path(project)/generation.C_SOURCE,Path(project)/generation.ASM_SOURCE]
 need(all(not path.is_symlink() and H(path.read_bytes())==h for path,h in zip(sources,[C_SOURCE_SHA256,DECODER_SOURCE_SHA256])),'unchanged source files')
 mixed,transform=compose_fresh(b.fresh_fa_bytes,sources[1].read_bytes(),c_source_sha256=C_SOURCE_SHA256)
 need(mixed==b.mixed_source_bytes and transform==r['transform'],'inverse exact same-call source transform')
 for key,content,receipt in [('mixed',b.object_bytes,'raw_mixed_SHA256'),('c5',b.c5_sidecar_bytes,'C5_sidecar_SHA256'),('fa',b.fresh_fa_bytes,'fresh_FA_SHA256'),('composed',b.mixed_source_bytes,'mixed_ASM_SHA256')]:
  need(H(content)==r[receipt]==p['comparison_only_expected_SHA256'][key],'unmodified actual output role '+key)
 return native_objects(read_omf(b.object_bytes),read_omf(b.c5_sidecar_bytes),p['original_units'],reference)

PROFILE_SHA256='3cf1d75f29297af609c65160ae4e12c258f35d139f78591f42099e1891340f4a'
