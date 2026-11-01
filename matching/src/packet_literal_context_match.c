extern void write_bytes_dbb5(unsigned char *,int);
extern int receive_packet_ddd3(unsigned char *);
extern int prompt_1296(char *,int,int);
void send_packet_dce2(unsigned char *input)
{
    /* e: used packet cursor in SI; d: used checksum count in DI. */
    register unsigned char *e=input;
    /* a attempts, b sum cursor, c checksum, f sum index, g length, h reply. */
    int a;
    unsigned char *b;
    unsigned char c[2];
    register int d;
    int f,g;
    unsigned long h;
    c[0]=0x20;
    c[1]=0x30;
    g=(e[1]-2)&127;
    b=e;
    for(d=g,f=0;d;d--,f^=1)
        c[f]+=*b++;
    write_bytes_dbb5(e,g);
    write_bytes_dbb5(c,2);
    a=0;
    do {
        if(receive_packet_ddd3(e)==-1) {
            h=0x34c604a6L;
            write_bytes_dbb5((unsigned char *)&h,4);
            e[0]=0;
        } else if(e[0]==0xa4) {
            write_bytes_dbb5(e,g);
            write_bytes_dbb5(c,2);
        } else if(e[0]!=0xa5) {
            prompt_1296("Sending at the same time...try again",12,0);
            return;
        }
        a++;
    } while(e[0]!=0xa5 && a<5);
    if(a>=5)prompt_1296("Opponent not responding",12,0);
}

typedef unsigned char Byte;
extern Byte input_reset_state,refresh_stop_11a6;
extern int read_bytes_dbe3(Byte *,int),available_bytes_dc91(void),prompt_1296(char *,int,int);
extern void write_bytes_dbb5(Byte *,int),discard_bytes_dc7f(void);
int receive_packet_ddd3(register Byte *packet)
{
 /* a=consumed byte cursor; b=two additive checksum bytes; c=retry;
    d=checksum count; e=alternating index; f=wire length; g=reply. */
 register Byte *a;
 Byte b[2];
 int c,d,e,f;
 long g;
 do {
  c=0;
  if(read_bytes_dbe3(packet,1)==0) {
   if((packet[0]&0xf0)==0xa0) {
    if(read_bytes_dbe3(packet+1,1)==0) {
     f=packet[1]&0x7f;
     if(f<40) {
      if(read_bytes_dbe3(packet+2,f-2)==0) {
       b[0]=0x20;b[1]=0x30;
       a=packet;
       for(d=f-2,e=0;d;d--,e^=1)
        b[e]+=*a++;
       if(b[0]==a[0]&&b[1]==a[1]) {
        switch(packet[0]) {
        case 0xaa:refresh_stop_11a6=1;break;
        case 0xa6:
         g=input_reset_state?0x34c404a4L:0x34c504a5L;
         write_bytes_dbb5((Byte *)&g,4);
         break;
        default:return 0;
        }
        if(available_bytes_dc91())c=1;
       }else {
        discard_bytes_dc7f();input_reset_state=1;
       }
      }
     }else {
      discard_bytes_dc7f();c=1;
     }
    }
   }else if(packet[0]<128) {
    if(packet[0]!=10) {
     a=packet;
     while(*a!=13) {
      if(*a>=32)a++;
      if(read_bytes_dbe3(a,1)==-1)*a=13;
     }
     *a=0;
     if(packet[0]&&!(packet[0]=='A'&&packet[1]=='T'&&packet[2]=='E'&&packet[3]==0))
      prompt_1296((char *)packet,12,0);
    }
    if(available_bytes_dc91())c=1;
   }else {
    discard_bytes_dc7f();input_reset_state=1;
   }
  }
 }while(c);
 return -1;
}

extern int modes[];
extern void pack_board_8cfa(unsigned char *);
extern void send_packet_dce2(unsigned char *);
void reset_df71(void)
{
    /* a is the consumed cursor; b is the protocol threshold-sized packet. */
    register unsigned char *a;
    unsigned char b[39];
    if(modes[0]==2 || modes[1]==2) {
        a=b;
        *a++=0xa1;
        *a++=0x25;
        pack_board_8cfa(a);
        send_packet_dce2(b);
    }
}

typedef union {unsigned word;struct {Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern void send_packet_dce2(Byte *);

void record_dfac(Move *move)
{
    register Byte *a;
    Byte b[39];
    a=b;
    *a++=0xa2;
    *a++=6;
    *a++=(Byte)move->to;
    *a++=(Byte)move->from;
    send_packet_dce2(b);
}

void record_kind_dfe3(int kind)
{
    register Byte *a;
    Byte b[39];
    a=b;
    *a++=0xa9;
    *a++=5;
    *a++=(Byte)kind;
    send_packet_dce2(b);
}

extern void write_bytes_dbb5(unsigned char *, int);
extern unsigned char input_reset_state;

void input_reset_e00f(void)
{
    unsigned command[2];
    command[0] = 0x04a5;
    command[1] = 0x34c5;
    write_bytes_dbb5((unsigned char *)command, 4);
    input_reset_state = 0;
}
