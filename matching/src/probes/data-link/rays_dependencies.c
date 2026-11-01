/* Isolated executable harness for the actual init_rays table consumer. */
Ray rays[239];
void fill_8a96(destination, length, value)
char *destination;
int length, value;
{
    while (length-- > 0) *destination++ = value;
}
int main(void) { init_rays(); return 0; }
