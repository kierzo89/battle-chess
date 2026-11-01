/* Separate controlled-clock fixture; this time function is not runtime credit. */
typedef unsigned char Byte;
extern int read_bytes_dbe3(Byte *,int);
extern Byte byte_ring_buffer[128],*byte_read_cursor,*byte_write_cursor;
long fixture_now;
unsigned fixture_calls,fixture_output;
long time(long *result)
{
    long now;
    now=fixture_now;fixture_now+=4;fixture_calls++;
    if(result)*result=now;
    return now;
}
void far write_byte_far(unsigned value)
{
    fixture_output=value;
}
int main(void)
{
    Byte guarded[3];
    if(byte_read_cursor||byte_write_cursor||fixture_now||fixture_calls||fixture_output)return 1;
    byte_read_cursor=byte_write_cursor=byte_ring_buffer;
    guarded[0]=165;guarded[1]=102;guarded[2]=90;
    if(read_bytes_dbe3(guarded+1,1)!=-1)return 2;
    if(fixture_calls!=3||fixture_now!=12)return 3;
    if(guarded[0]!=165||guarded[1]!=102||guarded[2]!=90)return 4;
    if(byte_read_cursor!=byte_ring_buffer||byte_write_cursor!=byte_ring_buffer)return 5;
    if(read_bytes_dbe3(guarded+1,0)||fixture_calls!=3)return 6;
    return 0;
}
