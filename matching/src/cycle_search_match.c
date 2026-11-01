typedef unsigned char Byte;
extern int setup_word_934a,waiting_0eee,state_57cc,current_side,modes[2];
extern int view_mode_053a,history_index,setup_word_9844,setup_word_9646,book_choice_offset,ready_9856,temporary;
extern Byte search_active;
extern void search_turn_8061(void),commit_turn_810c(void),empty_82a4(void);
extern void prepare_85c5(void),begin_turn(void),trim_history(void),prepare_hint_8384(void);
extern void select_mode(int),accept_hint_82db(void),step_872a(void),run_search(int),charge_clock_85fd(int);
extern int obtain_input(void);
void computer_cycle_801a(void)
{
 setup_word_934a=0;
 do {
  waiting_0eee=0;
  switch(setup_word_934a) {
  case 0:search_turn_8061();break;
  case 1:commit_turn_810c();break;
  case 2:empty_82a4();break;
  }
 }while(state_57cc==2 && modes[current_side]==1);
 state_57cc=0;
}
void search_turn_8061(void)
{
 prepare_85c5();
 begin_turn();
 trim_history();
 if(view_mode_053a)prepare_hint_8384();
 history_index=0;
 waiting_0eee=0;
 if(!view_mode_053a) {
  setup_word_9844=0;
  run_search(2);
 }else if(book_choice_offset>0) {
  search_active=1;
  select_mode(3);
  setup_word_9844=1;
  accept_hint_82db();
  search_active=0;
  if((modes[0]==modes[1])==1) {
   if(!ready_9856)ready_9856=obtain_input();
   if(ready_9856)step_872a();
  }
 }else {
  setup_word_9844=0;
  run_search(setup_word_9646);
 }
 history_index=-1;
 setup_word_934a=1;
 charge_clock_85fd(temporary);
}
