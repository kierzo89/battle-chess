#include "sound.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char **argv){
 assert(argc==2);BCSoundBank b;assert(bc_sound_load(&b,argv[1]));unsigned rendered=0,zero=0;
 for(unsigned slot=0;slot<15;slot++)for(int pitch=-64;pitch<=63;pitch++){
  BCSoundSample *s=&b.slots[slot];uint32_t interval;assert(bc_sound_interval(s->denominator,pitch,&interval));
  long long expected=1000000000/s->denominator+(long long)pitch*1120;
  assert(interval==(unsigned)(expected<0?0:expected));
  size_t n=bc_sound_frames(s,pitch,48000);
  if(!interval){assert(!n);zero++;continue;}
  assert(n);float *pcm=malloc(n*sizeof *pcm);assert(pcm);
  assert(!bc_sound_render(s,pitch,48000,pcm,n-1));assert(bc_sound_render(s,pitch,48000,pcm,n)==n);
  for(size_t i=0;i<n;i++){
   uint64_t source=(uint64_t)i*1000000000/((uint64_t)48000*interval);if(source>=s->count)source=s->count-1;
   assert(pcm[i]==((float)s->samples[source]-7.5f)/30.0f&&pcm[i]>=-.25f&&pcm[i]<=.25f);
  }
  free(pcm);rendered++;
 }
 bc_sound_destroy(&b);uint32_t x;assert(!bc_sound_interval(0,0,&x));assert(!bc_sound_interval(1,64,&x));
 printf("PASS:15 authenticated sound slots, %u pitch conversions, %u zero-period inputs explicitly held; complete nominal PCM sample comparisons.\n",rendered,zero);
}
