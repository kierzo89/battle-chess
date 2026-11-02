"""Compare native capture task endpoints and replay two-actor barriers."""
from pathlib import Path
import ctypes as C,json,hashlib,sys
root=Path(__file__).resolve().parents[2];lib=C.CDLL(sys.argv[1])
pins={r['path']:r['sha256'] for r in json.loads((root/'verification/asset-snapshot.json').read_text())['files']}
def read(path):
 b=(root/path).read_bytes();assert hashlib.sha256(b).hexdigest()==pins[path];return json.loads(b)
class Frame(C.Structure):_fields_=[(n,C.c_uint) for n in ('pair','list','step')]
class Sequence(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_uint),('count',C.c_uint),('frames',C.POINTER(Frame))]
class Clock(C.Structure):_fields_=[('control',C.POINTER(C.c_uint8)),('length',C.c_size_t),('cursor',C.c_size_t),('wait',C.c_uint8),('failed',C.c_bool)]
class Sync(C.Structure):_fields_=[('pending',C.c_uint),('animation_counter',C.c_uint),('registered',C.c_uint),('cleanup',C.c_bool)]
class Task(C.Structure):_fields_=[('sequence',C.POINTER(Sequence)),('clock',Clock),('cursor',C.c_uint),('side',C.c_uint)]+[(n,C.c_bool) for n in ('terminal','done','failed','command_active')]
CB=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_int)
lib.bc_capture_begin.argtypes=[C.POINTER(Task),C.POINTER(Sync)]+[C.c_uint]*4+[C.c_bool];lib.bc_capture_begin.restype=C.c_bool
lib.bc_capture_tick.argtypes=[C.POINTER(Task),C.POINTER(Sync),C.c_uint,CB,C.c_void_p,C.POINTER(Frame)];lib.bc_capture_tick.restype=C.c_int
mapping={2:1,5:2,6:3,1:4,3:5,4:6}
timelines={(r['side'],r['piece_kind'],r['opponent_kind'],r['profile']):r for r in read('assets/recovered/metadata/timing/timelines.json')['capture_sequences']}
@CB
def quiet(ctx,asset,colour,pitch):pass
cases=0
for row in read('assets/recovered/metadata/tasks/capture-tasks.json')['rows']:
 t=Task();s=Sync();f=Frame();right=int(row['side']=='right')
 assert lib.bc_capture_begin(C.byref(t),C.byref(s),right,mapping[row['piece']],mapping[row['opponent']],row['profile'],row['command_active'])
 for _ in range(4):assert lib.bc_capture_tick(C.byref(t),C.byref(s),64,quiet,None,C.byref(f))==0
 assert t.cursor==0 and t.clock.cursor==0 # pending1 must not consume delay/frame
 s.pending=2;events=[];sounds=[];now=0
 @CB
 def dispatch(ctx,asset,colour,pitch):sounds.append((now,asset,colour,pitch))
 for now in range(row['sequence_terminal_call']+1):
  result=lib.bc_capture_tick(C.byref(t),C.byref(s),64,dispatch,None,C.byref(f));assert result in (0,1)
  if result==1:events.append((now,f.pair,f.list,f.step))
 assert t.terminal and s.pending==3 and len(events)==row['frame_count']
 timeline=timelines[row['side'],row['piece'],row['opponent'],row['profile']]
 expected=[(i if row['command_active'] else e['eligible_dispatch_call'],e['bank_pair'],e['list_index'],e['frame_ordinal']) for i,e in enumerate(timeline['frames'])]
 assert events==expected,(row,events,expected)
 if row['command_active']:assert not sounds
 for _ in range(3):assert lib.bc_capture_tick(C.byref(t),C.byref(s),64,quiet,None,C.byref(f))==0
 s.pending=4;assert lib.bc_capture_tick(C.byref(t),C.byref(s),64,quiet,None,C.byref(f))==2
 assert s.animation_counter==4*right and s.cleanup==bool(right and not row['command_active'])
 assert lib.bc_capture_tick(C.byref(t),C.byref(s),64,quiet,None,C.byref(f))==2 and s.animation_counter==4*right
 cases+=1
assert cases==288
# Exercise shared synchronization with actual peers rather than injecting it.
# Both dispatch orders, all engine-kind pairs and both control profiles.
paired=0
for profile in range(2):
 for victim in range(1,7):
  for attacker in range(1,7):
   for order in ((0,1),(1,0)):
    s=Sync();tasks=[Task(),Task()];f=Frame()
    assert lib.bc_capture_begin(C.byref(tasks[0]),C.byref(s),0,victim,attacker,profile,False)
    assert lib.bc_capture_begin(C.byref(tasks[1]),C.byref(s),1,attacker,victim,profile,False)
    for tick in range(2000):
     for i in order:
      status=lib.bc_capture_tick(C.byref(tasks[i]),C.byref(s),i*64,quiet,None,C.byref(f));assert status>=0
      if status==2:assert all(t.terminal for t in tasks)
     if all(t.done for t in tasks):break
    assert all(t.done for t in tasks) and s.pending==4 and s.animation_counter==4 and s.cleanup
    paired+=1
print(f'PASS: {cases} original task cases (frame tuples/timing, terminal calls and cleanup); {paired} dual-actor barrier runs, both dispatch orders.')

s=Sync();a=Task();b=Task()
assert lib.bc_capture_begin(C.byref(a),C.byref(s),0,1,2,0,False)
assert not lib.bc_capture_begin(C.byref(b),C.byref(s),0,1,2,0,False)
assert s.pending==1 and s.registered==1
assert not lib.bc_capture_begin(C.byref(b),C.byref(s),2,1,2,0,False)
assert s.pending==1
print('PASS: duplicate actor registration and invalid side reject without changing shared synchronization.')
