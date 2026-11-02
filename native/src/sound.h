#ifndef BC_SOUND_H
#define BC_SOUND_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
typedef struct {uint8_t *samples;uint32_t count,denominator;} BCSoundSample;
typedef struct {BCSoundSample slots[15];} BCSoundBank;
bool bc_sound_load(BCSoundBank *,const char *path);
void bc_sound_destroy(BCSoundBank *);
/* Original C868 integer interval formula, nominal nanosecond interpretation.
 * This does not prove physical PSG calibration/transfer characteristics. */
bool bc_sound_interval(unsigned denominator,int pitch,uint32_t *interval);
/* Linux host mapping: held 4-bit amplitude -> centered linear float PCM,
 * gain1/4. This is explicitly a host adaptation, not a PSG hardware model.
 * Return0 for invalid/zero-period input or insufficient capacity. */
size_t bc_sound_frames(const BCSoundSample *,int pitch,unsigned output_rate);
size_t bc_sound_render(const BCSoundSample *,int pitch,unsigned output_rate,float *out,size_t capacity);
#endif
