typedef unsigned char Byte;
typedef struct {int kind,status,code,reserved,x,y,word6,word7,word8,word9;} DialogEvent;
extern void fill_8a96(char *,int,int);
extern char *strcpy(char *,const char *);
extern unsigned strlen(const char *);
extern void select_pattern_5b00(int),restore_region_58b0(int,int,int,int);
int prepare_game_name_d8b6(char *destination,const char *source)
{
 int a;
 fill_8a96(destination,15,32);
 strcpy(destination,source);
 a=strlen(destination);
 destination[a]=' ';
 return a;
}
int is_dialog_printable_d8f6(int key)
{
 if(key>=32 && key<=126)return 1;
 return 0;
}
void close_dialog_d90e(void)
{
 select_pattern_5b00(0);
 restore_region_58b0(12,66,51,148);
}
