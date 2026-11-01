unsigned char huge buffer_70000[70000L] = { 0 };
unsigned char huge buffer_150000[150000L] = { 0 };
unsigned char marker = 0x5a;
void allocate_probe(void) { marker = buffer_70000[0] + buffer_150000[0]; }
