"""Generate a width-correct host TU from the retained recovered evaluator.
No edits to matching sources. Transformations are explicit and fail closed.
"""
import argparse,hashlib,json,re
from pathlib import Path

def generate(root,output):
    pins={r['path']:r['sha256'] for r in json.loads((root/'verification/source-snapshot.json').read_text())['files']}
    def read_source(path):
        content=path.read_bytes()
        if hashlib.sha256(content).hexdigest()!=pins.get(path.relative_to(root).as_posix()):
            raise ValueError('Source differs from preserved snapshot: '+str(path))
        return content.decode()
    original=root/'matching/src/full_evaluation_match.c'
    src=read_source(original)
    # All source-side scalar widths are DOS widths, not host C ABI widths.
    def widths(s):
        s=re.sub(r'\bunsigned char\b','uint8_t',s)
        s=re.sub(r'\bunsigned\b','uint16_t',s)
        s=re.sub(r'\blong\b','int32_t',s)
        s=re.sub(r'\bint\b','int16_t',s)
        s=re.sub(r'\bfar\b','',s)
        return s
    names='''move_lookup_tables current_side opponent history_index best temporary
    evaluation_delta castle_bonus piece_value piece_square file_mask pawn_mask pawn_state
    board pieces endgame total_material pawn_material material_balance phase position_score
    pawn_bonus_side center_distance055a pawn_rank_bonus056a passed_rank_bonus057a
    pawn_file_weight058a rank_weight059e castle_95df castle_flags_9ad5 pawn_score
    pawn_bit_count evaluation_abs evaluation_max evaluation_min evaluation_piece
    evaluation_parity evaluate_full evaluation_pawn_remove evaluation_pawn_move evaluate_candidate'''.split()
    prefix='#include <stdint.h>\n#include <string.h>\n#include "evaluation.h"\n'
    prefix+='\n'.join(f'#define {n} ev_{n}' for n in names)+'\n'
    # Variable declarations are thread-local; functions keep normal linkage.
    src='\n'.join(line.replace('extern ','extern _Thread_local ',1)
                  if line.startswith('extern ') and '(' not in line else line
                  for line in src.splitlines())
    src=widths(src)
    globals='''
_Thread_local int16_t current_side,opponent,history_index,best,temporary;
_Thread_local int16_t evaluation_delta;
_Thread_local int16_t piece_square[2][6][120];
_Thread_local uint16_t pawn_mask;
_Thread_local PawnMask pawn_state[26][2];
_Thread_local Cell board[120];
_Thread_local Piece pieces[2][16];
_Thread_local int16_t endgame,total_material,pawn_material,material_balance,phase,position_score;
_Thread_local int16_t pawn_bonus_side;
static _Thread_local uint8_t castle_rights[2];
void castle_flags_9ad5(int16_t side,uint16_t *flags){*flags=castle_rights[side];}
void castle_95df(int16_t to,int16_t *u,int16_t *t) {
 if((to&7)>=4){*u=to-1;*t=to+1;}else{*u=to+1;*t=to-2;}
}
_Static_assert(sizeof(Cell)==4,"16-bit board ABI");
_Static_assert(sizeof(Move)==8,"16-bit move ABI");
_Static_assert(sizeof(PawnMask)==4,"32-bit pawn mask ABI");
'''
    data_files=['evaluation_piece_values.c','evaluation_center_distance.c','evaluation_pawn_rank_bonus.c','evaluation_passed_rank_bonus.c','evaluation_pawn_file_weight.c','evaluation_rank_weight.c','evaluation_file_masks.c','evaluation_castle_bonus.c']
    for name in data_files:
        text=widths(read_source(root/'matching/src/data'/name))
        text=re.sub(r'(?m)^(int16_t|uint16_t) ',r'_Thread_local \1 ',text)
        globals+=text+'\n'
    table=read_source(root/'matching/src/data/move_lookup_tables.c')
    table=table[table.index('MoveLookupTables move_lookup_tables ='):]
    globals+='_Thread_local '+widths(table)+'\n'
    # Undefine globals before accessing identically named fields in host structs.
    cleanup='\n'.join('#undef '+n for n in names)+'\n'
    wrapper='''
void bc_evaluate(const BCPosition *p,unsigned temporary_side,BCEvaluation *out) {
 memset(ev_piece_square,0,sizeof ev_piece_square);
 memset(ev_pawn_state,0,sizeof ev_pawn_state);
 for(int s=0;s<120;s++) {
  ev_board[s].kind=p->board.cells[s].kind;
  ev_board[s].side=p->board.cells[s].side;
  ev_board[s].index=p->board.cells[s].index;
 }
 for(int side=0;side<2;side++)for(int i=0;i<16;i++) {
  ev_pieces[side][i].kind=p->board.pieces[side][i].kind;
  ev_pieces[side][i].square=p->board.pieces[side][i].square;
 }
 ev_current_side=p->board.side;ev_opponent=ev_current_side^1;
 ev_temporary=(int16_t)(temporary_side&1);ev_history_index=0;ev_best=0;
 castle_rights[0]=p->castle[0];castle_rights[1]=p->castle[1];
 ev_evaluate_full();
 out->score=ev_position_score;out->phase=ev_phase;out->endgame=ev_endgame;
 out->total_material=ev_total_material;out->pawn_material=ev_pawn_material;
 out->material_balance=ev_material_balance;
 memcpy(out->piece_square,ev_piece_square,sizeof out->piece_square);
 for(int side=0;side<2;side++) {
  out->pawn_presence[side]=ev_pawn_state[0][side].bits.first;
  out->pawn_doubled[side]=ev_pawn_state[0][side].bits.second;
 }
}
'''
    wrapper += r"""
void bc_search_evaluation_init(BCSearchEvaluation *state,const BCEvaluation *root) {
 memset(state,0,sizeof *state);state->root=*root;
 for(int side=0;side<2;side++) {
  state->pawn_state[0][side][0]=root->pawn_presence[side];
  state->pawn_state[0][side][1]=root->pawn_doubled[side];
 }
}
bool bc_evaluate_delta(BCSearchEvaluation *state,BCMove move,unsigned side,
 unsigned ply,int16_t best_score,unsigned temporary_side,int16_t *delta) {
 if(!state||!delta||side>1||temporary_side>1||ply>23||move.from>=120||move.to>=120||
    (move.from&0x88)||(move.to&0x88)||move.kind<1||move.kind>6||move.capture>6||move.special>1)
  return false;
 if(move.special && move.kind==1) {
  unsigned home=side?116:4;
  if(move.from!=home||(move.to!=home-2&&move.to!=home+2))return false;
 }
 if(move.special && move.kind==6) {
  int target=move.to-(side?-16:16);
  if(target<0||target>=120||(target&0x88))return false;
 }
 memcpy(ev_piece_square,state->root.piece_square,sizeof ev_piece_square);
 memcpy(ev_pawn_state,state->pawn_state,sizeof ev_pawn_state);
 ev_current_side=(int16_t)side;ev_opponent=(int16_t)(side^1);
 ev_history_index=(int16_t)ply;ev_best=best_score;ev_temporary=(int16_t)temporary_side;
 Move candidate={move.to,move.from,move.special,{0}};
 candidate.detail.bytes.kind=move.kind;candidate.detail.bytes.capture=move.capture;
 *delta=ev_evaluate_candidate(candidate);
 memcpy(state->pawn_state,ev_pawn_state,sizeof ev_pawn_state);
 return true;
}
"""
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(prefix+src+globals+cleanup+wrapper)
    print('Generated recovered evaluator with DOS-width scalars and thread-local state')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();generate(a.root,a.output)
