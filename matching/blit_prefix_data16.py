"""Closed C5 initialized Blit consumed-prefix24 profile; no generic LIDATA relaxation.

Raw OMF is never patched. Generation takes only a source path and pinned tools;
comparison bytes/placements are not accepted or read by this module.
"""
from dataclasses import asdict,dataclass
from pathlib import Path
import hashlib
from msc import compile_c,validate_toolchain
from omf import read_omf,OMFError
BACKEND='msc500-blit-prefix-data-omf'
SYMBOL='_blit'
FLAGS=['/AS','/Zl','/Zi']
SOURCE_SHA256='0ab47498d057dc56f36d510d78a8290606302962b8952269a96391edbf564668'
OBJECT_SHA256='749a6e4f0967bc1febd83a70849b0f9b88e6b40997d05c77e368e83faad587d2'
MANIFEST_SHA256='d2889507d0729b9d09fb92015fedccbb533c368d428c1612781c3ff980f00a82'
TOOL_HASHES={'CL.ERR': 'b153605db3fbc0fa79e2f0d2ad5d814fbb70bfbebc1dbc0d2ed614194666621a', 'CL.EXE': '11e3c7d53b3efc085b7ad90c2190a1ddb395c8874f57aef3a5cfc0a4a0a0f504', 'C1.EXE': '3ef764476cb56dd14ae3c955a0b7717976d3b40f862fdff675ec8c6adc0ed791', 'C1.ERR': 'dd02a004e8912c96b90a5b3317dcfeed6f9e76374edfd90979705035c8097233', 'C2.EXE': '19fbe7914ba6ebe929a0e98e012fd5e8522643e5e40b6fcd89bef0e5f650f1f1', 'C3.EXE': 'ca4d82b90423086e68eb8d3af8f1c1c1034f164d0a0b98530c3b3a0fb0501669', 'C23.ERR': '75132883ac6507cccaa7d7105df6492f511ba029e4a12ee4a1fcc989517bfd18'}
CV=bytes.fromhex('010100800101008001010080010e007985c0000a830402830502820069011f007f83810083810083810083810083810083810083810083810083e00083e0000175007f82057368696674880082046d6f6465880282057769647468880482066865696768748806820b736f757263655f736b697088088209646573745f736b6970880a82096c6566745f6d61736b880c820a72696768745f6d61736b880e820b64657374696e6174696f6e88108206736f757263658814')
KINDS=[0x80,0x88,0x88,0x96]+[0x98]*6+[0x9a,0x9c,0x8c,0x90,0x88,0xa0,0xa2,0xa0,0x8a]
NAMES=['shift','mode','width','height','source_skip','dest_skip','left_mask','right_mask','destination','source']
OFFSETS=[0,2,4,6,8,10,12,14,16,20]
class BlitPrefixDataError(OMFError):pass

def require(value,message):
 if not value:raise BlitPrefixDataError(message)
def sha(data):return hashlib.sha256(data).hexdigest()

def validate_unit(unit):
 require(unit.get('language')=='c-data'and unit.get('backend')==BACKEND,'blit prefix backend/language mismatch')
 require(unit.get('symbol')==SYMBOL and unit.get('flags')==FLAGS,'blit prefix symbol/flags mismatch')
 require(type(unit.get('size'))is int and unit['size']==24 and unit.get('reference_region')=='exepack-expanded'and int(unit.get('image_offset','-1'),0)==0x61544,'blit prefix comparison extent/profile mismatch')
 require(not unit.get('externals')and not any(unit.get(k)is not None for k in ['owned_data','owned_const','owned_const_profile','owned_selector_const','owned_bss','extended_extent','code_address','data_address','compiler_source_name']),'blit prefix permits no placement aliases or code ownership')

def extract_data(object_bytes,symbol=SYMBOL):
 """Decode only whole initialized DATA24 and actual single 11-word LIDATA leaf.

 SEGDEF/CV/leaf arithmetic determine the full result. No expected size or target
 bytes enter extraction. Real unsupported-data state is retained in metadata.
 """
 require(isinstance(object_bytes,bytes),'blit prefix requires unchanged raw OMF bytes')
 require(symbol==SYMBOL,'blit prefix unexpected public')
 o=read_omf(object_bytes)
 require([k for k,_,_ in o.records]==KINDS,'blit prefix unreviewed record sequence/allocation')
 require(o.names==['','','DGROUP','_TEXT','CODE','_DATA','DATA','CONST','_BSS','BSS','$$TYPES','DEBTYP','$$SYMBOLS','DEBSYM'],'blit prefix LNAMES identity changed')
 expected=[('_TEXT','CODE',0,72),('_DATA','DATA',24,72),('CONST','CONST',0,72),('_BSS','BSS',0,72),('$$SYMBOLS','DEBSYM',0,32),('$$TYPES','DEBTYP',183,32)]
 require([(s.name,s.class_name,s.length,s.attributes)for s in o.segments.values()]==expected,'blit prefix segment allocation/attributes changed')
 require([b.hex()for k,_,b in o.records if k==0x98]==['480000030401','481800050601','480000070701','480000080901','2000000c0d01','20b7000a0b01'],'blit prefix segment overlay/identity changed')
 require(not o.fixups and not o.procedures,'blit prefix forbids fixups/procedures')
 require(o.externals=={1:'__acrtused'},'blit prefix foreign externals/startup marker')
 require(set(o.publics)=={SYMBOL},'blit prefix public aliases/count changed')
 p=o.publics[SYMBOL];require((p.segment,p.offset,p.group,p.type_index)==(2,0,1,0x203),'blit prefix public/group/struct type changed')
 fixed={0x80:[b'\x09C:\\UNIT.C'],0x88:[bytes.fromhex(x)for x in ['009d30734f','00a1014356','00a201']],0x9a:[bytes.fromhex('02ff03ff04ff02')],0x9c:[bytes.fromhex('000301020201030440014501')],0x8a:[b'\0']}
 for k,rows in fixed.items():require([b for kind,_,b in o.records if kind==k]==rows,'blit prefix header/DGROUP/directive changed')
 require(o.segments[2].chunks==[(0,b'\0\0')]and o.segments[2].unsupported_data,'blit prefix exact first-word LEDATA required')
 require(all(not s.chunks and not s.unsupported_data for i,s in o.segments.items()if i not in[2,6]),'blit prefix extra initialized allocation')
 require(o.segments[6].chunks==[(0,CV)]and not o.segments[6].unsupported_data,'blit prefix complete struct CV changed')
 types=[];at=0
 while at<len(CV):
  n=int.from_bytes(CV[at+1:at+3],'little');raw=CV[at:at+3+n];types.append({'type_index':0x200+len(types),'offset':at,'raw_hex':raw.hex()});at+=len(raw)
 struct_type=bytes.fromhex(types[3]['raw_hex']);bits=int.from_bytes(struct_type[5:7],'little');count=struct_type[7]
 require(types[3]['type_index']==p.type_index and bits%8==0 and bits//8==o.segments[2].length and count==len(NAMES),'blit prefix struct CV/SEGDEF extent mismatch')
 members=[];raw=bytes.fromhex(types[5]['raw_hex']);cursor=4
 for i,name in enumerate(NAMES):
  require(raw[cursor]==0x82,'blit prefix CV member name leaf changed');n=raw[cursor+1];start=cursor+2;actual=raw[start:start+n].decode('ascii');cursor=start+n
  require(raw[cursor]==0x88,'blit prefix CV member offset leaf changed');offset=raw[cursor+1];cursor+=2
  require(actual==name and offset==OFFSETS[i],'blit prefix CV meaningful member layout changed')
  members.append({'name':name,'offset':offset,'size':2 if i<8 else 4,'type':'int'if i<8 else'char huge *','raw_type_index':0x81 if i<8 else 0xe0})
 require(cursor==len(raw),'blit prefix extra CV members')
 lidata=next((at,b)for k,at,b in o.records if k==0xa2);payload=lidata[1]
 require(len(payload)==10,'blit prefix malformed/trailing LIDATA')
 segment=payload[0];offset=int.from_bytes(payload[1:3],'little');repeat=int.from_bytes(payload[3:5],'little');children=int.from_bytes(payload[5:7],'little');n=payload[7];literal=payload[8:]
 require(segment==2 and offset==2,'blit prefix foreign/overlapping/holey LIDATA')
 require(children==0 and n==2 and len(literal)==n,'blit prefix nested/malformed LIDATA')
 require(repeat==11 and literal==b'\0\0','blit prefix unreviewed repeat/literal')
 data=o.segments[2].chunks[0][1]+literal*repeat
 require(len(data)==o.segments[2].length==bits//8,'blit prefix incomplete initialized ownership')
 require(sha(object_bytes)==OBJECT_SHA256,'blit prefix complete deterministic OMF changed')
 return data,{'boundary':'complete_omf_data_segment','symbol':SYMBOL,'segment':{'index':2,'name':'_DATA','class_name':'DATA','length':len(data),'attributes':72},'public':asdict(p),'publics':{SYMBOL:asdict(p)},'group':{'index':1,'name':'DGROUP','segments':[3,4,2]},'data_writes':[{'kind':'LEDATA','offset':0,'length':2,'literal_hex':'0000'},{'kind':'LIDATA','record_offset':lidata[0],'raw_payload':payload.hex(),'offset':offset,'repeat_count':repeat,'child_blocks':children,'literal_hex':literal.hex(),'length':repeat*n}],'cv':{'records':types,'raw_hex':CV.hex(),'struct_bit_size':bits,'members':members},'all_segments':[{'index':s.index,'name':s.name,'class_name':s.class_name,'length':s.length,'attributes':s.attributes,'unsupported_data_retained':s.unsupported_data}for s in o.segments.values()],'object_sha256':sha(object_bytes),'sha256':sha(data),'startup_marker_unused':True,'thread_only_FIXUPP_retained':True,'emitted_mz_sites':[],'authored_c_function_count':0,'historical_aggregate_boundary_proven':False,'larger_historical_capacity_unknown':True,'six_gap_bytes_allocated':False}

def validate_compiled(c,source_bytes):
 require(sha(source_bytes)==SOURCE_SHA256 and c.source_sha256==SOURCE_SHA256,'blit prefix reviewed source fingerprint changed')
 require(c.compiler=='msc500'and list(c.flags)==FLAGS and c.source_name=='UNIT.C','blit prefix compiler/profile changed')
 require(c.toolchain_manifest_sha256==MANIFEST_SHA256 and c.tool_hashes==TOOL_HASHES,'blit prefix pinned tools/manifest changed')
 require(tuple(c.command)==('T:\\CL.EXE','/c',*FLAGS,'/FoC:\\UNIT.OBJ','C:\\UNIT.C'),'blit prefix compiler command changed')
 return extract_data(c.object_bytes)

@dataclass(frozen=True)
class Built:
 object_bytes:bytes
 data:bytes
 metadata:dict
 provenance:dict

def build(source):
 source=Path(source);require(not source.is_symlink(),'blit prefix source symlink forbidden');before=source.read_bytes()
 require(sha(before)==SOURCE_SHA256,'blit prefix reviewed source fingerprint changed')
 manifest,tools=validate_toolchain(compiler='msc500');require(manifest==MANIFEST_SHA256 and tools==TOOL_HASHES,'blit prefix tool pins changed')
 c=compile_c(source,FLAGS,compiler='msc500');require(source.read_bytes()==before,'blit prefix source changed during generation')
 data,metadata=validate_compiled(c,before);provenance=asdict(c);provenance.pop('object_bytes')
 return Built(c.object_bytes,data,metadata,provenance)
