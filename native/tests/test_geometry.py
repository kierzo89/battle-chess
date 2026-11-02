import ctypes as C,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[2];lib=C.CDLL(sys.argv[1])
lib.bc_geometry_hit.argtypes=[C.c_bool,C.c_int,C.c_int];lib.bc_geometry_hit.restype=C.c_int
lib.bc_geometry_anchor.argtypes=[C.c_bool,C.c_uint,C.POINTER(C.c_int),C.POINTER(C.c_int)];lib.bc_geometry_anchor.restype=C.c_bool
lib.bc_geometry_frame.argtypes=[C.c_uint]*3;lib.bc_geometry_frame.restype=C.c_uint
e=json.loads((root/'native/evidence/board-geometry.json').read_text());tables=e['tables']
source=(root/'matching/src/probes/board_coordinates_whole_group.c').read_bytes()
assert hashlib.sha256(source).hexdigest()=='bfb7a6e53e5e6ae3565a1edb079e7fea60fd1025393c3f7300a73702cc2f1b82'
s=source.decode();begin=s.index('void board_pointer_0daf(');brace=s.index('{',begin);depth=1;end=brace+1
while depth:
 depth+=(s[end]=='{')-(s[end]=='}');end+=1
function=s[begin:end]
header='''typedef unsigned char Byte;
int (*square_x)[9],*square_y;
unsigned selected_square_0efa,cursor_square_0efc,hover_square_0efe;
int menu_state;Byte marked_square_8dd6,mode_005a,row_mask_9230[8];
unsigned selection_colour_52ce,selection_xor_52cc;
void outline_square_543a(unsigned a,unsigned b){(void)a;(void)b;}
void input_select_11ef_001e(void){}
void input_init_11ef_0000(void){}
'''
footer='''
int hit(int *xs,int *ys,int x,int y){
 square_x=(int (*)[9])xs;square_y=ys;selected_square_0efa=cursor_square_0efc=hover_square_0efe=255;marked_square_8dd6=255;
 for(unsigned i=0;i<8;i++)row_mask_9230[i]=255;
 board_pointer_0daf(x,y);return hover_square_0efe;
}
'''
with tempfile.TemporaryDirectory(prefix='bc-geometry-') as d:
 p=Path(d);(p/'ref.c').write_text(header+function+footer)
 subprocess.run([sys.argv[2],'-shared','-fPIC',str(p/'ref.c'),'-o',str(p/'ref.so')],check=True)
 ref=C.CDLL(str(p/'ref.so'));ref.hit.argtypes=[C.POINTER(C.c_int)]*2+[C.c_int]*2;ref.hit.restype=C.c_int
 for perspective in (False,True):
  suffix='flat' if perspective else 'tilted'
  xs=(C.c_int*81)(*tables['square_x_'+suffix]['values']);ys=(C.c_int*9)(*tables['square_y_'+suffix]['values'])
  for y in range(-1,201):
   for x in range(-1,321):
    original=ref.hit(xs,ys,x,y);expected=-1 if original==255 else (7-(original>>3))*16+(original&7)
    assert lib.bc_geometry_hit(perspective,x,y)==expected,(perspective,x,y)
  for row in range(8):
   for col in range(8):
    sq=(7-row)*16+col;x=C.c_int();y=C.c_int();assert lib.bc_geometry_anchor(perspective,sq,C.byref(x),C.byref(y))
    assert (x.value,y.value)==(tables['screen_x_'+suffix]['values'][row*8+col],tables['screen_y_'+suffix]['values'][row])
    assert lib.bc_geometry_hit(perspective,x.value,y.value)==sq
for side in range(2):
 for kind in range(1,7):
  for row in range(8):
   for col in range(8):assert 17<=lib.bc_geometry_frame(kind,side,row*16+col)<=54
print('PASS: 130088 pixel hit comparisons against recovered pointer C; 128 original anchors; all standing-frame selectors in range.')

# Compare selection to the unchanged recovered queue_piece body with attach
# replaced only by a frame-index observation sink.
source=(root/'matching/src/queue_piece_match.c').read_bytes()
assert hashlib.sha256(source).hexdigest()=='cf929768281d5083f974334333df537ef658fe794f6502793f6f34856a272066'
body=source.decode().split('void queue_piece(',1)[1]
frame=(root/'matching/src/data/frame_index_flat_0166.c').read_text()
frame=frame[frame.index('unsigned char'):]
setup="""typedef unsigned char Byte;
typedef struct {Byte prefix[11];Byte square;Byte rest[16];} Actor;
typedef struct {int words[4];} Frame;
Actor actors[32];Byte cells[64],actor_map[64];Frame frames[100];
int xx[64],yy[8],*screen_x=xx,*screen_y=yy,observed;
void attach_actor(int x,int y,int c,Frame *f,Actor *a){observed=(int)(f-frames);}
"""+frame+'Byte *frame_index=frame_index_flat;\n'
with tempfile.TemporaryDirectory(prefix='bc-standing-') as d:
 p=Path(d);(p/'ref.c').write_text(setup+'void queue_piece('+body)
 subprocess.run([sys.argv[2],'-shared','-fPIC',str(p/'ref.c'),'-o',str(p/'ref.so')],check=True)
 ref=C.CDLL(str(p/'ref.so'));ref.queue_piece.argtypes=[C.c_int]*4
 mapping=[0,2,5,6,1,3,4]
 for side in range(2):
  for kind in range(1,7):
   for row in range(8):
    for col in range(8):
     sq=row*16+col;original_square=(7-row)*8+col
     ref.queue_piece(mapping[kind],(1-side)*64,0,original_square)
     assert lib.bc_geometry_frame(kind,side,sq)==C.c_int.in_dll(ref,'observed').value
print('PASS: 768 standing-frame choices match recovered queue_piece C.')

# Near/red army looks up-board; far/blue army looks down-board.
# Explicit frames prevent the reference bridge from hiding a reversed colour bit.
for kind,near,far in [(1,21,25),(2,41,45),(5,29,31),(6,33,37)]:
 assert lib.bc_geometry_frame(kind,0,4)==near
 assert lib.bc_geometry_frame(kind,1,116)==far
assert lib.bc_geometry_frame(4,0,2)==17
assert lib.bc_geometry_frame(4,1,114)==18
assert lib.bc_geometry_frame(4,0,5)==20
assert lib.bc_geometry_frame(4,1,117)==19
