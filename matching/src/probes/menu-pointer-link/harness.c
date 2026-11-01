/* Harness-only backing definitions: these are deliberately not original labels
 * or recovered complete MenuItem arrays, and carry no matching credit. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled, reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern Menu main_menus_114a[];
char menu_label_5094[]="fixture-file";
char menu_label_509a[]="fixture-board";
char menu_label_50a0[]="fixture-options";
char menu_label_50aa[]="fixture-help";
MenuItem menu_items_1066[]={{menu_label_5094,11,1,0},{0,0,0,0}};
MenuItem menu_items_108a[]={{menu_label_509a,22,1,0},{0,0,0,0}};
MenuItem menu_items_10a8[]={{menu_label_50a0,33,1,0},{0,0,0,0}};
MenuItem menu_items_10ea[]={{menu_label_50aa,44,1,0},{0,0,0,0}};
static int check(Menu *entry,char *label,MenuItem *items,int command)
{
    return entry->label==label && entry->items==items &&
        items[0].label==label && items[0].command==command &&
        items[0].enabled==1 && items[0].reserved==0 &&
        items[1].label==0 && items[1].command==0 &&
        items[1].enabled==0 && items[1].reserved==0;
}
int main(void)
{
    if (!check(&main_menus_114a[0],menu_label_5094,menu_items_1066,11))return 1;
    if (!check(&main_menus_114a[1],menu_label_509a,menu_items_108a,22))return 2;
    if (!check(&main_menus_114a[2],menu_label_50a0,menu_items_10a8,33))return 3;
    if (!check(&main_menus_114a[3],menu_label_50aa,menu_items_10ea,44))return 4;
    if (main_menus_114a[4].label!=0 || main_menus_114a[4].items!=0)return 5;
    return 0;
}
