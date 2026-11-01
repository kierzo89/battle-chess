typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_50b0[];
extern MenuItem menu_items_1132[];
Menu alternate_menus_115e[] = {
    { menu_label_50b0, menu_items_1132 },
    { 0, 0 },
};
