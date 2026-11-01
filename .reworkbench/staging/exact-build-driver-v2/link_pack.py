"""Fresh source-derived inputs, original LINK/EXEPACK, no binary rewriting."""
from pathlib import Path
import hashlib,json,subprocess,os,time,sys,struct
R=Path('/home/kierzo/chess');H=lambda b:hashlib.sha256(b).hexdigest()
def run(base,order_path,runtime_path,output):
 B=Path(base);order_path=Path(order_path);runtime_path=Path(runtime_path)
 spec=json.loads((B/'descriptor.json').read_text());order=json.loads(order_path.read_text());assert order['status']=='SAME_RUN_SOURCE_INPUTS_SEALED' and len(order['rows'])==225
 runtime=json.loads(runtime_path.read_text());assert runtime['status']=='FRESH_DERIVATION_ALL_350_MEMBERS_AUTHENTIC'
 S=Path(output);S.mkdir();T=S/'tools';T.mkdir()
 for row in order['rows']:
  raw=Path(row['object_path']).read_bytes();assert H(raw)==row['sha256'];(S/row['name']).write_bytes(raw)
 for key,name in [('LINK','LINK.EXE')]:
  pin=spec['tools'][key];raw=(R/'matching'/pin['path']).read_bytes();assert H(raw)==pin['sha256'];(T/name).write_bytes(raw)
 raw=Path(runtime['output_path']).read_bytes();assert H(raw)==runtime['output_sha256'];(T/'SLIBC.LIB').write_bytes(raw)
 packer=(R/'matching/toolchains/msc510/EXEPACK.EXE').read_bytes();assert H(packer)=='568554322d29e46f79c0c760ac2391cb0689dc7acb9aed79a428194ec6fb83e7';(T/'EXEPACK.EXE').write_bytes(packer)
 assert H(Path('/usr/bin/dosbox').read_bytes())=='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
 (S/'INPUTS.RSP').write_bytes(('+\r\n'.join(r['name']for r in order['rows'])+'\r\nPARTIAL.EXE\r\nPARTIAL.MAP\r\nT:\\SLIBC.LIB;\r\n').encode())
 (S/'RUN.BAT').write_bytes(b'@echo off\r\nT:\\LINK /NOD /NOEXTDICTIONARY /DOSSEG /NOFARCALLTRANSLATION /MAP /STACK:4096 @INPUTS.RSP > LINK.LOG\r\nif errorlevel 1 goto failed\r\necho success > LINK.OK\r\nT:\\EXEPACK PARTIAL.EXE PACKED.EXE > PACK.LOG\r\nif errorlevel 1 goto failed\r\necho success > PACK.OK\r\n:failed\r\nexit\r\n')
 (S/'dosbox.conf').write_text('[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(S)+'"\nmount t "'+str(T)+'" -ro\nc:\nRUN.BAT\n')
 t=time.monotonic();proc=subprocess.run(['/usr/bin/dosbox','-conf',str(S/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=90);(S/'stdout.bin').write_bytes(proc.stdout);(S/'stderr.bin').write_bytes(proc.stderr);assert proc.returncode==0;assert all((S/n).read_text().strip()=='success'for n in ['LINK.OK','PACK.OK'])
 # Native comparison starts only after both original tools terminate.
 sys.path.insert(0,str(R/'matching'));from reference import build_reference
 native=(R/'CHESS.EXE').read_bytes()
 assert H(native)=='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd' and len(native)==83415
 ref=build_reference(native);linked=(S/'PARTIAL.EXE').read_bytes();header=struct.unpack_from('<14H',linked);image=linked[header[4]*16:];sites=[seg*16+off for off,seg in struct.iter_unpack('<HH',linked[header[12]:header[12]+4*header[3]])];packed=(S/'PACKED.EXE').read_bytes()
 result={'status':'PASS_FRESH_SOURCE_DERIVED_EXACT_EXECUTABLE'if packed==native and image==ref['image'] and len(sites)==len(set(sites))==173 and sorted(sites,key=lambda address:address//65536)==list(ref['relocations']) else'HELD','base_run_id':order['base_run_id'],'object_count':225,'object_manifest_sha256':H(order_path.read_bytes()),'fresh_runtime_receipt_sha256':H(runtime_path.read_bytes()),'elapsed_seconds':time.monotonic()-t,'whole_expanded_image_equal':image==ref['image'],'image_size':len(image),'relocation_order_domain':'Original EXEPACK 64-KiB block emission order','relocation_count':len(sites),'relocation_order_exact':sorted(sites,key=lambda address:address//65536)==list(ref['relocations']),'packed_bytes_equal':packed==native,'packed_size':len(packed),'packed_sha256':H(packed),'native_sha256':H(native),'gameplay_verified':False,'canonical_admission':False,'canonical_credit_added':0};(S/'verification.json').write_text(json.dumps(result,indent=2)+'\n');return result
