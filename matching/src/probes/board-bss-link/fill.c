extern void *memset(void *,int,unsigned);
void fill_8a96(destination,length,value)
char *destination;
int length,value;
{
 memset(destination,value,length);
}
