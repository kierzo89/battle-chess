#include "sidestep.h"
#include "presentation.h"
#include <string.h>
bool bc_direction_step(unsigned direction,int *x,int *y){
 static const int dx[]={0,19,19,19,0,-19,-19,-19},dy[]={-9,-9,0,9,9,9,0,-9};
 if(direction>7||!x||!y)return false;
 *x=dx[direction];*y=dy[direction];return true;
}
bool bc_sidestep_begin(BCSidestep *t,int x,int y,unsigned direction){
 if(!t)return false;
 memset(t,0,sizeof *t);int dx,dy;
 if(!bc_direction_step(direction,&dx,&dy)||x< -1000||x>1000||y< -1000||y>1000){t->failed=true;return false;}
 t->from_x=t->x=t->anchor_x=x;t->from_y=t->y=t->anchor_y=y;t->to_x=x+dx;t->to_y=y+dy;return true;
}
int bc_sidestep_tick(BCSidestep *t){
 if(!t||t->failed)return -1;
 if(t->done)return 1;
 if(!bc_interpolate(t->from_x,t->from_y,t->to_x,t->to_y,6,t->step++,&t->x,&t->y)){t->failed=true;return -1;}
 if(t->step==7){t->done=true;t->anchor_x=t->to_x;t->anchor_y=t->to_y;return 1;}
 return 0;
}
