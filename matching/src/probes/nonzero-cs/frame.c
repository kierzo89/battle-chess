/* Independent segmented-link control, not a game reconstruction. */
extern int state;
int nearhelper(int value) { return value + state; }
extern int far frame_prefix(int);
int far frame_probe(int value) { return frame_prefix(value) + nearhelper(value); }
int main(void) { return frame_probe(7); }
