extern unsigned storage_access(unsigned,unsigned,unsigned);
extern unsigned storage_toggle(void);
extern unsigned common_probe, storage_guard;
int main(void)
{
    if (storage_access(0,0,0) || storage_access(1,0,0) || common_probe)
        return 1;
    if (storage_access(0,0xA35C,1) != 0xA35C ||
        storage_access(1,0x17E9,1) != 0x17E9) return 2;
    common_probe = 0x613B;
    if (storage_access(0,0,0) != 0xA35C ||
        storage_access(1,0,0) != 0x17E9 || common_probe != 0x613B)
        return 3;
    if (storage_toggle() != 0xB4B5 ||
        storage_access(0,0,0) != 0xA35C || storage_guard != 0x1379)
        return 4;
    return 0;
}
