/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_4f80[];
extern char menu_label_4f8a[];
extern char menu_label_4f96[];
extern char menu_label_4fa0[];
extern char menu_label_4faa[];
extern char menu_label_4fb8[];
extern char menu_label_4fc6[];
extern char menu_label_4fd4[];
extern char menu_label_4fe4[];
extern char menu_label_4ff4[];
MenuItem menu_items_10a8[] = {
    { menu_label_4f80, 8, 0, 0 },
    { menu_label_4f8a, 9, 0, 0 },
    { menu_label_4f96, 17, 0, 0 },
    { menu_label_4fa0, 16, 0, 0 },
    { menu_label_4faa, 12, 0, 0 },
    { menu_label_4fb8, 268, 0, 0 },
    { menu_label_4fc6, 524, 0, 0 },
    { menu_label_4fd4, 13, 0, 0 },
    { menu_label_4fe4, 269, 0, 0 },
    { menu_label_4ff4, 525, 0, 0 },
    { 0, 0, 0, 0 },
};
