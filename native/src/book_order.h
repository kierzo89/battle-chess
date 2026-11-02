#ifndef BC_BOOK_ORDER_H
#define BC_BOOK_ORDER_H
#include "rules.h"
/* Original book indexes refer to this pseudo-legal order, NOT legal move order.
 * Retains original 80-entry limit. Check selected moves with bc_play before use.
 * Castling uses host rights/legality; en-passant retains pseudo-legal ordering. */
bool bc_book_order(const BCPosition *p,const BCMove *previous,BCMoveList *out);
#endif
