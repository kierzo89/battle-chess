/* REA image 8F88. Names are inferred from observed effects, not symbols. */
extern void init_state(void);
extern void update_950d(void);
extern int state_8fde;

void reset_state(void)
{
    init_state();
    update_950d();
    state_8fde = 0;
}
