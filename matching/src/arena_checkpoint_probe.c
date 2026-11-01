/* Three adjacent reciprocal arena checkpoint operations. */
extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned count_0096,count_0094,frame_count,frame_list_count;
extern unsigned char huge *arena_cursor;
extern int *checkpoint_data_933e, **checkpoint_lists_a84e;
extern unsigned checkpoint_8180,checkpoint_8186,checkpoint_936e,checkpoint_987e;
extern unsigned char huge *checkpoint_arena_9368;

void save_arena_state(void)
{
    checkpoint_data_933e=frame_data_cursor;
    checkpoint_lists_a84e=frame_list_cursor;
    checkpoint_8180=count_0096;
    checkpoint_8186=count_0094;
    checkpoint_936e=frame_count;
    checkpoint_987e=frame_list_count;
    checkpoint_arena_9368=arena_cursor;
}

extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned count_0096,count_0094,frame_count,frame_list_count;
extern unsigned char huge *arena_cursor;
extern int *checkpoint_data_933e, **checkpoint_lists_a84e;
extern unsigned checkpoint_8180,checkpoint_8186,checkpoint_936e,checkpoint_987e;
extern unsigned char huge *checkpoint_arena_9368;

void restore_arena_state(void)
{
    frame_data_cursor=checkpoint_data_933e;
    frame_list_cursor=checkpoint_lists_a84e;
    count_0096=checkpoint_8180;
    count_0094=checkpoint_8186;
    frame_count=checkpoint_936e;
    frame_list_count=checkpoint_987e;
    arena_cursor=checkpoint_arena_9368;
}

extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned count_0096,count_0094,frame_count,frame_list_count;
extern unsigned char huge *arena_cursor;
extern int *active_data_b0ca, **active_lists_b080;
extern unsigned active_95fe,active_8e22,active_a834,active_964e;
extern unsigned char huge *active_arena_9344;

void save_active_arena(void)
{
    active_data_b0ca=frame_data_cursor;
    active_lists_b080=frame_list_cursor;
    active_95fe=count_0096;
    active_8e22=count_0094;
    active_a834=frame_count;
    active_964e=frame_list_count;
    active_arena_9344=arena_cursor;
}
