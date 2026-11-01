/* Update menu enable flags and label markers from current game/search state. */
typedef unsigned char Byte;
typedef struct {char *label;int command;Byte enabled,reserved;} MenuItem;
typedef struct {char *label;MenuItem *items;} Menu;
typedef union {unsigned word;struct{Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Menu *menus;
extern MenuItem menu_items_1066[],menu_items_108a[],menu_items_10a8[],menu_items_10ea[];
extern int refresh_active_0548,mode_8176,command_active,view_mode_053a,modes[2],history_index;
extern Byte animation_busy,search_active;
extern Move history[];
void poll_input(void)
{
 register int i;
 register MenuItem *item;
 {MenuItem *items;
 for(i=0;(items=menus[i].items)!=0;i++) {
  for(item=items;item->label;item++) {
   item->label[0]=' ';
   item->enabled=0;
  }
 }
 }
 menu_items_1066[4].enabled=1;
 menu_items_10a8[0].enabled=1;
 menu_items_10a8[1].enabled=1;
 item=menu_items_10a8+4;i=4;do {(item++)->enabled=1;}while(++i!=10);
 item=menu_items_10ea;i=0;do {(item++)->enabled=1;}while(++i!=11);
 if(refresh_active_0548)menu_items_108a[3].enabled=0;
 else if(!animation_busy) {
  if(search_active)menu_items_108a[0].enabled=1;
  else {
   item=menu_items_1066;i=0;do {(item++)->enabled=1;}while(++i!=4);
   menu_items_108a[1].enabled=(history[history_index+1].detail.bytes.kind!=0);
   menu_items_108a[2].enabled=(history[history_index+2].detail.bytes.kind!=0 && history_index<-1);
   menu_items_108a[3].enabled=1;
   menu_items_10a8[2].enabled=1;
   menu_items_10a8[3].enabled=1;
  }
 }
 if(modes[0]==2 || modes[1]==2) {
  menu_items_108a[1].enabled=0;
  menu_items_108a[2].enabled=0;
 }
 menu_items_10a8[9].enabled=(modes[0]!=2);
 menu_items_10a8[6].enabled=(modes[1]!=2);
 *(mode_8176?menu_items_10a8[0].label:menu_items_10a8[1].label)='+';
 *(command_active?menu_items_10a8[3].label:menu_items_10a8[2].label)='+';
 menu_items_10ea[view_mode_053a].label[0]='+';
 menu_items_10a8[modes[0]+4].label[0]='+';
 menu_items_10a8[modes[1]+7].label[0]='+';
}

/* Selection masks and validation use the same generated move stream. */
extern Move current,state_8d12,initial_move,history_tail[];
extern int history_index;
extern Byte row_mask_9230[8];
extern void fill_8a96(char*,int,int),generate_a348(void),advance(void);
extern int probe_move_86d6(Move);
void select_square_8c26(unsigned from)
{
 fill_8a96((char*)row_mask_9230,8,0);
 ++history_index;
 current=initial_move;
 generate_a348();
 do {
  advance();
  if(state_8d12.detail.bytes.kind && from==state_8d12.from)
   if(!probe_move_86d6(state_8d12))
    row_mask_9230[(state_8d12.to>>4)^7]|=1<<(state_8d12.to&7);
 }while(state_8d12.detail.bytes.kind);
 --history_index;
}
int validate_current_8ca1(void)
{
 current.detail.bytes.kind=0;
 ++history_index;
 generate_a348();
 do {
  advance();
  if(state_8d12.to==current.to && state_8d12.from==current.from){current=state_8d12;break;}
 }while(state_8d12.detail.bytes.kind);
 history_tail[history_index]=initial_move;
 --history_index;
 return current.detail.bytes.kind;
}
