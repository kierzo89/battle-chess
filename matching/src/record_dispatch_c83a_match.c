/* C83A: dispatch three words according to the observed byte mode flag. */
extern unsigned char mode_11aa;
extern void process_c868(int,int,int),process_c924(int,int,int);
void dispatch_c83a(int record,int arg2,int arg3)
{
 if(mode_11aa)process_c924(record,arg2,arg3);
 else process_c868(record,arg2,arg3);
}
