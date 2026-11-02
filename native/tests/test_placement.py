"""Exercise recovered effect and offset timing, plus target/visible split."""
from pathlib import Path
import ctypes as C,json,hashlib,sys
root=Path(__file__).resolve().parents[2];lib=C.CDLL(sys.argv[1])
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(root/path).read_bytes();assert hashlib.sha256(b).hexdigest()==pins[path];return json.loads(b)
class Walk(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_uint),('pair',C.c_uint),('list',C.c_uint),('count',C.c_uint)]
class Clock(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_size_t),('cursor',C.c_size_t),('wait',C.c_uint8),('failed',C.c_bool)]
class Task(C.Structure):_fields_=[('sequence',C.POINTER(Walk)),('clock',Clock)]+[(n,C.c_uint) for n in ('frame','emitted','total','steps')]+[(n,C.c_int) for n in ('from_x','from_y','to_x','to_y','x','y','anchor_x','anchor_y')]+[(n,C.c_bool) for n in ('done','failed','command_active')]+[('mode',C.c_int)]
CB=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_int)
lib.bc_placement_begin.argtypes=[C.POINTER(Task),C.c_int]+[C.c_uint]*3+[C.c_int]*4+[C.c_bool];lib.bc_placement_begin.restype=C.c_bool
lib.bc_placement_tick.argtypes=[C.POINTER(Task),C.c_uint,CB,C.c_void_p];lib.bc_placement_tick.restype=C.c_int
@CB
def dispatch(ctx,asset,colour,pitch):pass
mapping={2:1,5:2,6:3,1:4,3:5,4:6};modes={'effect':0,'offset_half':1,'offset_full':2};cases=0
# Original C truncates signed division toward zero, including rounding terms.
def div(a,b):return (abs(a)//b)*(1 if a>=0 else -1)
def interpolate(a,b,n,i):
 d=b-a;q=div(d,n);r=d-q*n
 return a+q*i+div(r*i+(n//2 if d>=0 else -(n//2)),n)
rows=read('assets/recovered/metadata/tasks/simple-tasks.json')['rows']
for row in rows:
 if row['operation'] not in modes:continue
 t=Task();mode=modes[row['operation']]
 assert lib.bc_placement_begin(C.byref(t),mode,mapping[row['piece_kind']],row['orientation'],row['profile'],120,90,101,99,row['command_active'])
 seq=t.sequence.contents;record=read(f'assets/recovered/animations/pair-{seq.pair:02d}-list-{seq.list:02d}/sequence.json')
 tokens=[record['initial_frame']['native_global_index']]+[100+d for d in record['delta_indices']]
 events=[];completed=None
 for tick in range(row['completed_call']+1):
  status=lib.bc_placement_tick(C.byref(t),64,dispatch,None);assert status in (0,1)
  if status==1:
   events.append((tick,tokens[t.frame]))
   assert (t.x,t.y)==(interpolate(120,101,t.steps,t.frame),interpolate(90,99,t.steps,t.frame))
  if t.done:completed=tick;break
 assert events==[(x['tick'],x['frame']) for x in row['emitted_frames']],row
 assert completed==row['completed_call'] and (t.anchor_x,t.anchor_y)==(101,99)
 if mode==0:assert (t.x,t.y)==(101,99)
 else:assert t.frame==t.steps-1 # displayed frame deliberately precedes final anchor
 assert lib.bc_placement_tick(C.byref(t),64,dispatch,None)==2
 cases+=1
assert cases==576,cases
for args in [(3,1,0,0,0,0,0,0,False),(0,0,0,0,0,0,0,0,False),(0,1,8,0,0,0,0,0,False),(0,1,0,0,0,0,1025,0,False)]:
 t=Task();assert not lib.bc_placement_begin(C.byref(t),*args);assert lib.bc_placement_tick(C.byref(t),0,dispatch,None)==-1
print(f'PASS: {cases} original placement tasks: frame identities, readiness and completion; source-derived interpolation and final anchor separation.')
