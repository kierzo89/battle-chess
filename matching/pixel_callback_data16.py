"""Exact complete DATA6 containing three near CODE function pointer fields.

Distinct from cdata_pointer's DS-pointer contract. Raw zero addends are linked
only by named CODE placements, with genuine target-derived frame5. No native
bytes, aliases, numeric C pointer initializers, trims or wider capacities.
"""
from pathlib import Path
from dataclasses import asdict
import hashlib,json
from omf import read_omf,OMFError,OMFObject
from library16 import link_segment
from pixel_callback_data_pins import SOURCE_SHA,OBJECT_SHA,MANIFEST_SHA,TOOLS,REA_SHA
BACKEND='msc500-near-code-callback-data6-v1'
SOURCE='src/data/pixel_callbacks.c';FLAGS=['/AS','/Zl'];ORIGIN=0x5d0c6;DS=0x5cc2;BASE=0x4a6
CODE={'_plot_region_5a7c':[0,0x5a7c],'_bios_plot_pixel_ea64':[0,0xea64]}
EXPECTED_FIELDS={0:'_plot_region_5a7c',2:'_plot_region_5a7c',4:'_bios_plot_pixel_ea64'}
class PixelCallbackError(OMFError):pass
def need(v,m):
 if not v:raise PixelCallbackError('pixel callback DATA6: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def validate_shape(o):
 need(isinstance(o,OMFObject),'strict OMF object required')
 need([(i,s.index,s.name,s.class_name,s.length,s.attributes)for i,s in o.segments.items()]==[(1,1,'_TEXT','CODE',0,72),(2,2,'_DATA','DATA',6,72),(3,3,'CONST','CONST',0,72),(4,4,'_BSS','BSS',0,72)],'exact four segments/whole DATA6/empty CODE CONST BSS')
 need(o.segments[2].chunks==[(0,bytes(6))]and not any(s.unsupported_data or(s.chunks and i!=2)for i,s in o.segments.items()),'one contiguous DATA6 zero-addend LEDATA; no hole/overlap/other writes')
 need(not o.procedures,'no procedures or debug')
 need({n:(p.name,p.segment,p.offset,p.group,p.type_index)for n,p in o.publics.items()}=={'_plot_pixel':('_plot_pixel',2,0,1,0),'_pixel_writers':('_pixel_writers',2,2,1,0)},'exact distinct PUBLICs0/2; no aliases')
 need(o.externals=={1:'__acrtused',2:'_plot_region_5a7c',3:'_bios_plot_pixel_ea64'},'exact named CODE targets and unused startup marker')
 groups=[]
 for k,at,p in o.records:
  need(k in{0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0x90,0xa0,0x8a},'supported record kinds only')
  if k==0x88:need(p in[bytes.fromhex(s)for s in ['009d30734f','00a1014356','00a201']],'exact C500 comments')
  if k==0x9a:groups.append(p)
  if k==0x8a:need(p==b'\0','no entry point')
 need(groups==[bytes.fromhex('02ff03ff04ff02')],'exact complete DGROUP; DATA placement distinct from CODE target frames')
 need(len(o.fixups)==3,'exact three fields')
 seen=set()
 for f in o.fixups:
  need(f.segment==2 and f.offset in EXPECTED_FIELDS and f.offset not in seen,'three distinct complete fields0/2/4')
  seen.add(f.offset)
  need(f.width==2 and f.location_type==1 and f.segment_relative is True and f.frame==(5,None)and f.target[0]==2 and o.externals.get(f.target[1])==EXPECTED_FIELDS[f.offset]and f.displacement is None,'true target-derived near CODE OFFSET16; no DS group frame/BASE/far/marker/addend')
  need(f.raw==bytes.fromhex({0:'c4005602',2:'c4025602',4:'c4045603'}[f.offset]),'exact genuine raw field encoding')
 return {'boundary':'complete_DATA6_three_near_CODE_callbacks','raw_data_bytes':6,'publics':{n:asdict(p)for n,p in o.publics.items()},'source_table_entries':2,'source_callback_slots':1,'raw_FIXUPP_fields':3,'unused_startup_marker_preserved':True,'authored_C_function_credit':0,'historical_capacity_TU_storageclass_or_physical_placement_proven':False}
def validate_raw(raw):
 need(isinstance(raw,bytes),'whole raw bytes');o=read_omf(raw);proof=validate_shape(o);need(sha(raw)==OBJECT_SHA,'exact untouched genuine whole object hardpin');return o,proof
def link_code_callbacks(raw,code_externals):
 o,proof=validate_raw(raw)
 need(isinstance(code_externals,dict)and set(code_externals)==set(CODE),'exact named CODE bindings')
 for n,v in code_externals.items():
  need(isinstance(v,(tuple,list))and len(v)==2 and all(type(x)is int for x in v)and list(v)==CODE[n],'CODE paragraph0/true near offset; DS bindings forbidden')
 # SOURCE allocation's DATA lives in DS. Pointer values are offsets within
 # CODE frame0: library16 frame5 derives frame from each target, NOT DGROUP.
 linked,fields=link_segment(o,2,{2:[DS,BASE]},{1:DS},code_externals)
 need(len(linked)==6 and len(fields)==3,'complete linked span and fields')
 for f in fields:
  at=f['object_offset'];need(f['mode']=='offset16'and f['target_paragraph']==f['frame_paragraph']==0 and f['target_symbol']==EXPECTED_FIELDS[at]and f['original_addend']==f['displacement']==0 and f['encoded_value']==CODE[f['target_symbol']][1]and f['mz_relocation_image_offset']is None,'actual CODE-frame arithmetic/no native MZ')
 proof.update(DATA_origin=ORIGIN,DATA_DGROUP={'paragraph':DS,'offset':BASE},CODE_bindings={n:list(v)for n,v in code_externals.items()},relocations=fields,emitted_mz_sites=[],whole_raw_object_sha256=sha(raw),linked_sha256=sha(linked))
 return linked,proof
def validate_unit(u):
 need(u['id']=='pixel_callbacks_04a6'and u['language']=='c-data'and u['backend']==BACKEND and u['source']==SOURCE and u['symbol']=='_plot_pixel'and type(u['size'])is int and u['size']==6 and int(u['image_offset'],0)==ORIGIN and u['reference_region']=='exepack-expanded'and u['flags']==FLAGS and u['code_externals']==CODE and not u.get('externals'),'exact profile unit and CODE bindings')
 need(u['rea_evidence']=='build/pen-callback-data-recovery/rea-callbacks6.json'and not any(k in u for k in ['extended_extent','owned_data','owned_const','owned_selector_const','owned_code_address_consts']),'no borrowed/extended ownership')
def validate_compiled(compiled,source_bytes,u):
 validate_unit(u);need(sha(source_bytes)==compiled.source_sha256==SOURCE_SHA and compiled.compiler=='msc500'and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'and compiled.toolchain_manifest_sha256==MANIFEST_SHA and compiled.tool_hashes==TOOLS,'exact source/compiler/flags/whole provenance')
 return link_code_callbacks(compiled.object_bytes,u['code_externals'])
def validate_evidence(u,project,reference,linked,fields):
 validate_unit(u);p=Path(project)/u['rea_evidence'];need(sha(p.read_bytes())==REA_SHA,'retained primary SHA');e=json.loads(p.read_text());n=e['normalized_result'];q=e['analysis_profile']['parameters']
 from reference import ORIGINAL_SHA256,CARRIER_SHA256
 need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==e['subject']['digest']['sha256']==CARRIER_SHA256,'original/carrier proof')
 need(e['evidence_id']=='ev_2637173be096e2fb21417284adb0da5da49d544308b51f8a88486d72fb3cda7f'and e['operation']=='read_bytes'and e['parameters']=={'address':'0x6d0c6','length':6}and q['language_id']=='x86:LE:16:Real Mode'and q['load_segment']=='0x1000'and q['target_format']=='dos-mz'and n['complete']and n['requested_bytes']==n['returned_bytes']==6,'exact full raw primary')
 need(len(linked)==6 and linked==reference['image'][ORIGIN:ORIGIN+6]==bytes.fromhex(n['bytes_hex']),'all six native bytes equal')
 need(not any(ORIGIN-1<=site<ORIGIN+6 for site in reference['relocations'])and len(fields)==3 and all(f['mz_relocation_image_offset']is None for f in fields),'complete original/emitted native MZ empty')
 return e['evidence_id']
