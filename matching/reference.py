"""Provenance-bound expanded reference bytes, used only for comparisons.

This module never generates reconstructed code/data or matching credit. It
checks a fixed original artifact and deterministic analysis carrier before
exposing the original unrelocated image to a comparison boundary.
"""
import hashlib

try:
    from .exepack import unpack_exepack
except ImportError:
    from exepack import unpack_exepack

ORIGINAL_SHA256 = 'c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
CARRIER_SHA256 = 'faf3516d0e72e30005ad90cb2da165081af5fe6871f5e8c3663980a5d725ef02'
IMAGE_SIZE = 401131


def validate_data_address(unit: dict, context: dict) -> tuple[int, int]:
    """Authenticate an initialized near-DATA placement in the original DGROUP.

    The two complete pinned CRT0 BASE16 sites independently carry this same
    paragraph. This is comparison placement evidence, not a source definition
    or reconstructed global link map.
    """
    image = context.get('image', b'')
    if (context.get('original_sha256') != ORIGINAL_SHA256
            or context.get('carrier_sha256') != CARRIER_SHA256
            or len(image) != IMAGE_SIZE):
        raise ValueError('Pointer DATA requires pinned original/expanded reference provenance')
    sites = set(context.get('relocations', ()))
    if (not {0xea91, 0xeb1c} <= sites or image[0xea90:0xea93] != b'\xbf\xc2\x5c'
            or image[0xeb1b:0xeb20] != b'\xb8\xc2\x5c\x8e\xd8'):
        raise ValueError('Pointer DATA requires the independently verified original CRT0 DGROUP operands')
    frame = int.from_bytes(image[0xea91:0xea93], 'little')
    address = unit.get('data_address')
    if (not isinstance(address, dict) or set(address) != {'segment', 'offset'}
            or any(type(address[k]) is not int or not 0 <= address[k] <= 0xffff
                   for k in ('segment', 'offset'))
            or address['segment'] != frame):
        raise ValueError('Pointer DATA requires the original explicit DGROUP paragraph and offset')
    origin = unit.get('image_offset')
    origin = int(origin, 0) if isinstance(origin, str) else origin
    size = unit.get('size')
    if (type(origin) is not int or type(size) is not int or size <= 0
            or origin != frame * 16 + address['offset']
            or address['offset'] + size > 0x10000 or origin + size > len(image)):
        raise ValueError('Pointer DATA placement must describe the full initialized extent')
    return frame, address['offset']


def build_reference(original: bytes) -> dict:
    """Return a checked comparison context; no filesystem reads or writes."""
    actual = hashlib.sha256(original).hexdigest()
    if actual != ORIGINAL_SHA256:
        raise ValueError('Expanded reference original SHA-256 mismatch')
    decoded = unpack_exepack(original)
    carrier = decoded.analysis_mz(trim_padding=5)
    carrier_sha256 = hashlib.sha256(carrier).hexdigest()
    if carrier_sha256 != CARRIER_SHA256:
        raise ValueError('Expanded reference analysis carrier SHA-256 mismatch')
    image = decoded.image[:-5]
    if len(image) != IMAGE_SIZE:
        raise ValueError('Expanded reference image size mismatch')
    return {'image': image, 'original_sha256': actual,
            'carrier_sha256': carrier_sha256, 'relocations': tuple(decoded.relocations),
            'prefix_size': decoded.prefix_size}


def validate_expanded_read(evidence: dict, unit: dict, linked: bytes, context: dict,
                           *, emitted_mz_sites=None) -> str:
    """Validate a full raw REA read against independent linked bytes.

    By default any overlapping MZ word is rejected. An explicit collection of
    absolute image sites enables exact forward DOS loader arithmetic: emitted
    sites must equal all original sites in the extent, linked bytes must match
    the unrelocated reference, and adding load paragraph 0x1000 to those words
    must match every raw REA byte. Crossing words are always rejected. This is
    comparison only; it establishes neither allocation ownership nor credit.
    """
    if (context.get('original_sha256') != ORIGINAL_SHA256
            or context.get('carrier_sha256') != CARRIER_SHA256
            or len(context['image']) != IMAGE_SIZE):
        raise ValueError('Expanded reference context provenance mismatch')
    if unit.get('reference_region') != 'exepack-expanded':
        raise ValueError('Expanded reference requires an explicit expanded-image region')
    origin = int(unit['image_offset'], 0) if isinstance(unit['image_offset'], str) else unit['image_offset']
    size = unit['size']
    if (type(origin) is not int or type(size) is not int or size <= 0
            or origin < 0 or origin + size > len(context['image']) or len(linked) != size):
        raise ValueError('Expanded reference invalid complete unit extent')
    overlapping = {site for site in context['relocations']
                   if site < origin + size and origin < site + 2}
    if emitted_mz_sites is None and overlapping:
        raise ValueError('Expanded reference unit overlaps MZ relocation; loader adjustment unsupported')
    if emitted_mz_sites is not None:
        if not isinstance(emitted_mz_sites, (list, tuple, set, frozenset)):
            raise ValueError('Expanded reference emitted MZ sites require an explicit collection')
        if any(type(site) is not int for site in emitted_mz_sites):
            raise ValueError('Expanded reference emitted MZ sites must be integer image offsets')
        emitted = set(emitted_mz_sites)
        if len(emitted) != len(emitted_mz_sites):
            raise ValueError('Expanded reference duplicate emitted MZ sites')
        if any(site < origin or site + 2 > origin + size for site in overlapping | emitted):
            raise ValueError('Expanded reference crossing or out-of-extent MZ word')
        if emitted != overlapping:
            raise ValueError('Expanded reference emitted MZ sites differ from original extent')
        ordered = sorted(emitted)
        if any(a + 2 > b for a, b in zip(ordered, ordered[1:])):
            raise ValueError('Expanded reference overlapping MZ words')
    else:
        emitted = set()
    if linked != context['image'][origin:origin + size]:
        raise ValueError('Expanded REA unrelocated source raw-byte comparison mismatch')
    profile = evidence.get('analysis_profile', {}).get('parameters', {})
    if (evidence.get('subject', {}).get('digest', {}).get('sha256') != context['carrier_sha256']
            or evidence.get('operation') != 'read_bytes'
            or profile.get('load_segment') != '0x1000'
            or profile.get('language_id') != 'x86:LE:16:Real Mode'
            or profile.get('target_format') != 'dos-mz'):
        raise ValueError('Expanded REA evidence target/profile mismatch')
    start = 0x10000 + origin
    loaded = bytearray(linked)
    for site in sorted(emitted):
        offset = site - origin
        word = int.from_bytes(linked[offset:offset + 2], 'little')
        loaded[offset:offset + 2] = ((word + 0x1000) & 0xffff).to_bytes(2, 'little')
    parameters = evidence['parameters']
    raw = evidence['normalized_result']
    try:
        observed = bytes.fromhex(raw['bytes_hex'])
    except (ValueError, TypeError) as exc:
        raise ValueError('Expanded REA raw bytes are invalid') from exc
    if (int(parameters['address'], 0) != start or parameters['length'] != size
            or int(raw['address'], 0) != start or raw.get('complete') is not True
            or raw['requested_bytes'] != size or raw['returned_bytes'] != size
            or len(observed) != size or observed != loaded):
        raise ValueError('Expanded REA complete raw-byte comparison mismatch')
    return evidence['evidence_id']
