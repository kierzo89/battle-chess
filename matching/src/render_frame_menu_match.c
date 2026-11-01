/* REA42A0: composite intersecting actors and present the dirty rectangle. */
typedef unsigned char Byte;
typedef struct {Byte width,height;signed char x,y;char huge *pixels;} Frame;
typedef struct Actor {
    int x,y,old_x,old_y,flag;
    Byte colour,square;
    int left,right,top,bottom;
    Frame *frame;
    void far *resource;
    struct Actor *next;
} Actor;
typedef struct {
    int shift,mode,width,height,source_skip,dest_skip,left_mask,right_mask;
    char huge *destination;
    char huge *source;
    int reserved[3],saved_word;
} Blit;
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
extern void copy_5cb5(int,int,int,int,char far *);
void render_42a0(void)
{
    /* p=top destination, a=output stride, q=pixel width, r=saved left,
       b=source area, s=destination area, f=left destination, v=left clip,
       g=source offset, h=destination offset, i=height, j=right clip,
       k=right gap, l/w=edge masks, n=top clip, o=source stride. */
    int p,q,a,r,b;
    int s;
    register Actor *c;
    int t,d,u,e; /* original frame words with no observed reads/writes */
    register int v;
    int f;
    int w,g,h,i,j,k,l,m,n; /* m is another unread original frame word */
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
 int d;
 MenuItem *e;
 Actor *f;
 MenuItem *g;
 int h,i,j,k;
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
