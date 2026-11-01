/* Asset file state, seek, read, and drive-probe helpers CB50..CC45. */
extern char flag_11b8;
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
