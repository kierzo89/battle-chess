"""Closed three-member read-only interpretation of certified authentic runtime OMF.

No OMF mutation, source emission, target reads, LINK invocation or ordinary-parser relaxation.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
from types import SimpleNamespace
import hashlib,json
from omf import _Cursor,_fixupp,OMFError
from library16 import LibraryError,extract_member
import runtime_external16 as old
from setup_libh import validate_helpers
from runtime_external3_pins import PINS,CERTIFICATE_SHA
BACKEND='msc500-authentic-external-runtime3-v1';SOURCE='config/runtime_external3.json'
LIBSHA='768bfe171ebcad6d44aeca830ec8d19b31f02ce84ab35c81fc48fcf3f1e14858'
SPECS={
 'LDIV':{'id':'near_ldiv','sha256':'6e210aff6aee94d45d3c8a9c8d91710fa77473eafbba5175ac64e9a064169af9','offset':7056,'raw_size':308,'size':163,'field':122,'symbol':'__aNldiv','native':0xf87c,'writes':[(0,161),(160,3)]},
 'ULDIV':{'id':'near_uldiv','sha256':'f89682360fe20794f53b64becf9fb0f5a6e95e324d17e41ff59cef184dd83c6c','offset':9872,'raw_size':249,'size':101,'field':72,'symbol':'__aNuldiv','native':0xf39c,'writes':[(0,99),(98,3)]},
 'ULREM':{'id':'near_ulrem','sha256':'0b97e465ea3efb91d49c994f67e12a5daedc68b1fdd1b9905c40f4b154e6c356','offset':10128,'raw_size':257,'size':109,'field':69,'symbol':'__aNulrem','native':0xf402,'writes':[(0,107),(106,3)]}}
def require(v,s):
 if not v:raise LibraryError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse_member(raw,name):
 """Account raw records and ordered writers; result is not a replacement OMF object."""
 require(name in SPECS and type(raw)is bytes,'runtime3 exact member name/raw');s=SPECS[name];at=0;names=[''];segs=[];groups=[];pub={};ext={};writes=[];records=[];o=SimpleNamespace(fixups=[]);last=None;threads={};ended=False
 try:
  while at<len(raw):
   start=at;require(not ended and at+3<=len(raw),'runtime3 record/trailing bounds');k=raw[at];n=int.from_bytes(raw[at+1:at+3],'little');require(n>0 and at+3+n<=len(raw),'runtime3 record length');r=raw[at:at+3+n];require(sum(r)%256==0,'runtime3 checksum');p=r[3:-1];at+=3+n;c=_Cursor(p);records.append({'kind':k,'offset':start,'raw_bytes':len(r),'sha256':sha(r)})
   if k==0x80:require(start==0 and c.name()==name,'runtime3 initial THEADR');c.finish()
   elif k==0x88:require(p==b'\0\xa3'+bytes([len('an'+name.lower())])+('an'+name.lower()).encode(),'runtime3 COMMENT')
   elif k==0x96:
    while c:names.append(c.name())
   elif k==0x98:
    a,z,sn,cl,ov=c.byte(),c.word(),c.index(),c.index(),c.index();c.finish();require(all(0<i<len(names)for i in(sn,cl,ov)),'runtime3 LNAMES bounds');segs.append({'index':len(segs)+1,'name':names[sn],'class_name':names[cl],'attributes':a,'length':z,'overlay':names[ov]})
   elif k==0x9a:
    ni=c.index();require(0<ni<len(names),'runtime3 group name');members=[]
    while c:require(c.byte()==255,'runtime3 group component');members.append(c.index())
    groups.append({'name':names[ni],'segments':members})
   elif k==0x8c:
    while c:nm,ty=c.name(),c.index();require(ty==0,'runtime3 EXTERN type');ext[len(ext)+1]=nm
   elif k==0x90:
    g,sn=c.index(),c.index();require((g,sn)==(0,1),'runtime3 PUBLIC frame')
    while c:
     nm,off,ty=c.name(),c.word(),c.index();require(nm not in pub,'runtime3 duplicate PUBLIC');pub[nm]={'segment':sn,'group':g,'offset':off,'type_index':ty}
   elif k==0xa0:
    sn,off=c.index(),c.word();b=c.take(len(c.data)-c.pos);require(sn==1 and b and off+len(b)<=s['size'],'runtime3 whole CODE writer bounds');writes.append({'record_offset':start,'offset':off,'bytes':b});last=sn,off,len(b)
   elif k==0x9c:_fixupp(o,p,last,threads,start)
   elif k==0x8a:require(p==b'\0'and at==len(raw),'runtime3 no entry MODEND');ended=True
   else:raise LibraryError('runtime3 unsupported record')
 except (OMFError,IndexError,UnicodeError)as e:
  if isinstance(e,LibraryError):raise
  raise LibraryError('runtime3 malformed bounded record')from e
 require(ended and names==['','','CODE','DATA','DGROUP','_DATA','_TEXT'],'runtime3 exact names/end')
 require(segs==[{'index':1,'name':'_TEXT','class_name':'CODE','attributes':72,'length':s['size'],'overlay':''},{'index':2,'name':'_DATA','class_name':'DATA','attributes':72,'length':0,'overlay':''}]and groups==[{'name':'DGROUP','segments':[2]}],'runtime3 CODE/emptyDATA/WORD ownership')
 require(pub=={s['symbol']:{'segment':1,'group':0,'offset':0,'type_index':0}}and ext=={1:'__aNulmul'},'runtime3 sole real PUBLIC/LMUL dependency')
 require([q['kind']for q in records]==[0x80,0x88,0x96,0x98,0x98,0x9a,0x8c,0xa0,0x9c,0xa0,0x90,0x8a],'runtime3 exact ordered records')
 require([(q['offset'],len(q['bytes']))for q in writes]==s['writes']and writes[1]['bytes']==b'\xc2\x08\0','runtime3 exact two raw writers/finalRET8')
 require(len(o.fixups)==1,'runtime3 sole typed field');f=o.fixups[0];require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(1,s['field'],2,1,False,(0,1),(2,1),None),'runtime3 exact relative CALL frame/target')
 require(writes[0]['bytes'][s['field']-1:s['field']+2]==b'\xe8\0\0','runtime3 raw CALL opcode/zero operand')
 owned={};chron=[]
 for w in writes:
  overwritten=[]
  for j,v in enumerate(w['bytes'],w['offset']):
   if j in owned:overwritten.append({'offset':j,'old':owned[j]['value'],'old_record':owned[j]['record'],'new':v})
   owned[j]={'value':v,'record':w['record_offset']}
  chron.append({'record_offset':w['record_offset'],'offset':w['offset'],'length':len(w['bytes']),'sha256':sha(w['bytes']),'overwritten':overwritten})
 require(set(owned)==set(range(s['size']))and chron[0]['overwritten']==[]and [q['offset']for q in chron[1]['overwritten']]==[s['size']-3]and not any(q['offset']<=f.offset+1 and f.offset<q['offset']+q['length']for q in chron[1:]),'runtime3 exact single RET-byte overlap/noholes/no overwrittenfield')
 require(len(raw)==s['raw_size']and sha(raw)==s['sha256'],'runtime3 immutable genuine whole member digest')
 # Reuse already-closed exact LDIV primitive without widening its ALDIV contract.
 if name=='LDIV':require(old._layout(raw,'LDIV')['segment']['length']==s['size'],'runtime3 existing exact LDIV gate')
 return {'member':name,'segment':segs[0],'segments':segs,'groups':groups,'publics':pub,'externals':ext,'records':records,'writers':chron,'last_writer_bytes':bytes(owned[i]['value']for i in range(s['size'])),'last_writer_records':[owned[i]['record']for i in range(s['size'])],'fixup':f,'object_sha256':sha(raw)}
def validate_unit(u):
 matches=[(n,s)for n,s in SPECS.items()if s['id']==u.get('member')];require(len(matches)==1,'runtime3 unit exact member');n,s=matches[0]
 require(u.get('id')=='runtime_libh_'+s['id']and u.get('backend')==BACKEND and u.get('source')==SOURCE and u.get('language')=='runtime'and u.get('runtime_kind','code')=='code'and u.get('reference_region','unchanged-prefix')=='unchanged-prefix'and u.get('symbol')==s['symbol']and u.get('size')==s['size']and int(u.get('image_offset','-1'),0)==s['native']and u.get('externals')=={'__aNulmul':{'segment':0,'offset':0xf32e}}and u.get('rea_evidence')=='evidence/runtime4-authentic/'+n+'-read.json','runtime3 closed whole-unit identity');return n,s
@dataclass(frozen=True)
class Runtime3Result:
 image:bytes
 object_bytes:bytes
 provenance:dict

def validate_calibration(cert,docs):
 require(cert['status']=='PASS_ONE_REAL_C5_AND_ONE_REAL_FULL_LIBRARY_LINK_HELPER_CALIBRATION'and cert['EXE_executed']is False and cert['generic_ordinary_overlap_parser_relaxed']is False and cert['game_C_or_runtime_credit']==0,'runtime3 authentic certificate semantics')
 require(len(cert['whole_members'])==3 and{q['member']for q in cert['whole_members']}==set(SPECS),'runtime3 allthree calibrated members')
 cg=json.loads(docs['C5_receipt']);lg=json.loads(docs['LINK_receipt']);co=json.loads(docs['C5_terminal']);lo=json.loads(docs['LINK_terminal'])
 for q,counter in[(cg,'actual_C5_calls'),(lg,'actual_LINK_calls')]:require(q['status']=='COMPLETE'and q['guard_closed']and q['error']is None and q[counter]==1 and len(q['calls'])==1 and q['calls'][0]['pid']>0 and q['calls'][0]['terminal']and q['calls'][0]['reaped']and q['calls'][0]['returncode']==0 and len(q['blocked_probes'])==20,'runtime3 genuine source-only terminal phases')
 for q in[co,lo]:require(q['terminal']and q['reaped']and q['exit_code']==0,'runtime3 observed root terminal')
 require(co['generation_receipt_sha256']==sha(docs['C5_receipt'])and co['raw_whole_object_sha256']==sha(docs['C5_object'])and co['raw_bytes']==len(docs['C5_object'])and lo['LINK_generation_receipt_sha256']==sha(docs['LINK_receipt'])and lo['GEN_LINK_calls']==1 and lo['EXE_executed']is False,'runtime3 root terminal artifact bindings')
 require(cg['source_tools_new_scratch_only']and not cg['native_original_oldOBJ_comparison_inputs_inside_GEN']and cg['compiler']=='msc500'and cg['flags']==['/AS','/Zi']and cg['source_name']=='UNIT.C'and cg['source_sha256']==sha(docs['control_source'])and cg['raw_whole_object_sha256']==sha(docs['C5_object']),'runtime3 meaningful fresh C5 provenance')
 require(lg['fresh_compiler_receipt_sha256']==sha(docs['C5_receipt'])and lg['fresh_compiler_outer_sha256']==sha(docs['C5_terminal'])and lg['fresh_compiler_whole_object_sha256']==sha(docs['C5_object'])and lg['whole_fresh_C5_OBJ_full_pinned_LIBs_LINK_only']and not lg['old_OBJ_original_native_or_expected_bytes_read_or_mounted_inside_GEN']and not lg['extra_stubs_aliases_native_inputs_EXE_execution'],'runtime3 full-library genuine LINK provenance')
 require(docs['LINK_RSP']==b'CONTROL.OBJ\r\nCONTROL.EXE\r\nCONTROL.MAP\r\nR:\\SLIBC.LIB+H:\\LIBH.LIB;\r\n','runtime3 exact full-library response/no injected members')
 for key,name in [('LINK_EXE','CONTROL.EXE'),('LINK_MAP','CONTROL.MAP'),('LINK_RSP','INPUTS.RSP'),('C5_object','CONTROL.OBJ'),('LIBH','libh/LIBH.LIB'),('SLIBC','slibc/SLIBC.LIB')]:require(lg['scratch_inventory'][name]['sha256']==sha(docs[key])and lg['scratch_inventory'][name]['size']==len(docs[key]),'runtime3 LINK complete input/output inventory')
 require(lg['scratch_inventory']['tools/LINK.EXE']['sha256']==old.LINKER_SHA256 and lg['command']=='T:\\LINK.EXE /NOD /DOSSEG /NOFARCALLTRANSLATION /MAP @INPUTS.RSP','runtime3 actual pinned LINK tool/command')
 require(sha(docs['LIBH'])==LIBSHA and sha(docs['SLIBC'])=='7eabd615308e9a05de24f6e6e82e61a65f733eb64d12b5318d8b3ed569e389b9','runtime3 whole input libraries')
 from omf import read_omf
 co_obj=read_omf(docs['C5_object']);require(set(co_obj.publics)==set(co_obj.procedures)=={'_signed_quotient','_unsigned_quotient','_unsigned_remainder','_main'},'runtime3 real arithmetic control functions');helpers={co_obj.externals[f.target[1]]for f in co_obj.fixups if f.segment==1 and f.target[0]==2 and co_obj.externals[f.target[1]].startswith('__aN')};require(helpers=={'__aNldiv','__aNuldiv','__aNulrem'},'runtime3 actual signed/unsigned helper identities')
 exe=docs['LINK_EXE'];text=docs['LINK_MAP'].decode('ascii');require(exe[:2]==b'MZ'and len(exe)>=28,'runtime3 calibration MZ');page=int.from_bytes(exe[4:6],'little');tail=int.from_bytes(exe[2:4],'little');header=int.from_bytes(exe[8:10],'little')*16;table=int.from_bytes(exe[24:26],'little');count=int.from_bytes(exe[6:8],'little');require(page>0 and tail<=511 and(page-1)*512+(tail or 512)==len(exe)and 28<=header<=len(exe)and 28<=table and table+4*count<=header,'runtime3 complete calibration FILE/header bounds');image=exe[header:];mz=[]
 for i in range(count):
  off=int.from_bytes(exe[table+i*4:table+i*4+2],'little');seg=int.from_bytes(exe[table+i*4+2:table+i*4+4],'little');site=seg*16+off;require(site+2<=len(image)and not any(abs(site-p)<2 for p in mz),'runtime3 calibration MZ bounds');mz.append(site)
 import re
 parts=text.split('Publics by Name');require(len(parts)==2 and len(parts[1].split('Publics by Value'))==2,'runtime3 MAP public sections');matches=re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:Abs\s+)?(\S+)\s*$',parts[1].split('Publics by Value')[0],re.M);mp={n:int(a,16)*16+int(b,16)for a,b,n in matches};require(len(mp)==len(matches),'runtime3 no duplicate MAP PUBLIC')
 require(cert['C5_raw_sha256']==sha(docs['C5_object'])and cert['LINK_EXE_sha256']==sha(exe)and cert['LINK_MAP_sha256']==sha(docs['LINK_MAP'])and cert['all_actual_MZ_sites']==mz,'runtime3 exact whole calibration output identities')
 for name,s in SPECS.items():
  member=extract_member(docs['LIBH'],name,LIBSHA,s['sha256'],validate_object=False);v=parse_member(member.data,name);at=mp[s['symbol']];actual=image[at:at+s['size']];f=v['fixup'];require(len(actual)==s['size']and not any(at-1<=q<at+s['size']for q in mz),'runtime3 whole calibrated helper/MZempty');raw=v['last_writer_bytes'];require(all(actual[i]==raw[i]for i in range(s['size'])if i not in(f.offset,f.offset+1))and int.from_bytes(actual[f.offset:f.offset+2],'little')==(mp['__aNulmul']-(at+f.offset+2))&65535,'runtime3 authentic LINK confirms every final writer and sole field');row=next(q for q in cert['whole_members']if q['member']==name);require(row['actual_MAP_origin']==at and row['actual_target']==mp['__aNulmul']and row['actual_CODE_sha256']==sha(actual)and row['whole_raw_sha256']==member.sha256 and row['whole_CODE_bytes']==s['size']and row['all_payload_and_field_equal']and row['actual_target_symbol']=='__aNulmul'and row['MZ']==[],'runtime3 certificate actual member provenance')
 return {'actual_helper_MAP_origins':{name:mp[s['symbol']]for name,s in SPECS.items()},'actual_LMUL':mp['__aNulmul'],'calibration_EXE_executed':False}

def _certificate(project):
 require(isinstance(CERTIFICATE_SHA,str)and len(CERTIFICATE_SHA)==64 and CERTIFICATE_SHA!='0'*64,'runtime3 HOLD: actual calibration certificate not closed');docs={}
 for key,row in PINS.items():
  p=(project/row['path']).resolve();require(p.is_relative_to(project),'runtime3 evidence path');b=p.read_bytes();require(sha(b)==row['sha256'],'runtime3 calibration/evidence pin '+key);docs[key]=b
 require(sha(docs['certificate'])==CERTIFICATE_SHA,'runtime3 exact certificate');cert=json.loads(docs['certificate']);validate_calibration(cert,docs);return cert,docs

def load_profile(u,project):
 project=Path(project).resolve();name,s=validate_unit(u);cfg=json.loads((project/SOURCE).read_text());require(cfg=={'schema':'runtime-external3-closed-overlap-v1','library_sha256':LIBSHA,'members':[{'id':v['id'],'name':k,'member_sha256':v['sha256'],'library_offset':v['offset'],'segment':1,'size':v['size'],'symbol':v['symbol'],'native_image_offset':v['native'],'native_LMUL':0xf32e}for k,v in SPECS.items()]},'runtime3 exact profile')
 cert,docs=_certificate(project);base=old.load_profile('near_aldiv',project);lib=validate_helpers(project/base['config']['destination'],base['config']);m=extract_member(lib,name,LIBSHA,s['sha256'],validate_object=False);require(m.offset==s['offset']and len(m.data)==s['raw_size'],'runtime3 exact library membership');v=parse_member(m.data,name);lm=base['members']['LMUL'];require(lm['publics']['__aNulmul']['offset']==0 and lm['segment']['length']==52 and lm['object_sha256']==old.SPECS['LMUL']['sha256'],'runtime3 actual LMUL whole provider')
 calibrated=next(q for q in cert['whole_members']if q['member']==name);require(calibrated['whole_raw_sha256']==m.sha256 and calibrated['whole_CODE_bytes']==s['size']and calibrated['all_payload_and_field_equal']and calibrated['actual_target_symbol']=='__aNulmul'and calibrated['MZ']==[],'runtime3 calibrated whole member')
 return cfg,m,v,cert

def render_for_comparison(u,project):
 cfg,m,v,cert=load_profile(u,project);name,s=validate_unit(u);image=bytearray(v['last_writer_bytes']);f=v['fixup'];word=(0xf32e-(s['native']+f.offset+2))&65535;image[f.offset:f.offset+2]=word.to_bytes(2,'little')
 provenance={k:val for k,val in v.items()if k not in('last_writer_bytes','fixup')};provenance.update(classification='independently_supplied_runtime_library',library_sha256=LIBSHA,config_sha256=sha((Path(project)/SOURCE).read_bytes()),member_sha256=m.sha256,library_offset=m.offset,certificate_sha256=CERTIFICATE_SHA,comparison_only=True,actual_game_LINK_input='whole genuine LIBH.LIB unchanged, never this view/object replacement',comparison_relocation={'image_offset':s['native']+f.offset,'width':2,'mode':'self_relative_code','target_symbol':'__aNulmul','target_offset':0xf32e,'encoded_value':word,'mz_relocation_image_offset':None,'raw':f.raw.hex()},actual_raw_field={**asdict(f),'raw':f.raw.hex()},native_MZ=[],authored_c_credit=0)
 return Runtime3Result(bytes(image),m.data,provenance)
