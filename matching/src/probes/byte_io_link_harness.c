/* Target-free execution fixture. The far collector is not the original callee. */
typedef unsigned char Byte;
extern void write_bytes_dbb5(Byte *,int),write_control_1562(void),write_banner_157c(void);
extern int read_bytes_dbe3(Byte *,int),available_bytes_dc91(void);
extern void discard_bytes_dc7f(void);
extern Byte byte_ring_buffer[128],*byte_read_cursor,*byte_write_cursor;
extern Byte control_bytes_0064[4],banner_bytes_4d0e[24];
extern long time(long *);
static Byte captured[256];
static unsigned captured_count,collector_overflow;
void far write_byte_far(unsigned value)
{
    if(captured_count<256) captured[captured_count++]=(Byte)value;
    else collector_overflow=1;
}
int main(void)
{
    Byte payload[5],guarded[7];
    int i;
    if(byte_read_cursor||byte_write_cursor||captured_count||collector_overflow) return 1;
    for(i=0;i<128;i++) if(byte_ring_buffer[i]) return 2;
    if(time(0)<=0) return 3;
    payload[0]=3;payload[1]=17;payload[2]=128;payload[3]=0;payload[4]=255;
    write_bytes_dbb5(payload,5);
    write_control_1562();
    write_banner_157c();
    write_bytes_dbb5(payload,0);
    if(captured_count!=33||collector_overflow) return 4;
    for(i=0;i<5;i++) if(captured[i]!=payload[i]) return 5;
    for(i=0;i<4;i++) if(captured[5+i]!=control_bytes_0064[i]) return 6;
    for(i=0;i<24;i++) if(captured[9+i]!=banner_bytes_4d0e[i]) return 7;
    byte_read_cursor=byte_write_cursor=byte_ring_buffer;
    if(available_bytes_dc91()) return 8;
    byte_read_cursor=byte_ring_buffer+20;byte_write_cursor=byte_ring_buffer+25;
    if(available_bytes_dc91()!=5) return 9;
    byte_read_cursor=byte_ring_buffer+126;byte_write_cursor=byte_ring_buffer+3;
    if(available_bytes_dc91()!=5) return 10;
    byte_ring_buffer[126]=11;byte_ring_buffer[127]=22;
    byte_ring_buffer[0]=33;byte_ring_buffer[1]=44;byte_ring_buffer[2]=55;
    guarded[0]=165;guarded[6]=90;
    for(i=1;i<6;i++)guarded[i]=0;
    if(read_bytes_dbe3(guarded+1,5)) return 11;
    for(i=0;i<5;i++)if(guarded[i+1]!=(i+1)*11) return 12;
    if(guarded[0]!=165||guarded[6]!=90) return 13;
    if(byte_read_cursor!=byte_ring_buffer+3||byte_write_cursor!=byte_ring_buffer+3) return 14;
    if(available_bytes_dc91()) return 15;
    byte_read_cursor=byte_ring_buffer+10;byte_write_cursor=byte_ring_buffer+17;
    if(available_bytes_dc91()!=7) return 16;
    discard_bytes_dc7f();
    if(byte_read_cursor!=byte_write_cursor||available_bytes_dc91()) return 17;
    if(read_bytes_dbe3(guarded+1,0)||guarded[0]!=165||guarded[6]!=90) return 18;
    return 0;
}
