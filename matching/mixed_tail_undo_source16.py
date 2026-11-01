"""Exact same-call compiler source plus authored undo PROC; never consumes OBJ."""
import hashlib,re
C_SOURCE_SHA256='04bbd276676732e28baf30a60c2be1d7e512e4f6ae0231fc445e0f99559705d0'
DECODER_SOURCE_SHA256='d904072821c84fa1672f6c22632ac1160962fd5d4bab1e424565f12dde075ad1'
TRANSFORM='tail547-undo327-authenticated-C3-EOF-one-imm16-type-v2'
H=lambda b:hashlib.sha256(b).hexdigest()
def compose_fresh(fa,asm,*,c_source_sha256):
 assert type(fa)is bytes and type(asm)is bytes and c_source_sha256==C_SOURCE_SHA256 and H(asm)==DECODER_SOURCE_SHA256
 assert b'\0'not in fa and b'\x1a'not in fa and fa.count(b'\tTITLE   C:\\UNIT.C\r\n')==1 and fa.count(b"_TEXT\tSEGMENT  WORD PUBLIC 'CODE'\r\n")==1
 names=[b'_transfer_task_758c\t',b'_capture_task_75f6\t',b'_task_ready_772d\t'];assert re.findall(rb'^([^;\r\n]*?)\bPROC\s+NEAR\r?$',fa,re.M)==names
 tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n';end=b'_task_ready_772d\tENDP\r\n';assert fa.endswith(end+tail)and fa.count(b'\tnop\t\r\n')==1
 source=fa[:-len(tail)];metadata=[]
 # Genuine C3 word-immediate AND was shortened by MASM. One independently
 # calibrated source type qualifier preserves value/register/immediate semantics.
 plain=b'\tand\tbx,63\r\n';qualified=b'\tand\tbx,WORD PTR 63\r\n'
 assert fa.count(plain)==1 and qualified not in fa
 source=source.replace(plain,qualified,1)
 for n,k in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  x=(n+"\tSEGMENT  BYTE PUBLIC '"+k+"'\r\n"+n+'\tENDS\r\n').encode();assert source.count(x)==1;source=source.replace(x,b'',1);metadata.append(x)
 # Existing C byte-array memory views are the same real externals. No allocation/type change.
 for name in ['_cells','_actors']:assert b'EXTRN\t'+name.encode()+b':BYTE\r\n'in fa
 assert b'EXTRN\t__chkstk:NEAR\r\n'in fa
 injected=[]
 for name,typ in [('_actor_map','BYTE'),('_kind_map','BYTE'),('_detach_actor','NEAR'),('_queue_piece','NEAR')]:
  line=b'EXTRN\t'+name.encode()+b':'+typ.encode()+b'\r\n';matches=re.findall(rb'^EXTRN\s+'+name.encode()+rb':[^\r\n]+\r?$',fa,re.M)
  if matches:assert matches==[line.rstrip(b'\n')]
  else:injected.append(line)
 marker=b'EXTRN\t__acrtused:ABS\r\n';assert source.count(marker)==1;source=source.replace(marker,marker+b''.join(injected),1)
 a=asm.index(b'PUBLIC _undo_animation\n');z=asm.index(b'_undo_animation ENDP')+len(b'_undo_animation ENDP');body=(asm[a:z]+b'\n').replace(b'\n',b'\r\n')
 labels=re.findall(rb'^(code_[0-9a-f]+):',body,re.M);assert labels and len(set(labels))==len(labels)
 assert all(not re.search(rb'(?<![\w$])'+re.escape(n)+rb'(?![\w$])',fa)for n in labels)
 assert not re.search(rb'^\s*(?:EXTRN|PUBLIC)\s+_undo_animation\b',fa,re.M)
 out=source+b'\r\n'+body+b'\r\n; Finalize WORD alignment after three genuine C PROCs and authored undo PROC.\r\n\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n'
 first=fa.index(b'_transfer_task_758c\tPROC NEAR');cbody=fa[first:len(fa)-len(tail)];qualified_body=cbody.replace(plain,qualified,1);assert qualified_body in out and body in out and qualified_body.count(qualified)==1 and qualified_body.replace(qualified,plain,1)==cbody
 rebuilt=source.replace(marker+b''.join(injected),marker,1);assert rebuilt.count(qualified)==1;rebuilt=rebuilt.replace(qualified,plain,1);gmarker=b'DGROUP\tGROUP\tCONST, _BSS, _DATA\r\n';assert rebuilt.count(gmarker)==1;rebuilt=rebuilt.replace(gmarker,b''.join(metadata)+gmarker,1)+tail;assert rebuilt==fa
 return out,{'transform':TRANSFORM,'fresh_FA_SHA256':H(fa),'C_source_SHA256':c_source_sha256,'authored_ASM_SHA256':H(asm),'original_C_three_PROCs_SHA256':H(cbody),'qualified_C_three_PROCs_SHA256':H(qualified_body),'C_PROCs_exact_except_one_immediate_type_qualifier':True,'only_qualifier_transition':{'plain':plain.decode(),'qualified':qualified.decode(),'semantics':'AND BX, immediate WORD63','native_and_genuine_C3_encoding':'81e33f00','calibration':'MASM510-AND-immediate-width-calibration-root-actual'},'authored_ASM_PROC_remains_verbatim':True,'ASM_PROC_verbatim_SHA256':H(body),'composed_source_SHA256':H(out),'inverse_reconstructs_full_fresh_FA':True,'only_empty_debug_declarations_omitted':4,'only_outside_ENDP_C3_NOP_deferred':True,'final_alignment_directive':'EVEN','new_real_external_declarations':[x.decode().strip()for x in injected],'shared_byte_views_unchanged':['_cells','_actors'],'target_profile_oldOBJ_reads':False}
