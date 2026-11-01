"""Versioned exact10 GROUP-frame Huff CODE944 source backend; old gates untouched."""
from pathlib import Path
import json,hashlib,shutil,subprocess,tempfile
import huff_code16 as old
from huff_workspace_omf16 import profile,extract_code,link_code,HuffWorkspaceError
SOURCE='asm/link/huffman_core_dgroup_omf.asm';SOURCE_SHA256='b96de66fb9f30286a1efb2e6f5c789a7c9a1e97e5066abf630f4e90562a1fc0e';OBJECT_PROFILE='huffman_core_dgroup1'
BASE=old.BASE;PUBLICS=old.PUBLICS;EXTERNALS=old.EXTERNALS;RAW_EVIDENCE=old.RAW_EVIDENCE;NASM_SHA256=old.NASM_SHA256;ORIGINAL_SHA256=old.ORIGINAL_SHA256;Build=old.Build
EVIDENCE_PINS={'huff_code16.py': 'abfc4b804efe87566e4501af400360673013ed824fc69d5f0abb10828b7805fe', 'link16.py': '3ed02730c5def1a3a4909647790d362f0eb624aa35c0888d52f1d704af2bf20e', 'evidence/rea-huff-core-944-raw.json': 'c99971ab8246a32a4a19a92e2383fc6813a29d23a0879da574461eb52ef05ce6', 'evidence/rea_huff_frame.json': 'daf5494aef098ff06b4f7dea7795df6835641c5dd8a5105071168db3c5f4ff00', 'evidence/rea_huff_tree.json': '52f03c482d7226658722dd4f9a0f51daf1b42378ffe208211a0435d89c99fdef', 'evidence/rea_huff_byte.json': '044a6e6486174187d745d955e3b9345bcf712063497fd40dc77e29b88c60ce4f', 'evidence/rea_bit.json': '81847fb6e382d003324049c78e9cf661f93bc42fd96ee095a7b593ef21b0210f', 'evidence/rea-huff-table_init.json': '9ddf6fc2c982f5916103ed3a6211d2b33e44c88ea6a0f2c0520b9feedbe1805d', 'evidence/rea-huff-stream-open.json': 'ba825e4427e6980d23baff496020d35620c50f91baa3a338a1ab121cb71d2e7f', 'evidence/rea_remaining_decode_callee_e282.json': '14cb4099fbe03f22d524d462768bee2db61dc1f1718ae133130558744f21692e', 'evidence/rea-huff-window_save.json': '0f0210b9cf761c3221c159b927d030e91495e6de11b6796a4d7aadf371cc5882', 'evidence/rea-huff-window-init.json': '870ac3de13d5531ff1e598f0a4b6d367fc16e596c9f81983caffbb8dfe2c199f'}
H=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise HuffWorkspaceError(m)
def validate_unit(u):
 require((u.get('language'),u.get('backend'),u.get('object_profile'),u.get('source'),u.get('source_sha256'))==('asm','nasm-code-omf',OBJECT_PROFILE,SOURCE,SOURCE_SHA256),'exact new Huff source/profile')
 row=old.UNITS.get(u.get('id'));require(row is not None and(u.get('symbol'),u.get('rea_evidence'))==row,'existing nine native identities')
 at=PUBLICS[row[0]];ix=list(PUBLICS).index(row[0]);end=list(PUBLICS.values())[ix+1]if ix+1<len(PUBLICS)else 944
 require(type(u.get('size'))is int and u['size']==end-at and u.get('image_offset')==hex(BASE+at)and u.get('externals')==EXTERNALS and u.get('reference_region','unchanged-prefix')=='unchanged-prefix','no native extent/binding change')
 require(not any(k in u for k in('flags','symbols','extended_extent','owned_const','owned_data','owned_bss','data_address','code_address','end_symbol')),'no foreign ownership/slice')
def assemble(source,unit,nasm='nasm'):
 validate_unit(unit);source=Path(source);content=source.read_bytes();require(H(content)==SOURCE_SHA256,'source pin');exe=shutil.which(nasm);require(exe is not None,'NASM unavailable');exe=Path(exe).resolve();require(H(exe.read_bytes())==NASM_SHA256,'NASM pin')
 with tempfile.TemporaryDirectory(prefix='huff-dgroup-omf-')as tmp:
  p=Path(tmp);(p/'UNIT.ASM').write_bytes(content);command=[str(exe),'-f','obj','-Ox','UNIT.ASM','-o','UNIT.OBJ'];r=subprocess.run(command,cwd=p,capture_output=True,text=True,timeout=30);require(r.returncode==0 and not r.stderr and(p/'UNIT.OBJ').is_file(),'fresh NASM failed');raw=(p/'UNIT.OBJ').read_bytes()
 require(H(exe.read_bytes())==NASM_SHA256 and source.read_bytes()==content,'source/tool changed');code,meta=extract_code(raw)
 return Build(raw,code,meta,{'source_sha256':H(content),'assembler_sha256':NASM_SHA256,'assembler_path':str(exe),'build_command':command,'assembler_log':r.stdout+r.stderr,'object_sha256':H(raw),'object_format':'OMF16','fresh_directory':True,'generation_target_input':False,'generation_original_placement_input':False})
def validate_comparison(unit,built,image,project,original_sites):
 validate_unit(unit)
 from huff_workspace_evidence import validate_link
 validate_link(project)
 project=Path(project).resolve()
 for rel,h in EVIDENCE_PINS.items():
  path=(project/rel).resolve();require(path.is_relative_to(project)and not path.is_symlink()and H(path.read_bytes())==h,'pinned complete native/pure helper closure')
 raw,meta=extract_code(built.object_bytes);require(raw==built.code and meta==built.metadata,'actual build whole object mismatch');whole,logs=link_code(built.object_bytes);require(len(whole)==944 and whole==image[BASE:BASE+944]and len(logs)==77,'whole944/all77 native exact')
 require(not any(s<BASE+944 and s+2>BASE for s in original_sites),'no original MZ crossing/inside');project=Path(project);e=json.loads((project/RAW_EVIDENCE).read_text());old.subject(e);r=e['normalized_result'];require(e['parameters']=={'address':'0x1e03a','length':944}and r['complete']and r['requested_bytes']==r['returned_bytes']==944 and bytes.fromhex(r['bytes_hex'])==whole,'whole native primary944')
 evidence_ids={RAW_EVIDENCE:e['evidence_id']};native={}
 for symbol,path in old.UNITS.values():
  b=(project/path).read_bytes();e=json.loads(b);old.subject(e);require(e['evidence_id']not in evidence_ids.values(),'distinct primaries');evidence_ids[path]=e['evidence_id'];at,size=old.public_extent(meta,symbol);a=BASE+at+0x10000;q=e['normalized_result']['procedure'];body=q['body'];require(e['operation']=='analyze_function'and e['parameters']=={'procedure':hex(a)}and int(q['address'],0)==a and not q['classification']['external']and not q['classification']['thunk']and body['available']and body['contains_entry']and not body['non_contiguous']and body['total_bytes']==body['span_bytes']==size and body['ranges']==[{'start':hex(a),'end':hex(a+size-1)}],'exact existing nine complete boundaries');native[path]=H(b)
 loads=[]
 for load in(0,1,4096,65535):
  b,ls=link_code(built.object_bytes,cs=load,ds=(0x5cc2+load)&65535);require(b==whole and len(ls)==77,'fourbase whole actual field arithmetic');loads.append({'load_paragraph':load,'all944bytes_exact':True,'sha256':H(b),'original_mz':[],'emitted_mz':[]})
 at,size=old.public_extent(meta,unit['symbol']);selected=[f for f in logs if BASE+at<=f['image_offset']<BASE+at+size]
 return whole[at:at+size],{'whole_allocation_image_offset':BASE,'whole_allocation_size':944,'whole_allocation_sha256':H(whole),'whole_linked_code_hex':whole.hex(),'whole_primary_path':RAW_EVIDENCE,'native_primaries_sha256':native,'native_evidence_ids':evidence_ids,'public_offset':at,'public_size':size,'whole_original_mz_sites':[],'unit_original_mz_sites':[],'emitted_mz_sites':[],'whole_bytes_equal':True,'four_load_bases':loads,'relocations':selected,'complete77_relocations':logs,'matching_credit_added':0,'actual_missing_storage_definitions_supplied':False,'exact10_GROUPframes':True}
