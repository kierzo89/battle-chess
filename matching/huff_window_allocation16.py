"""Closed future CODE120 source-window profile; legacy CODE95 stays unchanged."""
from pathlib import Path
from dataclasses import asdict
import hashlib,json,re,shutil,struct,subprocess,tempfile
import huff_allocation16 as old
from omf import read_omf,OMFObject
require=old.require;digest=old.digest;Build=old.Build
BASE=old.BASE;BINDINGS=old.BINDINGS;NASM_SHA256=old.NASM_SHA256
SOURCE='asm/link/huff_helpers_window_omf.asm'
SOURCE_SHA256='8332530bad5d3f2b50ddca362cd8d63c6111b29bdd23f4e9854c9ef4f9a6c67d'
RAW_CODE_SHA256='dcdd9076597a29e499d1e2b00ee38673d579f0fc74e57c7d43edbcc4ab5d8bbc'
PUBLICS={**old.PUBLICS,'_begin_asset_decode':95,'_end_asset_decode':114}
PROFILE=old.FIXUP_PROFILE+[(n,2,1,True,(5,None),(2,k),None)for n,k in[(98,2),(102,2),(106,1),(116,1)]]
STAGE='build/huff-source-window-wrappers/'
RAW_EVIDENCE=STAGE+'rea-whole-120.json'
WRAPPERS={'begin':(STAGE+'rea-begin-asset-e449.json',0xe449,19),
          'end':(STAGE+'rea-end-asset-e45c.json',0xe45c,6)}
LINK_PROOF='build/huff-source-window-120/authentic-link-reference.json'
LINK_PROOF_SHA256='f3e5694a9a751ecf694eac9f41e435a0748958e49b236d8ab8015d0a1e52f9ec'

def validate_unit(u):
 require((u.get('id'),u.get('language'),u.get('backend'),u.get('object_profile'),u.get('source'))==('huff_refill_source_window_code','asm-code','nasm-code-contribution-omf','huff_source_window_120',SOURCE),'Closed source-window CODE120 profile required')
 require(u.get('source_sha256')==SOURCE_SHA256 and u.get('assembler_sha256')==NASM_SHA256,'Pinned source/NASM required')
 require(u.get('public_symbols')==list(PUBLICS)and u.get('image_offset')==hex(BASE)and type(u.get('size'))is int and u['size']==120,'Whole120/four actual PUBLICs required')
 require(u.get('externals')==BINDINGS and u.get('rea_evidence')==RAW_EVIDENCE and u.get('reference_region','unchanged-prefix')=='unchanged-prefix','Native bindings/evidence mismatch')
 require(not any(k in u for k in('symbol','flags','end_symbol','extended_extent','owned_const','owned_data','owned_bss','data_address','code_address')),'No fabricated function/ownership/slice metadata')

def extract_code(o):
 require(isinstance(o,OMFObject)and set(o.segments)=={1},'Exactly one CODE allocation required')
 s=o.segments[1]
 require((s.name,s.class_name,s.attributes,s.length,s.unsupported_data)==('_TEXT','CODE',0x48,120,False),'Complete WORD CODE120 required')
 require(o.externals==dict(enumerate(BINDINGS,1)),'Exact four external identities required')
 require({n:p.offset for n,p in o.publics.items()}==PUBLICS and len(o.publics)==4 and all((p.segment,p.group,p.type_index)==(1,0,0)for p in o.publics.values()),'Exact four actual PUBLICs required')
 for kind,_,payload in o.records:
  require(kind in(0x80,0x88,0x96,0x98,0x8c,0x90,0xa0,0x9c,0x8a),'Foreign record/allocation/COMM/group')
  if kind==0x88:require(payload.startswith(b'\0\0')or payload==b'\x40\xa2\x01','Foreign directive')
  if kind==0x8a:require(payload==b'\0','No executable entry')
 raw=bytearray()
 for at,b in sorted(s.chunks):
  require(b and at==len(raw)and at+len(b)<=120,'Hole/overlap/excess in CODE120');raw.extend(b)
 require(len(raw)==120,'Missing CODE120 tail')
 require([(f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)for f in sorted(o.fixups,key=lambda f:f.offset)]==PROFILE and all(f.segment==1 for f in o.fixups),'Exact14 fields required')
 require(digest(raw)==RAW_CODE_SHA256,'Instruction/addend bytes changed')
 return bytes(raw),{'boundary':'complete_multi_entry_CODE_SEGDEF','length':120,'publics':[asdict(p)for p in o.publics.values()],'actual_fixup_count':14,'function_partition_claim':False,'authored_c_function_credit':0,'authored_asm_function_credit':0,'ASM_CODE_contributions':1}

def assemble(source,u,nasm='nasm'):
 validate_unit(u);data=Path(source).read_bytes();require(digest(data)==SOURCE_SHA256,'Source pin mismatch')
 tool=shutil.which(nasm);require(tool is not None,'NASM unavailable');tool=Path(tool).resolve();require(digest(tool.read_bytes())==NASM_SHA256,'NASM pin mismatch')
 with tempfile.TemporaryDirectory(prefix='huff-window-allocation-')as tmp:
  p=Path(tmp);(p/'UNIT.ASM').write_bytes(data);cmd=[str(tool),'-f','obj','-Ox','UNIT.ASM','-o','UNIT.OBJ'];r=subprocess.run(cmd,cwd=p,capture_output=True,text=True,timeout=30)
  require(r.returncode==0 and(p/'UNIT.OBJ').exists(),'NASM failure '+r.stdout+r.stderr);objbytes=(p/'UNIT.OBJ').read_bytes()
 require(digest(tool.read_bytes())==NASM_SHA256,'NASM changed');raw,meta=extract_code(read_omf(objbytes))
 return Build(objbytes,raw,meta,{'source_sha256':SOURCE_SHA256,'assembler_sha256':NASM_SHA256,'assembler_path':str(tool),'build_command':cmd,'assembler_log':r.stdout+r.stderr,'object_sha256':digest(objbytes),'object_format':'OMF16','fresh_directory':True})

def _link_fixed(o,origin,bindings):
 raw,_=extract_code(o);cs,ip=origin
 require(all(type(x)is int and 0<=x<=65535 for x in origin)and ip+120<=65536,'Invalid whole placement')
 require(set(bindings)==set(BINDINGS)and all(isinstance(v,dict)and set(v)=={'segment','offset'}and all(type(n)is int and 0<=n<=65535 for n in v.values())for v in bindings.values()),'Invalid whole bindings')
 require(all(bindings[n]['segment']==bindings['_huff_input_buffer']['segment']for n in('_huff_memory_mode','_huff_memory_cursor'))and bindings['_read_asset']['segment']==cs,'Wrong data group/code frame')
 full=bytearray(raw);logs=[]
 for f in sorted(o.fixups,key=lambda f:f.offset):
  n=o.externals[f.target[1]];t=bindings[n];add=int.from_bytes(raw[f.offset:f.offset+2],'little');mz=None;mode='dgroup_offset16'
  if f.location_type==2:
   require(f.offset==64 and n=='_huff_input_buffer'and add==0,'Only reviewed buffer BASE16');value=t['segment'];mz=cs*16+ip+64;mode='external_buffer_group_base16'
  elif not f.segment_relative:
   require(f.offset==27 and n=='_read_asset','Only native near read call');value=t['offset']+add-ip-f.offset-2;mode='self_relative_code'
  else:value=t['offset']+add
  full[f.offset:f.offset+2]=(value&65535).to_bytes(2,'little');q=asdict(f);q['raw']=f.raw.hex();q.update(symbol=n,addend=add,value=value&65535,mode=mode,image_offset=cs*16+ip+f.offset)
  if mz is not None:q['mz_segment_relocation_image_offset']=mz
  logs.append(q)
 return bytes(full),logs

def _native(project):
 p=Path(project);prefix,proofs=old._native(p);ids={v['id']for v in proofs.values()}
 e=json.loads((p/RAW_EVIDENCE).read_text());old._subject(e,'read_bytes',{'address':'0x1e3ea','length':120});r=e['normalized_result']
 require(e['evidence_id']not in ids and r['complete']and r['returned_bytes']==r['requested_bytes']==120 and r['address']=='0x1e3ea','Complete distinct raw120 required')
 raw=bytes.fromhex(r['bytes_hex']);require(len(raw)==120 and raw[:95]==prefix,'Whole120/prefix95 mismatch');ids.add(e['evidence_id']);proofs[RAW_EVIDENCE]={'id':e['evidence_id'],'sha256':digest((p/RAW_EVIDENCE).read_bytes())}
 expected={'begin':['0x1e449: POP CX','0x1e44a: POP word ptr [0x44da]','0x1e44e: POP word ptr [0x44dc]','0x1e452: MOV byte ptr [0x44de], 0x1','0x1e457: SUB SP, 0x4','0x1e45a: JMP CX'], 'end':['0x1e45c: MOV byte ptr [0x44de], 0x0','0x1e461: RET']}
 for k,(path,at,n)in WRAPPERS.items():
  e=json.loads((p/path).read_text());old._subject(e,'analyze_function',{'procedure':hex(0x10000+at)});v=e['normalized_result'];b=v['procedure']['body']
  require(e['evidence_id']not in ids,'Duplicate primary ID');ids.add(e['evidence_id'])
  require(v['procedure']['address']==hex(0x10000+at)and not v['procedure']['classification']['external']and not v['procedure']['classification']['thunk']and b==dict(available=True,provenance='ghidra-function-body-address-set',ranges=[dict(start=hex(0x10000+at),end=hex(0x10000+at+n-1))],total_bytes=n,span_bytes=n,non_contiguous=False,contains_entry=True),'Native wrapper extent changed')
  require(v['assembly']==expected[k]and v['basic_blocks']==[dict(start=hex(0x10000+at),end=hex(0x10000+at+n),successors=[])],'Native wrapper instructions/CFG changed')
  proofs[path]={'id':e['evidence_id'],'sha256':digest((p/path).read_bytes()),'body':b}
 return raw,proofs

def validate_evidence(u,project,target_sha256,reference=None):
 validate_unit(u);require(target_sha256==old.ORIGINAL_SHA256,'Wrong target');_,p=_native(project);return p[RAW_EVIDENCE]['id']

def _authenticate_links(project,o):
 p=Path(project);b=(p/LINK_PROOF).read_bytes();require(digest(b)==LINK_PROOF_SHA256,'Actual two-order LINK proof pin mismatch')
 proof=json.loads(b);runs=proof['authentic_LINK'];require(len(runs)==2,'Two actual LINK orders required');checked=[]
 for order,run in zip([['HELP','CALL','MAIN','READ'],['MAIN','READ','CALL','HELP']],runs):
  require(run['object_order']==order and run['executed']is False and run['original_read_or_mounted']is False,'LINK order/observation mismatch')
  d=p/'build/huff-source-window-120'/'-'.join(order);exe=(d/'UNIT.EXE').read_bytes();text=(d/'UNIT.MAP').read_text(encoding='cp437')
  require(digest(exe)==run['exe_sha256']and text==run['map'],'Actual EXE/MAP mismatch')
  part=text.split('Publics by Name')[1].split('Publics by Value')[0]
  pubs={n:(int(s,16),int(a,16))for s,a,n in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',part,re.M)}
  origin=pubs['_huff_refill_e3ea'];require(all(pubs[n]==(origin[0],origin[1]+a)for n,a in PUBLICS.items()),'Actual four PUBLIC placements mismatch')
  bindings={n:dict(segment=pubs[n][0],offset=pubs[n][1])for n in BINDINGS};ds=bindings['_huff_input_buffer']['segment']
  require(re.search(r'(?im)^\s*'+format(ds,'04X')+r':0\s+DGROUP\s*$',text)is not None,'Buffer BASE must be actual DGROUP')
  linked,fields=_link_fixed(o,origin,bindings);h=struct.unpack_from('<14H',exe);image=exe[h[4]*16:];start=origin[0]*16+origin[1]
  require(image[start:start+120]==linked,'Whole120 disagrees with actual LINK')
  mz=[int.from_bytes(exe[h[12]+4*i:h[12]+4*i+2],'little')+16*int.from_bytes(exe[h[12]+4*i+2:h[12]+4*i+4],'little')for i in range(h[3])]
  owned=sorted(s for s in mz if s<start+120 and s+2>start)
  require(owned==[start+64]and int.from_bytes(linked[64:66],'little')==ds,'Actual120 MZ/BASE differs')
  checked.append(dict(order=order,origin=origin,all120_equal=True,all14_fields=fields,actual_DGROUP=ds,MZ=owned,executed=False))
 return checked

def validate_comparison(u,built,image,project,original_sites):
 validate_unit(u);o=read_omf(built.object_bytes);raw,meta=extract_code(o);require(raw==built.code and meta==built.metadata,'Build/object mismatch')
 linked,logs=_link_fixed(o,(0,BASE),BINDINGS);native,proofs=_native(project)
 require(linked==native==image[BASE:BASE+120],'Complete120 mismatch')
 emitted=[f['mz_segment_relocation_image_offset']for f in logs if'mz_segment_relocation_image_offset'in f];sites=sorted(s for s in original_sites if s<BASE+120 and s+2>BASE)
 require(emitted==sites==[BASE+64],'Whole120 MZ set mismatch/crossing')
 loads=[]
 for load in(0,1,0x1000,0xffff):
  a=bytearray(linked);b=bytearray(image[BASE:BASE+120])
  for data in(a,b):data[64:66]=((int.from_bytes(data[64:66],'little')+load)&65535).to_bytes(2,'little')
  require(a==b,'Four-base mismatch');loads.append(dict(load_paragraph=load,whole120_equal=True,sha256=digest(a)))
 actual=_authenticate_links(project,o)
 return linked,dict(whole_allocation_size=120,whole_allocation_image_offset=BASE,whole_bytes_equal=True,relocations=logs,whole_original_mz_sites=sites,emitted_mz_sites=emitted,four_load_bases=loads,primary_evidence=proofs,authentic_two_order_LINK=actual,function_partition_claim=False,authored_c_function_credit=0,authored_asm_function_credit=0,ASM_CODE_contributions=1)
