/* BB0E: complete3371-byte ordinary-C reconstruction, MSC5 /AS /Zi.
 * Append/begin deliberately have no parameter prototype: original BB0E
 * supplies four/five and three words respectively. Missing trailing fields
 * are an unresolved original caller ABI, not supplied padding arguments. */
typedef unsigned char Byte;
typedef union {unsigned word;struct{Byte kind,capture;} bytes;} MoveKind;
typedef struct {int to,from,flag;MoveKind detail;} Move;
extern Byte animation_busy,record_latch,cells[],capture_types[],animation_done;
extern int current_side,modes[];
extern void record_dfac(Move *);
extern int append_command_5fbd(),begin_command_60d3();
extern void poll_input();
extern int obtain_input(void);
unsigned animation_stage(Move move,int suppress_record)
{
 /* a: chain exists; b: previous square; c: current square; d: destination;
  * e: knight direction; f: capture appearance; g: returned key;
  * h: destination move enabled; i/j/l: command handles; k: path count;
  * m: by-value Move view; n: origin; o: recursive Move;
  * O: polled key; _: direction. Byte locals still occupy aligned slots.
  * Neutral identifiers retain the recovered C5 stack allocation; O and _
  * share the final symbol bucket with o and are deliberately declared first. */
 int a;
 Byte b,c,d,e,f;
 int g;
 Byte h,i,j;
 int k;
 Byte l;
 Move *m;
 Byte n;
 Byte _;
 int O;
 Move o;
 animation_busy=1;
 m=&move;
 if(modes[current_side]==2) {
  if(record_latch||suppress_record)record_latch=0;
  else record_dfac(m);
 }
 e=0;h=1;
 if(m->flag) {
  if(modes[current_side]==2)record_latch=1;
  if(m->detail.bytes.kind==6) {
   o.to=(m->from&112)|(m->to&7);
   g=o.to;
   o.from=m->from;
   o.flag=0;
   o.detail.bytes.kind=m->detail.bytes.kind;
   o.detail.bytes.capture=6;
   animation_stage(o,0);
   animation_busy=1;
   m->from=g;m->flag=0;m->detail.bytes.capture=0;
  }else {
   o.to=m->to;o.from=m->from;o.flag=0;
   o.detail.bytes.kind=m->detail.bytes.kind;o.detail.bytes.capture=0;
   animation_stage(o,0);
   animation_busy=1;
   if((m->to&7)==6) {
    m->to=(m->to&240)|5;m->from=(m->from&240)|7;
   }else {
    m->to=(m->to&240)|3;m->from=m->from&240;
   }
   m->detail.bytes.kind=3;m->detail.bytes.capture=0;
  }
 }
 m->from=(((m->from>>1)&56)^56)|(m->from&7);
 m->to=(((m->to>>1)&56)^56)|(m->to&7);
 n=m->from;c=n;d=m->to;
 if(n==d)return 0;
 if(m->detail.bytes.capture) {
  for(k=0;c!=d;k++) {
   if((c&56)<(d&56))c+=8;
   else if((c&56)>(d&56))c-=8;
   if((c&7)<(d&7))c++;
   else if((c&7)>(d&7))c--;
  }
 }else k=200;
 c=n;a=0;
 if(m->detail.bytes.kind==3) {
  a=1;
  if((n&56)<(d&56))i=begin_command_60d3(6,n,1);
  else if((n&56)==(d&56)&&!(cells[n]&64))i=begin_command_60d3(6,n,1);
  else i=begin_command_60d3(6,n,0);
 }
 if(m->detail.bytes.kind==5) {
  k--;
  if((n&56)<(d&56)) {
   if(((n+8)&56)<(d&56)) {
    if((n&7)<(d&7)){_=2;c++;}else{_=6;c--;}
   }else{_=4;c+=8;}
  }else if(((n-8)&56)>(d&56)) {
   if((n&7)<(d&7)){_=2;c++;}else{_=6;c--;}
  }else{_=0;c-=8;}
  i=begin_command_60d3(2,n,_);
  if(cells[c])l=append_command_5fbd(i,8,c,_);
  e=_;i=append_command_5fbd(i,1,n,c);a=1;
 }
 if((c&56)<(d&56)) {
  if((c&7)<(d&7))_=3;
  else if((c&7)>(d&7))_=5;else _=4;
 }else if((c&56)>(d&56)) {
  if((c&7)<(d&7))_=1;
  else if((c&7)>(d&7))_=7;else _=0;
 }else if((c&7)<(d&7))_=2;
 else if((c&7)>(d&7))_=6;
 if(m->detail.bytes.kind==6) {
  if(_==2)_=1;else if(_==6)_=7;
 }
 if(!a)i=begin_command_60d3(2,n,_);
 else i=append_command_5fbd(i,2,n,_);
 a=1;

 if(k<2) {
  f=capture_types[cells[d]&7];
  if(_==1) {
   if(f==4) {
    i=append_command_5fbd(i,2,d,5);
    j=append_command_5fbd(i,4,d,6);
    j=append_command_5fbd(j,2,d,3);
   }else {
    if(f==3)i=append_command_5fbd(i,6,d,1);
    i=append_command_5fbd(i,2,d,6);
    j=append_command_5fbd(i,4,d,6);
    j=append_command_5fbd(j,2,d,4);
   }
   j=append_command_5fbd(j,7,d,d,0);
  }else {
   if(f==3)i=append_command_5fbd(i,6,d,1);
   else if(f==5)i=append_command_5fbd(i,2,d,4);
   else i=append_command_5fbd(i,2,d,5);
   j=append_command_5fbd(i,7,d,d,0);
  }
  if(f==3||f==5)j=append_command_5fbd(j,2,d,0);
  else j=append_command_5fbd(j,2,d,1);
  j=append_command_5fbd(j,3,d,d);
  j=append_command_5fbd(j,5,d,0);
  k=200;
 }

 while(c!=d) {
  b=c;
  if((c&56)<(d&56))c+=8;
  else if((c&56)>(d&56))c-=8;
  if((c&7)<(d&7))c++;
  else if((c&7)>(d&7))c--;
  if(m->detail.bytes.kind==5) {
   if(cells[c]&&c!=d)l=append_command_5fbd(i,8,c,e);
   if(cells[b])l=append_command_5fbd(i,8,b,(e+4)&7);
  }
  if(!cells[c]||c!=d||_<4||_>6)i=append_command_5fbd(i,1,n,c);
  else h=0;
  k--;

 if(k<2) {
  f=capture_types[cells[d]&7];
  if(_==1) {
   if(f==4) {
    i=append_command_5fbd(i,2,d,5);
    j=append_command_5fbd(i,4,d,6);
    j=append_command_5fbd(j,2,d,3);
   }else {
    if(f==3)i=append_command_5fbd(i,6,d,1);
    i=append_command_5fbd(i,2,d,6);
    j=append_command_5fbd(i,4,d,6);
    j=append_command_5fbd(j,2,d,4);
   }
   j=append_command_5fbd(j,7,d,d,0);
  }else {
   if(f==3)i=append_command_5fbd(i,6,d,1);
   else if(f==5)i=append_command_5fbd(i,2,d,4);
   else i=append_command_5fbd(i,2,d,5);
   j=append_command_5fbd(i,7,d,d,0);
  }
  if(f==3||f==5)j=append_command_5fbd(j,2,d,0);
  else j=append_command_5fbd(j,2,d,1);
  j=append_command_5fbd(j,3,d,d);
  j=append_command_5fbd(j,5,d,0);
  k=200;
 }

 }
 if(m->detail.bytes.capture) {
  f=m->detail.bytes.kind;
  if(h) {
   if(f==3||f==5)i=append_command_5fbd(i,2,n,0);
   else i=append_command_5fbd(i,2,n,1);
  }
  i=append_command_5fbd(i,7,n,d,1);
  if(f==3||f==5){i=append_command_5fbd(i,2,n,4);_=4;}
  else i=append_command_5fbd(i,2,n,5);
  i=append_command_5fbd(i,3,n,n);
  i=append_command_5fbd(i,5,n,1);
  i=append_command_5fbd(i,7,n,d,2);
 }
 if(m->detail.bytes.kind==3) {
  if(_==2||_==6) {
   if(cells[n]&64) {
    i=append_command_5fbd(i,2,n,0);i=append_command_5fbd(i,6,n,2);
   }else {
    i=append_command_5fbd(i,2,n,4);i=append_command_5fbd(i,6,n,3);
   }
  }else if(_==0)i=append_command_5fbd(i,6,n,2);
  else i=append_command_5fbd(i,6,n,3);
 }else if(m->detail.bytes.kind==4) {
  if(_!=0&&_<4) {
   if(cells[n]&64)i=append_command_5fbd(i,2,n,1);
   else i=append_command_5fbd(i,2,n,3);
  }else {
   if(cells[n]&64)i=append_command_5fbd(i,2,n,7);
   else i=append_command_5fbd(i,2,n,5);
  }
 }else {
  if(cells[n]&64)i=append_command_5fbd(i,2,n,0);
  else i=append_command_5fbd(i,2,n,4);
 }
 i=append_command_5fbd(i,3,n,d);
 g=O=0;
 poll_input(1);
 animation_done=0;
 while(!animation_done) {
  O=obtain_input();
  if(O&&!(O&0xf000))g=O;
 }
 animation_busy=0;
 return g;
}
