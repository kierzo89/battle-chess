"""Finite eight-owner C literal allocation; raw hole is never materialized here.

SOURCE-ready tokens are not matches. Only the live fresh aggregate can authorize
all eight rows after authentic LINK proves the complete allocation's alignment.
"""
from pathlib import Path
from dataclasses import dataclass,asdict
import json,hashlib
from omf import read_omf,OMFError
from library16 import link_segment,LibraryError
from reference import ORIGINAL_SHA256,CARRIER_SHA256,validate_expanded_read
POLICY='packet-literals61-alignment1-v1';BACKEND='msc500-packet-owned-literals61-omf-v1';SOURCE='src/packet_literal_context_match.c';FLAGS=['/AS','/Zi'];_CAP=object()
PROFILE_SHA256='8d79c608a6c77c9cdcf0b1f8958bfaeb2468fd4f29ca1afeaecc7b7675729bf2'
class PacketError(OMFError):pass
def need(v,m):
 if not v:raise PacketError('packet61: '+m)
def H(b):return hashlib.sha256(b).hexdigest()
def safe(x):
 if hasattr(x,'__dataclass_fields__'):return safe(asdict(x))
 if isinstance(x,bytes):return x.hex()
 if isinstance(x,dict):return{str(k):safe(v)for k,v in x.items()}
 if isinstance(x,(tuple,list)):return[safe(v)for v in x]
 return x
def canon(x):return json.dumps(safe(x),sort_keys=True,separators=(',',':'))
def profile():
 raw=Path(__file__).with_name('packet_literal61_profile.json').read_bytes();need(H(raw)==PROFILE_SHA256,'exact versioned profile');return json.loads(raw)
def contracts():return{u['id']:u for u in profile()['all8_unit_contracts']}
def validate_unit(u):need(u.get('id')in contracts()and canon(u)==canon(contracts()[u['id']]),'exact one of eight unit/source/view contracts')
def snapshot(o):return{'records':[[k,a,p.hex()]for k,a,p in o.records],'names':o.names,'segments':safe(o.segments),'publics':safe(o.publics),'procedures':safe(o.procedures),'fixups':safe(o.fixups),'data_writes':safe(o.data_writes)}
def validate_raw(raw):
 p=profile();need(type(raw)is bytes and len(raw)==p['raw_size']and H(raw)==p['raw_SHA256'],'whole genuine source object');o=read_omf(raw);need(canon(snapshot(o))==canon(p['whole_snapshot']),'all original raw records/TYPE/CV/fields/writes unchanged');need(o.segments[3].chunks[0][0]==0 and[(a,len(b))for a,b in o.segments[3].chunks]==[(0,37),(38,24)]and o.segments[3].length==62 and not o.segments[3].unsupported_data,'only exact literal61/rawhole37/fullspan62 shape')
 need(len(o.fixups)==57 and len(o.procedures)==len(o.publics)==6 and not any(f.target==(0,0)for f in o.fixups),'all57 fields/sixrealCV/no inventedPUBLIC/SEG0');return o

def _code(o):
 out=bytearray()
 for at,b in sorted(o.segments[1].chunks):need(at==len(out)and b,'whole CODE856 no hole/trim');out.extend(b)
 need(len(out)==856 and out[-1:]==b'\x90','whole CODE856 with genuine tail90');return bytes(out)
def native_core(raw,reference,project):
 o=validate_raw(raw);p=profile();need(reference['original_sha256']==ORIGINAL_SHA256 and reference['carrier_sha256']==CARRIER_SHA256,'independent native comparison context');image=reference['image'];need(not[x for x in reference['relocations']if x<0xe03a and x+2>0xdce2 or x<0x61e12 and x+2>0x61dd4],'complete CODE/pool MZ0')
 rawcode=_code(o);views=(o.segments[3].chunks[0][1],o.segments[3].chunks[1][1]);need(views[0]==image[0x61dd4:0x61df9]and views[1]==image[0x61dfa:0x61e12]and len(views[0])==37 and len(views[1])==24,'two complete genuine C literal objects, never a filled62-byte vector')
 native_ids={}
 for u in p['all8_unit_contracts']:
  if u['language']=='c-data':
   native_ids[u['id']]=validate_expanded_read(json.loads((Path(project)/u['rea_evidence']).read_text()),u,views[0 if u['size']==37 else 1],reference)
 bindings={n:v for u in p['all8_unit_contracts']for n,v in u.get('externals',{}).items()};near={o.externals[f.target[1]]for f in o.fixups if f.segment==1 and not f.segment_relative and f.target[0]==2};bases=[];code=None;fields=None
 for load in[0,1,4096,65535]:
  ds=(0x5cc2+load)&65535;placements={s.index:((load,0xdce2)if s.index==1 else(ds,0x51b4 if s.index==3 else 0))for s in o.segments.values()};ext={n:((load if n in near else ds),v)for n,v in bindings.items()};value,logs=link_segment(o,1,placements,{1:ds},ext);need(value==image[0xdce2:0xe03a]and len(logs)==36 and all(q['mz_relocation_image_offset']is None for q in logs),'whole CODE856/all36 native fields/fourbases');bases.append(load)
  if load==0:code=value;fields=logs
 from packet_receiver_literal61_native import validate_native
 receiver=contracts()['receive_packet_ddd3'];nativeproof=validate_native(receiver,Path(project),ORIGINAL_SHA256,o.function_info(receiver['symbol']),code[241:655])
 need(sum(o.function_info(n)['size']for n in o.procedures)==855,'all real CV855, tail uncredited')
 return {'code':code,'arrays':views,'relocations':fields,'four_bases':bases,'receiver_native_extent':nativeproof,'literal_REA_ids':native_ids,'raw_initialized_bytes':61,'raw_unwritten_offsets':[37],'allocation_complete':False,'alignment_match_or_credit':False}

class RunContext:
 def __init__(self,cap,lifecycle,project,output):
  need(cap is _CAP,'private current-run context factory');self._cap=cap;self.lifecycle=lifecycle;self.project=Path(project).resolve();self.output=Path(output).resolve();self.group=None;self.cache=None;self.source=None;self.observer=None;self.state='PARTITIONED_SOURCE_GROUP';self.finished=False
 def valid(self):
  from fresh_lifecycle import FreshLifecycle
  need(self._cap is _CAP and type(self.lifecycle)is FreshLifecycle and self.lifecycle.project==self.project and self.lifecycle.components.resolve()==self.output,'exact same current lifecycle/project/component context');need(self.lifecycle.packet_context is self,'context owned by current lifecycle');need(self.group is None or type(self.group)is _Group,'private group type, no duck-typed cache');need(self.source is None or self.lifecycle.seal is self.source,'same lifecycle seal object');return True
@dataclass(frozen=True)
class PendingOwner:
 cap:object
 group:object
 unit_json:str
 @property
 def unit_id(self):return json.loads(self.unit_json)['id']
class _Group:
 def __init__(self,cap,ctx,compiled,core,artifact):
  need(cap is _CAP,'private fresh group factory');self._cap=cap;self.ctx=ctx;self.compiled=compiled;self.core=core;self.artifact=Path(artifact).resolve();self.issued={};self.raw_sha=H(compiled.object_bytes)
 def valid(self):
  self.ctx.valid();need(self._cap is _CAP and self.ctx.group is self and self.raw_sha==profile()['raw_SHA256']and H(self.compiled.object_bytes)==self.raw_sha and self.artifact.read_bytes()==self.compiled.object_bytes,'unmodified exact live compiled group/artifact');return True

def registration(descriptor):
 jobs=descriptor.get('source_allocation_jobs',[])
 if not jobs:
  need(not any(r['source']==SOURCE for r in descriptor['rows']),'packet source cannot omit required group registration');return None
 p=profile();need(len(jobs)==1 and jobs[0]=={'policy':POLICY,'module':'packet_literal61','module_sha256':H(Path(__file__).read_bytes()),'profile_sha256':PROFILE_SHA256,'owners':p['owners'],'source':SOURCE,'source_sha256':p['source_SHA256'],'raw_sha256':p['raw_SHA256']},'sole exact packet8 registration')
 rows=[r for r in descriptor['rows']if r['source']==SOURCE];need(len(rows)==1 and rows[0]['kind']=='c-whole-omf'and rows[0]['selected_owners']==p['owners']and rows[0]['source_sha256']==p['source_SHA256']and rows[0]['comparison_expected_raw_sha256']==p['raw_SHA256']and rows[0]['compiler_flags']==FLAGS and rows[0]['source_name']=='UNIT.C','one exact eight-owner SOURCE row');return jobs[0]
def new_run_context(lifecycle,units):
 from fresh_lifecycle import FreshLifecycle
 need(type(lifecycle)is FreshLifecycle and lifecycle.phase=='NEW'and registration(lifecycle.descriptor)is not None,'real registered lifecycle only');need(all(next(u for u in units if u['id']==n)==v for n,v in contracts().items()),'all eight registered unit preimages');return RunContext(_CAP,lifecycle,lifecycle.project,lifecycle.components)
def stage_owner(unit,project,cache,output,reference,compiler_fn,context):
 validate_unit(unit);need(type(context)is RunContext,'same-fresh packet context required; standalone raw-hole build stays HELD');context.valid();need(context.state=='PARTITIONED_SOURCE_GROUP'and context.lifecycle.phase=='PARTITIONED_PENDING_CRT88'and Path(project).resolve()==context.project and Path(output).resolve()==context.output and type(cache)is dict,'same source phase/cache/output')
 source=Path(project)/SOURCE;need(H(source.read_bytes())==profile()['source_SHA256'],'exact versioned source')
 if context.cache is None:context.cache=cache
 need(context.cache is cache,'same current c_cache identity')
 key=('packet61-private',id(context),profile()['source_SHA256'],tuple(FLAGS),'UNIT.C')
 if context.group is None:
  need(key not in cache,'no injected/replayed prior cache');context.state='COMPILING_ONE_SOURCE'
  try:compiled=compiler_fn(source,FLAGS,compiler='msc500')
  except BaseException:context.state='POISONED_NO_RETRY';raise
  context.state='VALIDATING_ONE_SOURCE';p=profile();need(compiled.source_sha256==p['source_SHA256']and compiled.compiler=='msc500'and list(compiled.flags)==FLAGS and compiled.source_name=='UNIT.C'and compiled.toolchain_manifest_sha256==p['toolchain_manifest_SHA256']and compiled.tool_hashes==p['tool_hashes'],'genuine exact standard compiler/source/tools result');core=native_core(compiled.object_bytes,reference,project);directory=Path(output)/'packet-source';directory.mkdir(parents=True,exist_ok=True);artifact=directory/'packet.obj';need(not artifact.exists(),'exclusive shared group object');artifact.write_bytes(compiled.object_bytes);group=_Group(_CAP,context,compiled,core,artifact);context.group=group;cache[key]=group
 context.state='PARTITIONED_SOURCE_GROUP'
 group=context.group;need(cache.get(key)is group,'private cache entry, never parsed or fixture object alias');group.valid();need(unit['id']not in group.issued,'each packet owner requested once');token=PendingOwner(_CAP,group,canon(unit));group.issued[unit['id']]=token;return token

def split_source_results(results,context):
 context.valid();g=context.group;need(g is not None and len(g.issued)==8 and set(g.issued)==set(contracts()),'all eight source-ready tokens present');g.valid();pending=[r for r in results if type(r)is PendingOwner];need(len(pending)==8 and {r.unit_id for r in pending}==set(contracts())and all(r.cap is _CAP and r.group is g and r is g.issued[r.unit_id]and r.unit_json==canon(contracts()[r.unit_id])for r in pending),'only eight exact identity tokens, no dict/pending status waiver');ordinary=[r for r in results if type(r)is not PendingOwner];need(not any(isinstance(r,dict)and r.get('id')in contracts()for r in ordinary),'no fake matched group dict before alignment');return ordinary,pending

def bind_before_source(context,source,observer):
 from pipeline import SourceSeal
 from source_phase import SourceObserver
 context.valid();g=context.group;g.valid();need(context.source is None and type(source)is SourceSeal and source.valid()and type(observer)is SourceObserver and observer is context.lifecycle.observer and not observer.poisoned and observer.current is None and observer.roots==[],'exact live before-seal source/observer ownership')
 rows=[r for r in source.rows if r['source']==SOURCE];need(len(rows)==1,'one fresh SOURCE object');r=rows[0];need(r['selected_owners']==profile()['owners']and r['object_sha256']==g.raw_sha and Path(r['object_path']).resolve()==g.artifact,'same generated whole object and eight roles');need(observer._packet_live_results.get(r['order_slot'])is g.compiled,'same actual observed compiler result identity; retained hash equality is insufficient');context.source=source;context.observer=observer;context.state='SOURCE_BOUND';return True

def selector_metadata(context,pending):
 context.valid();g=context.group;need(len(pending)==8 and all(type(t)is PendingOwner and t.cap is _CAP and t.group is g and t is g.issued[t.unit_id]for t in pending),'only private eight-owner selector inputs');g.valid();return {t.unit_id:{**json.loads(t.unit_json),'object_artifact':str(g.artifact),'source':SOURCE,'source_sha256':profile()['source_SHA256'],'object_sha256':g.raw_sha}for t in pending}

def validate_materialized_payload(raw,payload):
 o=validate_raw(raw);need(type(payload)is bytes and len(payload)==62,'complete actual materialized allocation required; missing gap is not filled');writes=o.segments[3].chunks;need(all(payload[at:at+len(b)]==b for at,b in writes)and payload[37]==0,'all61 source payload bytes and actual zero37');return {'raw_literal_bytes':61,'actual_extent':62,'actual_alignment_byte':payload[37],'raw_hole_still_unwritten':[37],'fresh_capability':False,'credit':0}

def _materialized_allocation(group,aggregate):
 from closed_aggregate import ClosedAggregateSealV1
 from near_bss_layout_post16 import parse_map
 from packet_literal61_library_inventory import library_CONSTs
 need(type(aggregate)is ClosedAggregateSealV1,'only actual private fresh aggregate, never retained JSON/EXE fixture');aggregate.valid();ctx=group.ctx;ctx.valid();need(ctx.state=='SOURCE_BOUND'and ctx.lifecycle.phase=='AGGREGATE_LINK_CLOSED'and aggregate._source is ctx.source and aggregate.run_id==ctx.source.run_id and aggregate.SOURCE_digest==ctx.source.digest and registration(aggregate._descriptor)is not None,'exact same live SOURCE/run/descriptor allocation obligation')
 rows=aggregate.object_rows;raws=aggregate.source_raws();selected=[(i,r)for i,r in enumerate(rows)if r['source']==SOURCE];need(len(selected)==1,'one exact same-run source role');slot,row=selected[0];need(ctx.observer._packet_live_results.get(slot)is group.compiled,'same live actual compiler identity after closure');need(row['selected_owners']==profile()['owners']and row['object_sha256']==group.raw_sha and raws[slot]==group.compiled.object_bytes and Path(row['object_path']).resolve()==group.artifact,'exact whole current fresh object/owners/path')
 exe=aggregate.read_artifact('PARTIAL.EXE');import struct
 h=struct.unpack_from('<14H',exe);need(h[0]==0x5a4d and(h[2]-1)*512+(h[1]or 512)==len(exe),'whole actual MZ');header=h[4]*16;image=exe[header:];mz=[off+16*seg for off,seg in[struct.unpack_from('<HH',exe,h[12]+4*i)for i in range(h[3])]];pub,segs,ds=parse_map(aggregate.read_artifact('PARTIAL.MAP'));const=[s for s in segs if s['name']==s['class']=='CONST'];need(len(const)==1,'one actual combinedCONST');whole=const[0];need(whole['stop']+1==whole['start']+whole['length']and whole['stop']<len(image),'bounded whole actualCONST')
 cursor=0;fragments=[];own=None
 for r,raw in zip(rows,raws):
  o=read_omf(raw)
  for s in o.segments.values():
   if s.name!='CONST'and s.class_name!='CONST':continue
   need(s.name==s.class_name=='CONST'and(s.attributes>>2)&7==2 and s.attributes>>5 in[1,2,3,4,5],'real PUBLIC-combine CONST/all source alignments');a={1:1,2:2,3:16,4:256,5:4}[s.attributes>>5];at=(cursor+a-1)//a*a;need(image[whole['start']+cursor:whole['start']+at]==bytes(at-cursor),'actual observed between-source alignment bytes');f={'slot':r['order_slot'],'source':r['source'],'segment':s.index,'length':s.length,'alignment':a,'combined_offset':at,'actual_start':whole['start']+at};fragments.append(f)
   if r is row and s.index==3:own=f
   cursor=at+s.length
 inventories=[]
 for name in['only-slibc/SLIBC.LIB','only-libh/LIBH.LIB']:
  inventory=library_CONSTs(aggregate.read_artifact(name))
  for m in inventory['CONST_members']:
   if any(s['length']for s in m['CONST_segments']):need(m['PUBLICs']and not any(n in pub for n in m['PUBLICs']),'unmodeled selected nonzero library CONST: HOLD')
  inventories.append({'library':name,**inventory})
 need(cursor==whole['length']and own is not None and own['length']==62,'complete actual allocation placement from all source order/library accounting');start=own['actual_start'];payload=image[start:start+62];raw=o=None
 actual_obj=validate_raw(group.compiled.object_bytes);writes=actual_obj.segments[3].chunks;validate_materialized_payload(group.compiled.object_bytes,payload)
 need(not any(x<start+62 and x+2>start for x in mz),'actual complete CONST62 MZ0');codebase={pub[n][0]*16+pub[n][1]-p.offset for n,p in actual_obj.publics.items()};frames={pub[n][0]for n in actual_obj.publics};need(len(codebase)==len(frames)==1,'all6 real CODE PUBLICs');base=codebase.pop();frame=frames.pop();off=base-frame*16;need(all(pub[n]==(frame,off+p.offset)for n,p in actual_obj.publics.items())and off+856<=65536,'real complete CODEframe offsets')
 loads=[];codefields=None
 for load in[0,1,4096,65535]:
  groupframe=(ds+load)&65535;placements={s.index:(((frame+load)&65535,off)if s.index==1 else(groupframe,start-ds*16 if s.index==3 else 0))for s in actual_obj.segments.values()};externs={n:((v[0]+load)&65535,v[1])for n,v in pub.items()};code,fields=link_segment(actual_obj,1,placements,{1:groupframe},externs);need(code==image[base:base+856]and len(fields)==36 and not any(x<base+856 and x+2>base for x in mz),'whole actualCODE856/all36 typedfields/noMZ/fourbases');loads.append(load)
  if load==0:codefields=fields
 try:link_segment(actual_obj,3,{3:(ds,start-ds*16)},{1:ds},pub)
 except LibraryError as e:need('hole'in str(e),'strict generic rawhole rejection preserved');negative=str(e)
 else:raise PacketError('generic raw CONST hole policy was weakened')
 aggregate.valid();return payload,{'policy':POLICY,'same_fresh_aggregate':True,'retained_calibration_replay':False,'run_id':aggregate.run_id,'SOURCE_digest':aggregate.SOURCE_digest,'descriptor_sha256':aggregate.descriptor_sha256,'LINK_result_sha256':aggregate.link_result_sha256,'whole_raw_SHA256':group.raw_sha,'allocation_extent':62,'raw_literal_bytes':61,'raw_unwritten_offsets':[37],'authentic_LINK_alignment':{'IMAGE_site':start+37,'raw_offset':37,'actual_value':payload[37],'credit':0},'actual_IMAGE_range':[start,start+62],'actual_FILE_range':[header+start,header+start+62],'source_CONST_fragments':fragments,'complete_library_CONST_inventory':inventories,'actual_CODE_base':base,'all36_actual_CODE_fields':codefields,'four_bases':loads,'generic_rawhole_rejection':negative,'raw_or_parsed_object_writes_modified':False,'all_other_source_CONST_bytes_reaudited_here':False,'historical_TU_capacity_global_immutability_proven':False,'alignment_native_FILE_C_credit':0}

def complete(context,pending,aggregate,reference):
 need(type(context)is RunContext,'private production context only');context.valid();need(not context.finished and context.state=='SOURCE_BOUND','one same-run completion');group=context.group;group.valid();metadata=selector_metadata(context,pending);need(set(metadata)==set(contracts()),'whole eight-owner obligation, never partial')
 payload,proof=_materialized_allocation(group,aggregate);core=native_core(group.compiled.object_bytes,reference,context.project);need(payload==reference['image'][0x61dd4:0x61e12]and core['arrays'][0]==payload[:37]and core['arrays'][1]==payload[38:],'complete samefresh actual/native62 and both complete C arrays')
 o=validate_raw(group.compiled.object_bytes);rows={};compiled=group.compiled
 for uid,u in contracts().items():
  start=int(u['image_offset'],0);isdata=u['language']=='c-data';actual=core['arrays'][0 if u['size']==37 else 1]if isdata else core['code'][o.publics[u['symbol']].offset:o.publics[u['symbol']].offset+u['size']];need(actual==reference['image'][start:start+u['size']]and len(actual)==u['size'],'complete original owner span '+uid)
  result={**u,'status':'c_data_matched'if isdata else'c_matched','expected_size':u['size'],'actual_size':len(actual),'expected_sha256':H(actual),'actual_sha256':H(actual),'first_difference':None,'expected_byte':None,'actual_byte':None,'source_sha256':profile()['source_SHA256'],'object_sha256':group.raw_sha,'object_artifact':str(group.artifact),'compiler':'Microsoft C 5.00','compiler_flags':list(compiled.flags),'build_command':list(compiled.command),'compiler_log':compiled.compiler_log,'compiler_tool_hashes':compiled.tool_hashes,'toolchain_manifest_sha256':compiled.toolchain_manifest_sha256,'relocations':[]if isdata else[r for r in core['relocations']if start<=r['image_offset']<start+u['size']],'packet_same_aggregate_allocation':proof,'packet_literal_alignment_credit':0,'complete_allocation_verified_after_LINK':True,'emitted_mz_sites':[]}
  if isdata:result.update(emitted_data_segment={'boundary':'complete_anonymous_C_array_in_exact_same_aggregate_allocation','segment':3,'class':'CONST','size':u['size'],'array_bits':u['size']*8,'element_builtin':128,'public':None,'comparison_legacy_name_not_PUBLIC':u['symbol'],'anonymous_no_alias':True,'raw_literal_initialized_bytes':u['size'],'alignment_bytes_in_credited_array':0,'whole_context_extent':62,'full_context_same_fresh_LINK_required':True},classification='authored_c_initialized_literal_array',source_literal_bytes=u['size'],authentic_LINK_alignment_bytes=0,authored_c_function_credit=0)
  else:result.update(emitted_procedure={k:v for k,v in o.function_info(u['symbol']).items()if k!='fixups'},classification='compiler_produced_C_in_literal_allocation',authored_c_function_credit=1)
  if uid=='receive_packet_ddd3':result['extended_extent_proof']=core['receiver_native_extent']
  directory=context.output/'packet-source';(directory/(uid+'.bin')).write_bytes(actual);rows[uid]=result
 need(len(rows)==8 and sum(r['size']for r in rows.values()if r['language']=='c')==855 and sum(r['size']for r in rows.values()if r['language']=='c-data')==61,'only original C855/data61 coverage; alignment uncredited');context.finished=True;context.state='FINALIZED_ALL_EIGHT';return rows,proof

def restore_result_order(original,ordinary,completed):
 need(set(completed)==set(contracts())and len(completed)==8,'complete eight finalized row set');out=[];iterator=iter(ordinary)
 for r in original:
  if type(r)is PendingOwner:out.append(completed[r.unit_id])
  else:need(next(iterator)is r,'all other ordinary row objects/order unchanged');out.append(r)
 need(next(iterator,None)is None,'no extra ordinary rows');return out
