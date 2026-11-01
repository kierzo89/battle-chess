/* Position editor: palette drag/drop, clear/restore and validate/commit. */
typedef unsigned char Byte;
typedef struct {Byte kind,side;int index;} Cell;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {int x,y,old_x,old_y,flag;Byte colour,square;int left,right,top,bottom;Frame *frame;void far *resource;struct Actor *next;} Actor;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
extern int board_input_0ef2,command_active,waiting_0eee,cursor_kind_0ef4,cursor_colour_9850,cursor_actor_57d0;
extern int selected_square_0efa,pointer_x,pointer_y,current_side;
extern Menu *menus,main_menus_114a[],alternate_menus_115e[];
extern Byte page_mode,cells[],actor_map[],row_mask_9230[8],palette_kinds_0f01[6],editor_piece_map_004c[7],menu_open_0044;
extern Cell board[120];
extern Byte huge *arena_cursor;
extern Actor actors[];
extern Frame frames[];
extern int *screen_x,*screen_y;
extern char no_actor_message_4c00[],clear_board_question_4c12[];
extern void init_surface(void),refresh_panel_1d51(void),reset_graphics_3e4f(void),reset_display_0865(void);
extern void attach_actor(int,int,int,Frame *,Actor *),detach_actor(Actor *),detach_all(void);
extern int obtain_input(void),prompt_1296(char *,int,int);
extern char *validate_editor_8e36(void);
extern void show_error_0d6e(char *),finish_editor_df71(void);
extern void far draw_fce8(int);
void edit_board_08de(void)
{
 /* a=arena cursor, b=input command, c=board cursor; d/e=saved states;
  * f=loop count, g=converted square/palette row/actor index, h=clear index.
  * error is the validation message; i is scoped to a picked-up piece value.
  * All autos are read or passed; no stack padding auto is present. */
 Byte huge *a;
 int b;
 Byte huge *c;
 int d,e,f,g,h;
 char *error;
 board_input_0ef2=1;menus=alternate_menus_115e;
 d=command_active;e=waiting_0eee;
 if(!command_active){command_active=1;init_surface();}
 refresh_panel_1d51();page_mode=1;actors[32].square=0;
 for(f=0;f<6;f++) {
  actors[32].frame=0;
  attach_actor(16,f*24+16,0,frames+16+palette_kinds_0f01[f],&actors[32]);
  actors[32].frame=0;
  attach_actor(304,f*24+16,1,frames+16+palette_kinds_0f01[f],&actors[32]);
 }
 page_mode=0;detach_actor(&actors[32]);reset_graphics_3e4f();reset_display_0865();
 for(f=0;f<8;row_mask_9230[f++]=255);
 a=arena_cursor;c=(Byte huge *)board;
 for(f=0;f<(int)sizeof(board);f++)*a++=*c++;
 for(;;) {
  do{menu_open_0044=1;b=obtain_input();}while(!b);
  switch(b) {
   case 0x1002:
    g=(((selected_square_0efa<<1)&112)^112)|(selected_square_0efa&7);
    if(cursor_kind_0ef4) {
     if(cells[selected_square_0efa])detach_actor(&actors[actor_map[selected_square_0efa]]);
     if(actors[cursor_actor_57d0].frame)detach_actor(&actors[cursor_actor_57d0]);
     attach_actor(screen_x[selected_square_0efa],screen_y[selected_square_0efa>>3],cursor_colour_9850,frames+16+cursor_kind_0ef4,&actors[cursor_actor_57d0]);
     cells[selected_square_0efa]=(cursor_colour_9850<<6)|cursor_kind_0ef4;
     actor_map[selected_square_0efa]=cursor_actor_57d0;
     board[g].side=cursor_colour_9850==0;
     board[g].kind=editor_piece_map_004c[cursor_kind_0ef4];
     cursor_kind_0ef4=0;
    }else if(cells[selected_square_0efa]) {
     register unsigned i;
     i=cells[selected_square_0efa];cursor_kind_0ef4=i&7;cursor_colour_9850=i>>6;
     cursor_actor_57d0=actor_map[selected_square_0efa];cells[selected_square_0efa]=0;board[g].kind=0;
    }
    break;
   case 0x1003:
    if(cursor_kind_0ef4&&actors[cursor_actor_57d0].frame) {
     detach_actor(&actors[cursor_actor_57d0]);cursor_kind_0ef4=0;
    }
    g=(pointer_y-4)/24;
    if(g>=0&&g<=5) {
     if(pointer_x<25&&pointer_x>7){cursor_kind_0ef4=palette_kinds_0f01[g];cursor_colour_9850=0;}
     else if(pointer_x>295&&pointer_x<313){cursor_kind_0ef4=palette_kinds_0f01[g];cursor_colour_9850=1;}
    }
    if(cursor_kind_0ef4) {
     for(g=0;g<32&&actors[g].frame;g++);
     if(g==32){cursor_kind_0ef4=0;show_error_0d6e(no_actor_message_4c00);}
     else {cursor_actor_57d0=g;attach_actor(pointer_x,pointer_y+200,cursor_colour_9850,frames+16+cursor_kind_0ef4,&actors[cursor_actor_57d0]);}
    }
    break;
   case 0x3000:
    if(prompt_1296(clear_board_question_4c12,12,1)==0x1003) {
     detach_all();
     for(f=0;f<64;f++) {
      cells[f]=0;h=(((f<<1)&112)^112)|(f&7);board[h].kind=0;
     }
    }
    break;
   case 0x3002:
    a=arena_cursor;c=(Byte huge *)board;
    for(f=0;f<(int)sizeof(board);f++)*c++=*a++;
    detach_all();cursor_kind_0ef4=0;reset_display_0865();break;
   case 0x3003:
    error=validate_editor_8e36();
    if(error){cursor_kind_0ef4=0;show_error_0d6e(error);}
    else {
     menus=main_menus_114a;cursor_kind_0ef4=0;board_input_0ef2=0;
     command_active=d;waiting_0eee=e;init_surface();reset_graphics_3e4f();reset_display_0865();finish_editor_df71();
     if(waiting_0eee)draw_fce8(current_side);
     menu_open_0044=0;return;
    }
    break;
  }
 }
}
