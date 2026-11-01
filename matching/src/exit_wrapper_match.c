/* Preserve staged shutdown, including the observed empty stage-three check. */
extern int modes[],init_stage;
extern void write_banner_157c(void);
extern void far restore_mode_10e0d(void);
extern void far restore_input_11066(void);
extern void exit(int);
void exit_07f3(void)
{
    if(modes[0]==2 || modes[1]==2)write_banner_157c();
    if(init_stage>=5)restore_mode_10e0d();
    if(init_stage>=3){}
    if(init_stage>=2)restore_input_11066();
    restore_mode_10e0d();
    exit(10);
}
