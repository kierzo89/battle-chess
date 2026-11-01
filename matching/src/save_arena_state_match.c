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
