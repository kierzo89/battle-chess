"""Exact source-only two-PROC composition; no object/native/archived-listing input."""
import hashlib,re
C_SOURCE_SHA256='0c57840fac7f4b5c69d52dba278bb8238692234b09dd39a6b44b093c621d7a54'
DECODER_SOURCE_SHA256='22f092e8b137c90c69acc5eb455f7261cdcb8484799c62a95a42afba7949e52a'
TRANSFORM='restore51-authenticated-C3-EOF-plus-decoder289-exact-declaration-union-v1'
H=lambda b:hashlib.sha256(b).hexdigest()
class CompositionError(ValueError):pass
def need(v,m):
 if not v:raise CompositionError(m)
def compose_fresh(fa,decoder,*,c_source_sha256):
 need(type(fa)is bytes and type(decoder)is bytes and c_source_sha256==C_SOURCE_SHA256 and H(decoder)==DECODER_SOURCE_SHA256,'Exact unchanged real source identities')
 need(b'\0'not in fa and b'\x1a'not in fa,'No EOF/control truncation')
 need(fa.count(b'\tTITLE   C:\\UNIT.C\r\n')==1 and fa.count(b"_TEXT\tSEGMENT  WORD PUBLIC 'CODE'\r\n")==1,'Actual source basename/compiler WORD CODE')
 need(re.findall(rb'^([^;\r\n]*?)\bPROC\s+NEAR\r?$',fa,re.M)==[b'_restore_active_arena\t'],'Exactly sole real compiler procedure')
 end=b'_restore_active_arena\tENDP\r\n';tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n';need(fa.endswith(end+tail)and fa.count(b'\tnop\t\r\n')==1,'Unique exact outside-ENDP C3 module NOP')
 start=fa.index(b'_restore_active_arena\tPROC NEAR\r\n');cproc=fa[start:fa.index(end)+len(end)]
 accesses=[line for line in cproc.splitlines()if b'_arena_cursor'in line]
 need(len(accesses)==2 and re.fullmatch(rb'\s*mov\s+WORD PTR _arena_cursor,ax',accesses[0])and re.fullmatch(rb'\s*mov\s+WORD PTR _arena_cursor\+2,dx',accesses[1]),'Both C accesses must explicitly retain WORD PTR halves; no default DWORD-dependent C operation')
 debug=[b"$$SYMBOLS\tSEGMENT  BYTE PUBLIC 'DEBSYM'\r\n$$SYMBOLS\tENDS\r\n",b"$$TYPES\tSEGMENT  BYTE PUBLIC 'DEBTYP'\r\n$$TYPES\tENDS\r\n"]
 source=fa
 for block in debug:need(source.count(block)==1,'Only truly empty exact debug declarations');source=source.replace(block,b'',1)
 old=b'EXTRN\t_arena_cursor:DWORD\r\n';new=b'EXTRN\t_arena_cursor:WORD\r\n';need(source.count(old)==1 and new not in source,'Sole declared memory-view conflict')
 source=source.replace(old,new,1)
 # Existing decoder WORD view preserves its unqualified low-half MOV operands.
 # The C PROC's explicit WORD PTR operands and real C5 far-pointer type remain untouched.
 need(b'EXTRN\t_count_0096:WORD\r\n'in source,'Shared count declaration already compatible')
 extra=b'EXTRN\t_frames:BYTE\r\nEXTRN\t_huff_decode_stream:NEAR\r\n';needle=b'_TEXT      SEGMENT\r\n';need(source.count(needle)==1 and b'EXTRN\t_frames:'not in source and b'EXTRN\t_huff_decode_stream:'not in source,'Two real missing declarations only')
 source=source.replace(needle,extra+needle,1);source=source[:-len(tail)]
 text=decoder.decode('ascii');a=text.index('PUBLIC _decode_frame_directory\n');z=text.index('_decode_frame_directory ENDP')+len('_decode_frame_directory ENDP');asm=(text[a:z]+'\n').replace('\n','\r\n').encode()
 suffix=b'\r\n'+asm+b'\r\n; Whole WORD module finalization after both real procedures.\r\n\tEVEN\r\n_TEXT\tENDS\r\nEND\r\n';combined=source+suffix
 need(combined[combined.index(b'_restore_active_arena\tPROC NEAR'):combined.index(end)+len(end)]==cproc and asm in combined,'Both complete PROCs verbatim')
 inverse=combined[:-len(suffix)].replace(extra+needle,needle,1).replace(new,old,1)+tail
 marker=b'_BSS\tENDS\r\n';need(inverse.count(marker)==1,'Unique metadata inverse insertion point');inverse=inverse.replace(marker,marker+b''.join(debug),1)
 need(inverse==fa,'Exact declaration/debug/EOF inverse must reconstruct complete fresh FA')
 return combined,{'transform':TRANSFORM,'fresh_FA_SHA256':H(fa),'authored_ASM_SHA256':H(decoder),'C_source_SHA256':c_source_sha256,'C_PROC_through_ENDP_SHA256':H(cproc),'ASM_PUBLIC_PROC_through_ENDP_CRLF_SHA256':H(asm),'composed_source_SHA256':H(combined),'only_exact_empty_debug_declarations_omitted':4,'only_authenticated_module_EOF_NOP_deferred':True,'final_alignment_directive':'EVEN','declaration_union':{'sole_width_view':{'symbol':'_arena_cursor','FA_declaration':'DWORD','assembler_memory_view':'WORD','both_C_accesses_explicit_WORD_PTR_halves':True,'real_C5_pointer_type_sidecar_unchanged':True,'allocation_alias_historical_type_claim':False},'shared_count_0096':'WORD unchanged','new_real_externals':['_frames:BYTE','_huff_decode_stream:NEAR']},'all_source_metadata_transform_inverse_exact':True,'native_expected_profile_oldOBJ_reads':False}
