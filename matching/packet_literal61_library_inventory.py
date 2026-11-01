"""Exact prior strict full-library CONST inventory, comparison-only."""
from omf import _Cursor
from packet_literal61 import need,H
def library_CONSTs(raw):
 need(raw[0]==0xf0,'LIBHDR');page=int.from_bytes(raw[1:3],'little')+3;end=int.from_bytes(raw[3:7],'little');need(page>=16 and page&(page-1)==0 and page<=end<=len(raw),'library page/dictionary');pos=page;out=[];members=0
 while pos<end and raw[pos]!=0xf1:
  need(raw[pos]==0x80,'page-aligned THEADR');start=pos;names=[''];segs=[];pub=[];label=None;members+=1
  while True:
   need(pos+3<=end,'whole recordheader');kind=raw[pos];n=int.from_bytes(raw[pos+1:pos+3],'little');stop=pos+n+3;need(n>=1 and stop<=end and sum(raw[pos:stop])&255==0,'whole checksummed library record');c=_Cursor(raw[pos+3:stop-1]);pos=stop
   if kind==0x80:label=c.name()
   if kind==0x96:
    while c:names.append(c.name())
   if kind==0x98:
    attrs=c.byte()
    if attrs>>5==0:c.take(3)
    size=c.word();name,cls=names[c.index()],names[c.index()];c.index()
    if attrs&2 and size==0:size=65536
    if name=='CONST'or cls=='CONST':segs.append({'name':name,'class':cls,'length':size,'attributes':attrs})
   if kind==0x90:
    group,seg=c.index(),c.index()
    if seg==0:c.word()
    while c:pub.append(c.name());c.word();c.index()
   if kind==0x8a:break
  if segs:out.append({'member':label,'library_offset':start,'raw_sha256':H(raw[start:pos]),'CONST_segments':segs,'PUBLICs':pub})
  pos=(pos+page-1)//page*page
 return {'member_count':members,'CONST_members':out}
