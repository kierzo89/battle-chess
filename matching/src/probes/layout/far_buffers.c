unsigned char far buffer_70000[70000L];
unsigned char far buffer_150000[150000L];
unsigned char marker = 0x5a;
void allocate_probe(void) { marker = buffer_70000[0] + buffer_150000[0]; }
