typedef unsigned char Byte;
typedef struct { char *label; int command; Byte enabled,reserved; } MenuItem;
typedef struct { char *label; MenuItem *items; } Menu;
/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
MenuItem menu_items_1066[] = {
    { " Load Game", 14, 0, 0 },
    { " Save Game", 15, 0, 0 },
    { " New Game", 1, 0, 0 },
    { " Setup Board", 18, 0, 0 },
    { " Quit", 7, 0, 0 },
    { 0, 0, 0, 0 },
};
/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
MenuItem menu_items_108a[] = {
    { " Force Move", 2, 0, 230 },
    { " Take Back", 4, 0, 244 },
    { " Replay", 5, 0, 242 },
    { " Suggest Move", 11, 0, 237 },
    { 0, 0, 0, 0 },
};
/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
MenuItem menu_items_10a8[] = {
    { " Sound On", 8, 0, 0 },
    { " Sound Off", 9, 0, 0 },
    { " 3D Board", 17, 0, 0 },
    { " 2D Board", 16, 0, 0 },
    { " Human -- Red", 12, 0, 0 },
    { " I.B.M -- Red", 268, 0, 0 },
    { " Modem -- Red", 524, 0, 0 },
    { " Human -- Blue", 13, 0, 0 },
    { " I.B.M -- Blue", 269, 0, 0 },
    { " Modem -- Blue", 525, 0, 0 },
    { 0, 0, 0, 0 },
};
/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
MenuItem menu_items_10ea[] = {
    { " Novice", 3, 0, 0 },
    { " Level 1", 259, 0, 0 },
    { " Level 2", 515, 0, 0 },
    { " Level 3", 771, 0, 0 },
    { " Level 4", 1027, 0, 0 },
    { " Level 5", 1283, 0, 0 },
    { " Level 6", 1539, 0, 0 },
    { " Level 7", 1795, 0, 0 },
    { " Level 8", 2051, 0, 0 },
    { " Level 9", 2307, 0, 0 },
    { " Set Time", 2563, 0, 0 },
    { 0, 0, 0, 0 },
};
/* Complete sentinel-terminated MenuItem array; reserved bytes preserved as observed. */
MenuItem menu_items_1132[] = {
    { " Clear Board", 12288, 1, 0 },
    { " Restore Board", 12290, 1, 0 },
    { " Done", 12291, 1, 0 },
    { 0, 0, 0, 0 },
};
Menu main_menus_114a[] = {
    { "Disk", menu_items_1066 },
    { "Move", menu_items_108a },
    { "Settings", menu_items_10a8 },
    { "Level", menu_items_10ea },
    { 0, 0 },
};
Menu alternate_menus_115e[] = {
    { "Setup Options", menu_items_1132 },
    { 0, 0 },
};
