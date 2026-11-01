/* Observable state/call path only; native store-only stack values unresolved. */
extern int input_mode_0046;
extern void far input_select_11ef_001e(void),far input_init_11ef_0000(void);
void select_mode(register int mode)
{
 if(mode!=input_mode_0046) {
  input_mode_0046=mode;
  input_select_11ef_001e();
  input_init_11ef_0000();
 }
}
