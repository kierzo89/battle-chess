"""Finite reversible authored-prefix / genuine compiler-listing composition."""
import re
import hashlib
H=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)

def compose(fa,asm):
    need(fa.count(b"_TEXT\tSEGMENT  WORD PUBLIC 'CODE'\r\n")==1,'WORD CODE declaration')
    names=re.findall(rb'^([^;\r\n]*?)\bPROC\s+NEAR\r?$',fa,re.M)
    need(names==[n+b'\t' for n in [b'_empty_argument',b'_empty_5a37',b'_empty_5a43',b'_fill_5a4f',b'_plot_region_5a7c']],'five original compiler procedures')
    tail=b'\tnop\t\r\n_TEXT\tENDS\r\nEND\r\n'
    need(fa.endswith(b'_plot_region_5a7c\tENDP\r\n'+tail) and fa.count(b'\tnop\t\r\n')==1,'only outside-ENDP compiler tail')
    a=asm.index(b'PUBLIC _remove_actor_5934\n');z=asm.index(b'_remove_actor_5934 ENDP')+len(b'_remove_actor_5934 ENDP')
    body=(asm[a:z]+b'\n').replace(b'\n',b'\r\n')
    need(b'FULLWORD_IMMEDIATE_ZERO EQU 0\n'in asm and b'FULLWORD_IMMEDIATE_ZERO' not in fa,'original forward EQU')
    operations=[];source=fa[:-len(tail)]
    for name,kind in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
        old=(name+"\tSEGMENT  BYTE PUBLIC '"+kind+"'\r\n"+name+'\tENDS\r\n').encode()
        need(source.count(old)==1,'empty debug declarations')
        # Record precise original location for exact inverse replay.
        at=source.index(old);operations.append((at,old,b''));source=source[:at]+source[at+len(old):]
    edits=[(b"_DATA\tSEGMENT  WORD PUBLIC 'DATA'\r\n",b'EXTRN _dissolve_masks_0486:WORD\r\n'),
           (b'EXTRN\t__acrtused:ABS\r\n',b'EXTRN _rand:NEAR, _attach_actor:NEAR, _detach_actor:NEAR\r\n'),
           (b'; Line 1\r\n',body)]
    for marker,added in edits:
        need(source.count(marker)==1,'unique injection marker')
        at=source.index(marker)+(len(marker) if marker!=b'; Line 1\r\n' else 0)
        operations.append((at,b'',added));source=source[:at]+added+source[at:]
    end=b'\tEVEN\r\n_TEXT\tENDS\r\nFULLWORD_IMMEDIATE_ZERO EQU 0\r\nEND\r\n'
    result=source+end
    inverse=source
    for at,old,new in reversed(operations):
        need(inverse[at:at+len(new)]==new,'inverse insertion identity')
        inverse=inverse[:at]+old+inverse[at+len(new):]
    need(inverse+tail==fa,'complete fresh FA inverse')
    first=fa.index(b'_empty_argument\tPROC NEAR');last=len(fa)-len(tail)
    need(fa[first:last]in result and body in result,'all C instructions and authored ASM body verbatim')
    return result,{'inverse_recovers_complete_FA':True,'C_procedures_verbatim':True,'authored_ASM_body_verbatim':True,
        'outside_procedure_NOP_deferred_to_whole_WORD_EVEN':True,'FA_sha256':H(fa),'ASM_sha256':H(asm),'mixed_source_sha256':H(result),
        'sidecar_not_modified':True,'canonical_credit_added':0}

C_SOURCE_SHA256='98fecbdc15c912923f8c75c2ce15cf18744b0724bea1e1eadc7a12b8f1553f43'
DECODER_SOURCE_SHA256='991ec7390508894bcad675d2ca0dac58a9318873a15504d933b731dec8f7e338'
TRANSFORM='remove460-authored-prefix-five-C-procedures-exact-inverse-v1'

def compose_fresh(fa,asm,*,c_source_sha256):
    need(c_source_sha256==C_SOURCE_SHA256 and H(asm)==DECODER_SOURCE_SHA256,"exact authored C/ASM source identities")
    result,proof=compose(fa,asm)
    proof["transform"]=TRANSFORM
    return result,proof
