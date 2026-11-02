#include "sidestep.h"
#include "presentation.h"
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
/* Preserve DOS word width and union overlays in unchanged recovered source. */
#define int int16_t
#define huge
#define far
#include "../../matching/src/special_task_probe.c"
#include "../../matching/src/data/step_x.c"
#include "../../matching/src/data/step_y.c"
#undef int
int16_t command_active,motion_x,motion_y;
static unsigned attached;
void interpolate_position_5ebc(int16_t x,int16_t y,int16_t tx,int16_t ty,int16_t count,int16_t step){
 int ox,oy;assert(bc_interpolate(x,y,tx,ty,count,step,&ox,&oy));motion_x=ox;motion_y=oy;
}
void attach_actor(int16_t x,int16_t y,int16_t colour,Frame *f,Actor *a){assert(f==a->frame&&colour==a->colour);a->x=x;a->y=y;attached++;}
int main(void){
 unsigned cases=0;
 for(unsigned d=0;d<8;d++)for(int x=-100;x<=300;x+=40)for(int y=-20;y<=200;y+=22){
  Frame f={0};Actor a={0};a.x=a.old_x=x;a.y=a.old_y=y;a.frame=&f;a.colour=64;
  AnimationTask task={0};task.actor=&a;task.detail.bytes.x=step_x[d][0];task.detail.bytes.y=step_y[d][0];
  BCSidestep t;assert(bc_sidestep_begin(&t,x,y,d));attached=0;
  for(unsigned tick=0;tick<7;tick++){
   int expected=special_task_6bf9(&task),actual=bc_sidestep_tick(&t);
   assert(expected==actual&&a.x==t.x&&a.y==t.y&&a.old_x==t.anchor_x&&a.old_y==t.anchor_y&&a.flag==0);
  }
  assert(t.done&&attached==7);assert(bc_sidestep_tick(&t)==1);cases++;
 }
 BCSidestep t;assert(!bc_sidestep_begin(&t,0,0,8)&&bc_sidestep_tick(&t)==-1);
 printf("PASS: %u neighbouring-piece reactions match unchanged recovered6BF9 C, seven positions, completion and anchors.\n",cases);
}
