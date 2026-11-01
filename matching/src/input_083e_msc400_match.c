/* REA input flag branch; the meaning of returned code 0xb082 is unresolved. */
extern char input_flag_0061;
extern void input_reset_e00f();
extern void input_update_0886();
int input_083e()
{
    if (input_flag_0061) {
        input_reset_e00f();
        input_flag_0061 = 0;
        input_update_0886();
        return 0xb082;
    }
    return 0;
}
