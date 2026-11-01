/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_4f52[];
extern char menu_label_4f5e[];
extern char menu_label_4f6a[];
extern char menu_label_4f72[];
MenuItem menu_items_108a[] = {
    { menu_label_4f52, 2, 0, 230 },
    { menu_label_4f5e, 4, 0, 244 },
    { menu_label_4f6a, 5, 0, 242 },
    { menu_label_4f72, 11, 0, 237 },
    { 0, 0, 0, 0 },
};
