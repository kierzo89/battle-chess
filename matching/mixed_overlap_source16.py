import hashlib,re
H=lambda b:hashlib.sha256(b).hexdigest()
RECIPES={'9cfe972686121e02c8fce86ab10054c5cd45073e2cae4cef7b85974a5fa94d94': {'kind': 'input', 'C_SOURCE': 'src/input_mixed_context_match.c', 'ASM_SOURCE': 'asm/link/input_mixed_authored.asm', 'C_SOURCE_SHA256': '9cfe972686121e02c8fce86ab10054c5cd45073e2cae4cef7b85974a5fa94d94', 'DECODER_SOURCE_SHA256': 'da828231573e897db2f00160463f33e373e0daa3371152c986e6fa16f4906bf0', 'markers': ['_next_event_184d\tPROC NEAR']}, 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9': {'kind': 'motion', 'C_SOURCE': 'src/motion_mixed_context_match.c', 'ASM_SOURCE': 'asm/link/motion_mixed_authored.asm', 'C_SOURCE_SHA256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9', 'DECODER_SOURCE_SHA256': '953dbe20cad21a8a8c0202ddb2343f2fbe6d5a3fbedf66fb62690d45cc612dba', 'markers': ['_offset_task_70ef\tPROC NEAR', '_TEXT\tENDS\r\nEND\r\n']}}
def body(asm):
 a=re.search(rb'^PUBLIC ',asm,re.M).start();z=asm.rindex(b' ENDP')+len(b' ENDP');return asm[a:z]+b'\n'
def compose(fa, additions):
 original=fa;ops=[]
 def edit(old,new):
  nonlocal fa
  assert fa.count(old)==1,(old,fa.count(old));at=fa.index(old);ops.append((at,old,new));fa=fa[:at]+new+fa[at+len(old):]
 for name,kind in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  edit((name+"\tSEGMENT  BYTE PUBLIC '"+kind+"'\r\n"+name+'\tENDS\r\n').encode(),b'')
 tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n'
 if fa.endswith(tail):edit(tail,b'_TEXT\tENDS\r\nEND\r\n')
 procs=set(re.findall(rb'^(_\w+)\s+PROC ',fa,re.M));external=set(re.findall(rb'EXTRN\s+(\w+):',fa))
 for marker,asm in additions:
  data=[];code=[];indata=False
  for line in asm.splitlines():
   if line.startswith(b'_DATA SEGMENT'):indata=True
   if line.startswith(b'_DATA ENDS'):indata=False
   if line.startswith(b'EXTRN '):
    for name,typ in re.findall(rb'(\w+):(\w+)',line):
     if name in external or name in procs:continue
     external.add(name);(data if indata else code).append(name+b':'+typ)
  if data:edit(b"_DATA\tSEGMENT  WORD PUBLIC 'DATA'\r\n",b"_DATA\tSEGMENT  WORD PUBLIC 'DATA'\r\n"+b''.join(b'EXTRN '+x+b'\r\n' for x in data))
  if code:edit(b'EXTRN\t__acrtused:ABS\r\n',b'EXTRN\t__acrtused:ABS\r\n'+b''.join(b'EXTRN '+x+b'\r\n' for x in code))
  old=marker;new=body(asm).replace(b'\n',b'\r\n')+b'\r\n'+marker;edit(old,new)
 if b'_select_mode' in b''.join(x[1] for x in additions):
  old=b'\trep\tmovsw\r\n';new=b'\trepne\tmovsw\r\n';assert fa.count(old)==3
  for _ in range(3):
   at=fa.index(old);ops.append((at,old,new));fa=fa[:at]+new+fa[at+len(old):]
 # Complete original FA can be recovered, including EOF nop. Only the module
 # boundary changes: compiler functions and authored instruction bodies stay verbatim.
 tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n'
 if fa.endswith(tail):edit(tail,b'\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n')
 elif fa.endswith(b'_TEXT\tENDS\r\nEND\r\n'):edit(b'_TEXT\tENDS\r\nEND\r\n',b'\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n')
 else:raise ValueError('Unknown EOF')
 inverse=fa
 for at,old,new in reversed(ops):assert inverse[at:at+len(new)]==new;inverse=inverse[:at]+old+inverse[at+len(new):]
 assert inverse==original
 return fa,{'inverse_recovers_complete_FA':True,'operations':len(ops),'FA_sha256':H(original),'mixed_sha256':H(fa),'canonical_credit_added':0}


def compose_fresh(fa,asm,*,c_source_sha256):
 assert c_source_sha256 in RECIPES
 r=RECIPES[c_source_sha256];assert H(asm)==r['DECODER_SOURCE_SHA256']
 parts=asm.split(b'\n; SECOND_AUTHORED_SOURCE_BOUNDARY\n');assert len(parts)==len(r['markers'])
 result,proof=compose(fa,[(m.encode(),a) for m,a in zip(r['markers'],parts)])
 proof.update(transform='reviewed-mixed-overlap-source-v1',kind=r['kind'],ASM_sha256=H(asm),C_source_sha256=c_source_sha256,dialect_normalizations=3 if r['kind']=='input' else 0)
 return result,proof
