"""Explicit ABI adaptation of recovered phased search, not a replacement engine."""
import argparse,hashlib,json,re
from pathlib import Path

def generate(root,out):
 pins={r['path']:r['sha256'] for r in json.loads((root/'verification/source-snapshot.json').read_text())['files']}
 path='matching/src/search_engine_a4d4_b9ba_match.c';data=(root/path).read_bytes()
 if hashlib.sha256(data).hexdigest()!=pins[path]:raise ValueError('Unpinned search source')
 s=data.decode()
 def replace(a,b):
  nonlocal s
  if s.count(a)!=1:raise ValueError('Unexpected source shape: '+a)
  s=s.replace(a,b)
 replace('extern void *memcpy(void *,const void *,unsigned);','')
 replace('memcpy(search_frame+1,search_frame,222);','memcpy(search_frame+1,search_frame,sizeof *search_frame);')
 replace('memcpy(b->pv,b->line,192);','memcpy(b->pv,b->line,sizeof b->pv);')
 replace('memcpy(search_frame->line,search_frame->pv,192);','memcpy(search_frame->line,search_frame->pv,sizeof search_frame->pv);')
 replace('if((unsigned char *)search_frame==&packed_pen) exit_07f3(10);',
         'if(search_frame>=frames+25) { exit_07f3(10); search_frame--; return 0; }')
 replace('extern Move history[],history_tail[];','extern Move *history,*history_tail;')
 replace('extern Move initial_move,working_move,search_pair_moves[24][2];',
         'extern Move initial_move,search_pair_moves[24][2];\nextern Move working_pv[24];\n#define working_move working_pv[0]')
 # Original final UI wait is a game-loop responsibility on Linux, not engine work.
 replace('while(!finished && !interrupted) {','while(0) {')
 # Prevent cancellation being cleared during the original guaranteed first iteration.
 replace('if(finished && iteration<=1) interrupted=0;','if(finished && iteration<=1 && !hard_cancelled) interrupted=0;')
 replace('    b=search_frame;\n    a=0;','    b=search_frame;\n    if(host_cancel()) return 1;\n    a=0;')
 s=re.sub(r'\bunsigned char\b','uint8_t',s);s=re.sub(r'\bunsigned\b','uint16_t',s)
 s=re.sub(r'\blong\b','int32_t',s);s=re.sub(r'\bint\b','int16_t',s);s=re.sub(r'\bfar\b','',s)
 # Explicit definitions after declarations; all shared original state per-thread.
 s='\n'.join(line.replace('extern ','extern _Thread_local ',1) if line.startswith('extern ') and '(' not in line else line for line in s.splitlines())
 # Namespace all source global/function symbols, including forward declarations.
 names='''graphics_end evaluate_full graphics_begin search_side search_active current_side interrupted finished ready_9856 input_state search_level position_score iteration best window_limit first_score clock_value limit modes check_state home_pawn pawn_home initial_move working_pv search_pair_moves select_mode prepare_85c4 prepare_85c5 refresh min_i16 abs_i16 obtain_input poll_input accept_input search_frame packed_pen history_index opponent side_piece_counts pieces board history history_tail search_options exit_07f3 store_line attacked_9a50 try_move_ab58 capture_moves_b44a quiet_moves_b5ea stage_b860 stage_b8f4 legal_move setup_search search_moves stop_search search_window search_node state_index state_count state_8d12 move_list advance lowbit run_search paused preferred_move prepare_af87 prune_b2ae apply_9749 update_b383 max_i16 equal_state piece_attacks evaluate_candidate rand count_9bfd repetition_9c34 update_best history_storage piece_counts promote_search_b3e6 move_lookup_tables'''.split()
 pre='#include <stdint.h>\n#include <string.h>\n#include <stdlib.h>\n#include "search.h"\n#include "evaluation.h"\n'
 pre+='\n'.join('#define '+n+' sr_'+n for n in names)+'\n'
 # Frame storage declaration must follow the recovered types and precede functions.
 marker='extern void  graphics_end();'
 if marker not in s:raise ValueError('Type boundary changed')
 s=s.replace(marker,'static _Thread_local SearchFrame frames[26];\nstatic _Thread_local int hard_cancelled;\nstatic int host_cancel(void);\n'+marker)
 adapter=(root/'native/src/search_adapter.inc').read_text()
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(pre+s+'\n'+adapter)
 print('Generated original phased search with explicit host frame/history adapters')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();generate(a.root,a.output)
