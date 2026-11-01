/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_5070[];
extern char menu_label_507e[];
extern char menu_label_508e[];
MenuItem menu_items_1132[] = {
    { menu_label_5070, 12288, 1, 0 },
    { menu_label_507e, 12290, 1, 0 },
    { menu_label_508e, 12291, 1, 0 },
    { 0, 0, 0, 0 },
};
