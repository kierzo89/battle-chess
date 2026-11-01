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
