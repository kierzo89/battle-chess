"""Narrow inert raw-OMF closure checks, additive to all frozen comparisons.

No compiler, linking, rewriting, source/name model adaptation or credit. A
provider's type index is read from the genuine bytes; no future hash is guessed.
"""
from collections import Counter
from omf import read_omf,_Cursor
RENAME={'_counts':'_side_piece_counts'}
CLIENT_KINDS={0x80,0x88,0x96,0x98,0x9a,0x8c,0x90,0x94,0x9c,0xa0,0x8a}
PROVIDER_KINDS={0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a}
def require(v,m):
 if not v:raise ValueError('counts raw closure: '+m)
def bykind(o,k):return[p for kind,at,p in o.records if kind==k]
def payload(o,i):
 s=o.segments[i];out=bytearray(s.length);seen=set()
 for at,b in s.chunks:
  require(0<=at<=at+len(b)<=s.length,'payload bounds')
  require(s.class_name=='DEBSYM'or not seen.intersection(range(at,at+len(b))),'nondebug overlap');out[at:at+len(b)]=b;seen.update(range(at,at+len(b)))
 require(len(seen)==s.length and not s.unsupported_data,'complete payload');return bytes(out)
def extdefs(o):
 out=[]
 for b in bykind(o,0x8c):
  c=_Cursor(b)
  while c:out.append((c.name(),c.index()))
 require(len(out)==len({n for n,t in out}),'duplicate EXTDEF name');return out
def public_tuples(o):
 out=[]
 for p in bykind(o,0x90):
  c=_Cursor(p);group,segment=c.index(),c.index();frame=c.word()if segment==0 else None
  while c:out.append((group,segment,frame,c.name(),c.word(),c.index()))
 require(len(out)==len({r[3]for r in out}),'duplicate PUBDEF name')
 return Counter(out)
def validate_client_module(before,after):
 b=read_omf(before);o=read_omf(after)
 require(set(b.segments)==set(o.segments)=={1,2,3,4,5,6},'client exact six segments')
 require(all(k in CLIENT_KINDS for k,at,p in b.records+o.records),'client unsupported/additional record class')
 # The existing comparator already checks every segment payload/length and
 # permits only the exact +11-byte DEBSYM change. This closes the set too.
 require([(s.index,s.name,s.class_name,s.attributes,s.name_index,s.class_index,s.overlay_index)for s in b.segments.values()]==[(s.index,s.name,s.class_name,s.attributes,s.name_index,s.class_index,s.overlay_index)for s in o.segments.values()],'client exact segment identities')
 # Debug LEDATA/FIXUPP record packing and EXTDEF ordering may change honestly.
 # All structural records outside those families retain exact semantics/bytes.
 for k in [0x80,0x88,0x96,0x9a,0x94,0x8a]:require(bykind(b,k)==bykind(o,k),'client structural record '+hex(k))
 require(public_tuples(b)==public_tuples(o),'client exact decoded PUBDEF tuples')
 require(len(bykind(b,0x98))==len(bykind(o,0x98))==6,'client exact SEGDEF records')
 a=extdefs(b);c=extdefs(o);expected=Counter((RENAME.get(n,n),t)for n,t in a)
 # Canonicalize comparison tuples only; neither raw object is rewritten.
 # The frozen full comparator separately requires actual renamed targets.
 actual=Counter((RENAME.get(n,n),t)for n,t in c);require(actual==expected,'client exact observed EXTDEF name/type bijection')
 return {'segments':6,'no_added_COMMON_or_directives':True,'structural_records_exact':True,'no_object_model_mutation':True}
def validate_provider_module(raw):
 o=read_omf(raw);require(all(k in PROVIDER_KINDS for k,at,p in o.records),'provider unsupported record class')
 require(not o.publics and not o.procedures,'provider no PUBLIC/procedure')
 require(set(o.segments)=={1,2,3,4,5,6},'provider exact six segments')
 require([(s.name,s.class_name,s.attributes)for s in o.segments.values()]==[('_TEXT','CODE',72),('_DATA','DATA',72),('CONST','CONST',72),('_BSS','BSS',72),('$$SYMBOLS','DEBSYM',32),('$$TYPES','DEBTYP',32)],'provider standard segment identities')
 for i in[1,2,3,4]:s=o.segments[i];require(s.length==0 and not s.chunks and not s.unsupported_data,'provider no loaded allocation/bytes')
 require(o.names==['','','DGROUP','_TEXT','CODE','_DATA','DATA','CONST','_BSS','BSS','$$TYPES','DEBTYP','$$SYMBOLS','DEBSYM'],'provider exact LNAMES')
 require(bykind(o,0x80)==[bytes.fromhex('09433a5c554e49542e43')]and bykind(o,0x88)==[bytes.fromhex(x)for x in['009d30734f','00a1014356','00a201']]and bykind(o,0x9a)==[bytes.fromhex('02ff03ff04ff02')]and bykind(o,0x8a)==[b'\0'],'provider exact header/comments/group/MODEND')
 require(len(bykind(o,0x98))==6 and len(bykind(o,0x96))==1,'provider closed structural record counts')
 ds=[]
 for b in bykind(o,0xb0):
  q=_Cursor(b)
  while q:ds.append((q.name(),q.index(),q.byte(),q.byte()))
 require(len(bykind(o,0xb0))==1 and len(ds)==1 and ds[0][0]=='_side_piece_counts'and ds[0][2:]==(98,4),'provider sole near COMMON4')
 require(extdefs(o)==[('__acrtused',1)]and o.externals=={1:'__acrtused',2:'_side_piece_counts'},'provider exact external dependencies')
 types={};b=payload(o,6);at=0
 while at<len(b):
  require(at+3<=len(b)and b[at]==1,'provider type header');n=int.from_bytes(b[at+1:at+3],'little');require(n>0 and at+3+n<=len(b),'provider complete type bounds');types[512+len(types)]=b[at+3:at+3+n];at+=3+n
 t=ds[0][1];require(types.get(t)==bytes.fromhex('7820838100')and all(k==t or v==b'\x80'for k,v in types.items()),'provider exact observed int[2] graph and placeholder-only unused records')
 b=payload(o,5);name=b'side_piece_counts';require(len(b)==26 and b[0]==25 and b[1]==5 and b[2:6]==b'\0'*4 and int.from_bytes(b[6:8],'little')==t and b[8]==len(name)and b[9:]==name,'provider sole complete matching global CV record')
 require(len(o.fixups)==1,'provider sole debug address field');f=o.fixups[0];require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,2,4,3,True,(5,None),(2,2),None),'provider exact global FAR debug address identity')
 require(all(i in[5,6]for at,i,off,n in o.data_writes),'provider only debug writes')
 return {'symbol':ds[0][0],'size':4,'type_index_observed':t,'type_graph':'7820838100','global_record':b.hex(),'debug_fields':1,'loaded_bytes':0,'matching_credit':0}
