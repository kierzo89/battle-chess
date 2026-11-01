typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;
 int left,right,top,bottom;Frame *frame;void far *resource;struct Actor*next;} Actor;
extern Actor actors[];
extern int selected_actor;
extern int cursor_square_0efc,selected_square_0efa,waiting_0eee,saved_input_0ef0,saved_actor_0ef4;
extern Byte saved_cursor_8d0a,input_mode_984e,input_flag_8fe0,actor_flag_9374;
extern void outline_square_543a(int,int),detach_actor(Actor*);
void input_begin_0fb0(void)
{
 outline_square_543a(cursor_square_0efc,0);
 outline_square_543a(selected_square_0efa,0);
 saved_cursor_8d0a=cursor_square_0efc;
 cursor_square_0efc=selected_square_0efa=255;
 if(saved_actor_0ef4 && actors[selected_actor].frame)detach_actor(&actors[selected_actor]);
 actor_flag_9374=saved_actor_0ef4;
 input_mode_984e=waiting_0eee;
 input_flag_8fe0=saved_input_0ef0;
 waiting_0eee=0;saved_input_0ef0=0;saved_actor_0ef4=0;
}
void input_end_102d(void)
{
 cursor_square_0efc=saved_cursor_8d0a;
 outline_square_543a(cursor_square_0efc,28);
 waiting_0eee=input_mode_984e;
 saved_input_0ef0=input_flag_8fe0;
 saved_actor_0ef4=actor_flag_9374;
}
