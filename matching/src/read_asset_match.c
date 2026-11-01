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
