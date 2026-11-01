"""Complete C5 initialized near-pointer DATA, with explicit DGROUP placements.

This is separate from relocation-free cdata.extract_data. It derives size only
from the whole SEGDEF and never consumes target bytes, sizes or matching units.
"""
from dataclasses import asdict
import hashlib
try:
    from .omf import OMFObject,OMFError,_Cursor
    from .library16 import link_segment
except ImportError:
    from omf import OMFObject,OMFError,_Cursor
    from library16 import link_segment

class CDataPointerError(OMFError):pass


def _word(n):
    if type(n)is not int or not 0<=n<=65535:
        raise CDataPointerError('pointer DATA placement must be an explicit16-bit integer')
    return n


def _whole(segment):
    data=bytearray();writes=[]
    if segment.unsupported_data:raise CDataPointerError('pointer DATA forbids LIDATA')
    for offset,content in sorted(segment.chunks):
        if not content or type(offset)is not int or offset!=len(data)or offset+len(content)>segment.length:
            raise CDataPointerError('pointer DATA/debug has a hole, overlap or invalid LEDATA')
        data.extend(content);writes.append({'offset':offset,'length':len(content),'sha256':hashlib.sha256(content).hexdigest()})
    if len(data)!=segment.length:raise CDataPointerError('pointer DATA/debug has an uninitialized SEGDEF tail')
    return bytes(data),writes


def _groups(obj):
    groups=[]
    for kind,_,payload in obj.records:
        if kind!=0x9a:continue
        c=_Cursor(payload);idx=c.index()
        if not 0<idx<len(obj.names):raise CDataPointerError('pointer DATA undefined group name')
        members=[]
        while c:
            if c.byte()!=0xff:raise CDataPointerError('pointer DATA requires SEGDEF group components')
            member=c.index()
            if member not in obj.segments or member in members:raise CDataPointerError('pointer DATA invalid/duplicate group member')
            members.append(member)
        groups.append({'index':len(groups)+1,'name':obj.names[idx],'segments':members})
    return groups


def _debug(obj,selected,used):
    """Accept only bounded C5 CV3 type streams and external DATA symbol records.

    Debug FAR16 fixups do not earn bytes or MZ sites. Their exact address fields
    must reference the same named externals used by the actual DATA; arbitrary
    fixes in a segment merely called DEBSYM/DEBTYP are not ignored.
    """
    debug={};expected={};type_count=0;symbol_records=[];type_records=[]
    for s in obj.segments.values():
        if s.index==selected or not s.length:continue
        if (s.name,s.class_name)not in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]or s.attributes!=0x20:
            raise CDataPointerError('pointer DATA forbids other initialized allocations')
        if s.name in debug:raise CDataPointerError('pointer DATA duplicate debug segment')
        data,writes=_whole(s);debug[s.name]={'segment':s.index,'length':s.length,'sha256':hashlib.sha256(data).hexdigest(),'data_writes':writes}
        if s.name=='$$TYPES':
            at=0
            while at<len(data):
                if at+4>len(data)or data[at]!=1:raise CDataPointerError('pointer DATA unknown/truncated CV3 type record')
                size=int.from_bytes(data[at+1:at+3],'little')
                if size<1 or at+3+size>len(data)or data[at+3]not in {0x80,0x79,0x7f,0x7a,0x78}:
                    raise CDataPointerError('pointer DATA unsupported CV3 type record')
                type_records.append({'segment':s.index,'offset':at,'length':size+3,'leaf':data[at+3],'type_index':0x200+type_count,'raw_hex':data[at:at+3+size].hex()})
                at+=3+size;type_count+=1
        else:
            at=0
            while at<len(data):
                size=data[at]+1
                if size<10 or at+size>len(data)or data[at+1]!=5 or data[at+8]+9!=size:
                    raise CDataPointerError('pointer DATA only supports complete CV3 external DATA symbol records')
                record=data[at:at+size]
                try:name='_'+record[9:].decode('ascii')
                except UnicodeDecodeError as ex:raise CDataPointerError('pointer DATA non-ASCII CV3 name')from ex
                if name not in used or record[2:6]!=bytes(4):raise CDataPointerError('pointer DATA debug address is not an actual near DATA external')
                key=(s.index,at+2)
                expected[key]=name;symbol_records.append({'segment':s.index,'offset':at,'length':size,'name':name,'type_index':int.from_bytes(record[6:8],'little'),'raw_hex':record.hex()})
                at+=size
    if symbol_records and not type_count:raise CDataPointerError('pointer DATA symbols require bounded CV3 types')
    if '$$SYMBOLS'in debug and (len(symbol_records)!=len(used)or {r['name']for r in symbol_records}!=used):
        raise CDataPointerError('pointer DATA debug stream must describe each external DATA symbol once')
    for record in symbol_records:
        t=record['type_index']
        if t>=0x200 and not t<0x200+type_count:raise CDataPointerError('pointer DATA undefined CV3 type index')
    for p in obj.publics.values():
        if type_count and p.type_index>=0x200 and not p.type_index<0x200+type_count:
            raise CDataPointerError('pointer DATA public has undefined CV3 type index')
    seen=set()
    for f in obj.fixups:
        if f.segment==selected:continue
        key=(f.segment,f.offset)
        if (key not in expected or key in seen or f.width!=4 or f.location_type!=3
                or f.segment_relative is not True or f.frame!=(5,None)or f.target[0]!=2
                or obj.externals.get(f.target[1])!=expected[key]or(f.displacement or 0)!=0):
            raise CDataPointerError('pointer DATA invalid/unowned CV3 debug address fixup')
        seen.add(key)
    if seen!=set(expected):raise CDataPointerError('pointer DATA debug address fixup is missing')
    return {'segments':debug,'external_symbol_records':symbol_records,'type_records':type_records,'validated_debug_fixups':len(seen),'fixups':[asdict(f)|{'raw':f.raw.hex()}for f in obj.fixups if f.segment!=selected]}


def link_pointer_data(obj,symbol,origin,dgroup_segment,externals):
    """Return complete initialized bytes and metadata, using named DS offsets.

    origin is a linear unrelocated image address; dgroup_segment is the explicit
    image-relative DGROUP paragraph. The caller must independently authenticate
    that frame. Bindings are name->unsigned16 DS offsets, never guessed addresses.
    Only complete PUBLIC WORD _DATA plus empty standard C5 CODE/CONST/BSS and
    narrowly parsed CV3 metadata is allowed. Near pointers never emit MZ sites.
    """
    if not isinstance(obj,OMFObject):raise CDataPointerError('pointer DATA requires strict-reader OMF object')
    if (any(type(k)is not int or k<=0 or k!=s.index for k,s in obj.segments.items())
            or len({(s.name,s.class_name)for s in obj.segments.values()})!=len(obj.segments)
            or any(k!=p.name for k,p in obj.publics.items())):
        raise CDataPointerError('pointer DATA inconsistent segment/public identities')
    dgroup_segment=_word(dgroup_segment)
    if type(origin)is not int or origin<0:raise CDataPointerError('pointer DATA origin must be a nonnegative image address')
    base=origin-16*dgroup_segment
    if not 0<=base<=65535:raise CDataPointerError('pointer DATA origin is outside the explicit DGROUP frame')
    allowed={0x80,0x88,0x96,0x98,0x9a,0x9c,0x8c,0x90,0xa0,0x8a}
    for kind,_,payload in obj.records:
        if kind not in allowed:raise CDataPointerError('pointer DATA unsupported record/allocation kind')
        if kind==0x88 and payload not in [bytes.fromhex(s)for s in ['009d30734f','00a1014356','00a201']]:
            raise CDataPointerError('pointer DATA unsupported compiler/debug COMENT')
        if kind==0x8a and payload!=b'\0':raise CDataPointerError('pointer DATA MODEND must have no entry point')
    p=obj.publics.get(symbol)
    if p is None or p.offset!=0 or p.segment not in obj.segments:
        raise CDataPointerError('pointer DATA requires selected public at segment offset zero')
    seg=obj.segments[p.segment]
    if (seg.name!='_DATA'or seg.class_name!='DATA'or seg.attributes!=0x48
            or type(seg.length)is not int or not 0<seg.length<=65535 or base+seg.length>65536 or base%2):
        raise CDataPointerError('pointer DATA requires whole aligned16-bit PUBLIC WORD _DATA')
    empty={('_TEXT','CODE'),('CONST','CONST'),('_BSS','BSS')};normal={seg.index}
    for s in obj.segments.values():
        if s.index==seg.index:continue
        if not s.length:
            if (s.name,s.class_name)not in empty or s.attributes!=0x48 or s.chunks or s.unsupported_data:
                raise CDataPointerError('pointer DATA unsupported empty segment')
            if s.class_name!='CODE':normal.add(s.index)
        elif(s.name,s.class_name)not in [('$$SYMBOLS','DEBSYM'),('$$TYPES','DEBTYP')]:
            raise CDataPointerError('pointer DATA forbids another allocation')
    groups=_groups(obj)
    if (len(groups)!=1 or groups[0]['name']!='DGROUP'or set(groups[0]['segments'])!=normal
            or p.group!=groups[0]['index']):raise CDataPointerError('pointer DATA needs exactly one complete matching DGROUP')
    if any(q.segment!=seg.index or q.group!=p.group or type(q.offset)is not int or not 0<=q.offset<seg.length for q in obj.publics.values()):
        raise CDataPointerError('all pointer DATA publics must belong to complete selected DATA/DGROUP')
    names=list(obj.externals.values())
    if len(set(names))!=len(names):raise CDataPointerError('pointer DATA duplicate EXTDEF names')
    data,writes=_whole(seg);fixups=[f for f in obj.fixups if f.segment==seg.index];used=set();fields=set()
    if not fixups:raise CDataPointerError('pointer DATA requires actual near-pointer fixups')
    for f in fixups:
        if (f.width!=2 or f.location_type!=1 or f.segment_relative is not True
                or f.frame not in [(5,None),(1,p.group)]or f.target[0]!=2
                or type(f.offset)is not int or not 0<=f.offset<=len(data)-2
                or type(f.target[1])is not int or f.target[1]not in obj.externals
                or(f.displacement is not None and(type(f.displacement)is not int or not 0<=f.displacement<=65535))):
            raise CDataPointerError('pointer DATA requires explicit external OFFSET16 fields in DGROUP')
        if {f.offset,f.offset+1}&fields:raise CDataPointerError('pointer DATA duplicate/overlapping fixup')
        fields.update([f.offset,f.offset+1]);used.add(obj.externals[f.target[1]])
    if '__acrtused'in used or set(names)-used not in [set(),{'__acrtused'}]:
        raise CDataPointerError('pointer DATA unreferenced external other than unused startup marker')
    if not isinstance(externals,dict)or set(externals)!=used:
        raise CDataPointerError('pointer DATA needs exact named DS bindings without missing/extra entries')
    bindings={n:_word(v)for n,v in externals.items()}
    for f in fixups:
        value=bindings[obj.externals[f.target[1]]]+int.from_bytes(data[f.offset:f.offset+2],'little')+(f.displacement or 0)
        if not 0<=value<=65535:raise CDataPointerError('pointer DATA relocated near address overflows16 bits')
    debug=_debug(obj,seg.index,used)
    linked,logs=link_segment(obj,seg.index,{seg.index:(dgroup_segment,base)},{p.group:dgroup_segment},
                             {n:(dgroup_segment,v)for n,v in bindings.items()})
    return linked,{'boundary':'complete_omf_pointer_data_segment','symbol':symbol,'segment':{k:v for k,v in asdict(seg).items()if k!='chunks'},
                   'public':asdict(p),'publics':{n:asdict(q)for n,q in obj.publics.items()},'group':groups[0],
                   'origin':origin,'dgroup_segment':dgroup_segment,'dgroup_offset':base,
                   'data_writes':writes,'unlinked_sha256':hashlib.sha256(data).hexdigest(),
                   'sha256':hashlib.sha256(linked).hexdigest(),'relocations':logs,'debug':debug,
                   'externals':bindings,'startup_marker_unused':'__acrtused'in names,
                   'emitted_mz_sites':[],'authored_c_function_count':0}
