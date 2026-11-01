extern int shared_state;
extern int far loc5_prefix(int);
int far loc5_target(int value) { return loc5_prefix(value)+shared_state; }
