/* 3B3A: union the current/cached frame bounds and composite both pixel planes.
 * Complete789-byte MSC5 /AS /Zi function reconstruction. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct {
 int shift,mode,width,height,source_skip,dest_skip,left_mask,right_mask;
 char huge *destination;
 char huge *source;
 int reserved[3],saved_word;
} Blit;
typedef struct Actor {
 int x,y,old_x,old_y,flag;
 Byte colour,square;
 int left,right,top,bottom;
 Frame *frame;
 void far *resource;
 struct Actor *next;
} Actor;
extern Actor *actors_head;
extern void draw_actor(int,int,int,Frame *,Actor *);
extern Frame cached_frames[];
extern Blit blit;
extern void fill_5a4f(char huge *,int,char),blit_e57a(void);
void empty_3b2e() {}

void compose_frame_3b3a(register Frame *source,int index,Frame *destination)
{
 /* a: destination pointer; b: unsigned bound; c/d: coordinate deltas;
  * e: cached frame; f: signed pixel offset; g: observed unwritten word;
  * h: cached width. Neutral locals retain the recovered stack slots. */
 char huge *a;
 register unsigned b;
 int c,d;
 Frame *e;
 int f,g;
 Byte h;
 e=&cached_frames[index];
 h=e->width;
 if(h&&e->height) {
  if(e->x<source->x) {
   b=source->x-e->x+h;
   destination->width=source->width>b?source->width:b;
   destination->x=source->x;
  }else {
   b=e->x-source->x+source->width;
   destination->width=e->width>b?e->width:b;
   destination->x=e->x;
  }
  if(e->y<source->y) {
   b=source->y-e->y+e->height;
   destination->height=source->height>b?source->height:b;
   destination->y=source->y;
  }else {
   b=e->y-source->y+source->height;
   destination->height=e->height>b?e->height:b;
   destination->y=e->y;
  }
 }else {
  destination->width=source->width;
  destination->height=source->height;
  destination->x=source->x;
  destination->y=source->y;
 }
 fill_5a4f(destination->pixels,(((unsigned)destination->width+3)>>1)*destination->height,0);
 c=destination->x-source->x;
 d=destination->y-source->y;
 f=((((unsigned)destination->width+3)>>1)&0xfe)*d;
 f+=(c>>1)&0xfffe;
 a=destination->pixels+f;
 blit.height=source->height;
 blit.width=((((((unsigned)source->width+3)>>1)&0xfe)+2)>>1);
 blit.shift=c&3;
 blit.left_mask=-1;blit.right_mask=0;blit.source_skip=-2;
 blit.dest_skip=(((((unsigned)destination->width+3)>>1)&0xfe)-((((unsigned)source->width+3)>>1)&0xfe))-2;
 blit.source=source->pixels;blit.destination=a;
 blit.mode=0;
 blit_e57a();
 if(e->width&&e->height) {
  c=destination->x-e->x;
  d=destination->y-e->y;
  a=destination->pixels+((((unsigned)destination->width+3)>>1)&0xfe)*d+((c>>1)&0xfffe);
  blit.height=e->height;
  blit.width=((((((unsigned)e->width+3)>>1)&0xfe)+2)>>1);
  blit.shift=c&3;
  blit.mode=2;
  blit.left_mask=-1;blit.right_mask=0;blit.source_skip=-2;
  blit.dest_skip=(((((unsigned)destination->width+3)>>1)&0xfe)-((((unsigned)e->width+3)>>1)&0xfe))-2;
  blit.source=e->pixels;blit.destination=a;
  /* The original reads this frame word without an observed assignment. */
  blit.saved_word=g;
  blit_e57a();
 }
}

/* 3E4F: present the complete 160 by200 screen through the existing graphics ABI. */
extern char huge *screen;
extern void far graphics_begin(void);
extern void far graphics_copy(int,int,int,int,char far *);
extern void far graphics_end(void);
void reset_graphics_3e4f(void)
{
 graphics_begin();
 graphics_copy(0,0,160,200,screen);
 graphics_end();
}

void clear_actor_3e81(register Actor *actor)
{
    register Actor **link;
    link = &actors_head;
    while (*link) {
        if (*link == actor) *link = actor->next;
        else link = &(*link)->next;
    }
}

void insert_actor(register int y, register Actor *actor)
{
    Actor **link;
    link = &actors_head;
    while (*link != actor) {
        if (!*link) {
            actor->next = 0;
            *link = actor;
        } else if ((*link)->y >= y) {
            actor->next = *link;
            *link = actor;
        } else
            link = &(*link)->next;
    }
}

void attach_actor(register int x, register int y, int colour, Frame *frame, Actor *actor)
{
    clear_actor_3e81(actor);
    insert_actor(y,actor);
    draw_actor(x,y,colour,frame,actor);
}

void detach_actor(register Actor *actor)
{
    clear_actor_3e81(actor);
    draw_actor(actor->x,actor->y,actor->colour,actor->frame,actor);
    actor->frame = 0;
    actor->square = 0;
}

void detach_all(void)
{
    while (actors_head)
        detach_actor(actors_head);
}

extern int dirty_left,dirty_right,dirty_top,dirty_bottom;
extern Actor *active_actor;
extern void release_frame_3a99(Frame *),mark_region_41a8(int),render_42a0(void);
void draw_actor(register int x,register int y,int colour,Frame *frame,Actor *actor)
{
     /* original frame word has no observed reads/writes */
    Frame *b;
    int c;
    while (y>=200) y-=200;
    dirty_left = -(frame->x-x)>>2;
    dirty_right = (((frame->width+(unsigned)3)&0xfc)-frame->x+x-1)>>2;
    dirty_top = -(frame->y-y);
    dirty_bottom = -(frame->y-frame->height)+y-1;
    actor->left = -(frame->x-x);
    actor->right = ((frame->width+3)&0xfc)+actor->left-1;
    actor->top = dirty_top;
    actor->bottom = dirty_bottom;
    if (b=actor->frame) {
        if (actor->flag) release_frame_3a99(actor->frame);
        c = (actor->x-b->x)>>2;
        if (c<dirty_left) dirty_left=c;
        c = (((b->width+(unsigned)3)&0xfc)-b->x+actor->x-1)>>2;
        if (c>dirty_right) dirty_right=c;
        c = actor->y-b->y;
        if (c<dirty_top) dirty_top=c;
        c = actor->y-b->y+b->height-1;
        if (c>dirty_bottom) dirty_bottom=c;
    } else actor->flag=0;
    if (dirty_left<0) dirty_left=0;
    if (dirty_right>79) dirty_right=79;
    if (dirty_top<0) dirty_top=0;
    if (dirty_bottom>199) dirty_bottom=199;
    actor->x=x;
    actor->y=y;
    actor->old_x=x;
    actor->old_y=y;
    actor->colour=colour!=0;
    actor->frame=frame;
    if (dirty_right>=0 && dirty_left<=79 && dirty_top<=199 && dirty_bottom>=0) {
        if (actor->square==254) {
            mark_region_41a8(1);
            active_actor=actor;
        } else mark_region_41a8(0);
        render_42a0();
    }
}

extern int dirty_left,dirty_right,dirty_top,dirty_bottom;
extern int region_left,region_right,region_width,stride,height;
extern char huge *screen;
extern char huge region_buffer[];
extern Blit blit;
extern char overflow_message[];
extern int error_message(char *);
extern void blit_e57a(void),fill_5a4f(char huge *,int,char);
void mark_region_41a8(register int special)
{
    char huge *a;
    
    region_left = dirty_left << 2;
    region_right = (dirty_right << 2) + 3;
    region_width = region_right - region_left + 1;
    stride = ((dirty_right-dirty_left)<<1)+2;
    height = dirty_bottom-dirty_top+1;
    if (stride*height>3248) {
        error_message(overflow_message);
        return;
    }
    a = screen + (160*dirty_top + (dirty_left<<1));
    blit.left_mask=-1;
    blit.right_mask=-1;
    blit.source_skip=160-stride;
    blit.dest_skip=0;
    blit.source=a;
    blit.destination=region_buffer;
    blit.height=height;
    blit.width=stride>>1;
    blit.shift=0;
    blit.mode=0;
    if (!special) blit_e57a();
    else fill_5a4f(region_buffer,height*stride,0);
}

extern int region_left,region_right,dirty_top,dirty_bottom,stride,height;
extern int left_masks[],right_masks[];
extern Actor *actors_head,*active_actor;
extern Blit blit;
extern char far color_buffer[];
extern char huge region_buffer[];
extern Byte page_mode;
extern void prepare_color_4575(Frame *),blit_e57a(void);
extern void far graphics_begin(void);
extern void far graphics_copy(int,int,int,int,char far *);
extern void far graphics_end(void);
extern void copy_5cb5(int,int,int,int,char huge *);
void render_42a0(void)
{
    /* p=top destination, a=output stride, q=pixel width, r=saved left,
       b=source area, s=destination area, f=left destination, v=left clip,
       g=source offset, h=destination offset, i=height, j=right clip,
       k=right gap, l/w=edge masks, n=top clip, o=source stride. */
    int p,q,a,r,b;
    int s;
    register Actor *c;
     /* original frame words with no observed reads/writes */
    register int v;
    int f;
    int w,g,h,i,j,k,l,n; /* m is another unread original frame word */
    unsigned o;
    b = region_left >> 2;
    for (c=actors_head;c;c=c->next) {
        if (c->left<=region_right && c->right>=region_left &&
            c->top<=dirty_bottom && c->bottom>=dirty_top &&
            (!active_actor || active_actor==c)) {
            if (c->colour) prepare_color_4575(c->frame);
            f=c->left-region_left;
            if (f<0) {v=-f;f=0;w=left_masks[v&3];}
            else {v=0;w=-1;}
            k=region_right-c->right;
            if (k<0) {j=-k;k=0;l=right_masks[j&3];}
            else {j=0;l=(k&3)?0:-1;}
            q=((c->frame->width+3)&0xfc)-j-v;
            a=((q+3)>>1)&~1;
            if (c->left&3) {
                if (!j) a+=2;
                else if (v) a+=2;
            }
            p=c->top-dirty_top;
            if (p<0) {
                n=-p;p=0;
                i=(c->bottom>dirty_bottom)?dirty_bottom-dirty_top+1:c->bottom-dirty_top+1;
            } else {
                n=0;
                i=(c->bottom>dirty_bottom)?dirty_bottom-c->top+1:c->bottom-c->top+1;
            }
            o=(((unsigned)c->frame->width+3)>>1)&0xfe;
            g=((unsigned)(i-1)+n)*o+((v>>1)&~1);
            h=(i+p-1)*stride+((f>>1)&~1);
            if (v&3) h-=2;
            r=((((unsigned)c->frame->width+3)>>1)&0xfe)*c->frame->height;
            s=stride*height;
            blit.left_mask=w;
            blit.right_mask=l;
            blit.source_skip=-(((((unsigned)c->frame->width+3)>>1)&0xfe)+a);
            blit.dest_skip=-(a+stride);
            if (c->colour) blit.source=color_buffer+g;
            else blit.source=c->frame->pixels+g;
            blit.destination=region_buffer+h;
            blit.height=i;
            blit.width=a>>1;
            blit.shift=c->left&3;
            blit.mode=1;
            blit_e57a();
        }
    }
    active_actor=0;
    if (!page_mode) {
        graphics_begin();
        graphics_copy(b<<1,dirty_top,stride,height,region_buffer);
        graphics_end();
    } else copy_5cb5(b<<1,dirty_top,stride,height,region_buffer);
}

extern Frame frames[];
extern Actor actors[];
extern void far *frame_resources[];
extern void prepare_pixels_e8cb(char huge *,int,int),insert_actor(int,Actor *);
void prepare_color_4575(register Frame *frame)
{
 prepare_pixels_e8cb(frame->pixels,(((unsigned)frame->width+3)>>1)&0xfffe,frame->height);
}
void configure_actor_45a2(register int x,register int y,int frame_index,int actor_index)
{
 Frame *a;
 Actor *b;
 a=&frames[frame_index];
 b=&actors[actor_index];
 b->colour=0;
 b->x=x;b->y=y;
 b->left=-(a->x-x);
 b->right=((a->width+3)&252)+b->left-1;
 b->top=-(a->y-y);
 b->bottom=-(a->y-a->height)+y-1;
 b->resource=frame_resources[frame_index];
 b->square=255;
 b->frame=a;
 insert_actor(y+200,b);
}

typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
typedef struct {Byte colour,attribute;char *text;} Text;
extern Menu *menus;
extern Frame frames[];
extern Actor actors[];
extern int menu_positions[],menu_x,menu_y,menu_columns,menu_rows,menu_state,speed_2eb3;
extern Text menu_text;
extern void far graphics_begin(void);
extern void far graphics_end(void);
extern void configure_actor_45a2(int,int,int,int),attach_actor(int,int,int,Frame *,Actor *);
extern void clear_actor_3e81(Actor *),advance_menu_5381(void),draw_menu_row_527e(int,int),draw_text_e915(Text *,int,int);
void build_menu_466b(register int which)
{
 /* a: register loop index; b: label cursor; c: frame; e/g: menu entries;
  * f: actor cursor; k: length/row index; d/h/i/j: unread original words. */
 register int a;
 char *b;
 Frame *c;
 
 MenuItem *e;
 Actor *f;
 MenuItem *g;
 int k;
 graphics_begin();
 menu_text.attribute=9;
 menu_y=25;
 g=e=menus[which].items;
 menu_x=menu_positions[which]-32;
 menu_columns=0;
 while(b=(g++)->label) {
  k=0;
  while(*b++)k++;
  if(k>menu_columns)menu_columns=k;
 }
 menu_columns=(menu_columns>>1)-1;
 if((menu_columns<<4)+menu_x>224)menu_x=224-(menu_columns<<4);
 configure_actor_45a2(menu_x,menu_y,15,32);
 configure_actor_45a2(menu_x,menu_y,16,33);
 for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y,4,a+34);
 if(speed_2eb3<=3000) {
  configure_actor_45a2(menu_x+32,menu_y+23,8,44);
  configure_actor_45a2((menu_columns<<4)+menu_x+48,menu_y+23,10,45);
  configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y+23,9,a+46);
  configure_actor_45a2(menu_x+16,menu_y+23,5,56);
  for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y+23,6,a+58);
 }
 configure_actor_45a2(menu_x,menu_y,0,68);
 configure_actor_45a2((menu_columns<<4)+menu_x+32,menu_y,2,69);
 attach_actor(menu_x,menu_y+200,0,&frames[0],&actors[68]);
 attach_actor((menu_columns<<4)+menu_x+32,menu_y+200,0,&frames[2],&actors[69]);
 attach_actor((menu_columns<<4)+menu_x+32,menu_y+200,0,&frames[16],&actors[33]);
 if(speed_2eb3<=3000) {
  attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
  configure_actor_45a2(menu_x+16,menu_y+23,7,57);
 }
 g=e;
 menu_rows=0;k=0;
 while(b=g->label) {
  advance_menu_5381();
  menu_y+=8;menu_rows++;
  if(speed_2eb3>3000) {
   configure_actor_45a2((menu_columns<<4)+menu_x+48,menu_y+15,10,45);
   configure_actor_45a2(menu_x+32,menu_y+15,8,44);
   attach_actor(menu_x+32,menu_y+215,0,&frames[8],&actors[44]);
   attach_actor((menu_columns<<4)+menu_x+48,menu_y+215,0,&frames[10],&actors[45]);
   draw_menu_row_527e(k++,0);
  }else {
   configure_actor_45a2(menu_x+16,menu_y+23,5,56);
   for(a=0;a<menu_columns;a++) {
    c=&frames[6];f=&actors[a+58];
    f->y=menu_y+23;
    f->top=menu_y-c->y+23;
    f->bottom=menu_y-c->y+c->height+22;
   }
   attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
   menu_text.text=b;
   if(menu_state)menu_text.colour=g->enabled?14:8;
   else menu_text.colour=g->enabled?15:0;
   draw_text_e915(&menu_text,menu_x+36,menu_y+15);
   for(a=0;a<menu_columns;a++) {
    c=&frames[9];f=&actors[a+46];
    f->y=menu_y+23;
    f->top=menu_y-c->y+23;
    f->bottom=menu_y-c->y+c->height+22;
   }
   configure_actor_45a2((menu_columns<<4)+menu_x+48,menu_y+23,10,45);
   configure_actor_45a2(menu_x+32,menu_y+23,8,44);
   configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  }
  g++;
 }
 if(speed_2eb3>3000) {
  configure_actor_45a2(menu_x+16,menu_y+23,5,56);
  configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  for(a=0;a<menu_columns;a++)configure_actor_45a2((a<<4)+menu_x+48,menu_y+23,6,a+58);
  attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
 }
 f=&actors[44];
 for(a=0;a<menu_columns+2;a++) {
  clear_actor_3e81(f);
  (f++)->frame=0;
 }
 graphics_end();
}

extern Menu *menus;
extern Frame frames[];
extern Actor actors[];
extern void far *frame_resources[];
extern int menu_positions[],menu_x,menu_y,menu_columns,menu_rows,menu_state,speed_2eb3;
extern int selected_menu,menu_row_selected,menu_last;
extern Byte palette_mode;
extern Text menu_title_text;
extern void far graphics_begin(void);
extern void far graphics_end(void);
extern void configure_actor_45a2(int,int,int,int),attach_actor(int,int,int,Frame *,Actor *);
extern void clear_actor_3e81(Actor *),detach_actor(Actor *),advance_menu_5381(void),draw_menu_row_527e(int,int),draw_text_e915(Text *,int,int);
extern void restore_region_58b0(int,int,int,int),build_menu_466b(int);
void title_menu_50af(int,int);
void close_menu_4c74(void)
{
 register int a,b;Actor *c;
 graphics_begin();a=32;
 if(speed_2eb3<=3000) {
  while(menu_y>25) {
   advance_menu_5381();menu_y-=8;
   configure_actor_45a2(menu_x+16,menu_y+23,5,56);
   for(b=0;b<menu_columns;b++)configure_actor_45a2((b<<4)+menu_x+48,menu_y+23,6,b+58);
   attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
   configure_actor_45a2(menu_x+16,menu_y+23,7,57);
  }
  configure_actor_45a2(menu_x,menu_y,16,33);
 }
 c=&actors[56];
 for(b=0;b<menu_columns+2;b++){clear_actor_3e81(c);(c++)->frame=0;}
 c=&actors[32];
 for(b=0;b<menu_columns+2;b++){clear_actor_3e81(c);(c++)->frame=0;}
 detach_actor(&actors[68]);detach_actor(&actors[69]);
 if(speed_2eb3>3000)restore_region_58b0(actors[68].left>>2,actors[69].right>>2,actors[69].bottom,actors[57].bottom);
 else {
  actors[33].frame=&frames[16];actors[57].frame=&frames[7];
  attach_actor((menu_columns<<4)+menu_x+32,menu_y+200,0,&frames[16],&actors[33]);
  attach_actor((menu_columns<<4)+menu_x+48,menu_y+223,0,&frames[7],&actors[57]);
  detach_actor(&actors[33]);detach_actor(&actors[57]);
 }
 menu_row_selected=255;graphics_end();
}
void initialize_menu_bar_4e5d(void)
{
 char *a;register Menu *b;Actor *c;register int d;int e,f,g,h;
 graphics_begin();b=menus;d=f=0;h=32;c=&actors[h];
 c->square=255;c->resource=frame_resources[11];c->frame=0;
 attach_actor(d,200,0,&frames[11],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=48;
 while(a=(b++)->label) {
  e=0;while(*a++)e++;e=(e+1)>>1;menu_positions[f++]=d;
  for(g=0;g<e;g++) {
   c->square=255;c->resource=frame_resources[13];
   attach_actor(d,200,0,&frames[13],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=16;
  }
  title_menu_50af(f-1,0);
  if(b->label) {
   c->square=255;c->resource=frame_resources[12];
   attach_actor(d,200,0,&frames[12],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=16;
  }else {
   menu_positions[f++]=d;c->square=255;c->resource=frame_resources[14];
   attach_actor(d,200,0,&frames[14],c);clear_actor_3e81(c);c->frame=0;(c++)->square=0;d+=24;
  }
 }
 menu_last=f-1;graphics_end();
}
int finish_menu_5035(void)
{
 register MenuItem *a;int f;
 graphics_begin();f=0;
 if(selected_menu!=255) {
  if(menu_row_selected!=255) {
   a=&menus[selected_menu].items[menu_row_selected];
   if(a->enabled)f=a->command;
  }
  close_menu_4c74();
 }
 selected_menu=255;restore_region_58b0(0,79,0,23);graphics_end();return f;
}
void title_menu_50af(register int menu,register int active)
{
 graphics_begin();menu_title_text.text=menus[menu].label;
 if(menu_state)menu_title_text.colour=active?9:0;
 else if(palette_mode==3)menu_title_text.colour=active?15:0;
 else menu_title_text.colour=active?12:0;
 draw_text_e915(&menu_title_text,menu_positions[menu],8);graphics_end();
}
void track_menu_512d(register int x,int y)
{
 int a;register int b;int c;
 graphics_begin();
 if(y<16) {
  for(a=0;a<5&&menu_positions[a]<x;a++);
  if(a>0&&a<=menu_last) {
   a--;
   if(a!=selected_menu) {
    if(selected_menu!=255){close_menu_4c74();title_menu_50af(selected_menu,0);selected_menu=255;}
    title_menu_50af(a,1);selected_menu=a;build_menu_466b(a);
   }
  }
 }
 if(selected_menu!=255) {
  if(x>=menu_x+36&&x<(menu_columns<<4)+menu_x+52&&y>=48) {
   b=48;a=0;c=menu_y+31;while(b<c&&b<=y){b+=8;a++;}
   if(b<c) {
    a--;
    if(a!=menu_row_selected) {
     if(menu_row_selected!=255)draw_menu_row_527e(menu_row_selected,0);
     draw_menu_row_527e(a,1);menu_row_selected=a;
    }
   }else if(menu_row_selected!=255){draw_menu_row_527e(menu_row_selected,0);menu_row_selected=255;}
  }else if(menu_row_selected!=255){draw_menu_row_527e(menu_row_selected,0);menu_row_selected=255;}
 }
 graphics_end();
}

extern Menu *menus;
extern Text menu_text;
extern int menu_columns,menu_x,menu_state,selected_menu,menu_phase;
extern Byte menu_blink;
extern Frame frames[];
extern Actor actors[];
extern void far *frame_resources[];
extern void draw_text_e915(Text *,int,int),attach_actor(int,int,int,Frame *,Actor *);
void draw_menu_row_527e(register int row,register int selected)
{
 char *a,*b,*c;
 char line[20];
 c=line+(menu_columns<<1)+3;
 a=line;
 b=menus[selected_menu].items[row].label;
 while(*b)*a++=*b++;
 while(a!=c)*a++=' ';
 *a=0;
 menu_text.text=line;
 if(menus[selected_menu].items[row].enabled) {
  if(!menu_state) {
   menu_text.attribute=selected?0:9;
   menu_text.colour=15;
  }else {
   menu_text.attribute=selected?1:9;
   menu_text.colour=14;
  }
 }else {
  menu_text.attribute=9;
  if(!menu_state)menu_text.colour=0;
  else menu_text.colour=8;
 }
 draw_text_e915(&menu_text,menu_x+36,(row<<3)+48);
}
void advance_menu_5381(void)
{
 Actor *a;
 if(selected_menu!=255) {
  a=&actors[68];
  menu_phase=!menu_phase;
  a->resource=frame_resources[menu_phase];
  attach_actor(a->x,a->y+200,a->colour,&frames[menu_phase],a);
  a++;
  a->resource=frame_resources[menu_phase+2];
  attach_actor(a->x,a->y+200,a->colour,&frames[menu_phase+2],a);
  if(menu_blink++)menu_blink=0;
 }
}

/* Original board-square outline routine. */
extern int (*square_x)[9];
extern int *square_y;
extern int dirty_left,dirty_right,dirty_top,dirty_bottom,region_left,region_width;
extern unsigned adjacent_square;
extern void mark_region_41a8(int),render_42a0(void),select_pen_5b18(unsigned),move_pen_5b3d(int,int),line_pen_5b55(int,int);
void outline_square_543a(unsigned square,unsigned pen)
{
 register int *p;
 register int a;
 /* p=near x-row pointer inSI; a=left top inDI. Compiler reserves their
  * frame slots too. Unread original words b/c/d/f/g/k retain unknown purpose.
  * e=converted adjacent square; h=row; i=top; j=right top; l=column;
  * m=bottom; n=left bottom; o=right bottom. Two CSE words are compiler-made. */
 int e,h,i,j,l,m,n,o;
 if(square<=63) {
  h=square>>3;
  l=square&7;
  p=square_x[h];
  a=p[l]-1;
  j=p[l+1];
  p+=9;
  n=p[l]-1;
  o=p[l+1];
  i=square_y[h];
  m=square_y[h+1]+1;
  dirty_left=(a<n?a:n)>>2;
  dirty_right=(j>o?j:o)>>2;
  dirty_top=i;dirty_bottom=m;
  if(dirty_left<0)dirty_left=0;
  if(dirty_right>79)dirty_right=79;
  if(dirty_top<0)dirty_top=0;
  if(dirty_bottom>199)dirty_bottom=199;
  mark_region_41a8(0);
  if(pen) {
   select_pen_5b18(pen);
   a-=region_left;
   j-=region_left;
   n-=region_left;
   o-=region_left;
   move_pen_5b3d(a,0);
   line_pen_5b55(j,0);
   line_pen_5b55(o,m-i);
   line_pen_5b55(n,m-i);
   line_pen_5b55(a,0);
   move_pen_5b3d(a+1,1);
   line_pen_5b55(j-1,1);
   line_pen_5b55(j-1,0);
   line_pen_5b55(o-1,m-i);
   line_pen_5b55(o-1,m-i-1);
   line_pen_5b55(n+1,m-i-1);
   line_pen_5b55(n+1,m-i);
   line_pen_5b55(a+1,0);
   if(pen&&pen<28&&adjacent_square!=255) {
    select_pen_5b18(28);
    square=((square<<1)&0x70)|(square&7);
    e=((adjacent_square<<1)&0x70)|(adjacent_square&7);
    if(square-1==e||square-17==e) {
     move_pen_5b3d(0,0);line_pen_5b55(a,0);
     move_pen_5b3d(0,1);line_pen_5b55(a,1);
    }
    if(square-1==e||square+15==e) {
     move_pen_5b3d(0,m-i-1);line_pen_5b55(n,m-i-1);
     move_pen_5b3d(0,m-i);line_pen_5b55(n,m-i);
    }
    if(square+1==e||square-15==e) {
     move_pen_5b3d(region_width-1,0);line_pen_5b55(j,0);
     move_pen_5b3d(region_width-1,1);line_pen_5b55(j,1);
    }
    if(square+1==e||square+17==e) {
     move_pen_5b3d(region_width-1,m-i-1);line_pen_5b55(o,m-i-1);
     move_pen_5b3d(region_width-1,m-i);line_pen_5b55(o,m-i);
    }
   }
  }
  render_42a0();
 }
}
