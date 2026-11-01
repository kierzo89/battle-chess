"""Strict OMF86 reader for compiler output (never reads a reference executable).

Only contiguous, relocation-free LEDATA extents can be extracted. Relocations
are retained as evidence, never silently masked or applied. An explicit public
end symbol is preferable to an inferred next-public/segment-end boundary.
"""
from dataclasses import dataclass, field
from pathlib import Path


class OMFError(ValueError):
    pass


class _Cursor:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, size):
        if self.pos + size > len(self.data):
            raise OMFError('truncated OMF record payload')
        result = self.data[self.pos:self.pos + size]
        self.pos += size
        return result

    def byte(self):
        return self.take(1)[0]

    def word(self):
        return int.from_bytes(self.take(2), 'little')

    def index(self):
        first = self.byte()
        return ((first & 0x7f) << 8) | self.byte() if first & 0x80 else first

    def name(self):
        return self.take(self.byte()).decode('latin1')

    def finish(self):
        if self.pos != len(self.data):
            raise OMFError('unexpected trailing OMF record payload')

    def __bool__(self):
        return self.pos < len(self.data)


@dataclass
class Segment:
    index: int
    length: int
    name_index: int
    class_index: int
    overlay_index: int
    attributes: int
    chunks: list = field(default_factory=list)
    unsupported_data: bool = False
    name: str = ''
    class_name: str = ''


@dataclass(frozen=True)
class Public:
    name: str
    segment: int
    offset: int
    group: int
    type_index: int


@dataclass(frozen=True)
class Fixup:
    segment: int
    offset: int
    width: int
    location_type: int
    segment_relative: bool
    frame: tuple
    target: tuple
    displacement: int | None
    record_offset: int
    raw: bytes


@dataclass
class OMFObject:
    segments: dict = field(default_factory=dict)
    publics: dict = field(default_factory=dict)
    names: list = field(default_factory=lambda: [''])
    fixups: list = field(default_factory=list)
    records: list = field(default_factory=list)
    externals: dict = field(default_factory=dict)
    data_writes: list = field(default_factory=list)
    procedures: dict = field(default_factory=dict)

    def function_info(self, symbol, end_symbol=None):
        if symbol not in self.publics:
            raise OMFError(f'public symbol not found: {symbol}')
        public = self.publics[symbol]
        segment = self.segments.get(public.segment)
        if segment is None:
            raise OMFError(f'{symbol}: absolute or missing segment')
        if segment.unsupported_data:
            raise OMFError(f'{symbol}: segment contains unsupported iterated data')
        if segment.class_name.upper() != 'CODE' and not segment.name.upper().endswith('TEXT'):
            raise OMFError(f'{symbol}: segment is not identified as code')
        if end_symbol is not None:
            end_public = self.publics.get(end_symbol)
            if end_public is None or end_public.segment != public.segment:
                raise OMFError(f'{symbol}: end symbol missing or in another segment')
            end = end_public.offset
        elif symbol in self.procedures:
            end = public.offset + self.procedures[symbol]['length']
        else:
            end = min((p.offset for p in self.publics.values()
                       if p.segment == public.segment and p.offset > public.offset),
                      default=segment.length)
        if not public.offset < end <= segment.length:
            raise OMFError(f'{symbol}: invalid or empty extent')
        relocations = [f for f in self.fixups if f.segment == public.segment
                       and f.offset < end and f.offset + f.width > public.offset]
        return {'symbol': symbol, 'segment': public.segment, 'offset': public.offset,
                'end': end, 'size': end - public.offset,
                'boundary': ('explicit_public' if end_symbol else
                             'codeview3_procedure' if symbol in self.procedures else
                             'next_public_or_segment_end'),
                'fixups': relocations}

    def extract_function(self, symbol, end_symbol=None):
        info = self.function_info(symbol, end_symbol)
        if info['fixups']:
            raise OMFError(f'{symbol}: unresolved FIXUPP relocation in function extent')
        start, end = info['offset'], info['end']
        chunks = sorted(self.segments[info['segment']].chunks)
        result, position = bytearray(), start
        for offset, data in chunks:
            left, right = max(start, offset), min(end, offset + len(data))
            if left >= right:
                continue
            if left != position:
                raise OMFError(f'{symbol}: hole in LEDATA at {position:#x}')
            result.extend(data[left - offset:right - offset])
            position = right
        if position != end:
            raise OMFError(f'{symbol}: hole in LEDATA at {position:#x}')
        return bytes(result)


def _datum(cursor, method):
    if method <= 2:
        return cursor.index()
    if method == 3:
        return cursor.word()
    if method in (4, 5):
        return None
    raise OMFError('reserved FIXUPP method')


def _fixupp(obj, payload, last_data, threads, record_offset):
    c = _Cursor(payload)
    widths = {0: 1, 1: 2, 2: 2, 3: 4, 4: 1, 5: 2}
    while c:
        begin = c.pos
        first = c.byte()
        if not first & 0x80:
            if first & 0x20:
                raise OMFError('reserved FIXUPP thread bit')
            frame, method, slot = bool(first & 0x40), (first >> 2) & 7, first & 3
            if not frame:
                # TIS OMF 1.1, FIXUPP THREAD: only low two target
                # method bits apply; the referring FIXUP's P bit selects
                # displacement presence. T4/T5/T6 reuse T0/T1/T2 indexes.
                # https://refspecs.linuxfoundation.org/elf/TIS1.1.pdf
                if method == 7:
                    raise OMFError('reserved target thread method')
                method &= 3
            threads[(frame, slot)] = (method, _datum(c, method))
            continue
        if last_data is None:
            raise OMFError('FIXUPP without preceding LEDATA')
        location = (first >> 2) & 0xf
        if location not in widths:
            raise OMFError('unsupported FIXUPP location type')
        relative = ((first & 3) << 8) | c.byte()
        segment, offset, size = last_data
        width = widths[location]
        if relative + width > size:
            raise OMFError('FIXUPP location outside preceding LEDATA')
        fixdat = c.byte()
        if fixdat & 0x80:
            slot = (fixdat >> 4) & 3
            if (True, slot) not in threads:
                raise OMFError('undefined FIXUPP frame thread')
            frame = threads[(True, slot)]
        else:
            method = (fixdat >> 4) & 7
            frame = (method, _datum(c, method))
        if fixdat & 8:
            slot = fixdat & 3
            if (False, slot) not in threads:
                raise OMFError('undefined FIXUPP target thread')
            target = threads[(False, slot)]
        else:
            method = fixdat & 3
            target = (method, _datum(c, method))
        displacement = None if fixdat & 4 else c.word()
        obj.fixups.append(Fixup(segment, offset + relative, width, location,
                                bool(first & 0x40), frame, target, displacement,
                                record_offset, payload[begin:c.pos]))


def read_omf(data):
    """Parse one OMF86 object module, validating every record and data extent."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError('read_omf expects object bytes')
    obj, pos, ended, last_data, threads = OMFObject(), 0, False, None, {}
    while pos < len(data):
        record_offset = pos
        if ended:
            raise OMFError('data after MODEND (multiple modules are unsupported)')
        if pos + 3 > len(data):
            raise OMFError('truncated OMF record header')
        kind, length = data[pos], int.from_bytes(data[pos + 1:pos + 3], 'little')
        if length < 1 or pos + 3 + length > len(data):
            raise OMFError('invalid or truncated OMF record length')
        record = bytes(data[pos:pos + 3 + length])
        if sum(record) & 255:
            raise OMFError(f'OMF checksum mismatch at {pos:#x}')
        payload = record[3:-1]
        obj.records.append((kind, record_offset, payload))
        pos += 3 + length
        c = _Cursor(payload)
        if kind in (0x91, 0x95, 0x99, 0x9d, 0xa1, 0xa3, 0xb7, 0xc2, 0xc3):
            raise OMFError(f'unsupported 32-bit or COMDAT OMF record {kind:#x}')
        if kind in (0x80, 0x82):
            c.name()
            c.finish()
        elif kind == 0x96:
            while c:
                obj.names.append(c.name())
        elif kind == 0x98:
            attr = c.byte()
            alignment = attr >> 5
            if alignment == 0:
                c.word()
                c.byte()
            if attr & 1:
                raise OMFError('32-bit SEGDEF is unsupported')
            size = c.word()
            size = 65536 if attr & 2 else size
            segment = Segment(len(obj.segments) + 1, size, c.index(), c.index(), c.index(), attr)
            c.finish()
            obj.segments[segment.index] = segment
        elif kind in (0x90, 0xb6):
            group, segment = c.index(), c.index()
            if not segment:
                c.word()
            while c:
                name, offset, type_index = c.name(), c.word(), c.index()
                if name in obj.publics:
                    raise OMFError(f'duplicate public symbol {name}')
                obj.publics[name] = Public(name, segment, offset, group, type_index)
        elif kind in (0x8c, 0xb4):
            while c:
                symbol, type_index = c.name(), c.index()
                obj.externals[len(obj.externals) + 1] = symbol
        elif kind in (0xb0, 0xb8):
            while c:
                symbol, type_index, datatype = c.name(), c.index(), c.byte()
                if datatype not in (0x61, 0x62):
                    raise OMFError('unsupported communal data type')
                for _ in range(2 if datatype == 0x61 else 1):
                    leaf = c.byte()
                    if leaf > 0x80:
                        if leaf not in (0x81, 0x84, 0x88):
                            raise OMFError('unsupported communal numeric leaf')
                        c.take({0x81: 2, 0x84: 3, 0x88: 4}[leaf])
                obj.externals[len(obj.externals) + 1] = symbol
        elif kind in (0xa0, 0xa2):
            segment, offset = c.index(), c.word()
            if segment not in obj.segments:
                raise OMFError('data refers to undefined segment')
            seg = obj.segments[segment]
            content = c.take(len(payload) - c.pos)
            if kind == 0xa2:
                seg.unsupported_data = True
                last_data = None
            else:
                if offset + len(content) > seg.length:
                    raise OMFError('LEDATA exceeds SEGDEF length')
                # C5.10 /Zi backpatches lengths in $$SYMBOLS with later
                # LEDATA. Permit this only in the designated debug segment;
                # code/data overlap remains an error.
                debug_patch = (seg.name_index < len(obj.names) and
                               obj.names[seg.name_index] == '$$SYMBOLS' and
                               seg.class_index < len(obj.names) and
                               obj.names[seg.class_index] == 'DEBSYM')
                if not debug_patch and any(offset < old + len(chunk) and old < offset + len(content)
                       for old, chunk in seg.chunks):
                    raise OMFError('overlapping LEDATA records')
                seg.chunks.append((offset, content))
                obj.data_writes.append((record_offset, segment, offset, len(content)))
                last_data = (segment, offset, len(content))
        elif kind == 0x9c:
            _fixupp(obj, payload, last_data, threads, record_offset)
        elif kind in (0x8a, 0x8b):
            if kind == 0x8b:
                raise OMFError('32-bit MODEND is unsupported')
            if not payload:
                raise OMFError('empty MODEND')
            ended = True
        elif kind not in (0x88, 0x94, 0x9a, 0xb2, 0xbc, 0xc6):
            raise OMFError(f'unsupported OMF record {kind:#x}')
    if not obj.records or obj.records[0][0] not in (0x80, 0x82) or not ended:
        raise OMFError('expected THEADR/LHEADR and MODEND')
    for seg in obj.segments.values():
        try:
            seg.name = obj.names[seg.name_index]
            seg.class_name = obj.names[seg.class_index]
            obj.names[seg.overlay_index]
        except IndexError as exc:
            raise OMFError('SEGDEF refers to undefined LNAMES index') from exc
    for public in obj.publics.values():
        if public.segment and (public.segment not in obj.segments or
                               public.offset > obj.segments[public.segment].length):
            raise OMFError('PUBDEF lies outside segment')
    _codeview3_procedures(obj)
    return obj


def extract_function(data, symbol, end_symbol=None):
    return read_omf(data).extract_function(symbol, end_symbol)


def read_object(path):
    return read_omf(Path(path).read_bytes())


def _codeview3_procedures(obj):
    """Read C5.x CV3 procedure lengths, anchored by actual OMF relocations.

    CV3 PROC record: byte length, byte kind=1, offset16, type16,
    length16, debug-start16, debug-end16, reserved16, flags8, pstring.
    The unlinked offset field refers to an EXTDEF public via FIXUPP.
    We resolve only that debug reference; generated code is never relocated.
    """
    for seg in obj.segments.values():
        if seg.name != '$$SYMBOLS' or seg.class_name != 'DEBSYM':
            continue
        data, present = bytearray(seg.length), bytearray(seg.length)
        for offset, content in seg.chunks:
            data[offset:offset + len(content)] = content
            present[offset:offset + len(content)] = b'\x01' * len(content)
        if not all(present):
            raise OMFError('hole in CodeView symbols segment')
        if len(data) >= 4 and data[:4] == b'\x01\x00\x00\x00':
            # Later CodeView versions do not use the CV3 record layout.
            continue
        active = []
        for f in obj.fixups:
            if f.segment != seg.index:
                continue
            if any(record_offset > f.record_offset and segment == seg.index
                   and offset < f.offset + f.width and f.offset < offset + size
                   for record_offset, segment, offset, size in obj.data_writes):
                continue
            active.append(f)
        pos = 0
        while pos < len(data):
            size = data[pos] + 1
            if size < 2 or pos + size > len(data):
                raise OMFError('truncated CodeView3 symbol record')
            record = bytes(data[pos:pos + size])
            if record[1] == 1:
                if len(record) < 16 or 16 + record[15] != len(record):
                    raise OMFError('invalid CodeView3 procedure record')
                refs = [f for f in active if f.offset == pos + 2 and f.width == 2]
                if len(refs) != 1 or refs[0].target[0] != 2:
                    raise OMFError('CodeView3 procedure lacks unique external offset relocation')
                ref = refs[0]
                symbol = obj.externals.get(ref.target[1])
                public = obj.publics.get(symbol)
                if public is None:
                    raise OMFError('CodeView3 procedure references unknown public')
                if int.from_bytes(record[2:4], 'little') or ref.displacement not in (None, 0):
                    raise OMFError('unsupported CodeView3 procedure offset addend')
                length = int.from_bytes(record[6:8], 'little')
                if not length or public.offset + length > obj.segments[public.segment].length:
                    raise OMFError('CodeView3 procedure length lies outside code segment')
                if symbol in obj.procedures:
                    raise OMFError('duplicate CodeView3 procedure symbol')
                obj.procedures[symbol] = {
                    'length': length, 'debug_symbol_offset': pos,
                    'name': record[16:].decode('latin1'), 'debug_segment': seg.index,
                    'relocation_record_offset': ref.record_offset,
                }
            pos += size
