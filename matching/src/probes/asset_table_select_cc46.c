/* The two near table selections have independently observed DS offsets.
 * Element layouts and historical source ownership remain unresolved. */
extern unsigned char *asset_table_53f8, *asset_table_8ae4;
extern unsigned char asset_table_2010[], asset_table_2a98[];
extern unsigned char asset_table_11ba[], asset_table_1c62[];

void load_asset_tables(int alternate)
{
    if (alternate) {
        asset_table_53f8 = asset_table_2010;
        asset_table_8ae4 = asset_table_2a98;
    } else {
        asset_table_53f8 = asset_table_11ba;
        asset_table_8ae4 = asset_table_1c62;
    }
}
