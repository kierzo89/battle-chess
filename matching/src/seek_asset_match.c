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
