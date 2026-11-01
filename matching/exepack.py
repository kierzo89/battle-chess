"""Analysis-only decoder for the verified Microsoft EXEPACK 4.06 profile.

Recovered bytes and synthesized MZ headers are evidence, never rebuilt source
or matching credit. No original game bytes are embedded in this module.
"""
from dataclasses import dataclass
import hashlib
import struct

STUB_SHA256 = '3c2ecf0c7854abfe0390cfa2482fc3941cf255546ce1629132eb62bb08f3d435'
STUB_SIZE = 283
PACK_HEADER_SIZE = 18


class EXEPACKError(ValueError):
    pass


@dataclass(frozen=True)
class Packet:
    command: int
    count: int
    source_start: int
    destination_start: int
    fill: int | None


@dataclass(frozen=True)
class UnpackedImage:
    image: bytes
    relocations: tuple[int, ...]
    relocation_counts: tuple[int, ...]
    prefix_size: int
    packets: tuple[Packet, ...]
    pack_header_offset: int
    saved_ip: int
    saved_cs: int
    saved_sp: int
    saved_ss: int
    minalloc: int
    maxalloc: int
    overlay: bytes
    reserved_word: int
    relocation_table_offset: int

    def analysis_mz(self, trim_padding=0):
        """Synthesize an unpacked MZ for packer experiments, not original headers.

        File length before paragraph padding is not uniquely recoverable. Supply
        an explicit tested trim (0..15); default retains all recovered bytes.
        Original header padding, relocation aliases/order, checksum, and layout
        are not recovered by this operation.
        """
        if not isinstance(trim_padding, int) or not 0 <= trim_padding <= 15:
            raise EXEPACKError('Paragraph trim must be between 0 and 15')
        if trim_padding and self.image[-trim_padding:] != b'\0' * trim_padding:
            raise EXEPACKError('Only zero paragraph padding can be trimmed')
        image = self.image[:-trim_padding] if trim_padding else self.image
        if any(r + 2 > len(image) for r in self.relocations):
            raise EXEPACKError('Trim would remove relocation data')
        reloc_offset = self.relocation_table_offset
        if reloc_offset < 28:
            raise EXEPACKError('Invalid original relocation table metadata')
        header_size = ((reloc_offset + 4 * len(self.relocations) + 511) // 512) * 512
        header = bytearray(header_size)
        file_size = header_size + len(image)
        struct.pack_into('<14H', header, 0, 0x5a4d, file_size % 512,
                         (file_size + 511) // 512, len(self.relocations),
                         header_size // 16, self.minalloc, self.maxalloc,
                         self.saved_ss, self.saved_sp, 0, self.saved_ip,
                         self.saved_cs, reloc_offset, 0)
        if reloc_offset >= 30:
            struct.pack_into('<H', header, 28, self.reserved_word)
        for i, address in enumerate(self.relocations):
            struct.pack_into('<HH', header, reloc_offset + i * 4,
                             address % 65536, (address // 65536) * 4096)
        return bytes(header) + image


def decode_stream(packed: bytes, stream_end: int, unpacked_size: int):
    """Decode backward B0/B2 packets, retaining an unchanged leading prefix."""
    if not 0 < stream_end <= len(packed) or not 0 < unpacked_size <= 0xffff0:
        raise EXEPACKError('Invalid compressed stream bounds')
    source = stream_end
    padding = 0
    while source and packed[source - 1] == 0xff and padding < 16:
        source -= 1
        padding += 1
    image = bytearray(unpacked_size)
    destination = unpacked_size
    packets = []
    while True:
        if source < 3:
            raise EXEPACKError('Missing final packet or truncated command')
        command = packed[source - 1]
        count = struct.unpack_from('<H', packed, source - 3)[0]
        source -= 3
        if command & 0xfe not in (0xb0, 0xb2) or not count or count > destination:
            raise EXEPACKError('Invalid command or output bounds')
        destination -= count
        fill = None
        if command & 0xfe == 0xb0:
            if source < 1:
                raise EXEPACKError('Truncated fill byte')
            source -= 1
            fill = packed[source]
            image[destination:destination + count] = bytes([fill]) * count
        else:
            if source < count:
                raise EXEPACKError('Truncated literal data')
            source -= count
            image[destination:destination + count] = packed[source:source + count]
        packets.append(Packet(command, count, source, destination, fill))
        if command & 1:
            break
    if source != destination:
        raise EXEPACKError('Final packet does not meet unchanged prefix')
    image[:source] = packed[:source]
    return bytes(image), source, tuple(packets)


def unpack_exepack(data: bytes) -> UnpackedImage:
    """Recover image and relocation sites from an unrelocated packed DOS file."""
    if len(data) < 32 or data[:2] != b'MZ':
        raise EXEPACKError('Not a complete MZ executable')
    fields = struct.unpack_from('<14H', data)
    _, cblp, pages, reloc_count, header_paras, minalloc, maxalloc, _, _, _, ip, cs, reloc_ofs, _ = fields
    if not pages or cblp > 511 or reloc_count:
        raise EXEPACKError('Unsupported packed MZ header')
    file_size = (pages - 1) * 512 + (cblp or 512)
    header_size = header_paras * 16
    if not 32 <= header_size <= file_size <= len(data):
        raise EXEPACKError('Invalid MZ size')
    packed = data[header_size:file_size]
    header_offset = cs * 16
    if ip != PACK_HEADER_SIZE or header_offset + PACK_HEADER_SIZE > len(packed):
        raise EXEPACKError('Unrecognized EXEPACK entry/header')
    saved_ip, saved_cs, scratch, pack_size, saved_sp, saved_ss, dest_paras, skip_paras, signature = struct.unpack_from('<9H', packed, header_offset)
    if signature != 0x4252 or scratch or skip_paras != 1:
        raise EXEPACKError('Unsupported EXEPACK profile header')
    reloc_start = header_offset + PACK_HEADER_SIZE + STUB_SIZE
    if pack_size < PACK_HEADER_SIZE + STUB_SIZE + 32 or header_offset + pack_size != len(packed):
        raise EXEPACKError('Invalid EXEPACK block size')
    stub = packed[header_offset + PACK_HEADER_SIZE:reloc_start]
    if hashlib.sha256(stub).hexdigest() != STUB_SHA256:
        raise EXEPACKError('Unrecognized EXEPACK decompressor implementation')
    image, prefix, packets = decode_stream(packed, header_offset, dest_paras * 16)
    cursor = reloc_start
    relocations, counts = [], []
    for block in range(16):
        if cursor + 2 > len(packed):
            raise EXEPACKError('Truncated relocation count')
        count = struct.unpack_from('<H', packed, cursor)[0]
        cursor += 2
        counts.append(count)
        if cursor + count * 2 > len(packed):
            raise EXEPACKError('Truncated relocation offsets')
        for i in range(count):
            offset = struct.unpack_from('<H', packed, cursor)[0]
            cursor += 2
            address = block * 65536 + offset
            if address + 2 > len(image):
                raise EXEPACKError('Relocation outside recovered image')
            relocations.append(address)
    if cursor != len(packed) or len(set(relocations)) != len(relocations):
        raise EXEPACKError('Trailing or duplicate packed relocation data')
    original_minalloc = (len(packed) + 15) // 16 + minalloc - dest_paras
    if not 0 <= original_minalloc <= 65535:
        raise EXEPACKError('Invalid inferred unpacked allocation')
    return UnpackedImage(image, tuple(relocations), tuple(counts), prefix, packets,
                         header_offset, saved_ip, saved_cs, saved_sp, saved_ss,
                         original_minalloc, maxalloc, data[file_size:],
                         struct.unpack_from('<H', data, 28)[0], reloc_ofs)
