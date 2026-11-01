/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_4f1c[];
extern char menu_label_4f28[];
extern char menu_label_4f34[];
extern char menu_label_4f3e[];
extern char menu_label_4f4c[];
MenuItem menu_items_1066[] = {
    { menu_label_4f1c, 14, 0, 0 },
    { menu_label_4f28, 15, 0, 0 },
    { menu_label_4f34, 1, 0, 0 },
    { menu_label_4f3e, 18, 0, 0 },
    { menu_label_4f4c, 7, 0, 0 },
    { 0, 0, 0, 0 },
};
