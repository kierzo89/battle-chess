"""Strict extraction of complete standalone C DATA contributions.

Accepts strict-reader OMF objects, never reference bytes, expected sizes or
placements. This does not relax function extraction or establish matching
credit. The only external admitted is the unused C5 startup-selection marker.
"""
import hashlib
from dataclasses import asdict

try:
    from .omf import OMFError, OMFObject, _Cursor
except ImportError:
    from omf import OMFError, OMFObject, _Cursor


class CDataError(OMFError):
    pass


def extract_data(obj, symbol):
    """Return (bytes, metadata) for one wholly initialized _DATA/DGROUP extent.

    Size comes from the complete independent SEGDEF, never an expected unit
    size, the next public, or a reference. Public offset must be zero. Other
    nondebug allocations, all fixups, communal definitions, LIDATA, holes and
    overlaps are rejected. One unused __acrtused EXTDEF may remain, reflecting
    compiler startup selection rather than an address used by these bytes.
    """
    if not isinstance(obj, OMFObject):
        raise CDataError('C DATA extraction requires a strict-reader OMF object')
    if any(kind in (0xb0, 0xb8) for kind, _, _ in obj.records):
        raise CDataError('C DATA communal allocations are forbidden')
    if obj.fixups:
        raise CDataError('C DATA contribution requires no FIXUPP fields')
    externals = list(obj.externals.values())
    if externals not in ([], ['__acrtused']):
        raise CDataError('C DATA admits only one unused __acrtused external marker')
    public = obj.publics.get(symbol)
    if public is None or public.offset != 0 or public.segment not in obj.segments:
        raise CDataError('C DATA requires a defined public at segment offset zero')
    segment = obj.segments[public.segment]
    if segment.name != '_DATA' or segment.class_name != 'DATA':
        raise CDataError('C DATA public must identify _DATA class DATA')
    attributes = segment.attributes
    if (attributes & 3 or attributes >> 5 not in (1, 2, 3, 4, 5)
            or (attributes >> 2) & 7 not in (2, 4, 7)
            or not 0 < segment.length <= 65535):
        raise CDataError('C DATA requires a relocatable 16-bit PUBLIC segment')
    for other in obj.segments.values():
        if other.index == segment.index:
            continue
        debug = ((other.name, other.class_name) in
                 (('$$SYMBOLS', 'DEBSYM'), ('$$TYPES', 'DEBTYP')))
        if other.length and not debug:
            raise CDataError('C DATA requires zero other nondebug allocations')
    groups = []
    for kind, _, payload in obj.records:
        if kind != 0x9a:
            continue
        cursor = _Cursor(payload)
        name_index = cursor.index()
        if not 0 < name_index < len(obj.names):
            raise CDataError('C DATA group has undefined LNAMES index')
        members = []
        while cursor:
            if cursor.byte() != 0xff:
                raise CDataError('C DATA group requires SEGDEF components')
            member = cursor.index()
            if member not in obj.segments or member in members:
                raise CDataError('C DATA group has missing or duplicate segment')
            members.append(member)
        groups.append({'index': len(groups) + 1, 'name': obj.names[name_index],
                       'segments': members})
    if (len(groups) != 1 or groups[0]['name'] != 'DGROUP'
            or public.group != groups[0]['index'] or segment.index not in groups[0]['segments']):
        raise CDataError('C DATA requires one explicit matching DGROUP membership')
    if any(p.segment != segment.index or p.group != public.group
           or not 0 <= p.offset < segment.length for p in obj.publics.values()):
        raise CDataError('C DATA publics must belong to the complete DATA contribution')
    if segment.unsupported_data or any(kind == 0xa2 for kind, _, _ in obj.records):
        raise CDataError('C DATA iterated LIDATA is forbidden')
    data, writes = bytearray(), []
    for offset, content in sorted(segment.chunks):
        if not content or offset != len(data) or offset + len(content) > segment.length:
            raise CDataError('C DATA has a hole, overlap or invalid LEDATA extent')
        data.extend(content)
        writes.append({'offset': offset, 'length': len(content),
                       'sha256': hashlib.sha256(content).hexdigest()})
    if len(data) != segment.length:
        raise CDataError('C DATA has an uninitialized SEGDEF tail')
    metadata = {'boundary': 'complete_omf_data_segment', 'symbol': symbol,
                'segment': {'index': segment.index, 'name': segment.name,
                            'class_name': segment.class_name, 'length': segment.length,
                            'attributes': attributes},
                'public': asdict(public), 'publics': {n: asdict(p) for n, p in obj.publics.items()},
                'group': groups[0], 'data_writes': writes,
                'sha256': hashlib.sha256(data).hexdigest(),
                'startup_marker_unused': bool(externals), 'emitted_mz_sites': [],
                'authored_c_function_count': 0}
    return bytes(data), metadata
