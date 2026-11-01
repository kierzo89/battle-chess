/* Synthetic fixture and assertions only; no original allocation ownership. */
typedef unsigned char Byte;
typedef struct {Byte huge *begin,huge *end;unsigned unclassified_word;} AssetCache;
AssetCache asset_frames[3];
int mode_8176;
int recorded_calls,recorded_kind,recorded_length;
long recorded_frequency;
Byte huge *recorded_cursor;
Byte first_fixture[16]={9,0,232,3,17,18,19,20,21,22,23,24,25,91,92,93};
Byte second_fixture[16]={208,7,33,34,35,36,37,38,39,40,41,42,43,44,45,46};
Byte huge boundary_fixture[65552L];
extern void process_c868(int,int,int),process_c924(int,int,int);
extern int puts(char *),printf(char *,...);
typedef union {Byte huge *pointer;struct {unsigned offset,segment;} words;} PointerBits;
void report(void)
{
 PointerBits a;
 a.pointer=recorded_cursor;
 printf("CALL %d %d %ld %d %04x:%04x\n",recorded_calls,recorded_kind,recorded_frequency,recorded_length,a.words.segment,a.words.offset);
}
void report_cache(void)
{
 PointerBits a,b;
 a.pointer=(Byte huge *)&mode_8176;
 printf("ANCHOR %04x:%04x\n",a.words.segment,a.words.offset);
 a.pointer=asset_frames[2].begin;b.pointer=asset_frames[2].end;
 printf("CACHE %04x:%04x %04x:%04x\n",a.words.segment,a.words.offset,b.words.segment,b.words.offset);
}
int main(void)
{
 if(sizeof(AssetCache)!=10)return 1;
 mode_8176=0;recorded_calls=0;
 process_c868(0,1234,7);process_c924(1,-1234,9);
 if(recorded_calls)return 2;
 asset_frames[0].begin=(Byte huge *)first_fixture;
 asset_frames[0].end=asset_frames[0].begin+13;
 asset_frames[1].begin=(Byte huge *)second_fixture;
 asset_frames[1].end=asset_frames[1].begin+11;
 boundary_fixture[65534L]=232;boundary_fixture[65535L]=3;
 boundary_fixture[65536L]=90;boundary_fixture[65537L]=165;
 asset_frames[2].begin=boundary_fixture+65534L;
 asset_frames[2].end=boundary_fixture+65544L;
 report_cache();
 mode_8176=1;
 process_c868(0,1234,5);
 if(recorded_calls!=1||recorded_kind!=1||recorded_frequency!=1005600L||recorded_length!=9||recorded_cursor!=asset_frames[0].begin+4)return 3;
 report();
 process_c868(0,-1234,-1000);
 if(recorded_calls!=2||recorded_kind!=1||recorded_frequency!=0L||recorded_length!=9||recorded_cursor!=asset_frames[0].begin+4)return 4;
 report();
 process_c924(1,2222,2);
 if(recorded_calls!=3||recorded_kind!=2||recorded_frequency!=502240L||recorded_length!=11||recorded_cursor!=asset_frames[1].begin+2)return 5;
 report();
 process_c924(2,-2222,0);
 if(recorded_calls!=4||recorded_kind!=2||recorded_frequency!=1000000L||recorded_length!=10||recorded_cursor!=boundary_fixture+65536L)return 6;
 report();
 if(*recorded_cursor!=90||recorded_cursor[1]!=165)return 7;
 process_c924(2,777,-2000);
 if(recorded_calls!=5||recorded_kind!=2||recorded_frequency!=0L||recorded_length!=10||recorded_cursor!=boundary_fixture+65536L)return 8;
 report();
 first_fixture[2]=24;first_fixture[3]=252;
 process_c868(0,0,1000);
 if(recorded_calls!=6||recorded_kind!=1||recorded_frequency!=120000L||recorded_length!=9||recorded_cursor!=asset_frames[0].begin+4)return 9;
 report();
 first_fixture[2]=184;first_fixture[3]=11;
 process_c868(0,-99,0);
 if(recorded_calls!=7||recorded_kind!=1||recorded_frequency!=333333L||recorded_length!=9||recorded_cursor!=asset_frames[0].begin+4)return 10;
 report();
 puts("AUDIO_ABI_OK: mode gate, 7 callbacks, signed divide, clamp, huge boundary");
 return 0;
}
