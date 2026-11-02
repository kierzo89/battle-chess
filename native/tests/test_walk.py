"""Replay generated controls against original task machine-code evidence."""
from pathlib import Path
import ctypes as C,json,hashlib,sys
root=Path(__file__).resolve().parents[2];lib=C.CDLL(sys.argv[1])
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(root/path).read_bytes();assert hashlib.sha256(b).hexdigest()==pins[path];return json.loads(b)
class Walk(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_uint),('pair',C.c_uint),('list',C.c_uint),('count',C.c_uint)]
class Clock(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_size_t),('cursor',C.c_size_t),('wait',C.c_uint8),('failed',C.c_bool)]
CB=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_int)
lib.bc_walk_sequence.argtypes=[C.c_uint]*3;lib.bc_walk_sequence.restype=C.POINTER(Walk)
lib.bc_task_ready.argtypes=[C.POINTER(Clock),C.c_bool,C.c_uint,CB,C.c_void_p];lib.bc_task_ready.restype=C.c_bool
mapping={2:1,5:2,6:3,1:4,3:5,4:6};cases=frames=0
for row in read('assets/recovered/metadata/tasks/simple-tasks.json')['rows']:
 if row['operation']!='move' or row['command_active']:continue
 w=lib.bc_walk_sequence(mapping[row['piece_kind']],row['orientation'],row['profile']).contents
 assert (w.pair,w.list)==(row['bank_pair'],row['bank_list'])
 seq=read(f'assets/recovered/animations/pair-{w.pair:02d}-list-{w.list:02d}/sequence.json')
 assert w.count==len(seq['frames'])
 clock=Clock(w.control,w.length,0,0,False);ticks=[];completed=None
 @CB
 def dispatch(ctx,asset,colour,pitch):pass
 for tick in range(row['completed_call']+1):
  if lib.bc_task_ready(C.byref(clock),False,64,dispatch,None):
   if len(ticks)==w.count:completed=tick;break
   ticks.append(tick)
 assert ticks==[f['tick'] for f in row['emitted_frames']]
 assert completed==row['completed_call'] and not clock.failed
 expected=[seq['initial_frame']['native_global_index']]+[100+i for i in seq['delta_indices']]
 assert expected==[f['frame'] for f in row['emitted_frames']]
 cases+=1;frames+=len(ticks)
assert cases==96
print(f'PASS: {cases} walking tasks, {frames} frame identities/readiness timestamps and completion calls match original machine-code evidence.')
