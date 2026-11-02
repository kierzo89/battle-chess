"""Replay original compositor-verified assets through native indexed compositor."""
from pathlib import Path
import ctypes as C,json,hashlib,sys
root=Path(__file__).resolve().parents[2];lib=C.CDLL(sys.argv[1])
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(root/path).read_bytes();assert hashlib.sha256(b).hexdigest()==pins[path];return b
class Image(C.Structure):_fields_=[('width',C.c_uint),('height',C.c_uint),('x',C.c_int),('y',C.c_int),('pixels',C.POINTER(C.c_uint8)),('length',C.c_size_t)]
lib.bc_compose.argtypes=[C.POINTER(Image),C.POINTER(Image),C.POINTER(C.c_uint8),C.c_size_t,C.POINTER(Image)];lib.bc_compose.restype=C.c_bool
def image(desc,data):
 buf=(C.c_uint8*len(data)).from_buffer_copy(data);v=Image(*desc,buf,len(data));v.buffer=buf;return v
def load(folder,f):return image((f['width'],f['height'],f['anchor_x'],f['anchor_y']),read(folder+f['indices_file']))
def compose(a,b):
 buf=(C.c_uint8*65536)();v=Image();assert lib.bc_compose(C.byref(a),C.byref(b),buf,len(buf),C.byref(v));v.buffer=buf;return v
def value(v):return (v.width,v.height,v.x,v.y),bytes(v.pixels[:v.length])
base='assets/recovered/metadata/bank2-records/'
records={(r['pair'],r['record']):load(base,r) for r in json.loads(read(base+'report.json'))['records']}
count=0
for path in sorted(p for p in pins if p.startswith('assets/recovered/animations/') and p.endswith('/sequence.json')):
 seq=json.loads(read(path));folder=path.rsplit('/',1)[0]+'/'
 a=load(folder,seq['frames'][0])
 for f in seq['frames'][1:]:
  a=compose(a,records[seq['pair'],f['delta_record']]);expected=load(folder,f)
  assert value(a)==value(expected),(path,f['step']);count+=1
assert count>2000
# Descriptor bounds, palette, and buffer sizes must fail closed.
a=image((1,1,0,0),b'\x01\0\0\0');b=image((1,1,0,0),b'\x02\0\0\0');buf=(C.c_uint8*4)();out=Image()
assert not lib.bc_compose(C.byref(a),C.byref(b),buf,3,C.byref(out))
b.pixels[0]=16;assert not lib.bc_compose(C.byref(a),C.byref(b),buf,4,C.byref(out))
print(f'PASS: {count} cumulative frames match original native-compositor descriptors and complete indexed pixels.')

# Fresh original-machine evidence covers the cross-list queen exception,
# rather than accepting the visually similar independently composed frames.
proof_path=root/'native/evidence/queen-turn-composition.json'
raw=proof_path.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='53290ac74b204f4b0d6f243fb2fd1f26c3a97ef13dbae09ad8cd22619d78338d'
proof=json.loads(raw);folder='assets/recovered/animations/'+proof['initial_sequence']+'/'
seq=json.loads(read(folder+'sequence.json'));a=load(folder,seq['frames'][0])
for row in proof['rows']:
 a=compose(a,records[4,row['delta_record']]);desc,data=value(a)
 packed=bytes((data[i]<<4)|data[i+1] for i in range(0,len(data),2))
 assert list(desc)==row['proof']['descriptor']
 assert hashlib.sha256(packed).hexdigest()==row['proof']['pixel_sha256']
 assert row['proof']['original_fill_and_blitter_executed']
print(f"PASS: {len(proof['rows'])} newly verified original-machine queen cross-list compositions.")
