"""Source-only finite seven-PROC composition. No native/object/proof reads."""
import hashlib,re
H=lambda b:hashlib.sha256(b).hexdigest()
C_SOURCE_SHA256='82a71178acab4b3999110b255e3d69a6999b0f5120e3b747dbf4d316ea9965be'
SOURCES={'_draw_actor': {'file': 'asm/link/graphics7262/draw_actor.asm', 'sha256': '22f59d64f0a588c3adf8824964ca18fc01237c9e7b459c32b4caad4a8ef307c1'}, '_mark_region_41a8': {'file': 'asm/link/graphics7262/mark_region_41a8.asm', 'sha256': '1d24d5f197c70b4ad7ef7ba31f87c5a4400cb5ac3c5c473cfaee720259304041'}, '_render_42a0': {'file': 'asm/link/graphics7262/render_42a0.asm', 'sha256': '1f7efa0d8825f3fb721147fa7746d379e64efd9fb70826eef70a83eec3bd9d37'}, '_build_menu_466b': {'file': 'asm/link/graphics7262/build_menu_466b.asm', 'sha256': '213eaecc8baf913b63464b7361b6271925eb33cff0e8dc568f6a67a700836501'}, '_close_menu_4c74': {'file': 'asm/link/graphics7262/close_menu_4c74.asm', 'sha256': '8fe3037a2521cc2c850e661df00886685f17be381d39a5a6c3f6a628b558a4b3'}, '_finish_menu_5035': {'file': 'asm/link/graphics7262/finish_menu_5035.asm', 'sha256': '394832ee3e5942398b0312dd5e5db660617fe76d6e00f6561fcd2cf411b792b7'}, '_outline_square_543a': {'file': 'asm/link/graphics7262/outline_square_543a.asm', 'sha256': '63fa41031ab9ac9a89791f2b609ce9356685d49167210c9119cf27d2a1449d9f'}}
ORDER=['_empty_3b2e', '_compose_frame_3b3a', '_reset_graphics_3e4f', '_clear_actor_3e81', '_insert_actor', '_attach_actor', '_detach_actor', '_detach_all', '_draw_actor', '_mark_region_41a8', '_render_42a0', '_prepare_color_4575', '_configure_actor_45a2', '_build_menu_466b', '_close_menu_4c74', '_initialize_menu_bar_4e5d', '_finish_menu_5035', '_title_menu_50af', '_track_menu_512d', '_draw_menu_row_527e', '_advance_menu_5381', '_outline_square_543a']
def proc(fa,name):
 start=name.encode()+b'\tPROC NEAR\r\n';end=name.encode()+b'\tENDP\r\n';assert fa.count(start)==fa.count(end)==1
 a=fa.index(start);z=fa.index(end,a)+len(end);return a,z,fa[a:z]
def compose_fresh(fa,authored,*,c_source_sha256):
 assert type(fa)is bytes and type(authored)is dict and set(authored)==set(SOURCES)and c_source_sha256==C_SOURCE_SHA256
 assert b'\x00'not in fa and b'\x1a'not in fa and fa.count(b'\tTITLE   C:\\UNIT.C\r\n')==1
 assert re.findall(rb'^([^\s;]+)\tPROC NEAR\r$',fa,re.M)==[x.encode()for x in ORDER]
 original=[];current=fa
 for name,spec in SOURCES.items():
  source=authored[name];assert type(source)is bytes and H(source)==spec['sha256'];live='\n'.join(x.split(';',1)[0]for x in source.decode('ascii').splitlines())
  assert not re.search(r'\b(?:DB|DW|DD|DQ|DT|DUP|ORG|ALIGN|EVEN|INCLUDE|INCBIN|MACRO|REPT|IRP|IRPC|EQU)\b',live,re.I)
  first=name.encode()+b' PROC NEAR\n';last=name.encode()+b' ENDP\n';assert source.count(first)==source.count(last)==1 and source.endswith(last)
  body=source[source.index(first):].replace(first,name.encode()+b'\tPROC NEAR\n',1).replace(last,name.encode()+b'\tENDP\n',1).replace(b'\n',b'\r\n')
  a,z,old=proc(current,name);current=current[:a]+body+current[z:];original.append((name,old,body))
 # Exact known metadata-only MASM declaration projection; all real CV/TYPE remains
 # in the genuine C5 sidecar, not synthetic records in the game object.
 metadata=[]
 for n,k in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
  v=(n+"\tSEGMENT  BYTE PUBLIC '"+k+"'\r\n"+n+'\tENDS\r\n').encode();assert current.count(v)==1;current=current.replace(v,b'',1);metadata.append(v)
 inverse=current
 for name,old,new in original:assert inverse.count(new)==1;inverse=inverse.replace(new,old,1)
 marker=b'DGROUP\tGROUP\tCONST, _BSS, _DATA\r\n';assert inverse.count(marker)==1;inverse=inverse.replace(marker,b''.join(metadata)+marker,1);assert inverse==fa
 preserved=[]
 for name in ORDER:
  if name not in SOURCES:
   before=proc(fa,name)[2];assert proc(current,name)[2]==before;preserved.append({'symbol':name,'verbatim_PROC_SHA256':H(before)})
 assert current.endswith(b'_outline_square_543a\tENDP\r\n_TEXT\tENDS\r\nEND\r\n')
 return current,{'schema':'graphics7262-seven-PROC-exact-source-inverse-v1','fresh_FA_SHA256':H(fa),'C_source_SHA256':c_source_sha256,'authored_sources':{n:H(v)for n,v in authored.items()},'preserved_C_PROCs':preserved,'composed_SHA256':H(current),'inverse_reconstructs_full_fresh_FA':True,'only_empty_debug_declarations_omitted':4,'code_padding_or_tail_changes':False,'native_oldOBJ_profile_inputs':False}
