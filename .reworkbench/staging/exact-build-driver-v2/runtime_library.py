"""Fresh original-LIB derivation; authenticate all input and output members."""
from pathlib import Path
import hashlib,json,subprocess,os,time,sys
P=Path(__file__).resolve().parent;R=P.parents[2];sys.path.insert(0,str(R/'matching'))
from library16 import extract_member
H=lambda x:hashlib.sha256(x).hexdigest()
def inventory(path):
 d=path.read_bytes();assert d[0]==0xf0;page=int.from_bytes(d[1:3],'little')+3;end=int.from_bytes(d[3:7],'little');assert 16<=page and page&(page-1)==0 and page<=end<=len(d);i=page;rows=[]
 while i<end and d[i]!=0xf1:
  a=i;assert d[i]==0x80;name=d[i+4:i+4+d[i+3]].decode('latin1')
  while True:
   k=d[i];n=int.from_bytes(d[i+1:i+3],'little');z=i+3+n;assert n and z<=end and sum(d[i:z])&255==0;i=z
   if k==0x8a:break
  rows.append({'name':name,'sha256':H(d[a:i]),'size':i-a});i=(i+page-1)//page*page
 return rows
def run(output):
 pins={
  'LIB.EXE':('matching/build/probes/LIB.EXE','2512d3f175665f5283780cc10bb333ec26daeda218b84ed9d5f0b73e4bc2386f'),
  'SLIBC.LIB':('matching/toolchains/runtime500/SLIBC.LIB','7eabd615308e9a05de24f6e6e82e61a65f733eb64d12b5318d8b3ed569e389b9'),
  'LIBH.LIB':('matching/toolchains/runtime-libh/LIBH.LIB','768bfe171ebcad6d44aeca830ec8d19b31f02ce84ab35c81fc48fcf3f1e14858'),
  'BINMODE.OBJ':(str(P/'source-inputs/BINMODE.OBJ'),'f373b6ee1096e1e8e92f3a6d57ad0a28eaca7329b574f6b47480c98b0d668673')}
 assert H(Path('/usr/bin/dosbox').read_bytes())=='2a1cafe5dbbe7c4c1ab957756c2135435087ee8fb5d1f7bbe4bd29cb02c30477'
 S=Path(output);S.mkdir();calls=[]
 for name,(rel,h)in pins.items():
  raw=(R/rel).read_bytes();assert H(raw)==h;(S/name).write_bytes(raw)
 (S/'YES.TXT').write_bytes(b'y\r\n')
 def execute(command,tag):
  (S/'RUN.BAT').write_bytes(('@echo off\r\n'+command+' < YES.TXT > '+tag+'.LOG\r\nif errorlevel 1 goto failed\r\necho success > '+tag+'.OK\r\n:failed\r\nexit\r\n').encode());(S/'dosbox.conf').write_text('[sdl]\noutput=surface\n[mixer]\nnosound=true\n[cpu]\ncycles=max\n[autoexec]\nmount c "'+str(S)+'"\nc:\nRUN.BAT\n');t=time.monotonic();p=subprocess.run(['/usr/bin/dosbox','-conf',str(S/'dosbox.conf'),'-noconsole'],env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy'),capture_output=True,timeout=45);(S/(tag+'-stdout.bin')).write_bytes(p.stdout);(S/(tag+'-stderr.bin')).write_bytes(p.stderr);assert p.returncode==0 and (S/(tag+'.OK')).read_text().strip()=='success';calls.append({'command':command,'seconds':time.monotonic()-t,'returncode':p.returncode})
 execute('LIB COMBINED.LIB +SLIBC.LIB +LIBH.LIB;','MERGE')
 original=inventory(S/'SLIBC.LIB')+inventory(S/'LIBH.LIB');assert inventory(S/'COMBINED.LIB')==original and len(original)==350
 merge_hash=H((S/'COMBINED.LIB').read_bytes())
 execute('LIB COMBINED.LIB -TXTMODE +BINMODE.OBJ;','BINARY')
 actual=inventory(S/'COMBINED.LIB');expected=[x for x in original if x['name']!='TXTMODE'];assert len(expected)==349 and actual[:-1]==expected and actual[-1]['name']=='BINMODE'
 raw=(S/'BINMODE.OBJ').read_bytes();lib=(S/'COMBINED.LIB').read_bytes();member=extract_member(lib,'BINMODE',H(lib),actual[-1]['sha256'],validate_object=False).data;header=3+int.from_bytes(raw[1:3],'little');assert member==raw[:header]+bytes.fromhex('880b0000a30742494e4d4f4445c5')+raw[header:]
 result={'status':'FRESH_DERIVATION_ALL_350_MEMBERS_AUTHENTIC','pins':pins,'calls':calls,'combined_before_replacement_sha256':merge_hash,'output_path':str(S/'COMBINED.LIB'),'output_sha256':H(lib),'member_count':len(actual),'unchanged_member_count':349,'BINMODE_comment_only':True,'canonical_credit_added':0};(S/'verification.json').write_text(json.dumps(result,indent=2)+'\n');return result
