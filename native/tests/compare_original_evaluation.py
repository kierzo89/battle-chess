"""Optional original-code oracle. Unicorn is a TEST dependency, never game runtime.
Only castle_flags is a declared host/history contract; evaluator/math helpers run
unchanged from the original decompressed image. Requires the preserved workspace.
"""
import ctypes as C, hashlib, json, struct, sys
from pathlib import Path
from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE
from unicorn.x86_const import *
ROOT=Path(__file__).resolve().parents[2]
WORK=Path('/home/kierzo/chess')
sys.path.insert(0,str(WORK/'matching'))
from exepack import unpack_exepack
class Cell(C.Structure):_fields_=[('kind',C.c_uint8),('side',C.c_uint8),('index',C.c_int16)]
class Piece(C.Structure):_fields_=[('square',C.c_uint8),('kind',C.c_uint8)]
class Board(C.Structure):_fields_=[('cells',Cell*120),('pieces',(Piece*16)*2),('last',C.c_int16*2),('nonpawn',C.c_int16*2),('side',C.c_uint8)]
class Position(C.Structure):_fields_=[('board',Board),('castle',C.c_uint8*2),('ep',C.c_int16),('halfmove',C.c_uint),('fullmove',C.c_uint)]
class Move(C.Structure):_fields_=[('from_',C.c_uint8),('to',C.c_uint8),('special',C.c_uint8),('kind',C.c_uint8),('capture',C.c_uint8)]
class Moves(C.Structure):_fields_=[('moves',Move*256),('count',C.c_size_t)]
class Evaluation(C.Structure):_fields_=[('values',C.c_int16*6),('squares',C.c_int16*1440),('presence',C.c_uint16*2),('doubled',C.c_uint16*2)]
lib=C.CDLL(str(ROOT/'native/build/libevaluation_oracle.so'))
lib.bc_position_initial.argtypes=[C.POINTER(Position)]
lib.bc_evaluate.argtypes=[C.POINTER(Position),C.c_uint,C.POINTER(Evaluation)]
lib.bc_generate_legal.argtypes=[C.POINTER(Position),C.POINTER(Moves)]
lib.bc_play_unchecked.argtypes=[C.POINTER(Position),Move]
exe=(WORK/'CHESS.EXE').read_bytes()
assert hashlib.sha256(exe).hexdigest()=='c32d4f6bc732b67efa65d55bc5813bc74dcfb52b8616894b57ed7aeeeed2a1cd'
image=unpack_exepack(exe).image
rea=json.loads((ROOT/'native/evidence/rea-evaluator-bytes.json').read_text())
assert bytes.fromhex(rea['normalized_result']['bytes_hex'])==image[0xfe59:0xfe59+2851]
ext=json.loads((ROOT/'matching/mixed_evaluation_units.json').read_text())['full_evaluation_fe59']['externals']
DS=0x5cc2;BASE=DS*16
def compare_full():
    rows=[];p=Position();lib.bc_position_initial(C.byref(p));seed=1988
    for sample in range(24):
     for context in (0,1):
      for side in (0,1):
       p.board.side=side
       expected=Evaluation();lib.bc_evaluate(C.byref(p),context,C.byref(expected))
       uc=Uc(UC_ARCH_X86,UC_MODE_16);uc.mem_map(0,0x100000);uc.mem_write(0,image)
       def word(name,value):uc.mem_write(BASE+ext['_'+name],struct.pack('<H',value&65535))
       for name,value in [('current_side',side),('opponent',side^1),('temporary',context),('history_index',0),('best',0)]:word(name,value)
       uc.mem_write(BASE+ext['_board'],bytes(p.board.cells));uc.mem_write(BASE+ext['_pieces'],bytes(p.board.pieces))
       uc.mem_write(BASE+ext['_piece_square'],bytes(2880));uc.mem_write(BASE+ext['_pawn_state'],bytes(208))
       uc.reg_write(UC_X86_REG_DS,DS);uc.reg_write(UC_X86_REG_ES,DS);uc.reg_write(UC_X86_REG_SS,DS)
       uc.reg_write(UC_X86_REG_SP,0xff00);uc.mem_write(BASE+0xff00,struct.pack('<HH',0,0xf000))
       hits=[];done=[]
       def hook(u,address,size,data):
        if address==0xf0000:done.append(True);u.emu_stop();return
        if address==0x9ad5:
         sp=u.reg_read(UC_X86_REG_SP);ip,cs,s,ptr=struct.unpack('<4H',u.mem_read(BASE+sp,8))
         assert s<2;u.mem_write(BASE+ptr,struct.pack('<H',p.castle[s]));hits.append(s)
         u.reg_write(UC_X86_REG_SP,sp+4);u.reg_write(UC_X86_REG_CS,cs);u.reg_write(UC_X86_REG_IP,ip)
       uc.hook_add(UC_HOOK_CODE,hook)
       uc.reg_write(UC_X86_REG_CS,0xfdf);uc.reg_write(UC_X86_REG_IP,0x69)
       uc.emu_start(0xfe59,0xf0001,count=2000000)
       assert done and hits==[1,0],(done,hits,uc.reg_read(UC_X86_REG_CS),uc.reg_read(UC_X86_REG_IP))
       names=['position_score','phase','endgame','total_material','pawn_material','material_balance']
       observed=[struct.unpack('<h',uc.mem_read(BASE+ext['_'+n],2))[0] for n in names]
       assert observed==list(expected.values),(sample,side,context,observed,list(expected.values))
       squares=bytes(uc.mem_read(BASE+ext['_piece_square'],2880))
       assert squares==bytes(expected.squares),(sample,side,context,'piece-square mismatch')
       masks=struct.unpack('<4H',uc.mem_read(BASE+ext['_pawn_state'],8))
       assert masks==(expected.presence[0],expected.doubled[0],expected.presence[1],expected.doubled[1])
       rows.append({'sample':sample,'side':side,'temporary':context,'values':observed,'piece_square_sha256':hashlib.sha256(squares).hexdigest()})
     p.board.side=sample%2
     for _ in range(3):
      moves=Moves();lib.bc_generate_legal(C.byref(p),C.byref(moves))
      if not moves.count:lib.bc_position_initial(C.byref(p));break
      seed=(1664525*seed+1013904223)&0xffffffff
      lib.bc_play_unchecked(C.byref(p),moves.moves[seed%moves.count])
    report={'status':'PASS_ORIGINAL_EVALUATOR_CONTRACT_COMPARISON','original_exe_sha256':hashlib.sha256(exe).hexdigest(),'rea_evidence_id':rea['evidence_id'],'cases':rows,'contract':'Original castle_flags routine intercepted with supplied position rights; all evaluator/math code executes original bytes. No UI/search/gameplay parity claim.','game_runtime_uses_emulation':False}
    (ROOT/'native/evidence/evaluation-original-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(rows),'original machine-code comparisons: scalars, all 1440 table words and pawn masks')

if __name__=="__main__":compare_full()
