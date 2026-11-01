"""Execute unchanged original incremental evaluator against the host adapter.
Original image is a test oracle only; no emulation is linked into the game.
"""
from compare_original_evaluation import *
class SearchEvaluation(C.Structure):_fields_=[('root',Evaluation),('pawn_state',C.c_uint16*(26*2*2))]
lib.bc_search_evaluation_init.argtypes=[C.POINTER(SearchEvaluation),C.POINTER(Evaluation)]
lib.bc_evaluate_delta.argtypes=[C.POINTER(SearchEvaluation),Move,C.c_uint,C.c_uint,C.c_int16,C.c_uint,C.POINTER(C.c_int16)]
lib.bc_evaluate_delta.restype=C.c_bool
p=Position();lib.bc_position_initial(C.byref(p));root=Evaluation();lib.bc_evaluate(C.byref(p),0,C.byref(root))
rows=[]
for side in (0,1):
 mirror=0x70 if side else 0
 cases=[('pawn-quiet',Move(20^mirror,52^mirror,0,6,0)),('capture',Move(6^mirror,37^mirror,0,5,3)),
        ('castle-k',Move(4^mirror,6^mirror,1,1,0)),('castle-q',Move(4^mirror,2^mirror,1,1,0)),
        ('en-passant',Move(68^mirror,85^mirror,1,6,0))]
 for kind in range(2,6):
  cases+=[('promotion',Move(96^mirror,112^mirror,1,kind,0)),('promotion-capture',Move(96^mirror,113^mirror,1,kind,3))]
 for name,move in cases:
  for ply in (0,3,23):
   for best_score in (-512,0,512):
    context=1-side
    state=SearchEvaluation();lib.bc_search_evaluation_init(C.byref(state),C.byref(root))
    # Nonzero, distinct rows expose ordering errors before parent-state copy.
    for i in range(104):state.pawn_state[i]=(17*i+31)%256
    initial=bytes(state.pawn_state)
    delta=C.c_int16();assert lib.bc_evaluate_delta(C.byref(state),move,side,ply,best_score,context,C.byref(delta))
    uc=Uc(UC_ARCH_X86,UC_MODE_16);uc.mem_map(0,0x100000);uc.mem_write(0,image)
    for key,value in [('current_side',side),('opponent',side^1),('history_index',ply),('best',best_score),('temporary',context)]:
     uc.mem_write(BASE+ext['_'+key],struct.pack('<H',value&65535))
    uc.mem_write(BASE+ext['_piece_square'],bytes(root.squares));uc.mem_write(BASE+ext['_pawn_state'],initial)
    for reg,value in [(UC_X86_REG_DS,DS),(UC_X86_REG_ES,DS),(UC_X86_REG_SS,DS),(UC_X86_REG_SP,0xff00),(UC_X86_REG_CS,0xfdf),(UC_X86_REG_IP,0xd25)]:uc.reg_write(reg,value)
    uc.mem_write(BASE+0xff00,struct.pack('<6H',0,0xf000,move.to,move.from_,move.special,move.kind|(move.capture<<8)))
    done=[]
    def stop(u,address,size,data):
     if address==0xf0000:done.append(True);u.emu_stop()
    uc.hook_add(UC_HOOK_CODE,stop);uc.emu_start(0x10b15,0xf0001,count=100000)
    assert done,(name,'no far return')
    observed=struct.unpack('<h',struct.pack('<H',uc.reg_read(UC_X86_REG_AX)))[0]
    assert observed==delta.value,(name,side,ply,best_score,observed,delta.value)
    masks=bytes(uc.mem_read(BASE+ext['_pawn_state'],208));assert masks==bytes(state.pawn_state),(name,'mask state')
    rows.append({'kind':name,'side':side,'ply':ply,'best':best_score,'result':observed,'masks_sha256':hashlib.sha256(masks).hexdigest()})
(ROOT/'native/evidence/incremental-original-comparison.json').write_text(json.dumps({'status':'PASS_ORIGINAL_INCREMENTAL_EVALUATOR','original_exe_sha256':hashlib.sha256(exe).hexdigest(),'procedure_offset':'0x10b15','procedure_sha256':hashlib.sha256(image[0x10b15:0x10b15+538]).hexdigest(),'cases':rows,'scope':'Original evaluator and all called helpers execute unchanged. Only stop sentinel intercepted. Synthetic valid-range move records and seeded pawn histories; not whole-search parity.'},indent=2)+'\n')
print('PASS:',len(rows),'original incremental score + all 208 pawn-state bytes')
