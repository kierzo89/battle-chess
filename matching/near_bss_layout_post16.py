"""Exact same-run physical RAM comparison; no generator/fixture capability."""
from pathlib import Path
import re,struct
from omf import read_omf,_Cursor
import near_bss_layout16 as bss

def parse_map(data):
 pub={};segments=[];text=data.decode('cp437')
 for line in text.splitlines():
  m=re.fullmatch(r'\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+(\S+)\s*',line)
  if m:
   value=(int(m[1],16),int(m[2],16));assert m[3]not in pub or pub[m[3]]==value;pub[m[3]]=value
  m=re.fullmatch(r'\s*([0-9A-Fa-f]+)H\s+([0-9A-Fa-f]+)H\s+([0-9A-Fa-f]+)H\s+(\S+)\s+(\S+)\s*',line)
  if m:segments.append({'start':int(m[1],16),'stop':int(m[2],16),'length':int(m[3],16),'name':m[4],'class':m[5]})
 group=re.findall(r'^\s*([0-9A-Fa-f]{4}):0\s+DGROUP\s*$',text,re.M);assert len(group)==1
 return pub,segments,int(group[0],16)
def number(c):
 k=c.byte()
 if k<=0x80:return k
 assert k in (0x81,0x84,0x88)
 return int.from_bytes(c.take({0x81:2,0x84:3,0x88:4}[k]),'little')
def validate_client_frame(row,raw,f,symbol):
 if bss.H(raw)=='8ffb303e79a7c818b2efa5ee616c5c6d8a3708c4c9868da610519dfa1c640ea6':
  from mixed_remove460_bss16 import validate_client_frame as remove460_frame
  return remove460_frame(row,raw,f,symbol)
 if bss.H(raw)=='a8120c71456edd84cc7f8d566cf51a67a32f759978fe360d762e2c57365c4b65':
  from mixed_evaluation_bss16 import validate_client_frame as evaluator_frame
  return evaluator_frame(row,raw,f,symbol)
 if bss.H(raw)=='a0b4c1b81025aa26ea23bb5575fcad19b1e659d67d039f00e1d385a571f6dbff':
  from mixed_graphics_bss16 import validate_client_frame as graphics_frame
  return graphics_frame(row,raw,f,symbol)
 if f.frame in ((5,None),(1,1)):return 'default_or_explicit_DGROUP'
 if bss.H(raw) in ('db232231fe3e9ba1ce80e672cc19b4841d0f0818f49fab820aaf5013559c2648', 'f7ac7b7bd97f4aa326cf13053ad06339176b04761ff6a1d40ef583b9279deb29'):
  from mixed_visual_bss16 import validate_client_frame as visual_frame
  return visual_frame(row,raw,f,symbol)
 if bss.H(raw) in ('04fc9a5d5ed9624011c21ca811bb0fe7f4c29fb69061ad6606fe7018f51942e1', '909220367ff0a3197db9192a40e5ce78933cb0d95ec2843f5c9bd0dce9854ecc'):
  from mixed_overlap_bss16 import validate_client_frame as overlap_frame
  return overlap_frame(row,raw,f,symbol)
 if bss.H(raw)=='6f8a60b9a234f7597f2c2778ad0ea319a534c31235b4d9343a564c9182c9770c':
  assert row['kind']=='mixed-c-fa-authored-asm-whole-omf'and row['source']=='src/task_tail_handlers_match.c'and row['selected_owners']==['transfer_task_758c','capture_task_75f6','task_ready_772d','undo_animation_code327']
  allowed={29: ('_frame_index', 2, None, 'c41d260202'), 40: ('_frames', 8, None, 'c428260808'), 156: ('_animation_counter', 5, None, 'c49c260505'), 291: ('_frames', 8, None, 'c523260808')}
  assert f.offset in allowed and(symbol,f.target[1],f.displacement,f.raw.hex())==allowed[f.offset]
  assert f.frame==(2,f.target[1])and f.target[0]==2 and f.segment==1 and f.width==2 and f.location_type==1 and f.segment_relative
  return 'proven_MIXED874_external_PUBLIC_group1'
 if bss.H(raw)=='ec8dfc5b8e580856693bcc66ed13ddde05fd06ab5a70ecf51ed4936cd8abce8f':
  assert row['kind']=='mixed-c-fa-authored-asm-whole-omf'and row['source']=='src/motion_effect_tasks_match.c'and row['selected_owners']==['move_task_68ea','effect_task_6ab1','special_task_code187']
  allowed={138: ('_frames', 3, None, 'c48a260303'), 156: ('_frames', 3, None, 'c49c260303'), 170: ('_screen_x', 8, None, 'c4aa260808'), 175: ('_motion_x', 11, None, 'c4af260b0b'), 190: ('_screen_y', 9, None, 'c4be260909'), 195: ('_motion_y', 12, None, 'c4c3260c0c'), 209: ('_motion_y', 12, None, 'c4d1260c0c'), 213: ('_motion_x', 11, None, 'c4d5260b0b'), 246: ('_screen_x', 8, None, 'c4f6260808'), 266: ('_screen_y', 9, None, 'c50a260909'), 359: ('_screen_y', 9, None, 'c567260909'), 370: ('_screen_x', 8, None, 'c572260808'), 383: ('_screen_y', 9, None, 'c57f260909'), 394: ('_screen_x', 8, None, 'c58a260808'), 416: ('_motion_y', 12, None, 'c5a0260c0c'), 420: ('_motion_x', 11, None, 'c5a4260b0b'), 589: ('_frames', 3, None, 'c64d260303'), 709: ('_motion_y', 12, None, 'c6c5260c0c'), 713: ('_motion_x', 11, None, 'c6c9260b0b'), 903: ('_motion_y', 12, None, 'c787260c0c'), 907: ('_motion_x', 11, None, 'c78b260b0b')}
  assert f.offset in allowed and(symbol,f.target[1],f.displacement,f.raw.hex())==allowed[f.offset]
  assert f.frame==(2,f.target[1])and f.target[0]==2 and f.segment==1 and f.width==2 and f.location_type==1 and f.segment_relative
  return 'proven_MIXED970_external_PUBLIC_group1'
 if bss.H(raw)=='3b7173bc90908bc424cd47d3bb680bd5303833af65d7567f2bfbab8848e8b0f5':
  assert row['kind']=='mixed-c-fa-authored-asm-whole-omf'and row['source']=='src/restore_active_arena_match.c'and row['selected_owners']==['restore_active_arena_2ce0','decode_frame_directory_code289']
  allowed={1: ('_active_data_b0ca', 11, None, 'c401260b0b'), 4: ('_frame_data_cursor', 3, None, 'c404260303'), 7: ('_active_lists_b080', 17, None, 'c407261111'), 10: ('_frame_list_cursor', 4, None, 'c40a260404'), 13: ('_active_95fe', 16, None, 'c40d261010'), 19: ('_active_8e22', 14, None, 'c413260e0e'), 25: ('_active_a834', 13, None, 'c419260d0d'), 31: ('_active_964e', 15, None, 'c41f260f0f'), 37: ('_active_arena_9344', 12, None, 'c425260c0c'), 41: ('_active_arena_9344', 12, 2, 'c429220c0c0200'), 44: ('_arena_cursor', 7, None, 'c42c260707'), 48: ('_arena_cursor', 7, 2, 'c4302207070200'), 60: ('_arena_cursor', 7, None, 'c43c260707'), 64: ('_arena_cursor', 7, 2, 'c4402207070200'), 324: ('_arena_cursor', 7, None, 'c544260707'), 328: ('_arena_cursor', 7, 2, 'c5482207070200')}
  assert f.offset in allowed and(symbol,f.target[1],f.displacement,f.raw.hex())==allowed[f.offset]
  assert f.frame==(2,f.target[1])and f.target[0]==2 and f.segment==1 and f.width==2 and f.location_type==1 and f.segment_relative
  return 'proven_MIXED340_external_PUBLIC_group1'
 assert f.frame==(2,f.target[1])and f.target[0]==2 and row['kind']=='mixed-c-fa-authored-asm-whole-omf','Unproved/wrong raw client frame; no normalization'
 assert bss.H(raw)=='1585a54ced233f1f841f93afc4761614731246997e2a73290254ca867920f963','Only the genuine closed MIXED284 profile has this F2 contract'
 assert (f.offset,symbol)in [(85,'_ready_9856'),(94,'_ready_9856'),(98,'_ready_9856'),(142,'_menu_state')]
 assert f.width==2 and f.location_type==1 and f.segment_relative and f.displacement is None
 return 'proven_MIXED284_external_PUBLIC_group1'
def complete(aggregate):
 from closed_aggregate import ClosedAggregateSealV1
 bss.validate_evidence()
 assert type(aggregate)is ClosedAggregateSealV1;aggregate.valid();rows=aggregate.object_rows;raws=aggregate.source_raws();assert len(rows)==len(raws)
 selected=[(r,raw)for r,raw in zip(rows,raws)if r['kind']==bss.KIND];assert len(selected)==1;bss.inspect(selected[0][1]);spec=bss.spec();names={r['symbol']for r in spec['PUBLICs']}
 pub,segs,ds=parse_map(aggregate.read_artifact('PARTIAL.MAP'));linear=lambda x:x[0]*16+x[1]
 def one(name):
  v=[s for s in segs if s['name']==name];assert len(v)==1;return v[0]
 early,late=one('_BSS'),one('BC_NATIVE_LATE');assert early['class']==late['class']=='BSS'and early['length']==30 and late['length']==30960 and late['start']%16==0
 for name in ['XOB','XO','XOE']:assert one(name)['length']==0
 assert one('c_common')['length']==0
 views=[]
 for v in spec['PUBLICs']:
  start,base=(spec['early_bank'][0],early['start']+4)if v['native_DS']<spec['early_bank'][1]else(spec['late_bank'][0],late['start'])
  assert pub[v['symbol']][0]==ds and linear(pub[v['symbol']])==base+v['native_DS']-start
  views.append({'symbol':v['symbol'],'native_DS':v['native_DS'],'actual_MAP':pub[v['symbol']],'role':v['role'],'logical_view_size':v['logical_view_size'],'historical_C_identity_capacity_proven':False})
 assert len(views)==190 and len({linear(pub[n])for n in names})==186
 exe=aggregate.read_artifact('PARTIAL.EXE');h=struct.unpack_from('<14H',exe);assert h[0]==0x5a4d;end=(h[2]-1)*512+(h[1]or 512);assert end==len(exe);image=exe[h[4]*16:end]
 mz=[s*16+o for o,s in [struct.unpack_from('<HH',exe,h[12]+4*i)for i in range(h[3])]];assert len(mz)==len(set(mz))and len(image)<=early['start']and all(x+2<=len(image)for x in mz)
 stack=one('STACK');minimum=((len(image)+15)//16)*16+h[5]*16;assert stack['start']==late['start']+late['length']and stack['length']==4096 and stack['start']+stack['length']<=minimum and h[7]*16+h[8]==stack['start']+stack['length']
 assert linear(pub['_edata'])==early['start']and linear(pub['_end'])==late['start']+late['length']
 commons=[];private=[];fields=[];provider_publics=[]
 for row,raw in zip(rows,raws):
  o=read_omf(raw)
  for n,p in o.publics.items():
   if n in names:provider_publics.append((n,row['kind']))
  if row['kind']==bss.KIND:continue
  for s in o.segments.values():
   if s.class_name=='BSS'and s.length:assert not s.chunks;private.append({'object':row['DOS_name'],'segment':s.name,'length':s.length})
  for kind,at,payload in o.records:
   if kind==0xb0:
    c=_Cursor(payload)
    while c:
     name=c.name();typ=c.index();storage=c.byte();count=number(c);element=number(c)if storage==0x61 else 1;assert storage in (0x61,0x62);commons.append({'symbol':name,'type':typ,'storage':storage,'bytes':count*element})
  for f in o.fixups:
   if f.target[0]!=2 or o.externals[f.target[1]]not in names:continue
   n=o.externals[f.target[1]];seg=o.segments[f.segment];blocks=[]
   for k,at,payload in o.records:
    if k==0xa0 and at<f.record_offset:
     c=_Cursor(payload);si=c.index();off=c.word();blocks.append((at,si,off,payload[c.pos:]))
   at,si,off,data=blocks[-1];assert si==f.segment and off<=f.offset and f.offset+f.width<=off+len(data)
   add=data[f.offset-off:f.offset-off+f.width];expected=(pub[n][1]+int.from_bytes(add[:2],'little')+(f.displacement or 0))&65535
   v={'object':row['DOS_name'],'source':row['source'],'segment':seg.name,'class':seg.class_name,'offset':f.offset,'target':n,'frame':f.frame,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'displacement':f.displacement,'raw_field_hex':add.hex(),'owning_LEDATABlock':{'record_offset':at,'offset':off,'size':len(data),'sha256':bss.H(data)}}
   assert f.segment_relative and pub[n][0]==ds
   if seg.class_name in ('CODE','DATA'):
    assert f.width==2 and f.location_type==1
    v['frame_contract']=validate_client_frame(row,raw,f,n)
    bases={linear(pub[n])-p.offset for n,p in o.publics.items()if p.segment==f.segment};assert len(bases)==1
    address=next(iter(bases))+f.offset;actual=int.from_bytes(image[address:address+2],'little');assert actual==expected and not any(x<address+2 and x+2>address for x in mz)
    v.update(status='PASS_REAL_FILE_WORD',actual_FILE_observed=True,actual_image_offset=address,actual_WORD=actual,expected_DGROUP_WORD=expected)
   else:
    assert seg.class_name=='DEBSYM'and f.width==4 and f.location_type==3 and f.frame==(5,None)
    v.update(status='RAW_DEBUG_ONLY_NOT_FILE_OBSERVED',actual_FILE_observed=False,expected_group1_far_words=[expected,(ds+int.from_bytes(add[2:],'little'))&65535])
   fields.append(v)
 near=[c for c in commons if c['storage']==0x62];far=[c for c in commons if c['storage']==0x61]
 assert len(near)==142 and len({c['symbol']for c in near})==142 and sum(c['bytes']for c in near)==4978 and {c['symbol']for c in near}=={v['symbol']for v in spec['PUBLICs']if v['role']=='existing_typed_COMMON_view'}
 assert len(far)==2 and sum(c['bytes']for c in far)==220000 and sum(x['length']for x in private)==4
 assert len(provider_publics)==190 and all(k==bss.KIND for n,k in provider_publics)
 assert fields and any(v['class']=='CODE'for v in fields)
 aggregate.valid()
 return {'status':'PASS_FRESH_SAME_AGGREGATE_BSS190_ALL_CLIENT_FIELDS','SOURCE_count':len(rows),'run_id':aggregate.run_id,'SOURCE_digest':aggregate.SOURCE_digest,'LINK_result_sha256':aggregate.link_result_sha256,'all190_views':views,'physical_positions':186,'all_client_fields':fields,'CODE_FILE_fields':sum(v['class']=='CODE'for v in fields),'DATA_FILE_fields':sum(v['class']=='DATA'for v in fields),'DEBUG_raw_only_fields':sum(v['class']=='DEBSYM'for v in fields),'142_COMMON_logical_bytes':4978,'duplicated_COMMON_storage':False,'private_C_BSS4':private,'physical_uninitialized_bytes':30986,'BSS_FILE_bytes':0,'actual_early_BSS':early,'actual_late_BSS':late,'actual_alignment':late['start']-early['start']-early['length'],'native_absolute_placement_proven':False,'actual_MZ_header':list(h),'actual_partial_MZ_count':len(mz),'initialized_FILE_C_function_native_MZ_credit':0,'historical_C_identity_capacity_TU_claim':False}
