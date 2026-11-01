extern int asset_file, asset_drive_fallback, asset_drive_count;
extern char asset_drive_file[], asset_drive_error[], asset_drive_second_file[];
extern int open(char *, int), close(int), prompt_1296(char *, int, int);
extern unsigned _bios_equiplist(void);
extern void exit_07f3(int);

void probe_asset_drives(void)
{
    if ((asset_file = open(asset_drive_file, 0x8000)) == -1) {
        prompt_1296(asset_drive_error, 12, 0);
        exit_07f3(0);
    }
    close(asset_file);
    if ((asset_file = open(asset_drive_second_file, 0x8000)) == -1) {
        asset_drive_fallback = 1;
        asset_drive_count = (((unsigned char)_bios_equiplist() & 0xc0) >> 6) + 1;
    } else {
        asset_drive_fallback = 0;
        asset_drive_count = 1;
        close(asset_file);
    }
    asset_file = -1;
}
