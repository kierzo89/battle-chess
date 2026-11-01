"""Closed source-only C3 EOF-finalization transform; no native/object/profile inputs."""
import hashlib,re
C_SOURCE_SHA256='f1f82594fb7bc3502d832376faf3e654a12e04144c0229a7aba99f0fc651d75e'
CHAT_SOURCE_SHA256='70578a5d6b0e8105f27b88f3a8516faed832bd658729150f8df87a4c2e9c106c'
TRANSFORM='refresh-C3-authenticated-EOF-alignment-plus-authored-chat-v1'
H=lambda b:hashlib.sha256(b).hexdigest()
class CompositionError(ValueError):pass
def need(v,m):
 if not v:raise CompositionError(m)
def compose_fresh(fa,chat,*,c_source_sha256):
 need(type(fa)is bytes and type(chat)is bytes and c_source_sha256==C_SOURCE_SHA256 and H(chat)==CHAT_SOURCE_SHA256,'Exact real source identities')
 need(b'\0'not in fa and b'\x1a'not in fa,'No EOF/control truncation')
 text=fa.decode('ascii');need(fa.count(b'\tTITLE   C:\\UNIT.C\r\n')==1,'Actual fixed compiler DOS source name')
 need(fa.count(b"_TEXT\tSEGMENT  WORD PUBLIC 'CODE'\r\n")==1,'Original compiler WORD CODE declaration retained')
 # This predicate applies only to the pinned source/tool/compiler mode. No general
 # rule permits deleting arbitrary NOPs, even when they occur after an ENDP.
 need(re.findall(rb'^([^;\r\n]*?)\bPROC\s+NEAR\r?$',fa,re.M)==[b'_refresh_1446\t'],'Exactly one real compiler procedure')
 end=b'_refresh_1446\tENDP\r\n';tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n'
 need(fa.endswith(end+tail)and fa.count(b'\tnop\t\r\n')==1,'Unique authenticated C3 EOF NOP outside sole real procedure')
 source=fa
 metadata=[b"$$SYMBOLS\tSEGMENT  BYTE PUBLIC 'DEBSYM'\r\n",b'$$SYMBOLS\tENDS\r\n',b"$$TYPES\tSEGMENT  BYTE PUBLIC 'DEBTYP'\r\n",b'$$TYPES\tENDS\r\n']
 need(source.count(metadata[0]+metadata[1])==1 and source.count(metadata[2]+metadata[3])==1,'Only genuinely empty adjacent debug declarations')
 for line in metadata:need(source.count(line)==1,'Exact empty debug declaration');source=source.replace(line,b'',1)
 source=source[:-len(tail)];start=source.index(b'_refresh_1446\tPROC NEAR\r\n');c_body=source[start:];need(c_body.endswith(end),'C procedure exact endpoint')
 extra=['EXTRN\t_menu_state:WORD','EXTRN\t_begin_input_0fb0:NEAR','EXTRN\t_end_input_102d:NEAR','EXTRN\t_fill_region_1780:NEAR','EXTRN\t_text_input_1064:NEAR','EXTRN\t_restore_region_58b0:NEAR'];needle=b'_TEXT      SEGMENT\r\n';need(source.count(needle)==1,'Exact compiler segment reopen');source=source.replace(needle,('\r\n'.join(extra)+'\r\n').encode()+needle,1)
 body=chat.decode('ascii');a=body.index('PUBLIC _type_chat_14c1\n');z=body.index('_type_chat_14c1 ENDP')+len('_type_chat_14c1 ENDP');asm_body=(body[a:z]+'\n').replace('\n','\r\n').encode()
 combined=source+b'\r\n'+asm_body+b'\r\n; Combined module finalization: one WORD alignment after both real procedures.\r\n\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n'
 need(combined[combined.index(b'_refresh_1446\tPROC NEAR'):combined.index(end)+len(end)]==c_body and asm_body in combined,'Both real procedures retained verbatim')
 return combined,{'transform':TRANSFORM,'fresh_FA_SHA256':H(fa),'authored_ASM_SHA256':H(chat),'C_source_SHA256':c_source_sha256,'C_PROC_through_ENDP_SHA256':H(c_body),'ASM_PUBLIC_PROC_through_ENDP_CRLF_SHA256':H(asm_body),'composed_source_SHA256':H(combined),'only_exact_empty_debug_declarations_omitted':4,'only_authenticated_module_EOF_NOP_deferred':True,'final_alignment_directive':'EVEN','native_expected_profile_oldOBJ_reads':False}
