#ifndef BC_STOCKFISH_H
#define BC_STOCKFISH_H
#include "rules.h"
bool bc_uci_fen(const BCPosition *p,char *out,size_t capacity);
void bc_uci_move(BCMove move,char out[6]);
bool bc_uci_parse(const BCPosition *p,const char *text,BCMove *move);
bool bc_stockfish(const BCPosition *initial,const BCPosition *current,const BCMove *history,size_t count,unsigned depth,bool (*cancel)(void *),void *context,BCMove *move,char *error,size_t error_size);
#endif
