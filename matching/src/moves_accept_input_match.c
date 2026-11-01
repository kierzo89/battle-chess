/* BAAF: handle search input while the speculative history is unwound. */
extern int interrupted,ready,finished;
extern char input_message[];
extern void unwind_history_b9ba(void),restore_history_ba37(void);
extern void empty_8834(void),process_872a(void),message_1296(char *,int,int);
extern int stop_search(void);
void accept_input(void)
{
 unwind_history_b9ba();
 empty_8834();
 process_872a();
 interrupted=stop_search();
 if(ready) {
  if(finished) {
   if(ready==2)interrupted=1;
   ready=0;
  }else message_1296(input_message,12,0);
 }
 restore_history_ba37();
}
