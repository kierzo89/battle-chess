#include "presentation.h"
/* Native adaptation of task_tail_handlers_match.c:task_ready_772d. */
bool bc_task_ready(BCTaskClock *c,bool tilted,unsigned colour,BCSoundEvent event,void *context){
 if(!c||c->failed)return false;
 if(c->wait){c->wait--;return false;}
 if(tilted){c->wait=0;return true;}
 for(;;){
  if(!c->control||c->cursor>=c->length){c->failed=true;return false;}
  uint8_t a=c->control[c->cursor];
  if(a<=127||a==255){
   if(a==255)c->wait=0;
   else {c->wait=a;c->cursor++;}
   return true;
  }
  if(c->length-c->cursor<2){c->failed=true;return false;}
  if(event)event(context,a&15,colour,(int)c->control[c->cursor+1]-64);
  c->cursor+=2;
 }
}
/* board_display_match.c:interpolate_position_5ebc. Wider intermediates avoid
 * host UB; accepted coordinates are bounded to the original screen domain. */
bool bc_interpolate(int x,int y,int tx,int ty,unsigned steps,unsigned step,int *ox,int *oy){
 if(!ox||!oy||!steps||steps>128||step>steps||x< -1024||x>1024||y< -1024||y>1024||tx< -1024||tx>1024||ty< -1024||ty>1024)return false;
 int n=(int)steps,i=(int)step,dx=tx-x,dy=ty-y;
 *ox=(dx/n)*i+((dx%n)*i+(dx>=0?n/2:-n/2))/n+x;
 *oy=(dy/n)*i+((dy%n)*i+(dy>=0?n/2:-n/2))/n+y;
 return true;
}
bool bc_presentation_tick(uint64_t now,uint64_t *last,bool pending){
 if(!last||pending||now<*last||now-*last<2)return false;
 *last=now;return true;
}
