typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {Byte colour,attribute;char *text;} Text;
extern int modes[],command_active,menu_enabled_0ef0,pointer_x,pointer_y;
extern Byte remote_status_0063,menu_open_0044,highlight_flash_0057,mode_005a,flash_rank_b0a3,promotion_choices[];
extern Byte *frame_index;
extern Frame frames[];
extern Actor actors[];
extern Text menu_text;
extern char promotion_prompt[];
extern int obtain_input(void);
extern void fill_region_1780(int,int,int,int,int),attach_actor(int,int,int,Frame *,Actor *),clear_actor_3e81(Actor *),draw_text_e915(Text *,int,int),position_command_22c5(int,int),restore_region_58b0(int,int,int,int);
char select_promotion(register int side)
{
 register int y;
 unsigned choice;
 if(modes[side]==2) {
  while(!remote_status_0063)obtain_input();
  choice=remote_status_0063;remote_status_0063=0;
 }else {
  side=side==0;
  y=command_active?300:310;
  actors[32].square=254;
  fill_region_1780(80,60,240,140,0);
  attach_actor(112,y,side,&frames[frame_index[37]],&actors[32]);
  clear_actor_3e81(&actors[32]);actors[32].frame=0;
  attach_actor(144,y,side,&frames[frame_index[25]],&actors[32]);
  clear_actor_3e81(&actors[32]);actors[32].frame=0;
  attach_actor(176,y,side,&frames[frame_index[35]],&actors[32]);
  clear_actor_3e81(&actors[32]);actors[32].frame=0;
  attach_actor(208,y,side,&frames[frame_index[30]],&actors[32]);
  clear_actor_3e81(&actors[32]);actors[32].frame=0;
  actors[32].square=0;
  menu_text.text=promotion_prompt;menu_text.colour=15;menu_text.attribute=0;
  draw_text_e915(&menu_text,96,124);
  menu_open_0044=1;menu_enabled_0ef0=0;highlight_flash_0057=1;flash_rank_b0a3=0;
  if(!mode_005a)position_command_22c5(97,100);
  do {while(obtain_input()!=0x1003) {}}while(pointer_x<96||pointer_x>224||pointer_y<64||pointer_y>120);
  menu_enabled_0ef0=1;
  restore_region_58b0(20,60,60,140);
  menu_open_0044=0;highlight_flash_0057=0;
  choice=promotion_choices[(pointer_x-96)>>5];
 }
 return choice;
}
