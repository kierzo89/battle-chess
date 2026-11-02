#ifndef BC_AUDIO_OUTPUT_H
#define BC_AUDIO_OUTPUT_H
#include "sound.h"
#include <SDL3/SDL.h>
typedef struct {BCSoundBank bank;SDL_AudioStream *stream;bool initialized,muted,paused;unsigned accepted,rejected;} BCAudio;
bool bc_audio_open(BCAudio *,const char *path);
void bc_audio_close(BCAudio *);
void bc_audio_clear(BCAudio *);
void bc_audio_mute(BCAudio *,bool);
void bc_audio_pause(BCAudio *,bool);
bool bc_audio_busy(BCAudio *);
/* BCSoundEvent-compatible. Unsupported records/zero timing are counted and
 * held, never mapped to a different sound or guessed sample rate. */
void bc_audio_event(void *,unsigned asset,unsigned colour,int pitch);
#endif
