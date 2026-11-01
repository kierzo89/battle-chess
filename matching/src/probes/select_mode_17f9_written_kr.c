/* Same store-backed hypothesis using C4-compatible function syntax.
   Both long values are assigned but unread; purpose and callee use unknown. */
extern int input_mode_0046;
extern void far input_select_11ef_001e(), far input_init_11ef_0000();
void select_mode(mode)
register int mode;
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
