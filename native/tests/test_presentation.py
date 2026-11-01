"""Compare the native clock to retained original-byte timing evidence."""
import ctypes as C,hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
name='assets/recovered/metadata/timing/report.json'
raw=(root/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==pins[name]
report=json.loads(raw)
lib=C.CDLL(sys.argv[1])
class Clock(C.Structure):
 _fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_size_t),('cursor',C.c_size_t),('wait',C.c_uint8),('failed',C.c_bool)]
CB=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_int)
lib.bc_task_ready.argtypes=[C.POINTER(Clock),C.c_bool,C.c_uint,CB,C.c_void_p];lib.bc_task_ready.restype=C.c_bool
count=0;dispatch_count=0
for item in report['capture_controls']:
 data=bytes.fromhex(item['raw_hex']);assert hashlib.sha256(data).hexdigest()==item['sha256']
 buf=(C.c_uint8*len(data)).from_buffer_copy(data);clock=Clock(buf,len(data),0,0,False)
 actual=[];events=[]
 @CB
 def dispatch(ctx,asset,colour,pitch):
  assert colour==64
  events.append({'asset':asset,'argument':pitch})
 for tick in range(item['ready_events'][-1]['tick']+1):
  probe=clock.cursor
  if not clock.wait:
   while data[probe]>127 and data[probe]!=255:probe+=2
  terminal=not clock.wait and data[probe]==255
  ready=lib.bc_task_ready(C.byref(clock),False,64,dispatch,None)
  if ready:
   actual.append({'tick':tick,'delay':clock.wait,'dispatch':events.copy(),'terminal':bool(terminal)})
   events.clear()
 assert not clock.failed
 assert actual==item['ready_events']
 pos=clock.cursor;assert data[pos]==255
 for _ in range(3):assert lib.bc_task_ready(C.byref(clock),False,64,dispatch,None) and clock.cursor==pos
 count+=len(actual);dispatch_count+=sum(len(e['dispatch']) for e in actual)
# Malformed control never reads outside its buffer.
for data in (b'',b'\x80',b'\x80\x40'):
 buf=(C.c_uint8*len(data)).from_buffer_copy(data);c=Clock(buf,len(data),0,0,False)
 assert not lib.bc_task_ready(C.byref(c),False,64,dispatch,None) and c.failed
# Tilted presentation does not dereference control; pending delays still count.
c=Clock(None,0,0,2,False)
assert not lib.bc_task_ready(C.byref(c),True,64,dispatch,None)
assert not lib.bc_task_ready(C.byref(c),True,64,dispatch,None)
assert lib.bc_task_ready(C.byref(c),True,64,dispatch,None)
print(f'PASS: 144 original capture-control streams, {count} readiness events, {dispatch_count} sound dispatches; FF tails and bounds.')

# Compare signed rounding to the unchanged recovered function body. This is a
# host-source reference; original 16-bit-overflow coordinates are not claimed.
import subprocess,tempfile,random
source=(root/'matching/src/board_display_match.c').read_bytes()
assert hashlib.sha256(source).hexdigest()=='25932c27b44476a391070f1944ea6bfbeb7d2365714049c2a7e269dd24167271'
body=source.decode().split('void interpolate_position_5ebc',1)[1]
with tempfile.TemporaryDirectory(prefix='bc-interpolation-') as d:
 p=Path(d);(p/'reference.c').write_text('int motion_x,motion_y;\nvoid interpolate_position_5ebc'+body)
 subprocess.run([sys.argv[2],'-shared','-fPIC',str(p/'reference.c'),'-o',str(p/'reference.so')],check=True)
 ref=C.CDLL(str(p/'reference.so'));ref.interpolate_position_5ebc.argtypes=[C.c_int]*6
 lib.bc_interpolate.argtypes=[C.c_int]*4+[C.c_uint]*2+[C.POINTER(C.c_int)]*2;lib.bc_interpolate.restype=C.c_bool
 rng=random.Random(2026)
 for i in range(20000):
  args=[rng.randrange(-320,321),rng.randrange(-200,201),rng.randrange(-320,321),rng.randrange(-200,201)]
  n=rng.randrange(1,65);step=rng.randrange(n+1);args += [n,step]
  ref.interpolate_position_5ebc(*args);x=C.c_int();y=C.c_int()
  assert lib.bc_interpolate(*args,C.byref(x),C.byref(y))
  assert (x.value,y.value)==(C.c_int.in_dll(ref,'motion_x').value,C.c_int.in_dll(ref,'motion_y').value)
 assert not lib.bc_interpolate(0,0,1,1,0,0,C.byref(x),C.byref(y))
lib.bc_presentation_tick.argtypes=[C.c_uint64,C.POINTER(C.c_uint64),C.c_bool];lib.bc_presentation_tick.restype=C.c_bool
last=C.c_uint64(100)
assert not lib.bc_presentation_tick(100,C.byref(last),False)
assert not lib.bc_presentation_tick(101,C.byref(last),False)
assert lib.bc_presentation_tick(102,C.byref(last),False) and last.value==102
assert lib.bc_presentation_tick(110,C.byref(last),False) and last.value==110
assert not lib.bc_presentation_tick(110,C.byref(last),False)
assert not lib.bc_presentation_tick(200,C.byref(last),True) and last.value==110
print('PASS: 20000 recovered interpolation comparisons; two-tick gate, late polling and input priority.')
