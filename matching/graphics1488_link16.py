"""Closed source-link arithmetic for the exact genuine symbolic graphics1488.

This contribution-specific adapter leaves library16's runtime allowlist intact.
It accepts unchanged raw source-generated OMF and explicit linker placements,
never target bytes, native expected bytes, masks or replacement code. No storage
providers are fabricated. Placement inputs alone do not prove historical MAP.
"""
import hashlib
from omf import read_omf
from library16 import LibraryError,_word,_placement
OBJECT_SHA256='39f357944e24b233eb050b8b9dcaf5213bc5c4595119411ac56d98e3ff91d9c1'
SOURCE_SHA256='43f4ee388ef68067cca56d7f5cf76828a6350de02ca9cca3c28ea3767790b66c'
EXTERNALS={1: '_font_glyphs', 2: '_text_cursor', 3: '_graphics_end', 4: '_color_buffer', 5: '_text_glyph_pixels', 6: '_text_colour_words', 7: '_graphics_copy', 8: '_graphics_begin', 9: '_blit'}
FIELD_PROFILE=[(2, 268, 2, 1, True, (0, 2), (0, 2), 409, 'c50c0002029901', 1313), (2, 270, 2, 1, True, (0, 2), (0, 2), 453, 'c50e000202c501', 1313), (2, 272, 2, 1, True, (0, 2), (0, 2), 537, 'c5100002021902', 1313), (2, 274, 2, 1, True, (0, 2), (0, 2), 614, 'c5120002026602', 1313), (2, 276, 2, 1, True, (0, 2), (0, 2), 731, 'c514000202db02', 1313), (2, 278, 2, 1, True, (0, 2), (0, 2), 781, 'c5160002020d03', 1313), (2, 286, 2, 1, True, (1, 1), (2, 9), None, 'c51e160109', 1313), (2, 290, 2, 1, True, (1, 1), (2, 9), 2, 'c5221201090200', 1313), (2, 293, 2, 1, True, (1, 1), (2, 9), 4, 'c5251201090400', 1313), (2, 300, 2, 1, False, (0, 2), (0, 2), 868, '852c0002026403', 1313), (2, 304, 2, 1, True, (0, 2), (0, 2), None, 'c530040202', 1313), (2, 307, 2, 1, True, (1, 1), (2, 9), 6, 'c5331201090600', 1313), (2, 314, 2, 1, False, (0, 2), (0, 2), 868, '853a0002026403', 1313), (2, 318, 2, 1, True, (0, 2), (0, 2), 2, 'c53e0002020200', 1313), (2, 321, 2, 1, True, (1, 1), (2, 9), 8, 'c5411201090800', 1313), (2, 325, 2, 1, True, (0, 2), (0, 2), 4, 'c5450002020400', 1313), (2, 328, 2, 1, True, (1, 1), (2, 9), 10, 'c5481201090a00', 1313), (2, 332, 2, 1, True, (0, 2), (0, 2), 6, 'c54c0002020600', 1313), (2, 336, 2, 1, True, (1, 1), (2, 9), 16, 'c5501201091000', 1313), (2, 339, 2, 1, True, (1, 1), (2, 9), 12, 'c5531201090c00', 1313), (2, 343, 2, 1, True, (1, 1), (2, 9), 14, 'c5571201090e00', 1313), (2, 354, 2, 1, True, (0, 2), (0, 2), 8, 'c5620002020800', 1313), (2, 359, 2, 1, True, (0, 2), (0, 2), 10, 'c5670002020a00', 1313), (2, 363, 2, 1, True, (1, 1), (2, 9), 20, 'c56b1201091400', 1313), (2, 407, 2, 1, True, (0, 2), (0, 2), 268, 'c5970002020c01', 1313), (2, 412, 2, 1, True, (0, 2), (0, 2), None, 'c59c040202', 1313), (2, 418, 2, 1, True, (0, 2), (0, 2), 8, 'c5a20002020800', 1313), (2, 430, 2, 1, True, (0, 2), (0, 2), 10, 'c5ae0002020a00', 1313), (2, 436, 2, 1, True, (0, 2), (0, 2), 4, 'c5b40002020400', 1313), (2, 441, 2, 1, True, (0, 2), (0, 2), 6, 'c5b90002020600', 1313), (2, 446, 2, 1, True, (0, 2), (0, 2), 2, 'c5be0002020200', 1313), (2, 451, 2, 1, False, (0, 2), (0, 2), 868, '85c30002026403', 1313), (2, 456, 2, 1, True, (0, 2), (0, 2), None, 'c5c8040202', 1313), (2, 464, 2, 1, True, (0, 2), (0, 2), 8, 'c5d00002020800', 1313), (2, 495, 2, 1, True, (0, 2), (0, 2), 10, 'c5ef0002020a00', 1313), (2, 520, 2, 1, True, (0, 2), (0, 2), 4, 'c6080002020400', 1313), (2, 525, 2, 1, True, (0, 2), (0, 2), 6, 'c60d0002020600', 1313), (2, 530, 2, 1, True, (0, 2), (0, 2), 2, 'c6120002020200', 1313), (2, 535, 2, 1, False, (0, 2), (0, 2), 868, '86170002026403', 1313), (2, 538, 2, 1, True, (0, 2), (0, 2), 12, 'c61a0002020c00', 1313), (2, 543, 2, 1, True, (0, 2), (0, 2), None, 'c61f040202', 1313), (2, 549, 2, 1, True, (0, 2), (0, 2), 8, 'c6250002020800', 1313), (2, 576, 2, 1, True, (0, 2), (0, 2), 10, 'c6400002020a00', 1313), (2, 597, 2, 1, True, (0, 2), (0, 2), 4, 'c6550002020400', 1313), (2, 602, 2, 1, True, (0, 2), (0, 2), 6, 'c65a0002020600', 1313), (2, 607, 2, 1, True, (0, 2), (0, 2), 2, 'c65f0002020200', 1313), (2, 612, 2, 1, False, (0, 2), (0, 2), 868, '86640002026403', 1313), (2, 615, 2, 1, True, (0, 2), (0, 2), 12, 'c6670002020c00', 1313), (2, 620, 2, 1, True, (0, 2), (0, 2), None, 'c66c040202', 1313), (2, 628, 2, 1, True, (0, 2), (0, 2), 8, 'c6740002020800', 1313), (2, 674, 2, 1, True, (0, 2), (0, 2), 10, 'c6a20002020a00', 1313), (2, 714, 2, 1, True, (0, 2), (0, 2), 4, 'c6ca0002020400', 1313), (2, 719, 2, 1, True, (0, 2), (0, 2), 6, 'c6cf0002020600', 1313), (2, 724, 2, 1, True, (0, 2), (0, 2), 2, 'c6d40002020200', 1313), (2, 729, 2, 1, False, (0, 2), (0, 2), 868, '86d90002026403', 1313), (2, 734, 2, 1, True, (0, 2), (0, 2), None, 'c6de040202', 1313), (2, 740, 2, 1, True, (0, 2), (0, 2), 8, 'c6e40002020800', 1313), (2, 755, 2, 1, True, (0, 2), (0, 2), 10, 'c6f30002020a00', 1313), (2, 764, 2, 1, True, (0, 2), (0, 2), 4, 'c6fc0002020400', 1313), (2, 769, 2, 1, True, (0, 2), (0, 2), 6, 'c7010002020600', 1313), (2, 774, 2, 1, True, (0, 2), (0, 2), 2, 'c7060002020200', 1313), (2, 784, 2, 1, True, (0, 2), (0, 2), None, 'c710040202', 1313), (2, 792, 2, 1, True, (0, 2), (0, 2), 8, 'c7180002020800', 1313), (2, 826, 2, 1, True, (0, 2), (0, 2), 10, 'c73a0002020a00', 1313), (2, 854, 2, 1, True, (0, 2), (0, 2), 4, 'c7560002020400', 1313), (2, 859, 2, 1, True, (0, 2), (0, 2), 6, 'c75b0002020600', 1313), (2, 864, 2, 1, True, (0, 2), (0, 2), 2, 'c7600002020200', 1313), (2, 1135, 2, 2, True, (2, 4), (2, 4), None, 'c873260404', 2245), (2, 1140, 2, 1, True, (2, 4), (2, 4), None, 'c478260404', 2245), (2, 1183, 2, 1, True, (0, 2), (0, 2), 873, 'c4a30002026903', 2245), (2, 1204, 4, 3, True, (2, 8), (2, 8), None, 'ccb8260808', 2245), (2, 1223, 2, 1, True, (1, 1), (2, 2), None, 'c4cb160102', 2245), (2, 1229, 2, 1, True, (1, 1), (2, 2), 2, 'c4d11201020200', 2245), (2, 1247, 2, 1, True, (0, 1), (2, 6), None, 'c4e3060106', 2245), (2, 1355, 4, 3, True, (2, 3), (2, 3), None, 'cd4f260303', 2245), (2, 1372, 2, 1, True, (0, 1), (2, 1), None, 'c560060101', 2245), (2, 1377, 2, 1, True, (0, 1), (2, 5), None, 'c565060105', 2245), (2, 1380, 2, 1, True, (0, 1), (2, 6), None, 'c568060106', 2245), (2, 1447, 2, 1, True, (0, 1), (2, 5), None, 'c5ab060105', 2245), (2, 1460, 2, 1, True, (1, 1), (2, 2), 2, 'c5b81201020200', 2245), (2, 1463, 2, 1, True, (1, 1), (2, 2), None, 'c5bb160102', 2245), (2, 1470, 2, 1, True, (1, 1), (2, 2), None, 'c5c2160102', 2245), (2, 1473, 4, 3, True, (2, 7), (2, 7), None, 'cdc5260707', 2245), (2, 1486, 2, 1, False, (0, 2), (0, 2), 1346, '85d20002024205', 2245)]
PUBLICS={'_blit_e57a':280,'_prepare_pixels_e8cb':1129,'_draw_text_e915':1203}
FAR_NAMES={'_graphics_begin','_graphics_end','_graphics_copy'}
DS_NAMES=set(EXTERNALS.values())-FAR_NAMES-{'_color_buffer'}

def require(value,message):
 if not value:raise LibraryError(message)
def sha(b):return hashlib.sha256(b).hexdigest()

def validate_object(raw):
 require(isinstance(raw,bytes),'graphics1488 requires unchanged raw OMF bytes')
 o=read_omf(raw)
 require([(s.name,s.class_name,s.length,s.attributes,s.unsupported_data)for s in o.segments.values()]==[('_DATA','DATA',0,72,False),('_TEXT','CODE',1488,72,False)],'graphics1488 complete allocations changed')
 require(not o.segments[1].chunks and not o.procedures,'graphics1488 DATA/procedure allocation changed')
 require(o.externals==EXTERNALS and {n:p.offset for n,p in o.publics.items()}==PUBLICS,'graphics1488 PUBLIC/EXTDEF identity changed')
 require(all((p.segment,p.group,p.type_index)==(2,0,0)for p in o.publics.values()),'graphics1488 public frame/type changed')
 require([b for k,_,b in o.records if k==0x9a]==[b'\x02\xff\x01'],'graphics1488 DGROUP changed')
 require(not any(k in[0xb0,0xb2,0xa2]for k,_,_ in o.records),'graphics1488 COMMON/iterated data forbidden')
 shape=[(f.segment,f.offset,f.width,f.location_type,f.segment_relative,f.frame,f.target,f.displacement,f.raw.hex(),f.record_offset)for f in o.fixups]
 require(shape==FIELD_PROFILE,'graphics1488 exact84 raw field contract changed')
 result=bytearray()
 for offset,b in sorted(o.segments[2].chunks):require(b and offset==len(result),'graphics1488 CODE hole/overlap');result.extend(b)
 require(len(result)==o.segments[2].length,'graphics1488 CODE incomplete')
 require(sha(raw)==OBJECT_SHA256,'graphics1488 whole deterministic source object changed')
 return o,bytes(result)

def _field_encoding(o,f,raw,segment_placement,segments,groups,externals):
 """Restricted arithmetic kernel; diagnostic controls corroborate LINK semantics.

 Public link() always authenticates the complete closed object before using it.
 The kernel deliberately permits no arbitrary OMF frame methods or pointers.
 """
 paragraph,base=segment_placement
 def address(method,datum):
  if method==0 and datum in segments:return segments[datum]
  if method==1 and datum in groups:return groups[datum],0
  if method==2:
   n=o.externals.get(datum)
   require(n in externals,'missing explicit external placement');return externals[n]
  raise LibraryError('unsupported/unresolved frame or target')
 require(f.location_type in[1,2,3]and f.width==({1:2,2:2,3:4}[f.location_type]),'unsupported location/width')
 require(len(raw)==f.width,'incomplete raw fixup field')
 target_paragraph,target_offset=address(*f.target)
 frame_paragraph=target_paragraph if f.frame==(5,None)else address(*f.frame)[0]
 addend=int.from_bytes(raw,'little');disp=0 if f.displacement is None else _word(f.displacement)
 place=paragraph*16+base+f.offset;mz=None
 if f.location_type==2:
  require(f.segment_relative and f.target[0]==2 and f.frame==f.target and disp==0 and addend==0,'external BASE16 needs matching external frame/target and zero addend/displacement')
  value=target_paragraph;kind='external_BASE16';mz=place
 elif f.location_type==3:
  require(f.segment_relative and f.target[0]==2 and f.frame==f.target and disp==0 and addend==0,'external FAR16 needs matching external frame/target and zero addend/displacement')
  value=(target_paragraph<<16)|target_offset;kind='external_FAR16';mz=place+2
 elif f.segment_relative:
  value=target_paragraph*16+target_offset+disp-frame_paragraph*16+addend
  require(0<=value<=65535,'OFFSET16 target outside explicit frame')
  kind='ownCODE_OFFSET16'if f.target[0]==0 else'external_OFFSET16'
 else:
  require(f.target[0]==0 and f.frame==f.target and target_paragraph==paragraph,'selfrelative field requires same actual code frame')
  value=target_paragraph*16+target_offset+disp+addend-(place+2);kind='ownCODE_self_relative16'
 encoded=value&((1<<(f.width*8))-1)
 return encoded.to_bytes(f.width,'little'),{'segment':f.segment,'object_offset':f.offset,'image_offset':place,'width':f.width,'location_type':f.location_type,'segment_relative':f.segment_relative,'frame':list(f.frame),'target':list(f.target),'target_symbol':o.externals.get(f.target[1])if f.target[0]==2 else None,'target_paragraph':target_paragraph,'target_offset':target_offset,'frame_paragraph':frame_paragraph,'original_addend':addend,'displacement':disp,'arithmetic_result':value,'encoded_value':encoded,'encoded_hex':encoded.to_bytes(f.width,'little').hex(),'kind':kind,'raw_fixupp':f.raw.hex(),'record_offset':f.record_offset,'mz_relocation_image_offset':mz,'mz_segment_relocation_image_offset':mz}

def link(raw,segments,groups,externals):
 """Link every source-generated byte; no comparison/target input is accepted."""
 o,content=validate_object(raw)
 require(set(segments)=={1,2}and set(groups)=={1}and set(externals)==set(EXTERNALS.values()),'graphics1488 complete explicit binding sets required')
 segments={k:_placement(v)for k,v in segments.items()};groups={k:_word(v)for k,v in groups.items()};externals={k:_placement(v)for k,v in externals.items()}
 require(segments[1]==(groups[1],0),'graphics1488 empty DATA must use explicit DGROUP frame')
 require(all(externals[n][0]==groups[1]for n in DS_NAMES),'graphics1488 near DATA target must share declared DGROUP frame')
 require(segments[2][1]+len(content)<=65536,'graphics1488 CODE crosses frame boundary')
 result=bytearray(content);used=set();logs=[]
 for f in o.fixups:
  at=f.offset;require(f.segment==2 and at>=0 and at+f.width<=len(result),'graphics1488 field outside complete CODE')
  field=set(range(at,at+f.width));require(not(field&used),'graphics1488 overlapping fixups');used|=field
  encoded,log=_field_encoding(o,f,content[at:at+f.width],segments[2],segments,groups,externals)
  result[at:at+f.width]=encoded;logs.append(log)
 return bytes(result),logs
