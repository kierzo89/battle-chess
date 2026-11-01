/* Synthetic execution control only; no game storage or matching credit. */
extern int asset_file;
extern int open(char *,int,...),close(int);
extern void read_asset(unsigned char huge *,long);
static unsigned char huge fixture_copy[70000];
int main(void)
{
    unsigned i;
    if(asset_file!=-1)return 1;
    asset_file=open("READ.DAT",0x8000);
    if(asset_file<0)return 2;
    read_asset(fixture_copy+65000L,1234L);
    if(close(asset_file))return 3;
    asset_file=-1;
    for(i=0;i<1234;i++)
        if(fixture_copy[65000L+i]!=(unsigned char)(i*37u+11u))return 4;
    if(fixture_copy[64999L] || fixture_copy[66234L])return 5;
    return 0;
}
