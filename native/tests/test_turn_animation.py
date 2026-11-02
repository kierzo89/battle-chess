"""Compare every turn frame and completion time with retained native execution."""
from pathlib import Path
import ctypes as C,json,hashlib,sys
root=Path(__file__).resolve().parents[2];lib=C.CDLL(sys.argv[1])
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
path='assets/recovered/metadata/tasks/turn-tasks.json';raw=(root/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==pins[path]
class Clock(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_size_t),('cursor',C.c_size_t),('wait',C.c_uint8),('failed',C.c_bool)]
class Sequence(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_uint),('pair',C.c_uint),('list',C.c_uint),('count',C.c_uint),('tokens',C.POINTER(C.c_uint))]
class Turn(C.Structure):_fields_=[('clock',Clock),('sequence',C.POINTER(Sequence))]+[(s,C.c_uint) for s in ('kind','from_','to','profile','step','frame')]+[('direction',C.c_int),('failed',C.c_bool),('done',C.c_bool)]
CB=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_int)
lib.bc_turn_begin.argtypes=[C.POINTER(Turn)]+[C.c_uint]*4;lib.bc_turn_begin.restype=C.c_bool
lib.bc_turn_tick.argtypes=[C.POINTER(Turn),C.c_uint,CB,C.c_void_p];lib.bc_turn_tick.restype=C.c_int
mapping={2:1,5:2,6:3,1:4,3:5,4:6};cases=frames=0
@CB
def dispatch(ctx,asset,colour,pitch):pass
for row in json.loads(raw)['rows']:
 t=Turn();assert lib.bc_turn_begin(C.byref(t),mapping[row['piece']],row['from'],row['to'],row['profile'])
 actual=[];completed=None
 for tick in range(row['completed_call']+1):
  status=lib.bc_turn_tick(C.byref(t),64,dispatch,None);assert status>=0,(row,tick)
  if status==1:actual.append((tick,t.sequence.contents.tokens[t.frame]))
  if status==2:completed=tick;break
 expected=[(f['tick'],f['frame']) for f in row['frame_events']]
 assert actual==expected,(row,actual)
 assert completed==row['completed_call'],(row,completed)
 assert lib.bc_turn_tick(C.byref(t),64,dispatch,None)==2
 cases+=1;frames+=len(actual)
for args in [(0,0,1,0),(7,0,1,0),(1,8,0,0),(1,0,8,0),(1,0,1,2),(4,0,1,0)]:
 t=Turn();assert not lib.bc_turn_begin(C.byref(t),*args);assert lib.bc_turn_tick(C.byref(t),0,dispatch,None)==-1
assert cases==480
print(f'PASS: {cases} original turn tasks; {frames} frame identities/timestamps and all completion calls.')

# The original continuation applies a delta to the previous actor image. Check
# whether a precomposed-list shortcut has the same starting pixels; never assume
# this from frame-token equality. The known exception must be resolved before
# that shortcut can be used by the live renderer.
def pixels(pair,seq,step):
 folder=f'assets/recovered/animations/pair-{pair:02d}-list-{seq:02d}/'
 def read(name):
  b=(root/name).read_bytes();assert hashlib.sha256(b).hexdigest()==pins[name];return b
 record=json.loads(read(folder+'sequence.json'));f=record['frames'][step]
 b=read(folder+f['indices_file']);w=f['storage_width']
 return {(i%w-f['anchor_x'],i//w-f['anchor_y']):v for i,v in enumerate(b) if v}
exceptions=[];checked=0
for kind in (1,2,5):
 step=2 if kind==1 else 1
 for ori in range(0,8,step):
  for direction in (-1,1):
   first=ori+(8 if direction>0 else 16)
   following=((ori+direction*step)&7)+(8 if direction>0 else 16)
   if kind==1:first//=2;following//=2
   if pixels(kind-1,first,-1)!=pixels(kind-1,following,1):exceptions.append((kind,ori,direction))
   checked+=1
assert checked==40 and exceptions==[(5,5,-1)],exceptions
print('Rendering diagnostic: 39/40 continuation pixel preconditions agree; graphics kind5 orientation5 negative turn requires original delta composition (not renderer-ready).')
