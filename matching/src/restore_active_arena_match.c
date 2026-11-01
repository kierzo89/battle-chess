/* Restore the saved active arena cursor and directory state, image2CE0. */
extern int *frame_data_cursor, **frame_list_cursor;
extern unsigned count_0096,count_0094,frame_count,frame_list_count;
extern unsigned char huge *arena_cursor;
extern int *active_data_b0ca, **active_lists_b080;
extern unsigned active_95fe,active_8e22,active_a834,active_964e;
extern unsigned char huge *active_arena_9344;
void restore_active_arena(void)
{
 frame_data_cursor=active_data_b0ca;
 frame_list_cursor=active_lists_b080;
 count_0096=active_95fe;
 count_0094=active_8e22;
 frame_count=active_a834;
 frame_list_count=active_964e;
 arena_cursor=active_arena_9344;
}
