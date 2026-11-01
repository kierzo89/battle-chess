"""Closed genuine five-procedure pen CODE560/selector CONST2 ownership."""
from pathlib import Path
from dataclasses import asdict
import json,hashlib
from omf import OMFError,OMFObject,_Cursor
from reference import validate_data_address,validate_expanded_read
KIND='pen_far_array_selector_560_v1'
KEYS={'kind','segment','group','size','image_offset','data_address','rea_evidence','code_evidence','target_symbol'}
PROCEDURES={'_select_pen_5b18':(0,37),'_move_pen_5b3d':(37,24),'_line_pen_5b55':(61,310),'_sign_5c8b':(371,42),'_copy_5cb5':(413,147)}
OWNERS={'_select_pen_5b18'}
EXTERNALS={'__chkstk':0xecaa,'_packed_pen':0x8172,'_graphics_copy':{'segment':0x110d,'offset':0},'_pen_x':0x8d26,'_pen_y':0x8d2a,'_plot_pixel':0x4a6,'_abs_i16':0x8fb5,'_sign_5c8b':0x5c8b,'_screen':0x5ce,'__AHSHIFT':{'absolute':12},'__AHINCR':{'absolute':0x1000}}
class PenSelectorError(OMFError):pass
def require(v,message):
 if not v:raise PenSelectorError(message)
def full_bytes(s):
 result=bytearray();require(not s.unsupported_data,'Pen selector reserved/iterated data')
 for offset,body in sorted(s.chunks):require(body and offset==len(result),'Pen selector hole/overlap');result.extend(body)
 require(len(result)==s.length,'Pen selector uninitialized tail');return bytes(result)
def validate_unit_metadata(unit):
 d=unit.get('owned_selector_const');require(isinstance(d,dict)and set(d)==KEYS and d.get('kind')==KIND,'Pen selector exact descriptor')
 require(unit.get('language')=='c'and unit.get('backend')=='msc500-omf'and unit.get('symbol')=='_select_pen_5b18'and unit.get('size')==37 and unit.get('image_offset')=='0x5b18'and unit.get('flags')==['/AS','/Zi'],'Pen selector exact owner/extent/profile')
 require(not any(unit.get(k)is not None for k in ['owned_const','owned_data','owned_bss','code_address','extended_extent']),'Pen selector exclusive ownership')
def validate_layout(obj,d,externals):
 require(isinstance(obj,OMFObject)and isinstance(d,dict)and set(d)==KEYS and d.get('kind')==KIND,'Pen selector exact layout profile')
 require(d['target_symbol']=='_graphics_copy'and all(type(d[k])is int for k in ['segment','group','size'])and(d['segment'],d['group'],d['size'])==(3,1,2),'Pen selector indexes/target/size')
 require(d['image_offset']=='0x619b4'and d['data_address']=={'segment':0x5cc2,'offset':0x4d94}and all(type(x)is int for x in d['data_address'].values()),'Pen selector native placement')
 require(all(isinstance(d[k],str)and d[k]for k in ['rea_evidence','code_evidence']),'Pen selector primary paths')
 require(json.dumps(externals,sort_keys=True)==json.dumps(EXTERNALS,sort_keys=True),'Pen selector exact native binding map')
 require(set(obj.segments)=={1,2,3,4,5,6},'Pen selector foreign/missing SEGDEF')
 expected=[(1,'_TEXT','CODE',560,0x48),(2,'_DATA','DATA',0,0x48),(3,'CONST','CONST',2,0x48),(4,'_BSS','BSS',0,0x48)]
 require([(i,obj.segments[i].name,obj.segments[i].class_name,obj.segments[i].length,obj.segments[i].attributes)for i in range(1,5)]==expected,'Pen selector wholeCODE560/CONST2 identity')
 require([(obj.segments[i].name,obj.segments[i].class_name)for i in [5,6]]==[('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')],'Pen selector debug identities')
 for index in [1,2,3,4]:full_bytes(obj.segments[index])
 require(not any(s.unsupported_data for s in obj.segments.values()),'Pen selector unsupported segment data')
 require(set(obj.publics)==set(PROCEDURES)and set(obj.procedures)==set(PROCEDURES),'Pen selector all five actual PUBLIC/CVs required')
 for name,(offset,size)in PROCEDURES.items():
  p=obj.publics[name];i=obj.function_info(name);require(p.segment==1 and p.group==0 and p.offset==offset and(i['segment'],i['offset'],i['size'],i['boundary'])==(1,offset,size,'codeview3_procedure'),'Pen selector complete independent CV/public changed')
 groups=[]
 for kind,_,payload in obj.records:
  require(kind in {0x80,0x88,0x8a,0x8c,0x90,0x94,0x96,0x98,0x9a,0x9c,0xa0},'Pen selector unknown or hidden loaded OMF record')
  require(kind not in [0xa2,0xa3,0xb0,0xb8],'Pen selector LIDATA/COMMON forbidden')
  if kind!=0x9a:continue
  c=_Cursor(payload);index=c.index();require(0<index<len(obj.names),'Pen selector groupname');members=[]
  while c:require(c.byte()==0xff,'Pen selector groupcomponent');members.append(c.index())
  groups.append((obj.names[index],members))
 require(groups==[('DGROUP',[3,4,2])],'Pen selector real DGROUP')
 path=Path(__file__).with_name('pen_selector_profile.json');raw_profile=path.read_bytes();require(hashlib.sha256(raw_profile).hexdigest()=='c78414cbd3c7fc82d34c3a21f75f545eb351f2b4346f1684ece4c171c186e5e6','Pen selector fixed structuralprofile changed');profile=json.loads(raw_profile)
 actual=[]
 for f in obj.fixups:
  row=asdict(f);row['raw']=f.raw.hex();row['external']=obj.externals.get(f.target[1])if f.target[0]==2 else None;actual.append(row)
 require(json.dumps(actual,sort_keys=True)==json.dumps(profile['all_raw_fields'],sort_keys=True),'Pen selector all65 actual raw FIXUPP fields changed')
 require(len(actual)==65 and sum(f.segment==1 for f in obj.fixups)==43 and sum(f.segment==3 for f in obj.fixups)==1,'Pen selector CODE43/CONST1/debug21 accounting')
 for n,info in profile['debug_segments'].items():
  segment=obj.segments[int(n)];data=b''.join(body for offset,body in segment.chunks);chunks=[{'offset':offset,'length':len(body),'sha256':hashlib.sha256(body).hexdigest()}for offset,body in segment.chunks];require(segment.length==info['size']and chunks==info['chunks']and hashlib.sha256(data).hexdigest()==info['sha256'],'Pen selector complete raw CV/debug patch stream changed')
 require(full_bytes(obj.segments[3])==b'\0\0','Pen selector BASE16 zeroaddend')
 refs=[f for f in obj.fixups if f.target==(0,3)];require(len(refs)==1,'Pen selector sole actual CODE owner reference')
 f=refs[0];require((f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.displacement)==(1,10,2,1,True,(1,1),None)and full_bytes(obj.segments[1])[10:12]==b'\0\0','Pen selector owner field shape')
 return 0x4d94
def validate(unit,obj,project,reference,*,function_linker=None):
 validate_unit_metadata(unit);d=unit['owned_selector_const'];externals=unit.get('externals',{});validate_layout(obj,d,externals);project=Path(project).resolve()
 def primary(key):
  require(not Path(d[key]).is_absolute(),'Pen selector relative primary required');p=(project/d[key]).resolve();require(p.is_relative_to(project),'Pen selector primary escape');raw=p.read_bytes();return json.loads(raw),hashlib.sha256(raw).hexdigest()
 validate_data_address(dict(d,reference_region='exepack-expanded'),reference);selector=(0x110d).to_bytes(2,'little');se,sh=primary('rea_evidence');sid=validate_expanded_read(se,dict(d,reference_region='exepack-expanded'),selector,reference,emitted_mz_sites=[0x619b4])
 if function_linker is None:
  from link16 import link_function
  function_linker=link_function
 code=bytearray();fields=[]
 for name,(offset,size)in PROCEDURES.items():
  body,records=function_linker(obj,name,0x5b18+offset,externals,**({'owned_selector_const':d}if name in OWNERS else{}));require(len(body)==size and len(code)==offset,'Pen selector wholeCODE560 partition');code.extend(body);fields.extend(records)
 sites=[r['mz_segment_relocation_image_offset']for r in fields if'mz_segment_relocation_image_offset'in r];require(sites==[],'Pen selector unexpected CODE MZ')
 ce,ch=primary('code_evidence');cid=validate_expanded_read(ce,dict(image_offset='0x5b18',size=560,reference_region='exepack-expanded'),bytes(code),reference,emitted_mz_sites=sites)
 proof=dict(classification='complete_compiler_owned_far_array_selector_CONST_uncredited_context',authored_c_function_credit=0,source_data_credit=0,size=2,selector_bytes_hex=selector.hex(),complete_MZ_sites=[0x619b4],complete_CODE_bytes=560,complete_CODE_fields=fields,CODE_MZ_sites=sites,selector_primary_id=sid,selector_primary_sha256=sh,code_primary_id=cid,code_primary_sha256=ch,raw_CONST_fixup=asdict(next(f for f in obj.fixups if f.segment==3)),original_global_MAP_proved=False,omf_records_or_fields_modified=False)
 proof['raw_CONST_fixup']['raw']=proof['raw_CONST_fixup']['raw'].hex();return d,selector,proof
