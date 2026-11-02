#include "audio_output.h"
#include <stdlib.h>
#include <string.h>
bool bc_audio_open(BCAudio *a,const char *path){
 if(!a)return false;
 memset(a,0,sizeof *a);
 if(!bc_sound_load(&a->bank,path))return false;
 if(!SDL_InitSubSystem(SDL_INIT_AUDIO)){bc_sound_destroy(&a->bank);return false;}
 a->initialized=true;SDL_AudioSpec spec={.format=SDL_AUDIO_F32,.channels=1,.freq=48000};
 a->stream=SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK,&spec,NULL,NULL);
 if(!a->stream||!SDL_ResumeAudioStreamDevice(a->stream)){bc_audio_close(a);return false;}return true;
}
void bc_audio_close(BCAudio *a){if(!a)return;if(a->stream)SDL_DestroyAudioStream(a->stream);bc_sound_destroy(&a->bank);if(a->initialized)SDL_QuitSubSystem(SDL_INIT_AUDIO);memset(a,0,sizeof *a);}
void bc_audio_clear(BCAudio *a){if(a&&a->stream)(void)SDL_ClearAudioStream(a->stream);}
void bc_audio_mute(BCAudio *a,bool muted){if(!a)return;a->muted=muted;if(muted)bc_audio_clear(a);}
void bc_audio_pause(BCAudio *a,bool paused){if(!a)return;a->paused=paused;if(a->stream){if(paused)(void)SDL_PauseAudioStreamDevice(a->stream);else(void)SDL_ResumeAudioStreamDevice(a->stream);}}
bool bc_audio_busy(BCAudio *a){return a&&a->stream&&!a->muted&&SDL_GetAudioStreamQueued(a->stream)>0;}
void bc_audio_event(void *ctx,unsigned asset,unsigned colour,int pitch){
 BCAudio *a=ctx;(void)colour; /* The recovered nibble wrapper also ignores colour. */
 if(!a||!a->stream||a->muted)return;
 if(asset>=15){a->rejected++;return;}
 size_t frames=bc_sound_frames(&a->bank.slots[asset],pitch,48000);
 int queued=SDL_GetAudioStreamQueued(a->stream);
 if(!frames||frames>48000*10||queued<0||(size_t)queued+frames*sizeof(float)>48000*10*sizeof(float)){a->rejected++;return;}
 float *data=malloc(frames*sizeof *data);
 if(!data){a->rejected++;return;}
 if(bc_sound_render(&a->bank.slots[asset],pitch,48000,data,frames)==frames&&SDL_PutAudioStreamData(a->stream,data,(int)(frames*sizeof *data))&&SDL_FlushAudioStream(a->stream))a->accepted++;
 else a->rejected++;
 free(data);
}
