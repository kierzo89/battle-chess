#include "sound.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static bool word(FILE *f,uint32_t *out){unsigned char b[4];if(fread(b,1,4,f)!=4)return false;*out=(uint32_t)b[0]|(uint32_t)b[1]<<8|(uint32_t)b[2]<<16|(uint32_t)b[3]<<24;return true;}
void bc_sound_destroy(BCSoundBank *b){if(!b)return;for(unsigned i=0;i<15;i++)free(b->slots[i].samples);memset(b,0,sizeof *b);}
bool bc_sound_load(BCSoundBank *b,const char *path){
 if(!b||!path)return false;
 memset(b,0,sizeof *b);FILE *f=fopen(path,"rb");if(!f)return false;
 char magic[4];if(fread(magic,1,4,f)!=4||memcmp(magic,"BCA1",4))goto bad;
 for(unsigned i=0;i<15;i++){
  BCSoundSample *s=&b->slots[i];
  if(!word(f,&s->denominator)||!word(f,&s->count)||!s->denominator||s->denominator>32767||!s->count||s->count>1000000)goto bad;
  s->samples=malloc(s->count);if(!s->samples||fread(s->samples,1,s->count,f)!=s->count)goto bad;
  for(unsigned j=0;j<s->count;j++)if(s->samples[j]>15)goto bad;
 }
 if(fgetc(f)!=EOF||ferror(f))goto bad;
 fclose(f);return true;
bad:fclose(f);bc_sound_destroy(b);return false;
}
bool bc_sound_interval(unsigned denominator,int pitch,uint32_t *out){
 if(!denominator||denominator>32767||pitch< -64||pitch>63||!out)return false;
 int64_t value=1000000000/denominator+(int64_t)pitch*1120;*out=value<0?0:(uint32_t)value;return true;
}
size_t bc_sound_frames(const BCSoundSample *s,int pitch,unsigned rate){
 uint32_t interval;
 if(!s||!s->samples||!s->count||s->count>1000000||rate<8000||rate>192000||!bc_sound_interval(s->denominator,pitch,&interval)||!interval)return 0;
 uint64_t duration=(uint64_t)s->count*interval;
 /* At most30 seconds per event, preventing malformed files allocating huge clips. */
 if(duration>30000000000ULL)return 0;
 return (size_t)((duration*rate+999999999)/1000000000);
}
size_t bc_sound_render(const BCSoundSample *s,int pitch,unsigned rate,float *out,size_t capacity){
 size_t count=bc_sound_frames(s,pitch,rate);if(!count||!out||capacity<count)return 0;
 uint32_t interval;if(!bc_sound_interval(s->denominator,pitch,&interval))return 0;
 for(unsigned i=0;i<s->count;i++)if(s->samples[i]>15)return 0;
 for(size_t i=0;i<count;i++){
  uint64_t sample=(uint64_t)i*1000000000/((uint64_t)rate*interval);
  if(sample>=s->count)sample=s->count-1;
  out[i]=((float)s->samples[sample]-7.5f)/30.0f;
 }
 return count;
}
