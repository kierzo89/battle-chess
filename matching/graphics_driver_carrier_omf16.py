"""Closed whole physical carrier OMF view:12 mnemonic bytes +3604 zero DATA."""
import hashlib
class CarrierError(ValueError):pass
def need(v,s):
 if not v:raise CarrierError(s)
class C:
 def __init__(self,b):self.b=b;self.p=0
 def take(self,n):need(type(n)is int and n>=0 and self.p+n<=len(self.b),'truncated bounded field');x=self.b[self.p:self.p+n];self.p+=n;return x
 def u8(self):return self.take(1)[0]
 def u16(self):return int.from_bytes(self.take(2),'little')
 def index(self):
  n=self.u8();return((n&127)<<8)|self.u8()if n&128 else n
 def name(self):
  b=self.take(self.u8());need(all(32<=x<127 for x in b),'ASCII name');return b.decode()
 def eof(self):need(self.p==len(self.b),'record trailing bytes')
 def __bool__(self):return self.p<len(self.b)
PUBLICS={'_graphics_copy':0,'_graphics_rect_110d_0003':3,'_graphics_pointer_110d_0006':6,'_graphics_pointer_110d_0009':9,'_graphics_driver_colour_110dc':12}
def validate_obj(data):
 need(type(data)is bytes and 0<len(data)<=500000,'whole object size/type');records=[];p=0
 while p<len(data):
  need(len(records)<512 and p+3<=len(data),'raw record count/header');k=data[p];n=int.from_bytes(data[p+1:p+3],'little');need(n>=1 and p+3+n<=len(data),'raw record length');raw=data[p:p+3+n];need(sum(raw)%256==0,'raw checksum');records.append((k,p,raw[3:-1]));p+=3+n
 need(records[0][0]==0x80 and records[0][2]==b'\x08UNIT.ASM'and records[-1][0]==0x8a and records[-1][2]==b'\0','exact header/terminal noentry')
 need(all(k in[0x80,0x88,0x96,0x98,0x90,0xa0,0xa2,0x9c,0x8a]for k,_,_ in records),'unknown/foreign record family')
 for k in[0x80,0x88,0x96,0x98,0x8a]:need(sum(x==k for x,_,_ in records)==1,'exact sole structural record '+hex(k))
 need(1<=sum(k==0x90 for k,_,_ in records)<=5,'bounded PUBLIC records');need([b for k,_,b in records if k==0x88]==[bytes.fromhex('00a201')],'exact MASM directive')
 names=[''];segment=None;pubs={};chunks=[];seen_data=False;nodes=0
 for k,at,b in records:
  c=C(b)
  if k==0x96:
   need(segment is None and not seen_data,'LNAMES order')
   while c:names.append(c.name())
   need(len(names)==4 and set(names[1:])=={'','CODE','GRAPHICS_DRIVER_CARRIER'},'exact consumed names')
  elif k==0x98:
   need(segment is None and not seen_data,'one SEGDEF before DATA');attr,length=c.u8(),c.u16();ni,ci,oi=c.index(),c.index(),c.index();c.eof();need(0<ni<len(names)and 0<ci<len(names)and 0<=oi<len(names),'segment indices');need((attr,length,names[ni],names[ci],names[oi])==(0x60,3616,'GRAPHICS_DRIVER_CARRIER','CODE',''),'whole PRIVATE PARA USE16 CODE3616');segment={'index':1,'attributes':attr,'length':length,'name':names[ni],'class':names[ci],'record_offset':at}
  elif k==0x90:
   need(segment is not None,'PUBLIC after SEGDEF');g,s=c.index(),c.index();need(g==0 and s==1,'ungrouped PUBLIC frame');need(bool(c),'nonempty PUBLIC record')
   while c:
    name,off,typ=c.name(),c.u16(),c.index();need(name in PUBLICS and name not in pubs and off==PUBLICS[name]and typ==0,'exact distinct public coordinate/type');pubs[name]={'segment':1,'offset':off,'type_index':typ,'record_offset':at}
  elif k in[0xa0,0xa2]:
   seen_data=True;need(segment is not None,'DATA after SEGDEF');s,off=c.index(),c.u16();need(s==1 and off<3616,'data segment/offset');budget=3616-off;trees=[]
   if k==0xa0:
    value=c.take(len(c.b)-c.p);need(0<len(value)<=budget,'LEDATA extent')
   else:
    def tree(depth):
     nonlocal nodes
     nodes+=1;need(nodes<=4096 and depth<=8,'LIDATA depth/node limit');start=c.p;repeat,blocks=c.u16(),c.u16();need(repeat>0 and blocks<=256,'LIDATA repeat/block bound');children=[]
     if blocks:
      unit=0
      for _ in range(blocks):
       n,t=tree(depth+1);unit+=n;need(unit<=budget,'LIDATA child expansion bound');children.append(t)
     else:
      n=c.u8();literal=c.take(n);need(n>0 and not any(literal),'LIDATA zero-only nonempty leaf');unit=n
     need(unit>0 and repeat<=budget//unit,'LIDATA multiply/bounds');return unit*repeat,{'payload_start':start,'payload_end':c.p,'repeat':repeat,'blocks':blocks,'unit_bytes':unit,'expanded_bytes':unit*repeat,'children':children}
    count=0
    while c:
     n,t=tree(0);count+=n;need(count<=budget,'LIDATA roots extent');trees.append(t)
    need(count>0,'nonempty LIDATA');value=bytes(count)
   c.eof();need(not any(value[max(0,12-off):]),'nonzero physical DATA after header');chunks.append({'offset':off,'bytes':len(value),'kind':k,'record_offset':at,'raw_payload':b.hex(),'trees':trees,'value':value})
 need(sum(k==0x9c for k,_,_ in records)==1,'exact one self relative FIXUPP record');fixraw=next(b for k,_,b in records if k==0x9c);need(fixraw==b''.join(bytes([0x84,i,0,1,1,0x1d,0x0e])for i in[1,4,7,10]),'four exact self relative OFFSET16 fields/frame1/target1/displacementE1D');need(segment is not None and set(pubs)==set(PUBLICS),'whole segment/five PUBLICs');out=bytearray();header_ownership=[]
 for x in sorted(chunks,key=lambda x:x['offset']):
  need(x['offset']==len(out),'initialized hole/overlap');out.extend(x['value'])
  if x['offset']<12:need(x['kind']==0xa0,'mnemonic instructions must come from literal LEDATA');header_ownership.append([x['offset'],min(12,x['offset']+x['bytes'])])
 need(len(out)==3616 and not any(out[12:]),'whole initialized zero DATA tail');raw_initialized=bytes(out);internal_fields=[]
 for i in[1,4,7,10]:
  need(out[i:i+2]==b'\0\0','zero literal branch addend')
  displacement=3613-(i+2);out[i:i+2]=displacement.to_bytes(2,'little',signed=True);internal_fields.append({'offset':i,'width':2,'frame_segment':1,'target_segment':1,'target_displacement':3613,'self_relative':True,'encoded':out[i:i+2].hex(),'MZ':False})
 branches=[]
 for off in[0,3,6,9]:
  need(out[off]==0xe9,'exact mnemonic E9 near jump');disp=int.from_bytes(out[off+1:off+3],'little',signed=True);target=off+3+disp;need(target==3613,'exact actual private branch landing');branches.append({'offset':off,'mnemonic':'jmp near','signed_displacement':disp,'target_offset':target,'raw':out[off:off+3].hex()})
 for x in chunks:x.pop('value')
 return bytes(out),{'whole_object_sha256':hashlib.sha256(data).hexdigest(),'whole_object_bytes':len(data),'records':[{'kind':k,'file_offset':at,'payload':b.hex()}for k,at,b in records],'names':names,'segment':segment,'publics':pubs,'initialized_records':chunks,'mnemonic_instructions':branches,'header_literal_ownership':header_ownership,'mnemonic_bytes':12,'physical_zero_DATA_bytes':3604,'initialized_total':3616,'internal_fixups':4,'internal_fields':internal_fields,'raw_initialized_sha256':hashlib.sha256(raw_initialized).hexdigest(),'internal_MZ':[],'procedures':0,'C_credit':0,'historical_storage_or_capacity_proven':False,'classification':'mixed_physical_driver_carrier'}
