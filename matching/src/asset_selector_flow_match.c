/* Complete selector and four genuine neighboring asset helpers. */
extern int asset_file;
extern unsigned char flag_11b8;
extern char asset_name_zero[],asset_name_one[],asset_open_error[],asset_disk_one[],asset_disk_two[];
extern void _dos_getdrive(unsigned *);
extern char *strcat(char *,char *);
extern int close(int),open(char *,int),prompt_1296(char *,int,int);
extern void exit_07f3();
extern void seek_asset(long);
extern int probe_asset_file(char *);
void select_asset_file(int which)
{
 char a[40];unsigned b;unsigned char c;
 _dos_getdrive(&b);a[0]=b+64;a[1]=':';a[2]=0;
 if(!which){strcat(a,asset_name_zero);c=0;}
 else {strcat(a,asset_name_one);c=1;}
 if(c!=flag_11b8) {
  if(asset_file!=-1)close(asset_file);
  if(a[0]>='C') {
   if((asset_file=open(a,0x8000))==-1){prompt_1296(asset_open_error,12,0);exit_07f3(0);}
  }else {
   while(!probe_asset_file(a)) {
    a[0]^=3;
    if(probe_asset_file(a))break;
    if(a[9]=='1'){prompt_1296(asset_disk_one,12,0);continue;}
    else {prompt_1296(asset_disk_two,12,0);continue;}
   }
  }
  flag_11b8=c;
 }
 seek_asset(0L);
}

/* Asset file state, seek, read, and drive-probe helpers CB50..CC45. */
void set_flag_11b8(void){flag_11b8=-1;}
extern int asset_file;
extern long lseek(int,long,int);
extern char asset_seek_error[];
extern void print_error(char *), exit_07f3();
void seek_asset(long offset)
{
    if (lseek(asset_file,offset,0)==-1L) {
        print_error(asset_seek_error);
        exit_07f3();
    }
}
extern int asset_file;
extern int read(int,void *,unsigned);
void read_asset(unsigned char huge *destination,long count)
{
    unsigned char *p;
    unsigned char a[512];
    int b,c;
    while(count) {
        b=count>512L?512L:count;
        read(asset_file,a,b);
        for(c=0,p=a;c!=b;c++)
            *destination++=*p++;
        count-=b;
    }
}

extern int open(char *,int);
extern int far select_asset_drive(int);
int probe_asset_file(char *path)
{
 if(select_asset_drive(*path)) {
  if((asset_file=open(path,0x8000))!=-1)return 1;
 }
 return 0;
}
