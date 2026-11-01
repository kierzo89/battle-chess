"""Closed five-view workspace53184+32816 OMF ownership model.
Distinct exact five-PUBLIC profile; old two/three-PUBLIC decoders remain unchanged.
"""
import hashlib
class DataError(ValueError):pass
def need(v,s):
 if not v:raise DataError(s)
class C:
 def __init__(self,b):self.b=b;self.p=0
 def take(self,n):need(type(n)is int and n>=0 and self.p+n<=len(self.b),'truncated bounded field');x=self.b[self.p:self.p+n];self.p+=n;return x
 def u8(self):return self.take(1)[0]
 def u16(self):return int.from_bytes(self.take(2),'little')
 def index(self):
  n=self.u8();return((n&127)<<8)|self.u8()if n&128 else n
 def name(self):
  x=self.take(self.u8());need(all(32<=b<127 for b in x),'nonASCII name');return x.decode()
 def eof(self):need(self.p==len(self.b),'trailing record bytes')
 def __bool__(self):return self.p<len(self.b)
NAMES=['GRAPHICS_WORKSPACE_0','GRAPHICS_WORKSPACE_1'];SIZES=[53184,32816];PUBLICS={'_graphics_workspace':(1,0),'_color_buffer':(1,13024),'_region_buffer':(1,16272),'_metadata_workspace':(1,52332),'_splash_buffer':(2,0)}
def validate_obj(data):
 need(isinstance(data,bytes)and 0<len(data)<=2000000,'whole object size/type');p=0;records=[]
 while p<len(data):
  need(len(records)<2048 and p+3<=len(data),'record limit/header');kind=data[p];n=int.from_bytes(data[p+1:p+3],'little');need(n>=1 and p+3+n<=len(data),'raw record length');raw=data[p:p+3+n];need(sum(raw)%256==0,'raw checksum');records.append((kind,p,raw[3:-1]));p+=3+n
 need(records[0][0]==0x80 and records[0][2]==b'\x08UNIT.ASM','exact first THEADR');need(records[-1][0]==0x8a and records[-1][2]==b'\0','exact terminal no-entry MODEND');need(sum(k==0x80 for k,_,_ in records)==sum(k==0x8a for k,_,_ in records)==1,'duplicate/multiple modules')
 allowed={0x80,0x88,0x96,0x98,0x90,0xa0,0xa2,0x8a};need(all(k in allowed for k,_,_ in records),'unknown/foreign record family');comments=[b for k,_,b in records if k==0x88];need(comments==[bytes.fromhex('00a201')],'exact sole MASM OMF directive')
 need(sum(k==0x96 for k,_,_ in records)==1 and sum(k==0x90 for k,_,_ in records)==2,'exact one LNAMES/two PUBLIC records');names=[''];segs=[];pubs={};chunks=[];nodes=0;roots=[];seen_data=False;public_segments=[]
 for kind,at,b in records:
  c=C(b)
  if kind==0x96:
   need(not seen_data and not segs,'LNAMES must precede SEGDEF/data')
   while c:names.append(c.name())
  elif kind==0x98:
   need(not seen_data and len(segs)<2,'SEGDEF ordering/count');attr=c.u8();length=c.u16();ni,ci,oi=c.index(),c.index(),c.index();c.eof();need(attr==0x60,'exact PRIVATE PARA16 nonbig segment');need(0<ni<len(names)and 0<ci<len(names)and 0<=oi<len(names),'SEGDEF name indices');need(names[ni]==NAMES[len(segs)]and names[ci]=='FAR_DATA'and names[oi]=='','exact segment/class/overlay');need(length==SIZES[len(segs)],'exact complete segment length');segs.append({'index':len(segs)+1,'name':names[ni],'class':'FAR_DATA','attributes':attr,'length':length,'record_offset':at})
  elif kind==0x90:
   need(len(segs)==2,'PUBDEF after complete SEGDEFs');group,seg=c.index(),c.index();need(bool(c),'empty PUBLIC record');need(seg not in public_segments,'duplicate PUBLIC segment record');public_segments.append(seg);need(group==0 and seg in[1,2],'ungrouped DATA public')
   while c:
    name,off,typ=c.name(),c.u16(),c.index();need(name not in pubs and name in PUBLICS,'extra/duplicate/alias PUBLIC');need((seg,off)==PUBLICS[name]and typ==0,'exact PUBLIC coordinate/type');pubs[name]={'segment':seg,'offset':off,'type_index':typ,'record_offset':at}
  elif kind in[0xa0,0xa2]:
   seen_data=True;need(len(segs)==2,'complete SEGDEFs before DATA');seg,off=c.index(),c.u16();need(seg in[1,2]and off<SIZES[seg-1],'data segment/offset');budget=SIZES[seg-1]-off
   if kind==0xa0:
    raw=c.take(len(c.b)-c.p);need(0<len(raw)<=budget and not any(raw),'LEDATA nonzero/empty/extent');expanded=len(raw);trees=[]
   else:
    def tree(depth):
     nonlocal nodes
     nodes+=1;need(nodes<=4096 and depth<=8,'LIDATA node/depth limit');start=c.p;repeat,blocks=c.u16(),c.u16();need(repeat>0 and blocks<=256,'LIDATA repeat/block bound');children=[]
     if blocks:
      unit=0
      for _ in range(blocks):
       v,child=tree(depth+1);unit+=v;need(unit<=budget,'LIDATA child expansion budget');children.append(child)
     else:
      n=c.u8();raw=c.take(n);need(n>0 and not any(raw),'LIDATA nonzero/empty leaf');unit=n
     need(unit>0 and repeat<=budget//unit,'LIDATA multiplication/segment bound');return repeat*unit,{'payload_start':start,'payload_end':c.p,'repeat':repeat,'blocks':blocks,'unit_bytes':unit,'expanded_bytes':repeat*unit,'children':children}
    expanded=0;trees=[]
    while c:
     n,t=tree(0);expanded+=n;need(expanded<=budget,'LIDATA roots segment bound');trees.append(t)
    need(expanded>0,'empty LIDATA')
   c.eof();chunks.append({'segment':seg,'offset':off,'bytes':expanded,'kind':kind,'record_offset':at,'raw_payload':b.hex(),'trees':trees})
 need(sorted(public_segments)==[1,2],'complete two PUBLIC segment records');need(len(segs)==2 and pubs.keys()==PUBLICS.keys(),'complete2segments/5PUBLICs');need(set(names[1:])=={'',*NAMES,'FAR_DATA'}and len(names)==5,'exact consumed LNAMES inventory')
 outputs=[]
 for seg in[1,2]:
  selected=sorted((r for r in chunks if r['segment']==seg),key=lambda r:r['offset']);p=0
  for r in selected:need(r['offset']==p,'data hole/overlap');p+=r['bytes']
  need(p==SIZES[seg-1],'uninitialized/extra tail');outputs.append(bytes(p))
 need(sum(map(len,outputs))==86000,'whole complete decoded extent');meta={'whole_object_sha256':hashlib.sha256(data).hexdigest(),'whole_object_bytes':len(data),'records':[{'kind':k,'file_offset':at,'payload':b.hex()}for k,at,b in records],'names':names,'segments':segs,'publics':pubs,'initialized_records':chunks,'expanded_bytes':86000,'fixups':0,'native_MZ':[],'C_functions':0,'C_DATA':0,'historical_capacity_claim':False}
 return outputs,meta
