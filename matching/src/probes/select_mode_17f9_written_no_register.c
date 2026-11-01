/* Store-backed reconstruction hypothesis. The native function writes both
   long slots but has no authenticated reads of them. Their purpose and any
   relationship to the external 11EF:0000 callee remain unknown. */
extern int input_mode_0046;
extern void far input_select_11ef_001e(void), far input_init_11ef_0000(void);
void select_mode(int mode)
{
 long a,b;
 if(mode!=input_mode_0046) {
  a=-1L;
  b=-1L;
  input_mode_0046=mode;
  if(mode==4) {
   a=-7L;
   b=-24L;
  }
  input_select_11ef_001e();
  input_init_11ef_0000();
 }
}
