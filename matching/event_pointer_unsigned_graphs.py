"""Read-only exact CV3 near-pointer pointee graphs used by active event clients."""
from omf import OMFError,_Cursor

def need(v,s):
 if not v:raise OMFError(s)
def full(seg):
 b=bytearray(seg.length);seen=set()
 for at,x in seg.chunks:need(0<=at<=at+len(x)<=len(b),'Event CV bounds');b[at:at+len(x)]=x;seen.update(range(at,at+len(x)))
 need(len(seen)==len(b),'Event CV hole');return bytes(b)
def tables(obj):
 s=next(s for s in obj.segments.values()if s.class_name=='DEBTYP');b=full(s);p=0;t={};i=0x200
 while p<len(b):need(b[p]==1,'Event TYPE framing');n=int.from_bytes(b[p+1:p+3],'little');need(n>0 and p+3+n<=len(b),'Event TYPE bound');t[i]=b[p+3:p+3+n];p+=3+n;i+=1
 return t

def pointer_graph(obj,symbol):
 t=tables(obj);seg=next(s for s in obj.segments.values()if s.class_name=='DEBSYM');b=full(seg);pos=0;roots=[]
 while pos<len(b):
  n=b[pos]+1;need(n>=2 and pos+n<=len(b),'Event CV symbol framing');rec=b[pos:pos+n]
  if rec[1]==5:
   refs=[f for f in obj.fixups if f.segment==seg.index and f.offset==pos+2 and f.width==4 and f.target[0]==2 and obj.externals.get(f.target[1])==symbol]
   if refs:need(len(refs)==1 and len(rec)>=9 and rec[8]+9==len(rec)and rec[9:].decode()==symbol[1:],'Event CV global identity');roots.append(int.from_bytes(rec[6:8],'little'))
  pos+=n
 need(len(roots)==1,'Event unique typed global required')
 def number(c):
  n=c.byte()
  if n<0x80:return n
  need(n==0x85,'Event CV numeric leaf');return c.word()
 def ref(c):need(c.byte()==0x83,'Event CV type reference');return c.word()
 def graph(i,seen=frozenset()):
  if i<0x200:return {'primitive':i}
  need(i in t and i not in seen,'Event undefined/recursive graph');c=_Cursor(t[i]);tag=c.byte();seen=seen|{i}
  if tag==0x7a:
   need(c.byte()==0x74,'Event pointer must be genuine near data pointer');child=graph(ref(c),seen);need(c.take(len(c.data)-c.pos)==b'\x82\0','Event pointer qualifiers');return {'pointer':'near','to':child}
  if tag==0x78:
   bits=number(c);child=graph(ref(c),seen);c.finish();return {'array_bits':bits,'element':child}
  need(tag==0x79,'Event pointee must be struct');bits=number(c);count=c.byte();ti,ni=ref(c),ref(c);need(c.take(len(c.data)-c.pos)==b'\x82\0\x69','Event anonymous struct qualifiers')
  q=_Cursor(t[ti]);need(q.byte()==0x7f,'Event member type list');members=[]
  while q:members.append(graph(ref(q),seen))
  q=_Cursor(t[ni]);need(q.byte()==0x7f,'Event member name list');names=[]
  while q:
   need(q.byte()==0x82,'Event member name');name=q.name();need(q.byte()==0x88,'Event member offset');names.append((name,q.byte()))
  need(len(members)==len(names)==count,'Event member counts');return {'struct_bits':bits,'members':[{'name':n,'offset':o,'type':v}for(n,o),v in zip(names,members)]}
 result=graph(roots[0]);need(result.get('pointer')=='near','Event near pointer root required');return result
