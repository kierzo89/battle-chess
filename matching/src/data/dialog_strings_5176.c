typedef struct {
 char load[5];
 char separator[10];
 char done[5];
 char cancel[7];
 char filename[10];
 char active_cancel[7];
 char active_done[5];
 char inactive_cancel[7];
 char inactive_done[5];
} DialogStrings;
DialogStrings dialog_strings={
 "Load","---------","Done","Cancel","Chess.sav",
 "Cancel","Done","Cancel","Done"
};
