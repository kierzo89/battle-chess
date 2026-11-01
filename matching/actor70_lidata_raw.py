"""Closed read-only Actor70 genuine C5 LIDATA view. No parser/object changes."""
import hashlib,dataclasses
from omf import read_omf,_Cursor
from runtime_lidata16 import initialized_view,POLICY,decode_blocks
RAW_SHA='8d1acf0a7237d4d54dce04fe715df095db93615feefacb40253e3204c9c36e2e'
H=lambda b:hashlib.sha256(b).hexdigest()
def validate(raw):
 assert type(raw)is bytes and len(raw)==545 and H(raw)==RAW_SHA,'closed genuine Actor object identity'
 o=read_omf(raw);assert not o.fixups and not o.procedures and o.externals=={1:'__acrtused'}and set(o.publics)=={'_actors'}
 assert [(s.index,s.name,s.class_name,s.attributes,s.length)for s in o.segments.values()]==[(1,'_TEXT','CODE',72,0),(2,'_DATA','DATA',72,1960),(3,'CONST','CONST',72,0),(4,'_BSS','BSS',72,0),(5,'$$SYMBOLS','DEBSYM',32,0),(6,'$$TYPES','DEBTYP',32,269)]
 assert o.segments[2].chunks==[(0,b'\0\0')]and o.segments[2].unsupported_data
 before=repr(o);v=initialized_view(o,2,policy=POLICY);assert repr(o)==before
 assert [(w['record_offset'],w['record_kind'],w['offset'],w['size'],w['encoded_bytes'])for w in v.records]==[(241,0xa0,0,2,2),(250,0xa2,2,1958,7)]
 assert v.iterated_ranges==((2,1960),)and v.data==bytes(1960)
 tree=v.records[1]['blocks'];assert tree==[{'encoded_start':0,'repeat':979,'child_blocks':0,'literal_hex':'0000','encoded_end':7,'expanded_bytes':1958}]
 assert [(k,a,p.hex())for k,a,p in o.records if k==0xa2]==[(0xa2,250,'020200d3030000020000')]
 assert[p.hex()for k,a,p in o.records if k==0x9c]==['000301020201030440014501']
 assert all(k in{0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0x90,0xa0,0xa2,0x8a}for k,a,p in o.records)
 assert[p.hex()for k,a,p in o.records if k==0x88]==['009d30734f','00a1014356','00a201'];assert[p.hex()for k,a,p in o.records if k==0x9a]==['02ff03ff04ff02'];assert[p.hex()for k,a,p in o.records if k==0x8c]==['0a5f5f616372747573656401'];assert[p.hex()for k,a,p in o.records if k==0x8a]==['00']
 headers=[p for k,a,p in o.records if k==0x80];assert len(headers)==1;c=_Cursor(headers[0]);assert c.name()=='C:\\UNIT.C';c.finish()
 pub=o.publics['_actors'];assert(pub.group,pub.segment,pub.offset)==(1,2,0)
 tb=b''.join(p for off,p in o.segments[6].chunks);assert len(tb)==269;nodes={};at=0;i=0x200
 while at<len(tb):
  assert tb[at]==1;n=int.from_bytes(tb[at+1:at+3],'little');p=tb[at+3:at+3+n];assert n>0 and len(p)==n;nodes[i]=p;at+=3+n;i+=1
 assert at==len(tb)
 def num(p,at):
  tag=p[at];at+=1
  if tag<0x80:return tag,at
  assert tag==0x85;return int.from_bytes(p[at:at+2],'little'),at+2
 def ref(p,at):assert p[at]==0x83;return int.from_bytes(p[at+1:at+3],'little'),at+3
 ar=nodes[pub.type_index];assert ar[0]==0x78;bits,at=num(ar,1);element,at=ref(ar,at);assert bits==15680 and at==len(ar)
 st=nodes[element];assert st[0]==0x79;size,at=num(st,1);count,at=num(st,at);ti,at=ref(st,at);ni,at=ref(st,at);assert(size,count)==(224,14)and st[at:]==b'\x82\x05Actori'
 tt=nodes[ti];nn=nodes[ni];assert tt[0]==nn[0]==0x7f;types=[];at=1
 for _ in range(14):t,at=ref(tt,at);types.append(t)
 assert at==len(tt);names=[];offsets=[];at=1
 for _ in range(14):
  assert nn[at]==0x82;n=nn[at+1];names.append(nn[at+2:at+2+n].decode());at+=2+n;assert nn[at]==0x88;offsets.append(nn[at+1]);at+=2
 assert at==len(nn)and names==['x','y','old_x','old_y','flag','colour','square','left','right','top','bottom','frame','resource','next']and offsets==[0,2,4,6,8,10,11,12,14,16,18,20,22,26]
 assert types[:11]==[0x81]*5+[0x84]*2+[0x81]*4;pointers=[]
 for idx,cl,name in zip(types[11:],[0x74,0x73,0x74],['Frame','','Actor']):
  p=nodes[idx];assert p[:2]==bytes([0x7a,cl]);target,at=ref(p,2);assert p[at:]==bytes([0x82,len(name)])+name.encode()
  if name=='Frame':assert nodes[target]==b'\x80'
  elif name=='Actor':assert target==element
  else:assert target==0x85
  pointers.append({'type_index':idx,'pointer_class':cl,'target_type':target,'name':name,'raw':p.hex()})
 semantic={pub.type_index,element,ti,ni,*types[11:]};assert all(k in semantic or p==b'\x80'for k,p in nodes.items())
 return v.data,{'raw_sha256':H(raw),'raw_bytes':len(raw),'literal_bytes':2,'iterated_bytes':1958,'hole_fill_bytes':0,'writers':list(v.records),'iterated_ranges':list(v.iterated_ranges),'PUBLIC':dataclasses.asdict(pub),'TYPE_graph':{hex(k):p.hex()for k,p in nodes.items()},'ARRAY_bits':bits,'STRUCT_bits':size,'field_names':names,'field_offsets':offsets,'field_types':types,'pointer_graph':pointers,'no_object_mutation':True,'location_FIXUPPs':0,'source_MZ':[],'record_inventory':[{'kind':k,'offset':a,'payload_sha256':H(p)}for k,a,p in o.records]}
