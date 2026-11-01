import re,hashlib
H=lambda b:hashlib.sha256(b).hexdigest()
RECIPES={'attacks528': {'C_SOURCE': 'src/attacks_neighbors_match.c', 'ASM_SOURCE': 'asm/link/init_rays9840.asm', 'parts': [{'source': 'src/attacks_neighbors_match.c', 'flags': ['/AS', '/Zi'], 'owners': ['piece_attacks_98f9', 'pawn_attacks_99be'], 'sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd'}], 'DECODER_SOURCE_SHA256': 'b71de6aca2db4a609e21b31e6c1552b519d12be5e8e3dbfef66813346db52caf', 'C_SOURCE_SHA256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd'}, 'display860': {'C_SOURCE': 'src/display_queue_neighbors_match.c', 'ASM_SOURCE': 'asm/link/animate_move78f6.asm', 'parts': [{'source': 'src/display_queue_neighbors_match.c', 'flags': ['/AS', '/Zi'], 'owners': ['redraw_piece_7a61', 'queue_piece_7aa7'], 'sha256': 'e1d6a7e8c1d4e19dfb68c966f1094547c26e065261c491157c8571fc5fceae37'}, {'source': 'src/display_history_flow_match.c', 'flags': ['/AS', '/Gs', '/Os', '/Zi'], 'owners': ['reset_display_7b86', 'select_display_7ba4', 'init_display_7bc2', 'trim_history_7bf9'], 'sha256': '5255e557e42e4d1ef1a0c577f5a563478d1349e8f41ec82c63585d525e7f5413'}], 'DECODER_SOURCE_SHA256': '60ac7430e073061e15d2d081cbcd8c69741255cd1b68df31ffcec7d065a2907e', 'C_SOURCE_SHA256': 'e1d6a7e8c1d4e19dfb68c966f1094547c26e065261c491157c8571fc5fceae37'}}
def attacks(fa,authored):
 tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n';assert fa.endswith(b'_pawn_attacks\tENDP\r\n'+tail)and fa.count(b'\tnop\t\r\n')==1
 a=authored.index(b'PUBLIC _init_rays\n');b=authored.index(b'_init_rays ENDP')+len(b'_init_rays ENDP');body=(authored[a:b]+b'\n').replace(b'\n',b'\r\n')
 ops=[];src=fa[:-len(tail)]
 for name,kind in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  old=(name+"\tSEGMENT  BYTE PUBLIC '"+kind+"'\r\n"+name+'\tENDS\r\n').encode();assert src.count(old)==1;at=src.index(old);ops.append((at,old,b''));src=src[:at]+src[at+len(old):]
 for marker,added in [(b'EXTRN\t__acrtused:ABS\r\n',b'EXTRN _fill_8a96:NEAR\r\n'),(b'_piece_attacks\tPROC NEAR\r\n',body)]:
  assert src.count(marker)==1;at=src.index(marker)+(len(marker)if marker!=b'_piece_attacks\tPROC NEAR\r\n'else 0);ops.append((at,b'',added));src=src[:at]+added+src[at:]
 result=src+b'\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n';inverse=src
 for at,old,new in reversed(ops):assert inverse[at:at+len(new)]==new;inverse=inverse[:at]+old+inverse[at+len(new):]
 assert inverse+tail==fa;assert fa[fa.index(b'_piece_attacks\tPROC NEAR'):len(fa)-len(tail)]in result
 return result,{'exact_inverse':True,'C_procedures_verbatim':True,'authored_ASM_verbatim':body in result,'tail_alignment_deferred_to_whole_EVEN':True}

def display(q,d,a):
 qt=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n';dt=b'_TEXT\tENDS\r\nEND\r\n';assert q.endswith(qt)and d.endswith(dt)
 body=d[d.index(b'\tPUBLIC\t_reset_display\r\n'):-len(dt)];labels=sorted(set(re.findall(rb'\$[A-Z]+[0-9]+',body)),key=len,reverse=True);converted=body
 for label in labels:converted=re.sub(rb'(?<![A-Za-z0-9_$])'+re.escape(label)+rb'(?![A-Za-z0-9_$])',b'D'+label,converted)
 inverse=converted
 for label in labels:inverse=inverse.replace(b'D'+label,label)
 assert inverse==body
 start=a.index(b'PUBLIC _animate_move\n');end=a.index(b'_animate_move ENDP')+len(b'_animate_move ENDP');prefix=(a[start:end]+b'\n').replace(b'\n',b'\r\n');src=q[:-len(qt)];ops=[]
 old=b'\tand\tcx,7\r\n';new=b'\tand\tcx,FULLWORD_MASK7\r\n';assert src.count(old)==1;at=src.index(old);ops.append((at,old,new));src=src[:at]+new+src[at+len(old):]
 for name,kind in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  old=(name+"\tSEGMENT  BYTE PUBLIC '"+kind+"'\r\n"+name+'\tENDS\r\n').encode();assert src.count(old)==1;at=src.index(old);ops.append((at,old,b''));src=src[:at]+src[at+len(old):]
 extra=b''.join(line+b'\r\n'for line in d.split(b'\r\n')if line.startswith(b'EXTRN')and b'__acrtused'not in line)+b'EXTRN _detach_actor:NEAR, _undo_animation:NEAR\r\n'
 for marker,added,before in [(b'EXTRN\t__acrtused:ABS\r\n',extra,False),(b'\tPUBLIC\t_redraw_piece\r\n',prefix,True)]:
  assert src.count(marker)==1;at=src.index(marker)+(0 if before else len(marker));ops.append((at,b'',added));src=src[:at]+added+src[at:]
 composed=src+converted+b'\tEVEN\r\n_TEXT\tENDS\r\nFULLWORD_MASK7 EQU 7\r\nEND\r\n';inverse=src
 for at,old,new in reversed(ops):assert inverse[at:at+len(new)]==new;inverse=inverse[:at]+old+inverse[at+len(new):]
 assert inverse+qt==q;assert d[:d.index(body)]+body+dt==d
 return composed,{'exact_inverse_both_FA':True,'local_label_renames':{x.decode():'D'+x.decode()for x in labels},'C5_immediate_width_spelling':'and cx,7 -> forward FULLWORD_MASK7 EQU7','authored_ASM_verbatim':prefix in composed}

def compose_fresh(fas,asm,*,kind,source_hashes):
 r=RECIPES[kind]
 assert source_hashes==[p['sha256']for p in r['parts']] and H(asm)==r['DECODER_SOURCE_SHA256']
 assert len(fas)==len(r['parts'])
 result,proof=attacks(fas[0],asm)if kind=='attacks528'else display(fas[0],fas[1],asm)
 proof.update(transform='visual-'+kind+'-exact-inverse-v1',FA_hashes=[H(x)for x in fas],ASM_hash=H(asm),mixed_hash=H(result),canonical_credit_added=0)
 return result,proof
