"""Closed six native int COMMON providers; source-only allocation, zero byte credit.

No original BSS order/MAP is imposed. Existing source-input profiles are unchanged.
"""
from pathlib import Path
import dataclasses,hashlib,json
from msc import compile_c
from omf import read_omf,_Cursor
from reference import build_reference,ORIGINAL_SHA256
BACKEND='msc500-near-common-search-words-v1'
SOURCE='src/link/search_word_state.c'
SOURCE_SHA='bed856af741c607d4994e2d0a0c8663f3c2afa86662b4c3969aff96a1136a1d9'
OBJECT_SHA='b7bd98e77f649197e234ab4440bb778ed24714b39d15fcf69d03b3044d04f8ae'
MANIFEST_SHA='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOL_HASHES={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
PINS={'layout': {'path': 'build/search-word-common-followup/proof.json', 'sha256': 'd7befaacc480eb1e5356b60450c709da0de0294f9238b271939fb347ac99abbd'}, 'native_review': {'path': 'build/search-word-common-followup/native-type-review.json', 'sha256': 'a69c749d0ff996b3fe2a46e56e834473897456ec5242929afd669310bc418419'}, 'native': {'path': 'evidence/rea_moves_engine_a528.json', 'sha256': '3b674a13ed365648a3fdbf63beb01a9041ee2f0fadec93c26bb27b8633da9e7a'}, 'crt': {'path': 'evidence/rea_crt_startup_500.json', 'sha256': 'f1ef14871734df318dcf05a9ea366706a46bf2484a5623678271df7cf612d1ad'}}
FLAGS=['/AS','/Zl','/Zi']
NAMES=['_first_score','_window_limit','_position_score','_interrupted','_input_state','_search_level']
OFFSETS=[0x53f6,0x8b2c,0x922c,0x9340,0x9854,0xa838]
KEYS={'id','backend','source','source_sha256','compiler','flags','toolchain_manifest_sha256','objects','evidence'}
PROFILE_DIGEST='894e458d232de9bdeb2a5d661cd2b4791ee9e10f88d297423fc0c7553a7a66d8'
def require(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def local(project,path):
 p=(Path(project)/path).resolve();require(p.is_relative_to(Path(project).resolve()),'search-word input path escape');return p
def validate_item(item):
 require(isinstance(item,dict)and set(item)==KEYS,'unknown search-word allocation fields')
 require(item['id']=='search-word-state-common'and item['backend']==BACKEND and item['source']==SOURCE and item['source_sha256']==SOURCE_SHA and item['compiler']=='msc500'and item['flags']==FLAGS and item['toolchain_manifest_sha256']==MANIFEST_SHA,'unreviewed search-word source/profile')
 require(item['objects']==[{'symbol':n,'size':2,'storage':'near-common'}for n in NAMES],'incomplete six-word COMMON selection')
 require(item['evidence']==PINS,'search-word evidence set/identity changed')
def validate_object(raw):
 o=read_omf(raw)
 require(not o.publics and not o.procedures,'search-word COMMON defines PUBLIC/function')
 expected=[('_TEXT','CODE',0,0x48),('_DATA','DATA',0,0x48),('CONST','CONST',0,0x48),('_BSS','BSS',0,0x48),('$$SYMBOLS','DEBSYM',125,0x20),('$$TYPES','DEBTYP',0,0x20)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'search-word loaded/debug allocation changed')
 require(not any(s.unsupported_data for s in o.segments.values()),'search-word iterated data forbidden')
 require(all(k in {0x80,0x88,0x96,0x98,0x9a,0x8c,0xb0,0x9c,0xa0,0x8a}for k,_,_ in o.records),'unreviewed search-word OMF record')
 definitions=[]
 for kind,_,payload in o.records:
  if kind==0xb0:
   c=_Cursor(payload)
   while c:
    name,typ,datatype,size=c.name(),c.index(),c.byte(),c.byte()
    require(datatype==0x62 and size==2 and typ==0x81,'search-word requires native signed-int near COMMON2')
    definitions.append({'symbol':name,'size':size,'datatype':datatype,'type_index':typ})
  elif kind==0x88:require(payload in (bytes.fromhex('009d30734f'),bytes.fromhex('00a1014356'),bytes.fromhex('00a201')),'unreviewed search-word linker directive')
  elif kind==0x9a:require(payload==bytes.fromhex('02ff03ff04ff02'),'search-word DGROUP changed')
  elif kind==0x8a:require(payload==b'\0','search-word allocation has entrypoint')
 require([x['symbol']for x in definitions]==NAMES,'search-word missing/extra/duplicate/reordered COMMON')
 require(o.externals==dict(enumerate(['__acrtused']+NAMES,1)),'search-word external set/order changed')
 require(all(seg==5 for _,seg,_,_ in o.data_writes),'search-word initialized nondebug data')
 require(len(o.fixups)==6,'search-word debug fixup count changed')
 for f,(off,target)in zip(o.fixups,zip([106,86,66,43,22,2],range(7,1,-1))):
  require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement)==(5,off,4,3,True,(5,None),(2,target),None),'search-word nondebug or changed CodeView field')
 require(sha(raw)==OBJECT_SHA,'complete reviewed search-word OMF/CV object changed')
 return definitions

def validate_evidence(project,pins,target):
 require(pins==PINS,'search-word evidence identity changed');payloads={}
 for key,pin in pins.items():
  b=local(project,pin['path']).read_bytes();require(sha(b)==pin['sha256'],'search-word evidence pin mismatch');payloads[key]=json.loads(b)
 target=Path(target);require(sha(target.read_bytes())==ORIGINAL_SHA256,'search-word original target changed');r=build_reference(target.read_bytes());image=r['image']
 for key,operation,params in [('native','analyze_function',{'procedure':'0x1a528'}),('crt','read_bytes',{'address':'0x1ea86','length':179})]:
  e=payloads[key];p=e['analysis_profile']['parameters']
  require(e['subject']['digest']['sha256']==ORIGINAL_SHA256 and e['subject']['format']=='dos-mz'and e['subject']['architecture']=='x86'and e['provider']['id']=='ghidra'and e['analysis_profile']['digest']==PROFILE_DIGEST and p['loader']=='MzLoader'and p['language_id']=='x86:LE:16:Real Mode'and p['load_segment']=='0x1000'and p['address_coordinates']=='linear-byte-offset'and e['operation']==operation and e['parameters']==params,'search-word native subject/profile/operation changed')
 require(payloads['native']['evidence_id']!=payloads['crt']['evidence_id'],'search-word duplicate primary IDs')
 review=payloads['native_review'];layout=payloads['layout'];require(review['source_API_compatible']and not review['alias_or_definition_conflicts']and review['existing_COMMON_count']==51 and not set(NAMES).intersection(review['existing_COMMON_names']),'search-word source/native identity conflict')
 require(layout['source_sha256']==SOURCE_SHA and layout['object_sha256']==OBJECT_SHA and layout['complete_object']['initialized_bytes']==0 and layout['matching_credit']==0,'search-word fresh source/model layout proof changed')
 assembly=payloads['native']['normalized_result']['assembly'];constraints=[]
 for name,off,row in zip(NAMES,OFFSETS,review['names']):
  require(row['symbol']==name and row['type']=='int'and row['size']==2 and row['native_DS']==hex(off)and row['file_backed_bytes']==0 and row['source_COMMON_already_supplied']is False and row['native_MAP_or_BSS_allocation_order_proven']is False,'search-word native scalar model changed')
  lines=[l for l in assembly if '['+hex(off)+']'in l];require(lines==row['actual_WORD_accesses']and lines and all('byte ptr'not in l for l in lines),'search-word native WORD evidence changed')
  require(0x52cc<=off and off+2<=0xcbe0 and 0x5cc20+off>=len(image),'search-word outside actual native CRT/nonfilebacked interval')
  constraints.append({'symbol':name,'dgroup_segment':'0x5cc2','dgroup_offset':hex(off),'end_exclusive':hex(off+2),'inside_native_startup_clear':['0x52cc','0xcbe0'],'native_final_MAP_or_BSS_order_proven':False,'resolved':False})
 cr=payloads['crt']['normalized_result'];clear=bytes.fromhex('bfcc52b9e0cb2bcf33c0f3aa')
 require(cr['complete']and cr['requested_bytes']==cr['returned_bytes']==179 and bytes.fromhex(cr['bytes_hex'])==image[0xea86:0xeb39]and image[0xeaed:0xeaed+len(clear)]==clear,'search-word native fullCRT/clear bounds changed')
 return constraints

def build_input(item,project,target,output,*,compiler_fn=None):
 validate_item(item);project=Path(project).resolve();source=local(project,SOURCE);before=source.read_bytes();require(sha(before)==SOURCE_SHA,'search-word source pin mismatch');fn=compile_c if compiler_fn is None else compiler_fn
 # Actual fresh source compilation precedes original/native comparison access.
 c=fn(source,FLAGS,compiler='msc500');require(source.read_bytes()==before and c.source_sha256==SOURCE_SHA and c.toolchain_manifest_sha256==MANIFEST_SHA and c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C'and c.tool_hashes==TOOL_HASHES,'search-word fresh compiler/source/tool provenance changed')
 definitions=validate_object(c.object_bytes);constraints=validate_evidence(project,item['evidence'],target);output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/'search-word-state-common.obj';path.write_bytes(c.object_bytes);meta=dataclasses.asdict(c);meta.pop('object_bytes')
 return {'id':item['id'],'source':SOURCE,'object':str(path),'object_sha256':sha(c.object_bytes),'definitions':definitions,'allocation_bytes':12,'initialized_bytes':0,'matching_credit':0,'original_map_constraints':constraints,'placement_proven':False,'compiler':meta,'allocation_profile':'six_native_signed_int_search_scalars','authored_C_function_credit':0,'diagnostic_LINK_or_CRT_execution_claim':False}
