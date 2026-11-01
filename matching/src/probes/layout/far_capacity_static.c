/* Diagnostic alternative: private uninitialized huge storage with real access. */
static unsigned char huge buffer_70000[70000L];
static unsigned char huge buffer_150000[150000L];
unsigned char huge *get_buffer_70000(void) { return buffer_70000; }
unsigned char huge *get_buffer_150000(void) { return buffer_150000; }
