/* Recording callbacks only: no hardware audio or sample consumption. */
typedef unsigned char Byte;
extern int recorded_calls,recorded_kind,recorded_length;
extern long recorded_frequency;
extern Byte huge *recorded_cursor;
void far play_audio_10e3(long frequency,int length,Byte huge *cursor)
{
 recorded_calls++;recorded_kind=1;
 recorded_frequency=frequency;recorded_length=length;recorded_cursor=cursor;
}
void far play_audio_alt_10e3(long frequency,int length,Byte huge *cursor)
{
 recorded_calls++;recorded_kind=2;
 recorded_frequency=frequency;recorded_length=length;recorded_cursor=cursor;
}
