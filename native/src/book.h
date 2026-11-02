#ifndef BC_BOOK_H
#define BC_BOOK_H
#include "book_order.h"
/* Replay standard-start history and use recovered book scan/weighted selection.
 * draw is the original rand() low four bits. No match leaves output untouched.
 * Never substitutes book indexes into a different generator's ordering. */
bool bc_book_move(const BCPosition *root,const BCMove *history,size_t count,unsigned draw,BCMove *out);
#endif
