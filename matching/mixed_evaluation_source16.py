"""Source-only finite two-PROC composition. No native/object/proof reads."""
import hashlib,re
H=lambda b:hashlib.sha256(b).hexdigest()
C_SOURCE_SHA256='822473d561790d51382f54f6ccc0e2b91f8279f7014d4ee33b0e600cb9b8b49a'
SOURCES={'_pawn_bit_count': {'file': 'asm/link/evaluation3902/pawn_bit_count.asm', 'sha256': '576c7d98b12a07a44e7ec6c628ce2e1aaa836adb6a07d024fde1f6ed806e8c29'}, '_evaluate_candidate': {'file': 'asm/link/evaluation3902/evaluate_candidate.asm', 'sha256': 'daa6817283b07efeae64d1384ec470b80c7026bc0a795b3cb7f5172fa338ec1c'}}
ORDER=['_evaluation_abs', '_evaluation_max', '_evaluation_min', '_evaluation_parity', '_evaluate_full', '_pawn_bit_count', '_pawn_score', '_evaluation_piece', '_evaluation_pawn_remove', '_evaluation_pawn_move', '_evaluate_candidate']
def proc(fa,name):
 start=name.encode()+b'\tPROC FAR\r\n';end=name.encode()+b'\tENDP\r\n';assert fa.count(start)==fa.count(end)==1
 a=fa.index(start);z=fa.index(end,a)+len(end);return a,z,fa[a:z]
def compose_fresh(fa,authored,*,c_source_sha256):
 assert type(fa)is bytes and type(authored)is dict and set(authored)==set(SOURCES)and c_source_sha256==C_SOURCE_SHA256
 assert b'\x00'not in fa and b'\x1a'not in fa and fa.count(b'\tTITLE   C:\\UNIT.C\r\n')==1
 assert re.findall(rb'^([^\s;]+)\tPROC FAR\r$',fa,re.M)==[x.encode()for x in ORDER]
 original=[];current=fa
 for name,spec in SOURCES.items():
  source=authored[name];assert type(source)is bytes and H(source)==spec['sha256'];live='\n'.join(x.split(';',1)[0]for x in source.decode('ascii').splitlines())
  assert not re.search(r'\b(?:DB|DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC|EQU)\b',live,re.I)
  first=name.encode()+b'\tPROC FAR\n';last=name.encode()+b'\tENDP\n';assert source.count(first)==source.count(last)==1 and source.endswith(last)
  body=source[source.index(first):].replace(first,name.encode()+b'\tPROC FAR\n',1).replace(last,name.encode()+b'\tENDP\n',1).replace(b'\n',b'\r\n')
  a,z,old=proc(current,name);current=current[:a]+body+current[z:];original.append((name,old,body))
 # Exact known metadata-only MASM declaration projection; all real CV/TYPE remains
 # in the genuine C5 sidecar, not synthetic records in the game object.
 metadata=[]
 for n,k in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  v=(n+"\tSEGMENT  BYTE PUBLIC '"+k+"'\r\n"+n+'\tENDS\r\n').encode();assert current.count(v)==1;current=current.replace(v,b'',1);metadata.append(v)
 # C5 emits PUSH CS followed by a same-segment near CALL for these FAR
 # procedures. MASM cannot infer a forward FAR definition on its first pass.
 # Add the explicit operand distance; preserve the exact preprojection source
 # and require a lossless inverse. Native/C5 byte checks remain downstream.
 unqualified=current;call_projection=[]
 pattern=rb'(\tpush\tcs\r\n\tcall\t)(_[A-Za-z0-9_]+)(\r\n)'
 def qualify(m):
  name=m[2].decode('ascii');assert name in ORDER
  before=m[0];after=m[1]+b'NEAR PTR '+m[2]+m[3]
  call_projection.append({'symbol':name,'before':before,'after':after});return after
 current=re.sub(pattern,qualify,current);assert call_projection
 width_before=b'\tand\tbx,7\r\n';width_after=b'\tand\tbx,WORD PTR 7\r\n'
 assert current.count(width_before)==1 and proc(current,'_evaluate_full')[2].count(width_before)==1
 current=current.replace(width_before,width_after,1)
 inverse=current.replace(width_after,width_before,1)
 for x in call_projection:inverse=inverse.replace(x['after'],x['before'],1)
 assert inverse==unqualified
 for name,old,new in original:assert inverse.count(new)==1;inverse=inverse.replace(new,old,1)
 marker=b'DGROUP\tGROUP\tCONST, _BSS, _DATA\r\n';assert inverse.count(marker)==1;inverse=inverse.replace(marker,b''.join(metadata)+marker,1);assert inverse==fa
 preserved=[]
 for name in ORDER:
  if name not in SOURCES:
   before=proc(fa,name)[2];assert proc(unqualified,name)[2]==before;preserved.append({'symbol':name,'verbatim_PROC_SHA256':H(before)})
 assert current.endswith(b'_evaluate_candidate\tENDP\r\n\tnop\t\r\nUNIT_TEXT\tENDS\r\nEND\r\n')
 return current,{'schema':'evaluation3902-two-PROC-exact-source-inverse-v3','C5_immediate_width_projection':{'symbol':'_evaluate_full','instruction':'and bx,WORD PTR 7','count':1,'inverse_exact':True},'near_call_operand_projection':{'count':len(call_projection),'symbols':[x['symbol']for x in call_projection],'preprojection_C_PROCs_verbatim':True,'inverse_exact':True},'fresh_FA_SHA256':H(fa),'C_source_SHA256':c_source_sha256,'authored_sources':{n:H(v)for n,v in authored.items()},'preserved_C_PROCs':preserved,'composed_SHA256':H(current),'inverse_reconstructs_full_fresh_FA':True,'only_empty_debug_declarations_omitted':4,'code_padding_or_tail_changes':False,'native_oldOBJ_profile_inputs':False}
