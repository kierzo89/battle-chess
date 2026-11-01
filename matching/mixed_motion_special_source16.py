"""Finite source-only fresh C5 motion/effect plus authored special composition."""
import hashlib,re
C_SOURCE_SHA256='7df0efd9e7c26ca02ae1a5169e10e21343ec0a40590bb8fca5c53ea723ee797f'
DECODER_SOURCE_SHA256='ac9e3a433f7bbd5beed715b9c6b1324303214d8410daab0bb0b34d894ecb1487'
TRANSFORM='motion-effect-special-authenticated-C3-EOF-v1'
H=lambda b:hashlib.sha256(b).hexdigest()
def compose_fresh(fa,asm,*,c_source_sha256):
 assert type(fa)is bytes and type(asm)is bytes and c_source_sha256==C_SOURCE_SHA256 and H(asm)==DECODER_SOURCE_SHA256
 assert b'\x00'not in fa and b'\x1a'not in fa and fa.count(b'\tTITLE   C:\\UNIT.C\r\n')==1
 assert fa.count(b"_TEXT\tSEGMENT  WORD PUBLIC 'CODE'\r\n")==1
 assert re.findall(rb'^([^;\r\n]*?)\bPROC\s+NEAR\r?$',fa,re.M)==[b'_move_task_68ea\t',b'_effect_task_6ab1\t']
 tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n';end=b'_effect_task_6ab1\tENDP\r\n';assert fa.endswith(end+tail)and fa.count(b'\tnop\t\r\n')==1
 source=fa[:-len(tail)];metadata=[]
 for n,k in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  x=(n+"\tSEGMENT  BYTE PUBLIC '"+k+"'\r\n"+n+'\tENDS\r\n').encode();assert source.count(x)==1;source=source.replace(x,b'',1);metadata.append(x)
 a=asm.index(b'PUBLIC _special_task_6bf9\n');z=asm.index(b'_special_task_6bf9 ENDP')+len(b'_special_task_6bf9 ENDP');body=(asm[a:z]+b'\n').replace(b'\n',b'\r\n')
 for name,typ in {'__chkstk':'NEAR','_interpolate_position_5ebc':'NEAR','_attach_actor':'NEAR','_motion_x':'WORD','_motion_y':'WORD'}.items():assert b'EXTRN\t'+name.encode()+b':'+typ.encode()+b'\r\n'in fa
 out=source+b'\r\n'+body+b'\r\n; Finalize WORD module after two real C procedures and authored ASM.\r\n\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n'
 first=fa.index(b'_move_task_68ea\tPROC NEAR');cbody=fa[first:len(fa)-len(tail)];assert cbody in out and body in out
 # Exact inverse: remove appended body and restore only the outside-ENDP EOF tail
 # and truly empty debug declaration pairs at their original neighboring marker.
 rebuilt=source
 marker=b'DGROUP\tGROUP\tCONST, _BSS, _DATA\r\n';assert rebuilt.count(marker)==1
 rebuilt=rebuilt.replace(marker,b''.join(metadata)+marker,1)+tail
 assert rebuilt==fa
 return out,{'transform':'motion-effect-special-authenticated-C3-EOF-v1','fresh_FA_SHA256':H(fa),'C_source_SHA256':c_source_sha256,'authored_ASM_SHA256':H(asm),'C_two_PROCs_verbatim_SHA256':H(cbody),'ASM_PROC_verbatim_SHA256':H(body),'composed_source_SHA256':H(out),'inverse_reconstructs_full_fresh_FA':True,'only_empty_debug_declarations_omitted':4,'only_outside_ENDP_C3_NOP_deferred':True,'final_alignment_directive':'EVEN','target_profile_oldOBJ_reads':False}
