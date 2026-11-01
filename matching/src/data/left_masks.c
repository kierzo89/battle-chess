/* Four 16-bit clipping masks, indexed by the low two pixel-position bits.
 * Constants preserve word bit patterns; the C5 int representation is16 bits. */
int left_masks[4] = {0xffff, 0xff0f, 0xff00, 0x0f00};
