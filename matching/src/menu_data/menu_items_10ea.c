/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
extern char menu_label_5004[];
extern char menu_label_500c[];
extern char menu_label_5016[];
extern char menu_label_5020[];
extern char menu_label_502a[];
extern char menu_label_5034[];
extern char menu_label_503e[];
extern char menu_label_5048[];
extern char menu_label_5052[];
extern char menu_label_505c[];
extern char menu_label_5066[];
MenuItem menu_items_10ea[] = {
    { menu_label_5004, 3, 0, 0 },
    { menu_label_500c, 259, 0, 0 },
    { menu_label_5016, 515, 0, 0 },
    { menu_label_5020, 771, 0, 0 },
    { menu_label_502a, 1027, 0, 0 },
    { menu_label_5034, 1283, 0, 0 },
    { menu_label_503e, 1539, 0, 0 },
    { menu_label_5048, 1795, 0, 0 },
    { menu_label_5052, 2051, 0, 0 },
    { menu_label_505c, 2307, 0, 0 },
    { menu_label_5066, 2563, 0, 0 },
    { 0, 0, 0, 0 },
};
