/* B9BA/BA37: temporarily unwind and restore the searched move history. */
typedef union {unsigned word;struct{unsigned char kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Move history_tail[];
extern int history_index,saved_history_index,current_side,opponent,state_934c;
extern void apply_9749(Move,int),notify_86a1(Move),notify_866d(Move);
void unwind_history_b9ba(void)
{
 int side;
 saved_history_index=history_index;
 while(history_index>0) {
  history_index--;
  side=opponent;opponent=current_side;current_side=side;
  apply_9749(history_tail[history_index],1);
 }
 history_index--;
 if(state_934c)notify_86a1(history_tail[history_index]);
}
void restore_history_ba37(void)
{
 int side;
 if(state_934c)notify_866d(history_tail[history_index+1]);
 history_index++;
 while(history_index<saved_history_index) {
  apply_9749(history_tail[history_index],0);
  side=current_side;current_side=opponent;opponent=side;
  history_index++;
 }
}

/* BAAF: handle search input while the speculative history is unwound. */
extern int interrupted,ready_9856,finished;
extern void unwind_history_b9ba(void),restore_history_ba37(void);
extern void empty_8834(void),step_872a(void);
extern int prompt_1296(char *,int,int);
extern int stop_search(void);
void accept_input(void)
{
 unwind_history_b9ba();
 empty_8834();
 step_872a();
 interrupted=stop_search();
 if(ready_9856) {
  if(finished) {
   if(ready_9856==2)interrupted=1;
   ready_9856=0;
  }else prompt_1296("Jay was wrong #1",12,0);
 }
 restore_history_ba37();
}

void empty_bb01() {}
