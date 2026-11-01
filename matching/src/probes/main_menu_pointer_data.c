/* Typed initialized pointer DATA proposal; no current canonical credit.
 * Labels and complete item arrays still require independent definitions. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled, reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_5094[], menu_label_509a[];
extern char menu_label_50a0[], menu_label_50aa[];
extern MenuItem menu_items_1066[], menu_items_108a[];
extern MenuItem menu_items_10a8[], menu_items_10ea[];
Menu main_menus_114a[] = {
    { menu_label_5094, menu_items_1066 },
    { menu_label_509a, menu_items_108a },
    { menu_label_50a0, menu_items_10a8 },
    { menu_label_50aa, menu_items_10ea },
    { 0, 0 }
};
