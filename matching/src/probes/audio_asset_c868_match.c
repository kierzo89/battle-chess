typedef unsigned char Byte;
typedef struct {Byte huge *begin, huge *end;unsigned unclassified_word;} AssetCache;
extern AssetCache asset_frames[];
extern int mode_8176;
extern void far play_audio_10e3(long,int,Byte huge *);
void process_c868(int record,int unused_channel,int pitch)
{
 long a;
 int b,c;
 Byte huge *d;
 if(mode_8176) {
  d=(Byte huge *)asset_frames[record].begin;
  c=*(int huge *)d;b=*(int huge *)(d+2);
  a=1000000000L;
  a/=b;
  a+=((long)pitch<<2)*280L;
  if(a<0)a=0;
  play_audio_10e3(a,c,asset_frames[record].begin+4);
 }
}
