/* Typed asset index selection, surface reset, and background delta decode. */
typedef unsigned char Byte;
typedef struct { unsigned long directory, pixels; } AssetLocation;
extern AssetLocation far *setup_offsets, far *setup_lengths;
extern unsigned long far *asset_offsets, far *asset_lengths;
extern unsigned long far *startup_offsets_9648, far *startup_lengths_a8b6;
extern AssetLocation far *pair_offsets, far *pair_directory_lengths;
extern AssetLocation far setup_offsets_data[],far setup_lengths_data[];
extern unsigned long far asset_offsets_data[],far asset_lengths_data[];
extern unsigned long far startup_offsets_data[],far startup_lengths_data[];
extern AssetLocation far pair_offsets_data[],far pair_lengths_data[];
extern unsigned selected_square_0efa,cursor_square_0efc;
extern Byte asset_state[14],palette_mode;
extern int command_active;
extern Byte frame_directory[];
extern int *screen_y,*screen_x,*square_y,(*square_x)[9];
extern Byte *frame_index;
extern int screen_y_flat[],screen_x_flat[],square_y_flat[],square_x_flat[][9];
extern int screen_y_tilted[],screen_x_tilted[],square_y_tilted[],square_x_tilted[][9];
extern Byte frame_index_flat[],frame_index_tilted[];
extern Byte huge *screen;
extern void outline_square_543a(unsigned,unsigned),detach_all(void),restore_arena_state(void);
extern void select_asset_file(int),seek_asset(unsigned long),read_asset(Byte huge *,unsigned long);
extern void prepare_asset_decode(void),decode_frame_directory(Byte *);
extern long huff_frame_decode(Byte huge *,long);
extern void cache_asset_frame(int),reset_graphics_3e4f(void);
void configure_game(register int frame);

void setup_assets(void)
{
 setup_offsets=setup_offsets_data;
 asset_offsets=asset_offsets_data;
 startup_offsets_9648=startup_offsets_data;
 pair_offsets=pair_offsets_data;
 setup_lengths=setup_lengths_data;
 asset_lengths=asset_lengths_data;
 startup_lengths_a8b6=startup_lengths_data;
 pair_directory_lengths=pair_lengths_data;
}

void init_surface(void)
{
 register int i,mode;
 outline_square_543a(cursor_square_0efc,0);
 outline_square_543a(selected_square_0efa,0);
 cursor_square_0efc=255;
 selected_square_0efa=255;
 detach_all();
 restore_arena_state();
 i=0;goto test_first;
 first:asset_state[i++]=0;
 test_first:if(i<6)goto first;
 i=0;goto test_second;
 second:asset_state[6+i++]=255;
 test_second:if(i<8)goto second;
 if(command_active) {
  select_asset_file(0);
  mode=!palette_mode?3:2;
  seek_asset(setup_offsets[mode].directory);
  read_asset(frame_directory,setup_lengths[mode].directory);
  prepare_asset_decode();
  decode_frame_directory(frame_directory);
  screen_y=screen_y_tilted;screen_x=screen_x_tilted;
  square_y=square_y_tilted;square_x=square_x_tilted;
  frame_index=frame_index_tilted;
  configure_game(1);
 }else {
  select_asset_file(0);
  seek_asset(setup_offsets[0].directory);
  read_asset(frame_directory,setup_lengths[0].directory);
  prepare_asset_decode();
  decode_frame_directory(frame_directory);
  screen_y=screen_y_flat;screen_x=screen_x_flat;
  square_y=square_y_flat;square_x=square_x_flat;
  frame_index=frame_index_flat;
  configure_game(0);
  cache_asset_frame(10);
  cache_asset_frame(9);
 }
}

void configure_game(register int frame)
{
 /* a=source, b=next delta row, c=bytes left. Every local is used. */
 Byte huge *a,huge *b;
 long c;
 select_asset_file(0);
 if(!frame&&!palette_mode)frame=7;
 seek_asset(startup_offsets_9648[frame]);
 prepare_asset_decode();
 huff_frame_decode(screen,32000L);
 a=screen;
 b=a+160;
 for(c=31840L;c;--c,a++,b++)
  *b^=*a;
 reset_graphics_3e4f();
}
