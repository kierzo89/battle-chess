#ifndef BC_COMPOSITOR_H
#define BC_COMPOSITOR_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
/* Indexed pixels include original four-pixel row padding. Buffers are owned
 * by the caller. Descriptor width excludes padding; stride is (width+3)&~3. */
typedef struct {unsigned width,height;int x,y;const uint8_t *pixels;size_t length;} BCImage;
/* Preserve original union bounds and XOR, including padded-nibble row spill.
 * Output must not alias inputs. Reject unsupported bounds without publishing
 * an output descriptor; output pixel memory may be touched on failure. */
bool bc_compose(const BCImage *base,const BCImage *delta,uint8_t *pixels,size_t capacity,BCImage *out);
#endif
